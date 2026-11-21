## Summary

<!-- Briefly describe what this Pull Request adds, fixes, or improves. -->

## Compliance Checklist

- [ ] **Zero-Leak:** No tokens, API keys, passwords, `.pcp/` files, or local machine paths added anywhere in the diff.
- [ ] **Plain-English Quality:** Any new/edited app cards avoid developer jargon, truncated summaries (`...` or dangling stopwords), and raw technical licenses (`NOASSERTION`).
- [ ] **Honest Classification:** `app_type` (`desktop`, `selfhosted`, `cli`, `webapp`, `resource`) and `operatingSystem` reflect real upstream releases.
- [ ] **Strict `#ad` Isolation & Domain Coherence:** Exactly 3 distinct contextual partner links (`hubhum_01_MER*`) appear inside `### Sponsored Partner Tools (#ad)` and match the software category, with zero `#ad` links in editorial sections.
- [ ] **Accessibility (WCAG 2.1 AA):** Any UI or theme changes preserve contrast (`>= 4.5:1` text / `>= 3:1` UI) in both Light and Dark modes.
- [ ] **Local Verification Passed:**
  - `python scripts/generate_catalog_index.py`
  - `python scripts/cluster_orchestrator.py --generate-all`
  - `python scripts/validator_sanitizer.py --check-all` (exit code `0`)
  - `npm run build` (zero TypeScript or Astro build errors)
