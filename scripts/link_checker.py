"""Weekly release link verifier & auto-repair script (Workflow 6)."""

from __future__ import annotations

import re
import urllib.error
import urllib.request
from pathlib import Path

from scouter import fetch_repo_by_url
from validator_sanitizer import split_frontmatter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_APPS_DIR = PROJECT_ROOT / "content" / "apps"
USER_AGENT = "HubHum-LinkChecker/1.0 (DavanzoKeoma; keomadavanzo@gmail.com)"


def check_url_status(url: str) -> int:
    """Return HTTP status code (200/302/etc.) using HEAD with GET fallback."""
    headers = {"User-Agent": USER_AGENT}
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return int(resp.status)
        except urllib.error.HTTPError as err:
            if method == "HEAD" and err.code in (403, 405):
                continue
            return int(err.code)
        except Exception:
            return 0
    return 0


def repair_broken_download_links() -> int:
    """Check download_url in all app cards and auto-update via GitHub Releases on 404."""
    repaired = 0
    for md_path in sorted(CONTENT_APPS_DIR.glob("*.md")):
        raw = md_path.read_text(encoding="utf-8")
        meta, _ = split_frontmatter(raw)
        dl_url = str(meta.get("download_url") or "")
        source_url = str(meta.get("source_url") or "")
        if not dl_url or not source_url:
            continue

        status = check_url_status(dl_url)
        if status == 404:
            print(f"[BROKEN 404] {md_path.name}: {dl_url}")
            try:
                bundle = fetch_repo_by_url(source_url)
                new_url = bundle.primary_download_url
                if new_url and new_url != dl_url:
                    updated = raw.replace(dl_url, new_url)
                    updated = re.sub(
                        r'^download_url:\s*"[^"]*"',
                        f'download_url: "{new_url}"',
                        updated,
                        flags=re.MULTILINE,
                    )
                    md_path.write_text(updated, encoding="utf-8")
                    repaired += 1
                    print(f"[REPAIRED] {md_path.name} -> {new_url}")
            except Exception as exc:
                print(f"[WARN] Impossibile riparare {md_path.name}: {exc}")
        else:
            print(f"[OK {status}] {md_path.name}")

    print(f"Verifica link completata: {repaired} file corretti.")
    return repaired


if __name__ == "__main__":
    repair_broken_download_links()
