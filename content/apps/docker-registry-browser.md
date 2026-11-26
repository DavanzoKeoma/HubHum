---
title: "docker-registry-browser"
slug: "docker-registry-browser"
tagline: "Visual web dashboard for software registries"
summary: "Browse, inspect, and clean up stored software packages and image tags using a friendly visual web interface."
tags: ["self-hosted", "web-interface", "registry", "management"]
is_webapp: true
app_type: "selfhosted"
category: "Web Apps & Cloud"
icon: "/icons/docker-registry-browser.png"
stars: 701
source_url: "https://github.com/klausmeyer/docker-registry-browser"
download_url: "https://hub.docker.com/r/klausmeyer/docker-registry-browser/"
downloadUrl: "https://hub.docker.com/r/klausmeyer/docker-registry-browser/"
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
updated_at: "2026-11-24"
i18n:
  it:
    tagline: "Dashboard web per registri software"
    summary: "Esamina, controlla e pulisci i pacchetti software salvati tramite un'interfaccia web semplice e intuitiva."
  es:
    tagline: "Panel web para registros de software"
    summary: "Explora, inspecciona y limpia paquetes de software guardados mediante una interfaz web visual y amigable."
  fr:
    tagline: "Tableau de bord web pour registres logiciels"
    summary: "Parcourez, inspectez et nettoyez les paquets logiciels enregistrés grâce à une interface web claire et intuitive."
  de:
    tagline: "Web-Dashboard für Software-Registries"
    summary: "Durchsuchen, prüfen und bereinigen Sie gespeicherte Softwarepakete über eine übersichtliche Benutzeroberfläche."
---

### What it does in plain English
This tool provides an easy-to-use visual dashboard for managing your private software container registries. Instead of typing complex commands into a terminal, you can browse through saved application versions, inspect individual release tags, and delete old files directly from your web browser. It connects smoothly to standard registry systems to help development teams keep their storage clean and organized.

### Who it's for
* Software developers managing private container registries
* System administrators who need a quick visual overview of stored software images
* DevOps teams looking to clean up old release tags without using command-line tools

### Key features
* Clear visual overview of all stored software project pages
* Detailed breakdown of individual release tags and file versions
* Built-in option to delete outdated or unused tags safely
* Lightweight web application that starts up quickly using container runners

### How to install (Download)
You can access the official container package page and instructions on the [Docker Hub Registry Page](https://hub.docker.com/r/klausmeyer/docker-registry-browser/). 

To run it locally or on your server, use a container runner with a secure secret key:
```shell
$ docker run --name registry-browser -e SECRET_KEY_BASE="your-generated-secret-key" -p 8080:8080 klausmeyer/docker-registry-browser
```
Please read the [Official Documentation](https://github.com/klausmeyer/docker-registry-browser/blob/master/docs/README.md) for detailed configuration options.

### Pros and Cons
* **Pros:** Free and open source under the MIT License, provides a clean graphical view instead of text commands, easy to set up.
* **Cons:** Requires a basic understanding of running container software, configuration depends on environment variables.

### Sponsored Partner Tools (#ad)
*Optional commercial services unrelated to the open-source developer. Clicking an `#ad` link helps fund HubHum at no extra cost to you.*
* **★ Top Recommended — InterServer:** Launch and host self-hosted web apps 24/7 on managed Linux cloud VPS servers starting at $3/month — [**Activate InterServer →**](https://www.interserver.net/vps?id=1196747&sid=hubhum_01_MER008) (#ad)
* **GreenGeeks:** Eco-friendly 300% green-energy SSD hosting with free SSL, nightly backups, and 1-click app installers — [GreenGeeks](https://www.greengeeks.com/track/affiliatechproject/cp-ffltc/lp-1?subid=hubhum_01_MER063) (#ad)
* **Hosting.com (ex A2 Hosting):** High-speed NVMe Managed VPS and WordPress cloud hosting optimized for self-hosted apps and sites — [Hosting.com (ex A2 Hosting)](https://hosting.com/hosting/vps-hosting/managed/linux/?utm_source=fp_affiliate&utm_medium=15437677&utm_campaign=42825&utm_content=affiliates&fpr=h37jvi&subid=hubhum_01_MER062) (#ad)

**Official Source & Credits:** [Official Source / Credits](https://github.com/klausmeyer/docker-registry-browser)
