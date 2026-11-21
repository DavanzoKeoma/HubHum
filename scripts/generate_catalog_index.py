"""Generate public/catalog-index.json and data/catalog-index.json from content/apps/*.md."""

from __future__ import annotations

import json
import re
from pathlib import Path

from validator_sanitizer import split_frontmatter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_APPS_DIR = PROJECT_ROOT / "content" / "apps"
PUBLIC_INDEX_PATH = PROJECT_ROOT / "public" / "catalog-index.json"
DATA_INDEX_PATH = PROJECT_ROOT / "data" / "catalog-index.json"


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

        entries.append(
            {
                "slug": str(meta.get("slug") or md_path.stem),
                "name": str(meta.get("title") or md_path.stem),
                "repo_url": source_url.rstrip("/").lower(),
                "full_name": full_name,
                "category": str(meta.get("category") or "Productivity"),
                "icon": str(meta.get("icon") or "/icons/hubhum.svg"),
                "is_webapp": is_webapp,
                "app_type": app_type,
                "stars": stars,
                "tier": tier,
                "summary": str(meta.get("summary") or ""),
                "download_url": str(meta.get("download_url") or meta.get("downloadUrl") or ""),
                "updated_at": str(meta.get("updated_at") or ""),
            }
        )
    return entries


def write_catalog_index() -> Path:
    entries = build_catalog_index()
    payload = json.dumps(entries, ensure_ascii=False, indent=2) + "\n"
    for target in (PUBLIC_INDEX_PATH, DATA_INDEX_PATH):
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload, encoding="utf-8")
    print(f"[INDEX] Generated {PUBLIC_INDEX_PATH} and {DATA_INDEX_PATH} ({len(entries)} apps)")
    return PUBLIC_INDEX_PATH


if __name__ == "__main__":
    write_catalog_index()
