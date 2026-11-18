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

REQUIRED_HEADINGS = (
    "### What it does in plain English",
    "### Who it's for",
    "### Key features",
    "### How to install (Download)",
    "### Pros and Cons",
)

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
    if not normalized.startswith("---\n"):
        raise ValueError("Missing YAML frontmatter at start of file.")
    parts = normalized.split("\n---\n", 1)
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
        safe_text = re.sub(rf"^{re.escape(heading)}\s*:?\s*$", heading, safe_text, flags=re.MULTILINE)

    for idx, original_url in enumerate(preserved_urls):
        safe_text = safe_text.replace(f"__URL_{idx}__", original_url)

    return safe_text


def sanitize_full_document(markdown_text: str) -> str:
    """Re-serialize document with sanitized prose while keeping frontmatter intact."""
    normalized = markdown_text.replace("\r\n", "\n").strip()
    if not normalized.startswith("---\n") or "\n---\n" not in normalized:
        return markdown_text
    header, body = normalized.split("\n---\n", 1)
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
    if str(meta.get("summary") or "").endswith("..."):
        errors.append("Field 'summary' must be complete without trailing '...'.")

    for heading in REQUIRED_HEADINGS:
        if heading not in body:
            errors.append(f"Missing required heading: {heading}")

    if "Official Source / Credits" not in body:
        errors.append("Missing closing link [Official Source / Credits].")

    body_no_urls = re.sub(r"https?://[^\s\)\]>\"']+", "", body)
    for forbidden in ("pull request", "repository", "commit", "deploy"):
        if re.search(rf"\b{re.escape(forbidden)}\b", body_no_urls, re.IGNORECASE):
            errors.append(f"Forbidden tech jargon in body prose: '{forbidden}'")

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
