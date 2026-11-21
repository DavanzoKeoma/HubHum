---
title: "Magnetissimo"
slug: "magnetissimo"
tagline: "A smart, self-hosted torrent search engine"
summary: "Magnetissimo searches multiple torrent sites at once and saves the results to your own private, searchable database."
tags: ["torrent", "search", "self-hosted"]
is_webapp: true
app_type: "selfhosted"
category: "Web Apps & Cloud"
icon: "/icons/magnetissimo.png"
stars: 3111
source_url: "https://github.com/sergiotapia/magnetissimo"
download_url: "https://discord.gg/PWYfybKfcw"
downloadUrl: "https://discord.gg/PWYfybKfcw"
download_label: "Official Setup & Docs →"
license: "Open Source (MIT)"
scouting_tier: "tier2_webapp"
operatingSystem: "Self-Hosted / Browser"
applicationCategory: "BusinessApplication"
priceCurrency: "USD"
price: "0"
affiliate_merchant_id: "MER_047"
affiliate_name: "PureVPN"
affiliate_url: "https://billing.purevpn.com/aff.php?aff=49386762&subid=hubhum_01_MER047"
affiliate_pitch: "Protect your connection before downloading or using this app."
ai_provider: "tier1_gemini:gemini-3.1-flash-lite"
featured_weekly: true
updated_at: "2026-11-21"
i18n:
  it:
    tagline: "Un motore di ricerca torrent intelligente"
    summary: "Magnetissimo interroga più siti torrent contemporaneamente e salva i risultati nel tuo database privato e ricercabile."
  es:
    tagline: "Un buscador de torrents inteligente"
    summary: "Magnetissimo busca en varios sitios de torrents a la vez y guarda los resultados en tu propia base de datos privada."
  fr:
    tagline: "Un moteur de recherche torrent intelligent"
    summary: "Magnetissimo interroge plusieurs sites de torrents simultanément et enregistre les résultats dans votre base de données privée."
  de:
    tagline: "Eine intelligente Suchmaschine für Torrents"
    summary: "Magnetissimo durchsucht mehrere Torrent-Seiten gleichzeitig und speichert die Ergebnisse in deiner privaten, durchsuchbaren Datenbank."
---

### What it does in plain English
Magnetissimo acts as a central hub that queries multiple popular torrent websites simultaneously whenever you perform a search. It automatically collects and organizes the results into a local database, making future searches for the same content instant. You can also run a background crawler to discover new files directly from the peer-to-peer network.

### Who it's for
* Media enthusiasts who want to organize and search across multiple content sources from one single interface.
* Power users who manage home media servers and want to automate how they find and track new files.

### Key features
* **Unified Search:** Queries eight different torrent sites at once and displays results in a clean, live-updating interface.
* **Local Indexing:** Saves every search result to a local database, so you don't have to re-query external sites for popular files.
* **Smart Filtering:** Includes advanced search operators to filter by file size, age, and number of seeders.
* **Media Server Integration:** Works as a compatible indexer for popular automated media management tools.
* **Optional DHT Crawler:** Can actively discover torrents directly from the peer-to-peer network without relying on external websites.

### How to install (Download)
Magnetissimo is designed to be run as a self-hosted application. The easiest way to get started is using Docker:

1. Create a file named `compose.yaml` with the configuration provided in the [Official Source](https://github.com/sergiotapia/magnetissimo).
2. Run `docker compose up -d` in your terminal.
3. Access your dashboard by opening `http://localhost:4000` in your web browser.

For community support and updates, you can join the [Official Discord Server](https://discord.gg/PWYfybKfcw).

### Pros and Cons
* **Pros:** Completely self-hosted, supports automated media management tools, and provides a fast, ad-free search experience.
* **Cons:** Requires basic knowledge of setting up containerized software and may require a VPN for privacy when interacting with peer-to-peer networks.

### Sponsored Partner Tools (#ad)
*Optional commercial services unrelated to the open-source developer. Clicking an `#ad` link helps fund HubHum at no extra cost to you.*
* **PureVPN:** Optional encrypted VPN service for private connections on public Wi-Fi — [PureVPN](https://billing.purevpn.com/aff.php?aff=49386762&subid=hubhum_01_MER047) (#ad)
* **Surfshark VPN:** Optional encrypted VPN service across desktop and mobile devices — [Surfshark VPN](https://surfshark.com/?subid=hubhum_01_MER089) (#ad)
* **Private Internet Access:** Optional privacy-focused VPN client for multiple devices — [Private Internet Access](https://www.privateinternetaccess.com/?subid=hubhum_01_MER048) (#ad)

**Official Source & Credits:** [Official Source / Credits](https://github.com/sergiotapia/magnetissimo)
