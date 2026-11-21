"""Validation and Brand Safety / Zero-Jargon sanitization for HubHum English + i18n Markdown cards."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_APPS_DIR = PROJECT_ROOT / "content" / "apps"
AFFILIATES_PATH = PROJECT_ROOT / "data" / "affiliates_seed.json"

SPONSORED_HEADING = "### Sponsored Partner Tools (#ad)"

REQUIRED_HEADINGS = (
    "### What it does in plain English",
    "### Who it's for",
    "### Key features",
    "### How to install (Download)",
    "### Pros and Cons",
    SPONSORED_HEADING,
)

TRUNCATED_ENDING_WORDS = (
    "or", "and", "with", "without", "to", "for", "from", "in", "on", "at", "by",
    "of", "as", "into", "like", "than", "that", "which", "who", "a", "an", "the",
    "your", "their", "its", "heavy", "modern", "simple", "free", "using", "via",
    "over", "under", "between", "through", "such", "while", "during", "across",
    # IT / ES / FR / DE dangling stopwords
    "o", "e", "con", "senza", "per", "da", "su", "di", "il", "lo", "la", "i", "gli", "le", "un", "una",
    "y", "sin", "para", "por", "de", "el", "los", "las", "ou", "et", "avec", "sans", "pour", "par",
    "sur", "dans", "les", "une", "oder", "und", "mit", "ohne", "für", "von", "zu", "auf", "der", "die", "das", "ein", "eine",
)

TRUNCATED_SUMMARY_RE = re.compile(
    r"\b(?:" + "|".join(re.escape(w) for w in TRUNCATED_ENDING_WORDS) + r")\.$",
    re.IGNORECASE,
)


def is_summary_truncated(summary: str) -> bool:
    """Return True if a summary ends mid-thought on ellipsis or a dangling stopword."""
    s = str(summary or "").strip()
    if not s:
        return True
    if s.endswith("...") or s.endswith("…"):
        return True
    if s[-1] not in ".!?":
        return True
    return bool(TRUNCATED_SUMMARY_RE.search(s))

TRADEMARK_REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\b(?:the\s+)?killer\s+of\s+[A-Z0-9][A-Za-z0-9\s.+_-]{1,30}", re.IGNORECASE), "a free alternative to commercial software"),
    (re.compile(r"\bAdobe\s+Premiere(?:\s+Pro)?\b", re.IGNORECASE), "commercial video editors"),
    (re.compile(r"\bPremiere\s+Pro\b", re.IGNORECASE), "commercial video editors"),
    (re.compile(r"\bFinal\s+Cut(?:\s+Pro)?\b", re.IGNORECASE), "proprietary video editing software"),
    (re.compile(r"\bAdobe\s+Photoshop\b", re.IGNORECASE), "proprietary photo editors"),
    (re.compile(r"\bPhotoshop\b", re.IGNORECASE), "proprietary photo editors"),
    (re.compile(r"\bAdobe\s+Illustrator\b", re.IGNORECASE), "paid vector graphics software"),
    (re.compile(r"\bMicrosoft\s+Office\b", re.IGNORECASE), "commercial office suites"),
    (re.compile(r"\b1Password\b", re.IGNORECASE), "subscription password managers"),
    (re.compile(r"\bLastPass\b", re.IGNORECASE), "commercial password managers"),
    (re.compile(r"\bWordPress\.com\b", re.IGNORECASE), "closed publishing platforms"),
]

JARGON_REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bpull\s+requests?\b", re.IGNORECASE), "suggested update"),
    (re.compile(r"\brepositories\b", re.IGNORECASE), "project pages"),
    (re.compile(r"\brepository\b", re.IGNORECASE), "official project page"),
    (re.compile(r"\bcommits\b", re.IGNORECASE), "updates"),
    (re.compile(r"\bcommit\b", re.IGNORECASE), "update"),
    (re.compile(r"\bdeploy(?:ment|ing|ed)?\b", re.IGNORECASE), "cloud setup"),
    (re.compile(r"\bframeworks?\b", re.IGNORECASE), "software foundation"),
]


def _parse_yaml_scalar(val: str) -> object:
    val = val.strip()
    if val in ("true", "false"):
        return val == "true"
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        if not inner:
            return []
        return [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
    if re.fullmatch(r"\d+", val):
        return int(val)
    return val.strip('"').strip("'")


def split_frontmatter(markdown_text: str) -> tuple[dict[str, object], str]:
    """Parse lightweight YAML frontmatter (including nested i18n map) and return (data, body)."""
    normalized = markdown_text.replace("\r\n", "\n").strip()
    normalized = re.sub(r"^---[ \t]*\n", "---\n", normalized)
    if not normalized.startswith("---\n"):
        raise ValueError("Missing YAML frontmatter at start of file.")
    parts = re.split(r"\n---[ \t]*\n", normalized, maxsplit=1)
    if len(parts) != 2:
        raise ValueError("YAML frontmatter not closed with '---'.")

    header_raw = parts[0][4:]
    body = parts[1].strip()
    meta: dict[str, object] = {}
    current_top_map: str | None = None
    current_sub_map: str | None = None

    for raw_line in header_raw.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()
        if ":" not in stripped:
            continue
        key, val = stripped.split(":", 1)
        key = key.strip()
        val = val.strip()

        if indent == 0:
            current_sub_map = None
            if not val:
                meta[key] = {}
                current_top_map = key
            else:
                meta[key] = _parse_yaml_scalar(val)
                current_top_map = None
        elif indent == 2 and current_top_map and isinstance(meta.get(current_top_map), dict):
            top_dict = meta[current_top_map]  # type: ignore[assignment]
            if not val:
                top_dict[key] = {}
                current_sub_map = key
            else:
                top_dict[key] = _parse_yaml_scalar(val)
                current_sub_map = None
        elif indent >= 4 and current_top_map and current_sub_map:
            top_dict = meta.get(current_top_map)
            if isinstance(top_dict, dict) and isinstance(top_dict.get(current_sub_map), dict):
                top_dict[current_sub_map][key] = _parse_yaml_scalar(val)

    return meta, body


def sanitize_markdown_body(body: str) -> str:
    """Apply brand-safety and zero-jargon replacements outside Markdown link URLs."""
    preserved_urls: list[str] = []

    def _stash_url(match: re.Match[str]) -> str:
        preserved_urls.append(match.group(2))
        return f"[{match.group(1)}](__URL_{len(preserved_urls) - 1}__)"

    safe_text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", _stash_url, body)

    for pattern, repl in TRADEMARK_REPLACEMENTS:
        safe_text = pattern.sub(repl, safe_text)
    for pattern, repl in JARGON_REPLACEMENTS:
        safe_text = pattern.sub(repl, safe_text)

    for heading in REQUIRED_HEADINGS:
        title_part = heading.replace("### ", "")
        safe_text = re.sub(
            rf"^#{{1,6}}\s*{re.escape(title_part)}\s*:?\s*$",
            heading,
            safe_text,
            flags=re.MULTILINE | re.IGNORECASE,
        )

    for idx, original_url in enumerate(preserved_urls):
        safe_text = safe_text.replace(f"__URL_{idx}__", original_url)

    return safe_text


def strip_disallowed_markdown_links(markdown_text: str, allowed_urls: list[str]) -> str:
    """Replace any third-party Markdown link URLs outside allowed_urls/aff_hosts with plain link text."""
    aff_hosts = _load_allowed_affiliate_hosts()
    allowed_norm = {u.rstrip(".,;:/") for u in allowed_urls}
    allowed_hosts = {urlparse(u).netloc.lower() for u in allowed_urls if urlparse(u).netloc}

    def _filter_link(match: re.Match[str]) -> str:
        anchor = match.group(1)
        url = match.group(2).rstrip(".,;:/")
        host = urlparse(url).netloc.lower()
        if url in allowed_norm or host in aff_hosts or host in allowed_hosts or any(url.startswith(a) for a in allowed_norm):
            return f"[{anchor}]({match.group(2)})"
        return anchor

    return re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", _filter_link, markdown_text)


CLEAN_SPONSOR_COPY: dict[str, tuple[str, str]] = {
    "hubhum_01_MER047": ("PureVPN", "Optional encrypted VPN service for private connections on public Wi-Fi"),
    "hubhum_01_MER008": ("InterServer", "Optional managed hosting if you want to run cloud/self-hosted apps 24/7"),
    "hubhum_01_MER054": ("Creative Fabrica", "Optional creative marketplace offering fonts, icons, and design templates"),
    "hubhum_01_MER349": ("Envato Elements Direct", "Optional royalty-free stock footage, music tracks, and motion templates"),
    "hubhum_01_MER276": ("Rank Math Direct", "Optional search optimization toolkit for managing site previews and indexing"),
    "hubhum_01_MER269": ("WP Rocket Direct", "Optional caching add-on to accelerate WordPress page loads"),
    "hubhum_01_MER369": ("Placeit by Envato", "Optional browser-based mockup and template generator"),
    "hubhum_01_MER265": ("Elementor Pro Direct", "Optional visual page builder for WordPress sites"),
    "hubhum_01_MER023": ("ThemeIsle", "Optional lightweight themes and layout starter packs for websites"),
    "hubhum_01_MER089": ("Surfshark VPN", "Optional encrypted VPN service across desktop and mobile devices"),
    "hubhum_01_MER064": ("TorGuard", "Optional configurable VPN service for private networking"),
    "hubhum_01_MER048": ("Private Internet Access", "Optional privacy-focused VPN client for multiple devices"),
    "hubhum_01_MER009": ("ScalaHosting", "Optional managed VPS cloud hosting for web applications"),
    "hubhum_01_MER014": ("RoseHosting", "Optional managed Linux cloud server hosting"),
}


def _load_merchants_by_subid() -> dict[str, dict[str, str]]:
    """Map hubhum_01_MER* SubIDs to merchant metadata from data/affiliates_seed.json."""
    mapping: dict[str, dict[str, str]] = {}
    if not AFFILIATES_PATH.exists():
        return mapping
    data = json.loads(AFFILIATES_PATH.read_text(encoding="utf-8"))
    for m in data.get("merchants_by_id", {}).values():
        subid = str(m.get("subid") or "").strip()
        if subid:
            mapping[subid] = {
                "subid": subid,
                "name": str(m.get("name") or "Partner"),
                "tracking_url": str(m.get("tracking_url") or ""),
            }
    return mapping


def _strip_affiliates_from_editorial_text(editorial_text: str) -> str:
    """Remove any embedded (#ad) or hubhum_01_MER* sentences/bullets from editorial sections."""
    cleaned_lines: list[str] = []
    aff_marker_re = re.compile(r"hubhum_01_MER\d+|\(#ad\)", re.IGNORECASE)

    for raw_line in editorial_text.splitlines():
        if not aff_marker_re.search(raw_line):
            cleaned_lines.append(raw_line)
            continue

        stripped = raw_line.lstrip()
        # Drop affiliate bullet items injected into Key features or Who it's for
        if stripped.startswith("* ") or stripped.startswith("- "):
            continue

        # Protect markdown link periods temporarily before sentence splitting
        protected_links: list[str] = []

        def _stash(m: re.Match[str]) -> str:
            protected_links.append(m.group(0))
            return f"__MDLINK_{len(protected_links) - 1}__"

        masked = re.sub(r"\[[^\]]+\]\([^)]+\)", _stash, raw_line)
        segments = re.split(r"(?<=[.!?])\s+", masked)
        kept_segments: list[str] = []

        for seg in segments:
            if not seg.strip():
                continue
            restored_seg = seg
            for idx, orig in enumerate(protected_links):
                restored_seg = restored_seg.replace(f"__MDLINK_{idx}__", orig)
            if "hubhum_01_MER" in restored_seg or re.search(r"\(#ad\)", restored_seg, re.IGNORECASE):
                # Preserve leading editorial clause when connected via comma (", while...", ", or...")
                clause_split = re.split(
                    r",\s+(?:while|or|paired with|and explore|while also|alongside)\b",
                    restored_seg,
                    maxsplit=1,
                    flags=re.IGNORECASE,
                )
                if (
                    len(clause_split) == 2
                    and "hubhum_01_MER" not in clause_split[0]
                    and not re.search(r"\(#ad\)", clause_split[0], re.IGNORECASE)
                    and len(clause_split[0].strip()) >= 25
                ):
                    kept = clause_split[0].strip().rstrip(".,;:") + "."
                    kept_segments.append(kept)
                continue
            kept_segments.append(restored_seg)

        if kept_segments:
            cleaned_lines.append(" ".join(kept_segments))

    collapsed = re.sub(r"\n{3,}", "\n\n", "\n".join(cleaned_lines)).strip()
    return collapsed


def relocate_affiliate_links_to_sponsored_section(body: str, triplet: list[dict] | None = None) -> str:
    """Strictly isolate all 3 affiliate links inside '### Sponsored Partner Tools (#ad)'."""
    merchants_by_subid = _load_merchants_by_subid()
    host_to_url: dict[str, str] = {}
    triplet_items: list[dict[str, str]] = []

    if triplet:
        for item in triplet:
            u = str(item.get("tracking_url") or "").strip()
            s = str(item.get("subid") or "").strip()
            n = str(item.get("name") or "").strip()
            h = urlparse(u).netloc.lower()
            if h and u:
                host_to_url[h] = u
            if s and u:
                triplet_items.append({"subid": s, "name": n, "tracking_url": u})

    # Canonicalize any transposed SubIDs first before extracting present SubIDs
    def _canonicalize_aff_link(match: re.Match[str]) -> str:
        raw = match.group(0)
        h = urlparse(raw).netloc.lower()
        return host_to_url.get(h, raw)

    normalized_body = re.sub(r"https?://[^\s\)\]>\"']*hubhum_01_MER\d+[^\s\)\]>\"']*", _canonicalize_aff_link, body)
    present_subids = list(dict.fromkeys(re.findall(r"hubhum_01_MER\d+", normalized_body)))

    # Preserve Official Source / Credits footer link
    credits_match = re.search(r"(\[Official Source / Credits\]\([^)]+\))", normalized_body)
    credits_line = credits_match.group(1) if credits_match else ""

    # Strip existing Sponsored section & closing Official Source line so editorial sections are isolated cleanly
    work_body = re.split(r"\n?###\s+Sponsored Partner Tools\s*\(#ad\)", normalized_body, flags=re.IGNORECASE)[0]
    work_body = re.sub(r"\n?\*{0,2}Official Source[^:\n]*:\*{0,2}\s*\[Official Source / Credits\]\([^)]+\)\s*$", "", work_body)
    work_body = re.sub(r"\n?\[Official Source / Credits\]\([^)]+\)\s*$", "", work_body)
    clean_editorial = _strip_affiliates_from_editorial_text(work_body)

    # Assemble exactly 3 distinct partner items (prioritizing supplied triplet, then existing SubIDs, then defaults)
    chosen_partners: list[dict[str, str]] = []
    seen_subids: set[str] = set()
    for candidate in triplet_items:
        if candidate["subid"] not in seen_subids:
            seen_subids.add(candidate["subid"])
            chosen_partners.append(candidate)
        if len(chosen_partners) >= 3:
            break

    if len(chosen_partners) < 3:
        for sid in present_subids:
            if sid not in seen_subids and sid in merchants_by_subid:
                seen_subids.add(sid)
                chosen_partners.append(merchants_by_subid[sid])
            if len(chosen_partners) >= 3:
                break

    if len(chosen_partners) < 3:
        for fallback_sid in ("hubhum_01_MER008", "hubhum_01_MER047", "hubhum_01_MER276", "hubhum_01_MER054"):
            if fallback_sid not in seen_subids and fallback_sid in merchants_by_subid:
                seen_subids.add(fallback_sid)
                chosen_partners.append(merchants_by_subid[fallback_sid])
            if len(chosen_partners) >= 3:
                break

    partner_bullets = [
        SPONSORED_HEADING,
        "*Optional commercial services unrelated to the open-source developer. Clicking an `#ad` link helps fund HubHum at no extra cost to you.*",
    ]
    for p in chosen_partners[:3]:
        sid = p["subid"]
        url = p["tracking_url"]
        label, desc = CLEAN_SPONSOR_COPY.get(sid, (p["name"], "Optional partner tool for cloud hosting or creative assets"))
        partner_bullets.append(f"* **{label}:** {desc} — [{label}]({url}) (#ad)")

    parts = [clean_editorial.rstrip(), "", "\n".join(partner_bullets)]
    if credits_line:
        parts.extend(["", f"**Official Source & Credits:** {credits_line}"])
    return "\n".join(parts).strip() + "\n"


def ensure_triplet_links_in_body(body: str, triplet: list[dict] | None = None) -> str:
    """Isolate >= 3 distinct partner SubIDs strictly inside '### Sponsored Partner Tools (#ad)'."""
    return relocate_affiliate_links_to_sponsored_section(body, triplet=triplet)


def sanitize_full_document(markdown_text: str) -> str:
    """Re-serialize document with sanitized prose while keeping frontmatter intact."""
    normalized = markdown_text.replace("\r\n", "\n").strip()
    normalized = re.sub(r"^---[ \t]*\n", "---\n", normalized)
    if not normalized.startswith("---\n"):
        return markdown_text
    parts = re.split(r"\n---[ \t]*\n", normalized, maxsplit=1)
    if len(parts) != 2:
        return markdown_text
    header, body = parts
    clean_body = sanitize_markdown_body(body.strip())
    return f"{header}\n---\n\n{clean_body}\n"


def _load_allowed_affiliate_hosts() -> set[str]:
    hosts: set[str] = set()
    if not AFFILIATES_PATH.exists():
        return hosts
    data = json.loads(AFFILIATES_PATH.read_text(encoding="utf-8"))
    for m in data.get("merchants_by_id", {}).values():
        for key in ("tracking_url", "policy_url"):
            u = m.get(key)
            if u:
                hosts.add(urlparse(u).netloc.lower())
    return hosts


def validate_markdown_card(
    markdown_text: str,
    allowed_urls: list[str] | None = None,
    strict_urls: bool = True,
) -> list[str]:
    """Validate Zod-equivalent schema, required English headings, zero-jargon, and URL integrity."""
    errors: list[str] = []
    try:
        meta, body = split_frontmatter(markdown_text)
    except ValueError as exc:
        return [str(exc)]

    for req_key in ("title", "slug", "tags", "is_webapp"):
        if req_key not in meta:
            errors.append(f"Missing required frontmatter field: {req_key}")

    if "slug" in meta and not re.fullmatch(r"[a-z0-9-]+", str(meta["slug"])):
        errors.append(f"Invalid slug: {meta['slug']}")
    if "tags" in meta and (not isinstance(meta["tags"], list) or len(meta["tags"]) == 0):
        errors.append("Field 'tags' must contain at least one item.")
    if "is_webapp" in meta and not isinstance(meta["is_webapp"], bool):
        errors.append("Field 'is_webapp' must be boolean (true/false).")
    if "app_type" in meta and str(meta["app_type"]) not in ("desktop", "webapp", "selfhosted", "cli", "resource"):
        errors.append(f"Invalid app_type '{meta['app_type']}': expected desktop, webapp, selfhosted, cli, or resource.")

    main_summary = str(meta.get("summary") or "").strip()
    if is_summary_truncated(main_summary):
        errors.append(f"Field 'summary' appears truncated or incomplete: '{main_summary}'")

    raw_i18n = meta.get("i18n")
    if isinstance(raw_i18n, dict):
        for lang_code, lang_block in raw_i18n.items():
            if isinstance(lang_block, dict) and lang_block.get("summary"):
                l_sum = str(lang_block.get("summary") or "").strip()
                if is_summary_truncated(l_sum):
                    errors.append(f"Field 'i18n.{lang_code}.summary' appears truncated or incomplete: '{l_sum}'")

    for heading in REQUIRED_HEADINGS:
        if heading not in body:
            errors.append(f"Missing required heading: {heading}")

    if "Official Source / Credits" not in body:
        errors.append("Missing closing link [Official Source / Credits].")

    body_no_urls = re.sub(r"https?://[^\s\)\]>\"']+", "", body)
    for forbidden in ("pull request", "repository", "commit", "deploy"):
        if re.search(rf"\b{re.escape(forbidden)}\b", body_no_urls, re.IGNORECASE):
            errors.append(f"Forbidden tech jargon in body prose: '{forbidden}'")

    editorial_only, sponsored_marker, sponsored_part = body.partition(SPONSORED_HEADING)
    if sponsored_marker and (re.search(r"hubhum_01_MER\d+", editorial_only) or re.search(r"\(#ad\)", editorial_only, re.IGNORECASE)):
        errors.append("Affiliate links or (#ad) disclosures are forbidden inside editorial sections before '### Sponsored Partner Tools (#ad)'.")

    distinct_aff_subids = set(re.findall(r"hubhum_01_MER\d+", sponsored_part or body))
    if len(distinct_aff_subids) < 3:
        errors.append(
            f"Expected at least 3 distinct affiliate links (hubhum_01_MER*) inside '{SPONSORED_HEADING}', found {len(distinct_aff_subids)}."
        )

    if strict_urls and allowed_urls is not None:
        aff_hosts = _load_allowed_affiliate_hosts()
        allowed_norm = {u.rstrip(".,;:/") for u in allowed_urls}
        allowed_hosts = {urlparse(u).netloc.lower() for u in allowed_urls if urlparse(u).netloc}
        found_urls = re.findall(r"https?://[^\s\)\]>\"']+", body)
        for found in found_urls:
            found_clean = found.rstrip(".,;:/")
            host = urlparse(found_clean).netloc.lower()
            if found_clean in allowed_norm or host in aff_hosts:
                continue
            if any(found_clean.startswith(a) for a in allowed_norm) or host in allowed_hosts:
                continue
            errors.append(f"URL not present in source metadata or affiliate seed: {found_clean}")

    return errors


def validate_directory(apps_dir: Path = CONTENT_APPS_DIR) -> int:
    """Validate all Markdown cards in content/apps and return exit code (0=OK, 2=ERROR)."""
    files = sorted(apps_dir.glob("*.md"))
    if not files:
        print("No cards found in content/apps/")
        return 2

    has_error = False
    for md_file in files:
        content = md_file.read_text(encoding="utf-8")
        meta, _ = split_frontmatter(content)
        errs = validate_markdown_card(content, allowed_urls=None, strict_urls=False)
        if errs:
            has_error = True
            print(f"[ERROR] {md_file.name}:")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"[OK] {md_file.name} (slug={meta.get('slug')}, is_webapp={meta.get('is_webapp')})")
    return 2 if has_error else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HubHum Markdown Validator & Brand-Safety Sanitizer")
    parser.add_argument("--check-all", action="store_true", help="Validate all cards in content/apps")
    args = parser.parse_args()
    sys.exit(validate_directory())
