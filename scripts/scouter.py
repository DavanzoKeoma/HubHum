"""GitHub REST API 3-Tier Quota Scouter for HubHum (1,000 pages/day target within 1,500 RPD ceiling)."""

from __future__ import annotations

import base64
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

from vault_loader import get_secret

GITHUB_API_BASE = "https://api.github.com"
USER_AGENT = "HubHum-Bot/1.0 (DavanzoKeoma; keomadavanzo@gmail.com)"
MAX_README_LINES = 500
MIN_STARS = 200

# 1,500 RPD Gemini Flash Lite Quota Allocation
GEMINI_RPD_CEILING = 1500
DAILY_TARGET_QUOTA = 1000
TIER_1_LIMIT = 500  # 50%: Desktop & Mobile GUI apps (stars > 500)
TIER_2_LIMIT = 300  # 30%: Web Apps, CMS & Self-Hosted SaaS (is_webapp: true)
TIER_3_LIMIT = 200  # 20%: Power Tools, CLI & Utilities (stars > 2,000)
TRENDING_RESERVE = 100  # Headroom part 1: rapid-growth trending repos (last 30d/24h)
ONDEMAND_HEADROOM = 400  # Headroom part 2: Chrome extension + Web on-demand conversions

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_APPS_DIR = PROJECT_ROOT / "content" / "apps"
PROCESSED_REPOS_PATH = PROJECT_ROOT / "data" / "processed_repos.json"
CATALOG_INDEX_PATHS = (
    PROJECT_ROOT / "data" / "catalog-index.json",
    PROJECT_ROOT / "public" / "catalog-index.json",
)

# Strictly stay under GitHub Search API 30 req/min limit (~2.1s between search calls)
_LAST_SEARCH_TS = 0.0
SEARCH_MIN_INTERVAL_SEC = 2.1

TIER_1_GUI_TOPICS = (
    "gui",
    "desktop-app",
    "windows",
    "macos",
    "linux",
    "android",
    "ios",
    "video-editor",
    "password-manager",
)

TIER_2_WEBAPP_TOPICS = (
    "self-hosted",
    "docker",
    "cms",
    "web-app",
    "saas",
    "dashboard",
    "webapp",
)

TIER_3_POWERTOOL_TOPICS = (
    "cli",
    "terminal",
    "command-line",
    "utility",
    "automation",
    "productivity",
)

DEV_LIBRARY_KEYWORDS = (
    "sdk",
    "boilerplate",
    "library for",
    "npm package",
    "rust crate",
    "python package",
    "compiler",
    "framework for developers",
    "curated list",
    "awesome list",
    "cheatsheet",
    "interview questions",
    "immediate mode gui",
    "gui library",
    "ui library",
    "widget toolkit",
    "gui framework",
    "ui framework",
    "cross-platform gui",
    "rust gui",
    "golang gui",
    "python gui",
    "c++ gui",
    "tui library",
    "terminal ui framework",
    "component library",
    "wrapper for",
)

TECH_JARGON_TAGS = {
    "react",
    "reactjs",
    "typescript",
    "javascript",
    "electron",
    "c-plus-plus",
    "cpp",
    "c",
    "csharp",
    "rust",
    "rust-lang",
    "golang",
    "go",
    "python",
    "python3",
    "java",
    "kotlin",
    "swift",
    "vue",
    "vuejs",
    "svelte",
    "nodejs",
    "node",
    "webpack",
    "vite",
    "html",
    "css",
    "scss",
    "tailwind",
    "docker-compose",
    "api",
    "sdk",
    "library",
    "framework",
    "boilerplate",
    "qt",
    "gtk",
    "wxwidgets",
    "reverse-engineering",
    "ai-agents",
    "gplv2",
    "gplv3",
    "mit",
    "apache-2",
    "cli",
    "terminal",
    "shell",
    "bash",
    "zsh",
    "dotfiles",
    "neovim",
    "vim",
    "command-line",
    "binary",
    "tokens",
    "llm",
    "mcp",
    "osint",
    "ctf",
    "web-scraping",
    "crawler",
    "playwright",
    "puppeteer",
}

TAG_HUMAN_REMAP = {
    "reverse-engineering": "security",
    "ai-agents": "automation",
    "cli": "system-utility",
    "terminal": "system-utility",
    "command-line": "system-utility",
    "shell": "automation",
    "bash": "automation",
    "zsh": "productivity",
    "dotfiles": "productivity",
    "neovim": "writing",
    "vim": "writing",
    "docker": "self-hosted",
    "self-hosted": "self-hosted",
    "osint": "privacy",
    "web-scraping": "automation",
    "llm": "ai-assistant",
    "mcp": "automation",
}

KNOWN_REFERENCE_SLUGS = {
    "awesome",
    "ui-ux-pro-max-skill",
    "self-hosting-guide",
    "linux-command",
    "cheat-sh",
    "claude-code-templates",
    "obsidian-skills",
    "pythonguis-examples",
    "qtexamples",
    "you-dont-need-gui",
    "awesome-mac",
}

