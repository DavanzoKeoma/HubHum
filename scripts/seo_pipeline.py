"""HubHum Programmatic SEO Pipeline (Nightly Scouting + Single-URL Async Translation)."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from ai_router import AllTiersFailedError, generate_card_with_cascade
from scouter import ScoutedRepo, classify_repo, fetch_repo_by_url, scout_trending_consumer_apps
from validator_sanitizer import sanitize_full_document, split_frontmatter, validate_markdown_card

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
    """Pick the top-priority merchant matching the repository category."""
    _, _, aff_cat_key = classify_repo(repo.description, repo.topics, repo.readme_excerpt, repo.release_assets)
    cat_block = affiliates_data.get("categories", {}).get(aff_cat_key) or affiliates_data["categories"]["webapp_cms"]
    primary_id = cat_block["primary_merchant_id"]
    merchant = affiliates_data["merchants_by_id"][primary_id]
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
    }


def enrich_frontmatter(markdown_text: str, repo: ScoutedRepo, aff: dict) -> str:
    """Merge UI & affiliate metadata fields into generated Markdown frontmatter."""
    meta, body = split_frontmatter(markdown_text)

    # Extract first sentence of "Cos'è in parole semplici" as summary if needed
    summary = repo.description.strip()
    match_intro = re.search(r"### Cos'è in parole semplici\s+([^\n#]+)", body)
    if match_intro:
        summary = match_intro.group(1).strip()

    tags_list = meta.get("tags") if isinstance(meta.get("tags"), list) else (repo.topics[:3] or ["utilità"])
    tags_yaml = ", ".join(f'"{str(t).lower()}"' for t in tags_list[:5])
    safe_title = str(meta.get("title") or repo.name).replace('"', "'")
    safe_summary = summary.replace('"', "'")[:240]
    safe_pitch = aff["injection_message"].replace('"', "'")
    today = datetime.now(timezone.utc).date().isoformat()

    frontmatter = "\n".join(
        [
            "---",
            f'title: "{safe_title}"',
            f'slug: "{repo.slug}"',
            f"tags: [{tags_yaml}]",
            f"is_webapp: {str(repo.is_webapp).lower()}",
            f'category: "{repo.category}"',
            f'summary: "{safe_summary}"',
            f"stars: {repo.stars}",
            f'source_url: "{repo.html_url}"',
            f'download_url: "{repo.primary_download_url}"',
            f'download_label: "{repo.primary_download_label}"',
            f'license: "{repo.license_id}"',
            f'affiliate_merchant_id: "{aff["merchant_id"]}"',
            f'affiliate_name: "{aff["merchant_name"]}"',
            f'affiliate_url: "{aff["tracking_url"]}"',
            f'affiliate_pitch: "{safe_pitch}"',
            "featured_weekly: true",
            f'updated_at: "{today}"',
            "---",
        ]
    )
    return sanitize_full_document(f"{frontmatter}\n\n{body}\n")


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


def process_single_repo(repo: ScoutedRepo, affiliates_data: dict, blocklist: set[str]) -> bool:
    """Translate, validate, sanitize, and write one app card. Returns True if written."""
    if repo.slug in blocklist:
        print(f"[SKIP] {repo.slug} è nella takedown blocklist.")
        return False

    aff = select_affiliate_for_repo(repo, affiliates_data)
    try:
        raw_card, tier_used = generate_card_with_cascade(repo, aff)
        final_card = enrich_frontmatter(raw_card, repo, aff)
        errs = validate_markdown_card(final_card, allowed_urls=repo.allowed_urls, strict_urls=True)
        if errs:
            raise AllTiersFailedError(f"Post-enrichment validation error: {errs}")
        out_path = CONTENT_APPS_DIR / f"{repo.slug}.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(final_card, encoding="utf-8")
        print(f"[PUBLISHED] {out_path.name} via {tier_used}")
        return True
    except AllTiersFailedError as exc:
        print(f"[QUEUED] {repo.full_name}: {exc}")
        enqueue_retry(repo, str(exc))
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="HubHum SEO Pipeline")
    parser.add_argument("--limit", type=int, default=15, help="Numero massimo di nuove app da elaborare")
    parser.add_argument("--repo-url", help="URL GitHub singolo per traduzione asincrona")
    args = parser.parse_args()

    affiliates_data: dict = load_json_file(AFFILIATES_PATH, {})  # type: ignore[assignment]
    if not affiliates_data:
        raise FileNotFoundError(f"File affiliazioni mancante: {AFFILIATES_PATH}")

    blocklist_raw: dict = load_json_file(BLOCKLIST_PATH, {"blocked_slugs": []})  # type: ignore[assignment]
    blocklist = set(blocklist_raw.get("blocked_slugs", []))

    if args.repo_url:
        repo = fetch_repo_by_url(args.repo_url)
        process_single_repo(repo, affiliates_data, blocklist)
        return

    repos = scout_trending_consumer_apps(limit=args.limit)
    published = 0
    for repo in repos:
        target = CONTENT_APPS_DIR / f"{repo.slug}.md"
        if target.exists():
            continue
        if process_single_repo(repo, affiliates_data, blocklist):
            published += 1
    print(f"Pipeline completata: {published} nuove schede generate.")


if __name__ == "__main__":
    main()
