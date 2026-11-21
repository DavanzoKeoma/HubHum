"""Submit HubHum Pillar, Guide, and core URLs to the Wayback Machine archival API."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLUSTERS_MANIFEST_PATH = PROJECT_ROOT / "data" / "clusters_manifest.json"
SITE_URL_PREFIX = "https://davanzokeoma.github.io/HubHum"
WAYBACK_SAVE_BASE = "https://web.archive.org/save/"
USER_AGENT = "HubHum-Archiver/1.0 (+https://davanzokeoma.github.io/HubHum/)"


def collect_target_urls() -> list[str]:
    """Collect homepage, Topic Cluster pillars, sub-pillars, and key API/RAG URLs."""
    urls: list[str] = [
        f"{SITE_URL_PREFIX}/",
        f"{SITE_URL_PREFIX}/guides/",
        f"{SITE_URL_PREFIX}/about/",
        f"{SITE_URL_PREFIX}/llms.txt",
        f"{SITE_URL_PREFIX}/api/openapi.yaml",
    ]
    if CLUSTERS_MANIFEST_PATH.exists():
        try:
            data = json.loads(CLUSTERS_MANIFEST_PATH.read_text(encoding="utf-8"))
            for p in data.get("pillars", []):
                macro_slug = str(p.get("macro_slug") or "").strip()
                if macro_slug:
                    urls.append(f"{SITE_URL_PREFIX}/guides/{macro_slug}/")
                for s in p.get("subpillars", []):
                    sub_slug = str(s.get("sub_slug") or "").strip()
                    if sub_slug:
                        urls.append(f"{SITE_URL_PREFIX}/guides/{sub_slug}/")
            for b in data.get("bundles", []):
                if b:
                    urls.append(f"{SITE_URL_PREFIX}/bundles/{b}/")
        except Exception:
            pass
    return list(dict.fromkeys(urls))


def submit_wayback_snapshots(urls: list[str], limit: int = 10, delay: float = 5.0, dry_run: bool = False) -> int:
    """Request Wayback Machine snapshot creation with polite pacing (non-fatal on transient errors)."""
    selected = urls[:limit] if limit > 0 else urls
    if dry_run:
        print(f"[WAYBACK DRY-RUN] Prepared {len(selected)} URLs for archival.")
        for u in selected[:10]:
            print(f"  - {u}")
        return 0

    for idx, target_url in enumerate(selected, start=1):
        save_endpoint = f"{WAYBACK_SAVE_BASE}{target_url}"
        req = urllib.request.Request(save_endpoint, headers={"User-Agent": USER_AGENT}, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                print(f"[WAYBACK] ({idx}/{len(selected)}) {target_url} -> HTTP {resp.status}")
        except urllib.error.HTTPError as exc:
            print(f"[WAYBACK WARN] ({idx}/{len(selected)}) {target_url} -> HTTP {exc.code}")
        except Exception as exc:
            print(f"[WAYBACK WARN] ({idx}/{len(selected)}) {target_url} -> {exc}")

        if idx < len(selected) and delay > 0:
            time.sleep(delay)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit HubHum Pillar and Guide URLs to Wayback Machine")
    parser.add_argument("--limit", type=int, default=10, help="Maximum URLs to submit per run (0 = all)")
    parser.add_argument("--delay", type=float, default=5.0, help="Delay between requests in seconds")
    parser.add_argument("--dry-run", action="store_true", help="Print URLs without making network requests")
    args = parser.parse_args()

    urls = collect_target_urls()
    return submit_wayback_snapshots(urls, limit=args.limit, delay=args.delay, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
