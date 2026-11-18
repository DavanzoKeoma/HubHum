"""GitHub REST API scouter for HubHum (NO-FORK policy, >500 stars, consumer tags, 500-line README cap)."""

from __future__ import annotations

import base64
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from vault_loader import get_secret

GITHUB_API_BASE = "https://api.github.com"
USER_AGENT = "HubHum-Bot/1.0 (DavanzoKeoma; keomadavanzo@gmail.com)"
MAX_README_LINES = 500
MIN_STARS = 500

CONSUMER_TOPICS = (
    "windows",
    "macos",
    "utility",
    "video-editor",
    "productivity",
    "password-manager",
    "self-hosted",
    "cms",
    "design",
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
)

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
    release_assets: list[dict[str, str]] = field(default_factory=list)
    allowed_urls: list[str] = field(default_factory=list)
    primary_download_url: str = ""
    primary_download_label: str = ""


def _github_get_json(url: str, token: str | None = None) -> dict:
    """Perform authenticated or public GitHub REST GET request."""
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def truncate_readme(text: str, max_lines: int = MAX_README_LINES) -> tuple[str, bool]:
    """Truncate long READMEs cleanly to the first 500 lines (Workflow 8)."""
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
        k in combined for k in ("cms", "self-hosted", "web app", "webapp", "dashboard", "blogging", "publishing", "docker")
    ) and not has_desktop_installer

    if any(k in combined for k in ("password", "vpn", "privacy", "security", "encryption", "torrent", "adblock")):
        return is_webapp, "Sicurezza & Privacy", "privacy_security"
    if any(k in combined for k in ("video", "audio", "ffmpeg", "subtitle", "video editing", "screen recorder")):
        return is_webapp, "Video & Audio", "graphics_video_design"
    if is_webapp:
        return True, "Web App & Cloud", "webapp_cms"
    if any(k in combined for k in ("wordpress", "seo", "landing page", "website builder")):
        return is_webapp, "Siti Web & SEO", "webdev_wordpress"
    if any(k in combined for k in ("design", "vector", "image", "photo", "svg", "drawing", "mockup")):
        return is_webapp, "Grafica & Design", "graphics_video_design"
    return False, "Produttività", "webdev_wordpress"


def is_consumer_repo(repo: dict) -> bool:
    """Enforce NO-FORK, >500 stars, license compatibility, and exclude dev-only libraries."""
    if repo.get("fork") is True:
        return False
    if int(repo.get("stargazers_count") or 0) <= MIN_STARS:
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
        return f"Scarica per Windows ({Path(name).suffix})"
    if low.endswith(".dmg") or low.endswith(".pkg"):
        return f"Scarica per Mac ({Path(name).suffix})"
    if low.endswith(".apk"):
        return "Scarica per Android (.apk)"
    if low.endswith(".appimage") or low.endswith(".deb"):
        return f"Scarica per Linux ({Path(name).suffix})"
    return f"Scarica ({name})"


def fetch_repo_bundle(owner: str, repo_name: str, token: str | None = None) -> ScoutedRepo:
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
    is_webapp, category, _ = classify_repo(desc, topics, readme_excerpt, release_assets)

    html_url = meta["html_url"]
    homepage = (meta.get("homepage") or "").strip()
    allowed_urls = [html_url]
    if homepage.startswith("http"):
        allowed_urls.append(homepage)
    allowed_urls.extend(a["url"] for a in release_assets)
    allowed_urls.extend(extract_urls_from_text(readme_excerpt)[:25])

    primary_url = release_assets[0]["url"] if release_assets else (homepage if homepage.startswith("http") else f"{html_url}/releases")
    primary_label = release_assets[0]["label"] if release_assets else "Vai al sito ufficiale"

    slug = re.sub(r"[^a-z0-9-]+", "-", repo_name.lower()).strip("-")
    lic = (meta.get("license") or {}).get("spdx_id") or "Open Source"

    return ScoutedRepo(
        owner=owner,
        name=meta["name"],
        slug=slug,
        full_name=meta["full_name"],
        html_url=html_url,
        description=desc,
        stars=int(meta.get("stargazers_count") or 0),
        topics=topics,
        license_id=lic,
        is_webapp=is_webapp,
        category=category,
        readme_excerpt=readme_excerpt,
        readme_truncated=truncated,
        release_assets=release_assets,
        allowed_urls=list(dict.fromkeys(allowed_urls)),
        primary_download_url=primary_url,
        primary_download_label=primary_label,
    )


def fetch_repo_by_url(repo_url: str, token: str | None = None) -> ScoutedRepo:
    """Parse a GitHub URL and fetch its bundle safely."""
    match = re.match(r"^https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git|/.*)?$", repo_url.strip())
    if not match:
        raise ValueError(f"URL GitHub non valido: {repo_url}")
    return fetch_repo_bundle(match.group(1), match.group(2), token=token)


def scout_trending_consumer_apps(limit: int = 15, token: str | None = None) -> list[ScoutedRepo]:
    """Query GitHub Search API for popular non-fork consumer repositories (>500 stars)."""
    if token is None:
        token = get_secret("dev.github", "pat", "GITHUB_TOKEN")

    topic_query = " ".join(f"topic:{t}" for t in CONSUMER_TOPICS[:4])
    q = urllib.parse.quote(f"stars:>{MIN_STARS} fork:false archived:false ({topic_query})")
    url = f"{GITHUB_API_BASE}/search/repositories?q={q}&sort=stars&order=desc&per_page={min(limit * 2, 40)}"
    data = _github_get_json(url, token=token)

    results: list[ScoutedRepo] = []
    for item in data.get("items", []):
        if not is_consumer_repo(item):
            continue
        owner = item["owner"]["login"]
        name = item["name"]
        try:
            bundle = fetch_repo_bundle(owner, name, token=token)
            results.append(bundle)
        except Exception:
            continue
        if len(results) >= limit:
            break
    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="HubHum GitHub Consumer Scouter")
    parser.add_argument("--repo", help="Singolo repository owner/name")
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()

    if args.repo:
        owner, name = args.repo.split("/", 1)
        bundle = fetch_repo_bundle(owner, name)
        print(json.dumps({
            "name": bundle.name,
            "slug": bundle.slug,
            "stars": bundle.stars,
            "is_webapp": bundle.is_webapp,
            "category": bundle.category,
            "assets": len(bundle.release_assets),
            "readme_truncated": bundle.readme_truncated,
        }, indent=2))
    else:
        found = scout_trending_consumer_apps(limit=args.limit)
        print(json.dumps([{"name": r.name, "stars": r.stars, "category": r.category} for r in found], indent=2))
