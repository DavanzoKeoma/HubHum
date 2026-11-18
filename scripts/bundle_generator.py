"""Monthly Bundle Pages generator when a tag reaches threshold (Workflow 7)."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from validator_sanitizer import sanitize_full_document, split_frontmatter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_APPS_DIR = PROJECT_ROOT / "content" / "apps"
CONTENT_BUNDLES_DIR = PROJECT_ROOT / "content" / "bundles"


def generate_bundles(threshold: int = 50) -> int:
    """Group app cards by tag and generate English bundle guides when count >= threshold."""
    CONTENT_BUNDLES_DIR.mkdir(parents=True, exist_ok=True)
    by_tag: dict[str, list[dict]] = {}

    for md_path in sorted(CONTENT_APPS_DIR.glob("*.md")):
        meta, _ = split_frontmatter(md_path.read_text(encoding="utf-8"))
        for tag in meta.get("tags") or []:  # type: ignore[union-attr]
            tag_key = str(tag).lower()
            by_tag.setdefault(tag_key, []).append(meta)

    created = 0
    today = datetime.now(timezone.utc).date().isoformat()
    for tag_key, apps in sorted(by_tag.items()):
        if len(apps) < threshold:
            continue
        bundle_slug = f"best-free-{tag_key}-apps"
        out_path = CONTENT_BUNDLES_DIR / f"{bundle_slug}.md"
        top_apps = sorted(apps, key=lambda x: int(x.get("stars") or 0), reverse=True)[:5]
        slugs_yaml = ", ".join(f'"{a["slug"]}"' for a in top_apps)

        bullets = "\n".join(
            f"- **[{a['title']}](/HubHum/apps/{a['slug']})**: {a.get('summary', 'Free open-source tool.')}"
            for a in top_apps
        )
        doc = f"""---
title: "Top {len(top_apps)} Free Alternatives for {tag_key}"
slug: "{bundle_slug}"
category: "Curated Guides"
summary: "Monthly selection of the best free and easy-to-use programs in the {tag_key} category."
tags: ["{tag_key}", "collection"]
app_slugs: [{slugs_yaml}]
updated_at: "{today}"
---

### Why this guide
We curated the strongest free solutions for **{tag_key}**, explaining in plain English what each program does and how to start right away with zero subscription fees.

### Top picks this month
{bullets}

### Partner tip (#ad)
Explore the recommended tools inside each app card to launch cloud apps in one click or keep your connection protected.
"""
        out_path.write_text(sanitize_full_document(doc), encoding="utf-8")
        created += 1
        print(f"[BUNDLE] Generated {out_path.name} ({len(top_apps)} apps)")

    print(f"Bundle generation complete: {created} bundles created (threshold={threshold}).")
    return created


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HubHum Bundle Generator")
    parser.add_argument("--threshold", type=int, default=50, help="Minimum apps per tag")
    args = parser.parse_args()
    generate_bundles(threshold=args.threshold)
