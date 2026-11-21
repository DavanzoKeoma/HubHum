"""Real-browser Playwright E2E Human Simulation Test (Desktop + Mobile) & Blind Audit Capture for HubHum."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import Page, expect, sync_playwright

LIVE_URL = "https://davanzokeoma.github.io/HubHum/"
WORKER_HEALTH_URL = "https://hubhum-api-bridge.keomadavanzo.workers.dev/api/health"
WORKER_CONVERT_URL = "https://hubhum-api-bridge.keomadavanzo.workers.dev/api/convert"

EXPECTED_HERO_PREFIX = {
    "it": "Programmi gratuiti e potenti",
    "es": "Software gratuito y potente",
    "fr": "Des logiciels gratuits puissants",
    "de": "Starke kostenlose Software",
    "en": "Powerful free software",
}


def screenshot_dir(custom: str = "") -> Path:
    raw = custom.strip() or os.environ.get("E2E_SCREENSHOT_DIR", "").strip()
    out = Path(raw) if raw else Path(tempfile.gettempdir()) / "hubhum_e2e_screenshots"
    out.mkdir(parents=True, exist_ok=True)
    return out


def verify_worker_health() -> None:
    print("\n=== STEP 0: Cloudflare Worker /api/health Verification ===")
    req = urllib.request.Request(WORKER_HEALTH_URL, headers={"User-Agent": "HubHum-E2E/2.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        assert resp.status == 200, f"Worker /api/health returned HTTP {resp.status}"
        data = json.loads(resp.read().decode("utf-8"))
        print(f"[PASS] Worker /api/health -> HTTP 200: {data}")


def verify_theme_and_i18n(page: Page, shots: Path) -> None:
    print("\n=== STEP A1: Brand, Light/Dark Theme Toggle & 5-Language i18n ===")
    page.goto(LIVE_URL, wait_until="networkidle", timeout=45000)

    logo = page.locator("img.brand-logo")
    expect(logo).to_be_visible(timeout=15000)
    natural_w = logo.evaluate("el => el.naturalWidth")
    logo_src = logo.get_attribute("src") or ""
    assert natural_w > 0 and "logo.svg" in logo_src, f"Brand logo broken: src={logo_src}, width={natural_w}"
    print(f"[PASS] Navbar logo loaded ({logo_src}, naturalWidth={natural_w}).")

    # Light <-> Dark mode toggle check
    theme_btn = page.locator("#theme-toggle-btn")
    expect(theme_btn).to_be_visible()
    initial_theme = page.evaluate("() => document.documentElement.dataset.theme")
    theme_btn.click()
    toggled_theme = page.evaluate("() => document.documentElement.dataset.theme")
    assert toggled_theme != initial_theme and toggled_theme in ("light", "dark"), (
        f"Theme did not toggle: before={initial_theme}, after={toggled_theme}"
    )
    if toggled_theme == "dark":
        page.screenshot(path=str(shots / "01_home_desktop_dark.png"), full_page=False)
        theme_btn.click()
    assert page.evaluate("() => document.documentElement.dataset.theme") == "light"
    page.screenshot(path=str(shots / "02_home_desktop_light.png"), full_page=False)
    print(f"[PASS] Light/Dark theme toggle verified (initial={initial_theme}, toggled={toggled_theme}).")

    # 5-language switcher check
    lang_select = page.locator("#lang-switcher")
    hero_h1 = page.locator('[data-i18n="heroTitle"]')
    nav_guides = page.locator('header nav [data-i18n="navGuides"]')
    footer_disc = page.locator('footer [data-i18n="footerDisclaimer"]')
    footer_aff = page.locator('footer [data-i18n="footerAffiliate"]')

    for lang in ("it", "es", "fr", "de", "en"):
        lang_select.select_option(lang)
        page.wait_for_function("l => document.documentElement.lang === l", arg=lang, timeout=5000)
        h1_text = hero_h1.inner_text().strip()
        guides_text = nav_guides.inner_text().strip()
        disc_text = footer_disc.inner_text().strip()
        aff_text = footer_aff.inner_text().strip()
        assert EXPECTED_HERO_PREFIX[lang].lower() in h1_text.lower(), f"i18n hero mismatch '{lang}': {h1_text}"
        assert len(guides_text) > 5 and len(disc_text) > 15 and len(aff_text) > 20
        print(f"[PASS] i18n '{lang}' active -> hero='{h1_text[:45]}', nav='{guides_text}'")


def verify_pagination_and_underlinenav(page: Page) -> None:
    print("\n=== STEP A2: UnderlineNav Category Counters & 24-Apps-Per-Page Pagination ===")
    initial_cards = page.locator("#catalog-grid [data-app-card]").count()
    assert initial_cards == 24, f"Expected strictly 24 initial DOM cards for PageSpeed, got {initial_cards}"
    print(f"[PASS] Initial Home DOM contains {initial_cards} paginated cards.")

    # Verify counters on UnderlineNav
    for cat in ("All", "Productivity", "Security & Privacy", "Video & Audio", "Web Apps & Cloud", "Utilities & Power Tools"):
        cnt = int(page.locator(f'[data-cat-count="{cat}"]').inner_text().strip())
        assert cnt >= 10, f"Expected >= 10 apps in '{cat}', got {cnt}"

    # Load 24 more button -> 48 cards
    load_more = page.locator("#load-more-btn")
    expect(load_more).to_be_visible()
    load_more.click()
    page.wait_for_function("() => document.querySelectorAll('#catalog-grid [data-app-card]').length === 48", timeout=15000)
    print("[PASS] 'Load 24 more' dynamically rendered 48 cards.")

    # Next page -> Page 2 via UnderlineNav filter determinism
    for cat in ("Security & Privacy", "Video & Audio", "All"):
        expected_cnt = page.locator(f'[data-cat-count="{cat}"]').inner_text().strip()
        btn = page.locator(f'[data-category-btn="{cat}"]')
        btn.click()
        expect(btn).to_have_attribute("aria-pressed", "true")
        page.wait_for_function(
            "prefix => (document.getElementById('catalog-count')?.textContent || '').trim().startsWith(prefix + ' ')",
            arg=expected_cnt,
            timeout=15000,
        )
        if cat != "All":
            cats = page.locator("#catalog-grid [data-app-card]").evaluate_all(
                "els => els.map(e => e.getAttribute('data-category'))"
            )
            assert len(cats) >= 1 and all(c == cat for c in cats), f"Category filter '{cat}' failed: {cats}"
        print(f"[PASS] UnderlineNav '{cat}' -> {page.locator('#catalog-count').inner_text().strip()}")

    page.locator("#page-next-btn").click()
    page.wait_for_function("() => document.getElementById('page-num')?.textContent === '2'", timeout=10000)
    page_2_cards = page.locator("#catalog-grid [data-app-card]").count()
    assert page_2_cards == 24, f"Expected 24 cards on Page 2, got {page_2_cards}"
    print("[PASS] Pagination 'Next' switched cleanly to Page 2 (24 cards).")
    page.locator("#page-prev-btn").click()
    page.wait_for_function("() => document.getElementById('page-num')?.textContent === '1'", timeout=10000)

    # Verify honest type badges and stars (never "Chosen by ... users")
    body_text = page.locator("main").inner_text()
    assert "Chosen by" not in body_text, "Found legacy ambiguous 'Chosen by' copy!"
    assert "★" in body_text, "Missing transparent star badge '★'!"


def verify_favorites_dialog_a11y(page: Page) -> None:
    print("\n=== STEP A3: Favorites Dialog (#favorites-dialog) & Keyboard Esc ===")
    page.goto(f"{LIVE_URL}apps/handbrake/", wait_until="networkidle", timeout=30000)
    fav_btn = page.locator("#favorite-btn")
    expect(fav_btn).to_be_visible()
    fav_btn.click()
    saved_ls = page.evaluate("() => localStorage.getItem('hubhum_favorites_v1') || ''")
    assert "handbrake" in saved_ls, f"Favorite missing in localStorage: {saved_ls}"

    login_btn = page.locator("#oauth-login-btn")
    login_btn.click()
    dialog = page.locator("#favorites-dialog[open]")
    expect(dialog).to_be_visible(timeout=5000)
    expect(dialog.locator("#dialog-fav-list")).to_contain_text("handbrake")
    assert dialog.locator("input").count() == 0, "Unexpected manual token input in dialog!"
    page.keyboard.press("Escape")
    expect(dialog).not_to_be_visible(timeout=3000)
    print("[PASS] #favorites-dialog opened, listed favorite, and closed via Escape key.")


def verify_five_level_topic_clusters(page: Page, shots: Path, audit_dir: Path | None = None) -> None:
    print("\n=== STEP B: Full 5-Level Topic Cluster Traversal & Bi-Directional Internal Links ===")
    # Level 0 Home -> Level 1 Guides Hub -> Level 1 Pillar (video-audio)
    page.goto(LIVE_URL, wait_until="networkidle", timeout=30000)
    if audit_dir:
        page.screenshot(path=str(audit_dir / "home_desktop.png"), full_page=False)
        (audit_dir / "home_text.txt").write_text(page.locator("body").inner_text(), encoding="utf-8")

    page.locator('header a[href*="/guides/"]').first.click()
    page.wait_for_load_state("networkidle")
    assert "/guides/" in page.url

    # Navigate to Video & Audio Level 1 Pillar
    page.locator('a[href*="/guides/video-audio/"]').first.click()
    page.wait_for_load_state("networkidle")
    assert page.url.rstrip("/").endswith("/guides/video-audio")
    l1_ld = page.evaluate("() => document.querySelector('script[type=\"application/ld+json\"]')?.textContent || ''")
    assert "CollectionPage" in l1_ld and "BreadcrumbList" in l1_ld, "Missing CollectionPage/BreadcrumbList JSON-LD on Level 1!"
    print(f"[PASS] Level 1 Pillar reached: {page.url}")

    # Level 1 -> Level 2 Sub-Pillar
    page.locator('a[href*="/guides/video-audio/free-video-editors/"]').first.click()
    page.wait_for_load_state("networkidle")
    assert page.url.rstrip("/").endswith("/guides/video-audio/free-video-editors")
    print(f"[PASS] Level 2 Sub-Pillar reached: {page.url}")

    # Level 2 -> Level 3 Comparison Guide
    page.locator('a[href*="/guides/video-audio/free-video-editors/best-free-video-editors/"]').first.click()
    page.wait_for_load_state("networkidle")
    assert "best-free-video-editors" in page.url
    l3_ld = page.evaluate("() => document.querySelector('script[type=\"application/ld+json\"]')?.textContent || ''")
    assert '"Article"' in l3_ld and "BreadcrumbList" in l3_ld, "Missing Article/BreadcrumbList JSON-LD on Level 3!"
    page.screenshot(path=str(shots / "03_level3_cluster_guide.png"), full_page=False)
    if audit_dir:
        page.screenshot(path=str(audit_dir / "guide_level3_desktop.png"), full_page=False)
        (audit_dir / "guide_level3_text.txt").write_text(page.locator("body").inner_text(), encoding="utf-8")
    print(f"[PASS] Level 3 Cluster Article reached: {page.url}")

    # Horizontal sibling link inside "Related Guides in This Topic"
    sibling_link = page.locator('[aria-labelledby="sibling-guides-heading"] a.app-card').first
    expect(sibling_link).to_be_visible()
    sib_href = sibling_link.get_attribute("href") or ""
    assert "how-to-choose-" in sib_href or "troubleshooting-" in sib_href
    sibling_link.click()
    page.wait_for_load_state("networkidle")
    print(f"[PASS] Horizontal sibling traversal succeeded -> {page.url}")

    # Level 3 -> Level 4 Money Page (featured app card)
    app_link = page.locator('[aria-labelledby="cluster-apps-heading"] a.app-card').first
    expect(app_link).to_be_visible()
    app_link.click()
    page.wait_for_load_state("networkidle")
    assert "/apps/" in page.url

    # Verify Level 4 Money Page upward cluster links, JSON-LD, 3 affiliate links, no jargon
    up_pillar = page.locator('aside a[href*="/guides/video-audio/"]').first
    expect(up_pillar).to_be_visible()
    l4_ld = page.evaluate("() => document.querySelector('script[type=\"application/ld+json\"]')?.textContent || ''")
    assert "SoftwareApplication" in l4_ld or "WebApplication" in l4_ld
    assert "BreadcrumbList" in l4_ld

    aff_hrefs = page.locator('article a[href*="hubhum_01_MER"]').evaluate_all(
        "els => els.map(e => e.getAttribute('href'))"
    )
    unique_subids = set(re.findall(r"hubhum_01_MER\d+", " ".join(h or "" for h in aff_hrefs)))
    assert len(unique_subids) >= 3, f"Expected >= 3 distinct affiliate links on Level 4, found {unique_subids}"

    page.screenshot(path=str(shots / "04_level4_app_detail.png"), full_page=False)
    if audit_dir:
        page.screenshot(path=str(audit_dir / "app_level4_desktop.png"), full_page=False)
        (audit_dir / "app_level4_text.txt").write_text(page.locator("body").inner_text(), encoding="utf-8")
    print(f"[PASS] Level 4 Money Page verified (upward cluster links, JSON-LD, SubIDs={sorted(unique_subids)}): {page.url}")


def verify_live_github_search(page: Page, query: str) -> None:
    print(f"\n=== STEP C: Live GitHub Search ('{query}') ===")
    page.goto(LIVE_URL, wait_until="networkidle", timeout=30000)
    search_input = page.locator("#gh-live-search-input")
    search_input.scroll_into_view_if_needed()
    search_input.fill(query)

    results_grid = page.locator("#gh-search-results-grid")
    first_result = results_grid.locator(".live-card:not(.live-skeleton) a.live-repo-link").first
    expect(first_result).to_be_visible(timeout=20000)
    cards = results_grid.locator(".live-card:not(.live-skeleton)")
    assert cards.count() >= 1
    first_btn_or_link = cards.first.locator("a.btn, button.btn").first
    expect(first_btn_or_link).to_be_visible()
    print(f"[PASS] Live GitHub Search returned {cards.count()} cards; primary action='{first_btn_or_link.inner_text().strip()}'.")


def verify_mobile_viewport(p_playwright, shots: Path, audit_dir: Path | None = None) -> None:
    print("\n=== STEP D: Mobile Viewport (375x812) Navigation, Drawer & Overflow Check ===")
    browser = p_playwright.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 375, "height": 812}, is_mobile=True, has_touch=True, locale="en-US")
    m_page = ctx.new_page()
    try:
        m_page.goto(LIVE_URL, wait_until="networkidle", timeout=45000)
        # Check horizontal overflow <= 1px
        has_overflow = m_page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth + 1")
        assert not has_overflow, "Detected horizontal overflow on 375px mobile viewport!"

        # Check mobile menu drawer
        menu_btn = m_page.locator("#mobile-menu-btn")
        expect(menu_btn).to_be_visible()
        menu_btn.click()
        drawer = m_page.locator("#mobile-drawer")
        expect(drawer).to_be_visible()
        expect(drawer.locator('a[href*="/guides/"]')).to_be_visible()
        menu_btn.click()

        m_page.screenshot(path=str(shots / "05_home_mobile.png"), full_page=False)
        if audit_dir:
            m_page.screenshot(path=str(audit_dir / "home_mobile.png"), full_page=False)
        print("[PASS] 375x812 Mobile layout zero horizontal overflow & drawer verified.")
    finally:
        ctx.close()
        browser.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="HubHum Full Desktop + Mobile E2E Verification Suite")
    parser.add_argument("--query", default="handbrake", help="Live GitHub Search query")
    parser.add_argument("--screenshots-dir", default="", help="Optional output folder for E2E screenshots")
    parser.add_argument("--blind-audit-dir", default="", help="Optional folder for capturing DOM text + screenshots")
    args = parser.parse_args()

    shots = screenshot_dir(args.screenshots_dir)
    audit_dir = Path(args.blind_audit_dir) if args.blind_audit_dir.strip() else None
    if audit_dir:
        audit_dir.mkdir(parents=True, exist_ok=True)

    verify_worker_health()

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800}, locale="en-US")
        page = context.new_page()
        try:
            verify_theme_and_i18n(page, shots)
            verify_pagination_and_underlinenav(page)
            verify_favorites_dialog_a11y(page)
            verify_five_level_topic_clusters(page, shots, audit_dir=audit_dir)
            verify_live_github_search(page, args.query)
        finally:
            context.close()
            browser.close()

        verify_mobile_viewport(pw, shots, audit_dir=audit_dir)

    print("\nALL DESKTOP + MOBILE E2E & TOPIC CLUSTER CHECKS PASSED 100%.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
