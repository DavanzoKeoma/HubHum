"""Autonomous 5-Level Inverse-Pyramid SEO Topic Cluster Orchestrator for HubHum."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from validator_sanitizer import split_frontmatter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_APPS_DIR = PROJECT_ROOT / "content" / "apps"
CONTENT_GUIDES_DIR = PROJECT_ROOT / "content" / "guides"
MANIFEST_PATH = PROJECT_ROOT / "data" / "clusters_manifest.json"
APP_CLUSTER_MAP_PATH = PROJECT_ROOT / "src" / "data" / "app_cluster_map.json"

MIN_PILLAR_APPS = 10
MIN_SUBPILLAR_APPS = 6

MACRO_DEFINITIONS: list[dict[str, object]] = [
    {
        "category": "Video & Audio",
        "macro_slug": "video-audio",
        "pillar_title": "Best Free Video & Audio Software (Plain-English Guide)",
        "pillar_summary": "Compare free desktop editors, media players, audio tools, and streaming apps explained without technical jargon.",
        "subpillars": [
            {
                "sub_slug": "free-video-editors",
                "sub_topic": "Free Video Editors, Cutters & Converters",
                "keywords": ("video", "handbrake", "cutter", "lossless", "transcod", "convert", "bili23", "youtube", "yt-dlp", "screen", "record"),
                "sub_summary": "Top free tools for cutting clips, shrinking large video files, and saving online media cleanly.",
            },
            {
                "sub_slug": "audio-media-players",
                "sub_topic": "Audio Editors & Music Players",
                "keywords": ("audio", "music", "audacity", "spotif", "navidrome", "finetune", "vlc", "mpv", "sound", "equalizer"),
                "sub_summary": "Reliable free desktop and cloud players for organizing music libraries, editing audio tracks, and clear playback.",
            },
        ],
    },
    {
        "category": "Graphics & Design",
        "macro_slug": "graphics-design",
        "pillar_title": "Best Free Graphics, Photo & Creative Design Tools",
        "pillar_summary": "Discover free screenshot tools, image optimizers, photo galleries, and 3D creative software for everyday projects.",
        "subpillars": [
            {
                "sub_slug": "photo-image-tools",
                "sub_topic": "Photo Optimizers, Galleries & Screen Capture",
                "keywords": ("photo", "image", "flameshot", "screenshot", "photoprism", "koharu", "diffusion", "optim"),
                "sub_summary": "Free creative apps for compressing photos, capturing crisp screenshots, and organizing visual collections.",
            },
            {
                "sub_slug": "3d-visual-design-tools",
                "sub_topic": "3D Modeling & Visual Interface Studios",
                "keywords": ("3d", "cura", "slicer", "dreamfusion", "designer", "ui", "ux", "widgets", "slint", "tkinter"),
                "sub_summary": "Accessible free software for 3D printing preparation, visual layouts, and interactive prototypes.",
            },
        ],
    },
    {
        "category": "Security & Privacy",
        "macro_slug": "security-privacy",
        "pillar_title": "Best Free Security, Privacy & Password Tools",
        "pillar_summary": "Protect passwords, monitor network traffic, and declutter operating systems safely with transparent free software.",
        "subpillars": [
            {
                "sub_slug": "password-network-privacy",
                "sub_topic": "Password Managers, VPNs & Network Monitors",
                "keywords": ("password", "keepass", "vpn", "singbox", "v2ray", "sniffnet", "firewall", "safeline", "ipsec", "airgorah", "marauder"),
                "sub_summary": "Verified free tools to lock down logins, inspect network connections, and protect your everyday browsing.",
            },
            {
                "sub_slug": "system-cleaners-auditors",
                "sub_topic": "Privacy Cleaners & System Auditors",
                "keywords": ("bleachbit", "debloat", "sophia", "win11", "gitleaks", "sherlock", "maigret", "mole", "termix", "pentagi", "pangolin"),
                "sub_summary": "Free system cleanup utilities and privacy auditing tools that remove unnecessary bloat and tracking.",
            },
        ],
    },
    {
        "category": "Productivity",
        "macro_slug": "productivity",
        "pillar_title": "Best Free Productivity, Notes & Workspace Apps",
        "pillar_summary": "Get more done every day with free note-taking apps, window managers, file organizers, and workflow tools.",
        "subpillars": [
            {
                "sub_slug": "notes-knowledge-apps",
                "sub_topic": "Free Note-Taking & Knowledge Apps",
                "keywords": ("note", "joplin", "markdown", "knowledge", "writing", "doc", "awesome", "pdf", "obsidian", "editor", "dbx"),
                "sub_summary": "Distraction-free note-taking and personal knowledge organizers with offline control over your writing.",
            },
            {
                "sub_slug": "desktop-workflow-helpers",
                "sub_topic": "Window Switchers & Everyday Workflow Helpers",
                "keywords": ("window", "menu", "mouse", "switch", "alt-tab", "thaw", "ice", "uniget", "dbeaver", "bruno", "automa"),
                "sub_summary": "Lightweight free helpers that organize windows, speed up repetitive tasks, and tidy up your computer.",
            },
        ],
    },
    {
        "category": "Web Apps & Cloud",
        "macro_slug": "web-apps-cloud",
        "pillar_title": "Best Free Web Apps, Dashboards & Cloud Platforms",
        "pillar_summary": "Run modern dashboards, publishing tools, bookmark hubs, and family cloud apps directly in your browser.",
        "subpillars": [
            {
                "sub_slug": "self-hosted-cloud-apps",
                "sub_topic": "Personal Cloud Hubs, Wikis & Bookmark Apps",
                "keywords": ("wiki", "bookmark", "linkwarden", "karakeep", "ghost", "siyuan", "trilium", "memos", "immich", "archive", "resume", "hubhum"),
                "sub_summary": "Browser-based workspaces for saving links, publishing articles, and backing up photos privately.",
            },
            {
                "sub_slug": "server-dashboards-automation",
                "sub_topic": "Server Dashboards, Monitoring & Cloud Panels",
                "keywords": ("dashboard", "casaos", "coolify", "dokploy", "dockge", "uptime", "beszel", "dashy", "homepage", "glance", "analytics", "dify", "appsmith"),
                "sub_summary": "Visual cloud panels that replace complex commands with one clean browser control center.",
            },
        ],
    },
    {
        "category": "Utilities & Power Tools",
        "macro_slug": "utilities-power-tools",
        "pillar_title": "Best Free Power Tools, Terminals & System Utilities",
        "pillar_summary": "Fast command-line tools, modern terminal apps, and smart file finders explained clearly without jargon.",
        "subpillars": [
            {
                "sub_slug": "modern-terminal-apps",
                "sub_topic": "Modern Terminal Emulators & Fast File Finders",
                "keywords": ("alacritty", "wezterm", "kitty", "tabby", "waveterm", "windterm", "conemu", "cool-retro", "yazi", "broot", "fzf", "ripgrep", "bat", "fd", "zoxide", "zellij", "tmux"),
                "sub_summary": "Speed up everyday navigation and file searches with fast, clean command-line replacements.",
            },
            {
                "sub_slug": "automation-power-utilities",
                "sub_topic": "Automation & System Power Utilities",
                "keywords": ("lazygit", "git", "aider", "agent", "powershell", "vagrant", "playwright", "puppeteer", "ohmyzsh", "fastfetch", "asciinema"),
                "sub_summary": "Time-saving automation utilities that simplify repetitive technical routines for busy makers.",
            },
        ],
    },
]


def _escape_yaml(val: str) -> str:
    return " ".join(str(val or "").replace("\r", " ").replace("\n", " ").replace('"', "'").split()).strip()


def _format_app_type(app_type: str) -> str:
    if app_type == "webapp":
        return "Cloud Web App"
    if app_type == "cli":
        return "CLI Tool"
    return "Desktop App"


def _load_all_apps() -> list[dict]:
    apps: list[dict] = []
    for p in sorted(CONTENT_APPS_DIR.glob("*.md")):
        meta, _ = split_frontmatter(p.read_text(encoding="utf-8"))
        slug = str(meta.get("slug") or p.stem)
        app_type = str(meta.get("app_type") or ("webapp" if meta.get("is_webapp") else "desktop"))
        apps.append(
            {
                "slug": slug,
                "title": str(meta.get("title") or slug),
                "summary": str(meta.get("summary") or "").strip(),
                "category": str(meta.get("category") or "Productivity").strip(),
                "app_type": app_type,
                "is_webapp": bool(meta.get("is_webapp")),
                "stars": int(meta.get("stars") or 0),
                "license": str(meta.get("license") or "Open Source"),
                "operatingSystem": str(meta.get("operatingSystem") or "Windows, macOS, Linux"),
                "tags": [str(t) for t in (meta.get("tags") or [])],
            }
        )
    apps.sort(key=lambda a: a["stars"], reverse=True)
    return apps


def _write_guide_file(
    rel_path: str,
    frontmatter_data: dict[str, object],
    body_markdown: str,
) -> Path:
    target = CONTENT_GUIDES_DIR / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = ["---"]
    for k in (
        "title",
        "slug",
        "level",
        "macro_category",
        "macro_slug",
        "sub_topic",
        "sub_slug",
        "intent",
        "summary",
        "parent_slug",
    ):
        val = frontmatter_data.get(k)
        if val is None or val == "":
            continue
        if isinstance(val, int):
            lines.append(f"{k}: {val}")
        else:
            lines.append(f'{k}: "{_escape_yaml(str(val))}"')

    for list_k in ("child_slugs", "sibling_slugs", "app_slugs"):
        items = frontmatter_data.get(list_k) or []
        if isinstance(items, list):
            encoded = ", ".join(f'"{_escape_yaml(str(x))}"' for x in items)
            lines.append(f"{list_k}: [{encoded}]")

    lines.append(f'updated_at: "{frontmatter_data.get("updated_at")}"')
    lines.append("---")
    target.write_text("\n".join(lines) + "\n\n" + body_markdown.strip() + "\n", encoding="utf-8")
    return target


def _assign_apps_to_subpillars(macro_apps: list[dict], sub_defs: list[dict]) -> list[tuple[dict, list[dict]]]:
    """Deterministically assign apps across sub-pillars and fold any sub-pillar below threshold."""
    buckets: dict[str, list[dict]] = {str(sd["sub_slug"]): [] for sd in sub_defs}
    first_sub_slug = str(sub_defs[0]["sub_slug"])

    for idx, app in enumerate(macro_apps):
        blob = f"{app['slug']} {app['title']} {app['summary']} {' '.join(app['tags'])}".lower()
        matched_slug: str | None = None
        for sd in sub_defs:
            kws: tuple[str, ...] = sd["keywords"]  # type: ignore[assignment]
            if any(k in blob for k in kws):
                matched_slug = str(sd["sub_slug"])
                break
        if matched_slug is None:
            # Balance evenly across the two sub-pillars when keywords tie
            matched_slug = str(sub_defs[idx % len(sub_defs)]["sub_slug"])
        buckets[matched_slug].append(app)

    # Enforce strict >= 6 app threshold per sub-pillar (fold any sparse bucket so zero thin pages exist)
    valid_pairs: list[tuple[dict, list[dict]]] = []
    overflow: list[dict] = []
    for sd in sub_defs:
        s_slug = str(sd["sub_slug"])
        items = buckets[s_slug]
        if len(items) >= MIN_SUBPILLAR_APPS:
            valid_pairs.append((sd, items))
        else:
            overflow.extend(items)

    if overflow:
        if valid_pairs:
            valid_pairs[0][1].extend(overflow)
        elif len(macro_apps) >= MIN_SUBPILLAR_APPS:
            valid_pairs.append((sub_defs[0], list(macro_apps)))

    for _, items in valid_pairs:
        items.sort(key=lambda a: a["stars"], reverse=True)
    return valid_pairs


def generate_clusters() -> dict[str, object]:
    """Generate Level 1 Pillars, Level 2 Sub-Pillars, Level 3 Cluster Articles, and manifests."""
    today = datetime.now(timezone.utc).date().isoformat()
    apps = _load_all_apps()

    # Clean stale generated guides so removed/reclassified clusters stay accurate
    if CONTENT_GUIDES_DIR.exists():
        for old_md in CONTENT_GUIDES_DIR.rglob("*.md"):
            old_md.unlink()

    manifest: dict[str, object] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "min_pillar_apps": MIN_PILLAR_APPS,
        "min_subpillar_apps": MIN_SUBPILLAR_APPS,
        "pillars": [],
        "total_guide_pages": 0,
    }
    app_cluster_map: dict[str, dict[str, str]] = {}
    generated_files = 0

    for macro in MACRO_DEFINITIONS:
        category = str(macro["category"])
        macro_slug = str(macro["macro_slug"])
        macro_apps = [a for a in apps if a["category"] == category]
        if len(macro_apps) < MIN_PILLAR_APPS:
            continue

        sub_pairs = _assign_apps_to_subpillars(macro_apps, macro["subpillars"])  # type: ignore[arg-type]
        if not sub_pairs:
            continue

        sub_slugs = [f"{macro_slug}/{sd['sub_slug']}" for sd, _ in sub_pairs]

        # 1. Generate Level 1 Pillar Page
        pillar_apps = macro_apps[:18]
        pillar_bullets = "\n".join(
            f"- **[{a['title']}](/HubHum/apps/{a['slug']}/)** ({_format_app_type(a['app_type'])}, ★ {a['stars']:,}) — {a['summary']}"
            for a in macro_apps[:10]
        )
        pillar_body = f"""## Why Explore Free {category} Software?

