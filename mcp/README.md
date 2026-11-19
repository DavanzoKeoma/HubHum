# HubHum MCP Server (Model Context Protocol)

Expose HubHum's plain-English open-source software catalog and 1-click AI translation workflow directly to AI assistants (Claude Desktop, Cursor, Google Antigravity IDE).

---

## Exposed Tools

| Tool Name | Arguments | Purpose |
|---|---|---|
| `search_apps` | `query: str`, `category?: str` | Searches the local HubHum catalog index (`data/catalog-index.json`) and returns matching apps, popularity, categories, and download URLs. |
| `get_app_guide` | `slug: str` | Reads `content/apps/{slug}.md` and returns the plain-English overview, user profiles, verified download installers, and pros/cons. |
| `humanize_github_repo` | `repo_url: str` | Submits any public GitHub URL to `POST https://hubhum-api-bridge.keomadavanzo.workers.dev/api/convert` (or returns immediately if already indexed). |

---

## Quick Verification

```bash
python mcp/hubhum_mcp_server.py --self-test
```

Works with Python 3.11+ standard library out-of-the-box (automatically upgrades to `FastMCP` if `mcp` is installed in your environment).

---

## Client Configuration Examples

Replace `<PATH_TO_HUBHUM_REPO>` with the absolute path to your local clone of `HubHum`.

### 1. Claude Desktop (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "hubhum": {
      "command": "python",
      "args": ["<PATH_TO_HUBHUM_REPO>/mcp/hubhum_mcp_server.py"]
    }
  }
}
```

### 2. Cursor / Google Antigravity IDE (`mcpServers`)

```json
{
  "mcpServers": {
    "hubhum": {
      "command": "python",
      "args": ["<PATH_TO_HUBHUM_REPO>/mcp/hubhum_mcp_server.py"],
      "env": {}
    }
  }
}
```
