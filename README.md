# HubHum — a Git Hub for Humans

**Discover powerful free and open-source software explained in plain language, with zero tech jargon.**

🌐 **Live Catalog:** https://davanzokeoma.github.io/HubHum/

---

## Overview

Open-source tools are often hidden behind technical documentation meant for developers. **HubHum** translates popular open-source applications into clear, concise guides for everyday users—complete with direct links to official downloads and optional cloud-hosting launchers for web apps.

## Key Features

- **Jargon-Free Guides:** Every app card explains what the tool does, who it is for, and its pros and cons in plain everyday language.
- **Verified Official Downloads:** Direct links pulled strictly from official project releases (`.exe`, `.msi`, `.dmg`, `.AppImage`)—never repackaged or mirrored.
- **Instant Multi-Language UI:** English by default with automatic browser detection and instant switching across **EN / IT / ES / FR / DE**.
- **Static Speed (Astro SSG):** Built as pure static HTML with inlined critical CSS, zero render-blocking stylesheets, automatic XML sitemap, and semantic accessibility.
- **2-Tier AI Content Pipeline:** Automated nightly discovery via GitHub REST API (`> 500` stars, no forks) powered by Google AI Studio (`gemini-flash-lite-latest` / `gemini-3.1-flash-lite`) and Groq (`openai/gpt-oss-120b` / `qwen/qwen3.8-27b`).
- **MCP Server Ready:** Includes a JSON-RPC 2.0 Model Context Protocol server (`src/mcp/server.py`) exposing `search_human_apps` and `get_human_app` for AI agents.

## Submit an App

Want to add an open-source application to the catalog?
1. Visit https://davanzokeoma.github.io/HubHum/#submit and paste the project's GitHub URL, **or**
2. Open a new Issue in this repository with the project link.

## Local Development

```bash
npm install
npm run dev
```

Build the static production bundle into `dist/`:

```bash
npm run build
```

## Compliance & Disclaimer

- Every app card credits and links directly to the original project source.
- Partner recommendations are clearly labeled (`#ad`) in compliance with disclosure standards.
- **HubHum is an independent tool and is not affiliated with GitHub, Inc.**

## License

MIT