This central guide brings together **{len(macro_apps)} verified free applications** in the **{category}** category. Every app listed on HubHum links strictly to official creator channels, translates confusing instructions into plain English, and clearly marks whether a program installs on your computer, opens as a cloud web app, or runs in your terminal.

### Explore Focus Guides Inside {category}

Choose the focus topic below that matches your task best to see step-by-step comparisons, buying alternatives, and troubleshooting checklists.

### Top Featured {category} Software

{pillar_bullets}"""

        _write_guide_file(
            f"{macro_slug}/index.md",
            {
                "title": macro["pillar_title"],
                "slug": macro_slug,
                "level": 1,
                "macro_category": category,
                "macro_slug": macro_slug,
                "intent": "pillar",
                "summary": macro["pillar_summary"],
                "child_slugs": sub_slugs,
                "app_slugs": [a["slug"] for a in pillar_apps],
                "updated_at": today,
            },
            pillar_body,
        )
        generated_files += 1

        manifest_subs = []
        for sd, sub_apps in sub_pairs:
            sub_slug_short = str(sd["sub_slug"])
            sub_full_slug = f"{macro_slug}/{sub_slug_short}"
            sub_topic = str(sd["sub_topic"])

            comp_slug = f"{sub_full_slug}/best-{sub_slug_short}"
            found_slug = f"{sub_full_slug}/how-to-choose-{sub_slug_short}"
            trouble_slug = f"{sub_full_slug}/troubleshooting-{sub_slug_short}"
            article_slugs = [comp_slug, found_slug, trouble_slug]

            for app in sub_apps:
                app_cluster_map[app["slug"]] = {
                    "macro_slug": macro_slug,
                    "macro_title": str(macro["pillar_title"]),
                    "macro_category": category,
                    "sub_slug": sub_full_slug,
                    "sub_title": sub_topic,
                    "comparison_slug": comp_slug,
                    "foundations_slug": found_slug,
                }

            # 2. Generate Level 2 Sub-Pillar Page
            sub_highlights = "\n".join(
                f"- **[{a['title']}](/HubHum/apps/{a['slug']}/)** — {a['summary']} *({_format_app_type(a['app_type'])} · License: {a['license']})*"
                for a in sub_apps[:12]
            )
            sub_body = f"""## Plain-English Overview: {sub_topic}

