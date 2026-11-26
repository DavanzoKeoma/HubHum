---
title: "RIBs"
slug: "ribs"
tagline: "Cross-platform mobile app architecture framework"
summary: "Build scalable mobile applications using Uber's robust cross-platform architecture framework designed for large engineering teams."
tags: ["mobile", "architecture", "android", "development"]
is_webapp: false
app_type: "desktop"
category: "Productivity"
icon: "/icons/ribs.png"
stars: 7952
source_url: "https://github.com/uber/RIBs"
download_url: "https://eng.uber.com/tag/ribs/"
downloadUrl: "https://eng.uber.com/tag/ribs/"
download_label: "Visit Official Site"
license: "Open Source (Apache 2.0)"
scouting_tier: "tier1_gui"
operatingSystem: "Android"
applicationCategory: "UtilitiesApplication"
priceCurrency: "USD"
price: "0"
affiliate_merchant_id: "MER_061"
affiliate_name: "Systeme.io"
affiliate_url: "https://systeme.io/?sa=sa023692845080664785297106081136cf8d3a59ee&subid=hubhum_01_MER061"
affiliate_pitch: "Automate everyday online workflows free forever and safeguard your devices and backups."
ai_provider: "tier1_gemini:gemini-flash-lite-latest"
featured_weekly: true
updated_at: "2026-11-24"
i18n:
  it:
    tagline: "Framework di architettura per app mobili"
    summary: "Crea app mobili scalabili utilizzando il robusto framework di architettura di Uber per grandi team di ingegneri."
  es:
    tagline: "Framework de arquitectura para apps móviles"
    summary: "Construya aplicaciones móviles escalables utilizando el sólido framework de arquitectura de Uber para equipos grandes."
  fr:
    tagline: "Cadre d'architecture d'applications mobiles"
    summary: "Créez des applications mobiles évolutives grâce au cadre d'architecture robuste d'Uber pour les grandes équipes."
  de:
    tagline: "Mobile App-Architektur-Framework"
    summary: "Erstellen Sie skalierbare mobile Apps mit Ubars robustem Architektur-Framework für große Entwicklungsteams."
---

### What it does in plain English
RIBs is a cross-platform mobile app structure created by Uber to help large engineering teams build massive, reliable applications. It divides your app code into logical pieces called Routers, Interactors, and Builders that keep business rules completely separate from visual layouts. This organized layout lets multiple programmers work on the exact same project simultaneously without stepping on each other's toes.

### Who it's for
* Mobile software engineers building complex, large-scale apps with heavy business logic.
* Development teams needing a shared architecture across both Android and iOS projects.
* Programmers looking for strict testability and isolation of app components.

### Key features
* Driven by business logic rather than traditional visual screen hierarchies.
* Enables shared logic and cross-code reviews between Android and iOS teams.
* Highly testable components that operate in clean isolation for simpler debugging.
* Scalable software foundation proven to handle apps with hundreds of independent components.
* Includes helpful companion tools for code generation and memory leak checks.

### How to install (Download)
To integrate RIBs into your Android project, add the recommended minimum setup dependencies to your `build.gradle` configuration:

```gradle
dependencies {
  annotationProcessor 'com.uber.rib:rib-compiler-test:0.17.0'
  implementation 'com.uber.rib:rib-android:0.17.0'
  testImplementation 'com.uber.rib:rib-test:0.17.0'
}
```

Learn more about getting started, tutorials, and documentation at the [Official RIBs Documentation Website](https://eng.uber.com/tag/ribs/).

### Pros and Cons
* **Pros:** Highly scalable for massive teams, ensures robust testability, keeps business logic clean and isolated.
* **Cons:** Steep learning curve for developers new to the pattern, requires disciplined upfront planning.

### Sponsored Partner Tools (#ad)
*Optional commercial services unrelated to the open-source developer. Clicking an `#ad` link helps fund HubHum at no extra cost to you.*
* **Systeme.io:** Free-forever all-in-one platform to build landing pages, newsletters, and automated workflows with zero monthly fees — [Systeme.io](https://systeme.io/?sa=sa023692845080664785297106081136cf8d3a59ee&subid=hubhum_01_MER061) (#ad)
* **AdGuard:** Block intrusive ads, tracking scripts, and phishing domains system-wide across all browsers and desktop apps — [AdGuard](https://adguard.com/?aid=138327&subid=hubhum_01_MER119) (#ad)
* **InterServer:** Launch and host self-hosted web apps 24/7 on managed Linux cloud VPS servers starting at $3/month — [InterServer](https://www.interserver.net/r/1196747?id=hubhum_01_MER008) (#ad)

**Official Source & Credits:** [Official Source / Credits](https://eng.uber.com/tag/ribs/)
