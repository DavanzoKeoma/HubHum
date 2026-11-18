# **HubHum – a Git Hub for Humans**

**Manifesto D.O.E. (Directive Orchestration Execution) unificato per Antigravity IDE/CLI**

Questo documento fonde in un'unica fonte di verità il manifesto D.O.E. (versione italiana e inglese), i dieci workflow operativi e le decisioni prese durante la progettazione. Dove i documenti originali divergevano, la scelta adottata è indicata in modo esplicito.

## **Indice**

1. Scopo e decisioni consolidate  
2. Protocollo di inizializzazione e permessi  
3. Frontend: Astro, UI/UX e deploy  
4. Ecosistema operativo 100% GitHub  
5. Architettura AI a cascata  
6. Dati di affiliazione (Data Handoff)  
7. Prompt di sistema e iniezione contestuale  
8. Pipeline notturna di Programmatic SEO  
9. Workflow operativi (10 scenari)  
10. Traduzione asincrona e Takedown  
11. Predisposizione futura: MCP e GitHub Login  
12. Conformità e brand safety  
13. Punti di attenzione da verificare  
14. Sequenza di esecuzione per l'agente

## **1\. Scopo e decisioni consolidate**

**Scopo.** Tradurre il mondo open-source tecnico in un catalogo accessibile agli utenti comuni (stile "App Store" / "Product Hunt"), monetizzando tramite affiliazioni inserite con logica e contesto dentro le pagine. Il sistema deve funzionare in autonomia, senza server esterni.

**Decisioni consolidate**

| Tema | Decisione |
| :---- | :---- |
| Nome | **HubHum** (sostituisce ogni riferimento al nome provvisorio precedente) |
| Frontend | **Astro**, esportazione puramente statica, Content Collections con validazione Zod |
| Hosting | GitHub Pages (repository pubblico) |
| Database contenuti | File Markdown in /content/apps/ |
| Backend | GitHub Actions (cron \+ dispatch) |
| AI | Cascata a 3 livelli: Google AI Studio → Groq → Mistral. **GitHub Models escluso** perché dismesso il 30 luglio 2026 |
| Affiliazioni | Lette dal database locale affiliatechproject (Desktop) ed esportate in un file JSON leggero dentro il repository |
| Fork | **Vietati** (regola NO-FORK) |
| Disclaimer | Footer: "HubHum is an independent tool and is not affiliated with GitHub, Inc." |

## **2\. Protocollo di inizializzazione e permessi**

**DIRETTIVA PER L'AGENTE ANTIGRAVITY:** comprendi subito lo scopo del progetto (sezione 1). Prima di qualsiasi installazione, chiedi all'utente **in un'unica richiesta** queste autorizzazioni:

1. **Lettura e scrittura sul file system**: per creare/gestire la cartella locale HubHum ed esplorare la directory esterna affiliatechproject sul Desktop.  
2. **Esecuzione di comandi shell**: per inizializzare i progetti, usare Astro CLI e GitHub CLI.  
3. **Accesso alle variabili d'ambiente**: per recuperare le chiavi API in modo sicuro (politica *Zero-Leak*: nessuna chiave nel codice o nei log).

Non creare file né installare nulla finché **tutte e tre** le autorizzazioni non sono state confermate esplicitamente. Poi procedi passo per passo, nell'ordine della sezione 14\.

## **3\. Frontend: Astro, UI/UX e deploy**

Il livello di presentazione è un sito statico (SSG) ultra-veloce basato su Astro.

* **Generazione:** inizializza Astro per l'esportazione puramente statica dei file Markdown tramite Content Collections con validazione Zod rigorosa sul frontmatter (title, slug, tags, is\_webapp).  
* **Deploy (CI/CD):** crea .github/workflows/deploy.yml con i permessi contents: read, pages: write, id-token: write, necessari per l'autenticazione OIDC e il deploy senza password su GitHub Pages.  
* **Schedulazione:** cron notturno alle **03:00** con fuso orario esplicito Europe/Rome, per evitare il drift rispetto all'UTC (vedi sezione 13 per la verifica del parametro).  
* **Vincoli UI/UX (Zero Git-Jargon):** l'interfaccia NON deve sembrare un repository di codice.  
  * Layout minimalista tipo App Store / Product Hunt.  
  * Barra di ricerca centrale ben visibile.  
  * Categorie comprensibili (Produttività, Sicurezza, Grafica, Video…).  
  * Griglia dinamica "Migliori app della settimana".  
  * Mai termini come *commit*, *pull request*, *deploy*, *repository* nel frontend.  
