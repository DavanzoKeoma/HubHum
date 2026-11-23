---
title: "Cloudflare DDNS"
slug: "cloudflare-ddns"
tagline: "Keep your home network accessible remotely."
summary: "This tool automatically updates your domain name settings whenever your home internet IP address changes."
tags: ["networking", "cloudflare", "automation"]
is_webapp: true
app_type: "selfhosted"
category: "Web Apps & Cloud"
icon: "/icons/cloudflare-ddns.png"
stars: 4572
source_url: "https://github.com/timothymiller/cloudflare-ddns"
download_url: "https://timknowsbest.com/free-dynamic-dns"
downloadUrl: "https://timknowsbest.com/free-dynamic-dns"
download_label: "Official Setup & Docs →"
license: "Open Source (GPL v3)"
scouting_tier: "tier2_webapp"
operatingSystem: "Self-Hosted / Browser"
applicationCategory: "BusinessApplication"
priceCurrency: "USD"
price: "0"
affiliate_merchant_id: "MER_008"
affiliate_name: "InterServer"
affiliate_url: "https://www.interserver.net/r/1196747?id=hubhum_01_MER008"
affiliate_pitch: "Prefer not to configure a server manually? Launch it in 1 click on managed cloud hosting."
ai_provider: "tier1_gemini:gemini-3.1-flash-lite"
featured_weekly: true
updated_at: "2026-11-21"
i18n:
  it:
    tagline: "Accedi alla tua rete domestica da remoto."
    summary: "Questo strumento aggiorna automaticamente le impostazioni del tuo dominio ogni volta che cambia l'indirizzo IP di casa."
  es:
    tagline: "Accede a tu red doméstica de forma remota."
    summary: "Esta herramienta actualiza automáticamente la configuración de tu dominio cada vez que cambia tu dirección IP de casa."
  fr:
    tagline: "Accédez à votre réseau domestique à distance."
    summary: "Cet outil met à jour automatiquement les paramètres de votre domaine chaque fois que votre adresse IP domestique change."
  de:
    tagline: "Greifen Sie aus der Ferne auf Ihr Heimnetzwerk zu."
    summary: "Dieses Tool aktualisiert automatisch Ihre Domain-Einstellungen, sobald sich Ihre IP-Adresse zu Hause ändert."
---

### What it does in plain English
Many home internet connections change their public address periodically, which can break access to your home servers or smart devices. This tool monitors your current address and instantly notifies your domain provider to ensure your custom web address always points to the right place. It runs quietly in the background, ensuring your remote connections stay active without any manual intervention.

### Who it's for
* Home lab enthusiasts who host their own websites or file servers.
* People who need reliable remote access to home security cameras or smart home hubs.

### Key features
* **Automatic Updates:** Constantly checks for IP changes and updates your records so you never lose connection.
* **Multi-Domain Support:** Manages multiple domains and subdomains simultaneously, including wildcard support.
* **Outage Protection:** Safely ignores bad data to prevent your website from going offline due to temporary network glitches.
* **Notification Alerts:** Sends messages to services like Discord, Slack, or Telegram if an update fails or succeeds.
* **Lightweight:** Designed to use minimal computer resources, making it perfect for small home servers.

### How to install (Download)
This tool is designed to run as a containerized application. You can find the official image and setup instructions on the [Docker Hub page](https://hub.docker.com/r/timothyjmiller/cloudflare-ddns). For detailed guides on how to get started, visit the [official project website](https://timknowsbest.com/free-dynamic-dns).

### Pros and Cons
* **Pros:** Extremely lightweight, supports both IPv4 and IPv6, and offers robust error handling to prevent accidental downtime.
* **Cons:** Requires basic knowledge of how to configure environment variables and set up a Cloudflare API token.

### Sponsored Partner Tools (#ad)
*Optional commercial services unrelated to the open-source developer. Clicking an `#ad` link helps fund HubHum at no extra cost to you.*
* **InterServer:** Launch and host self-hosted web apps 24/7 on managed Linux cloud VPS servers starting at $3/month — [InterServer](https://www.interserver.net/r/1196747?id=hubhum_01_MER008) (#ad)
* **Hosting.com (ex A2 Hosting):** High-speed NVMe Turbo cloud hosting optimized for self-hosted web applications, databases, and sites — [Hosting.com (ex A2 Hosting)](https://hosting.com/?utm_source=fp_affiliate&utm_medium=15437677&utm_campaign=42825&utm_content=affiliates&fpr=h37jvi&subid=hubhum_01_MER062) (#ad)
* **NameSilo:** Register custom domains at wholesale prices with free lifetime WHOIS privacy and instant DNS setup — [NameSilo](https://www.namesilo.com/?rid=b01c445hx&subid=hubhum_01_MER007) (#ad)

**Official Source & Credits:** [Official Source / Credits](https://github.com/timothymiller/cloudflare-ddns)
