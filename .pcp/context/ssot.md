---
schema_version: "1.0"
project:
  id: hubhum
  name: "HubHum – a Git Hub for Humans"
  type: software
  version: "0.1.0"
  status: active
  last_updated: "2026-11-18T14:35:00+01:00"
  owners: ["DavanzoKeoma"]
  tags: ["astro", "github-pages", "programmatic-seo", "ai-cascade"]
  adapters: ["hubhum-astro-seo"]
  environments: ["local", "github-pages"]
metrics:
  health: 1.0
  velocity: 1.0
  risk: 0.15
  coverage: 0.9
sections:
  - id: manifest
  - id: identity
  - id: goals
  - id: constraints
  - id: domain
  - id: state
  - id: tasks
  - id: decisions
  - id: artifacts
  - id: metrics
  - id: events
  - id: policies
  - id: risks
  - id: interfaces
  - id: absorb_archive
  - id: glossary
  - id: changelog
---

<!-- @section:manifest -->
# Manifest Operativo
- **Progetto:** HubHum (`hubhum`)
- **Origine:** [HubHum – a Git Hub for Humans.md](../../HubHum%20%E2%80%93%20a%20Git%20Hub%20for%20Humans.md)
- **Namespace GitHub:** `DavanzoKeoma/HubHum` (`keomadavanzo@gmail.com`)
- **Adapter attivo:** `.agents/adapters/hubhum-astro-seo.yaml`

<!-- @section:identity -->
# Identità del Progetto
HubHum traduce progetti open-source tecnici in un catalogo consumer accessibile stile App Store / Product Hunt, monetizzato con raccomandazioni contestuali di affiliazione e ospitato al 100% su infrastruttura gratuita GitHub (Pages + Actions).

<!-- @section:goals -->
# Obiettivi
1. Sito statico Astro SSG con Content Collections e validazione Zod rigorosa (`title`, `slug`, `tags`, `is_webapp`).
2. Interfaccia Zero Git-Jargon con ricerca istantanea, categorie umane, griglia settimanale e switch `Scarica Gratis` / `Lancia nel Cloud`.
3. Pipeline notturna autonoma (scouting GitHub API > 500 stelle, troncamento README 500 righe, cascata AI Gemini -> Groq -> Mistral, sanitizzazione brand safety).
4. Data Handoff da `affiliatechproject` in `data/affiliates_seed.json` con SubID dedicato `hubhum_01_<MER_ID>`.
5. Automazioni di manutenzione (link checker settimanale, bundle mensili, sync affiliati, Dependabot auto-merge, takedown < 60s) e predisposizione MCP + GitHub OAuth.

<!-- @section:constraints -->
# Vincoli Inviolabili
- **Regola NO-FORK:** nessun fork dei repository sorgenti.
- **Zero-Leak:** chiavi API solo in `.pcp/vault.local.jsonl` (locale) o GitHub Actions Secrets (remoto).
- **Zero Git-Jargon:** nessun termine tecnico (`commit`, `pull request`, `deploy`, `repository`) visibile nel frontend consumer.
- **Brand Safety:** nessun marchio terzo in slogan comparativi ("killer di X"); nessuna alterazione degli URL ufficiali di download.
- **Disclaimer & Disclosure:** footer obbligatorio GitHub non-affiliation + disclosure FTC/affiliazioni.

<!-- @section:domain -->
# Dominio e Architettura
- **Frontend:** Astro SSG (`src/layouts/`, `src/pages/`, `src/content.config.ts`) -> `dist/`
- **Contenuti:** `content/apps/*.md`, `content/bundles/*.md`
- **Affiliazioni:** `data/affiliates_seed.json` (14 merchant da `affiliatechproject`)
- **Automazione Python:** `scripts/` (`vault_loader.py`, `export_affiliates.py`, `scouter.py`, `ai_router.py`, `validator_sanitizer.py`, `seo_pipeline.py`, `affiliate_sync.py`, `link_checker.py`, `bundle_generator.py`, `takedown.py`, `takedown.sh`)
- **Predisposizione Esterna:** `src/mcp/server.py`, `src/lib/github-oauth.ts`