This topic hub groups **{len(sub_apps)} vetted free tools** specializing in **{sub_topic}** inside **{category}**. Whether you want an easy installer for Windows or Mac or an instant web option, every tool below includes verified official download sources.

### Recommended Reading Guides
Before picking your software, read our practical guides below covering head-to-head comparisons, beginner setup, and common problem fixes.

### All Qualifying Software in This Topic

{sub_highlights}"""

            _write_guide_file(
                f"{sub_full_slug}/index.md",
                {
                    "title": f"{sub_topic} — Top Free Software & Guides",
                    "slug": sub_full_slug,
                    "level": 2,
                    "macro_category": category,
                    "macro_slug": macro_slug,
                    "sub_topic": sub_topic,
                    "sub_slug": sub_slug_short,
                    "intent": "subpillar",
                    "summary": sd["sub_summary"],
                    "parent_slug": macro_slug,
                    "child_slugs": article_slugs,
                    "app_slugs": [a["slug"] for a in sub_apps[:18]],
                    "updated_at": today,
                },
                sub_body,
            )
            generated_files += 1

            # 3A. Level 3 Cluster Article: Comparison & Roundup (TopApp1 vs TopApp2)
            top1 = sub_apps[0]
            top2 = sub_apps[1] if len(sub_apps) > 1 else sub_apps[0]
            table_rows = "\n".join(
                f"| [{a['title']}](/HubHum/apps/{a['slug']}/) | {_format_app_type(a['app_type'])} | {a['operatingSystem']} | ★ {a['stars']:,} | {a['license']} |"
                for a in sub_apps[:6]
            )
            comp_body = f"""## Quick Answer: {top1['title']} vs {top2['title']}

