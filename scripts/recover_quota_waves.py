"""Instant Multi-Tier Quota Audit & Recovery Dispatcher for HubHum (500 Tier1 / 300 Tier2 / 200 Tier3)."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

from generate_catalog_index import write_catalog_index
from scouter import (
    DAILY_TARGET_QUOTA,
    TIER_1_LIMIT,
    TIER_2_LIMIT,
    TIER_3_LIMIT,
    scout_tiered_apps,
)
from seo_pipeline import BLOCKLIST_PATH, AFFILIATES_PATH, load_json_file, process_single_repo
from validator_sanitizer import split_frontmatter
from vault_loader import get_secret

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_APPS_DIR = PROJECT_ROOT / "content" / "apps"
GITHUB_DISPATCH_URL = "https://api.github.com/repos/DavanzoKeoma/HubHum/actions/workflows/seo-builder.yml/dispatches"


def compute_catalog_status() -> dict:
    """Count current live apps by Tier and AI provider fallback rate."""
    counts = {"tier1_gui": 0, "tier2_webapp": 0, "tier3_powertool": 0, "other": 0}
    providers = {"gemini": 0, "groq": 0, "unknown_or_manual": 0}
    files = sorted(CONTENT_APPS_DIR.glob("*.md"))

    for md_path in files:
        meta, _ = split_frontmatter(md_path.read_text(encoding="utf-8"))
        is_webapp = bool(meta.get("is_webapp"))
        tier = str(meta.get("scouting_tier") or ("tier2_webapp" if is_webapp else "tier1_gui"))
        if tier in counts:
            counts[tier] += 1
        else:
            counts["other"] += 1

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


def execute_local_recovery(per_tier: int, min_delay: float, force_provider: str = "auto") -> dict:
    """Run an immediate multi-tier batch recovery locally, respecting RPM and Search API limits."""
    affiliates_data: dict = load_json_file(AFFILIATES_PATH, {})  # type: ignore[assignment]
    if not affiliates_data:
        raise FileNotFoundError(f"Missing affiliates file: {AFFILIATES_PATH}")

    blocklist_raw: dict = load_json_file(BLOCKLIST_PATH, {"blocked_slugs": []})  # type: ignore[assignment]
    blocklist = set(blocklist_raw.get("blocked_slugs", []))

    summary = {"tier1": 0, "tier2": 0, "tier3": 0}
    ai_calls = 0

    for tier_arg in ("tier1", "tier2", "tier3"):
        repos = scout_tiered_apps(limit=per_tier, tier=tier_arg)
        for repo in repos:
            target = CONTENT_APPS_DIR / f"{repo.slug}.md"
            if target.exists():
                continue
            if ai_calls > 0 and min_delay > 0:
                time.sleep(min_delay)
            ai_calls += 1
            if process_single_repo(repo, affiliates_data, blocklist, force_provider=force_provider):
                summary[tier_arg] += 1

    if sum(summary.values()) > 0:
        write_catalog_index()
    return summary


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
    parser.add_argument("--per-tier", type=int, default=2, help="Number of new apps per tier for local recovery")
    parser.add_argument("--min-delay", type=float, default=4.1, help="Pause between LLM calls (seconds)")
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
        print(f"\n=== EXECUTING LOCAL MULTI-TIER RECOVERY (per_tier={args.per_tier}) ===")
        res = execute_local_recovery(per_tier=args.per_tier, min_delay=args.min_delay)
        print("Local recovery summary:", json.dumps(res))

    if args.dispatch_waves:
        tier_list = tuple(t.strip() for t in args.tiers.split(",") if t.strip())
        print(f"\n=== DISPATCHING RECOVERY WAVES ON GITHUB ACTIONS (limit={args.wave_limit}) ===")
        dispatched = dispatch_recovery_waves(wave_limit=args.wave_limit, tiers=tier_list)
        print("Dispatched:", json.dumps(dispatched))

    return 0


if __name__ == "__main__":
    sys.exit(main())
