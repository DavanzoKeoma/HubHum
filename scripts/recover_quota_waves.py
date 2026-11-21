"""Instant Multi-Tier Quota Audit & Streaming Batch Recovery for HubHum (500 Tier1 / 300 Tier2 / 200 Tier3)."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from generate_catalog_index import write_catalog_index
from scouter import (
    DAILY_TARGET_QUOTA,
    GITHUB_API_BASE,
    TIER_1_LIMIT,
    TIER_2_LIMIT,
    TIER_3_LIMIT,
    _github_get_json,
    _throttle_github_search,
    fetch_repo_bundle,
    is_consumer_repo,
    load_existing_catalog_state,
)
from seo_pipeline import AFFILIATES_PATH, BLOCKLIST_PATH, load_json_file, process_single_repo
from validator_sanitizer import split_frontmatter
from vault_loader import get_secret

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_APPS_DIR = PROJECT_ROOT / "content" / "apps"
GITHUB_DISPATCH_URL = "https://api.github.com/repos/DavanzoKeoma/HubHum/actions/workflows/seo-builder.yml/dispatches"

TIER_QUERY_SETS: dict[str, dict[str, object]] = {
    "tier1": {
        "tier_key": "tier1_gui",
        "min_stars": 500,
        "topics": (
            "gui",
            "desktop-app",
            "windows",
            "macos",
            "linux",
            "android",
            "ios",
            "video-editor",
            "password-manager",
            "audio-player",
            "markdown-editor",
            "note-taking",
            "screen-recorder",
            "media-player",
        ),
    },
    "tier2": {
        "tier_key": "tier2_webapp",
        "min_stars": 200,
        "topics": (
            "self-hosted",
            "cms",
            "web-app",
            "webapp",
            "saas",
            "dashboard",
            "docker",
            "analytics",
            "wiki",
            "bookmark-manager",
        ),
    },
    "tier3": {
        "tier_key": "tier3_powertool",
        "min_stars": 2000,
        "topics": (
            "cli",
            "terminal",
            "command-line",
            "utility",
            "automation",
            "productivity",
            "devtools",
            "developer-tools",
        ),
    },
}


def compute_catalog_status() -> dict:
    """Count current live apps by mutually exclusive Tier and AI provider fallback rate."""
    counts = {"tier1_gui": 0, "tier2_webapp": 0, "tier3_powertool": 0, "other": 0}
    providers = {"gemini": 0, "groq": 0, "unknown_or_manual": 0}
    files = sorted(CONTENT_APPS_DIR.glob("*.md"))

    for md_path in files:
        meta, _ = split_frontmatter(md_path.read_text(encoding="utf-8"))
        is_webapp = bool(meta.get("is_webapp"))
        raw_tier = str(meta.get("scouting_tier") or "").strip()
        tier = raw_tier if raw_tier in counts else ("tier2_webapp" if is_webapp else "tier1_gui")
        counts[tier] += 1

        ai_p = str(meta.get("ai_provider") or "").lower()
        if "gemini" in ai_p:
            providers["gemini"] += 1
        elif "groq" in ai_p:
            providers["groq"] += 1
        else:
            providers["unknown_or_manual"] += 1

    total = len(files)
    deltas = {
        "tier1_gui": max(TIER_1_LIMIT - counts["tier1_gui"], 0),
        "tier2_webapp": max(TIER_2_LIMIT - counts["tier2_webapp"], 0),
        "tier3_powertool": max(TIER_3_LIMIT - counts["tier3_powertool"], 0),
        "daily_total_delta": max(DAILY_TARGET_QUOTA - total, 0),
    }

    return {
        "total_apps": total,
        "daily_target": DAILY_TARGET_QUOTA,
        "tier_counts": counts,
        "tier_targets": {
            "tier1_gui": TIER_1_LIMIT,
            "tier2_webapp": TIER_2_LIMIT,
            "tier3_powertool": TIER_3_LIMIT,
        },
        "remaining_deltas": deltas,
        "ai_provider_breakdown": providers,
    }


def _atomic_git_commit(published_so_far: int, total_target: int) -> None:
    """Regenerate catalog indices and commit a 50-card batch atomically."""
    write_catalog_index()
    subprocess.run(
        [
            "git",
            "add",
            "content/apps",
            "public/icons",
            "public/catalog-index.json",
            "data/catalog-index.json",
            "data/retry_queue.json",
            "data/processed_repos.json",
            "data/daily_quota_state.json",
        ],
        cwd=PROJECT_ROOT,
        check=True,
    )
    diff_res = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=PROJECT_ROOT)
    if diff_res.returncode == 0:
        return
    msg = f"chore(seo): atomic batch commit {published_so_far}/{total_target} HubHum app cards"
    subprocess.run(["git", "commit", "-m", msg], cwd=PROJECT_ROOT, check=True)
    print(f"[ATOMIC COMMIT] {msg}", flush=True)


def execute_streaming_recovery(
    tier1_target: int,
    tier2_target: int,
    tier3_target: int,
    min_delay: float = 4.1,
    batch_commit_size: int = 50,
    commit_batches: bool = False,
    force_provider: str = "auto",
) -> dict:
    """Stream candidates topic-by-topic until exact Tier targets are published with 50-card atomic commits."""
    affiliates_data: dict = load_json_file(AFFILIATES_PATH, {})  # type: ignore[assignment]
    if not affiliates_data:
        raise FileNotFoundError(f"Missing affiliates file: {AFFILIATES_PATH}")

    blocklist_raw: dict = load_json_file(BLOCKLIST_PATH, {"blocked_slugs": []})  # type: ignore[assignment]
    blocklist = set(blocklist_raw.get("blocked_slugs", []))
    token = get_secret("dev.github", "pat", "GITHUB_TOKEN")

    known_slugs, known_repos = load_existing_catalog_state()
    tier_targets = [("tier1", tier1_target), ("tier2", tier2_target), ("tier3", tier3_target)]
    total_target = sum(t for _, t in tier_targets)

    published_by_tier = {"tier1": 0, "tier2": 0, "tier3": 0}
    total_published = 0
    since_last_commit = 0
    last_ai_ts = 0.0

    for tier_arg, target_count in tier_targets:
        if target_count <= 0:
            continue
        cfg = TIER_QUERY_SETS[tier_arg]
        tier_key = str(cfg["tier_key"])
        min_stars = int(cfg["min_stars"])
        topics: tuple[str, ...] = cfg["topics"]  # type: ignore[assignment]

        print(f"\n--- Streaming {tier_arg} ({tier_key}, target={target_count}, min_stars>{min_stars}) ---", flush=True)

        for topic in topics:
            if published_by_tier[tier_arg] >= target_count:
                break
            for page_num in (1, 2, 3, 4):
                if published_by_tier[tier_arg] >= target_count:
                    break
                _throttle_github_search()
                raw_q = f"topic:{topic} stars:>{min_stars} fork:false archived:false"
                encoded_q = urllib.parse.quote(raw_q)
                url = f"{GITHUB_API_BASE}/search/repositories?q={encoded_q}&sort=stars&order=desc&per_page=30&page={page_num}"
                try:
                    data = _github_get_json(url, token=token)
                except Exception as exc:
                    print(f"[SEARCH WARN] {topic} p{page_num}: {exc}", flush=True)
                    break

                items = data.get("items", [])
                if not items:
                    break

                for item in items:
                    if published_by_tier[tier_arg] >= target_count:
                        break
                    full_name = str(item.get("full_name") or "")
                    repo_name = str(item.get("name") or "")
                    slug = re.sub(r"[^a-z0-9-]+", "-", repo_name.lower()).strip("-")
                    if (
                        not full_name
                        or not slug
                        or slug in known_slugs
                        or slug in blocklist
                        or full_name.lower() in known_repos
                        or (CONTENT_APPS_DIR / f"{slug}.md").exists()
                    ):
                        continue
                    if not is_consumer_repo(item, min_stars=min_stars):
                        continue

                    known_slugs.add(slug)
                    known_repos.add(full_name.lower())

                    owner = item["owner"]["login"]
                    try:
                        bundle = fetch_repo_bundle(owner, repo_name, token=token, scouting_tier=tier_key)
                    except Exception:
                        continue

                    if tier_arg == "tier1":
                        if bundle.app_type in ("cli", "resource"):
                            continue
                        raw_topics = {t.lower() for t in (item.get("topics") or [])}
                        if not bundle.release_assets and not (
                            raw_topics & {"gui", "desktop-app", "windows", "macos", "android", "ios"}
                        ):
                            continue
                        bundle.is_webapp = False
                        bundle.app_type = "desktop"
                        bundle.scouting_tier = "tier1_gui"
                    elif tier_arg == "tier2":
                        bundle.is_webapp = True
                        bundle.app_type = "selfhosted"
                        bundle.category = "Web Apps & Cloud"
                        bundle.operating_system = "Self-Hosted / Browser"
                        bundle.scouting_tier = "tier2_webapp"
                    elif tier_arg == "tier3":
                        bundle.is_webapp = False
                        if bundle.app_type != "resource":
                            bundle.app_type = "cli"
                        bundle.scouting_tier = "tier3_powertool"
                        if bundle.category == "Graphics & Design":
                            bundle.category = "Utilities & Power Tools"

                    if last_ai_ts > 0 and min_delay > 0:
                        elapsed = time.monotonic() - last_ai_ts
                        if elapsed < min_delay:
                            time.sleep(min_delay - elapsed)
                    last_ai_ts = time.monotonic()

                    if process_single_repo(bundle, affiliates_data, blocklist, force_provider=force_provider):
                        published_by_tier[tier_arg] += 1
                        total_published += 1
                        since_last_commit += 1

                        if total_published % 10 == 0:
                            print(
                                f"[PROGRESS] {total_published}/{total_target} "
                                f"(tier1={published_by_tier['tier1']}/{tier1_target}, "
                                f"tier2={published_by_tier['tier2']}/{tier2_target}, "
                                f"tier3={published_by_tier['tier3']}/{tier3_target})",
                                flush=True,
                            )

                        if batch_commit_size > 0 and since_last_commit >= batch_commit_size:
                            if commit_batches:
                                _atomic_git_commit(total_published, total_target)
                            else:
                                write_catalog_index()
                            since_last_commit = 0

    if since_last_commit > 0:
        if commit_batches:
            _atomic_git_commit(total_published, total_target)
        else:
            write_catalog_index()

    return {
        "published_by_tier": published_by_tier,
        "total_published": total_published,
        "total_target": total_target,
    }


def dispatch_recovery_waves(wave_limit: int, tiers: tuple[str, ...] = ("tier1", "tier2", "tier3")) -> list[dict]:
    """Dispatch seo-builder.yml recovery runs on GitHub Actions for each specified tier."""
    token = get_secret("dev.github", "pat", "GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Missing GITHUB_TOKEN / dev.github pat for workflow dispatch.")

    dispatched = []
    for t in tiers:
        payload = json.dumps(
            {
                "ref": "main",
                "inputs": {
                    "tier": t,
                    "limit": str(wave_limit),
                    "force_provider": "auto",
                },
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            GITHUB_DISPATCH_URL,
            data=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "Content-Type": "application/json",
                "User-Agent": "HubHum-Recovery/1.0",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            dispatched.append({"tier": t, "limit": wave_limit, "http_status": resp.status})
    return dispatched


def main() -> int:
    parser = argparse.ArgumentParser(description="HubHum Instant Multi-Tier Quota Audit & Recovery")
    parser.add_argument("--status", action="store_true", help="Show current catalog counts, Tier split, and quota deltas")
    parser.add_argument("--execute-local", action="store_true", help="Run immediate local multi-tier recovery generation")
    parser.add_argument("--per-tier", type=int, default=0, help="Shorthand equal target per tier (overrides individual targets if > 0)")
    parser.add_argument("--tier1-target", type=int, default=75, help="Target new Tier 1 GUI apps")
    parser.add_argument("--tier2-target", type=int, default=45, help="Target new Tier 2 Web/Cloud apps")
    parser.add_argument("--tier3-target", type=int, default=30, help="Target new Tier 3 Power Tools/CLI")
    parser.add_argument("--min-delay", type=float, default=4.1, help="Minimum interval between AI calls (seconds)")
    parser.add_argument("--batch-commit-size", type=int, default=50, help="Rebuild index & commit atomically every N cards")
    parser.add_argument("--commit-batches", action="store_true", help="Create atomic git commits every batch_commit_size cards")
    parser.add_argument("--dispatch-waves", action="store_true", help="Trigger recovery waves via GitHub Actions workflow_dispatch")
    parser.add_argument("--wave-limit", type=int, default=15, help="Apps per dispatched GitHub Actions wave")
    parser.add_argument("--tiers", default="tier1,tier2,tier3", help="Comma-separated tiers to dispatch")
    args = parser.parse_args()

    if not any((args.status, args.execute_local, args.dispatch_waves)):
        args.status = True

    if args.status:
        print("=== CURRENT QUOTA STATUS ===")
        print(json.dumps(compute_catalog_status(), indent=2))

    if args.execute_local:
        t1 = args.per_tier if args.per_tier > 0 else args.tier1_target
        t2 = args.per_tier if args.per_tier > 0 else args.tier2_target
        t3 = args.per_tier if args.per_tier > 0 else args.tier3_target
        print(
            f"\n=== EXECUTING STREAMING MULTI-TIER RECOVERY "
            f"(tier1={t1}, tier2={t2}, tier3={t3}, batch_commit={args.batch_commit_size}) ==="
        )
        res = execute_streaming_recovery(
            tier1_target=t1,
            tier2_target=t2,
            tier3_target=t3,
            min_delay=args.min_delay,
            batch_commit_size=args.batch_commit_size,
            commit_batches=args.commit_batches,
        )
        print("Local recovery summary:", json.dumps(res))

    if args.dispatch_waves:
        tier_list = tuple(t.strip() for t in args.tiers.split(",") if t.strip())
        print(f"\n=== DISPATCHING RECOVERY WAVES ON GITHUB ACTIONS (limit={args.wave_limit}) ===")
        dispatched = dispatch_recovery_waves(wave_limit=args.wave_limit, tiers=tier_list)
        print("Dispatched:", json.dumps(dispatched))

    return 0


if __name__ == "__main__":
    sys.exit(main())