Comparing **{top1['title']}** and **{top2['title']}** comes down to how you prefer to work. **{top1['title']}** stands out as a top community favorite ({top1['stars']:,} GitHub stars) and runs as a **{_format_app_type(top1['app_type'])}**: {top1['summary']} Meanwhile, **{top2['title']}** ({top2['stars']:,} GitHub stars) gives you another trusted free option: {top2['summary']}

### Side-by-Side Comparison

| Software | Format | Systems Supported | Community Stars | License |
| --- | --- | --- | --- | --- |
{table_rows}

### When to Pick Which Option
- **Choose [{top1['title']}](/HubHum/apps/{top1['slug']}/)** if you want the broadest community support and an established tool trusted by thousands of users.
- **Choose [{top2['title']}](/HubHum/apps/{top2['slug']}/)** if its focused features fit your workflow faster without extra clutter.
- Check every individual app card below to review pros, cons, and verified official download links before installing."""

            _write_guide_file(
                f"{sub_full_slug}/best-{sub_slug_short}.md",
                {
                    "title": f"Best Free {sub_topic}: {top1['title']} vs {top2['title']} Compared",
                    "slug": comp_slug,
                    "level": 3,
                    "macro_category": category,
                    "macro_slug": macro_slug,
                    "sub_topic": sub_topic,
                    "sub_slug": sub_slug_short,
                    "intent": "comparison",
                    "summary": f"Compare {top1['title']} vs {top2['title']} and the top free tools for {sub_topic} with clear differences and official downloads.",
                    "parent_slug": sub_full_slug,
                    "sibling_slugs": [found_slug, trouble_slug],
                    "app_slugs": [a["slug"] for a in sub_apps[:8]],
                    "updated_at": today,
                },
                comp_body,
            )
            generated_files += 1

            # 3B. Level 3 Cluster Article: Foundations (What is / How to choose)
            found_picks = sub_apps[:4]
            found_bullets = "\n".join(
                f"- **[{a['title']}](/HubHum/apps/{a['slug']}/)** — {a['summary']}"
                for a in found_picks
            )
            found_body = f"""## How to Choose Free {sub_topic} Without Getting Lost

