"""Generate a read-only curated report of Awesome-list submission candidates.

This script operates strictly locally from data/catalog-index.json and
data/clusters_manifest.json without making external requests or automated PRs.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_INDEX_PATH = PROJECT_ROOT / "data" / "catalog-index.json"
CLUSTERS_MANIFEST_PATH = PROJECT_ROOT / "data" / "clusters_manifest.json"
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "data" / "awesome_candidates.json"
SITE_URL_PREFIX = "https://davanzokeoma.github.io/HubHum"
REPO_URL = "https://github.com/DavanzoKeoma/HubHum"

AWESOME_TARGETS = [
    {
        "list_name": "awesome-selfhosted",
        "fit_reason": "300 validated Self-Hosted & Web Apps (Docker/web panels) with official upstream source links and zero-fork curation.",
        "recommended_entry": f"- [HubHum Self-Hosted Catalog]({SITE_URL_PREFIX}/guides/web-apps-cloud/) - Plain-English directory covering 300+ self-hosted web applications with direct source links (`MIT`).",
    },
    {
        "list_name": "awesome-open-source / free-software",
        "fit_reason": "1,000 validated non-forked OSS tools across Desktop GUI (500), Self-Hosted (300), and CLI (200) explained without developer jargon.",
        "recommended_entry": f"- [HubHum]({REPO_URL}) - Curated plain-English directory of 1,000 free & open-source apps built with Astro (`MIT`, `llms.txt` & OpenAPI ready).",
    },
    {
        "list_name": "awesome-privacy",
        "fit_reason": "Dedicated Security & Privacy pillar with password managers, VPN clients, local-first notes, and transparent privacy policy.",
        "recommended_entry": f"- [HubHum Privacy Guides]({SITE_URL_PREFIX}/guides/security-privacy/) - Plain-English open-source security & privacy tools directory with strict upstream download links.",
    },
    {
        "list_name": "awesome-astro",
        "fit_reason": "Static Astro SSG site compiling 1,081 pages (Content Collections, Schema.org SoftwareApplication/SoftwareSourceCode, RSS, OpenAPI, llms.txt).",
        "recommended_entry": f"- [HubHum]({REPO_URL}) - Open-source software directory statically built with Astro SSG indexing 1,000+ GitHub projects across 5 languages.",
    },
    {
        "list_name": "awesome-llms-txt / rag-directories",
        "fit_reason": "Full AI/RAG suite: /llms.txt, /llms-full.txt, /catalog-rag.txt, /codebase-full.txt, /.well-known/ai-plugin.json, and /api/openapi.yaml.",
        "recommended_entry": f"- [HubHum AI & RAG Endpoints]({SITE_URL_PREFIX}/llms.txt) - Complete machine-readable index and OpenAPI 3.0 spec for 1,000 open-source tools.",
    },
]


def build_awesome_report(top_per_category: int = 8) -> dict[str, object]:
    """Assemble verified Awesome-list candidates and highest-starred guides per category."""
    if not DATA_INDEX_PATH.exists():
        raise FileNotFoundError(f"Missing catalog index: {DATA_INDEX_PATH}")

    catalog = json.loads(DATA_INDEX_PATH.read_text(encoding="utf-8"))
    clusters = (
        json.loads(CLUSTERS_MANIFEST_PATH.read_text(encoding="utf-8"))
        if CLUSTERS_MANIFEST_PATH.exists()
        else {}
    )

    by_category: dict[str, list[dict[str, object]]] = {}
    for entry in catalog:
        cat = str(entry.get("category") or "Productivity")
        by_category.setdefault(cat, []).append(entry)

    category_highlights: dict[str, list[dict[str, object]]] = {}
    for cat, items in sorted(by_category.items()):
        ranked = sorted(
            (i for i in items if str(i.get("license") or "") and str(i.get("license")) != "NOASSERTION"),
            key=lambda x: int(x.get("stars") or 0),
            reverse=True,
        )[:top_per_category]
        formatted = []
        for item in ranked:
            slug = str(item.get("slug") or "")
            name = str(item.get("name") or slug)
            repo_url = str(item.get("repo_url") or "")
            summary = str(item.get("summary") or "").strip()
            guide_url = f"{SITE_URL_PREFIX}/apps/{slug}/"
            formatted.append(
                {
                    "slug": slug,
                    "name": name,
                    "stars": int(item.get("stars") or 0),
                    "app_type": item.get("app_type"),
                    "license": item.get("license"),
                    "repo_url": repo_url,
                    "hubhum_url": guide_url,
                    "awesome_markdown": f"- [{name}]({repo_url}) - {summary} ([Plain-English Guide]({guide_url}))",
                }
            )
        category_highlights[cat] = formatted

    pillars_out = []
    for p in clusters.get("pillars", []):
        macro_slug = str(p.get("macro_slug") or "")
        pillars_out.append(
            {
                "category": p.get("category"),
                "app_count": p.get("app_count"),
                "url": f"{SITE_URL_PREFIX}/guides/{macro_slug}/",
                "subpillar_count": len(p.get("subpillars", [])),
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_catalog_apps": len(catalog),
        "total_guide_pages": int(clusters.get("total_guide_pages") or 0),
        "total_bundles": len(clusters.get("bundles", [])),
        "submission_policy": "Read-only manual review artifact; submit only after verifying target repository contribution rules (no unsolicited automated PRs).",
        "target_awesome_lists": AWESOME_TARGETS,
        "pillar_guides": pillars_out,
        "top_candidates_by_category": category_highlights,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare Awesome-list submission candidates locally")
    parser.add_argument("--top", type=int, default=8, help="Top apps per category to highlight")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PATH), help="Output JSON report path")
    args = parser.parse_args()

    report = build_awesome_report(top_per_category=args.top)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        rel_out = out_path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()
    except ValueError:
        rel_out = out_path.name
    print(
        f"[AWESOME REPORT] Wrote {rel_out} "
        f"({report['total_catalog_apps']} apps, {len(report['target_awesome_lists'])} list templates, "
        f"{len(report['top_candidates_by_category'])} categories)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