KNOWN_CLI_OR_TOOLKIT_SLUGS = {
    "lazygit", "zoxide", "tqdm", "ohmyzsh", "bat", "fd", "fzf", "ripgrep",
    "yazi", "btop", "fastfetch", "starship", "atuin", "zellij", "tmux",
    "neovim", "helix", "jq", "yq", "just", "mise", "uv", "ruff", "aria2",
    "yt-dlp", "ffmpeg", "eza", "delta", "gitui", "gemini-cli", "angular-cli",
    "cz-cli", "officecli", "inquirer-js", "cli", "n-m3u8dl-cli",
    # UI toolkits/frameworks & CLI/Dev utilities
    "imgui", "egui", "yew", "avalonia", "wxwidgets", "slint", "fyne",
    "dearpygui", "customtkinter", "nuklear", "gocui", "guilite", "arwes",
    "tweakpane", "winit", "toga", "pywebview", "nicegui", "gdbgui",
    "agent-desktop", "agent-reach", "aider", "airflow", "android-tools",
    "appium", "archon", "ast-grep", "awx", "azul", "basscss", "broot",
    "bullet", "carbonyl", "claude-hud",
    "cobra", "common-utility", "compose-multiplatform", "continue",
    "create-t3-app", "ctop", "distrobox", "dive", "dufs", "exa",
    "fastlane", "fselect", "fx", "fyrox", "gh-stack", "glow", "go-app",
    "goaccess", "gping", "gtop", "gitsome", "herdr", "http-server",
    "hyperfine", "implot", "instapy", "jj", "kestra", "kilocode", "leva",
    "licia", "lxrunoffline", "metrics", "micro", "miller",
    "ms", "ntrace-core", "nx", "oh-my-claudecode", "oh-my-pi", "oha",
    "onefetch", "plandex", "playwright", "pm2", "powershell", "prefect",
    "puppeteer", "pysimplegui", "pywinauto", "q", "qrcp", "qwen-code",
    "rd-agent", "react-nodegui", "reflex", "rtk", "sampler", "saws",
    "scrapling", "semantic-release", "skill-seekers", "sloth",
    "spaceship-prompt", "spotify-tui", "taipy", "tauri", "terminal",
    "terminalizer", "termscp", "trigger-dev", "ts-prune", "ts-toolbelt",
    "typer", "ufo", "uhubctl", "underscore-string", "usql", "util",
    "vagrant", "vhs", "walk", "winget-cli", "witr", "wtf", "wttr-in",
    "xterm-js", "zx",
    # Technical developer / security / OSINT / UI-toolkit tools better classified as CLI/Power tools than everyday desktop GUIs
    "rea", "sherlock", "maigret", "cutter", "gitleaks",
    "orbtk", "awtk", "imgui-rs", "rinf", "remi", "ttkbootstrap", "jclasslib", "python-uiautomation-for-windows", "iced",
}

LICENSE_HUMAN_MAP: dict[str, str] = {
    "NOASSERTION": "Custom Open License",
    "": "Custom Open License",
    "NONE": "Custom Open License",
    "CUSTOM": "Custom Open License",
    "OPEN SOURCE": "Open Source License",
    "MIT": "Open Source (MIT)",
    "APACHE-2.0": "Open Source (Apache 2.0)",
    "GPL-3.0": "Open Source (GPL v3)",
    "GPL-3.0-ONLY": "Open Source (GPL v3)",
    "GPL-3.0-OR-LATER": "Open Source (GPL v3)",
    "GPL-2.0": "Open Source (GPL v2)",
    "GPL-2.0-ONLY": "Open Source (GPL v2)",
    "GPL-2.0-OR-LATER": "Open Source (GPL v2)",
    "AGPL-3.0": "Open Source (AGPL v3)",
    "AGPL-3.0-ONLY": "Open Source (AGPL v3)",
    "AGPL-3.0-OR-LATER": "Open Source (AGPL v3)",
    "MPL-2.0": "Open Source (MPL 2.0)",
    "BSD-3-CLAUSE": "Open Source (BSD)",
    "BSD-2-CLAUSE": "Open Source (BSD)",
    "LGPL-2.1": "Open Source (LGPL)",
    "LGPL-3.0": "Open Source (LGPL)",
    "LGPL-2.1-ONLY": "Open Source (LGPL)",
    "LGPL-3.0-ONLY": "Open Source (LGPL)",
    "UNLICENSE": "Public Domain / Free",
    "CC0-1.0": "Public Domain / Free",
    "WTFPL": "Public Domain / Free",
    "ISC": "Open Source (ISC)",
    "ZLIB": "Open Source (zlib)",
    "EPL-2.0": "Open Source (EPL 2.0)",
    "CC-BY-4.0": "Creative Commons (CC BY 4.0)",
    "CC-BY-SA-4.0": "Creative Commons (CC BY-SA 4.0)",
}


def humanize_license(raw_lic: str | None) -> str:
    """Translate raw GitHub/SPDX license identifiers into plain human labels."""
    clean = str(raw_lic or "").strip()
    if clean in LICENSE_HUMAN_MAP.values():
        return clean
    upper = clean.upper()
    if upper in LICENSE_HUMAN_MAP:
        return LICENSE_HUMAN_MAP[upper]
    return f"Open Source ({clean})" if clean else "Custom Open License"

DESKTOP_TERMINAL_SLUGS = {
    "alacritty", "conemu", "cool-retro-term", "kitty", "tabby",
    "waveterm", "wezterm", "windterm", "cmux",
}

TOPIC_CATEGORY_MAP = {
    "Video & Audio": {"video-editor", "video", "audio", "ffmpeg", "recording", "sound", "media-player", "podcast", "music", "streaming"},
    "Productivity": {"notes", "markdown", "todo", "office", "document", "calendar", "productivity", "writing", "pdf"},
    "Security & Privacy": {"vpn", "password-manager", "passwords", "encryption", "privacy", "security", "firewall", "adblock"},
    "Graphics & Design": {"design", "vector", "image-editor", "photo-editor", "svg-editor", "drawing", "mockup", "graphics", "3d-modeling", "pixel-art"},
    "Web Apps & Cloud": {"cms", "self-hosted", "dashboard", "docker", "web-app", "webapp", "saas", "cloud", "blog", "newsletter"},
    "Utilities & Power Tools": {"cli", "terminal", "command-line", "utility", "automation", "devtools", "developer-tools", "shell", "system-utility"},
}

INSTALLER_EXTENSIONS = (".exe", ".msi", ".dmg", ".pkg", ".apk", ".appimage", ".deb")
SOURCE_ARCHIVE_EXTENSIONS = (".zip", ".tar.gz", ".tgz", ".tar.xz")

PERMISSIVE_OR_OSS_LICENSES = {
    "MIT",
    "Apache-2.0",
    "GPL-2.0",
    "GPL-3.0",
    "LGPL-2.1",
    "LGPL-3.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "MPL-2.0",
    "AGPL-3.0",
    "ISC",
    "Unlicense",
    "CC0-1.0",
    "NOASSERTION",
}


