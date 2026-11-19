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
    "golang",
    "go",
    "python",
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
}

TOPIC_CATEGORY_MAP = {
    "Video & Audio": {"video-editor", "video", "audio", "ffmpeg", "recording", "sound", "media-player", "podcast", "music"},
    "Productivity": {"notes", "markdown", "todo", "office", "document", "calendar", "productivity", "writing", "pdf", "cli", "terminal", "utility"},
    "Security & Privacy": {"vpn", "password-manager", "passwords", "encryption", "privacy", "security", "firewall", "adblock"},
    "Graphics & Design": {"design", "vector", "image", "photo", "svg", "drawing", "mockup", "graphics"},
    "Web Apps & Cloud": {"cms", "self-hosted", "dashboard", "docker", "web-app", "webapp", "saas", "cloud", "blog", "newsletter", "ai", "automation"},
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
    """Return known lowercase slugs and full_names from content/apps/ and catalog-index.json."""
    known_slugs: set[str] = set()
    known_repos: set[str] = set()

    if CONTENT_APPS_DIR.exists():
        known_slugs.update(p.stem.lower() for p in CONTENT_APPS_DIR.glob("*.md"))

    for idx_path in CATALOG_INDEX_PATHS:
        if not idx_path.exists():
            continue
        try:
            items = json.loads(idx_path.read_text(encoding="utf-8"))
            if isinstance(items, list):
                for item in items:
                    slug = str(item.get("slug") or "").lower().strip()
                    full_name = str(item.get("full_name") or "").lower().strip()
                    if slug:
                        known_slugs.add(slug)
                    if full_name:
                        known_repos.add(full_name)
        except Exception:
            continue

    return known_slugs, known_repos


def normalize_human_topics(topics: list[str], description: str = "") -> tuple[list[str], str]:
    """Filter out developer-only stack tags and infer a human macro-category."""
    cleaned = [t.lower() for t in topics if t and t.lower() not in TECH_JARGON_TAGS]
    combined_tokens = set(cleaned) | set(re.findall(r"[a-z0-9-]+", description.lower()))

    macro_category = "Productivity"
    for label, keywords in TOPIC_CATEGORY_MAP.items():
        if combined_tokens & keywords:
            macro_category = label
            break

    if not cleaned:
        cleaned = [macro_category.lower().replace(" & ", "-").replace(" ", "-")]
    return cleaned[:4], macro_category


def truncate_readme(text: str, max_lines: int = MAX_README_LINES) -> tuple[str, bool]:
    """Truncate long READMEs cleanly to the first 500 lines."""
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text, False
    return "\n".join(lines[:max_lines]) + "\n\n[... contenuto abbreviato per limite di lunghezza ...]", True


def classify_repo(description: str, topics: list[str], readme: str, release_assets: list[dict[str, str]]) -> tuple[bool, str, str]:
    """Infer is_webapp, human category, and affiliate category key."""
    combined = f"{description} {' '.join(topics)} {readme[:1500]}".lower()

    has_desktop_installer = any(
        asset["url"].lower().endswith(INSTALLER_EXTENSIONS) for asset in release_assets
    )
    is_webapp = any(
        k in combined for k in ("cms", "self-hosted", "web app", "webapp", "saas", "dashboard", "blogging", "publishing", "docker")
    ) and not has_desktop_installer

    if any(k in combined for k in ("password", "vpn", "privacy", "security", "encryption", "torrent", "adblock")):
        return is_webapp, "Security & Privacy", "privacy_security"
    if any(k in combined for k in ("video", "audio", "ffmpeg", "subtitle", "video editing", "screen recorder")):
        return is_webapp, "Video & Audio", "graphics_video_design"
    if is_webapp:
        return True, "Web Apps & Cloud", "webapp_cms"
    if any(k in combined for k in ("wordpress", "seo", "landing page", "website builder")):
        return is_webapp, "Websites & SEO", "webdev_wordpress"
    if any(k in combined for k in ("design", "vector", "image", "photo", "svg", "drawing", "mockup")):
        return is_webapp, "Graphics & Design", "graphics_video_design"
    return False, "Productivity", "webdev_wordpress"


def derive_operating_system(is_webapp: bool, release_assets: list[dict[str, str]], topics: list[str]) -> str:
    """Compute crisp Schema.org operatingSystem string from release assets and topics."""
    if is_webapp:
        return "All / Browser"
    oses: list[str] = []
    asset_names = " ".join(a.get("name", "").lower() for a in release_assets)
    topic_str = " ".join(t.lower() for t in topics)
    if any(ext in asset_names for ext in (".exe", ".msi")) or "windows" in topic_str:
        oses.append("Windows")
    if any(ext in asset_names for ext in (".dmg", ".pkg")) or "macos" in topic_str:
        oses.append("macOS")
    if any(ext in asset_names for ext in (".appimage", ".deb")) or "linux" in topic_str:
        oses.append("Linux")
    if ".apk" in asset_names or "android" in topic_str:
        oses.append("Android")
    if "ios" in topic_str:
        oses.append("iOS")
    if not oses:
        return "Windows, macOS, Linux, Android"
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

    topics = meta.get("topics") or []
    desc = meta.get("description") or ""
    stars_count = int(meta.get("stargazers_count") or 0)
    human_topics, _ = normalize_human_topics(topics, desc)
    is_webapp, category, _ = classify_repo(desc, human_topics, readme_excerpt, release_assets)

    if scouting_tier is None:
        if is_webapp:
            scouting_tier = "tier2_webapp"
        elif release_assets or any(t in ("gui", "desktop-app", "windows", "macos", "android", "ios") for t in topics):
            scouting_tier = "tier1_gui"
        elif stars_count > 2000:
            scouting_tier = "tier3_powertool"
        else:
            scouting_tier = "tier1_gui"

    if scouting_tier == "tier2_webapp":
        is_webapp = True

    operating_system = derive_operating_system(is_webapp, release_assets, topics)

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
    primary_label = release_assets[0]["label"] if release_assets else "Visit Official Site"

    slug = re.sub(r"[^a-z0-9-]+", "-", repo_name.lower()).strip("-")
    lic = (meta.get("license") or {}).get("spdx_id") or "Open Source"
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

                if require_installer and not bundle.release_assets and tier_key == "tier1_gui":
                    # Still allow GUI repos with explicit consumer mobile/desktop topics even without GitHub releases assets
                    raw_topics = {t.lower() for t in (item.get("topics") or [])}
                    if not (raw_topics & {"gui", "desktop-app", "windows", "macos", "android", "ios"}):
                        continue

                if tier_key == "tier2_webapp":
                    bundle.is_webapp = True
                    bundle.category = "Web Apps & Cloud"
                    bundle.operating_system = "All / Browser"

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
