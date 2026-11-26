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
CONTENT_BUNDLES_DIR = PROJECT_ROOT / "content" / "bundles"
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
                "sub_topic": "Video Cutters, Converters & Downloaders",
                "keywords": ("handbrake", "cutter", "lossless", "transcod", "bili23", "youtube", "yt-dlp", "concat", "subtitle", "video-editor"),
                "sub_summary": "Compare video trimming, file conversion, subtitling, and media downloading tools with honest format details.",
            },
            {
                "sub_slug": "audio-media-players",
                "sub_topic": "Audio Editors & Music Players",
                "keywords": ("audio", "music", "audacity", "spotif", "navidrome", "finetune", "shpotify", "sound", "equalizer", "podcast"),
                "sub_summary": "Reliable desktop and self-hosted players for organizing music libraries, editing audio tracks, and clear playback.",
            },
            {
                "sub_slug": "screen-recorders-streaming",
                "sub_topic": "Screen Recorders, Streaming & Media Players",
                "keywords": ("vlc", "mpv", "obs", "screen", "recorder", "capture", "stream", "player", "media", "video"),
                "sub_summary": "Free screen recorders, desktop media players, and streaming tools that work smoothly on any computer.",
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
                "keywords": ("photo", "image", "flameshot", "screenshot", "photoprism", "koharu", "diffusion", "optim", "drawing"),
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
                "sub_slug": "free-password-managers",
                "sub_topic": "Free Password Managers & Auth Vaults",
                "keywords": ("password", "keepass", "bitwarden", "vaultwarden", "auth", "2fa", "totp", "passkey", "credential"),
                "sub_summary": "Offline and self-hosted password managers and 2FA vaults that keep your logins encrypted under your control.",
            },
            {
                "sub_slug": "password-network-privacy",
                "sub_topic": "Privacy Tools, VPNs & Network Monitors",
                "keywords": ("vpn", "wireguard", "singbox", "v2ray", "sniffnet", "firewall", "safeline", "ipsec", "airgorah", "marauder", "encryption", "privacy"),
                "sub_summary": "Verified free tools to inspect network connections, encrypt traffic, and protect your everyday browsing.",
            },
            {
                "sub_slug": "system-cleaners-auditors",
                "sub_topic": "Privacy Cleaners & System Auditors",
                "keywords": ("bleachbit", "debloat", "sophia", "win11", "gitleaks", "sherlock", "maigret", "mole", "termix", "pentagi", "pangolin", "backup"),
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
                "sub_topic": "Encrypted Notes, Wikis & Knowledge Apps",
                "keywords": ("note", "joplin", "markdown", "knowledge", "writing", "obsidian", "editor", "todo", "calendar"),
                "sub_summary": "Distraction-free note-taking and personal knowledge organizers with offline control over your writing.",
            },
            {
                "sub_slug": "pdf-document-office-tools",
                "sub_topic": "Free PDF, Document & E-Book Tools",
                "keywords": ("pdf", "ebook", "epub", "reader", "doc", "office", "ocr", "scan", "paperless", "rss"),
                "sub_summary": "Everyday open-source software to edit PDFs, read e-books comfortably, organize documents, and scan files.",
            },
            {
                "sub_slug": "desktop-workflow-helpers",
                "sub_topic": "Window Switchers & Everyday Workflow Helpers",
                "keywords": ("window", "menu", "mouse", "switch", "alt-tab", "thaw", "ice", "uniget", "dbeaver", "bruno", "automa", "launcher", "clipboard", "file-manager", "backup"),
                "sub_summary": "Lightweight free helpers that organize windows, speed up repetitive tasks, and tidy up your computer.",
            },
            {
                "sub_slug": "ai-local-assistants-chat",
                "sub_topic": "Local AI Assistants, LLM Studios & Chat Workspaces",
                "keywords": ("ai", "llm", "ollama", "deepseek", "claude", "gpt", "chat", "agent", "prompt", "whisper", "copilot"),
                "sub_summary": "Run private AI chat workspaces, coding helpers, and local language models on your own computer.",
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
                "sub_slug": "self-hosted-cms-blogs",
                "sub_topic": "Self-Hosted CMS, Blogs & Publishing Platforms",
                "keywords": ("cms", "blog", "ghost", "wiki", "outline", "bookstack", "publish", "knowledge-base", "rss"),
                "sub_summary": "Open-source web publishing platforms and team wikis that replace expensive hosted subscriptions.",
            },
            {
                "sub_slug": "self-hosted-cloud-apps",
                "sub_topic": "Personal Cloud Hubs, Photos & File Sharing",
                "keywords": ("bookmark", "linkwarden", "karakeep", "siyuan", "trilium", "memos", "immich", "archive", "resume", "hubhum", "nextcloud", "file-sharing", "cloud-storage", "photo-gallery"),
                "sub_summary": "Browser-based workspaces for saving links, backing up family photos, and sharing cloud storage privately.",
            },
            {
                "sub_slug": "server-dashboards-automation",
                "sub_topic": "Server Dashboards, Monitoring & Cloud Panels",
                "keywords": ("dashboard", "casaos", "coolify", "dokploy", "dockge", "uptime", "beszel", "dashy", "homepage", "glance", "analytics", "dify", "appsmith", "crm", "erp", "invoicing"),
                "sub_summary": "Visual cloud panels that replace complex commands with one clean browser control center.",
            },
            {
                "sub_slug": "home-lab-media-servers",
                "sub_topic": "Home Lab Media Servers, E-Books & Streaming Hubs",
                "keywords": ("media-server", "jellyfin", "audiobookshelf", "kavita", "calibre", "suwayomi", "music-server", "iptv", "stream", "podcast", "radio", "ebook-server"),
                "sub_summary": "Self-hosted streaming servers for organizing movies, music, audiobooks, comics, and household media libraries.",
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


def _dedup_words(text: str) -> str:
    """Prevent accidental adjacent duplicate words like 'Free Free' in generated headings."""
    return re.sub(r"\b(Free)\s+\1\b", r"\1", str(text or ""), flags=re.IGNORECASE)


def _format_app_type(app_type: str) -> str:
    mapping = {
        "desktop": "Desktop App",
        "webapp": "Cloud Web App",
        "selfhosted": "Self-Hosted Web App",
        "cli": "CLI Tool",
        "resource": "Open Reference",
    }
    return mapping.get(app_type, "Desktop App")


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
            clean_val = _dedup_words(str(val))
            lines.append(f'{k}: "{_escape_yaml(clean_val)}"')

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


def _specific_pick_guidance(app: dict, peer: dict) -> str:
    """Produce specific decision criteria based on format, platform, and purpose rather than boilerplate."""
    fmt = _format_app_type(app["app_type"])
    os_str = app["operatingSystem"]
    peer_fmt = _format_app_type(peer["app_type"])
    if app["app_type"] == "cli" and peer["app_type"] == "desktop":
        mode_note = "runs as fast terminal commands suited for automation and batch scripts (no graphical buttons)"
    elif app["app_type"] == "desktop" and peer["app_type"] == "cli":
        mode_note = "provides a visual desktop window with point-and-click controls instead of terminal commands"
    elif app["app_type"] == "selfhosted":
        mode_note = "runs on your own private server or local computer so files stay under your control"
    elif app["app_type"] == "desktop":
        mode_note = f"installs directly as a desktop application ({os_str})"
    else:
        mode_note = f"works in **{fmt}** mode ({os_str})"
    return (
        f"**Choose [{app['title']}](/HubHum/apps/{app['slug']}/) ({fmt})** if you need what it specializes in: "
        f"{app['summary'].rstrip('.')} — it {mode_note} ({app['stars']:,} GitHub stars, vs {peer['title']} which runs as a {peer_fmt})."
    )


def generate_clusters() -> dict[str, object]:
    """Generate Level 1 Pillars, Level 2 Sub-Pillars, Level 3 Cluster Articles, and manifests."""
    today = datetime.now(timezone.utc).date().isoformat()
    apps = _load_all_apps()

    # Clean stale generated guides so removed/reclassified clusters stay accurate
    if CONTENT_GUIDES_DIR.exists():
        for old_md in CONTENT_GUIDES_DIR.rglob("*.md"):
            if "deals" in old_md.relative_to(CONTENT_GUIDES_DIR).parts:
                continue
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
            comp_apps = sub_apps[:8]
            top1 = comp_apps[0]
            top2 = comp_apps[1] if len(comp_apps) > 1 else comp_apps[0]
            table_rows = "\n".join(
                f"| [{a['title']}](/HubHum/apps/{a['slug']}/) | {_format_app_type(a['app_type'])} | {a['operatingSystem']} | ★ {a['stars']:,} | {a['license']} |"
                for a in comp_apps
            )
            pick1 = _specific_pick_guidance(top1, top2)
            pick2 = _specific_pick_guidance(top2, top1) if top2["slug"] != top1["slug"] else ""
            picks_block = "\n".join(line for line in (f"- {pick1}", f"- {pick2}" if pick2 else "") if line)
            comp_body = _dedup_words(
                f"""## Quick Answer: {top1['title']} vs {top2['title']}

Comparing **{top1['title']}** and **{top2['title']}** highlights two distinct approaches in **{sub_topic}**. **{top1['title']}** runs as a **{_format_app_type(top1['app_type'])}** on **{top1['operatingSystem']}** ({top1['stars']:,} GitHub stars): {top1['summary']} By contrast, **{top2['title']}** runs as a **{_format_app_type(top2['app_type'])}** on **{top2['operatingSystem']}** ({top2['stars']:,} GitHub stars): {top2['summary']}

### Side-by-Side Comparison ({len(comp_apps)} Tools Reviewed)

| Software | Format | Systems Supported | GitHub Stars | License |
| --- | --- | --- | --- | --- |
{table_rows}

### When to Pick Which Option
{picks_block}
- Review the individual app cards below to verify exact installer options, operating system requirements, and transparent GitHub source links before downloading."""
            )

            clean_sub_noun = re.sub(r"^Free\s+", "", sub_topic, flags=re.IGNORECASE)
            _write_guide_file(
                f"{sub_full_slug}/best-{sub_slug_short}.md",
                {
                    "title": f"Best Free {clean_sub_noun}: {top1['title']} vs {top2['title']} Compared",
                    "slug": comp_slug,
                    "level": 3,
                    "macro_category": category,
                    "macro_slug": macro_slug,
                    "sub_topic": sub_topic,
                    "sub_slug": sub_slug_short,
                    "intent": "comparison",
                    "summary": f"Compare {top1['title']} vs {top2['title']} and {len(comp_apps)} free tools for {clean_sub_noun} with honest format, OS, and license details.",
                    "parent_slug": sub_full_slug,
                    "sibling_slugs": [found_slug, trouble_slug],
                    "app_slugs": [a["slug"] for a in comp_apps],
                    "updated_at": today,
                },
                comp_body,
            )
            generated_files += 1

            # 3B. Level 3 Cluster Article: Foundations (What is / How to choose)
            found_picks = sub_apps[:6]
            found_bullets = "\n".join(
                f"- **[{a['title']}](/HubHum/apps/{a['slug']}/)** ({_format_app_type(a['app_type'])}) — {a['summary']}"
                for a in found_picks
            )
            found_body = _dedup_words(
                f"""## How to Choose Free {clean_sub_noun} Without Getting Lost

Switching to free open-source tools in **{clean_sub_noun}** lets you avoid recurring monthly fees and keep ownership of your files. Before downloading anything, focus on three practical checks:

1. **Pick the right format for your comfort level:** **Desktop Apps** install with visual windows and menus; **Self-Hosted Web Apps** run on hardware or a server you control; **CLI Tools** operate via text commands inside a terminal window.
2. **Verify the official creator source:** Every HubHum card links directly to official GitHub releases or creator sites to help you avoid bundled adware—always check your operating system and run local security scans as standard practice.
3. **Check community activity and license:** GitHub star counts and human-readable licenses shown on every table help confirm an active project.

### Great Starting Points in {clean_sub_noun}

{found_bullets}"""
            )

            _write_guide_file(
                f"{sub_full_slug}/how-to-choose-{sub_slug_short}.md",
                {
                    "title": f"How to Choose and Use Free {clean_sub_noun} Safely",
                    "slug": found_slug,
                    "level": 3,
                    "macro_category": category,
                    "macro_slug": macro_slug,
                    "sub_topic": sub_topic,
                    "sub_slug": sub_slug_short,
                    "intent": "foundations",
                    "summary": f"Beginner-friendly guide explaining what {clean_sub_noun} tools do, desktop vs self-hosted vs terminal formats, and how to download safely.",
                    "parent_slug": sub_full_slug,
                    "sibling_slugs": [comp_slug, trouble_slug],
                    "app_slugs": [a["slug"] for a in found_picks],
                    "updated_at": today,
                },
                found_body,
            )
            generated_files += 1

            # 3C. Level 3 Cluster Article: Problems & Solutions (Troubleshooting)
            trouble_picks = sub_apps[:5]
            trouble_body = _dedup_words(
                f"""## Fixing Common Problems with Free {clean_sub_noun}

Moving away from expensive commercial software occasionally brings small setup questions. Here are the most common hurdles everyday users face with **{clean_sub_noun}** and how to avoid them:

### 1. Opening a Command-Line Tool Expecting Visual Buttons
Some top tools (marked **CLI Tool**) do not open a traditional window—double-clicking their executable flashes a terminal and closes. Check the format badge before downloading: choose a **Desktop App** if you prefer visual buttons, or open a terminal prompt when running CLI tools.

### 2. Choosing Between Self-Hosted Server Tools and Instant Web Apps
Tools marked **Self-Hosted Web App** require Docker or local server setup on your machine or a private host rather than working like a public SaaS website.

### 3. Picking the Right Installer for Your Device
Windows users usually look for `.exe` or `.msi` installers, macOS users look for `.dmg`, and Linux/Android users have their own dedicated packages when listed in Quick Specs.

### Recommended Alternatives Covered

"""
            ) + "\n".join(f"- **[{a['title']}](/HubHum/apps/{a['slug']}/)** ({_format_app_type(a['app_type'])}) — {a['summary']}" for a in trouble_picks)

            _write_guide_file(
                f"{sub_full_slug}/troubleshooting-{sub_slug_short}.md",
                {
                    "title": f"Common {clean_sub_noun} Problems & How to Fix Them",
                    "slug": trouble_slug,
                    "level": 3,
                    "macro_category": category,
                    "macro_slug": macro_slug,
                    "sub_topic": sub_topic,
                    "sub_slug": sub_slug_short,
                    "intent": "troubleshooting",
                    "summary": f"Practical troubleshooting tips for terminal tools vs GUI installers, self-hosted setup, and system compatibility in {clean_sub_noun}.",
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
    manifest["bundles"] = generate_bundle_sets(apps, today)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    APP_CLUSTER_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
    APP_CLUSTER_MAP_PATH.write_text(json.dumps(app_cluster_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return manifest


def _pick_bundle_apps(apps: list[dict], preferred_slugs: tuple[str, ...], category: str | None = None, app_type: str | None = None, limit: int = 6) -> list[dict]:
    """Select existing high-signal apps for curated bundle sets without fabricating missing slugs."""
    by_slug = {a["slug"]: a for a in apps}
    picked: list[dict] = []
    seen: set[str] = set()
    for s in preferred_slugs:
        if s in by_slug and s not in seen:
            picked.append(by_slug[s])
            seen.add(s)
    for a in apps:
        if len(picked) >= limit:
            break
        if a["slug"] in seen:
            continue
        if category and a["category"] != category:
            continue
        if app_type and a["app_type"] != app_type:
            continue
        if a["app_type"] == "resource":
            continue
        picked.append(a)
        seen.add(a["slug"])
    return picked[:limit]


def generate_bundle_sets(apps: list[dict], today: str) -> list[str]:
    """Generate and refresh curated bundle Markdown sets in content/bundles/."""
    CONTENT_BUNDLES_DIR.mkdir(parents=True, exist_ok=True)
    bundle_specs = [
        {
            "slug": "top-free-apps-this-week",
            "title": "Top Free Open-Source Picks of the Week",
            "category": "Curated Guides",
            "summary": "Essential free tools to organize private notes, edit video and audio without limits, protect passwords, and publish online.",
            "tags": ["collection", "productivity", "privacy", "video"],
            "preferred": ("joplin", "ghost", "losslesscut", "keepassxc", "audacity"),
            "filter_cat": None,
            "filter_type": "desktop",
            "why": "Every week we highlight trustworthy free software that replaces costly monthly subscriptions with simple, reliable alternatives you control.",
        },
        {
            "slug": "privacy-security-starter-pack",
            "title": "Complete Free Privacy & Security Starter Pack",
            "category": "Security & Privacy",
            "summary": "Lock down passwords, monitor network traffic, clean system trackers, and browse safely with zero subscription fees.",
            "tags": ["privacy", "security", "password-manager", "vpn"],
            "preferred": ("keepassxc", "sniffnet", "bleachbit", "localsend", "gitleaks"),
            "filter_cat": "Security & Privacy",
            "filter_type": None,
            "why": "Replace scattered security utilities and paid trackers with verified open-source tools you can audit and run directly.",
        },
        {
            "slug": "self-hosted-personal-cloud-bundle",
            "title": "Self-Hosted Personal Cloud & Publishing Bundle",
            "category": "Web Apps & Cloud",
            "summary": "Run private photo backups, dashboards, CMS blogs, and bookmark hubs on your own server or mini-PC.",
            "tags": ["self-hosted", "cloud", "photos", "cms"],
            "preferred": ("immich", "casaos", "coolify", "ghost", "linkwarden", "memos"),
            "filter_cat": "Web Apps & Cloud",
            "filter_type": "selfhosted",
            "why": "Keep full ownership of family memories, notes, websites, and server panels while running cleanly with 1-click cloud hosting or local Docker.",
        },
        {
            "slug": "creator-video-audio-studio-bundle",
            "title": "Free Creator Video & Audio Studio Bundle",
            "category": "Video & Audio",
            "summary": "Cut footage without re-encoding, convert formats fast, record audio cleanly, and manage offline music libraries.",
            "tags": ["video", "audio", "creator", "media"],
            "preferred": ("vlc", "handbrake", "losslesscut", "audacity", "yt-dlp", "navidrome"),
            "filter_cat": "Video & Audio",
            "filter_type": None,
            "why": "Build a complete multimedia workstation with zero watermarks, zero subscription lock-in, and official creator installers.",
        },
        {
            "slug": "paperless-office-notes-bundle",
            "title": "Paperless Office, PDF & Knowledge Vault Bundle",
            "category": "Productivity",
            "summary": "Manage PDFs, encrypted notes, e-books, and personal wikis cleanly without proprietary cloud formats.",
            "tags": ["notes", "pdf", "office", "knowledge"],
            "preferred": ("joplin", "stirling-pdf", "siyuan", "trilium", "sumatra-pdf"),
            "filter_cat": "Productivity",
            "filter_type": None,
            "why": "Keep your everyday documents, receipts, study notes, and reference libraries fast, searchable, and portable.",
        },
        {
            "slug": "desktop-productivity-power-pack",
            "title": "Everyday Desktop Workflow & Utility Power Pack",
            "category": "Productivity",
            "summary": "Switch windows effortlessly, organize backups, share files across devices, and trim daily desktop friction.",
            "tags": ["desktop", "workflow", "windows", "macos"],
            "preferred": ("alt-tab-macos", "localsend", "flameshot", "unigetui", "dbeaver", "bruno"),
            "filter_cat": "Productivity",
            "filter_type": "desktop",
            "why": "Small, lightweight desktop helpers save hours every week without cluttering your system or prompting for upgrades.",
        },
        {
            "slug": "ai-local-privacy-pack",
            "title": "Local AI & Private LLM Workspace Pack",
            "category": "Productivity",
            "summary": "Run AI chat workspaces, writing companions, voice transcription, and personal assistants locally without sending private notes to external clouds.",
            "tags": ["ai", "privacy", "local-llm", "productivity"],
            "preferred": ("jan", "chat-ollama", "aider", "openwhispr", "incarnamind", "atomic-chat"),
            "filter_cat": "Productivity",
            "filter_type": None,
            "why": "Local AI desktops and self-hosted chat workspaces let everyday users harness modern language models while keeping files and prompts strictly private.",
        },
        {
            "slug": "home-server-media-hub",
            "title": "Home Server Media, Books & Streaming Hub",
            "category": "Web Apps & Cloud",
            "summary": "Build an ad-free family media hub for audiobooks, comics, e-books, personal photos, and private music libraries on your own server.",
            "tags": ["self-hosted", "media-server", "streaming", "ebooks"],
            "preferred": ("audiobookshelf", "kavita", "navidrome", "calibre-web-automated", "suwayomi-server", "immich"),
            "filter_cat": "Web Apps & Cloud",
            "filter_type": "selfhosted",
            "why": "Turn an inexpensive mini-PC or cloud VPS into a clean household streaming center without recurring platform fees or tracking.",
        },
        {
            "slug": "creator-audio-video-suite",
            "title": "Prosumer Audio, Video & Subtitle Production Suite",
            "category": "Video & Audio",
            "summary": "Combine non-linear video editing, fast lossless cutting, format transcoding, clean audio mastering, and automated subtitling.",
            "tags": ["video-editor", "audio", "subtitles", "transcoding"],
            "preferred": ("shotcut", "olive", "losslesscut", "handbrake", "audacity", "whispersubtranslate"),
            "filter_cat": "Video & Audio",
            "filter_type": None,
            "why": "Equip creators and podcasters with an integrated, zero-watermark production stack using official desktop releases.",
        },
    ]

    created_slugs: list[str] = []
    for spec in bundle_specs:
        picked = _pick_bundle_apps(
            apps,
            spec["preferred"],  # type: ignore[arg-type]
            category=spec["filter_cat"],  # type: ignore[arg-type]
            app_type=spec["filter_type"],  # type: ignore[arg-type]
            limit=6,
        )
        if len(picked) < 3:
            continue
        tags_yaml = ", ".join(f'"{t}"' for t in spec["tags"])
        slugs_yaml = ", ".join(f'"{a["slug"]}"' for a in picked)
        bullets = "\n".join(
            f"* **[{a['title']}](/HubHum/apps/{a['slug']}/)** (*{_format_app_type(a['app_type'])}*): {a['summary']}"
            for a in picked
        )
        content = "\n".join(
            [
                "---",
                f'title: "{_escape_yaml(str(spec["title"]))}"',
                f'slug: "{spec["slug"]}"',
                f'category: "{spec["category"]}"',
                f'summary: "{_escape_yaml(str(spec["summary"]))}"',
                f"tags: [{tags_yaml}]",
                f"app_slugs: [{slugs_yaml}]",
                f'updated_at: "{today}"',
                "---",
                "",
                "### Why this curated guide",
                str(spec["why"]),
                "",
                "### Featured highlights",
                bullets,
                "",
            ]
        )
        out_path = CONTENT_BUNDLES_DIR / f"{spec['slug']}.md"
        out_path.write_text(content, encoding="utf-8")
        created_slugs.append(str(spec["slug"]))

    return created_slugs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HubHum 5-Level Topic Cluster Orchestrator")
    parser.add_argument("--generate", action="store_true", help="Generate Level 1-3 guides and update cluster manifest")
    parser.add_argument("--generate-all", action="store_true", help="Generate all Topic Clusters (Levels 1-3) and Curated Bundle Sets")
    args = parser.parse_args()
    res = generate_clusters()
    print(f"[CLUSTERS] Generated {res['total_guide_pages']} guide pages across {len(res['pillars'])} macro-pillars and {len(res.get('bundles', []))} bundle sets.")
    print(json.dumps(res, indent=2))
