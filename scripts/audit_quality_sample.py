"""Qualitative & Compliance Audit across the 1,250-app HubHum catalog (+250 post-rebase focus)."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from validator_sanitizer import is_summary_truncated, split_frontmatter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_APPS_DIR = PROJECT_ROOT / "content" / "apps"
CONTENT_GUIDES_DIR = PROJECT_ROOT / "content" / "guides"
CONTENT_BUNDLES_DIR = PROJECT_ROOT / "content" / "bundles"
DEFAULT_REPORT_PATH = PROJECT_ROOT / "data" / "quality_audit_report.json"

TRAILING_OPEN_PREP_RE = re.compile(
    r"\b(?:or|and|of|instead of|from your|from the|from a|with a|with the|with your|to the|to a|for the|for a|for your|into a|into the|via a|without a|without your|that your|than a)\.$",
    re.IGNORECASE,
)
RAW_JARGON_RE = re.compile(
    r"\b(?:node-based workflow engine|workflow node-based engine|CLI wrapper for|wrapper CLI per LLM|AST parser|binary-level analysis)\b",
    re.IGNORECASE,
)
MERCHANT_SUBID_RE = re.compile(r"hubhum_01_MER(\d+)", re.IGNORECASE)
DUPLICATE_FREE_RE = re.compile(r"\b(Free)\s+\1\b", re.IGNORECASE)

WP_SEO_MERCHANTS = {"MER_276", "MER_265", "MER_269", "MER_023", "MER_141", "MER_192"}
VPN_MERCHANTS = {"MER_089", "MER_064", "MER_048"}


def _get_commit_app_files(commit_sha: str) -> set[str]:
    """Return content/apps/*.md filenames introduced in a specific commit if reachable."""
    try:
        res = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_sha, "--", "content/apps/"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return {Path(line.strip()).name for line in res.stdout.splitlines() if line.strip().endswith(".md")}
    except Exception:
        return set()


def _extract_section_slice(body: str, heading: str) -> str:
    pattern = re.compile(rf"(?:^|\n)###\s+{re.escape(heading)}\s*\n(.*?)(?=\n###\s+|\n\*\*Official Source|\Z)", re.DOTALL)
    m = pattern.search(body)
    return m.group(1).strip() if m else ""


def _audit_single_card(md_path: Path) -> dict[str, object]:
    raw_text = md_path.read_text(encoding="utf-8")
    meta, body = split_frontmatter(raw_text)

    slug = str(meta.get("slug") or md_path.stem)
    title = str(meta.get("title") or slug)
    category = str(meta.get("category") or "Productivity")
    app_type = str(meta.get("app_type") or ("webapp" if meta.get("is_webapp") else "desktop"))
    is_webapp = bool(meta.get("is_webapp"))
    scouting_tier = str(meta.get("scouting_tier") or "")
    license_str = str(meta.get("license") or "").strip()
    os_str = str(meta.get("operatingSystem") or "").strip()
    summary = str(meta.get("summary") or "").strip()
    tagline = str(meta.get("tagline") or "").strip()

    issues: list[str] = []

    # 1. Plain-English, zero-jargon & truncation checks
    plain_section = _extract_section_slice(body, "What it does in plain English")
    if is_summary_truncated(summary) or TRAILING_OPEN_PREP_RE.search(summary):
        issues.append(f"truncated_or_open_summary: {summary[-40:]}")
    if TRAILING_OPEN_PREP_RE.search(tagline):
        issues.append(f"open_prep_tagline: {tagline[-40:]}")
    if plain_section and TRAILING_OPEN_PREP_RE.search(plain_section.splitlines()[0]):
        issues.append("open_prep_plain_english")
    if RAW_JARGON_RE.search(f"{summary} {plain_section}"):
        issues.append("raw_unexplained_jargon")
    if DUPLICATE_FREE_RE.search(f"{title} {summary} {tagline}"):
        issues.append("duplicate_free_word")

    # 2. #ad Confinement & Affiliate Matrix pertinence
    editorial_sections = (
        "What it does in plain English",
        "Who it's for",
        "Key features",
        "How to install",
        "Pros and Cons",
    )
    for sec_name in editorial_sections:
        sec_text = _extract_section_slice(body, sec_name)
        if MERCHANT_SUBID_RE.search(sec_text) or "(#ad)" in sec_text.lower():
            issues.append(f"ad_leak_in_{sec_name.lower().replace(' ', '_')}")

    sponsored_block = _extract_section_slice(body, "Sponsored Partner Tools (#ad)")
    found_subids = [f"MER_{m}" for m in MERCHANT_SUBID_RE.findall(sponsored_block)]
    distinct_subids = list(dict.fromkeys(found_subids))
    if not sponsored_block:
        issues.append("missing_sponsored_section")
    elif len(distinct_subids) != 3:
        issues.append(f"invalid_subid_count:{len(distinct_subids)}")

    # Cross-domain merchant check
    all_body_subids = {f"MER_{m}" for m in MERCHANT_SUBID_RE.findall(body)}
    fm_merchant = str(meta.get("affiliate_merchant_id") or "")
    if fm_merchant:
        all_body_subids.add(fm_merchant)
    if category in {"Video & Audio", "Graphics & Design", "Security & Privacy"} and (all_body_subids & WP_SEO_MERCHANTS):
        issues.append(f"cross_domain_wp_on_{category}")
    if category == "Graphics & Design" and (all_body_subids & VPN_MERCHANTS):
        issues.append("cross_domain_vpn_on_graphics")

    # 3. Format warning triggers & license humanization
    if not license_str or "NOASSERTION" in license_str.upper():
        issues.append(f"raw_or_missing_license:{license_str}")
    if app_type == "cli" and is_webapp:
        issues.append("cli_marked_as_webapp")
    if app_type == "selfhosted":
        if not is_webapp:
            issues.append("selfhosted_not_marked_is_webapp")
        if os_str != "Self-Hosted / Browser":
            issues.append(f"selfhosted_unexpected_os:{os_str}")

    # 4. Multilingual localization (IT, ES, FR, DE)
    raw_i18n = meta.get("i18n") if isinstance(meta.get("i18n"), dict) else {}
    for lang in ("it", "es", "fr", "de"):
        blk = raw_i18n.get(lang)
        if isinstance(blk, dict):
            lsum = str(blk.get("summary") or "").strip()
            ltag = str(blk.get("tagline") or "").strip()
            if lsum and (is_summary_truncated(lsum) or TRAILING_OPEN_PREP_RE.search(lsum)):
                issues.append(f"truncated_i18n_{lang}_summary")
            if DUPLICATE_FREE_RE.search(f"{ltag} {lsum}"):
                issues.append(f"duplicate_free_i18n_{lang}")

    return {
        "file": md_path.name,
        "slug": slug,
        "category": category,
        "app_type": app_type,
        "scouting_tier": scouting_tier,
        "license": license_str,
        "distinct_subids": distinct_subids,
        "issues": issues,
    }


def _build_stratified_sample(records: list[dict[str, object]], target_size: int = 75) -> list[dict[str, object]]:
    by_cat: dict[str, list[dict[str, object]]] = {}
    for rec in records:
        by_cat.setdefault(str(rec["category"]), []).append(rec)
    picked: list[dict[str, object]] = []
    seen: set[str] = set()
    round_idx = 0
    cats = sorted(by_cat.keys())
    while len(picked) < target_size and cats:
        added_any = False
        for c in cats:
            if round_idx < len(by_cat[c]):
                item = by_cat[c][round_idx]
                f = str(item["file"])
                if f not in seen:
                    picked.append(item)
                    seen.add(f)
                    added_any = True
                if len(picked) >= target_size:
                    break
        if not added_any:
            break
        round_idx += 1
    return picked


def run_audit(rebase_commit: str = "b7ccf21", sample_size: int = 75, output_path: Path = DEFAULT_REPORT_PATH) -> dict[str, object]:
    app_files = sorted(CONTENT_APPS_DIR.glob("*.md"))
    post_rebase_names = _get_commit_app_files(rebase_commit)

    all_records = [_audit_single_card(p) for p in app_files]
    stratified = _build_stratified_sample(all_records, target_size=sample_size)
    post_rebase_records = [r for r in all_records if str(r["file"]) in post_rebase_names]

    issue_counter: Counter[str] = Counter()
    flagged_cards: list[dict[str, object]] = []
    category_counts: Counter[str] = Counter()
    type_counts: Counter[str] = Counter()
    tier_counts: Counter[str] = Counter()

    for rec in all_records:
        category_counts[str(rec["category"])] += 1
        type_counts[str(rec["app_type"])] += 1
        tier_counts[str(rec["scouting_tier"])] += 1
        rec_issues = list(rec["issues"])  # type: ignore[arg-type]
        if rec_issues:
            flagged_cards.append({"file": rec["file"], "category": rec["category"], "issues": rec_issues})
            for iss in rec_issues:
                issue_counter[iss.split(":")[0]] += 1

    # Also check guide & bundle headings for 'Free Free'
    heading_issues: list[str] = []
    for folder in (CONTENT_GUIDES_DIR, CONTENT_BUNDLES_DIR):
        if folder.exists():
            for md_p in sorted(folder.rglob("*.md")):
                txt = md_p.read_text(encoding="utf-8")
                if DUPLICATE_FREE_RE.search(txt):
                    heading_issues.append(md_p.relative_to(PROJECT_ROOT).as_posix())

    post_rebase_flagged = [r for r in post_rebase_records if r["issues"]]
    report: dict[str, object] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_catalog_cards": len(all_records),
        "post_rebase_commit": rebase_commit,
        "post_rebase_cards_checked": len(post_rebase_records),
        "post_rebase_flagged_count": len(post_rebase_flagged),
        "stratified_sample_size": len(stratified),
        "stratified_sample_flagged": sum(1 for r in stratified if r["issues"]),
        "global_flagged_cards_count": len(flagged_cards),
        "issue_breakdown": dict(issue_counter),
        "category_distribution": dict(sorted(category_counts.items())),
        "app_type_distribution": dict(sorted(type_counts.items())),
        "tier_distribution": dict(sorted(tier_counts.items())),
        "guide_bundle_duplicate_word_headings": heading_issues,
        "flagged_cards_preview": flagged_cards[:30],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="HubHum Qualitative & Compliance Catalog Audit")
    parser.add_argument("--rebase-commit", default="b7ccf21", help="Commit SHA to isolate post-rebase batch")
    parser.add_argument("--sample-size", type=int, default=75, help="Stratified sample target size")
    parser.add_argument("--output", default=str(DEFAULT_REPORT_PATH), help="Output JSON report path")
    args = parser.parse_args()

    report = run_audit(rebase_commit=args.rebase_commit, sample_size=args.sample_size, output_path=Path(args.output))
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
