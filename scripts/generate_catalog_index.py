"""Generate public/catalog-index.json, data/catalog-index.json, and AI/Bot discovery artifacts (llms.txt, api/*.json)."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from validator_sanitizer import split_frontmatter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_APPS_DIR = PROJECT_ROOT / "content" / "apps"
PUBLIC_INDEX_PATH = PROJECT_ROOT / "public" / "catalog-index.json"
DATA_INDEX_PATH = PROJECT_ROOT / "data" / "catalog-index.json"
PUBLIC_LLMS_PATH = PROJECT_ROOT / "public" / "llms.txt"
PUBLIC_LLMS_FULL_PATH = PROJECT_ROOT / "public" / "llms-full.txt"
PUBLIC_API_CATALOG_PATH = PROJECT_ROOT / "public" / "api" / "catalog.json"
PUBLIC_API_CLUSTERS_PATH = PROJECT_ROOT / "public" / "api" / "clusters.json"
CLUSTERS_MANIFEST_PATH = PROJECT_ROOT / "data" / "clusters_manifest.json"
SITE_URL_PREFIX = "https://davanzokeoma.github.io/HubHum"


def build_catalog_index() -> list[dict[str, object]]:
    """Collect rich metadata for all published apps for UI, scouter dedupe, and MCP search."""
    entries: list[dict[str, object]] = []
    if not CONTENT_APPS_DIR.exists():
        return entries

    for md_path in sorted(CONTENT_APPS_DIR.glob("*.md")):
        meta, _ = split_frontmatter(md_path.read_text(encoding="utf-8"))
        source_url = str(meta.get("source_url") or "").strip()
        full_name = ""
        m = re.match(r"^https?://github\.com/([^/]+/[^/?#]+)", source_url, re.IGNORECASE)
        if m:
            full_name = m.group(1).lower()

        is_webapp = bool(meta.get("is_webapp"))
        stars = int(meta.get("stars") or 0)
        tier = str(meta.get("scouting_tier") or ("tier2_webapp" if is_webapp else "tier1_gui"))
        app_type = str(meta.get("app_type") or ("webapp" if is_webapp else ("cli" if tier == "tier3_powertool" else "desktop")))
        raw_tags = meta.get("tags") if isinstance(meta.get("tags"), list) else []
        tags = [str(t) for t in raw_tags[:2]]
        raw_i18n = meta.get("i18n") if isinstance(meta.get("i18n"), dict) else {}
        i18n_sums: dict[str, str] = {}
        for l_code in ("it", "es", "fr", "de"):
            blk = raw_i18n.get(l_code)
            if isinstance(blk, dict) and blk.get("summary"):
                i18n_sums[l_code] = str(blk["summary"])

        entries.append(
            {
                "slug": str(meta.get("slug") or md_path.stem),
                "name": str(meta.get("title") or md_path.stem),
                "tagline": str(meta.get("tagline") or ""),
                "repo_url": source_url.rstrip("/").lower(),
                "full_name": full_name,
                "category": str(meta.get("category") or "Productivity"),
                "tags": tags,
                "icon": str(meta.get("icon") or "/icons/hubhum.svg"),
                "is_webapp": is_webapp,
                "app_type": app_type,
                "operatingSystem": str(meta.get("operatingSystem") or "Windows, macOS, Linux"),
                "license": str(meta.get("license") or "Open Source License"),
                "stars": stars,
                "tier": tier,
                "summary": str(meta.get("summary") or ""),
                "i18n": i18n_sums,
                "download_url": str(meta.get("download_url") or meta.get("downloadUrl") or ""),
                "updated_at": str(meta.get("updated_at") or ""),
            }
        )
    entries.sort(key=lambda item: int(item.get("stars") or 0), reverse=True)
    return entries


def write_discovery_artifacts(entries: list[dict[str, object]]) -> None:
    """Write llms.txt, llms-full.txt, public/api/catalog.json, and public/api/clusters.json."""
    now_iso = datetime.now(timezone.utc).isoformat()
    tier_counts: dict[str, int] = {}
    type_counts: dict[str, int] = {}
    by_category: dict[str, list[dict[str, object]]] = {}

    for item in entries:
        t = str(item.get("tier") or "tier1_gui")
        at = str(item.get("app_type") or "desktop")
        cat = str(item.get("category") or "Productivity")
        tier_counts[t] = tier_counts.get(t, 0) + 1
        type_counts[at] = type_counts.get(at, 0) + 1
        by_category.setdefault(cat, []).append(item)

    clusters_data: dict[str, object] = {}
    if CLUSTERS_MANIFEST_PATH.exists():
        try:
            clusters_data = json.loads(CLUSTERS_MANIFEST_PATH.read_text(encoding="utf-8"))
        except Exception:
            clusters_data = {}

    # 1. Open JSON Catalog API
    api_catalog = {
        "schema_version": "1.1",
        "project": "HubHum — A Git Hub for Humans",
        "site_url": f"{SITE_URL_PREFIX}/",
        "generated_at": now_iso,
        "total_apps": len(entries),
        "tier_counts": tier_counts,
        "app_type_counts": type_counts,
        "categories": {k: len(v) for k, v in sorted(by_category.items())},
        "apps": entries,
    }
    PUBLIC_API_CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_API_CATALOG_PATH.write_text(json.dumps(api_catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 2. Open JSON Clusters API
    pillars_raw = clusters_data.get("pillars") if isinstance(clusters_data.get("pillars"), list) else []
    enriched_pillars = []
    for p in pillars_raw:
        if not isinstance(p, dict):
            continue
        subs = []
        for s in p.get("subpillars", []):
            if not isinstance(s, dict):
                continue
            subs.append(
                {
                    **s,
                    "url": f"{SITE_URL_PREFIX}/guides/{s.get('sub_slug', '')}/",
                    "article_urls": [f"{SITE_URL_PREFIX}/guides/{a}/" for a in s.get("articles", [])],
                }
            )
        enriched_pillars.append(
            {
                "macro_slug": p.get("macro_slug", ""),
                "category": p.get("category", ""),
                "app_count": p.get("app_count", 0),
                "url": f"{SITE_URL_PREFIX}/guides/{p.get('macro_slug', '')}/",
                "subpillars": subs,
            }
        )
    bundles_raw = clusters_data.get("bundles") if isinstance(clusters_data.get("bundles"), list) else []
    api_clusters = {
        "schema_version": "1.0",
        "generated_at": clusters_data.get("generated_at", now_iso),
        "total_guide_pages": clusters_data.get("total_guide_pages", 0),
        "pillars": enriched_pillars,
        "bundles": [
            {"slug": b, "url": f"{SITE_URL_PREFIX}/bundles/{b}/"} for b in bundles_raw
        ],
    }
    PUBLIC_API_CLUSTERS_PATH.write_text(json.dumps(api_clusters, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 3. Standard llms.txt concise index
    llms_lines = [
        "# HubHum — A Git Hub for Humans",
        "",
        "> Plain-English, verified directory of free and open-source software explained without developer jargon, pointing strictly to official GitHub releases and upstream creator channels.",
        "",
        f"Catalog Size: {len(entries)} open-source tools ({type_counts.get('desktop', 0)} Desktop GUI, {type_counts.get('selfhosted', 0)} Self-Hosted, {type_counts.get('cli', 0)} CLI/Power Tools, {type_counts.get('resource', 0)} Open References).",
        "",
        "## Primary Endpoints",
        f"- [Homepage & Interactive Catalog]({SITE_URL_PREFIX}/): Search and filter free software by format, OS, and everyday task",
        f"- [Full Plain-English Software Digest (RAG)]({SITE_URL_PREFIX}/llms-full.txt): Structured index of every app summarized by category",
        f"- [Open JSON Catalog API]({SITE_URL_PREFIX}/api/catalog.json): Machine-readable metadata for all {len(entries)} software cards",
        f"- [Topic Clusters & Bundles JSON API]({SITE_URL_PREFIX}/api/clusters.json): Hierarchical topic guide tree and curated starter bundles",
        f"- [RSS Feed]({SITE_URL_PREFIX}/feed.xml): Latest indexed software guides and category comparisons",
        f"- [About & Editorial Transparency]({SITE_URL_PREFIX}/about/): Methodology, official link verification policy, and #ad isolation",
        "",
        "## Topic Cluster Pillars (Main Guides)",
    ]
    for ep in enriched_pillars:
        llms_lines.append(
            f"- [{ep['category']} ({ep['app_count']} apps)]({ep['url']})"
        )
        for sub in ep.get("subpillars", []):
            llms_lines.append(
                f"  - [{sub.get('sub_topic')} ({sub.get('app_count')} apps)]({sub.get('url')})"
            )

    if bundles_raw:
        llms_lines.extend(["", "## Curated Software Bundles"])
        for b_slug in bundles_raw:
            llms_lines.append(f"- [{b_slug}]({SITE_URL_PREFIX}/bundles/{b_slug}/)")

    PUBLIC_LLMS_PATH.write_text("\n".join(llms_lines).strip() + "\n", encoding="utf-8")

    # 4. Complete llms-full.txt RAG catalog
    full_lines = [
        "# HubHum Complete Open-Source Catalog Digest",
        "",
        f"Generated: {now_iso} | Total Applications: {len(entries)}",
        "",
    ]
    for cat in sorted(by_category.keys()):
        cat_items = by_category[cat]
        full_lines.append(f"## {cat} ({len(cat_items)} apps)")
        full_lines.append("")
        for item in cat_items:
            slug = item["slug"]
            stars = int(item.get("stars") or 0)
            full_lines.append(
                f"- **{item['name']}** (`{item['app_type']}` | OS: {item['operatingSystem']} | License: {item['license']} | ★ {stars:,}): "
                f"{item['summary']} — Guide: {SITE_URL_PREFIX}/apps/{slug}/ | Source: {item['repo_url']}"
            )
        full_lines.append("")

    PUBLIC_LLMS_FULL_PATH.write_text("\n".join(full_lines).strip() + "\n", encoding="utf-8")


def write_catalog_index() -> Path:
    entries = build_catalog_index()
    payload = json.dumps(entries, ensure_ascii=False, indent=2) + "\n"
    for target in (PUBLIC_INDEX_PATH, DATA_INDEX_PATH):
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload, encoding="utf-8")
    write_discovery_artifacts(entries)
    print(f"[INDEX] Generated {PUBLIC_INDEX_PATH}, {DATA_INDEX_PATH}, llms.txt, llms-full.txt, and api/*.json ({len(entries)} apps)")
    return PUBLIC_INDEX_PATH


if __name__ == "__main__":
    write_catalog_index()
