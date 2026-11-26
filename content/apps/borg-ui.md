---
title: "borg-ui"
slug: "borg-ui"
tagline: "Manage your file backups effortlessly via web"
summary: "Replace complex terminal commands with a clean web interface to easily create, schedule, and restore your system backups."
tags: ["backup", "web-ui", "automation", "storage"]
is_webapp: true
app_type: "selfhosted"
category: "Web Apps & Cloud"
icon: "/icons/borg-ui.png"
stars: 1694
source_url: "https://github.com/karanhudia/borg-ui"
download_url: "https://github.com/karanhudia/borg-ui/releases/download/v2.4.10/borg-ui-2.4.10.tar.gz.sha256"
downloadUrl: "https://github.com/karanhudia/borg-ui/releases/download/v2.4.10/borg-ui-2.4.10.tar.gz.sha256"
download_label: "Download (borg-ui-2.4.10.tar.gz.sha256)"
license: "Open Source (AGPL v3)"
scouting_tier: "tier2_webapp"
operatingSystem: "Self-Hosted / Browser"
applicationCategory: "BusinessApplication"
priceCurrency: "USD"
price: "0"
affiliate_merchant_id: "MER_008"
affiliate_name: "InterServer"
affiliate_url: "https://www.interserver.net/r/1196747?id=hubhum_01_MER008"
affiliate_pitch: "Prefer not to configure a server manually? Launch it in 1 click on managed cloud hosting."
ai_provider: "tier1_gemini:gemini-flash-lite-latest"
featured_weekly: true
updated_at: "2026-11-25"
i18n:
  it:
    tagline: "Gestisci i backup dei file facilmente via web"
    summary: "Sostituisci i comandi da terminale con un'interfaccia web per creare, pianificare e ripristinare i backup."
  es:
    tagline: "Gestiona las copias de seguridad fácilmente por web"
    summary: "Sustituye los comandos de terminal por una interfaz web para crear, programar y restaurar tus copias."
  fr:
    tagline: "Gérez vos sauvegardes de fichiers facilement via le web"
    summary: "Remplacez les commandes complexes par une interface web claire pour créer, planifier et restaurer vos sauvegardes."
  de:
    tagline: "Verwalten Sie Ihre Dateisicherungen ganz einfach per Web"
    summary: "Ersetzen Sie komplexe Befehle durch eine übersichtliche Benutzeroberfläche zum Erstellen und Wiederherstellen."
---

### What it does in plain English
This application gives you a friendly web dashboard to handle secure data backups without touching a command line. You can monitor storage health, schedule regular snapshots, and browse past archives with just a few clicks. It connects your backup archives securely and sends you alerts if anything needs your attention.

### Who it's for
* Everyday computer users who want secure, automated backups without learning command-line tools.
* System administrators looking for a centralized dashboard to track backup health across multiple machines.
* Anyone who values data privacy and wants total control over their encrypted file archives.

### Key features
* Visual dashboard displaying storage health, recent backup activity, and schedule statuses.
* Live progress tracking and straightforward file restoration workflows without command-line input.
* Automated scheduling with pre- and post-backup action hooks.
* Flexible official project page management supporting local drives, secure shell, and network shares.
* Instant alert notifications through over one hundred messaging and notification services.

### How to install (Download)
You can run the application instantly using Docker by pulling the container image or running:
```bash
docker run -d \
  --name borg-web-ui \
  -p 8081:8081 \
  -v borg_data:/data \
  -v borg_cache:/home/borg/.cache/borg \
  -v /home/yourusername:/local:rw \
  ainullcode/borg-ui:latest
```
Access the app locally at `http://localhost:8081` using the default credentials `admin` / `admin123`.

Alternatively, for Debian or Ubuntu host setups, download and run the official automated setup script:
[Download install.sh](https://github.com/karanhudia/borg-ui/releases/download/v2.4.10/install.sh)

For verification checksums and detailed native cloud setup options, visit the [official installation guide](https://docs.borgui.com/installation).

### Pros and Cons
* **Pros:** Clean modern interface, eliminates complex command-line steps, supports automation and instant notifications.
* **Cons:** Requires a self-hosted environment or server container setup to run continuously.

### Sponsored Partner Tools (#ad)
*Optional commercial services unrelated to the open-source developer. Clicking an `#ad` link helps fund HubHum at no extra cost to you.*
* **InterServer:** Launch and host self-hosted web apps 24/7 on managed Linux cloud VPS servers starting at $3/month — [InterServer](https://www.interserver.net/r/1196747?id=hubhum_01_MER008) (#ad)
* **Hosting.com (ex A2 Hosting):** High-speed NVMe Turbo cloud hosting optimized for self-hosted web applications, databases, and sites — [Hosting.com (ex A2 Hosting)](https://hosting.com/?utm_source=fp_affiliate&utm_medium=15437677&utm_campaign=42825&utm_content=affiliates&fpr=h37jvi&subid=hubhum_01_MER062) (#ad)
* **NameSilo:** Register custom domains at wholesale prices with free lifetime WHOIS privacy and instant DNS setup — [NameSilo](https://www.namesilo.com/?rid=b01c445hx&subid=hubhum_01_MER007) (#ad)

**Official Source & Credits:** [Official Source / Credits](https://github.com/karanhudia/borg-ui)