Switching to free software in **{sub_topic}** lets you avoid recurring monthly fees and keep ownership of your files. Before downloading the first result you see, focus on three practical checks:

1. **Pick the right format for your device:** Desktop apps install directly onto Windows, macOS, or Linux; Cloud Web Apps open straight in a browser; CLI tools run quickly inside a terminal window.
2. **Verify the official creator page:** Every guide on HubHum links strictly to the creator's official page so you avoid bundled adware or fake installer sites.
3. **Start simple:** Look for active community maintenance (shown cleanly on every card via GitHub star counts) so the tool stays compatible with modern operating systems.

### Great Starting Points for Beginners

{found_bullets}"""

            _write_guide_file(
                f"{sub_full_slug}/how-to-choose-{sub_slug_short}.md",
                {
                    "title": f"How to Choose and Use Free {sub_topic} Safely",
                    "slug": found_slug,
                    "level": 3,
                    "macro_category": category,
                    "macro_slug": macro_slug,
                    "sub_topic": sub_topic,
                    "sub_slug": sub_slug_short,
                    "intent": "foundations",
                    "summary": f"Beginner-friendly plain-English guide explaining what {sub_topic} tools do, desktop vs cloud formats, and how to pick safely.",
                    "parent_slug": sub_full_slug,
                    "sibling_slugs": [comp_slug, trouble_slug],
                    "app_slugs": [a["slug"] for a in sub_apps[:6]],
                    "updated_at": today,
                },
                found_body,
            )
            generated_files += 1

            # 3C. Level 3 Cluster Article: Problems & Solutions (Troubleshooting)
            trouble_picks = sub_apps[:5]
            trouble_body = f"""## Fixing Common Problems with Free {sub_topic}

