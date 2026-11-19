"""2-Tier Cascade AI Router (Google AI Studio Gemini -> Groq) outputting native English + i18n frontmatter."""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from scouter import ScoutedRepo
from validator_sanitizer import ensure_triplet_links_in_body, sanitize_full_document, validate_markdown_card
from vault_loader import get_all_runtime_keys

GEMINI_FLASH_MODELS = (
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash",
)

GROQ_CHAT_MODELS = (
    "openai/gpt-oss-120b",
    "qwen/qwen3.8-27b",
    "llama-3.3-70b-versatile",
)

SYSTEM_INSTRUCTION = """[SYSTEM INSTRUCTION FOR AI ROUTER]
You are an expert editor translating technical open-source documentation
for everyday non-technical readers. You receive: (a) the project README,
(b) the latest release assets with exact file names and URLs, and (c) the
Affiliate Database mapping for this app's category.

Write the main document in clear, natural ENGLISH, AND generate concise
localized summaries + taglines inside the YAML frontmatter `i18n` block
for `it`, `es`, `fr`, and `de` in this single response.

STRICT RULES:
1. PLAIN LANGUAGE: zero tech jargon (avoid "repository", "framework",
   "deploy", "API", "build", "commit", "pull request"). Explain the real-life
   problem the app solves in 3 crisp, friendly sentences.
2. COMPLETE SUMMARIES (NO ELLIPSIS): write `tagline` (max 55 chars) and
   `summary` (90-145 chars, complete sentence ending with a period, NEVER
   truncated with "..."). Same completeness rule for `i18n.it/es/fr/de`.
3. LINK INTEGRITY: NEVER invent URLs. Use only URLs present in the README
   or in the Releases data. Present download links with clear labels, e.g.
   [Download for Windows (.exe)](ORIGINAL_URL). Ignore badges, source
   archives (.zip, .tar.gz), and terminal commands unless no installer exists.
4. TRIPLE NATURAL AFFILIATE INJECTION: `(c) Affiliate Database Mapping`
   provides a `recommended_triplet` of 3 distinct, policy-audited partner
   tools for this app's category. Naturally weave ALL 3 distinct affiliate
   URLs (each with a discreet `(#ad)` disclosure) into 3 separate sections:
   - 1 contextual tip inside `### What it does in plain English`
   - 1 complementary productivity/media/SEO bullet inside `### Key features`
   - 1 privacy/hosting/transfer tip inside `### How to install (Download)`
   Never lump all 3 links into the same paragraph and never spam.
   For web apps (`is_webapp: true`), mention opening in the cloud in 1 click.
5. BRAND SAFETY: never use comparative "killer of X" slogans or third-party
   trademarks; replace them with generic terms (e.g. "commercial video editors").
6. CREDITS: always end with `[Official Source / Credits](SOURCE_URL)`.

REQUIRED MARKDOWN STRUCTURE (exact headings):
---
title: "{App Name}"
slug: "{app-slug}"
tagline: "{Short 4-7 word value hook}"
summary: "{Complete 1-2 sentence plain-English summary ending with a period.}"
tags: ["{tag1}", "{tag2}"]
is_webapp: {true/false}
i18n:
  it:
    tagline: "{Italian tagline}"
    summary: "{Complete 1-2 sentence Italian summary ending with a period.}"
  es:
    tagline: "{Spanish tagline}"
    summary: "{Complete 1-2 sentence Spanish summary ending with a period.}"
  fr:
    tagline: "{French tagline}"
    summary: "{Complete 1-2 sentence French summary ending with a period.}"
  de:
    tagline: "{German tagline}"
    summary: "{Complete 1-2 sentence German summary ending with a period.}"
---
### What it does in plain English
{3 simple sentences}
### Who it's for
{2-3 practical everyday user profiles}
### Key features
{4-5 concrete bullet points}
### How to install (Download)
{direct links to installers, or official site + 1-click cloud hosting link for web apps}
### Pros and Cons
* **Pros:** {e.g. free forever, no subscription}
* **Cons:** {e.g. advanced options take a few minutes to learn}
[Official Source / Credits]({source_url})"""


class AllTiersFailedError(RuntimeError):
    """Raised when Tier 1 (Gemini) and Tier 2 (Groq) both fail or lack keys."""


