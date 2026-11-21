"""Opt-in multi-channel content distribution for HubHum guides and bundles.

Supports Dev.to, Hashnode, Mastodon, Bluesky, and Telegram when configured via
environment variables / GitHub Actions Secrets. Channels without credentials
are cleanly skipped so automation never fails on missing opt-in configuration.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

from validator_sanitizer import split_frontmatter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_GUIDES_DIR = PROJECT_ROOT / "content" / "guides"
CONTENT_BUNDLES_DIR = PROJECT_ROOT / "content" / "bundles"
CLUSTERS_MANIFEST_PATH = PROJECT_ROOT / "data" / "clusters_manifest.json"
SITE_URL_PREFIX = "https://davanzokeoma.github.io/HubHum"
USER_AGENT = "HubHum-Distributor/1.0 (+https://davanzokeoma.github.io/HubHum/)"


def _post_json(url: str, payload: dict[str, object], headers: dict[str, str] | None = None) -> tuple[int, dict[str, object]]:
    req_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=req_headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
        parsed = json.loads(raw) if raw.strip() else {}
        return resp.status, parsed if isinstance(parsed, dict) else {"raw": parsed}


def select_target_content(target_slug: str | None = None) -> dict[str, object]:
    """Load the target guide or bundle Markdown for canonical distribution."""
    candidates: list[tuple[str, Path, dict[str, object], str]] = []

    for g_path in sorted(CONTENT_GUIDES_DIR.rglob("*.md")):
        meta, body = split_frontmatter(g_path.read_text(encoding="utf-8"))
        slug = str(meta.get("slug") or "").strip("/")
        if slug:
            candidates.append(("guide", g_path, meta, body))

    for b_path in sorted(CONTENT_BUNDLES_DIR.glob("*.md")):
        meta, body = split_frontmatter(b_path.read_text(encoding="utf-8"))
        slug = str(meta.get("slug") or b_path.stem).strip("/")
        if slug:
            candidates.append(("bundle", b_path, meta, body))

    if not candidates:
        return {
            "kind": "site",
            "slug": "",
            "title": "HubHum — 1,000+ Free & Open-Source Apps Explained in Plain English",
            "summary": "Explore 1,000+ curated free and open-source apps across 70 plain-English guides with direct official release downloads.",
            "canonical_url": f"{SITE_URL_PREFIX}/",
            "body_markdown": f"Discover 1,000+ open-source apps without jargon at {SITE_URL_PREFIX}/.",
            "tags": ["opensource", "productivity", "selfhosted", "software"],
        }

    chosen = candidates[0]
    if target_slug:
        norm = target_slug.strip("/")
        for item in candidates:
            if str(item[2].get("slug") or "").strip("/") == norm:
                chosen = item
                break
    else:
        # Prefer top-level Pillar guide from clusters_manifest.json when no slug is specified
        for item in candidates:
            if item[0] == "guide" and int(item[2].get("level") or 3) == 1:
                chosen = item
                break

    kind, _, meta, body = chosen
    slug = str(meta.get("slug") or "").strip("/")
    route_prefix = "guides" if kind == "guide" else "bundles"
    canonical_url = f"{SITE_URL_PREFIX}/{route_prefix}/{slug}/"
    title = str(meta.get("title") or slug).strip()
    summary = str(meta.get("summary") or f"Plain-English guide on HubHum: {title}").strip()
    clean_body = re.sub(r"^\s*#.*$", "", body, count=1, flags=re.MULTILINE).strip()
    article_md = (
        f"{summary}\n\n"
        f"{clean_body}\n\n"
        f"---\n"
        f"*Originally published on [HubHum — A Git Hub for Humans]({canonical_url}).*\n"
    )
    return {
        "kind": kind,
        "slug": slug,
        "title": title,
        "summary": summary,
        "canonical_url": canonical_url,
        "body_markdown": article_md,
        "tags": ["opensource", "software", "productivity", "selfhosted"],
    }


def publish_devto(post: dict[str, object], dry_run: bool = False) -> str:
    api_key = os.getenv("DEVTO_API_KEY", "").strip()
    if not api_key:
        print("[DISTRIBUTE SKIP] Dev.to: DEVTO_API_KEY not configured (opt-in inactive)")
        return "skipped"
    if dry_run:
        print(f"[DISTRIBUTE DRY-RUN] Dev.to: ready for canonical_url={post['canonical_url']}")
        return "dry-run"
    publish_live = os.getenv("DEVTO_PUBLISH", "false").lower() == "true"
    payload = {
        "article": {
            "title": post["title"],
            "published": publish_live,
            "body_markdown": post["body_markdown"],
            "canonical_url": post["canonical_url"],
            "tags": post["tags"],
        }
    }
    status, _ = _post_json(
        "https://dev.to/api/articles",
        payload,
        headers={"api-key": api_key},
    )
    print(f"[DISTRIBUTE OK] Dev.to -> HTTP {status} (canonical={post['canonical_url']})")
    return "sent"


def publish_hashnode(post: dict[str, object], dry_run: bool = False) -> str:
    token = os.getenv("HASHNODE_TOKEN", "").strip()
    pub_id = os.getenv("HASHNODE_PUB_ID", "").strip()
    if not token or not pub_id:
        print("[DISTRIBUTE SKIP] Hashnode: HASHNODE_TOKEN or HASHNODE_PUB_ID not configured (opt-in inactive)")
        return "skipped"
    if dry_run:
        print(f"[DISTRIBUTE DRY-RUN] Hashnode: ready for originalArticleURL={post['canonical_url']}")
        return "dry-run"
    mutation = """
    mutation PublishPost($input: PublishPostInput!) {
      publishPost(input: $input) {
        post { id url }
      }
    }
    """
    payload = {
        "query": mutation,
        "variables": {
            "input": {
                "title": post["title"],
                "contentMarkdown": post["body_markdown"],
                "publicationId": pub_id,
                "originalArticleURL": post["canonical_url"],
                "tags": [{"slug": str(t), "name": str(t)} for t in list(post["tags"])[:4]],  # type: ignore[arg-type]
            }
        },
    }
    status, _ = _post_json(
        "https://gql.hashnode.com",
        payload,
        headers={"Authorization": token},
    )
    print(f"[DISTRIBUTE OK] Hashnode -> HTTP {status} (canonical={post['canonical_url']})")
    return "sent"


def publish_mastodon(post: dict[str, object], dry_run: bool = False) -> str:
    instance = os.getenv("MASTODON_INSTANCE_URL", "").strip().rstrip("/")
    token = os.getenv("MASTODON_ACCESS_TOKEN", "").strip()
    if not instance or not token:
        print("[DISTRIBUTE SKIP] Mastodon: MASTODON_INSTANCE_URL or MASTODON_ACCESS_TOKEN not configured (opt-in inactive)")
        return "skipped"
    if dry_run:
        print(f"[DISTRIBUTE DRY-RUN] Mastodon: ready for {instance} ({post['canonical_url']})")
        return "dry-run"
    status_text = f"{post['title']}\n\n{post['summary']}\n\n{post['canonical_url']}\n#OpenSource #FreeSoftware #HubHum"
    status, _ = _post_json(
        f"{instance}/api/v1/statuses",
        {"status": status_text[:490], "visibility": "public"},
        headers={"Authorization": f"Bearer {token}"},
    )
    print(f"[DISTRIBUTE OK] Mastodon -> HTTP {status}")
    return "sent"


def publish_bluesky(post: dict[str, object], dry_run: bool = False) -> str:
    handle = os.getenv("BLUESKY_HANDLE", "").strip()
    app_pw = os.getenv("BLUESKY_APP_PASSWORD", "").strip()
    if not handle or not app_pw:
        print("[DISTRIBUTE SKIP] Bluesky: BLUESKY_HANDLE or BLUESKY_APP_PASSWORD not configured (opt-in inactive)")
        return "skipped"
    if dry_run:
        print(f"[DISTRIBUTE DRY-RUN] Bluesky: ready for {handle} ({post['canonical_url']})")
        return "dry-run"
    from datetime import datetime, timezone

    _, sess = _post_json(
        "https://bsky.social/xrpc/com.atproto.server.createSession",
        {"identifier": handle, "password": app_pw},
    )
    access_jwt = str(sess.get("accessJwt") or "")
    did = str(sess.get("did") or "")
    text = f"{post['title']} — {post['summary'][:140]} {post['canonical_url']}"[:295]
    status, _ = _post_json(
        "https://bsky.social/xrpc/com.atproto.repo.createRecord",
        {
            "repo": did,
            "collection": "app.bsky.feed.post",
            "record": {
                "$type": "app.bsky.feed.post",
                "text": text,
                "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            },
        },
        headers={"Authorization": f"Bearer {access_jwt}"},
    )
    print(f"[DISTRIBUTE OK] Bluesky -> HTTP {status}")
    return "sent"


def publish_telegram(post: dict[str, object], dry_run: bool = False) -> str:
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not bot_token or not chat_id:
        print("[DISTRIBUTE SKIP] Telegram: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not configured (opt-in inactive)")
        return "skipped"
    if dry_run:
        print(f"[DISTRIBUTE DRY-RUN] Telegram: ready for chat target ({post['canonical_url']})")
        return "dry-run"
    msg = f"{post['title']}\n\n{post['summary']}\n\n{post['canonical_url']}"
    status, _ = _post_json(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        {"chat_id": chat_id, "text": msg, "disable_web_page_preview": False},
    )
    print(f"[DISTRIBUTE OK] Telegram -> HTTP {status}")
    return "sent"


def main() -> int:
    parser = argparse.ArgumentParser(description="HubHum opt-in multi-channel content distribution")
    parser.add_argument("--slug", default="", help="Optional guide or bundle slug to feature")
    parser.add_argument("--dry-run", action="store_true", help="Inspect target content and channel status without posting")
    args = parser.parse_args()

    slug = args.slug.strip() or os.getenv("DISTRIBUTE_SLUG", "").strip() or None
    dry_run = bool(args.dry_run or os.getenv("DISTRIBUTE_DRY_RUN", "").lower() == "true")
    post = select_target_content(slug)
    print(f"[DISTRIBUTE TARGET] {post['kind']}: {post['title']} ({post['canonical_url']})")

    channels = (
        ("Dev.to", publish_devto),
        ("Hashnode", publish_hashnode),
        ("Mastodon", publish_mastodon),
        ("Bluesky", publish_bluesky),
        ("Telegram", publish_telegram),
    )
    results: dict[str, str] = {}
    for name, fn in channels:
        try:
            results[name] = fn(post, dry_run=dry_run)
        except urllib.error.HTTPError as exc:
            print(f"[DISTRIBUTE WARN] {name} returned HTTP {exc.code}: {exc.reason}")
            results[name] = f"http_{exc.code}"
        except Exception as exc:
            print(f"[DISTRIBUTE WARN] {name} non-fatal warning: {exc}")
            results[name] = "warn"

    print(f"[DISTRIBUTE SUMMARY] {json.dumps(results)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