* **Comportamento da tag:** se il frontmatter contiene is\_webapp: true, il template sostituisce il pulsante "Download" con "Lancia nel Cloud" (link affiliato hosting).  
* **Footer globale:** disclaimer di non affiliazione con GitHub, Inc. e informativa sulle affiliazioni (sezione 12).

## **4\. Ecosistema operativo 100% GitHub**

L'agente orchestra esclusivamente la suite ufficiale GitHub (piano Free) per un'infrastruttura coesa, autonoma e a costo zero.

**REGOLA CRITICA – NO FORK:** non fare mai fork dei repository originali, per evitare disordine nell'account e ban delle API.

| Servizio | Ruolo in HubHum |
| :---- | :---- |
| Repositories & Codespaces | Codice sorgente e ambienti cloud isolati |
| API & Webhooks | Scouting notturno via REST/GraphQL (5.000 richieste/ora autenticate); filtro sui tag consumer (windows, macos, utility, video-editor) con **oltre 500 stelle**; escludere le librerie per sviluppatori |
| Actions | Motore backend: esegue gli script che contattano l'AI |
| Releases & Packages | Estrazione dinamica dei link diretti agli eseguibili (.exe, .dmg, .apk) |
| Pages | Front-end pubblico e dominio personalizzato (DNS/CNAME) |
| CLI & Desktop | Gestione programmatica di Git e dei token |
| Git LFS, Gists, Profile README | Asset pesanti, snippet pubblici, vetrina dell'organizzazione |
| Issues, Projects, Dependabot | Trigger asincroni, Kanban, patching di sicurezza automatico |
| Copilot Free | Supporto al debug degli script Python/Node |

## **5\. Architettura AI a cascata**

L'elaborazione testuale usa un motore LLM a 3 livelli per azzerare i blocchi da rate limit.

| Livello | Servizio e modello | Note |
| :---- | :---- | :---- |
| **Tier 1** (primario) | Google AI Studio – gemini-2.5-flash | Contesto da 1 milione di token; \~1.500 richieste/giorno gratuite; assorbe il carico principale |
| **Tier 2** (primo fallback) | Groq Cloud – llama-3.3-70b-versatile | \~1.000 richieste/giorno; inferenza ultra-rapida; interfaccia compatibile OpenAI; output JSON/Markdown strutturato |
| **Tier 3** (rete finale) | Mistral AI – mistral-small-latest | 1 richiesta/secondo, \~1 miliardo di token/mese; ottima fluidità nelle lingue europee |

**Regole di instradamento**

1. Il fallimento di un livello (errore 429, 503, timeout) viene intercettato in millisecondi e il payload passa al livello successivo.  
2. L'output di **qualsiasi** livello viene validato prima del commit: presenza dei titoli obbligatori, frontmatter valido, URL di download identici a quelli di partenza. Se la validazione fallisce, si passa al livello successivo.  
3. Se tutti i livelli falliscono, l'app viene rimessa in coda per la notte successiva (nessun file parziale committato).

## **6\. Dati di affiliazione (Data Handoff)**

**DIRETTIVA PER L'AGENTE:** prima di generare qualsiasi pagina recupera i dati di monetizzazione.

1. Esci dalla cartella del progetto e ispeziona la directory affiliatechproject sul Desktop.  
2. Leggi il database interno (SQLite/JSONL) ed estrai il catalogo dei merchant partner (B2B, SaaS, hosting) con i relativi SubID tracciati e le policy di linking.  
3. Associa i link alle categorie semantiche (mapping sotto).  
4. **Esporta il risultato in un file leggero data/affiliates\_seed.json committato nel repository.** Le GitHub Actions non possono leggere il Desktop dell'utente: devono pescare solo da questo file, ignorando il resto dell'ecosistema locale.  
5. Per la tracciabilità, usa un SubID dedicato per HubHum (es. hubhum\_01\_MER047).

**Mapping categoria → merchant → messaggio**

| Categoria app | Merchant (ID dal database) | Messaggio di iniezione |
| :---- | :---- | :---- |
| Privacy, torrenting, sicurezza | PureVPN (MER\_047), Surfshark (MER\_089), PIA (MER\_048), TorGuard (MER\_064) | "Proteggi la tua connessione prima di scaricare/usare questa app." |
| Web app, CMS, gestionali | InterServer (MER\_008), ScalaHosting (MER\_009), RoseHosting (MER\_014) | "Non vuoi installarlo a mano su un server? Avvialo in 1 click su un hosting ottimizzato." |
| Grafica, video, design | Envato Elements (MER\_349), Creative Fabrica (MER\_054), Placeit (MER\_369) | "Scarica font, template e asset pronti da usare con questo programma." |
| Sviluppo web e WordPress | WP Rocket (MER\_269), Rank Math (MER\_276), Elementor (MER\_265), ThemeIsle (MER\_023) | "Ottimizza o costruisci il tuo sito con gli standard di settore." |