@dataclass
class ScoutedRepo:
    owner: str
    name: str
    slug: str
    full_name: str
    html_url: str
    description: str
    stars: int
    topics: list[str]
    license_id: str
    is_webapp: bool
    category: str
    readme_excerpt: str
    readme_truncated: bool
    icon_path: str = "/icons/hubhum.svg"
    release_assets: list[dict[str, str]] = field(default_factory=list)
    allowed_urls: list[str] = field(default_factory=list)
    primary_download_url: str = ""
    primary_download_label: str = ""
    scouting_tier: str = "tier1_gui"
    app_type: str = "desktop"
    operating_system: str = "Windows, macOS, Linux"


def _github_get_json(url: str, token: str | None = None) -> dict:
    """Perform authenticated or public GitHub REST GET request with rate-limit safety."""
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    for attempt in range(2):
        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 429) and attempt == 0:
                retry_after = int(exc.headers.get("Retry-After") or "5")
                time.sleep(min(max(retry_after, 2), 30))
                continue
            raise
    return {}


def _throttle_github_search() -> None:
    """Enforce >= 2.1s between Search API calls to stay below GitHub's 30 req/min cap."""
    global _LAST_SEARCH_TS
    now = time.monotonic()
    elapsed = now - _LAST_SEARCH_TS
    if _LAST_SEARCH_TS > 0 and elapsed < SEARCH_MIN_INTERVAL_SEC:
        time.sleep(SEARCH_MIN_INTERVAL_SEC - elapsed)
    _LAST_SEARCH_TS = time.monotonic()


def load_existing_catalog_state() -> tuple[set[str], set[str]]:
    """Return known lowercase slugs and canonical owner/repo full_names across files, index, and processed cache."""
    known_slugs: set[str] = set()
    known_repos: set[str] = set()

    if CONTENT_APPS_DIR.exists():
        known_slugs.update(p.stem.lower() for p in CONTENT_APPS_DIR.glob("*.md"))

    if PROCESSED_REPOS_PATH.exists():
        try:
            proc_data = json.loads(PROCESSED_REPOS_PATH.read_text(encoding="utf-8"))
            if isinstance(proc_data, dict):
                for s in proc_data.get("slugs", []):
                    if s:
                        known_slugs.add(str(s).lower().strip())
                for r in proc_data.get("full_names", []):
                    if r:
                        known_repos.add(str(r).lower().strip())
                for u in proc_data.get("repo_urls", []):
                    m = re.match(r"^https?://github\.com/([^/]+/[^/?#]+)", str(u), re.IGNORECASE)
                    if m:
                        known_repos.add(m.group(1).lower().strip())
        except Exception:
            pass

    for idx_path in CATALOG_INDEX_PATHS:
        if not idx_path.exists():
            continue
        try:
            items = json.loads(idx_path.read_text(encoding="utf-8"))
            if isinstance(items, list):
                for item in items:
                    slug = str(item.get("slug") or "").lower().strip()
                    full_name = str(item.get("full_name") or "").lower().strip()
                    repo_url = str(item.get("repo_url") or "").lower().strip()
                    if slug:
                        known_slugs.add(slug)
                    if full_name:
                        known_repos.add(full_name)
                    if repo_url:
                        m = re.match(r"^https?://github\.com/([^/]+/[^/?#]+)", repo_url, re.IGNORECASE)
                        if m:
                            known_repos.add(m.group(1).lower().strip())
        except Exception:
            continue

    return known_slugs, known_repos


