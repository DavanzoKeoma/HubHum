"""Submit updated HubHum URLs from sitemap-0.xml to IndexNow search engines."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOCAL_SITEMAP = PROJECT_ROOT / "dist" / "sitemap-0.xml"
LIVE_SITEMAP_URL = "https://davanzokeoma.github.io/HubHum/sitemap-0.xml"
HOST = "davanzokeoma.github.io"
INDEXNOW_KEY = "hubhum8f4a2c9e1d7b3a6f5c0e9d2b4a7f1c3e"
KEY_LOCATION = f"https://{HOST}/HubHum/{INDEXNOW_KEY}.txt"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
USER_AGENT = "HubHum-IndexNow/1.0"


def load_sitemap_urls(sitemap_path: Path) -> list[str]:
    """Read URLs from local dist/sitemap-0.xml or fall back to live sitemap XML."""
    xml_bytes: bytes | None = None
    if sitemap_path.exists():
        xml_bytes = sitemap_path.read_bytes()
    else:
        try:
            req = urllib.request.Request(LIVE_SITEMAP_URL, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=20) as resp:
                xml_bytes = resp.read()
        except Exception as exc:
            print(f"[INDEXNOW WARN] Could not load sitemap from file or URL: {exc}")
            return []

    urls: list[str] = []
    try:
        root = ET.fromstring(xml_bytes)
        for loc in root.iter():
            if loc.tag.endswith("loc") and loc.text:
                u = loc.text.strip()
                if u.startswith("https://davanzokeoma.github.io/HubHum"):
                    urls.append(u)
    except ET.ParseError as exc:
        print(f"[INDEXNOW WARN] Failed to parse sitemap XML: {exc}")
        return []

    return list(dict.fromkeys(urls))


def submit_indexnow_batches(urls: list[str], batch_size: int = 500, dry_run: bool = False) -> int:
    """Submit URL batches to IndexNow API (graceful non-fatal on external HTTP errors)."""
    if not urls:
        print("[INDEXNOW] No URLs found to submit.")
        return 0

    total = len(urls)
    if dry_run:
        print(f"[INDEXNOW DRY-RUN] Prepared {total} URLs (host={HOST}, keyLocation={KEY_LOCATION}).")
        return 0

    for idx in range(0, total, batch_size):
        chunk = urls[idx : idx + batch_size]
        payload = {
            "host": HOST,
            "key": INDEXNOW_KEY,
            "keyLocation": KEY_LOCATION,
            "urlList": chunk,
        }
        req = urllib.request.Request(
            INDEXNOW_ENDPOINT,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": USER_AGENT,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                print(f"[INDEXNOW] Batch {idx // batch_size + 1}: submitted {len(chunk)} URLs -> HTTP {resp.status}")
        except urllib.error.HTTPError as exc:
            print(f"[INDEXNOW WARN] Batch {idx // batch_size + 1} HTTP {exc.code}: {exc.reason}")
        except Exception as exc:
            print(f"[INDEXNOW WARN] Batch {idx // batch_size + 1} request warning: {exc}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Ping IndexNow with HubHum sitemap URLs")
    parser.add_argument("--sitemap", default=str(DEFAULT_LOCAL_SITEMAP), help="Path to local sitemap-0.xml")
    parser.add_argument("--batch-size", type=int, default=500, help="Max URLs per IndexNow POST")
    parser.add_argument("--dry-run", action="store_true", help="Inspect URLs without sending POST request")
    args = parser.parse_args()

    urls = load_sitemap_urls(Path(args.sitemap))
    return submit_indexnow_batches(urls, batch_size=args.batch_size, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
