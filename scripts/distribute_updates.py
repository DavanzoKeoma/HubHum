"""Opt-in high-EPC multi-channel content distribution for HubHum guides and bundles.

Focuses strictly on high-intent conversion content: Curated Starter Bundles and
Level-3 Comparison roundups ("Best of"), ranking Cloud/VPS, Local AI, Privacy/VPN,
and Creator Suites by monetization EPC before syndicating via opt-in Secrets.
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
SITE_URL_PREFIX = "https://davanzokeoma.github.io/HubHum"
USER_AGENT = "HubHum-Distributor/1.1 (+https://davanzokeoma.github.io/HubHum/)"


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


def _score_monetization_intent(kind: str, slug: str, meta: dict[str, object]) -> tuple[int, str, str]:
    """Return (epc_score, monetization_vertical, conversion_cta_hook) for a guide or bundle."""
    text = f"{slug} {meta.get('category', '')} {meta.get('title', '')} {' '.join(meta.get('tags') or [])}".lower()
    base = 50 if kind == "bundle" else (35 if str(meta.get("intent") or "") == "comparison" else 10)

    if any(k in text for k in ("self-hosted", "cloud", "home-server", "media-server", "ai-local", "llm", "vps", "dashboard")):
        return (
            base + 45,
            "cloud_vps_hosting",
            "Compare tested 1-click cloud hosting & VPS plans optimized for running this stack 24/7 cleanly.",
        )
    if any(k in text for k in ("privacy", "security", "password", "vpn", "cleaner", "network")):
        return (
            base + 35,
            "privacy_vpn",
            "Compare verified zero-log VPN and encrypted connection tools alongside every download step.",
        )
    if any(k in text for k in ("video", "audio", "creator", "graphics", "photo", "3d", "subtitle")):
        return (
            base + 25,
            "creator_assets",
            "Explore side-by-side feature notes, official installers, and creator workstation add-ons.",
        )
    return (
        base + 15,
        "general_productivity",
        "Read plain-English pros, cons, and verified direct official links on HubHum.",
    )


def select_target_content(target_slug: str | None = None, content_filter: str = "high-intent") -> dict[str, object]:
    """Load the highest-intent Bundle or Level-3 Comparison guide for canonical syndication."""
    candidates: list[tuple[int, str, str, str, Path, dict[str, object], str]] = []

    for b_path in sorted(CONTENT_BUNDLES_DIR.glob("*.md")):
        meta, body = split_frontmatter(b_path.read_text(encoding="utf-8"))
        slug = str(meta.get("slug") or b_path.stem).strip("/")
        if not slug:
            continue
        score, vertical, hook = _score_monetization_intent("bundle", slug, meta)
        candidates.append((score, vertical, hook, "bundle", b_path, meta, body))

    for g_path in sorted(CONTENT_GUIDES_DIR.rglob("*.md")):
        meta, body = split_frontmatter(g_path.read_text(encoding="utf-8"))
        slug = str(meta.get("slug") or "").strip("/")
        if not slug:
            continue
        intent = str(meta.get("intent") or "")
        level = int(meta.get("level") or 3)
        if content_filter == "high-intent" and not target_slug:
            if not (level == 3 and intent == "comparison"):
                continue
        score, vertical, hook = _score_monetization_intent("guide", slug, meta)
        candidates.append((score, vertical, hook, "guide", g_path, meta, body))

    if not candidates:
        return {
            "kind": "site",
            "slug": "",
            "vertical": "cloud_vps_hosting",
            "cta_hook": "Compare 1,250+ vetted free apps with direct official downloads and hosting comparisons.",
            "epc_score": 50,
            "title": "HubHum — 1,250+ Free & Open-Source Apps Explained in Plain English",
            "summary": "Explore 1,250+ curated free and open-source apps across 78 plain-English guides and 9 bundles.",
            "canonical_url": f"{SITE_URL_PREFIX}/",
            "body_markdown": f"Discover 1,250+ open-source apps without jargon at {SITE_URL_PREFIX}/.",
            "tags": ["opensource", "productivity", "selfhosted", "software"],
        }

    chosen = None
    if target_slug:
        norm = target_slug.strip("/")
        for item in candidates:
            if str(item[5].get("slug") or "").strip("/") == norm:
                chosen = item
                break
    if chosen is None:
        candidates.sort(key=lambda x: x[0], reverse=True)
        chosen = candidates[0]

    score, vertical, hook, kind, _, meta, body = chosen
    slug = str(meta.get("slug") or "").strip("/")
    route_prefix = "guides" if kind == "guide" else "bundles"
    canonical_url = f"{SITE_URL_PREFIX}/{route_prefix}/{slug}/"
    title = str(meta.get("title") or slug).strip()
    summary = str(meta.get("summary") or f"Plain-English guide on HubHum: {title}").strip()
    clean_body = re.sub(r"^\s*#.*$", "", body, count=1, flags=re.MULTILINE).strip()
    article_md = (
        f"{summary}\n\n"
        f"> **Interactive Comparison & Direct Official Downloads:** [{title}]({canonical_url})\n"
        f"> {hook}\n\n"
        f"{clean_body}\n\n"
        f"---\n"
        f"*Canonical interactive directory & setup picks: [Open {title} on HubHum]({canonical_url}).*\n"
    )
    return {
        "kind": kind,
        "slug": slug,
        "vertical": vertical,
        "epc_score": score,
        "cta_hook": hook,
        "title": title,
        "summary": summary,
        "canonical_url": canonical_url,
        "body_markdown": article_md,
        "tags": ["opensource", "selfhosted", "productivity", "freesoftware"],
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
    status, resp_data = _post_json(
        "https://dev.to/api/articles",
        payload,
        headers={"api-key": api_key},
    )
    live_url = str(resp_data.get("url") or "")
    print(f"[DISTRIBUTE OK] Dev.to -> HTTP {status} (live_url={live_url or 'n/a'}, canonical={post['canonical_url']})")
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
    status, resp_data = _post_json(
        "https://gql.hashnode.com",
        payload,
        headers={"Authorization": token},
    )
    post_obj = ((resp_data.get("data") or {}).get("publishPost") or {}).get("post") if isinstance(resp_data, dict) else {}
    live_url = str((post_obj or {}).get("url") or "")
    print(f"[DISTRIBUTE OK] Hashnode -> HTTP {status} (live_url={live_url or 'n/a'}, canonical={post['canonical_url']})")
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
    status_text = (
        f"{post['title']}\n\n{post['summary']}\n\n{post['cta_hook']}\n"
        f"{post['canonical_url']}\n#OpenSource #SelfHosted #FreeSoftware #HubHum"
    )
    status, resp_data = _post_json(
        f"{instance}/api/v1/statuses",
        {"status": status_text[:490], "visibility": "public"},
        headers={"Authorization": f"Bearer {token}"},
    )
    live_url = str(resp_data.get("url") or resp_data.get("uri") or "")
    print(f"[DISTRIBUTE OK] Mastodon -> HTTP {status} (live_url={live_url or 'n/a'})")
    return "sent"


def _build_bluesky_link_facets(text: str) -> list[dict[str, object]]:
    """Build AT Protocol byte-offset facets so URLs in Bluesky posts are clickable."""
    facets: list[dict[str, object]] = []
    for match in re.finditer(r"https?://[^\s]+", text):
        url = match.group(0).rstrip(".,;)")
        byte_start = len(text[: match.start()].encode("utf-8"))
        byte_end = byte_start + len(url.encode("utf-8"))
        facets.append(
            {
                "index": {"byteStart": byte_start, "byteEnd": byte_end},
                "features": [{"$type": "app.bsky.richtext.facet#link", "uri": url}],
            }
        )
    return facets


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
    url_str = str(post["canonical_url"])
    prefix_budget = max(40, 295 - len(url_str) - 2)
    blurb = f"{post['title']} — {post['summary']}"[:prefix_budget].rstrip()
    text = f"{blurb}\n{url_str}"[:298]
    facets = _build_bluesky_link_facets(text)
    record: dict[str, object] = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    if facets:
        record["facets"] = facets
    status, resp_data = _post_json(
        "https://bsky.social/xrpc/com.atproto.repo.createRecord",
        {
            "repo": did,
            "collection": "app.bsky.feed.post",
            "record": record,
        },
        headers={"Authorization": f"Bearer {access_jwt}"},
    )
    rkey = str(resp_data.get("uri") or "").split("/")[-1]
    live_url = f"https://bsky.app/profile/{handle}/post/{rkey}" if rkey else ""
    print(f"[DISTRIBUTE OK] Bluesky -> HTTP {status} (live_url={live_url or 'n/a'})")
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
    msg = f"{post['title']}\n\n{post['summary']}\n\n{post['cta_hook']}\n{post['canonical_url']}"
    status, _ = _post_json(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        {"chat_id": chat_id, "text": msg, "disable_web_page_preview": False},
    )
    print(f"[DISTRIBUTE OK] Telegram -> HTTP {status}")
    return "sent"


def main() -> int:
    parser = argparse.ArgumentParser(description="HubHum high-EPC opt-in content distribution")
    parser.add_argument("--slug", default="", help="Optional guide or bundle slug to feature")
    parser.add_argument(
        "--filter",
        dest="content_filter",
        choices=["high-intent", "all"],
        default="high-intent",
        help="Restrict syndication to high-EPC Bundles and Level-3 Comparisons (default: high-intent)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Inspect target content and channel status without posting")
    args = parser.parse_args()

    slug = args.slug.strip() or os.getenv("DISTRIBUTE_SLUG", "").strip() or None
    dry_run = bool(args.dry_run or os.getenv("DISTRIBUTE_DRY_RUN", "").lower() == "true")
    post = select_target_content(slug, content_filter=args.content_filter)
    print(
        f"[DISTRIBUTE TARGET] filter={args.content_filter} kind={post['kind']} "
        f"vertical={post['vertical']} score={post['epc_score']} "
        f"title={post['title']} canonical={post['canonical_url']}"
    )
    if dry_run:
        print(f"[DISTRIBUTE HOOK] {post['cta_hook']}")

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
