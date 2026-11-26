"""Retroactively synchronize affiliate URLs and SubIDs across all content/apps/*.md cards (Workflow 2)."""

from __future__ import annotations

import json
import re
from pathlib import Path

from validator_sanitizer import split_frontmatter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_APPS_DIR = PROJECT_ROOT / "content" / "apps"
AFFILIATES_PATH = PROJECT_ROOT / "data" / "affiliates_seed.json"


def sync_affiliates() -> int:
    """Update affiliate_url and inline markdown links when data/affiliates_seed.json changes."""
    seed = json.loads(AFFILIATES_PATH.read_text(encoding="utf-8"))
    merchants_by_id = seed.get("merchants_by_id", {})
    valid_urls_by_mid: dict[str, set[str]] = {}
    for mid_k, m_obj in merchants_by_id.items():
        if m_obj.get("tracking_url"):
            valid_urls_by_mid.setdefault(mid_k, set()).add(str(m_obj["tracking_url"]))
    for cat_obj in (seed.get("categories") or {}).values():
        for m_obj in (cat_obj.get("merchants") or []) + (cat_obj.get("recommended_triplet") or []):
            mk = str(m_obj.get("merchant_id") or "")
            tu = str(m_obj.get("tracking_url") or "")
            if mk and tu:
                valid_urls_by_mid.setdefault(mk, set()).add(tu)

    updated_count = 0

    for md_path in sorted(CONTENT_APPS_DIR.glob("*.md")):
        raw = md_path.read_text(encoding="utf-8")
        meta, _ = split_frontmatter(raw)
        mid = str(meta.get("affiliate_merchant_id") or "")
        old_url = str(meta.get("affiliate_url") or "")
        merchant = merchants_by_id.get(mid)
        if not merchant:
            continue

        new_url = merchant["tracking_url"]
        if not new_url or old_url == new_url or old_url in valid_urls_by_mid.get(mid, set()):
            continue

        updated = raw
        if old_url:
            updated = updated.replace(old_url, new_url)
        updated = re.sub(
            r'^affiliate_url:\s*"[^"]*"',
            f'affiliate_url: "{new_url}"',
            updated,
            flags=re.MULTILINE,
        )
        if updated != raw:
            md_path.write_text(updated, encoding="utf-8")
            updated_count += 1
            print(f"[SYNCED] {md_path.name} -> {mid} ({merchant['subid']})")

    print(f"Sincronizzazione affiliazioni completata: {updated_count} schede aggiornate.")
    return updated_count


if __name__ == "__main__":
    sync_affiliates()
