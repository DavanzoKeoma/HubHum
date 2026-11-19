"""Real-browser Playwright E2E Human Simulation Test for HubHum live site."""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import Page, Response, expect, sync_playwright

LIVE_URL = "https://davanzokeoma.github.io/HubHum/"
WORKER_CONVERT_URL = "https://hubhum-api-bridge.keomadavanzo.workers.dev/api/convert"

EXPECTED_HERO_PREFIX = {
    "it": "Programmi gratuiti e potenti",
    "es": "Software gratuito y potente",
    "fr": "Des logiciels gratuits puissants",
    "de": "Starke kostenlose Software",
    "en": "Powerful free software",
}


def screenshot_dir() -> Path:
    raw = os.environ.get("E2E_SCREENSHOT_DIR", "").strip()
    out = Path(raw) if raw else Path(tempfile.gettempdir()) / "hubhum_e2e_screenshots"
    out.mkdir(parents=True, exist_ok=True)
    return out


def run_step_a_ui_i18n_filters_favorites(page: Page, shots: Path) -> None:
    print("\n=== STEP A: Official Brand, i18n Switcher, Filters & Favorites Modal ===")
    page.goto(LIVE_URL, wait_until="networkidle", timeout=45000)

    logo = page.locator("img.brand-logo")
    expect(logo).to_be_visible(timeout=15000)
    natural_w = logo.evaluate("el => el.naturalWidth")
    logo_src = logo.get_attribute("src") or ""
    assert natural_w > 0 and "logo.svg" in logo_src, f"Brand logo broken: src={logo_src}, width={natural_w}"
    print(f"[PASS] Official navbar logo loaded cleanly ({logo_src}, naturalWidth={natural_w}).")

    lang_select = page.locator("#lang-switcher")
    hero_h1 = page.locator('[data-i18n="heroTitle"]')
    search_eye = page.locator('[data-i18n="liveSearchEyebrow"]')
    footer_aff = page.locator('[data-i18n="footerAffiliate"]')

    for lang in ("it", "es", "fr", "de", "en"):
        lang_select.select_option(lang)
        page.wait_for_function("l => document.documentElement.lang === l", arg=lang, timeout=5000)
        h1_text = hero_h1.inner_text().strip()
        eye_text = search_eye.inner_text().strip()
        foot_text = footer_aff.inner_text().strip()
        assert EXPECTED_HERO_PREFIX[lang].lower() in h1_text.lower(), (
            f"i18n hero mismatch for '{lang}': got '{h1_text}'"
        )
        assert len(eye_text) > 10 and len(foot_text) > 20
        print(f"[PASS] i18n '{lang}' live translation -> hero='{h1_text[:50]}'")
        if lang == "it":
            page.screenshot(path=str(shots / "01_homepage_it.png"), full_page=False)

    page.screenshot(path=str(shots / "02_homepage_en.png"), full_page=False)

    for cat in ("Security & Privacy", "Video & Audio", "Productivity", "All"):
        btn = page.locator(f'[data-category-btn="{cat}"]')
        btn.click()
        expect(btn).to_have_attribute("aria-pressed", "true")
        if cat not in ("All", "Productivity"):
            visible_cats = page.locator('#catalog-grid [data-app-card]:visible').evaluate_all(
                "els => els.map(e => e.getAttribute('data-category'))"
            )
            assert len(visible_cats) >= 1 and all(c == cat for c in visible_cats), (
                f"Category filter '{cat}' failed: {visible_cats}"
            )
        count_txt = page.locator("#catalog-count").inner_text().strip()
        print(f"[PASS] Category filter '{cat}' active -> {count_txt}")

    page.locator('main a[href*="/apps/joplin"]:visible').first.click()
    page.wait_for_load_state("networkidle")
    fav_btn = page.locator("#favorite-btn")
    expect(fav_btn).to_be_visible()
    fav_btn.click()
    saved_ls = page.evaluate("() => localStorage.getItem('hubhum_favorites_v1') || ''")
    assert "joplin" in saved_ls, f"Favorite not persisted in localStorage: {saved_ls}"

    page.locator("#oauth-login-btn").click()
    dialog = page.locator("#account-dialog[open]")
    expect(dialog).to_be_visible(timeout=5000)
    expect(dialog.locator("#dialog-fav-list")).to_contain_text("joplin")
    expect(dialog.locator("#github-1click-signin")).to_be_visible()
    assert dialog.locator("input").count() == 0, "Unexpected manual token input inside OAuth modal!"
    dialog_txt = dialog.inner_text().lower()
    assert "cors" not in dialog_txt, "Forbidden CORS jargon in account modal!"
    page.screenshot(path=str(shots / "03_favorites_modal.png"))
    page.locator("#dialog-close-btn").click()
    print("[PASS] Favorites persistence + Zero-CORS 1-click GitHub OAuth modal verified.")

    page.locator("a.brand").click()
    page.wait_for_load_state("networkidle")


def run_step_b_live_search(page: Page, query: str, shots: Path) -> None:
    print(f"\n=== STEP B: Live GitHub Search ('{query}') ===")
    search_input = page.locator("#gh-live-search-input")
    expect(search_input).to_be_visible()
    search_input.scroll_into_view_if_needed()
    search_input.fill(query)

    results_grid = page.locator("#gh-search-results-grid")
    first_result = results_grid.locator(".live-card:not(.live-skeleton) a.live-repo-link").first
    expect(first_result).to_be_visible(timeout=20000)

    cards = results_grid.locator(".live-card:not(.live-skeleton)")
    card_count = cards.count()
    assert card_count >= 1, "Expected at least 1 live GitHub result card."
    first_card = cards.first
    expect(first_card.locator("img.live-avatar")).to_be_visible()
    expect(first_card.locator(".tag-chip").first).to_be_visible()
    first_title = first_result.inner_text().strip()
    print(f"[PASS] Live search returned {card_count} results (top match: {first_title}).")
    page.screenshot(path=str(shots / "04_live_search_results.png"), full_page=False)


