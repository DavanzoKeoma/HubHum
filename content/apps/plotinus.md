---
title: "Plotinus"
slug: "plotinus"
tagline: "Universal command palette for Linux"
summary: "Plotinus adds a searchable command palette to any GTK+ 3 application on Linux."
tags: ["linux", "productivity"]
is_webapp: false
app_type: "desktop"
category: "Productivity"
icon: "/icons/plotinus.png"
stars: 1024
source_url: "https://github.com/p-e-w/plotinus"
download_url: "https://github.com/p-e-w/plotinus/releases"
downloadUrl: "https://github.com/p-e-w/plotinus/releases"
download_label: "Visit Official Site"
license: "Custom Open License"
scouting_tier: "tier1_gui"
operatingSystem: "Linux"
applicationCategory: "UtilitiesApplication"
priceCurrency: "USD"
price: "0"
affiliate_merchant_id: "MER_061"
affiliate_name: "Systeme.io"
affiliate_url: "https://systeme.io/?sa=sa023692845080664785297106081136cf8d3a59ee&subid=hubhum_01_MER061"
affiliate_pitch: "Automate everyday online workflows free forever and safeguard your devices and backups."
ai_provider: "tier2_groq:qwen/qwen3.8-27b"
featured_weekly: true
updated_at: "2026-11-24"
i18n:
  it:
    tagline: "Palette di comandi universale per Linux"
    summary: "Plotinus aggiunge una palette di comandi ricercabile a qualsiasi applicazione GTK+ 3 su Linux."
  es:
    tagline: "Paleta de comandos universal para Linux"
    summary: "Plotinus añade una paleta de comandos buscable a cualquier aplicación GTK+ 3 en Linux."
  fr:
    tagline: "Palette de commandes universelle pour Linux"
    summary: "Plotinus ajoute une palette de commandes recherchable à toute application GTK+ 3 sur Linux."
  de:
    tagline: "Universelles Befehlspalette für Linux"
    summary: "Plotinus fügt jeder GTK+ 3-Anwendung unter Linux eine durchsuchbare Befehlspalette hinzu."
---

### What it does in plain English
Plotinus brings the familiar "command palette" experience from popular code editors to your entire Linux desktop. It works with any program built on the GTK+ 3 toolkit, allowing you to press a shortcut and type to find any action available in that specific app. This tool automatically detects what the application can do, so you never have to hunt through nested menus again.

### Who it's for
* **Power users** who want to navigate complex desktop applications with speed and precision.
* **Linux enthusiasts** who prefer keyboard-driven workflows over mouse-based menu navigation.
* **Developers** who frequently switch between different GTK-based tools and want a consistent way to access features.

### Key features
* **Universal Compatibility:** Works seamlessly with any modern GTK+ 3 application without requiring changes to the app itself.
* **Instant Search:** Type a few letters to filter and execute commands, similar to how you would in a code editor.
* **Automatic Detection:** The tool introspects running applications to list only the actions currently available, adapting to UI changes in real-time.
* **Customizable Shortcuts:** You can change the keyboard combination used to open the palette globally or for specific applications.

### How to install (Download)
Since there are no pre-built installer files available in the latest releases, you must build the tool from source code. This process requires a command-line interface and specific development libraries.

1.  **Install Prerequisites:** Use your system's package manager to install Git, CMake, Vala, and GTK+ 3 development files.
    *   *For Fedora/RHEL:* `sudo dnf install git cmake vala gtk3-devel`
    *   *For Ubuntu/Mint:* `sudo apt-get install git cmake valac libgtk-3-dev`
2.  **Download Source Code:** Clone the project from the official official project page.
    *   `git clone https://github.com/p-e-w/plotinus.git`
3.  **Build and Install:** Navigate to the folder and compile the tool.
    *   `cd plotinus`
    *   `mkdir build && cd build`
    *   `cmake ..`
    *   `make`
    *   `sudo make install`
4.  **Enable the Tool:** You must manually enable Plotinus for your applications by setting an environment variable. Find the path to `libplotinus.so` using `whereis -b libplotinus`, then add `GTK3_MODULES=[path]` to your `/etc/environment` file or run individual apps with this variable set.

### Pros and Cons
* **Pros:** Free and open-source, works with a wide range of Linux applications, significantly speeds up navigation in complex software.
* **Cons:** Requires manual installation from source code, needs specific command-line configuration to enable, only supports GTK+ 3 applications (not all Linux apps).

### Sponsored Partner Tools (#ad)
*Optional commercial services unrelated to the open-source developer. Clicking an `#ad` link helps fund HubHum at no extra cost to you.*
* **★ Top Recommended — Systeme.io:** Free-forever all-in-one platform to build landing pages, newsletters, and automated workflows with zero monthly fees — [**Activate Systeme.io →**](https://systeme.io/?sa=sa023692845080664785297106081136cf8d3a59ee&subid=hubhum_01_MER061) (#ad)
* **AdGuard:** Block intrusive ads, tracking scripts, and phishing domains system-wide across all browsers and desktop apps — [AdGuard](https://adguard.com/?aid=138327&subid=hubhum_01_MER119) (#ad)
* **InterServer:** Launch and host self-hosted web apps 24/7 on managed Linux cloud VPS servers starting at $3/month — [InterServer](https://www.interserver.net/vps?id=1196747&sid=hubhum_01_MER008) (#ad)

**Official Source & Credits:** [Official Source / Credits](https://github.com/p-e-w/plotinus)
