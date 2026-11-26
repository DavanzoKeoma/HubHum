---
title: "uwsgi-nginx-docker"
slug: "uwsgi-nginx-docker"
tagline: "Run Python web apps in containers easily."
summary: "Bundle Python web applications with uWSGI and Nginx inside a single container for straightforward deployment."
tags: ["self-hosted", "nginx", "uwsgi"]
is_webapp: true
app_type: "selfhosted"
category: "Web Apps & Cloud"
icon: "/icons/uwsgi-nginx-docker.png"
stars: 661
source_url: "https://github.com/tiangolo/uwsgi-nginx-docker"
download_url: "https://hub.docker.com/r/tiangolo/uwsgi-nginx/"
downloadUrl: "https://hub.docker.com/r/tiangolo/uwsgi-nginx/"
download_label: "Official Setup & Docs →"
license: "Open Source (Apache 2.0)"
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
updated_at: "2026-11-24"
i18n:
  it:
    tagline: "Esegui app web Python nei contenitori facilmente."
    summary: "Raggruppa applicazioni web Python con uWSGI e Nginx in un unico contenitore per una facile pubblicazione."
  es:
    tagline: "Ejecuta aplicaciones web Python en contenedores."
    summary: "Empaqueta aplicaciones web de Python con uWSGI y Nginx dentro de un solo contenedor para facilitar su despliegue."
  fr:
    tagline: "Exécutez des applications web Python facilement."
    summary: "Regroupez des applications web Python avec uWSGI et Nginx dans un seul conteneur pour simplifier le déploiement."
  de:
    tagline: "Python-Web-Apps einfach in Containern ausführen."
    summary: "Bündeln Sie Python-Webanwendungen mit uWSGI und Nginx in einem einzigen Container für ein unkompliziertes Hosting."
---

### What it does in plain English
This project provides a ready-to-use template that combines a Python application server with a high-performance web server inside a single isolated environment. It allows developers to package their website files and startup instructions cleanly so they can run reliably on any computer or cloud server. Although the original tool is no longer actively updated by its creator, it remains a helpful blueprint for understanding how to structure containerized web services.

### Who it's for
* Python developers looking to understand container architecture for web applications.
* System administrators maintaining legacy container setups that rely on combined server layers.
* Students exploring how web servers and application servers communicate behind the scenes.

### Key features
* Combines a fast web server and a Python application server in one neat package.
* Automatically detects and starts application files without complex setup steps.
* Supports customizable worker process counts to handle varying site traffic loads.
* Allows pre-start scripts to run database upgrades automatically before launching.
* Configurable upload size limits and network ports through simple environment variables.

### How to install (Download)
No installation files are provided since this is a container base image template. You can view the official image details and tagged versions on the [Docker Hub Image Page](https://hub.docker.com/r/tiangolo/uwsgi-nginx/).

### Pros and Cons
* **Pros:** Simplifies combining multiple server layers; highly configurable via environment variables; well-documented historic blueprint.
* **Cons:** Officially deprecated by the author; newer setups prefer running separate lightweight processes; Python Alpine tags can cause complex build issues.

### Sponsored Partner Tools (#ad)
*Optional commercial services unrelated to the open-source developer. Clicking an `#ad` link helps fund HubHum at no extra cost to you.*
* **InterServer:** Launch and host self-hosted web apps 24/7 on managed Linux cloud VPS servers starting at $3/month — [InterServer](https://www.interserver.net/r/1196747?id=hubhum_01_MER008) (#ad)
* **Hosting.com (ex A2 Hosting):** High-speed NVMe Turbo cloud hosting optimized for self-hosted web applications, databases, and sites — [Hosting.com (ex A2 Hosting)](https://hosting.com/?utm_source=fp_affiliate&utm_medium=15437677&utm_campaign=42825&utm_content=affiliates&fpr=h37jvi&subid=hubhum_01_MER062) (#ad)
* **NameSilo:** Register custom domains at wholesale prices with free lifetime WHOIS privacy and instant DNS setup — [NameSilo](https://www.namesilo.com/?rid=b01c445hx&subid=hubhum_01_MER007) (#ad)

**Official Source & Credits:** [Official Source / Credits](https://github.com/tiangolo/uwsgi-nginx-docker)
