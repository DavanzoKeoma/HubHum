"""3-Tier Cascade AI Router (Google AI Studio -> Groq -> Mistral) with Sezione 7 System Prompt."""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from scouter import ScoutedRepo
from validator_sanitizer import sanitize_full_document, validate_markdown_card
from vault_loader import get_all_runtime_keys

SYSTEM_INSTRUCTION = """[SYSTEM INSTRUCTION FOR AI ROUTER]
You are an expert editor translating technical open-source documentation
for absolute beginners. You receive: (a) the GitHub README, (b) the latest
"Releases" data with exact file names and URLs, (c) the Affiliate Database
mapping for this app's category. Write in Italian.

STRICT RULES:
1. HUMAN TRANSLATION: no technical jargon (avoid "repository", "framework",
   "deploy", "API", "build", "commit", "pull request"). Explain the real-life problem the app solves
   in exactly 3 simple sentences.
2. LINK INTEGRITY: NEVER invent URLs. Use only URLs present in the README
   or in the Releases data. Present download links with clear names, e.g.
   [Scarica per Windows (.exe)](ORIGINAL_URL), but NEVER alter or shorten
   the underlying URL. Ignore technical badges, source archives (.zip,
   .tar.gz) and terminal commands, unless no other alternative exists.
3. AFFILIATE INJECTION: based on the app's category, naturally weave in a
   recommendation for a related service from the Affiliate Database
   mapping, more than once if it fits the text. It must read as valuable
   advice, not spam. Use only links from the provided mapping.
   Example (web CMS): "Non vuoi installarlo a mano? Avvialo in 1 click su
   [Hosting Link]."
4. WEB APPS: if the project is a web application and not a downloadable
   program, set is_webapp: true and mention one-click hosting.
5. BRAND SAFETY: never reproduce third-party trademarks in comparative or
   "killer of X" slogans; replace them with generic terms (e.g. "software
   di design proprietari"). No trademark bidding.
6. CREDITS: always end with a discreet link "Fonte ufficiale / Crediti"
   pointing to the original GitHub repository.

REQUIRED MARKDOWN STRUCTURE (exact headings):
---
title: "{App Name}"
slug: "{app-slug}"
tags: ["{tag1}", "{tag2}"]
is_webapp: {true/false}
---
### Cos'è in parole semplici
{3 sentences}
### A chi è utile
{2-3 practical user profiles}
### Cosa puoi farci
{4-5 concrete features in bullet points}
### Come si installa (Download)
{direct links to executables, or official site URL for web apps}
### Pro e Contro
* **Pro:** {e.g. gratis, senza abbonamenti}
* **Contro:** {e.g. solo in inglese}
[Fonte ufficiale / Crediti]({source_url})"""


class AllTiersFailedError(RuntimeError):
    """Raised when Tier 1, Tier 2, and Tier 3 all fail or lack keys."""


def _post_json(url: str, payload: dict, headers: dict[str, str], timeout: int = 35) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _call_tier1_gemini(api_key: str, user_prompt: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {"temperature": 0.35},
    }
    res = _post_json(url, payload, {"Content-Type": "application/json"})
    return res["candidates"][0]["content"]["parts"][0]["text"]


def _call_tier2_groq(api_key: str, user_prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.35,
    }
    res = _post_json(
        url,
        payload,
        {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
    )
    return res["choices"][0]["message"]["content"]


def _call_tier3_mistral(api_key: str, user_prompt: str) -> str:
    url = "https://api.mistral.ai/v1/chat/completions"
    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.35,
    }
    res = _post_json(
        url,
        payload,
        {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
    )
    return res["choices"][0]["message"]["content"]


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
        f"Detected is_webapp: {str(repo.is_webapp).lower()}\n"
        f"Description: {repo.description}\n\n"
        f"(a) README Excerpt:\n{repo.readme_excerpt}\n\n"
        f"(b) Latest Releases Assets:\n{releases_json}\n\n"
        f"(c) Affiliate Database Mapping:\n{aff_json}\n\n"
        "Output ONLY the Markdown document starting with --- frontmatter."
    )


def generate_card_with_cascade(repo: ScoutedRepo, affiliate_context: dict) -> tuple[str, str]:
    """Try Tier 1 -> Tier 2 -> Tier 3, sanitizing and validating before acceptance."""
    keys = get_all_runtime_keys()
    user_prompt = build_user_prompt(repo, affiliate_context)

    tiers = [
        ("tier1_gemini", keys.get("GEMINI_API_KEY"), _call_tier1_gemini),
        ("tier2_groq", keys.get("GROQ_API_KEY"), _call_tier2_groq),
        ("tier3_mistral", keys.get("MISTRAL_API_KEY"), _call_tier3_mistral),
    ]

    failures: list[str] = []
    for tier_name, api_key, fn in tiers:
        if not api_key:
            failures.append(f"{tier_name}: chiave non configurata")
            continue
        try:
            raw_md = _strip_code_fence(fn(api_key, user_prompt))
            sanitized_md = sanitize_full_document(raw_md)
            errors = validate_markdown_card(
                sanitized_md,
                allowed_urls=repo.allowed_urls,
                strict_urls=True,
            )
            if not errors:
                return sanitized_md, tier_name
            failures.append(f"{tier_name}: validazione fallita ({'; '.join(errors)})")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, KeyError, IndexError, json.JSONDecodeError) as exc:
            failures.append(f"{tier_name}: errore chiamata ({exc})")

    raise AllTiersFailedError(" | ".join(failures))