def record_processed_repo(slug: str, full_name: str, repo_url: str = "") -> None:
    """Append newly processed canonical repo identifiers to persistent data/processed_repos.json."""
    state: dict[str, list[str]] = {"slugs": [], "full_names": [], "repo_urls": []}
    if PROCESSED_REPOS_PATH.exists():
        try:
            loaded = json.loads(PROCESSED_REPOS_PATH.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                state["slugs"] = list(loaded.get("slugs") or [])
                state["full_names"] = list(loaded.get("full_names") or [])
                state["repo_urls"] = list(loaded.get("repo_urls") or [])
        except Exception:
            pass

    s_norm = str(slug or "").lower().strip()
    f_norm = str(full_name or "").lower().strip()
    u_norm = str(repo_url or "").rstrip("/").lower().strip()
    if s_norm and s_norm not in state["slugs"]:
        state["slugs"].append(s_norm)
    if f_norm and f_norm not in state["full_names"]:
        state["full_names"].append(f_norm)
    if u_norm and u_norm not in state["repo_urls"]:
        state["repo_urls"].append(u_norm)

    PROCESSED_REPOS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED_REPOS_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sanitize_human_tags(topics: list[str], category: str = "Productivity", app_type: str = "desktop") -> list[str]:
    """Strip dev stack tags and remap cryptic topics to friendly human tags."""
    cleaned: list[str] = []
    for raw_t in topics:
        t = re.sub(r"[^a-z0-9-]+", "-", str(raw_t or "").lower()).strip("-")
        if not t:
            continue
        if t in TAG_HUMAN_REMAP:
            t = TAG_HUMAN_REMAP[t]
        elif t in TECH_JARGON_TAGS:
            continue
        if t and t not in cleaned:
            cleaned.append(t)

    if not cleaned:
        fallback_by_cat = {
            "Security & Privacy": ["privacy", "security"],
            "Video & Audio": ["media-tools", "multimedia"],
            "Graphics & Design": ["creative-tools", "design"],
            "Web Apps & Cloud": ["cloud-app", "web-workspace"],
            "Utilities & Power Tools": ["system-utility", "automation"] if app_type == "cli" else ["system-utility", "productivity"],
            "Productivity": ["productivity", "workflow"],
        }
        cleaned = fallback_by_cat.get(category, ["productivity", "open-source"])
    return cleaned[:4]


def normalize_human_topics(topics: list[str], description: str = "") -> tuple[list[str], str]:
    """Filter out developer-only stack tags and infer a human macro-category."""
    desc_low = description.lower()
    topic_set = {str(t or "").lower() for t in topics if t}
    desc_tokens = set(re.findall(r"[a-z0-9-]+", desc_low))
    combined_tokens = topic_set | desc_tokens

    macro_category = "Productivity"
    for label, keywords in TOPIC_CATEGORY_MAP.items():
        if combined_tokens & keywords:
            macro_category = label
            break

    cleaned = sanitize_human_tags(topics, category=macro_category)
    return cleaned, macro_category


def truncate_readme(text: str, max_lines: int = MAX_README_LINES) -> tuple[str, bool]:
    """Truncate long READMEs cleanly to the first 500 lines."""
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text, False
    return "\n".join(lines[:max_lines]) + "\n\n[... contenuto abbreviato per limite di lunghezza ...]", True


def classify_app_type_and_category(
    slug: str,
    title: str,
    description: str,
    topics: list[str],
    readme: str,
    has_desktop_installer: bool,
    current_tier: str = "",
) -> tuple[str, str, str, bool, str]:
    """Deterministically classify (app_type, category, scouting_tier, is_webapp, aff_cat_key).

    Uses strict word-boundary regexes on title, slug, description, and topics (never
    prose filler in READMEs or substring traps like 'obs' inside 'jobs').
    """
    slug_low = slug.lower().strip()
    meta_text = f"{title} {slug_low} {description} {' '.join(topics)}".lower()
    topic_set = {t.lower().strip() for t in topics if t}

    is_security_domain = slug_low not in {"joplin", "photoprism", "reactive-resume", "analytics", "core", "memos", "meetily", "siyuan", "jan", "appsmith", "illa-builder"} and bool(
        re.search(
            r"\b(?:password manager|passwords|vpn|ipsec|wireguard|adblock|firewall|network monitor|"
            r"packet analyzer|secret scanning|system cleaner|debloat|debloating|waf|"
            r"bleachbit|gitleaks|sniffnet|safeline|v2raya|setup-ipsec-vpn|singbox|esp32marauder|airgorah|keepass|bitwarden|vaultwarden|maigret|sherlock|pangolin|pentagi|win11debloat|sophiapp|sophia-script-for-windows)\b",
            meta_text,
        )
        or (topic_set & {"password-manager", "vpn", "adblock", "firewall"})
    )
    is_video_audio_domain = bool(
        re.search(
            r"\b(?:video editor|video player|video downloader|screen recorder|audio editor|audio player|"
            r"music player|media player|media server|music streaming|subtitle|podcast|transcoder|"
            r"ffmpeg|handbrake|obs studio|losslesscut|audacity|vlc|navidrome|spotifast|yt-dlp|bili23-downloader|mpv-net|finetune|youtube-dl-gui)\b",
            meta_text,
        )
        or (topic_set & {"video-editor", "audio-player", "media-player", "screen-recorder", "music", "podcast"})
    )
    is_graphics_domain = bool(
        re.search(
            r"\b(?:image editor|photo editor|photo optimizer|image optimizer|vector graphics|svg editor|"
            r"drawing app|painting app|screenshot tool|screenshot|mockup|3d modeling|3d printing|3d slicer|"
            r"pixel art|design tool|figma|cad software|illustration|flameshot|imageoptim|cura|easydiffusion|photoprism|koharu|stable-dreamfusion|butterfly|tools-ocr)\b",
            meta_text,
        )
        or (topic_set & {"design", "vector", "image-editor", "photo-editor", "drawing", "mockup", "3d-modeling"})
    )

    is_torrent_or_dl_domain = bool(
        re.search(
            r"\b(?:torrent|bittorrent|transgui|ariang|aria2|yt-dlp|youtube-dl|bili23|metube|"
            r"fanqie-novel-downloader|youtubeplaylistdownloader|download-manager)\b",
            meta_text,
        )
        or (topic_set & {"torrent", "bittorrent", "downloader"})
    )
    is_webdev_seo_domain = bool(
        re.search(
            r"\b(?:wordpress|seo|blogging|static site|website builder|headless cms|ghost|hugo|hexo|jekyll|strapi|payload|directus|grav|wagtail)\b",
            meta_text,
        )
        or (topic_set & {"wordpress", "seo", "blog", "cms"})
    )

    # 0. Open Reference / Curated Guides / Skill Packs (never labeled Desktop App)
    if slug_low in KNOWN_REFERENCE_SLUGS or slug_low.startswith("awesome-") or re.search(
        r"\b(?:curated list|awesome list|collections of|cheatsheet|prompt library|ai skill|ui ux)\b",
        meta_text,
    ):
        ref_cat = "Productivity"
        ref_aff = "productivity_utilities"
        if "self-hosting" in slug_low:
            ref_cat, ref_aff = "Web Apps & Cloud", "webapp_cms"
        elif is_graphics_domain:
            ref_cat, ref_aff = "Graphics & Design", "graphics_video_design"
        elif slug_low in {"linux-command", "cheat-sh", "you-dont-need-gui"}:
            ref_cat, ref_aff = "Utilities & Power Tools", "productivity_utilities"
        return "resource", ref_cat, "tier3_powertool", False, ref_aff

    is_known_cli_or_tk = slug_low in KNOWN_CLI_OR_TOOLKIT_SLUGS or slug_low.endswith("-cli")
    has_cli_signal = is_known_cli_or_tk or bool(
        re.search(
            r"\b(?:command[- ]line|terminal utility|shell prompt|directory jumper|progress bar|fuzzy finder|"
            r"zsh framework|gui library|ui library|widget toolkit|immediate mode gui|terminal ui|tui|"
            r"game engine|rendering engine|plotting library|css framework|utility library|binary level|"
            r"reverse engineering|osint|command-line interface)\b",
            meta_text,
        )
    ) or bool(topic_set & {"cli", "terminal", "command-line", "zsh", "shell", "dotfiles", "tui"})

    is_hosted_browser_app = slug_low == "hubhum" or bool(
        re.search(r"\b(?:hosted online|free online service|no installation required|runs on our servers)\b", meta_text)
    )
    has_webapp_signal = current_tier == "tier2_webapp" or slug_low in {
        "analytics", "core", "openblocks", "dify", "maxun", "skyvern", "puter", "ai-website-cloner-template",
    } or (
        not has_desktop_installer
        and not has_cli_signal
        and slug_low not in DESKTOP_TERMINAL_SLUGS
        and bool(
            re.search(
                r"\b(?:self-hosted|web app|webapp|saas|browser-based|cms|control panel|web dashboard|"
                r"cloud workspace|headless cms|wiki platform|webmail|knowledge base server|media server|"
                r"music server|homepage dashboard|analytics platform|low-code|no-code)\b",
                meta_text,
            )
            or (topic_set & {"self-hosted", "cms", "web-app", "webapp", "saas", "dashboard"})
        )
    )

    if slug_low in DESKTOP_TERMINAL_SLUGS:
        return "desktop", "Utilities & Power Tools", "tier1_gui", False, "productivity_utilities"

    if is_known_cli_or_tk or (has_cli_signal and not has_desktop_installer and current_tier != "tier2_webapp"):
        app_type = "cli"
        scouting_tier = "tier3_powertool"
        is_webapp = False
        if is_security_domain or is_torrent_or_dl_domain:
            cat = "Security & Privacy" if is_security_domain else ("Video & Audio" if is_video_audio_domain else "Utilities & Power Tools")
            return app_type, cat, scouting_tier, is_webapp, "privacy_security"
        if is_video_audio_domain:
            return app_type, "Video & Audio", scouting_tier, is_webapp, "graphics_video_design"
        if is_graphics_domain:
            return app_type, "Graphics & Design", scouting_tier, is_webapp, "graphics_video_design"
        if is_webdev_seo_domain:
            return app_type, "Websites & SEO", scouting_tier, is_webapp, "webdev_wordpress"
        return app_type, "Utilities & Power Tools", scouting_tier, is_webapp, "productivity_utilities"

    if has_webapp_signal or (current_tier == "tier2_webapp" and not has_cli_signal):
        app_type = "webapp" if is_hosted_browser_app else "selfhosted"
        scouting_tier = "tier2_webapp"
        is_webapp = True
        if is_webdev_seo_domain:
            return app_type, "Web Apps & Cloud", scouting_tier, is_webapp, "webdev_wordpress"
        if is_security_domain or is_torrent_or_dl_domain:
            return app_type, "Security & Privacy", scouting_tier, is_webapp, "privacy_security"
        if is_video_audio_domain:
            return app_type, "Video & Audio", scouting_tier, is_webapp, "graphics_video_design"
        if is_graphics_domain:
            return app_type, "Graphics & Design", scouting_tier, is_webapp, "graphics_video_design"
        return app_type, "Web Apps & Cloud", scouting_tier, is_webapp, "webapp_cms"

    if has_cli_signal and current_tier == "tier3_powertool" and not has_desktop_installer:
        return "cli", "Utilities & Power Tools", "tier3_powertool", False, "productivity_utilities"

    if is_security_domain:
        cat, aff = "Security & Privacy", "privacy_security"
    elif is_torrent_or_dl_domain:
        cat = "Video & Audio" if is_video_audio_domain else "Productivity"
        aff = "privacy_security"
    elif is_video_audio_domain:
        cat, aff = "Video & Audio", "graphics_video_design"
    elif is_graphics_domain:
        cat, aff = "Graphics & Design", "graphics_video_design"
    elif is_webdev_seo_domain:
        cat, aff = "Websites & SEO", "webdev_wordpress"
    else:
        cat, aff = "Productivity", "productivity_utilities"

    return "desktop", cat, "tier1_gui", False, aff


def classify_repo(description: str, topics: list[str], readme: str, release_assets: list[dict[str, str]]) -> tuple[bool, str, str]:
    """Infer is_webapp, human category, and affiliate category key from metadata signals."""
    has_desktop_installer = any(
        asset["url"].lower().endswith(INSTALLER_EXTENSIONS) for asset in release_assets
    )
    _, cat, _, is_webapp, aff = classify_app_type_and_category(
        slug="",
        title="",
        description=description,
        topics=topics,
        readme=readme,
        has_desktop_installer=has_desktop_installer,
    )
    return is_webapp, cat, aff


def derive_operating_system(
    is_webapp: bool,
    release_assets: list[dict[str, str]],
    topics: list[str],
    app_type: str = "desktop",
) -> str:
    """Compute accurate Schema.org operatingSystem string without falsely claiming Android."""
    if app_type == "webapp":
        return "Browser / Online"
    if app_type == "selfhosted" or is_webapp:
        return "Self-Hosted / Browser"
    if app_type == "resource":
        return "All / Reference"
    oses: list[str] = []
    asset_names = " ".join(a.get("name", "").lower() for a in release_assets)
    topic_str = " ".join(t.lower() for t in topics)
    if any(ext in asset_names for ext in (".exe", ".msi")) or "windows" in topic_str:
        oses.append("Windows")
    if any(ext in asset_names for ext in (".dmg", ".pkg")) or "macos" in topic_str:
        oses.append("macOS")
    if any(ext in asset_names for ext in (".appimage", ".deb")) or "linux" in topic_str:
        oses.append("Linux")
    if (".apk" in asset_names or "android" in topic_str) and app_type != "cli":
        oses.append("Android")
    if "ios" in topic_str and app_type != "cli":
        oses.append("iOS")
    if not oses:
        return "Windows, macOS, Linux"
    return ", ".join(oses)


def is_consumer_repo(repo: dict, min_stars: int = MIN_STARS) -> bool:
    """Enforce NO-FORK, star threshold, license compatibility, and exclude dev-only libraries or list repos."""
    if repo.get("fork") is True or repo.get("archived") is True:
        return False
    if int(repo.get("stargazers_count") or 0) <= min_stars:
        return False
    name_low = (repo.get("name") or "").lower()
    if name_low == "awesome" or name_low.startswith("awesome-"):
        return False
    desc = (repo.get("description") or "").lower()
    topics_raw = " ".join(str(t) for t in (repo.get("topics") or []))
    safety_text = f"{name_low} {desc} {topics_raw}".lower()
    if re.search(
        r"\b(?:keygen|crack|piracy|warez|cheat|aimbot|exploit|payload|ransomware|stealer|nsfw|hentai|adult|bypass-paywall)\b",
        safety_text,
    ):
        return False
    if any(kw in desc for kw in DEV_LIBRARY_KEYWORDS):
        return False
    lic = (repo.get("license") or {}).get("spdx_id") or "NOASSERTION"
    if lic not in PERMISSIVE_OR_OSS_LICENSES and lic != "NOASSERTION":
        return False
    return True


def extract_urls_from_text(text: str) -> list[str]:
    """Extract clean HTTP/HTTPS URLs from README while ignoring badge images."""
    urls = re.findall(r"https?://[^\s\)\]>\"']+", text)
    cleaned = []
    for u in urls:
        u = u.rstrip(".,;:")
        if any(b in u.lower() for b in ("shields.io", "badge", "travis-ci", "codecov.io")):
            continue
        if u not in cleaned:
            cleaned.append(u)
    return cleaned


def label_for_asset(name: str) -> str:
    """Create a human-friendly download label from installer filename."""
    low = name.lower()
    if low.endswith(".exe") or low.endswith(".msi"):
        return f"Download for Windows ({Path(name).suffix})"
    if low.endswith(".dmg") or low.endswith(".pkg"):
        return f"Download for Mac ({Path(name).suffix})"
    if low.endswith(".apk"):
        return "Download for Android (.apk)"
    if low.endswith(".appimage") or low.endswith(".deb"):
        return f"Download for Linux ({Path(name).suffix})"
    return f"Download ({name})"


def download_repo_icon(slug: str, owner_avatar_url: str) -> str:
    """Download owner avatar icon locally into public/icons/<slug>.png to avoid slow hotlinks."""
    icons_dir = PROJECT_ROOT / "public" / "icons"
    icons_dir.mkdir(parents=True, exist_ok=True)
    for ext in (".svg", ".png"):
        if (icons_dir / f"{slug}{ext}").exists():
            return f"/icons/{slug}{ext}"

    if owner_avatar_url:
        sep = "&" if "?" in owner_avatar_url else "?"
        sized_url = f"{owner_avatar_url}{sep}s=128"
        try:
            req = urllib.request.Request(sized_url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status == 200:
                    (icons_dir / f"{slug}.png").write_bytes(resp.read())
                    return f"/icons/{slug}.png"
        except Exception:
            pass
    return "/icons/hubhum.svg"


def fetch_repo_bundle(
    owner: str,
    repo_name: str,
    token: str | None = None,
    scouting_tier: str | None = None,
) -> ScoutedRepo:
    """Fetch metadata, README (<=500 lines), and latest release direct links without forking."""
    if token is None:
        token = get_secret("dev.github", "pat", "GITHUB_TOKEN")

    meta = _github_get_json(f"{GITHUB_API_BASE}/repos/{owner}/{repo_name}", token=token)
    if meta.get("fork") is True:
        raise ValueError(f"Regola NO-FORK violata: {owner}/{repo_name} è un fork.")

    readme_text = ""
    try:
        readme_json = _github_get_json(f"{GITHUB_API_BASE}/repos/{owner}/{repo_name}/readme", token=token)
        content_b64 = readme_json.get("content", "")
        if content_b64:
            readme_text = base64.b64decode(content_b64).decode("utf-8", errors="replace")
    except urllib.error.HTTPError:
        readme_text = meta.get("description") or ""

    readme_excerpt, truncated = truncate_readme(readme_text, MAX_README_LINES)

    release_assets: list[dict[str, str]] = []
    fallback_assets: list[dict[str, str]] = []
    try:
        rel = _github_get_json(f"{GITHUB_API_BASE}/repos/{owner}/{repo_name}/releases/latest", token=token)
        for asset in rel.get("assets", []):
            name = asset.get("name", "")
            dl_url = asset.get("browser_download_url", "")
            if not dl_url or "dont-use" in name.lower():
                continue
            item = {"name": name, "url": dl_url, "label": label_for_asset(name)}
            if name.lower().endswith(INSTALLER_EXTENSIONS):
                release_assets.append(item)
            elif not name.lower().endswith(SOURCE_ARCHIVE_EXTENSIONS):
                fallback_assets.append(item)
    except urllib.error.HTTPError:
        pass

    def _asset_rank(item: dict[str, str]) -> int:
        low = item["name"].lower()
        for idx, ext in enumerate(INSTALLER_EXTENSIONS):
            if low.endswith(ext):
                return idx
        return len(INSTALLER_EXTENSIONS)

    release_assets.sort(key=_asset_rank)
    if not release_assets and fallback_assets:
        release_assets = fallback_assets

    slug = re.sub(r"[^a-z0-9-]+", "-", repo_name.lower()).strip("-")
    topics = meta.get("topics") or []
    desc = meta.get("description") or ""
    stars_count = int(meta.get("stargazers_count") or 0)
    has_desktop_installer = any(
        asset["url"].lower().endswith(INSTALLER_EXTENSIONS) for asset in release_assets
    )

    app_type, category, detected_tier, is_webapp, _ = classify_app_type_and_category(
        slug=slug,
        title=meta.get("name") or repo_name,
        description=desc,
        topics=topics,
        readme=readme_excerpt,
        has_desktop_installer=has_desktop_installer,
        current_tier=scouting_tier or "",
    )
    if scouting_tier is None:
        scouting_tier = detected_tier
    if scouting_tier == "tier2_webapp":
        is_webapp = True
        if app_type not in ("webapp", "selfhosted"):
            app_type = "selfhosted"
    elif scouting_tier == "tier3_powertool" and app_type == "desktop" and not has_desktop_installer:
        app_type = "cli"
        if category == "Graphics & Design":
            category = "Utilities & Power Tools"

    human_topics = sanitize_human_tags(topics, category=category, app_type=app_type)
    operating_system = derive_operating_system(is_webapp, release_assets, topics, app_type=app_type)

    html_url = meta["html_url"]
    homepage = (meta.get("homepage") or "").strip()
    allowed_urls = [html_url]
    if homepage.startswith("http"):
        allowed_urls.append(homepage)
        if homepage.startswith("http://"):
            allowed_urls.append("https://" + homepage[7:])
    allowed_urls.extend(a["url"] for a in release_assets)
    allowed_urls.extend(extract_urls_from_text(readme_excerpt))

    safe_homepage = ("https://" + homepage[7:]) if homepage.startswith("http://") else homepage
    primary_url = release_assets[0]["url"] if release_assets else (safe_homepage if safe_homepage.startswith("http") else f"{html_url}/releases")
    if release_assets:
        primary_label = release_assets[0]["label"]
    elif app_type == "cli":
        primary_label = "Get Command-Line Tool →"
    elif app_type == "resource":
        primary_label = "Browse Reference →"
    elif app_type == "selfhosted":
        primary_label = "Official Setup & Docs →"
    elif is_webapp:
        primary_label = "Open in Cloud →"
    else:
        primary_label = "Visit Official Site"

    raw_lic = (meta.get("license") or {}).get("spdx_id") or ""
    lic = humanize_license(raw_lic)
    avatar_url = ((meta.get("owner") or {}).get("avatar_url") or "").strip()
    icon_path = download_repo_icon(slug, avatar_url)

    return ScoutedRepo(
        owner=owner,
        name=meta["name"],
        slug=slug,
        full_name=meta["full_name"],
        html_url=html_url,
        description=desc,
        stars=stars_count,
        topics=human_topics,
        license_id=lic,
        is_webapp=is_webapp,
        category=category,
        readme_excerpt=readme_excerpt,
        readme_truncated=truncated,
        icon_path=icon_path,
        release_assets=release_assets,
        allowed_urls=list(dict.fromkeys(allowed_urls)),
        primary_download_url=primary_url,
        primary_download_label=primary_label,
        scouting_tier=scouting_tier,
        app_type=app_type,
        operating_system=operating_system,
    )


def fetch_repo_by_url(repo_url: str, token: str | None = None) -> ScoutedRepo:
    """Parse a GitHub URL and fetch its bundle safely."""
    match = re.match(r"^https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git|/.*)?$", repo_url.strip())
    if not match:
        raise ValueError(f"URL GitHub non valido: {repo_url}")
    return fetch_repo_bundle(match.group(1), match.group(2), token=token)


def _search_tier_candidates(
    queries: list[str],
    tier_limit: int,
    tier_key: str,
    min_stars: int,
    token: str | None,
    known_slugs: set[str],
    known_repos: set[str],
    require_installer: bool = False,
) -> list[ScoutedRepo]:
    """Query GitHub Search API politely (<= 30 req/min) for one specific scouting tier."""
    if tier_limit <= 0:
        return []

    collected: list[ScoutedRepo] = []
    for raw_q in queries:
        if len(collected) >= tier_limit:
            break
        for page_num in (1, 2):
            if len(collected) >= tier_limit:
                break
            _throttle_github_search()
            encoded_q = urllib.parse.quote(raw_q)
            url = f"{GITHUB_API_BASE}/search/repositories?q={encoded_q}&sort=stars&order=desc&per_page=30&page={page_num}"
            try:
                data = _github_get_json(url, token=token)
            except Exception:
                break

            items = data.get("items", [])
            if not items:
                break

            for item in items:
                full_name = str(item.get("full_name") or "")
                repo_name = str(item.get("name") or "")
                slug = re.sub(r"[^a-z0-9-]+", "-", repo_name.lower()).strip("-")
                if not full_name or slug in known_slugs or full_name.lower() in known_repos:
                    continue
                if not is_consumer_repo(item, min_stars=min_stars):
                    continue

                known_repos.add(full_name.lower())
                known_slugs.add(slug)
                owner = item["owner"]["login"]
                try:
                    bundle = fetch_repo_bundle(owner, repo_name, token=token, scouting_tier=tier_key)
                except Exception:
                    continue

                if tier_key == "tier1_gui" and bundle.app_type in ("cli", "resource"):
                    continue

                if require_installer and not bundle.release_assets and tier_key == "tier1_gui":
                    # Still allow GUI repos with explicit consumer mobile/desktop topics even without GitHub releases assets
                    raw_topics = {t.lower() for t in (item.get("topics") or [])}
                    if not (raw_topics & {"gui", "desktop-app", "windows", "macos", "android", "ios"}):
                        continue

                if tier_key == "tier2_webapp":
                    bundle.is_webapp = True
                    bundle.app_type = "selfhosted"
                    bundle.category = "Web Apps & Cloud"
                    bundle.operating_system = "Self-Hosted / Browser"
                elif tier_key == "tier3_powertool":
                    if bundle.app_type != "resource":
                        bundle.app_type = "cli"
                    bundle.is_webapp = False

                collected.append(bundle)
                if len(collected) >= tier_limit:
                    break
    return collected


def compute_tier_allocations(total_limit: int, tier_mode: str = "all") -> dict[str, int]:
    """Partition total_limit strictly into 50% Tier 1 / 30% Tier 2 / 20% Tier 3 (or 100% single tier)."""
    if tier_mode == "tier1":
        return {"tier1_gui": min(total_limit, TIER_1_LIMIT), "tier2_webapp": 0, "tier3_powertool": 0, "trending": 0}
    if tier_mode == "tier2":
        return {"tier1_gui": 0, "tier2_webapp": min(total_limit, TIER_2_LIMIT), "tier3_powertool": 0, "trending": 0}
    if tier_mode == "tier3":
        return {"tier1_gui": 0, "tier2_webapp": 0, "tier3_powertool": min(total_limit, TIER_3_LIMIT), "trending": 0}
    if tier_mode == "trending":
        return {"tier1_gui": 0, "tier2_webapp": 0, "tier3_powertool": 0, "trending": min(total_limit, TRENDING_RESERVE)}

    capped = min(max(total_limit, 0), DAILY_TARGET_QUOTA)
    if capped == 0:
        return {"tier1_gui": 0, "tier2_webapp": 0, "tier3_powertool": 0, "trending": 0}

    t1 = round(capped * (TIER_1_LIMIT / DAILY_TARGET_QUOTA))
    t2 = round(capped * (TIER_2_LIMIT / DAILY_TARGET_QUOTA))
    t3 = capped - t1 - t2
    if capped >= 3:
        if t2 == 0:
            t2 = 1
            t1 = max(t1 - 1, 1)
        if t3 == 0:
            t3 = 1
            t1 = max(t1 - 1, 1)
    return {"tier1_gui": t1, "tier2_webapp": t2, "tier3_powertool": t3, "trending": 0}


def scout_tiered_apps(
    limit: int = DAILY_TARGET_QUOTA,
    tier: str = "all",
    token: str | None = None,
) -> list[ScoutedRepo]:
    """Scout apps partitioned across Tier 1 (GUI), Tier 2 (Web/CMS), Tier 3 (Power Tools), and Trending."""
    if token is None:
        token = get_secret("dev.github", "pat", "GITHUB_TOKEN")

    known_slugs, known_repos = load_existing_catalog_state()
    alloc = compute_tier_allocations(limit, tier_mode=tier)

    results: list[ScoutedRepo] = []

    if alloc["tier1_gui"] > 0:
        t1_queries = [f"topic:{t} stars:>500 fork:false archived:false" for t in TIER_1_GUI_TOPICS]
        results.extend(
            _search_tier_candidates(
                t1_queries,
                alloc["tier1_gui"],
                "tier1_gui",
                min_stars=500,
                token=token,
                known_slugs=known_slugs,
                known_repos=known_repos,
                require_installer=True,
            )
        )

    if alloc["tier2_webapp"] > 0:
        t2_queries = [f"topic:{t} stars:>200 fork:false archived:false" for t in TIER_2_WEBAPP_TOPICS]
        results.extend(
            _search_tier_candidates(
                t2_queries,
                alloc["tier2_webapp"],
                "tier2_webapp",
                min_stars=200,
                token=token,
                known_slugs=known_slugs,
                known_repos=known_repos,
            )
        )

    if alloc["tier3_powertool"] > 0:
        t3_queries = [f"topic:{t} stars:>2000 fork:false archived:false" for t in TIER_3_POWERTOOL_TOPICS]
        results.extend(
            _search_tier_candidates(
                t3_queries,
                alloc["tier3_powertool"],
                "tier3_powertool",
                min_stars=2000,
                token=token,
                known_slugs=known_slugs,
                known_repos=known_repos,
            )
        )

    if alloc["trending"] > 0:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=30)).date().isoformat()
        tr_queries = [
            f"created:>{cutoff} stars:>200 fork:false archived:false",
            f"pushed:>{(datetime.now(timezone.utc) - timedelta(days=1)).date().isoformat()} stars:>1000 fork:false archived:false",
        ]
        results.extend(
            _search_tier_candidates(
                tr_queries,
                alloc["trending"],
                "trending",
                min_stars=200,
                token=token,
                known_slugs=known_slugs,
                known_repos=known_repos,
            )
        )

    return results[:limit]