<!-- @section:state -->
# Stato Corrente
- Workspace inizializzato e validato: Astro SSG (`5` pagine statiche in `dist/`), 14 merchant esportati in `data/affiliates_seed.json`, pipeline Python, server MCP e 6 workflow GitHub Actions + Dependabot pronti.
- In attesa di inserimento chiavi API locali da parte dell'utente in `.pcp/vault.local.jsonl` (o `.env`) e GitHub Secrets remoti.

<!-- @section:tasks -->
# Task Attivi
- [x] Bootstrap PCP e configurazione Git (`DavanzoKeoma`)
- [x] Estrazione 14 merchant in `data/affiliates_seed.json`
- [x] Setup Astro SSG, Content Collections Zod e UI Zero Git-Jargon
- [x] Pipeline Python (scouting, AI cascade, sanitizer, manutenzione, takedown, MCP/OAuth)
- [x] Workflow GitHub Actions e Dependabot
- [x] Test E2E con 3 app reali (`losslesscut`, `keepassxc`, `ghost`) e build statica

<!-- @section:decisions -->
# Decisioni Architetturali
- **GitHub Models escluso:** dismesso il 30 luglio 2026; cascata fissata su Google AI Studio (`gemini-2.5-flash`) -> Groq (`llama-3.3-70b-versatile`) -> Mistral (`mistral-small-latest`).
- **Cron Schedule UTC compensato:** `0 1,2 * * *` in `.github/workflows/seo-builder.yml` con filtro runtime `TZ=Europe/Rome` alle `03:00` per evitare il drift CET/CEST su GitHub Actions.
- **Data Handoff statico:** estrazione dal DB locale SQLite in `data/affiliates_seed.json` committato nel repo pubblico (solo link pubblici e SubID, zero segreti).

<!-- @section:artifacts -->
# Artefatti Principali
- `data/affiliates_seed.json`
- `content/apps/*.md`
- `content/bundles/*.md`
- `.github/workflows/*.yml`
- `scripts/*.py`, `scripts/takedown.sh`
- `src/mcp/server.py`, `src/lib/github-oauth.ts`

<!-- @section:metrics -->
# Metriche
- Target merchant seed: 14
- App di test iniziali: 3 (`losslesscut`, `keepassxc`, `ghost`)
- Soglia scouting: > 500 stelle, `fork:false`
- Soglia troncamento README: 500 righe

<!-- @section:events -->
# Eventi
Tracciamento append-only in `.pcp/context/events.log`.

<!-- @section:policies -->
# Policy di Sicurezza & Conformità
- Local Vault Policy su `.pcp/vault.local.jsonl`
- Nessun binario ospitato su HubHum (solo link diretti ufficiali)
- Rimozione rapida tramite `scripts/takedown.sh <slug>` o workflow `takedown.yml`

<!-- @section:risks -->
# Rischi & Mitigazioni
- Rate limit API AI/GitHub -> Cascata a 3 tier + `data/retry_queue.json` + OAuth utente futuro.
- Link 404 su nuove versioni -> `scripts/link_checker.py` settimanale automatico.
- Drift fuso orario GitHub Actions -> Doppio cron UTC con verifica oraria `Europe/Rome` in bash.

<!-- @section:interfaces -->
# Interfacce
- **MCP JSON-RPC:** `src/mcp/server.py` (`search_human_apps`, `get_human_app`)
- **GitHub Dispatch:** `translate-app` (`repository_dispatch`)
- **CLI Admin:** `scripts/takedown.sh <slug>`

<!-- @section:absorb_archive -->
# Archivio e Assorbimento
Il documento sorgente `HubHum – a Git Hub for Humans.md` è mantenuto nella root come manifesto di riferimento utente; la specifica normalizzata risiede in questa SSOT.

<!-- @section:glossary -->
# Glossario
- **SSOT:** Single Source of Truth (`.pcp/context/ssot.md`)
- **NO-FORK:** divieto di creare fork dei progetti indicizzati
- **Zero Git-Jargon:** divieto di esporre gergo tecnico da sviluppatori nell'interfaccia utente
- **SubID:** identificatore di tracciamento campagna (`hubhum_01_<MER_ID>`)

<!-- @section:changelog -->
# Changelog
- **2026-11-18:** Bootstrap iniziale PCP, Git, Vault, Adapter e implementazione completa HubHum v0.1.0.
