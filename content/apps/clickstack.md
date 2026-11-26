---
title: "ClickStack"
slug: "clickstack"
tagline: "Unify logs, traces, and metrics easily."
summary: "An open-source observability platform that helps engineers quickly investigate and resolve production issues in one central place."
tags: ["observability", "monitoring", "logging", "tracing"]
is_webapp: true
app_type: "selfhosted"
category: "Web Apps & Cloud"
icon: "/icons/clickstack.png"
stars: 10061
source_url: "https://github.com/ClickHouse/ClickStack"
download_url: "https://github.com/ClickHouse/ClickStack/releases/download/cli-v0.9.1/hdx-darwin-arm64"
downloadUrl: "https://github.com/ClickHouse/ClickStack/releases/download/cli-v0.9.1/hdx-darwin-arm64"
download_label: "Official Setup & Docs →"
license: "Open Source (MIT)"
scouting_tier: "tier2_webapp"
operatingSystem: "Self-Hosted / Browser"
applicationCategory: "BusinessApplication"
priceCurrency: "USD"
price: "0"
affiliate_merchant_id: "MER_008"
affiliate_name: "InterServer"
affiliate_url: "https://www.interserver.net/vps?id=1196747&sid=hubhum_01_MER008"
affiliate_pitch: "Prefer not to configure a server manually? Launch it in 1 click on a $3/mo Linux Cloud VPS."
ai_provider: "tier1_gemini:gemini-flash-lite-latest"
featured_weekly: true
updated_at: "2026-11-21"
i18n:
  it:
    tagline: "Unifica log, tracce e metriche facilmente."
    summary: "Una piattaforma di osservabilità open-source per risolvere rapidamente i problemi di produzione in un unico posto."
  es:
    tagline: "Unifica registros, rastreos y métricas."
    summary: "Una plataforma de observabilidad de código abierto para investigar y resolver problemas de producción rápidamente."
  fr:
    tagline: "Unifiez journaux, traces et métriques."
    summary: "Une plateforme d'observabilité open-source pour enquêter et résoudre rapidement les problèmes de production."
  de:
    tagline: "Protokolle, Traces und Metriken vereinen."
    summary: "Eine Open-Source-Beobachtungsplattform zur schnellen Untersuchung und Behebung von Produktionsproblemen."
---

### What it does in plain English
ClickStack brings together application logs, error traces, and performance metrics into a single intuitive dashboard. Instead of jumping between multiple confusing monitoring tools, you can search and visualize all your operational telemetry data instantly. It helps development teams quickly pinpoint the root cause of production bugs so systems stay healthy and reliable.

### Who it's for
* Software engineers and developers troubleshooting live application errors and performance slowdowns
* DevOps teams seeking a unified system to monitor application health without expensive commercial licensing fees
* Data-driven teams who want fast full-text searching across logs and traces stored on reliable database clusters

### Key features
* Combines logs, metrics, user session replays, and performance traces in one dashboard
* Blazing fast search and visualization capabilities designed for heavy database workloads
* Simple full-text search syntax that lets you query data quickly without complex query languages
* Built-in support for standard open-source telemetry collectors right out of the box
* Live log streaming so you can watch incoming application events in real time

### How to install (Download)
To run the complete platform locally or on a server, use the all-in-one container command:
```bash
docker run -p 8080:8080 -p 4317:4317 -p 4318:4318 docker.clickhouse.com/clickhouse/clickstack-all-in-one
```
After starting the container, open `http://localhost:8080` in your web browser. 

If you prefer using the terminal command-line tool, you can download the official pre-compiled releases directly:
* [Download (hdx-darwin-arm64)](https://github.com/ClickHouse/ClickStack/releases/download/cli-v0.9.1/hdx-darwin-arm64)
* [Download (hdx-darwin-x64)](https://github.com/ClickHouse/ClickStack/releases/download/cli-v0.9.1/hdx-darwin-x64)
* [Download (hdx-linux-x64)](https://github.com/ClickHouse/ClickStack/releases/download/cli-v0.9.1/hdx-linux-x64)

### Pros and Cons
* **Pros:** Completely open-source, fast search performance, avoids costly enterprise telemetry bills
* **Cons:** Requires initial server setup and configuration of your application telemetry SDKs

### Sponsored Partner Tools (#ad)
*Optional commercial services unrelated to the open-source developer. Clicking an `#ad` link helps fund HubHum at no extra cost to you.*
* **★ Top Recommended — InterServer:** Launch and host self-hosted web apps 24/7 on managed Linux cloud VPS servers starting at $3/month — [**Activate InterServer →**](https://www.interserver.net/vps?id=1196747&sid=hubhum_01_MER008) (#ad)
* **GreenGeeks:** Eco-friendly 300% green-energy SSD hosting with free SSL, nightly backups, and 1-click app installers — [GreenGeeks](https://www.greengeeks.com/track/affiliatechproject/cp-ffltc/lp-1?subid=hubhum_01_MER063) (#ad)
* **Hosting.com (ex A2 Hosting):** High-speed NVMe Managed VPS and WordPress cloud hosting optimized for self-hosted apps and sites — [Hosting.com (ex A2 Hosting)](https://hosting.com/hosting/vps-hosting/managed/linux/?utm_source=fp_affiliate&utm_medium=15437677&utm_campaign=42825&utm_content=affiliates&fpr=h37jvi&subid=hubhum_01_MER062) (#ad)

**Official Source & Credits:** [Official Source / Credits](https://github.com/ClickHouse/ClickStack)
