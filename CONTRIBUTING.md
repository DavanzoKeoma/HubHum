# Contributing to HubHum

Thank you for helping make open-source software accessible to everyday people!

## 1. Suggesting a New Application ("Submit an App")

You can propose an open-source application in three ways:

1. **Directly on HubHum:** Use the **Submit an App** form on the homepage (`https://davanzokeoma.github.io/HubHum/#submit`) or the live search action **Go with HubHum**.
2. **Via GitHub Issue Form:** Open a new issue using the [Suggest a Free App](https://github.com/DavanzoKeoma/HubHum/issues/new?template=app_suggestion.yml) template.
3. **Via Pull Request:** Add or update a card in `content/apps/<slug>.md` following the rules below.

## 2. Editorial & Plain-English Standards

- **Zero Tech Jargon:** Explain what the software actually solves in plain language. Avoid developer acronyms (`CLI`, `ORM`, `SDK`, `K8s`, `container`, `stdout`) unless clearly translated into everyday terms.
- **No Truncated Copy:** All English (`summary`) and localized (`i18n.it/es/fr/de`) descriptions must be complete sentences ending in punctuation (never `...` or dangling words).
- **Honest Format Classification:** Set `app_type` accurately (`desktop`, `selfhosted`, `cli`, `webapp`, or `resource`) and keep `operatingSystem` aligned with real official release packages (never claim Android support without an `.apk` or official mobile release).
- **Direct Official Links Only:** Every `source_url` and `download_url` must point strictly to the official upstream GitHub repository, GitHub Releases, or creator's primary website. Never submit third-party download mirrors or wrappers.
- **5-Language Localization:** Include clean translations for `it`, `es`, `fr`, and `de` in frontmatter `i18n`.

## 3. Affiliate & `#ad` Isolation Rules

- Never inject sponsored or `#ad` links inside `What it does in plain English`, `Who it's for`, `Key features`, `How to install (Download)`, or `Pros and Cons`.
- All optional partner links (`hubhum_01_MER*`) must remain isolated inside the `### Sponsored Partner Tools (#ad)` section and match the software domain cleanly.

## 4. Local Validation Before Opening a PR

Run these checks locally before submitting any Pull Request:

```bash
python scripts/generate_catalog_index.py
python scripts/cluster_orchestrator.py --generate-all
python scripts/validator_sanitizer.py --check-all
npm run build
```

All checks must finish with `0` errors and zero leaked credentials or local paths.