def run_step_c_convert_and_redirect(page: Page, shots: Path) -> str:
    print("\n=== STEP C: Click 'Go with HubHum' & Wait for Real Worker + Actions + Redirect ===")
    convert_responses: list[tuple[int, dict]] = []

    def _on_response(resp: Response) -> None:
        if resp.url.startswith(WORKER_CONVERT_URL) and resp.request.method == "POST":
            try:
                data = resp.json()
            except Exception:
                data = {}
            convert_responses.append((resp.status, data))

    page.on("response", _on_response)

    convert_btn = page.locator("#gh-search-results-grid .live-card button.btn-cloud").first
    expect(convert_btn).to_be_visible(timeout=10000)
    aria_label = convert_btn.get_attribute("aria-label") or ""
    print(f"[INFO] Clicking convert button: {aria_label}")
    convert_btn.click()

    conv_dialog = page.locator("#conversion-dialog[open]")
    expect(conv_dialog).to_be_visible(timeout=5000)
    expect(conv_dialog.locator("#conv-spinner-icon")).to_be_visible()
    expect(conv_dialog.locator("#conv-progressbar")).to_be_visible()

    assert conv_dialog.locator('a[href*="/issues"]').count() == 0, "Unexpected GitHub Issue link inside modal!"

    page.wait_for_function("() => document.getElementById('conv-pct-label')?.textContent !== '0%'", timeout=15000)
    page.screenshot(path=str(shots / "05_conversion_progress.png"))

    deadline_wait = 0
    while not convert_responses and deadline_wait < 25:
        page.wait_for_timeout(500)
        deadline_wait += 1
    assert convert_responses, "No POST response observed from Worker /api/convert!"
    status_code, body_json = convert_responses[0]
    assert status_code == 200 and body_json.get("status") == "queued" and body_json.get("slug"), (
        f"Worker /api/convert failed: status={status_code}, body={body_json}"
    )
    print(f"[PASS] Worker POST /api/convert returned HTTP {status_code}: {body_json}")

    print("[INFO] Waiting for GitHub Actions seo-builder + deploy + auto-redirect (up to 180s)...")
    page.wait_for_url(re.compile(r".*/apps/[a-z0-9-]+/?$"), timeout=185000)
    page.wait_for_load_state("networkidle", timeout=30000)
    final_url = page.url
    print(f"[PASS] Browser automatically redirected to new app page: {final_url}")
    return final_url


def run_step_d_verify_generated_page(page: Page, page_url: str, shots: Path) -> None:
    print(f"\n=== STEP D: Verify Generated Page Content & 3+ Affiliate Links ({page_url}) ===")
    resp = page.request.get(page_url)
    assert resp.status == 200, f"Expected HTTP 200 for {page_url}, got {resp.status}"

    h1 = page.locator("main h1").first
    expect(h1).to_be_visible(timeout=10000)
    title_text = h1.inner_text().strip()
    assert len(title_text) > 1, "Missing <h1> title on generated page."

    hero_sum = page.locator("#detail-hero-summary").inner_text().strip()
    assert not hero_sum.endswith("..."), f"Truncated summary found: {hero_sum}"

    credits_link = page.locator('article a[href*="github.com/"]').first
    expect(credits_link).to_be_visible()

    primary_cta = page.locator(".detail-actions a.btn").first
    expect(primary_cta).to_be_visible()
    cta_href = primary_cta.get_attribute("href") or ""
    assert cta_href.startswith("https://"), f"Unexpected primary CTA href: {cta_href}"

    aff_hrefs = page.locator('article a[href*="hubhum_01_MER"]').evaluate_all(
        "els => els.map(e => e.getAttribute('href'))"
    )
    unique_subids = set(re.findall(r"hubhum_01_MER\d+", " ".join(h or "" for h in aff_hrefs)))
    assert len(unique_subids) >= 3, f"Expected >= 3 distinct affiliate SubIDs, found {len(unique_subids)}: {unique_subids}"

    article_text = page.locator("article").inner_text().lower()
    article_text_no_links = re.sub(r"https?://\S+", "", article_text)
    for forbidden in ("pull request", "commit ", "repository"):
        assert forbidden not in article_text_no_links, f"Forbidden tech jargon '{forbidden}' in generated article!"

    page.screenshot(path=str(shots / "06_converted_app_page.png"), full_page=True)
    print(
        f"[PASS] Page verified (HTTP 200, title='{title_text}', CTA='{urlparse(cta_href).netloc}', "
        f"affiliate_subids={sorted(unique_subids)})."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="HubHum Real Browser E2E Human Simulation Test")
    parser.add_argument("--query", default="handbrake", help="Live GitHub search query for an unindexed consumer app")
    args = parser.parse_args()

    shots = screenshot_dir()
    print(f"[INFO] Saving E2E screenshots to: {shots}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1366, "height": 900}, locale="en-US")
        page = context.new_page()
        try:
            run_step_a_ui_i18n_filters_favorites(page, shots)
            run_step_b_live_search(page, args.query, shots)
            generated_url = run_step_c_convert_and_redirect(page, shots)
            run_step_d_verify_generated_page(page, generated_url, shots)
        finally:
            context.close()
            browser.close()

    print("\nALL E2E HUMAN SIMULATION STEPS (A, B, C, D) PASSED 100%.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
