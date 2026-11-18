"""HubHum Model Context Protocol (MCP) JSON-RPC 2.0 Server (Sezione 11).

Exposes HubHum translated catalog to external AI agents via stdio JSON-RPC:
- search_human_apps(query, category, is_webapp, limit)
- get_human_app(slug)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from validator_sanitizer import split_frontmatter  # noqa: E402

CONTENT_APPS_DIR = PROJECT_ROOT / "content" / "apps"


def _load_catalog() -> list[dict]:
    items: list[dict] = []
    if not CONTENT_APPS_DIR.exists():
        return items
    for md_path in sorted(CONTENT_APPS_DIR.glob("*.md")):
        raw = md_path.read_text(encoding="utf-8")
        meta, body = split_frontmatter(raw)
        items.append({**meta, "body": body})
    return items


def search_human_apps(
    query: str = "",
    category: str | None = None,
    is_webapp: bool | None = None,
    limit: int = 10,
) -> list[dict]:
    """Search consumer-friendly app cards in HubHum."""
    q = query.strip().lower()
    results = []
    for item in _load_catalog():
        if category and str(item.get("category", "")).lower() != category.lower():
            continue
        if is_webapp is not None and bool(item.get("is_webapp")) != is_webapp:
            continue
        haystack = " ".join(
            [
                str(item.get("title", "")),
                str(item.get("summary", "")),
                str(item.get("category", "")),
                " ".join(str(t) for t in (item.get("tags") or [])),
                str(item.get("body", "")),
            ]
        ).lower()
        if q and q not in haystack:
            continue
        results.append(
            {
                "title": item.get("title"),
                "slug": item.get("slug"),
                "category": item.get("category"),
                "tags": item.get("tags"),
                "is_webapp": item.get("is_webapp"),
                "summary": item.get("summary"),
                "stars": item.get("stars"),
                "download_url": item.get("download_url"),
                "affiliate_url": item.get("affiliate_url"),
                "source_url": item.get("source_url"),
            }
        )
    results.sort(key=lambda x: int(x.get("stars") or 0), reverse=True)
    return results[:limit]


def get_human_app(slug: str) -> dict | None:
    """Return full Markdown card and metadata for a specific app slug."""
    for item in _load_catalog():
        if str(item.get("slug", "")).lower() == slug.strip().lower():
            return item
    return None


def handle_jsonrpc_request(req: dict) -> dict | None:
    """Dispatch MCP JSON-RPC 2.0 request."""
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params") or {}

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "hubhum-mcp", "version": "0.1.0"},
                "capabilities": {"tools": {}},
            },
        }

    if method == "notifications/initialized":
        return None

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "search_human_apps",
                        "description": "Cerca app open-source spiegate in parole semplici nel catalogo HubHum.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Parola chiave o bisogno utente"},
                                "category": {"type": "string", "description": "Filtro categoria opzionale"},
                                "is_webapp": {"type": "boolean", "description": "Filtra per app cloud o desktop"},
                                "limit": {"type": "integer", "default": 10},
                            },
                        },
                    },
                    {
                        "name": "get_human_app",
                        "description": "Recupera la scheda completa di un'app HubHum tramite il suo slug.",
                        "inputSchema": {
                            "type": "object",
                            "required": ["slug"],
                            "properties": {"slug": {"type": "string"}},
                        },
                    },
                ]
            },
        }

    if method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments") or {}
        if tool_name == "search_human_apps":
            res = search_human_apps(
                query=args.get("query", ""),
                category=args.get("category"),
                is_webapp=args.get("is_webapp"),
                limit=int(args.get("limit", 10)),
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}]},
            }
        if tool_name == "get_human_app":
            res = get_human_app(slug=args.get("slug", ""))
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False, indent=2)}]},
            }
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Tool sconosciuto: {tool_name}"},
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Metodo sconosciuto: {method}"},
    }


def run_stdio_server() -> None:
    """Run MCP server reading newline-delimited JSON-RPC from stdin."""
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        req = json.loads(line)
        resp = handle_jsonrpc_request(req)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


def run_self_test() -> None:
    """Run local verification on MCP tool discovery and search."""
    tools_resp = handle_jsonrpc_request({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    search_resp = handle_jsonrpc_request(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "search_human_apps", "arguments": {"query": ""}},
        }
    )
    tools = [t["name"] for t in tools_resp["result"]["tools"]]  # type: ignore[index]
    apps = json.loads(search_resp["result"]["content"][0]["text"])  # type: ignore[index]
    print(json.dumps({"mcp_tools": tools, "indexed_apps_count": len(apps)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HubHum MCP Server")
    parser.add_argument("--self-test", action="store_true", help="Verifica funzionamento server MCP")
    args = parser.parse_args()
    if args.self_test:
        run_self_test()
    else:
        run_stdio_server()
