"""HubHum Programmatic SEO Pipeline (Nightly Scouting + Single/Multi-URL Async Translation)."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from ai_router import AllTiersFailedError, generate_card_with_cascade
from generate_catalog_index import write_catalog_index
from scouter import ScoutedRepo, classify_repo, fetch_repo_by_url, scout_tiered_apps
from validator_sanitizer import ensure_triplet_links_in_body, sanitize_full_document, split_frontmatter, validate_markdown_card

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_APPS_DIR = PROJECT_ROOT / "content" / "apps"
AFFILIATES_PATH = PROJECT_ROOT / "data" / "affiliates_seed.json"
RETRY_QUEUE_PATH = PROJECT_ROOT / "data" / "retry_queue.json"
BLOCKLIST_PATH = PROJECT_ROOT / "data" / "takedown_blocklist.json"


def load_json_file(path: Path, default: object) -> object:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json_file(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def select_affiliate_for_repo(repo: ScoutedRepo, affiliates_data: dict) -> dict:
    """Pick the top-priority merchant and 3-link contextual triplet matching the repository category."""
    _, _, aff_cat_key = classify_repo(repo.description, repo.topics, repo.readme_excerpt, repo.release_assets)
    cat_block = affiliates_data.get("categories", {}).get(aff_cat_key) or affiliates_data["categories"]["webapp_cms"]
    primary_id = cat_block["primary_merchant_id"]
    merchant = affiliates_data["merchants_by_id"][primary_id]
    triplet = cat_block.get("recommended_triplet") or []
    return {
        "category_key": aff_cat_key,
        "category_label": cat_block["label"],
        "injection_message": cat_block["injection_message"],
        "cta_label": cat_block["cta_label"],
        "merchant_id": merchant["merchant_id"],
        "merchant_name": merchant["name"],
        "tracking_url": merchant["tracking_url"],
        "subid": merchant["subid"],
        "disclosure_text": merchant["disclosure_text"],
        "recommended_triplet": triplet,
    }


def _clean_sentence(text: str, fallback: str) -> str:
    cleaned = " ".join(str(text or "").replace('"', "'").split()).rstrip(".")
    if not cleaned:
        cleaned = fallback.rstrip(".")
    return f"{cleaned}."


def _commit_batch(batch_count: int) -> None:
    """Persist intermediate batches to git atomically every N cards so long runs never lose progress."""
    subprocess.run(
        [
            "git",
            "add",
            "content/apps",
            "public/icons",
            "public/catalog-index.json",
            "data/catalog-index.json",
            "data/retry_queue.json",
        ],
        cwd=PROJECT_ROOT,
        check=False,
    )
    diff_res = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=PROJECT_ROOT)
    if diff_res.returncode == 0:
        return
    subprocess.run(
        ["git", "commit", "-m", f"chore(seo): batch commit {batch_count} HubHum app cards"],
        cwd=PROJECT_ROOT,
        check=False,
    )
    subprocess.run(["git", "pull", "--rebase", "origin", "main"], cwd=PROJECT_ROOT, check=False)
    subprocess.run(["git", "push", "origin", "main"], cwd=PROJECT_ROOT, check=False)


def _derive_application_category(category: str) -> str:
    mapping = {
        "Security & Privacy": "SecurityApplication",
        "Video & Audio": "MultimediaApplication",
        "Graphics & Design": "DesignApplication",
        "Web Apps & Cloud": "BusinessApplication",
        "Websites & SEO": "DeveloperApplication",
        "Productivity": "UtilitiesApplication",
    }
    return mapping.get(category, "UtilitiesApplication")


def enrich_frontmatter(markdown_text: str, repo: ScoutedRepo, aff: dict, provider_used: str) -> str:
    """Merge UI, icon, i18n, AI provider, and affiliate metadata fields into YAML frontmatter."""
    meta, body = split_frontmatter(markdown_text)

    fallback_summary = repo.description.strip() or f"{repo.name} is a free open-source application."
    match_intro = re.search(r"### What it does in plain English\s+([^\n#]+)", body)
    raw_summary = str(meta.get("summary") or (match_intro.group(1) if match_intro else fallback_summary))
    if len(raw_summary) > 155:
        first_sent = raw_summary.split(".")[0].strip()
        raw_summary = first_sent if 40 <= len(first_sent) <= 155 else raw_summary[:150].rsplit(" ", 1)[0]
    safe_summary = _clean_sentence(raw_summary, fallback_summary)
    safe_tagline = str(meta.get("tagline") or repo.category).replace('"', "'")[:65]

    tags_list = meta.get("tags") if isinstance(meta.get("tags"), list) else (repo.topics[:3] or ["utility"])
    tags_yaml = ", ".join(f'"{str(t).lower()}"' for t in tags_list[:5])
    safe_title = str(meta.get("title") or repo.name).replace('"', "'")
    safe_pitch = aff["injection_message"].replace('"', "'")
    today = datetime.now(timezone.utc).date().isoformat()

    raw_i18n = meta.get("i18n") if isinstance(meta.get("i18n"), dict) else {}
    i18n_lines = ["i18n:"]
    for lang in ("it", "es", "fr", "de"):
        lang_obj = raw_i18n.get(lang) if isinstance(raw_i18n.get(lang), dict) else {}
        l_tag = str(lang_obj.get("tagline") or safe_tagline).replace('"', "'")
        l_sum = _clean_sentence(str(lang_obj.get("summary") or safe_summary), safe_summary)
        i18n_lines.append(f"  {lang}:")
        i18n_lines.append(f'    tagline: "{l_tag}"')
        i18n_lines.append(f'    summary: "{l_sum}"')

    frontmatter = "\n".join(
        [
            "---",
            f'title: "{safe_title}"',
            f'slug: "{repo.slug}"',
            f'tagline: "{safe_tagline}"',
            f'summary: "{safe_summary}"',
            f"tags: [{tags_yaml}]",
            f"is_webapp: {str(repo.is_webapp).lower()}",
            f'category: "{repo.category}"',
            f'icon: "{repo.icon_path}"',
            f"stars: {repo.stars}",
            f'source_url: "{repo.html_url}"',
            f'download_url: "{repo.primary_download_url}"',
            f'downloadUrl: "{repo.primary_download_url}"',
            f'download_label: "{repo.primary_download_label}"',
            f'license: "{repo.license_id}"',
            f'scouting_tier: "{repo.scouting_tier}"',
            f'operatingSystem: "{repo.operating_system}"',
            f'applicationCategory: "{_derive_application_category(repo.category)}"',
            'priceCurrency: "USD"',
            'price: "0"',
            f'affiliate_merchant_id: "{aff["merchant_id"]}"',
            f'affiliate_name: "{aff["merchant_name"]}"',
            f'affiliate_url: "{aff["tracking_url"]}"',
            f'affiliate_pitch: "{safe_pitch}"',
            f'ai_provider: "{provider_used}"',
            "featured_weekly: true",
            f'updated_at: "{today}"',
            *i18n_lines,
            "---",
        ]
    )
    enriched_body = ensure_triplet_links_in_body(body, aff.get("recommended_triplet") or [])
    return sanitize_full_document(f"{frontmatter}\n\n{enriched_body}\n")


def enqueue_retry(repo: ScoutedRepo, reason: str) -> None:
    queue: list[dict] = load_json_file(RETRY_QUEUE_PATH, [])  # type: ignore[assignment]
    if any(item.get("html_url") == repo.html_url for item in queue):
        return
    queue.append(
        {
            "full_name": repo.full_name,
            "slug": repo.slug,
            "html_url": repo.html_url,
            "reason": reason,
            "queued_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    save_json_file(RETRY_QUEUE_PATH, queue)


def dequeue_retry(slug: str) -> None:
    queue: list[dict] = load_json_file(RETRY_QUEUE_PATH, [])  # type: ignore[assignment]
    filtered = [item for item in queue if item.get("slug") != slug]
    if len(filtered) != len(queue):
        save_json_file(RETRY_QUEUE_PATH, filtered)


def process_single_repo(
    repo: ScoutedRepo,
    affiliates_data: dict,
    blocklist: set[str],
    force_provider: str = "auto",
) -> bool:
    """Translate, validate, sanitize, and write one app card. Returns True if written."""
    if repo.slug in blocklist:
        print(f"[SKIP] {repo.slug} is in takedown blocklist.")
        return False

    aff = select_affiliate_for_repo(repo, affiliates_data)
    try:
        raw_card, tier_used = generate_card_with_cascade(repo, aff, force_provider=force_provider)
        final_card = enrich_frontmatter(raw_card, repo, aff, provider_used=tier_used)
        errs = validate_markdown_card(final_card, allowed_urls=repo.allowed_urls, strict_urls=True)
        if errs:
            raise AllTiersFailedError(f"Post-enrichment validation error: {errs}")
        out_path = CONTENT_APPS_DIR / f"{repo.slug}.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(final_card, encoding="utf-8")
        dequeue_retry(repo.slug)
        print(f"[PUBLISHED] {out_path.name} via {tier_used} (merchant={aff['merchant_id']})")
        return True
    except AllTiersFailedError as exc:
        print(f"[QUEUED] {repo.full_name}: {exc}")
        enqueue_retry(repo, str(exc))
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="HubHum 3-Tier SEO Pipeline")
    parser.add_argument("--limit", type=int, default=250, help="Max nightly apps to process in this wave")
    parser.add_argument(
        "--tier",
        choices=["all", "tier1", "tier2", "tier3", "trending"],
        default="all",
        help="Target scouting tier (500 Tier1 / 300 Tier2 / 200 Tier3)",
    )
    parser.add_argument(
        "--min-delay",
        type=float,
        default=4.1,
        help="Minimum pause (seconds) between consecutive AI requests to stay below 15 RPM",
    )
    parser.add_argument(
        "--batch-commit-size",
        type=int,
        default=50,
        help="Rebuild catalog index and checkpoint-commit every N newly generated cards",
    )
    parser.add_argument(
        "--auto-git-push",
        action="store_true",
        help="Automatically commit and push intermediate checkpoints during large batch runs",
    )
    parser.add_argument("--repo-url", "--single-repo", dest="repo_url", help="Single GitHub URL for async translation")
    parser.add_argument("--repo-urls", help="Comma-separated GitHub URLs (bypasses star threshold)")
    parser.add_argument(
        "--force-provider",
        choices=["auto", "gemini", "groq", "both"],
        default="auto",
        help="Select AI provider",
    )
    args = parser.parse_args()

    affiliates_data: dict = load_json_file(AFFILIATES_PATH, {})  # type: ignore[assignment]
    if not affiliates_data:
        raise FileNotFoundError(f"Missing affiliates file: {AFFILIATES_PATH}")

    blocklist_raw: dict = load_json_file(BLOCKLIST_PATH, {"blocked_slugs": []})  # type: ignore[assignment]
    blocklist = set(blocklist_raw.get("blocked_slugs", []))

    explicit_urls: list[str] = []
    if args.repo_url and args.repo_url.strip():
        explicit_urls.append(args.repo_url.strip())
    if args.repo_urls and args.repo_urls.strip():
        for raw_u in args.repo_urls.split(","):
            u = raw_u.strip()
            if u and u not in explicit_urls:
                explicit_urls.append(u)

    if explicit_urls:
        published = 0
        for idx, repo_u in enumerate(explicit_urls):
            if idx > 0 and args.min_delay > 0:
                time.sleep(args.min_delay)
            provider = args.force_provider
            if args.force_provider == "both":
                provider = "groq" if idx == len(explicit_urls) - 1 and len(explicit_urls) > 1 else "gemini"
            repo = fetch_repo_by_url(repo_u)
            if process_single_repo(repo, affiliates_data, blocklist, force_provider=provider):
                published += 1
        if published > 0:
            write_catalog_index()
        print(f"Explicit pipeline complete: {published}/{len(explicit_urls)} cards generated.")
        if published == 0:
            raise SystemExit(2)
        return

    repos = scout_tiered_apps(limit=args.limit, tier=args.tier)
    published = 0
    since_last_checkpoint = 0
    for idx, repo in enumerate(repos):
        target = CONTENT_APPS_DIR / f"{repo.slug}.md"
        if target.exists():
            continue
        if idx > 0 and args.min_delay > 0:
            time.sleep(args.min_delay)
        provider = (
            "gemini"
            if args.force_provider == "both" and idx % 2 == 0
            else ("groq" if args.force_provider == "both" else args.force_provider)
        )
        if process_single_repo(repo, affiliates_data, blocklist, force_provider=provider):
            published += 1
            since_last_checkpoint += 1
            if args.batch_commit_size > 0 and since_last_checkpoint >= args.batch_commit_size:
                write_catalog_index()
                if args.auto_git_push:
                    _commit_batch(published)
                since_last_checkpoint = 0

    if published > 0:
        write_catalog_index()
    print(f"Pipeline complete (tier={args.tier}): {published} new cards generated.")


if __name__ == "__main__":
    main()