Moving away from expensive paid tools occasionally brings small setup hiccups. Here are the most common hurdles everyday users face with **{sub_topic}** and the fastest ways to solve them:

### 1. Confusion Between Desktop Installers and Command-Line Tools
Some free projects only run inside a terminal window (`CLI Tool`), while others provide a point-and-click installer (`Desktop App`). Always check the transparent badge at the top of any HubHum card before downloading so you pick an interface you feel comfortable using.

### 2. Unsure Which Official File to Download
Windows users usually want `.exe` or `.msi` installers, macOS users want `.dmg`, and Android users want `.apk`. Every HubHum software page filters out technical source bundles and highlights the direct installer link at the top.

### 3. Heavy Feature Bloat Slowing Down Older Computers
If commercial suites freeze on your laptop, lightweight open-source tools like **[{top1['title']}](/HubHum/apps/{top1['slug']}/)** or **[{top2['title']}](/HubHum/apps/{top2['slug']}/)** give you clean performance without background tracking or forced logins.

### Recommended Reliable Alternatives

""" + "\n".join(f"- **[{a['title']}](/HubHum/apps/{a['slug']}/)** ({_format_app_type(a['app_type'])}) — {a['summary']}" for a in trouble_picks)

            _write_guide_file(
                f"{sub_full_slug}/troubleshooting-{sub_slug_short}.md",
                {
                    "title": f"Common {sub_topic} Problems & How to Fix Them",
                    "slug": trouble_slug,
                    "level": 3,
                    "macro_category": category,
                    "macro_slug": macro_slug,
                    "sub_topic": sub_topic,
                    "sub_slug": sub_slug_short,
                    "intent": "troubleshooting",
                    "summary": f"Practical troubleshooting tips for installer formats, compatibility issues, and performance when using free {sub_topic} tools.",
                    "parent_slug": sub_full_slug,
                    "sibling_slugs": [comp_slug, found_slug],
                    "app_slugs": [a["slug"] for a in trouble_picks],
                    "updated_at": today,
                },
                trouble_body,
            )
            generated_files += 1

            manifest_subs.append(
                {
                    "sub_slug": sub_full_slug,
                    "sub_topic": sub_topic,
                    "app_count": len(sub_apps),
                    "articles": article_slugs,
                }
            )

        manifest["pillars"].append(  # type: ignore[attr-defined]
            {
                "macro_slug": macro_slug,
                "category": category,
                "app_count": len(macro_apps),
                "subpillars": manifest_subs,
            }
        )

    manifest["total_guide_pages"] = generated_files
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    APP_CLUSTER_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
    APP_CLUSTER_MAP_PATH.write_text(json.dumps(app_cluster_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HubHum 5-Level Topic Cluster Orchestrator")
    parser.add_argument("--generate", action="store_true", help="Generate Level 1-3 guides and update cluster manifest")
    args = parser.parse_args()
    res = generate_clusters()
    print(f"[CLUSTERS] Generated {res['total_guide_pages']} guide pages across {len(res['pillars'])} macro-pillars.")
    print(json.dumps(res, indent=2))
