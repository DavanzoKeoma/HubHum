"""Compliance / DMCA rapid takedown handler for HubHum (Sezione 10)."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_APPS_DIR = PROJECT_ROOT / "content" / "apps"
BLOCKLIST_PATH = PROJECT_ROOT / "data" / "takedown_blocklist.json"
EVENTS_LOG_PATH = PROJECT_ROOT / ".pcp" / "context" / "events.log"


def execute_takedown(slug: str, reason: str = "compliance", auto_commit: bool = True) -> int:
    """Remove app card, add slug to blocklist, log event, and commit removal."""
    clean_slug = slug.strip().lower()
    if not clean_slug:
        print("Errore: specifica uno slug valido.")
        return 2

    target_md = CONTENT_APPS_DIR / f"{clean_slug}.md"
    removed = False
    if target_md.exists():
        target_md.unlink()
        removed = True
        print(f"[REMOVED] {target_md}")
    else:
        print(f"[INFO] Scheda {target_md.name} già assente; aggiungo comunque alla blocklist.")

    BLOCKLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    if BLOCKLIST_PATH.exists():
        blocklist = json.loads(BLOCKLIST_PATH.read_text(encoding="utf-8"))
    else:
        blocklist = {"blocked_slugs": [], "history": []}

    if clean_slug not in blocklist["blocked_slugs"]:
        blocklist["blocked_slugs"].append(clean_slug)
    blocklist["history"].append(
        {
            "slug": clean_slug,
            "reason": reason,
            "removed_file": removed,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )
    BLOCKLIST_PATH.write_text(json.dumps(blocklist, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if EVENTS_LOG_PATH.parent.exists():
        digest = hashlib.sha256(f"takedown:{clean_slug}:{reason}".encode("utf-8")).hexdigest()
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "action": "TAKEDOWN_EXECUTED",
            "slug": clean_slug,
            "reason": reason,
            "sha256": digest,
        }
        with EVENTS_LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")

    if auto_commit:
        subprocess.run(["git", "add", "content/apps", "data/takedown_blocklist.json"], cwd=PROJECT_ROOT, check=False)
        subprocess.run(
            ["git", "commit", "-m", f"Remove: [{clean_slug}] per compliance"],
            cwd=PROJECT_ROOT,
            check=False,
        )

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HubHum Rapid Takedown")
    parser.add_argument("slug", help="Slug dell'app da rimuovere")
    parser.add_argument("--reason", default="compliance")
    parser.add_argument("--no-commit", action="store_true")
    args = parser.parse_args()
    sys.exit(execute_takedown(args.slug, reason=args.reason, auto_commit=not args.no_commit))