## **7\. Prompt di sistema e iniezione contestuale**

Questo blocco è il prompt di sistema comune a tutti e tre i livelli della cascata. Unifica le regole del manifesto, del prompt di test e dei workflow di brand safety e troncamento.

\[SYSTEM INSTRUCTION FOR AI ROUTER\]  
You are an expert editor translating technical open-source documentation  
for absolute beginners. You receive: (a) the GitHub README, (b) the latest  
"Releases" data with exact file names and URLs, (c) the Affiliate Database  
mapping for this app's category. Write in Italian.

STRICT RULES:  
1\. HUMAN TRANSLATION: no technical jargon (avoid "repository", "framework",  
   "deploy", "API", "build"). Explain the real-life problem the app solves  
   in exactly 3 simple sentences.  
2\. LINK INTEGRITY: NEVER invent URLs. Use only URLs present in the README  
   or in the Releases data. Present download links with clear names, e.g.  
   \[Scarica per Windows (.exe)\](ORIGINAL\_URL), but NEVER alter or shorten  
   the underlying URL. Ignore technical badges, source archives (.zip,  
   .tar.gz) and terminal commands, unless no other alternative exists.  
3\. AFFILIATE INJECTION: based on the app's category, naturally weave in a  
   recommendation for a related service from the Affiliate Database  
   mapping, more than once if it fits the text. It must read as valuable  
   advice, not spam. Use only links from the provided mapping.  
   Example (web CMS): "Non vuoi installarlo a mano? Avvialo in 1 click su  
   \[Hosting Link\]."  
4\. WEB APPS: if the project is a web application and not a downloadable  
   program, set is\_webapp: true and mention one-click hosting.  
