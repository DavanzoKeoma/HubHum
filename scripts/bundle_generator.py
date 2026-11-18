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
    """Group app cards by tag and generate bundle guides when count >= threshold."""
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
        bundle_slug = f"migliori-app-{tag_key}"
        out_path = CONTENT_BUNDLES_DIR / f"{bundle_slug}.md"
        top_apps = sorted(apps, key=lambda x: int(x.get("stars") or 0), reverse=True)[:5]
        slugs_yaml = ", ".join(f'"{a["slug"]}"' for a in top_apps)

        bullets = "\n".join(
            f"- **[{a['title']}](/apps/{a['slug']})**: {a.get('summary', 'Strumento open-source gratuito.')}"
            for a in top_apps
        )
        doc = f"""---
title: "Le {len(top_apps)} migliori alternative gratuite per {tag_key}"
slug: "{bundle_slug}"
category: "Raccolte Guidate"
summary: "Selezione mensile dei migliori programmi gratuiti e facili da usare per la categoria {tag_key}."
tags: ["{tag_key}", "raccolta"]
app_slugs: [{slugs_yaml}]
updated_at: "{today}"
---

### Perché questa raccolta
Abbiamo selezionato le migliori soluzioni gratuite dedicate a **{tag_key}**, spiegando in parole semplici cosa fanno e come iniziare subito senza costi di abbonamento.

### Le scelte migliori di questo mese
{bullets}

### Consiglio extra (#ad)
Per proteggere i tuoi dati online o velocizzare il lavoro creativo e web, consulta le soluzioni consigliate all'interno delle singole schede.
"""
        out_path.write_text(sanitize_full_document(doc), encoding="utf-8")
        created += 1
        print(f"[BUNDLE] Generato {out_path.name} ({len(top_apps)} app)")

    print(f"Generazione raccolte completata: {created} bundle creati (soglia={threshold}).")
    return created


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HubHum Bundle Generator")
    parser.add_argument("--threshold", type=int, default=50, help="Numero minimo di app per tag")
    args = parser.parse_args()
    generate_bundles(threshold=args.threshold)
