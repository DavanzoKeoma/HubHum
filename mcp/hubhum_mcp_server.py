"""HubHum Model Context Protocol (MCP) Server exposing catalog search, guide reader, and 1-click conversion.

Supports FastMCP (when `mcp` package is installed) and includes a zero-dependency
JSON-RPC 2.0 stdio transport implementation so AI assistants can connect cleanly
using Python 3.11+ standard library alone.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_CATALOG_PATH = PROJECT_ROOT / "data" / "catalog-index.json"
PUBLIC_CATALOG_PATH = PROJECT_ROOT / "public" / "catalog-index.json"
CONTENT_APPS_DIR = PROJECT_ROOT / "content" / "apps"
HUBHUM_SITE = "https://davanzokeoma.github.io/HubHum"
WORKER_CONVERT_URL = "https://hubhum-api-bridge.keomadavanzo.workers.dev/api/convert"

SERVER_INFO = {"name": "hubhum-mcp", "version": "1.0.0"}
PROTOCOL_VERSION = "2024-11-05"


def _load_catalog() -> list[dict]:
    for path in (DATA_CATALOG_PATH, PUBLIC_CATALOG_PATH):
        if path.is_file():
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
    return []


def search_apps(query: str, category: str | None = None) -> dict:
    """Search the HubHum human-friendly software catalog by keyword and optional category."""
    items = _load_catalog()
    q = (query or "").strip().lower()
    cat_filter = (category or "").strip().lower()

    matches = []
    for item in items:
        item_cat = str(item.get("category") or "").lower()
        if cat_filter and cat_filter not in item_cat:
            continue
        searchable = " ".join(
            [
                str(item.get("name") or ""),
                str(item.get("slug") or ""),
                str(item.get("summary") or ""),
                str(item.get("category") or ""),
                str(item.get("full_name") or ""),
            ]
        ).lower()
        if not q or q in searchable:
            slug = str(item.get("slug") or "")
            matches.append(
                {
                    "slug": slug,
                    "name": item.get("name"),
                    "category": item.get("category"),
                    "is_webapp": item.get("is_webapp", False),
                    "stars": item.get("stars", 0),
                    "summary": item.get("summary", ""),
                    "download_url": item.get("download_url", ""),
                    "hubhum_url": f"{HUBHUM_SITE}/apps/{slug}/",
                }
            )

    matches.sort(key=lambda x: int(x.get("stars") or 0), reverse=True)
    return {
        "query": query,
        "category": category,
        "total_matches": len(matches),
        "results": matches[:25],
    }


def get_app_guide(slug: str) -> dict:
    """Return the plain-English Markdown guide, downloads, and credits for a HubHum app slug."""
    clean_slug = (slug or "").strip().lower()
    if not re.fullmatch(r"[a-z0-9-]+", clean_slug):
        return {"error": f"Invalid app slug '{slug}'. Expected lowercase alphanumeric/hyphen identifier."}

    md_path = CONTENT_APPS_DIR / f"{clean_slug}.md"
    if not md_path.is_file():
        return {"error": f"App guide '{clean_slug}' not found in HubHum catalog."}

    raw_text = md_path.read_text(encoding="utf-8")
    return {
        "slug": clean_slug,
        "hubhum_url": f"{HUBHUM_SITE}/apps/{clean_slug}/",
        "markdown": raw_text,
    }


def humanize_github_repo(repo_url: str) -> dict:
    """Convert any public GitHub repository URL into a plain-English HubHum guide via the Worker bridge."""
    raw = (repo_url or "").strip()
    match = re.match(
        r"^https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git|/.*)?$",
        raw,
    )
    if not match:
        return {"error": "Invalid URL. Expected format: https://github.com/owner/repo"}

    owner, repo = match.group(1), match.group(2)
    clean_url = f"https://github.com/{owner}/{repo}"
    slug = re.sub(r"[^a-z0-9-]+", "-", repo.lower()).strip("-")

    # Short-circuit if guide already exists locally
    if (CONTENT_APPS_DIR / f"{slug}.md").is_file():
        return {
            "status": "already_exists",
            "slug": slug,
            "repo_url": clean_url,
            "guide_url": f"{HUBHUM_SITE}/apps/{slug}/",
        }

    payload = json.dumps({"repo_url": clean_url}).encode("utf-8")
    req = urllib.request.Request(
        WORKER_CONVERT_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://davanzokeoma.github.io",
            "User-Agent": "HubHum-MCP/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            resolved_slug = str(data.get("slug") or slug)
            return {
                "status": data.get("status", "queued"),
                "slug": resolved_slug,
                "repo_url": clean_url,
                "guide_url": f"{HUBHUM_SITE}/apps/{resolved_slug}/",
                "note": "Build and AI translation queued on GitHub Actions (~45-60s until live).",
            }
    except urllib.error.HTTPError as exc:
        return {"error": f"Worker bridge returned HTTP {exc.code}: {exc.read().decode(errors='replace')[:200]}"}
    except Exception as exc:
        return {"error": f"Failed to contact HubHum Worker: {exc}"}


TOOL_SCHEMAS = [
    {
        "name": "search_apps",
        "description": "Search HubHum's human-friendly software catalog by keyword and optional category.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search keyword (app name, use case, or topic)"},
                "category": {"type": "string", "description": "Optional category filter (e.g., Video & Audio, Security & Privacy)"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_app_guide",
        "description": "Read the full plain-English guide, verified downloads, and pros/cons for a HubHum slug.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slug": {"type": "string", "description": "App URL slug (e.g., 'vlc', 'joplin', 'handbrake')"},
            },
            "required": ["slug"],
        },
    },
    {
        "name": "humanize_github_repo",
        "description": "Queue an AI plain-English translation for any public GitHub repository URL on HubHum.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo_url": {"type": "string", "description": "Full GitHub repository URL (https://github.com/owner/repo)"},
            },
            "required": ["repo_url"],
        },
    },
]


def handle_jsonrpc_message(msg: dict) -> dict | None:
    """Process one MCP JSON-RPC 2.0 request and return a response dict (or None for notifications)."""
    method = msg.get("method")
    msg_id = msg.get("id")
    params = msg.get("params") or {}

    if msg_id is None:
        return None

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
            },
        }

    if method == "ping":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOL_SCHEMAS}}

    if method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments") or {}
        if tool_name == "search_apps":
            res = search_apps(args.get("query", ""), args.get("category"))
        elif tool_name == "get_app_guide":
            res = get_app_guide(args.get("slug", ""))
        elif tool_name == "humanize_github_repo":
            res = humanize_github_repo(args.get("repo_url", ""))
        else:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
            }
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}],
                "isError": bool(isinstance(res, dict) and res.get("error")),
            },
        }

    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def run_stdio_server() -> None:
    """Run via FastMCP if installed, otherwise serve JSON-RPC 2.0 cleanly over stdin/stdout."""
    try:
        from mcp.server.fastmcp import FastMCP  # type: ignore

        mcp = FastMCP("HubHum")
        mcp.tool()(search_apps)
        mcp.tool()(get_app_guide)
        mcp.tool()(humanize_github_repo)
        mcp.run()
        return
    except ImportError:
        pass

    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError as exc:
            resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}
        else:
            resp = handle_jsonrpc_message(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


def run_self_test() -> int:
    """Run offline self-test of all MCP tools and JSON-RPC 2.0 protocol handlers."""
    init_res = handle_jsonrpc_message({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    assert init_res and init_res["result"]["serverInfo"]["name"] == "hubhum-mcp"

    list_res = handle_jsonrpc_message({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    tool_names = [t["name"] for t in list_res["result"]["tools"]]  # type: ignore[index]
    assert tool_names == ["search_apps", "get_app_guide", "humanize_github_repo"]

    search_out = search_apps("video")
    assert search_out["total_matches"] >= 1, "Expected at least 1 match for 'video'"

    guide_out = get_app_guide("vlc")
    assert "What it does in plain English" in guide_out.get("markdown", ""), "Missing VLC guide content"

    bad_slug = get_app_guide("../.env")
    assert "error" in bad_slug, "Path traversal check failed!"

    existing_convert = humanize_github_repo("https://github.com/videolan/vlc")
    assert existing_convert.get("status") == "already_exists"

    print(
        f"[OK] HubHum MCP self-test passed (tools={tool_names}, "
        f"video_matches={search_out['total_matches']}, protocol={PROTOCOL_VERSION})."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="HubHum Model Context Protocol Server")
    parser.add_argument("--self-test", action="store_true", help="Verify MCP schemas and local tool calls")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    run_stdio_server()
    return 0


if __name__ == "__main__":
    sys.exit(main())
