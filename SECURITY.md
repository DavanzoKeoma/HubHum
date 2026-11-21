# Security Policy

## Scope & Security Model

HubHum is a static open-source software directory generated with Astro and deployed via GitHub Pages. It does not host user accounts, store passwords, execute user-submitted binaries, or distribute repackaged installers. Primary download links route directly to upstream author repositories and official releases.

## Supported Versions

Only the latest deployment built from the `main` branch (`https://davanzokeoma.github.io/HubHum/`) and the Cloudflare Workers OAuth/Dispatch bridge (`workers/github-oauth-proxy/`) are actively supported.

## Reporting a Vulnerability or Malicious Software Listing

If you discover:

- A security vulnerability in the website, Cloudflare Worker, Chrome Extension, or GitHub Actions pipeline;
- A listed upstream repository that has been compromised, hijacked, or distributes malware;
- Exposed credentials or sensitive data anywhere in the repository;

Please report it confidentially to **`keomadavanzo@gmail.com`** (or open a private Security Advisory on GitHub) with:

1. Affected URL, file path, or listed application slug (`content/apps/<slug>.md`).
2. Steps to reproduce or evidence of compromise.
3. Suggested remediation or takedown request details.

## Rapid Quarantine & Takedown SLA

- Compromised or malicious upstream software listings are added immediately to `data/takedown_blocklist.json`, removed from `content/apps/` and `public/catalog-index.json`, and rebuilt on GitHub Pages typically within 24 hours of confirmation.
- Reported security issues in project scripts or Workers receive an initial acknowledgment within 48 hours.
