---
title: "abtop"
slug: "abtop"
tagline: "Monitor your AI coding agent sessions."
summary: "Keep track of active AI assistant sessions, token usage, context windows, and rate limits in a single real-time dashboard."
tags: ["developer-tools", "monitoring", "system-utility", "ai"]
is_webapp: false
app_type: "desktop"
category: "Productivity"
icon: "/icons/abtop.png"
stars: 3880
source_url: "https://github.com/graykode/abtop"
download_url: "https://github.com/graykode/abtop/releases/download/v0.5.5/abtop-aarch64-apple-darwin.tar.xz.sha256"
downloadUrl: "https://github.com/graykode/abtop/releases/download/v0.5.5/abtop-aarch64-apple-darwin.tar.xz.sha256"
download_label: "Download (abtop-aarch64-apple-darwin.tar.xz.sha256)"
license: "Open Source (MIT)"
scouting_tier: "tier1_gui"
operatingSystem: "Windows, macOS, Linux"
applicationCategory: "UtilitiesApplication"
priceCurrency: "USD"
price: "0"
affiliate_merchant_id: "MER_061"
affiliate_name: "Systeme.io"
affiliate_url: "https://systeme.io/?sa=sa023692845080664785297106081136cf8d3a59ee&subid=hubhum_01_MER061"
affiliate_pitch: "Automate everyday online workflows free forever and safeguard your devices and backups."
ai_provider: "tier1_gemini:gemini-flash-lite-latest"
featured_weekly: true
updated_at: "2026-11-25"
i18n:
  it:
    tagline: "Monitora le sessioni dei tuoi assistenti AI."
    summary: "Tieni d'occhio le sessioni di programmazione AI, l'uso dei token, i limiti di velocità e la memoria in tempo reale."
  es:
    tagline: "Monitorea tus sesiones de agentes de código."
    summary: "Supervisa las sesiones de asistentes virtuales de código, el uso de tokens, límites de velocidad y puertos."
  fr:
    tagline: "Surveillez vos sessions d'assistants de code."
    summary: "Suivez vos sessions d'intelligence artificielle, l'utilisation des jetons et les limites de taux en temps réel."
  de:
    tagline: "Überwachen Sie Ihre KI-Programmiersitzungen."
    summary: "Behalten Sie den Überblick über aktive KI-Assistenten, Token-Verbrauch, Kontextfenster und Ratenlimits."
---

### What it does in plain English
abtop is a live monitor designed specifically for tracking multiple AI coding assistants running on your computer. It gives you a single screen to watch token usage, memory consumption, context window fill levels, and open internet ports across all your active tasks. By reading local process data safely and quietly in the background, it helps you spot runaway tasks, avoid sudden rate limits, and keep your workspace tidy without needing any external passwords or accounts.

### Who it's for
* Software developers juggling multiple AI coding assistants across different projects at the same time.
* Programmers who want to prevent unexpected rate limits and keep a close eye on token consumption.
* Developers needing a quick way to locate and close background server ports left open by background tasks.

### Key features
* Real-time tracking of active AI coding agent sessions from a single unified screen.
* Clear progress bars showing your current context window limits and memory warnings.
* Orphaned port detection to instantly spot and clean up forgotten background servers.
* Twelve built-in themes including several options designed for colorblind users.
* Optional one-shot JSON snapshot output for scripting and custom automation tools.

### How to install (Download)
You can quickly install abtop on macOS and Linux using the automated installation script:
```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/graykode/abtop/releases/latest/download/abtop-installer.sh | sh
```

For Windows users, native support is available via PowerShell:
```powershell
powershell -c "irm https://github.com/graykode/abtop/releases/latest/download/abtop-installer.ps1 | iex"
```

You can also install it via Rust's package manager if you have it set up:
```bash
cargo install abtop
```
For manual setup files and checksums, browse the official [GitHub Releases](https://github.com/graykode/abtop/releases) page.

### Pros and Cons
* **Pros:** Free forever with no subscription or account setup, lightweight terminal interface, zero external API keys required.
* **Cons:** Requires terminal usage, advanced configuration options take a short time to learn.

### Sponsored Partner Tools (#ad)
*Optional commercial services unrelated to the open-source developer. Clicking an `#ad` link helps fund HubHum at no extra cost to you.*
* **★ Top Recommended — Systeme.io:** Free-forever all-in-one platform to build landing pages, newsletters, and automated workflows with zero monthly fees — [**Activate Systeme.io →**](https://systeme.io/?sa=sa023692845080664785297106081136cf8d3a59ee&subid=hubhum_01_MER061) (#ad)
* **AdGuard:** Block intrusive ads, tracking scripts, and phishing domains system-wide across all browsers and desktop apps — [AdGuard](https://adguard.com/?aid=138327&subid=hubhum_01_MER119) (#ad)
* **InterServer:** Launch and host self-hosted web apps 24/7 on managed Linux cloud VPS servers starting at $3/month — [InterServer](https://www.interserver.net/vps?id=1196747&sid=hubhum_01_MER008) (#ad)

**Official Source & Credits:** [Official Source / Credits](https://github.com/graykode/abtop)
