"""Validate Chrome Extension (Manifest V3) and package dist-extension/hubhum-chrome-extension.zip."""

from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXTENSION_DIR = PROJECT_ROOT / "extension"
DIST_ZIP = PROJECT_ROOT / "dist-extension" / "hubhum-chrome-extension.zip"

REQUIRED_FILES = (
    "manifest.json",
    "background.js",
    "content.js",
    "content.css",
    "popup/popup.html",
    "popup/popup.css",
    "popup/popup.js",
    "icons/icon-16.png",
    "icons/icon-32.png",
    "icons/icon-48.png",
    "icons/icon-128.png",
)

EXPECTED_ICON_SIZES = {
    "icons/icon-16.png": (16, 16),
    "icons/icon-32.png": (32, 32),
    "icons/icon-48.png": (48, 48),
    "icons/icon-128.png": (128, 128),
}

FORBIDDEN_PATTERNS = (
    re.compile(r"\.pcp[/\\]", re.IGNORECASE),
    re.compile(r"\.env\b", re.IGNORECASE),
    re.compile(r"C:\\\\?Users\\\\?", re.IGNORECASE),
    re.compile(r"/home/[a-z0-9_-]+/", re.IGNORECASE),
    re.compile(r"affiliatech", re.IGNORECASE),
    re.compile(r"(?:ghp_|github_pat_|AIzaSy|gsk_)[A-Za-z0-9_-]{12,}"),
)


def validate_manifest(manifest_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Invalid manifest.json: {exc}"]

    if manifest.get("manifest_version") != 3:
        errors.append(f"Expected manifest_version=3, got {manifest.get('manifest_version')}")
    if not manifest.get("name"):
        errors.append("Missing required manifest field: name")
    if not manifest.get("version"):
        errors.append("Missing required manifest field: version")
    if (manifest.get("background") or {}).get("service_worker") != "background.js":
        errors.append("background.service_worker must be 'background.js'")
    if (manifest.get("action") or {}).get("default_popup") != "popup/popup.html":
        errors.append("action.default_popup must be 'popup/popup.html'")

    perms = set(manifest.get("permissions") or [])
    for req_perm in ("activeTab", "storage", "notifications"):
        if req_perm not in perms:
            errors.append(f"Missing required permission: {req_perm}")

    hosts = set(manifest.get("host_permissions") or [])
    for req_host in (
        "https://davanzokeoma.github.io/*",
        "https://hubhum-api-bridge.keomadavanzo.workers.dev/*",
    ):
        if req_host not in hosts:
            errors.append(f"Missing required host_permission: {req_host}")

    cs = manifest.get("content_scripts") or []
    if not cs or "https://github.com/*/*" not in (cs[0].get("matches") or []):
        errors.append("Missing content_scripts match 'https://github.com/*/*'")

    return errors


def validate_files_and_secrets() -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        fpath = EXTENSION_DIR / rel
        if not fpath.is_file():
            errors.append(f"Missing required extension file: extension/{rel}")
            continue

        if rel in EXPECTED_ICON_SIZES:
            try:
                with Image.open(fpath) as im:
                    if im.size != EXPECTED_ICON_SIZES[rel]:
                        errors.append(
                            f"Icon {rel} must be {EXPECTED_ICON_SIZES[rel]}, found {im.size}"
                        )
            except Exception as exc:
                errors.append(f"Invalid image {rel}: {exc}")
        elif rel.endswith((".json", ".js", ".css", ".html")):
            text = fpath.read_text(encoding="utf-8")
            for pat in FORBIDDEN_PATTERNS:
                if pat.search(text):
                    errors.append(f"Forbidden secret/local pattern ({pat.pattern}) found in {rel}")

    return errors


def package_zip() -> Path:
    DIST_ZIP.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DIST_ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for rel in REQUIRED_FILES:
            zf.write(EXTENSION_DIR / rel, arcname=rel)

    with zipfile.ZipFile(DIST_ZIP, "r") as zf:
        bad = zf.testzip()
        if bad is not None:
            raise RuntimeError(f"Corrupt ZIP entry detected: {bad}")
        entries = set(zf.namelist())
        missing = [r for r in REQUIRED_FILES if r not in entries]
        if missing:
            raise RuntimeError(f"Missing files in packaged ZIP: {missing}")
    return DIST_ZIP


def main() -> int:
    if not EXTENSION_DIR.is_dir():
        print(f"[ERROR] Extension directory not found: {EXTENSION_DIR}")
        return 2

    errors = validate_manifest(EXTENSION_DIR / "manifest.json") + validate_files_and_secrets()
    if errors:
        for e in errors:
            print(f"[ERROR] {e}")
        return 2

    zip_path = package_zip()
    size_kb = zip_path.stat().st_size / 1024
    print(f"[OK] Manifest V3 validated ({len(REQUIRED_FILES)} files verified, zero leaks).")
    print(f"[OK] Packaged Chrome Extension ZIP: {zip_path} ({size_kb:.2f} KiB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