5\. BRAND SAFETY: never reproduce third-party trademarks in comparative or  
   "killer of X" slogans; replace them with generic terms (e.g. "software  
   di design proprietari"). No trademark bidding.  
6\. CREDITS: always end with a discreet link "Fonte ufficiale / Crediti"  
   pointing to the original GitHub repository.

REQUIRED MARKDOWN STRUCTURE (exact headings):  
\---  
title: "{App Name}"  
slug: "{app-slug}"  
tags: \["{tag1}", "{tag2}"\]  
is\_webapp: {true/false}  
\---  
\#\#\# Cos'è in parole semplici  
{3 sentences}  
\#\#\# A chi è utile  
{2-3 practical user profiles}  
\#\#\# Cosa puoi farci  
{4-5 concrete features in bullet points}  
\#\#\# Come si installa (Download)  
{direct links to executables, or official site URL for web apps}  
\#\#\# Pro e Contro  
\* \*\*Pro:\*\* {e.g. gratis, senza abbonamenti}  
\* \*\*Contro:\*\* {e.g. solo in inglese}  
\[Fonte ufficiale / Crediti\]  
**Nota sulla lingua:** i titoli sezione sono in italiano perché il sito è destinato al pubblico italiano. Per una versione inglese basta cambiare la lingua di output e i titoli nel prompt e nello schema Zod.

## **8\. Pipeline notturna di Programmatic SEO**

È il cuore del sistema: invece di generare pagine al momento della ricerca (sito vuoto, niente indicizzazione, consumo di token), le pagine vengono create in anticipo.

1. **Innesco:** GitHub Actions cron alle 03:00 (Europe/Rome).  
2. **Scouting:** interroga la GitHub API per i 10–20 repository con più stelle guadagnate nelle ultime 24 ore, filtrando per tag consumer e soglia \> 500 stelle.  
3. **Estrazione:** scarica il README e l'endpoint /releases/latest per nomi e link esatti degli eseguibili.  
4. **Controllo dimensione:** se il README supera la soglia di sicurezza, troncamento intelligente alle prime 500 righe (descrizione e funzionalità).  
5. **Generazione:** invio alla cascata AI (sezione 5\) con il prompt della sezione 7 e il mapping affiliato.  
6. **Validazione e sanitizzazione:** struttura, URL, termini di marchio (sezione 12).  
7. **Salvataggio:** scrittura in content/apps/nome-app.md, commit e push automatico.  
8. **Build e pubblicazione:** il push innesca Astro e il deploy su GitHub Pages.

**Risultato:** al risveglio il sito ha circa 15 nuove landing page indicizzabili. I visitatori navigano HTML statico e non consumano mai i limiti API.

## **9\. Workflow operativi**

### **Workflow comuni (automazione quotidiana)**

**1\. Ciclo notturno di scouting e pubblicazione.** Descritto nella sezione 8\. Esempio: un tool di editing video viene riconosciuto e riceve automaticamente il link Envato Elements con suggerimento di template.

**2\. Rotazione e aggiornamento dei link affiliati.**

* *Innesco:* modifica al database Master locale (affiliatechproject).  
* *Processo:* tramite Antigravity CLI si rigenera e si invia data/affiliates\_seed.json al repository; una Action rileva la modifica ed esegue un "trova e sostituisci" contestuale su tutti i .md (es. vecchio SubID PureVPN → nuovo SubID della campagna), poi build Astro.  
* *Risultato:* l'intera piattaforma aggiorna i link retroattivamente in circa 2 minuti, senza rigenerare i testi con l'AI.

**3\. Web-app e "1-Click Hosting".**

* *Innesco:* l'AI nota che il repository è un CMS o un gestionale (es. Ghost, Odoo), non un eseguibile.  
* *Processo:* aggiunge is\_webapp: true, inietta il consiglio di hosting in 1 click (InterServer/ScalaHosting); Astro legge il tag e sostituisce il pulsante "Download" con "Lancia nel Cloud".  
* *Risultato:* monetizzazione mirata degli utenti non tecnici che cercano alternative gratuite ai SaaS.

**4\. Patching di sicurezza (Dependabot).**

* *Innesco:* vulnerabilità in una libreria npm usata da Astro.  
* *Processo:* Dependabot apre una Pull Request; le Actions eseguono la build in un container isolato; se la build statica riesce, la PR viene unita (anche in auto-merge).  
* *Risultato:* frontend sicuro e aggiornato senza intervento manuale.

### **Workflow non comuni (edge case e resilienza)**

**5\. Cascade Routing in azione.** Se Google restituisce 429/503, lo script scarta Gemini, passa a Groq, poi a Mistral; l'output viene validato prima del commit. La catena SEO non si interrompe.

**6\. Link di release rotto e auto-correzione.** Uno script settimanale verifica tutti gli URL di download nei .md; su un 404 interroga di nuovo la GitHub API per il nuovo link, aggiorna il file e fa un commit correttivo. Meno link rotti, meno bounce rate.

**7\. Raccolte automatiche (Bundle Pages).** Quando un tag (es. video-editor) raggiunge 50 app, uno script mensile fa generare dall'AI un articolo riassuntivo ("Le 5 migliori alternative gratuite a Premiere Pro") basato sulle schede già prodotte, con banner affiliati incrociati e collegamenti alle singole schede.

**8\. README eccessivamente grande.** Controllo preventivo della lunghezza; sopra soglia, troncamento alle prime 500 righe e scheda semplificata basata sull'abstract.

**9\. Termini vietati (brand safety).** Se un README si presenta come "il killer di \[Marchio\]", il prompt e uno script di sanitizzazione post-generazione sostituiscono il marchio con un termine generico, nel rispetto delle policy dei merchant e della normativa sulla pubblicità.

**10\. Richiesta di rimozione (DMCA).** Vedi sezione 10\.

## **10\. Traduzione asincrona e Takedown**

**Traduzione di un'app via URL GitHub**

* La casella "Traduci un'app da un link GitHub" non elabora nulla in locale: invia un payload a un webhook repository\_dispatch (oppure apre una Issue automatica silenziosa). Questo evita abusi delle API e carico sul backend.  
* *UX:* l'utente vede "L'app è in traduzione. Sarà online tra circa 2 minuti."  
* *Backend:* la Action si attiva, esegue la cascata AI, committa il nuovo .md e avvia la build Astro.

**Richieste di rimozione (DMCA / conformità)**

* Script /scripts/takedown.sh \<slug-app\> lanciabile dall'amministratore (o da Antigravity) in Codespaces, oppure attivato da una Issue con tag dedicato.  
* Lo script elimina il .md, fa commit "Remove: \[slug-app\] per compliance", fa purgare la pagina dalla build Astro e aggiorna i metadati del sito.  
* *Risultato:* rimozione in meno di 60 secondi.

## **11\. Predisposizione futura: MCP e GitHub Login**

* **MCP (Model Context Protocol):** struttura gli script Python/Node in moduli, in modo che HubHum possa essere esposto come server MCP e interrogato da agenti AI esterni (es. search\_human\_apps(query)) via JSON-RPC.  
* **GitHub Login (OAuth):** prepara l'architettura Astro ad accettare il login GitHub. Oggi il sito è statico, ma questo abilita "Salva nei preferiti", "Lascia una recensione" e permette di instradare le ricerche con il token dell'utente, scaricando i limiti di frequenza dai token principali di HubHum.

## **12\. Conformità e brand safety**

* **Disclaimer:** footer "HubHum is an independent tool and is not affiliated with GitHub, Inc."  
* **Crediti:** ogni scheda rimanda alla fonte originale.  
* **Marchi:** nessun uso comparativo o di bidding su marchi registrati; sanitizzazione automatica.  
* **Trasparenza sulle affiliazioni:** aggiungere in ogni pagina e nel footer una dicitura chiara (es. "Alcuni link sono di affiliazione: se acquisti tramite questi link potremmo ricevere una commissione, senza costi aggiuntivi per te"). Integrazione consigliata: richiesta dalle norme FTC e dai termini dei network di affiliazione, e coerente con le policy dei merchant già validate nel database Master.  
* **Licenze:** verificare che la licenza del progetto originale consenta la redistribuzione dei link e delle descrizioni; mai ospitare i binari altrui, solo linkare.  
* **Takedown:** procedura documentata nella sezione 10\.  
* **Sicurezza:** chiavi solo in variabili d'ambiente/Secrets, mai nel repository.

## **13\. Punti di attenzione da verificare**

Questi punti emergono dal confronto dei documenti e vanno controllati durante l'esecuzione:

1. **Parametro timezone nel cron.** Verifica nella documentazione ufficiale di GitHub Actions che la chiave timezone sia supportata per il trigger schedule. In caso contrario, imposta il cron in UTC e compensa l'ora legale/solare.  
2. **Limiti dei piani gratuiti.** Le quote indicate (Gemini \~1.500/giorno, Groq \~1.000/giorno, Mistral) sono quelle dichiarate nei documenti sorgente: confermale sulle pagine ufficiali prima della messa a regime, perché cambiano spesso.  
3. **Repository pubblico.** GitHub Pages richiede un repository pubblico sul piano Free: il file affiliates\_seed.json sarà quindi visibile a chiunque. Contiene link e SubID di tracciamento, non segreti; tienilo separato da qualsiasi chiave o dato sensibile.  
4. **Conflitto risolto sui dati affiliati.** Il manifesto chiedeva all'agente di leggere il database sul Desktop, mentre l'idea di isolamento voleva le Action autonome. La soluzione adottata (sezione 6\) li concilia: lettura locale una tantum, esportazione in JSON, uso del JSON da parte delle Action.  
5. **Soglia \> 500 stelle e tag.** Rivedila dopo i primi cicli: se i risultati sono pochi, abbassa la soglia o amplia i tag.  
6. **Auto-merge Dependabot.** Abilitalo solo se la build statica è l'unico controllo; valuta una revisione manuale per gli aggiornamenti maggiori.

## **14\. Sequenza di esecuzione per l'agente**

1. Richiedi le tre autorizzazioni in un'unica richiesta e attendi la conferma (sezione 2).  
2. Crea la struttura del progetto HubHum e inizializza il repository Git (senza fork).  
3. Ispeziona affiliatechproject, estrai i merchant e genera data/affiliates\_seed.json (sezione 6).  
4. Inizializza Astro con Content Collections e schema Zod; costruisci l'interfaccia secondo i vincoli Zero Git-Jargon (sezione 3).  
5. Configura deploy.yml con permessi OIDC e GitHub Pages; collega il dominio personalizzato se disponibile.  
6. Implementa lo script di scouting, l'estrazione README/Releases e il troncamento (sezione 8).  
7. Implementa il router AI a 3 livelli con validazione dell'output (sezione 5\) e il prompt di sistema (sezione 7).  
8. Aggiungi la sanitizzazione dei marchi e la dicitura di affiliazione (sezione 12).  
9. Crea il workflow notturno seo-builder.yml con cron 03:00 Europe/Rome e commit automatico dei nuovi .md.  
10. Aggiungi i workflow di manutenzione: controllo link settimanale, raccolte mensili, sincronizzazione affiliati, Dependabot (sezione 9).  
11. Implementa la traduzione asincrona via repository\_dispatch e lo script takedown.sh (sezione 10).  
12. Struttura i moduli per MCP e prepara l'architettura OAuth (sezione 11).  
13. Esegui un test completo con 2–3 app reali, verifica pagine, link e build, poi attiva il cron.

*HubHum is an independent tool and is not affiliated with GitHub, Inc.*