def scout_trending_consumer_apps(limit: int = 15, token: str | None = None) -> list[ScoutedRepo]:
    """Backwards-compatible entrypoint returning proportional 3-Tier candidates."""
    return scout_tiered_apps(limit=limit, tier="all", token=token)


def describe_quota_architecture() -> dict[str, object]:
    """Return current quota allocation table for diagnostics and telemetry."""
    return {
        "gemini_rpd_ceiling": GEMINI_RPD_CEILING,
        "daily_target_quota": DAILY_TARGET_QUOTA,
        "tiers": {
            "tier1_gui": {"limit": TIER_1_LIMIT, "share": "50%", "filter": "GUI Desktop/Mobile (stars > 500)"},
            "tier2_webapp": {"limit": TIER_2_LIMIT, "share": "30%", "filter": "Web Apps, CMS, Self-Hosted (is_webapp: true)"},
            "tier3_powertool": {"limit": TIER_3_LIMIT, "share": "20%", "filter": "CLI, Power Tools & Utilities (stars > 2,000)"},
        },
        "headroom_rpd": {
            "trending_reserve": TRENDING_RESERVE,
            "ondemand_extension_web": ONDEMAND_HEADROOM,
            "total_reserved": TRENDING_RESERVE + ONDEMAND_HEADROOM,
        },
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="HubHum 3-Tier GitHub Scouter (1,000/day Quota)")
    parser.add_argument("--repo", help="Single repository owner/name")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--tier", choices=["all", "tier1", "tier2", "tier3", "trending"], default="all")
    parser.add_argument("--show-quota", action="store_true", help="Print 3-tier quota architecture")
    args = parser.parse_args()

    if args.show_quota:
        print(json.dumps(describe_quota_architecture(), indent=2))
    elif args.repo:
        owner, name = args.repo.split("/", 1)
        bundle = fetch_repo_bundle(owner, name)
        print(
            json.dumps(
                {
                    "name": bundle.name,
                    "slug": bundle.slug,
                    "stars": bundle.stars,
                    "is_webapp": bundle.is_webapp,
                    "category": bundle.category,
                    "scouting_tier": bundle.scouting_tier,
                    "operating_system": bundle.operating_system,
                    "assets": len(bundle.release_assets),
                },
                indent=2,
            )
        )
    else:
        found = scout_tiered_apps(limit=args.limit, tier=args.tier)
        print(
            json.dumps(
                [
                    {
                        "name": r.name,
                        "stars": r.stars,
                        "category": r.category,
                        "scouting_tier": r.scouting_tier,
                    }
                    for r in found
                ],
                indent=2,
            )
        )
