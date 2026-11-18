"""Generate public/catalog-index.json from content/apps/*.md for instant client-side lookup."""

from __future__ import annotations

import json
import re
from pathlib import Path

from validator_sanitizer import split_frontmatter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_APPS_DIR = PROJECT_ROOT / "content" / "apps"
OUTPUT_PATH = PROJECT_ROOT / "public" / "catalog-index.json"


def build_catalog_index() -> list[dict[str, str]]:
    """Collect lightweight slug/name/repo_url metadata for all published apps."""
    entries: list[dict[str, str]] = []
    if not CONTENT_APPS_DIR.exists():
        return entries

    for md_path in sorted(CONTENT_APPS_DIR.glob("*.md")):
        meta, _ = split_frontmatter(md_path.read_text(encoding="utf-8"))
        source_url = str(meta.get("source_url") or "").strip()
        full_name = ""
        m = re.match(r"^https?://github\.com/([^/]+/[^/?#]+)", source_url, re.IGNORECASE)
        if m:
            full_name = m.group(1).lower()
        entries.append(
            {
                "slug": str(meta.get("slug") or md_path.stem),
                "name": str(meta.get("title") or md_path.stem),
                "repo_url": source_url.rstrip("/").lower(),
                "full_name": full_name,
                "category": str(meta.get("category") or "Productivity"),
                "icon": str(meta.get("icon") or "/icons/hubhum.svg"),
            }
        )
    return entries


def write_catalog_index() -> Path:
    entries = build_catalog_index()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[INDEX] Generated {OUTPUT_PATH} ({len(entries)} apps)")
    return OUTPUT_PATH


if __name__ == "__main__":
    write_catalog_index()
