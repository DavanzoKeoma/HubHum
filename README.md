# HubHum — A Git Hub for Humans: Curated Directory of Free & Open-Source Software Without Tech Jargon

[![Total Apps](https://img.shields.io/badge/Total_Apps-1%2C000%2B-0f766e?style=for-the-badge)](https://davanzokeoma.github.io/HubHum/)
[![Live Catalog](https://img.shields.io/badge/Live_Catalog-Online-16a34a?style=for-the-badge)](https://davanzokeoma.github.io/HubHum/)
[![License](https://img.shields.io/badge/License-MIT-2563eb?style=for-the-badge)](./LICENSE)
[![Community Standards](https://img.shields.io/badge/Community_Standards-100%25-7c3aed?style=for-the-badge)](https://github.com/DavanzoKeoma/HubHum/community)
[![Topic Guides](https://img.shields.io/badge/Topic_Guides-58%2B-d97706?style=for-the-badge)](https://davanzokeoma.github.io/HubHum/guides/)
[![AI & RAG Ready](https://img.shields.io/badge/AI_%26_RAG-llms.txt_%2B_OpenAPI-0284c7?style=for-the-badge)](https://davanzokeoma.github.io/HubHum/llms.txt)

**Discover 1,000+ curated free and open-source applications explained in plain, everyday English—complete with direct official release downloads, transparent licensing, and zero developer jargon.**

🌐 **Live Directory:** [https://davanzokeoma.github.io/HubHum/](https://davanzokeoma.github.io/HubHum/)

---

## Table of Contents

- [Overview](#overview)
- [Catalog Breakdown (1,000 Validated Apps)](#catalog-breakdown-1000-validated-apps)
- [Architecture (Astro + GitHub Pages + Actions)](#architecture-astro--github-pages--actions)
- [Public JSON API, OpenAPI & RAG Endpoints](#public-json-api-openapi--rag-endpoints)
- [Submit an App](#submit-an-app)
- [Community & GitHub Discussions](#community--github-discussions)
- [Local Development](#local-development)
- [Governance, Security & License](#governance-security--license)

---

## Overview

Open-source software is often buried behind developer-centric READMEs, build instructions, and terminal jargon. **HubHum** bridges that gap by translating vetted open-source projects into crystal-clear, accessible guides for everyday users, creators, privacy-conscious households, and teams.

- **Plain-English Clarity:** Every guide explains *what it does*, *who it is for*, *pros and cons*, and *how to start in minutes* across **5 languages (EN / IT / ES / FR / DE)**.
- **Verified Official Sources Only (Zero Repackaging):** All download buttons point strictly to upstream GitHub Releases (`.exe`, `.msi`, `.dmg`, `.AppImage`, `.apk`) or official project websites—never third-party mirrors or unverified forks (`NO-FORK` rule).
- **Strict `#ad` Disclosure & Separation:** Optional partner recommendations are cleanly isolated inside `### Sponsored Partner Tools (#ad)` and domain-matched by category (Privacy, Cloud Hosting, Video/Design, Productivity).
- **Topic Clusters & Starter Bundles:** 58+ structured Topic Cluster pillars, sub-guides, and curated starter bundles (e.g., *Creator Studio Pack*, *Privacy Essentials*, *Clean Office Alternatives*).

---

## Catalog Breakdown (1,000 Validated Apps)

| Tier | Format | Target Quota | Description |
| :--- | :--- | :---: | :--- |
| **Tier 1** | Desktop & Mobile GUI | **500** | Point-and-click installers for Windows, macOS, Linux, and Android (`> 500` GitHub stars) |
| **Tier 2** | Web App & Self-Hosted | **300** | Browser-based platforms, self-hosted cloud workspaces, wikis, dashboards, and Docker stacks |
| **Tier 3** | Power Tools & CLI | **200** | High-impact command-line utilities and open-source developer/power-user references |

---

## Architecture (Astro + GitHub Pages + Actions)

1. **Static SSG Core (`src/`):** Built with [Astro](https://astro.build/) as pure zero-runtime-bloat HTML/CSS/JS with inlined critical styling, WCAG AA contrast in both Light and Dark themes, and rich Schema.org JSON-LD (`SoftwareApplication`, `WebApplication`, `SoftwareSourceCode`, `BreadcrumbList`).
2. **Automated Content Pipeline (`scripts/`):**
   - `scouter.py` queries original, non-forked GitHub repositories with verified licenses and release assets.
   - `ai_router.py` & `seo_pipeline.py` generate structured, jargon-free 5-language cards via Gemini Flash and Groq fallback cascade.
   - `validator_sanitizer.py` enforces strict URL allowlists, summary completeness, humanized licenses (`0` `NOASSERTION`), and `#ad` isolation.
   - `cluster_orchestrator.py` and `generate_catalog_index.py` build Topic Clusters, search indexes, and AI/RAG endpoints.
3. **CI/CD (`deploy.yml` & `seo-builder.yml`):** Automated validation (`validator_sanitizer.py --check-all`), static build (`npm run build`), GitHub Pages deployment, and IndexNow notifications.

---

## Public JSON API, OpenAPI & RAG Endpoints

HubHum is designed to be natively discoverable by browsers, search engines, LLM agents, and RAG pipelines:

| Resource | URL | Purpose |
| :--- | :--- | :--- |
| **OpenAPI 3.0 Spec** | [`/api/openapi.yaml`](https://davanzokeoma.github.io/HubHum/api/openapi.yaml) | Machine-readable REST specification (also in [Swagger JSON](https://davanzokeoma.github.io/HubHum/api/swagger.json)) |
| **AI Plugin Manifest** | [`/.well-known/ai-plugin.json`](https://davanzokeoma.github.io/HubHum/.well-known/ai-plugin.json) | Standard manifest linking AI tools to HubHum OpenAPI spec |
| **Catalog JSON API** | [`/api/catalog.json`](https://davanzokeoma.github.io/HubHum/api/catalog.json) | Complete JSON array of all indexed applications and metadata |
| **Clusters JSON API** | [`/api/clusters.json`](https://davanzokeoma.github.io/HubHum/api/clusters.json) | Hierarchical Topic Pillars, Sub-Pillars, and Starter Bundles |
| **LLMs Summary Index** | [`/llms.txt`](https://davanzokeoma.github.io/HubHum/llms.txt) | Concise AI-friendly directory map |
| **Full RAG Digest** | [`/catalog-rag.txt`](https://davanzokeoma.github.io/HubHum/catalog-rag.txt) | Compact 2-line single-file catalog digest for RAG context windows |
| **Codebase & Architecture Map** | [`/codebase-full.txt`](https://davanzokeoma.github.io/HubHum/codebase-full.txt) | Full architecture map + guide tree + complete app catalog digest |
| **RSS Feed & Sitemap** | [`/feed.xml`](https://davanzokeoma.github.io/HubHum/feed.xml) / [`/sitemap-index.xml`](https://davanzokeoma.github.io/HubHum/sitemap-index.xml) | Live syndication feed and XML sitemaps |

Quick JSON API query example:

```bash
curl -s https://davanzokeoma.github.io/HubHum/api/catalog.json | jq '.apps[:5] | .[] | {name, category, license, stars}'
```

---

## Submit an App

Know a great free & open-source tool that deserves a plain-English guide?

1. Use the interactive **Submit an App** section at [https://davanzokeoma.github.io/HubHum/#submit](https://davanzokeoma.github.io/HubHum/#submit), **or**
2. Open a structured **[App Suggestion Issue](./.github/ISSUE_TEMPLATE/app_suggestion.yml)** with the upstream GitHub repository URL. *(Forks, closed-source paywalls, and cracked software are automatically rejected.)*

---

## Community & GitHub Discussions

Have a question like *"What is the easiest free alternative to Photoshop for beginners?"* or want to suggest a new Topic Cluster guide?

💬 Join **[GitHub Discussions](https://github.com/DavanzoKeoma/HubHum/discussions)** to request comparisons, vote on starter bundles, and help make open source welcoming for everyone.

---

## Local Development

```bash
npm install
npm run dev
```

Validate content cards and build the static bundle into `dist/`:

```bash
python scripts/generate_catalog_index.py
python scripts/validator_sanitizer.py --check-all
npm run build
```

---

## Governance, Security & License

- **Community Standards:** See [`CONTRIBUTING.md`](./CONTRIBUTING.md), [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md), [`SECURITY.md`](./SECURITY.md), and [`ACCESSIBILITY.md`](./ACCESSIBILITY.md).
- **Disclaimer:** Every app card credits and links directly to its original upstream creator. **HubHum is an independent directory and is not affiliated with GitHub, Inc.**
- **License:** Released under the [MIT License](./LICENSE). If citing this project in research or datasets, please see [`CITATION.cff`](./CITATION.cff).
