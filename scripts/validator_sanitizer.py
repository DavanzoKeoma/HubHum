"""Validation and Brand Safety / Zero-Jargon sanitization for HubHum Markdown cards."""

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
    "### Cos'è in parole semplici",
    "### A chi è utile",
    "### Cosa puoi farci",
    "### Come si installa (Download)",
    "### Pro e Contro",
)

TRADEMARK_REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\b(?:il\s+)?killer\s+di\s+[A-Z0-9][A-Za-z0-9\s.+_-]{1,30}", re.IGNORECASE), "un'alternativa gratuita ai programmi commerciali"),
    (re.compile(r"\bAdobe\s+Premiere(?:\s+Pro)?\b", re.IGNORECASE), "programmi di montaggio video a pagamento"),
    (re.compile(r"\bPremiere\s+Pro\b", re.IGNORECASE), "programmi di montaggio video a pagamento"),
    (re.compile(r"\bFinal\s+Cut(?:\s+Pro)?\b", re.IGNORECASE), "software di editing video proprietari"),
    (re.compile(r"\bAdobe\s+Photoshop\b", re.IGNORECASE), "software di fotoritocco proprietari"),
    (re.compile(r"\bPhotoshop\b", re.IGNORECASE), "software di fotoritocco proprietari"),
    (re.compile(r"\bAdobe\s+Illustrator\b", re.IGNORECASE), "software di grafica vettoriale a pagamento"),
    (re.compile(r"\bMicrosoft\s+Office\b", re.IGNORECASE), "suite d'ufficio commerciali"),
    (re.compile(r"\b1Password\b", re.IGNORECASE), "gestori di password in abbonamento"),
    (re.compile(r"\bLastPass\b", re.IGNORECASE), "gestori di password commerciali"),
    (re.compile(r"\bWordPress\.com\b", re.IGNORECASE), "piattaforme editoriali chiuse"),
]

JARGON_REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bpull\s+request\b", re.IGNORECASE), "proposta di aggiornamento"),
    (re.compile(r"\brepository\b", re.IGNORECASE), "pagina ufficiale del progetto"),
    (re.compile(r"\bcommit\b", re.IGNORECASE), "aggiornamento"),
    (re.compile(r"\bdeploy\b", re.IGNORECASE), "pubblicazione online"),
    (re.compile(r"\bframework\b", re.IGNORECASE), "struttura di base"),
]


def split_frontmatter(markdown_text: str) -> tuple[dict[str, object], str]:
    """Parse lightweight YAML frontmatter block and return (data, body)."""
    normalized = markdown_text.replace("\r\n", "\n").strip()
    if not normalized.startswith("---\n"):
        raise ValueError("Frontmatter YAML mancante all'inizio del file.")
    parts = normalized.split("\n---\n", 1)
    if len(parts) != 2:
        raise ValueError("Frontmatter YAML non chiuso correttamente con '---'.")

    header_raw = parts[0][4:]
    body = parts[1].strip()
    meta: dict[str, object] = {}

    for line in header_raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if val in ("true", "false"):
            meta[key] = val == "true"
        elif val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            if not inner:
                meta[key] = []
            else:
                meta[key] = [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
        elif re.fullmatch(r"\d+", val):
            meta[key] = int(val)
        else:
            meta[key] = val.strip('"').strip("'")
    return meta, body


def sanitize_markdown_body(body: str) -> str:
    """Apply brand-safety and zero-jargon replacements outside Markdown link URLs."""
    # Protect markdown links [label](url) from accidental URL mutation
    preserved_urls: list[str] = []

    def _stash_url(match: re.Match[str]) -> str:
        preserved_urls.append(match.group(2))
        return f"[{match.group(1)}](__URL_{len(preserved_urls) - 1}__)"

    safe_text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", _stash_url, body)

    for pattern, repl in TRADEMARK_REPLACEMENTS:
        safe_text = pattern.sub(repl, safe_text)
    for pattern, repl in JARGON_REPLACEMENTS:
        safe_text = pattern.sub(repl, safe_text)

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
    """Validate Zod-equivalent schema, required headings, zero-jargon, and URL integrity."""
    errors: list[str] = []
    try:
        meta, body = split_frontmatter(markdown_text)
    except ValueError as exc:
        return [str(exc)]

    for req_key in ("title", "slug", "tags", "is_webapp"):
        if req_key not in meta:
            errors.append(f"Campo frontmatter obbligatorio mancante: {req_key}")

    if "slug" in meta and not re.fullmatch(r"[a-z0-9-]+", str(meta["slug"])):
        errors.append(f"Slug non valido: {meta['slug']}")
    if "tags" in meta and (not isinstance(meta["tags"], list) or len(meta["tags"]) == 0):
        errors.append("Il campo tags deve contenere almeno un elemento.")
    if "is_webapp" in meta and not isinstance(meta["is_webapp"], bool):
        errors.append("Il campo is_webapp deve essere booleano (true/false).")

    for heading in REQUIRED_HEADINGS:
        if heading not in body:
            errors.append(f"Intestazione obbligatoria mancante: {heading}")

    if "Fonte ufficiale / Crediti" not in body:
        errors.append("Manca il collegamento finale [Fonte ufficiale / Crediti].")

    # Check prose (excluding URLs) for forbidden git-jargon
    body_no_urls = re.sub(r"https?://[^\s\)\]>\"']+", "", body)
    for forbidden in ("pull request", "repository", "commit", "deploy"):
        if re.search(rf"\b{re.escape(forbidden)}\b", body_no_urls, re.IGNORECASE):
            errors.append(f"Termine tecnico non ammesso nel testo: '{forbidden}'")

    if strict_urls and allowed_urls is not None:
        aff_hosts = _load_allowed_affiliate_hosts()
        allowed_set = set(allowed_urls)
        found_urls = re.findall(r"https?://[^\s\)\]>\"']+", body)
        for found in found_urls:
            found_clean = found.rstrip(".,;:")
            host = urlparse(found_clean).netloc.lower()
            if found_clean in allowed_set or host in aff_hosts:
                continue
            errors.append(f"URL non presente nei dati sorgente o nel seed affiliati: {found_clean}")

    return errors


def validate_directory(apps_dir: Path = CONTENT_APPS_DIR) -> int:
    """Validate all Markdown cards in content/apps and return exit code (0=OK, 2=ERROR)."""
    files = sorted(apps_dir.glob("*.md"))
    if not files:
        print("Nessuna scheda trovata in content/apps/")
        return 2

    has_error = False
    for md_file in files:
        content = md_file.read_text(encoding="utf-8")
        meta, _ = split_frontmatter(content)
        allowed = []
        for k in ("source_url", "download_url", "affiliate_url"):
            if meta.get(k):
                allowed.append(str(meta[k]))
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
    parser.add_argument("--check-all", action="store_true", help="Valida tutte le schede in content/apps")
    args = parser.parse_args()

    code = validate_directory() if args.check_all or True else 0
    sys.exit(code)
