"""Retroactive Data Hygiene & Taxonomy Remediation across all content/apps/*.md cards."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from generate_catalog_index import write_catalog_index
from scouter import (
    INSTALLER_EXTENSIONS,
    PROCESSED_REPOS_PATH,
    classify_app_type_and_category,
    humanize_license,
    sanitize_human_tags,
)
from seo_pipeline import AFFILIATES_PATH, _derive_application_category, clean_complete_summary
from validator_sanitizer import (
    is_summary_truncated,
    relocate_affiliate_links_to_sponsored_section,
    split_frontmatter,
    validate_directory,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_APPS_DIR = PROJECT_ROOT / "content" / "apps"


def _strip_markdown_for_summary(raw_text: str) -> str:
    """Remove Markdown links and (#ad) disclosures when extracting fallback summary prose."""
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", raw_text)
    cleaned = re.sub(r"\(#ad\)", "", cleaned, flags=re.IGNORECASE)
    return " ".join(cleaned.split()).strip()


def _escape_yaml_str(val: object) -> str:
    s = str(val or "").replace("\r", " ").replace("\n", " ").replace('"', "'")
    # Decode literal \uXXXX escapes if any older card stored escaped ASCII unicode
    if "\\u" in s:
        try:
            s = s.encode("utf-8").decode("unicode_escape")
        except Exception:
            pass
    return " ".join(s.split()).replace('"', "'").strip()


def _serialize_card(meta: dict[str, object], body: str) -> str:
    """Serialize remediated metadata back into canonical YAML frontmatter + body."""
    tags_list = meta.get("tags") if isinstance(meta.get("tags"), list) else ["productivity"]
    tags_yaml = ", ".join(f'"{_escape_yaml_str(t).lower()}"' for t in tags_list[:5])

    ordered_keys = [
        "title",
        "slug",
        "tagline",
        "summary",
        "tags",
        "is_webapp",
        "app_type",
        "category",
        "icon",
        "stars",
        "source_url",
        "download_url",
        "downloadUrl",
        "download_label",
        "license",
        "scouting_tier",
        "operatingSystem",
        "applicationCategory",
        "fileSize",
        "priceCurrency",
        "price",
        "affiliate_merchant_id",
        "affiliate_name",
        "affiliate_url",
        "affiliate_pitch",
        "ai_provider",
        "featured_weekly",
        "updated_at",
    ]

    lines = ["---"]
    for key in ordered_keys:
        if key not in meta or meta[key] is None or meta[key] == "":
            continue
        val = meta[key]
        if key == "tags":
            lines.append(f"tags: [{tags_yaml}]")
        elif isinstance(val, bool):
            lines.append(f"{key}: {str(val).lower()}")
        elif isinstance(val, int):
            lines.append(f"{key}: {val}")
        else:
            lines.append(f'{key}: "{_escape_yaml_str(val)}"')

    raw_i18n = meta.get("i18n")
    if isinstance(raw_i18n, dict):
        lines.append("i18n:")
        for lang in ("it", "es", "fr", "de"):
            block = raw_i18n.get(lang)
            if isinstance(block, dict):
                lines.append(f"  {lang}:")
                if block.get("tagline"):
                    lines.append(f'    tagline: "{_escape_yaml_str(block["tagline"])}"')
                if block.get("summary"):
                    lines.append(f'    summary: "{_escape_yaml_str(block["summary"])}"')

    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.strip() + "\n"


def remediate_all() -> dict[str, object]:
    """Run deterministic taxonomy, honest app_type, license cleanup, and #ad isolation across all cards."""
    files = sorted(CONTENT_APPS_DIR.glob("*.md"))
    affiliates_data: dict = {}
    if AFFILIATES_PATH.exists():
        affiliates_data = json.loads(AFFILIATES_PATH.read_text(encoding="utf-8"))
    aff_cats: dict = affiliates_data.get("categories") or {}

    stats: dict[str, object] = {
        "total_scanned": len(files),
        "updated_files": 0,
        "repaired_summaries": 0,
        "repaired_i18n_summaries": 0,
        "reclassified_categories": 0,
        "isolated_sponsored_sections": 0,
        "by_app_type": {"desktop": 0, "webapp": 0, "selfhosted": 0, "cli": 0, "resource": 0},
        "by_category": {},
    }
    processed_slugs: list[str] = []
    processed_full_names: list[str] = []
    processed_urls: list[str] = []

    for md_path in files:
        raw_text = md_path.read_text(encoding="utf-8")
        meta, body = split_frontmatter(raw_text)
        before_snapshot = json.dumps(meta, ensure_ascii=False, sort_keys=True)
        before_body = body.strip()

        slug = str(meta.get("slug") or md_path.stem).strip()
        title = str(meta.get("title") or slug).strip()
        source_url = str(meta.get("source_url") or "").strip()
        dl_url = str(meta.get("download_url") or meta.get("downloadUrl") or "").strip()
        current_tier = str(meta.get("scouting_tier") or "").strip()
        old_cat = str(meta.get("category") or "Productivity").strip()
        old_summary = str(meta.get("summary") or "").strip()

        if slug:
            processed_slugs.append(slug.lower())
        if source_url:
            processed_urls.append(source_url.rstrip("/").lower())
            m_fn = re.match(r"^https?://github\.com/([^/]+/[^/?#]+)", source_url, re.IGNORECASE)
            if m_fn:
                processed_full_names.append(m_fn.group(1).lower())

        has_installer = dl_url.lower().endswith(INSTALLER_EXTENSIONS)

        # Extract plain-English paragraph for both classification fallback & summary repair
        match_intro = re.search(r"### What it does in plain English\s+([^\n#]+)", body)
        intro_clean = _strip_markdown_for_summary(match_intro.group(1) if match_intro else "")
        fallback_prose = intro_clean or old_summary or f"{title} is a free open-source tool."

        if is_summary_truncated(old_summary):
            source_for_fix = intro_clean if len(intro_clean) >= 35 else old_summary
            fixed_sum = clean_complete_summary(source_for_fix, fallback_prose, max_len=210)
            if is_summary_truncated(fixed_sum):
                fixed_sum = clean_complete_summary(fallback_prose, f"{title} simplifies everyday work without technical jargon.", max_len=210)
            meta["summary"] = fixed_sum
            stats["repaired_summaries"] = int(stats["repaired_summaries"]) + 1

        # Repair truncated localized summaries
        raw_i18n = meta.get("i18n")
        if isinstance(raw_i18n, dict):
            for lang in ("it", "es", "fr", "de"):
                block = raw_i18n.get(lang)
                if isinstance(block, dict) and block.get("summary"):
                    l_sum = str(block.get("summary") or "").strip()
                    if is_summary_truncated(l_sum):
                        block["summary"] = clean_complete_summary(l_sum, str(meta.get("summary") or fallback_prose), max_len=210)
                        stats["repaired_i18n_summaries"] = int(stats["repaired_i18n_summaries"]) + 1

        raw_tags = [str(t) for t in (meta.get("tags") or [])]
        app_type, new_cat, new_tier, new_is_webapp, aff_key = classify_app_type_and_category(
            slug=slug,
            title=title,
            description=str(meta.get("summary") or "") + " " + intro_clean[:250],
            topics=raw_tags,
            readme=body[:800],
            has_desktop_installer=has_installer,
            current_tier=current_tier,
        )

        # Preserve explicit Web App designation for native browser tools like HubHum
        if slug == "hubhum":
            app_type, new_cat, new_tier, new_is_webapp, aff_key = "webapp", "Web Apps & Cloud", "tier2_webapp", True, "webapp_cms"

        if new_cat != old_cat:
            stats["reclassified_categories"] = int(stats["reclassified_categories"]) + 1

        meta["app_type"] = app_type
        meta["category"] = new_cat
        meta["scouting_tier"] = new_tier
        meta["is_webapp"] = new_is_webapp
        meta["applicationCategory"] = _derive_application_category(new_cat)
        meta["tags"] = sanitize_human_tags(raw_tags, category=new_cat, app_type=app_type)
        meta["license"] = humanize_license(str(meta.get("license") or ""))

        cur_dl_label = str(meta.get("download_label") or "")
        if app_type == "resource":
            meta["download_label"] = "Browse Reference →"
        elif app_type == "selfhosted" and not has_installer:
            meta["download_label"] = "Official Setup & Docs →"
        elif app_type == "cli" and (
            "checksums" in dl_url.lower()
            or cur_dl_label.startswith("Download (checksums")
            or cur_dl_label == "Visit Official Site"
        ):
            meta["download_label"] = "Get Command-Line Tool →"

        if app_type == "webapp":
            meta["operatingSystem"] = "Browser / Online"
        elif app_type == "selfhosted":
            meta["operatingSystem"] = "Self-Hosted / Browser"
        elif app_type == "resource":
            meta["operatingSystem"] = "All / Reference"
        else:
            cur_os = str(meta.get("operatingSystem") or "Windows, macOS, Linux")
            has_android_signal = (
                dl_url.lower().endswith(".apk")
                or any("android" in str(t).lower() for t in raw_tags)
                or "android" in f"{title} {meta.get('summary', '')}".lower()
            )
            if cur_os == "All / Browser":
                meta["operatingSystem"] = "Windows, macOS, Linux"
            elif ("Android" in cur_os and (app_type == "cli" or not has_android_signal)):
                cleaned_oses = [o.strip() for o in cur_os.split(",") if o.strip() and o.strip() != "Android"]
                meta["operatingSystem"] = ", ".join(cleaned_oses) if cleaned_oses else "Windows, macOS, Linux"

        # Isolate all #ad partner links strictly inside ### Sponsored Partner Tools (#ad) AND align frontmatter merchant
        cat_block = aff_cats.get(aff_key) or aff_cats.get("productivity_utilities") or aff_cats.get("webapp_cms") or {}
        merchants_by_id = affiliates_data.get("merchants_by_id") or {}
        primary_id = str(cat_block.get("primary_merchant_id") or "")
        cat_merchants_list = cat_block.get("merchants") or []
        pm_override = next((m for m in cat_merchants_list if m.get("merchant_id") == primary_id), None)
        if primary_id and (pm_override or primary_id in merchants_by_id):
            pm = pm_override or merchants_by_id[primary_id]
            meta["affiliate_merchant_id"] = pm.get("merchant_id", primary_id)
            meta["affiliate_name"] = pm.get("name", meta.get("affiliate_name", ""))
            meta["affiliate_url"] = pm.get("tracking_url", meta.get("affiliate_url", ""))
            meta["affiliate_pitch"] = str(cat_block.get("injection_message") or meta.get("affiliate_pitch", "")).replace('"', "'")
        triplet = cat_block.get("recommended_triplet") or []
        new_body = relocate_affiliate_links_to_sponsored_section(body, triplet=triplet).strip()
        if "### Sponsored Partner Tools (#ad)" in new_body:
            stats["isolated_sponsored_sections"] = int(stats["isolated_sponsored_sections"]) + 1

        by_type = stats["by_app_type"]  # type: ignore[assignment]
        by_type[app_type] = int(by_type.get(app_type, 0)) + 1
        by_cat = stats["by_category"]  # type: ignore[assignment]
        by_cat[new_cat] = int(by_cat.get(new_cat, 0)) + 1

        after_snapshot = json.dumps(meta, ensure_ascii=False, sort_keys=True)
        if before_snapshot != after_snapshot or before_body != new_body:
            md_path.write_text(_serialize_card(meta, new_body), encoding="utf-8")
            stats["updated_files"] = int(stats["updated_files"]) + 1

    # Write persistent anti-duplication cache
    PROCESSED_REPOS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED_REPOS_PATH.write_text(
        json.dumps(
            {
                "slugs": sorted(set(processed_slugs)),
                "full_names": sorted(set(processed_full_names)),
                "repo_urls": sorted(set(processed_urls)),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    write_catalog_index()
    return stats


if __name__ == "__main__":
    summary = remediate_all()
    print("=== REMEDIATION SUMMARY ===")
    print(json.dumps(summary, indent=2))
    exit_code = validate_directory(CONTENT_APPS_DIR)
    print(f"=== VALIDATOR EXIT CODE: {exit_code} ===")
    sys.exit(exit_code)
