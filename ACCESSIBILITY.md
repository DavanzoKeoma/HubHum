# Accessibility Statement — HubHum

HubHum aims to conform to **WCAG 2.1 Level AA** across all catalog pages, interactive filters, topic guides, and the Chrome extension landing experience (`https://davanzokeoma.github.io/HubHum/`).

## Key Accessibility Measures

- **Color Contrast (Light & Dark Modes):** Body text, navigation controls, status badges (`Desktop App`, `Self-Hosted App`, `CLI Tool`, `Cloud Web App`, `Open Reference`), and interactive callouts maintain at least a `4.5:1` text contrast ratio and `3:1` UI component contrast in both Light and Dark themes (including dedicated dark-mode brand logo wordmark contrast).
- **Keyboard Navigation:** All header controls, category tabs, format/OS quick filters, card links, pagination buttons, and modal dialogs are reachable via `Tab` / `Shift+Tab` with visible `:focus-visible` outlines.
- **Accessible Modals & Live Regions:** The Saved Favorites dialog (`#favorites-dialog`) uses native `<dialog>` semantics with `Escape` key dismissal and focus restoration; live search and form status updates announce changes via `aria-live="polite"`.
- **Semantic Structure:** Every page includes a single logical `<main>` landmark, hierarchical headings (`h1`–`h3`), descriptive `aria-label` attributes, and explicit table headers in comparative guides.
- **Language Switching:** Dynamically updates `document.documentElement.lang` (`en`, `it`, `es`, `fr`, `de`) across cards, headings, and navigation labels.

## Feedback & Contact

If you encounter any accessibility barrier on HubHum, please let us know via:

- Email: `keomadavanzo@gmail.com`
- GitHub Issues: [DavanzoKeoma/HubHum/issues](https://github.com/DavanzoKeoma/HubHum/issues)