def _post_json(url: str, payload: dict, headers: dict[str, str], timeout: int = 35) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _call_tier1_gemini(api_key: str, user_prompt: str) -> tuple[str, str]:
    """Call Google AI Studio Flash models using X-goog-api-key header."""
    last_err: Exception | None = None
    for model_name in GEMINI_FLASH_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
        payload = {
            "system_instruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
            "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
            "generationConfig": {"temperature": 0.3},
        }
        try:
            res = _post_json(
                url,
                payload,
                {"Content-Type": "application/json", "X-goog-api-key": api_key},
                timeout=35,
            )
            return res["candidates"][0]["content"]["parts"][0]["text"], f"tier1_gemini:{model_name}"
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, KeyError, IndexError, json.JSONDecodeError) as exc:
            last_err = exc
            continue
    raise last_err or RuntimeError("No Gemini Flash model available")


def _call_tier2_groq(api_key: str, user_prompt: str) -> tuple[str, str]:
    """Call Groq Cloud chat models with automatic fallback across active models."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    last_err: Exception | None = None
    for model_name in GROQ_CHAT_MODELS:
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
        }
        try:
            res = _post_json(
                url,
                payload,
                {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}", "User-Agent": "HubHum-Router/1.0"},
                timeout=35,
            )
            content = (res["choices"][0]["message"]["content"] or "").strip()
            if not content:
                raise RuntimeError(f"Empty response from Groq ({model_name})")
            return content, f"tier2_groq:{model_name}"
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, KeyError, IndexError, json.JSONDecodeError, RuntimeError) as exc:
            last_err = exc
            continue
    raise last_err or RuntimeError("No Groq chat model available")


def _strip_code_fence(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            cleaned = "\n".join(lines[1:-1]).strip()
    return cleaned


def build_user_prompt(repo: ScoutedRepo, affiliate_context: dict) -> str:
    """Assemble input payload (a) README, (b) Releases data, (c) Affiliate mapping."""
    releases_json = json.dumps(repo.release_assets[:8], ensure_ascii=False, indent=2)
    aff_json = json.dumps(affiliate_context, ensure_ascii=False, indent=2)
    return (
        f"App Name: {repo.name}\n"
        f"Suggested Slug: {repo.slug}\n"
        f"Source URL: {repo.html_url}\n"
        f"Primary Download or Site URL: {repo.primary_download_url}\n"
        f"Detected is_webapp: {str(repo.is_webapp).lower()}\n"
        f"Description: {repo.description}\n\n"
        f"(a) README Excerpt:\n{repo.readme_excerpt}\n\n"
        f"(b) Latest Releases Assets:\n{releases_json}\n\n"
        f"(c) Affiliate Database Mapping:\n{aff_json}\n\n"
        "Output ONLY the Markdown document starting with --- frontmatter."
    )


def generate_card_with_cascade(
    repo: ScoutedRepo,
    affiliate_context: dict,
    force_provider: str = "auto",
) -> tuple[str, str]:
    """Run 2-Tier Cascade (Tier 1 Gemini -> Tier 2 Groq) or forced provider."""
    keys = get_all_runtime_keys()
    user_prompt = build_user_prompt(repo, affiliate_context)

    all_tiers = [
        ("gemini", "tier1_gemini", keys.get("GEMINI_API_KEY"), _call_tier1_gemini),
        ("groq", "tier2_groq", keys.get("GROQ_API_KEY"), _call_tier2_groq),
    ]
    if force_provider in ("gemini", "groq"):
        tiers = [t for t in all_tiers if t[0] == force_provider]
    else:
        tiers = all_tiers

    failures: list[str] = []
    for _, tier_name, api_key, fn in tiers:
        if not api_key:
            failures.append(f"{tier_name}: missing API key")
            continue
        try:
            raw_text, provider_label = fn(api_key, user_prompt)
            raw_md = _strip_code_fence(raw_text)
            triplet = affiliate_context.get("recommended_triplet") or []
            if triplet and "\n---\n" in raw_md:
                hdr, bd = raw_md.split("\n---\n", 1)
                raw_md = f"{hdr}\n---\n\n{ensure_triplet_links_in_body(bd.strip(), triplet)}\n"
            sanitized_md = sanitize_full_document(raw_md)
            if "Official Source / Credits" not in sanitized_md:
                sanitized_md = sanitized_md.rstrip() + f"\n\n[Official Source / Credits]({repo.html_url})\n"
            errors = validate_markdown_card(
                sanitized_md,
                allowed_urls=repo.allowed_urls,
                strict_urls=True,
            )
            if not errors:
                return sanitized_md, provider_label
            failures.append(f"{tier_name}: validation failed ({'; '.join(errors)})")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, KeyError, IndexError, json.JSONDecodeError, RuntimeError) as exc:
            failures.append(f"{tier_name}: call error ({exc})")

    raise AllTiersFailedError(" | ".join(failures))
