export type SupportedLang = 'en' | 'it' | 'es' | 'fr' | 'de';

export const SUPPORTED_LANGS: SupportedLang[] = ['en', 'it', 'es', 'fr', 'de'];

export function formatCompactStars(stars: number): string {
  if (stars >= 1000) {
    const val = stars / 1000;
    return `★ ${val >= 100 ? Math.round(val) : val.toFixed(1).replace(/\.0$/, '')}k GitHub`;
  }
  return `★ ${stars.toLocaleString('en')} GitHub`;
}

export interface TranslationDict {
  brandSub: string;
  navGuides: string;
  navTopPicks: string;
  navSubmit: string;
  navSignIn: string;
  navFavorites: string;
  themeToggleAria: string;
  eyebrow: string;
  heroTitle: string;
  heroSubtitle: string;
  searchPlaceholder: string;
  searchAriaLabel: string;
  categoriesLabel: string;
  catAll: string;
  catProductivity: string;
  catSecurity: string;
  catGraphics: string;
  catVideo: string;
  catWebApps: string;
  catUtilities: string;
  catWebsites: string;
  liveSearchEyebrow: string;
  liveSearchPlaceholder: string;
  liveSearchAria: string;
  liveSearchLoading: string;
  liveSearchEmpty: string;
  liveSearchRateLimit: string;
  liveSearchRateHint: string;
  btnAlreadyOnHubHum: string;
  btnGoWithHubHum: string;
  convTitle: string;
  convStep1: string;
  convStep2: string;
  convStep3: string;
  convStep4: string;
  convDone: string;
  convPollingHint: string;
  convErrorMsg: string;
  convTimeoutMsg: string;
  convRetryBtn: string;
  topPicksHeading: string;
  topPicksSub: string;
  allSoftwareHeading: string;
  appsAvailableSuffix: string;
  emptySearch: string;
  pagePrev: string;
  pageNext: string;
  loadMoreBtn: string;
  pageLabel: string;
  ofLabel: string;
  guidesHeading: string;
  guidesSub: string;
  guideReadMore: string;
  guideAppsIncluded: string;
  guidesAllCta: string;
  badgeCloud: string;
  badgeSelfHosted: string;
  badgeDesktop: string;
  badgeCli: string;
  badgeResource: string;
  badgeNew: string;
  starsSuffix: string;
  chosenByPrefix: string;
  chosenBySuffix: string;
  ctaDesktop: string;
  ctaCloud: string;
  ctaSelfHosted: string;
  ctaCli: string;
  ctaResource: string;
  cliWarningTitle: string;
  cliWarningBody: string;
  selfHostedWarningTitle: string;
  selfHostedWarningBody: string;
  jumpLiveSearch: string;
  submitTitle: string;
  submitDesc: string;
  submitPlaceholder: string;
  submitBtn: string;
  submitSuccess: string;
  submitInvalidUrl: string;
  backAllApps: string;
  saveFavorite: string;
  savedFavorite: string;
  partnerTipBadge: string;
  partnerHeadingPrefix: string;
  partnerFallbackHeading: string;
  partnerFallbackDesc: string;
  partnerCloudBtn: string;
  partnerDiscoverPrefix: string;
  detailsHeading: string;
  detailCategory: string;
  detailMode: string;
  detailModeCloud: string;
  detailModeSelfHosted: string;
  detailModeDesktop: string;
  detailModeCli: string;
  detailModeResource: string;
  detailLicense: string;
  detailOfficialPage: string;
  detailOpenSource: string;
  clusterSidebarHeading: string;
  clusterPillarLabel: string;
  clusterSubpillarLabel: string;
  clusterComparisonLabel: string;
  relatedGuidesHeading: string;
  reviewTitlePrefix: string;
  reviewDesc: string;
  reviewBtn: string;
  disclosureTitle: string;
  disclosureBody: string;
  footerDisclaimer: string;
  footerAffiliate: string;
  footerCredits: string;
  aboutLink: string;
  privacyLink: string;
  dashboardLink: string;
  sitemapLink: string;
  dialogTitle: string;
  dialogDescLocal: string;
  dialogDescAuth: string;
  dialogNoFavs: string;
  dialogClose: string;
  dialogLogout: string;
  detailSummaryNotice: string;
  oauthSignInBtn: string;
  oauthSignInDesc: string;
  oauthConnecting: string;
  filterFormatLabel: string;
  filterFormatAll: string;
  filterFormatDesktop: string;
  filterFormatSelfHosted: string;
  filterFormatCli: string;
  filterOsLabel: string;
  filterOsAll: string;
  filterOsBrowser: string;
  secWhatItDoes: string;
  secWhoItsFor: string;
  secKeyFeatures: string;
  secHowToInstall: string;
  secProsAndCons: string;
  secSponsoredTools: string;
  secSponsoredNote: string;
  secOfficialSource: string;
  labelPros: string;
  labelCons: string;
  guideLevelPillar: string;
  guideLevelSubpillar: string;
  guideLevelComparison: string;
  guideLevelFoundations: string;
  guideLevelTroubleshooting: string;
  guideSubpillarsHeading: string;
  guideArticlesHeading: string;
  guideGuidesSub: string;
  guideFeaturedAppsHeading: string;
  guideFeaturedAppsSub: string;
  guideToolsCoveredSuffix: string;
}

export const TRANSLATIONS: Record<SupportedLang, TranslationDict> = {
  en: {
    brandSub: 'Free software for humans',
    navGuides: 'Topic Guides',
    navTopPicks: 'Top Picks',
    navSubmit: 'Submit an App',
    navSignIn: 'Sign In',
    navFavorites: 'Favorites',
    themeToggleAria: 'Toggle light and dark theme',
    eyebrow: 'Hand-picked selection of the best free software',
    heroTitle: 'Powerful free software, zero tech jargon',
    heroSubtitle:
      'No complicated terms. Find out what each program really does and download the official version right away.',
    searchPlaceholder: 'Search by name or task (e.g., video, passwords...)',
    searchAriaLabel: 'Search software catalog',
    categoriesLabel: 'Filter by category',
    catAll: 'All',
    catProductivity: 'Productivity',
    catSecurity: 'Security & Privacy',
    catGraphics: 'Graphics & Design',
    catVideo: 'Video & Audio',
    catWebApps: 'Web Apps & Cloud',
    catUtilities: 'Utilities & Power Tools',
    catWebsites: 'Websites & SEO',
    liveSearchEyebrow: "Can't find your favorite open-source app?",
    liveSearchPlaceholder: 'Search 800M+ open-source projects on GitHub...',
    liveSearchAria: 'Search open-source projects live on GitHub',
    liveSearchLoading: 'Searching open-source index...',
    liveSearchEmpty: 'No matching projects found. Try a broader name or keyword.',
    liveSearchRateLimit: 'You made several fast searches. Wait a few seconds or paste the project URL below.',
    liveSearchRateHint: 'Paste URL directly below',
    btnAlreadyOnHubHum: 'Already on HubHum →',
    btnGoWithHubHum: 'Go with HubHum ⚡',
    convTitle: 'Translating App Guide',
    convStep1: 'Fetching information from GitHub...',
    convStep2: 'Creating plain-English guide with AI...',
    convStep3: 'Checking official download links...',
    convStep4: 'Publishing guide to HubHum catalog...',
    convDone: 'Done! Redirecting to your new guide...',
    convPollingHint: 'Usually ready in 35–60 seconds. Checking catalog automatically...',
    convErrorMsg: 'Could not start the conversion right now. Please try again in a moment.',
    convTimeoutMsg: 'Publishing is taking slightly longer than usual. Click Retry to keep checking or reopen shortly.',
    convRetryBtn: 'Try Again',
    topPicksHeading: 'Top Picks This Week',
    topPicksSub: 'Most starred open-source software in the catalog',
    allSoftwareHeading: 'All Software',
    appsAvailableSuffix: 'apps available',
    emptySearch: 'No apps match your search. Try another keyword or submit a link below.',
    pagePrev: 'Previous',
    pageNext: 'Next',
    loadMoreBtn: 'Load 24 more',
    pageLabel: 'Page',
    ofLabel: 'of',
    guidesHeading: 'Topic Guides & Comparisons',
    guidesSub: 'Practical buyer guides, alternatives, and troubleshooting organized by topic',
    guideReadMore: 'Explore guide →',
    guideAppsIncluded: 'apps covered',
    guidesAllCta: 'Browse all Topic Guides →',
    badgeCloud: 'Cloud Web App',
    badgeSelfHosted: 'Self-Hosted App',
    badgeDesktop: 'Desktop App',
    badgeCli: 'CLI Tool',
    badgeResource: 'Open Reference',
    badgeNew: 'New',
    starsSuffix: 'stars on GitHub',
    chosenByPrefix: '★',
    chosenBySuffix: 'stars on GitHub',
    ctaDesktop: 'Explore & Download →',
    ctaCloud: 'Open in Cloud →',
    ctaSelfHosted: 'Setup & Docs →',
    ctaCli: 'Get CLI Tool →',
    ctaResource: 'Browse Guide →',
    cliWarningTitle: 'Command-Line (Terminal) Tool:',
    cliWarningBody:
      'This program runs via typed text commands in Windows Terminal, PowerShell, or macOS/Linux Terminal rather than a visual point-and-click window. If you prefer graphical buttons, check alternative Desktop Apps in the Topic Cluster sidebar.',
    selfHostedWarningTitle: 'Self-Hosted Software:',
    selfHostedWarningBody:
      'Designed to be installed on your own computer, local network, or private cloud server (not a hosted public website). Click Official Setup & Docs for installation steps.',
    jumpLiveSearch: "Looking for an unindexed GitHub project? Search 800M+ repositories below ↓",
    submitTitle: 'Submit an App',
    submitDesc: 'Paste any GitHub URL to add a plain-English guide to HubHum',
    submitPlaceholder: 'https://github.com/author/app-name',
    submitBtn: 'Submit App',
    submitSuccess: 'Your app is being processed and will be live shortly.',
    submitInvalidUrl: 'Please enter a valid URL formatted as https://github.com/author/app-name.',
    backAllApps: '← Back to all software',
    saveFavorite: 'Save to Favorites',
    savedFavorite: 'Saved in Favorites',
    partnerTipBadge: 'Sponsored Partner (#ad)',
    partnerHeadingPrefix: 'Partner Service:',
    partnerFallbackHeading: 'Enhance your setup',
    partnerFallbackDesc: 'Optional commercial partner solution.',
    partnerCloudBtn: 'Launch on Cloud Host (#ad)',
    partnerDiscoverPrefix: 'Explore',
    detailsHeading: 'Quick Specs',
    detailCategory: 'Category:',
    detailMode: 'Format:',
    detailModeCloud: 'Runs in your browser / cloud',
    detailModeSelfHosted: 'Runs on your own server or PC (Self-Hosted)',
    detailModeDesktop: 'Desktop GUI installer',
    detailModeCli: 'Command-line / terminal tool',
    detailModeResource: 'Curated reference list or guide',
    detailLicense: 'License:',
    detailOfficialPage: 'Official Source:',
    detailOpenSource: 'Visit GitHub source',
    clusterSidebarHeading: 'Topic Cluster Guides',
    clusterPillarLabel: 'Main Category Guide:',
    clusterSubpillarLabel: 'Focus Topic Hub:',
    clusterComparisonLabel: 'Compare Top Alternatives →',
    relatedGuidesHeading: 'Related Guides in This Topic',
    reviewTitlePrefix: 'Have you tried',
    reviewDesc: 'Help everyday users decide by sharing a quick review.',
    reviewBtn: 'Write a review',
    disclosureTitle: 'Affiliate transparency (#ad):',
    disclosureBody:
      'Some links inside Sponsored Partner Tools (#ad) and the sidebar partner box are affiliate links. If you choose to activate a service through them, we may earn a commission at no extra cost to you.',
    footerDisclaimer: 'HubHum is an independent directory and is not affiliated with GitHub, Inc.',
    footerAffiliate:
      'Affiliate transparency (#ad): HubHum displays affiliate links exclusively in clearly marked Sponsored Partner sections. Software choices and GitHub star counts are never paid placements.',
    footerCredits:
      'All listed software links strictly to official creator channels in full respect of open-source licenses.',
    aboutLink: 'About & Transparency',
    privacyLink: 'Privacy Policy',
    dashboardLink: 'Dashboard',
    sitemapLink: 'Sitemap',
    dialogTitle: 'Your Saved Favorites',
    dialogDescLocal: 'Your favorite apps are saved right here in this browser.',
    dialogDescAuth: 'Signed in with GitHub. Manage your saved favorites below.',
    dialogNoFavs: 'You have not saved any favorite apps yet. Click the heart button on any app page!',
    dialogClose: 'Close',
    dialogLogout: 'Sign Out',
    detailSummaryNotice: 'Plain-language summary in your language:',
    oauthSignInBtn: 'Sign in with GitHub',
    oauthSignInDesc: 'Sign in with one click to link your GitHub profile and sync favorites.',
    oauthConnecting: 'Connecting your GitHub account...',
    filterFormatLabel: 'Filter by format',
    filterFormatAll: 'All Formats',
    filterFormatDesktop: 'Desktop Apps (GUI)',
    filterFormatSelfHosted: 'Self-Hosted Apps',
    filterFormatCli: 'Developer / CLI Tools',
    filterOsLabel: 'Filter by operating system',
    filterOsAll: 'All Systems',
    filterOsBrowser: 'Browser / Cloud',
    secWhatItDoes: 'What it does in plain English',
    secWhoItsFor: "Who it's for",
    secKeyFeatures: 'Key features',
    secHowToInstall: 'How to install (Download)',
    secProsAndCons: 'Pros and Cons',
    secSponsoredTools: 'Sponsored Partner Tools (#ad)',
    secSponsoredNote:
      'Optional commercial services unrelated to the open-source developer. Clicking an #ad link helps fund HubHum at no extra cost to you.',
    secOfficialSource: 'Official Source & Credits:',
    labelPros: 'Pros',
    labelCons: 'Cons',
    guideLevelPillar: 'Main Category Guide',
    guideLevelSubpillar: 'Focus Topic Hub',
    guideLevelComparison: 'Comparison Guide',
    guideLevelFoundations: 'Beginner Foundations',
    guideLevelTroubleshooting: 'Troubleshooting Guide',
    guideSubpillarsHeading: 'Focus Topics in This Category',
    guideArticlesHeading: 'Practical Guides & Comparisons',
    guideGuidesSub: 'Choose a guide below to compare options and find step-by-step advice',
    guideFeaturedAppsHeading: 'Verified Free Software Featured in This Guide',
    guideFeaturedAppsSub: 'Click any tool to open its plain-English sheet and official download links',
    guideToolsCoveredSuffix: 'tools covered',
  },
  it: {
    brandSub: 'App libere per tutti',
    navGuides: 'Guide Tematiche',
    navTopPicks: 'Top della settimana',
    navSubmit: "Proponi un'app",
    navSignIn: 'Accedi',
    navFavorites: 'Preferiti',
    themeToggleAria: 'Cambia tema chiaro o scuro',
    eyebrow: 'La selezione curata a mano dei migliori software gratuiti',
    heroTitle: 'Programmi gratuiti e potenti, senza gergo tecnico',
    heroSubtitle:
      'Niente termini complicati. Scopri a cosa serve davvero ogni programma e scarica subito la versione ufficiale.',
    searchPlaceholder: 'Cerca per nome o scopo (es. video, password...)',
    searchAriaLabel: 'Cerca nel catalogo applicazioni',
    categoriesLabel: 'Filtra per categoria',
    catAll: 'Tutte',
    catProductivity: 'Produttività',
    catSecurity: 'Sicurezza & Privacy',
    catGraphics: 'Grafica & Design',
    catVideo: 'Video & Audio',
    catWebApps: 'Web App & Cloud',
    catUtilities: 'Utilità & Power Tools',
    catWebsites: 'Siti Web & SEO',
    liveSearchEyebrow: 'Non trovi il tuo programma open-source preferito?',
    liveSearchPlaceholder: 'Cerca tra milioni di progetti open-source su GitHub...',
    liveSearchAria: 'Cerca progetti open-source in tempo reale su GitHub',
    liveSearchLoading: 'Ricerca in corso tra i progetti open-source...',
    liveSearchEmpty: 'Nessun progetto trovato. Prova un nome più semplice o un altro termine.',
    liveSearchRateLimit: 'Hai fatto troppe ricerche veloci. Attendi qualche secondo o incolla direttamente l’URL qui sotto.',
    liveSearchRateHint: 'Incolla l’URL qui sotto',
    btnAlreadyOnHubHum: 'Già disponibile →',
    btnGoWithHubHum: 'Traduci con HubHum ⚡',
    convTitle: 'Creazione guida in corso',
    convStep1: 'Recupero informazioni da GitHub...',
    convStep2: 'Elaborazione guida semplice con IA...',
    convStep3: 'Verifica dei link ufficiali di download...',
    convStep4: 'Pubblicazione scheda nel catalogo...',
    convDone: 'Fatto! Reindirizzamento alla nuova guida...',
    convPollingHint: 'Di solito è pronta in 35–60 secondi. Controllo automatico attivo...',
    convErrorMsg: 'Impossibile avviare la traduzione in questo momento. Riprova tra poco.',
    convTimeoutMsg: 'La pubblicazione sta richiedendo qualche secondo in più. Premi Riprova per continuare il controllo.',
    convRetryBtn: 'Riprova',
    topPicksHeading: 'Migliori della Settimana',
    topPicksSub: 'I software con più stelle su GitHub nel catalogo',
    allSoftwareHeading: 'Tutto il Catalogo',
    appsAvailableSuffix: 'app disponibili',
    emptySearch: "Nessuna app corrisponde alla ricerca. Prova un'altra parola o proponi un link qui sotto.",
    pagePrev: 'Precedente',
    pageNext: 'Successiva',
    loadMoreBtn: 'Carica altre 24',
    pageLabel: 'Pagina',
    ofLabel: 'di',
    guidesHeading: 'Guide Tematiche & Confronti',
    guidesSub: 'Guide pratiche, confronti tra alternative e soluzioni ai problemi più comuni',
    guideReadMore: 'Apri guida →',
    guideAppsIncluded: 'app analizzate',
    guidesAllCta: 'Esplora tutte le Guide →',
    badgeCloud: 'Web App Cloud',
    badgeSelfHosted: 'App Self-Hosted',
    badgeDesktop: 'App Desktop',
    badgeCli: 'Strumento CLI',
    badgeResource: 'Guida & Risorsa',
    badgeNew: 'Novità',
    starsSuffix: 'stelle su GitHub',
    chosenByPrefix: '★',
    chosenBySuffix: 'stelle su GitHub',
    ctaDesktop: 'Scopri & Scarica →',
    ctaCloud: 'Apri nel Cloud →',
    ctaSelfHosted: 'Guida & Setup →',
    ctaCli: 'Scopri Strumento CLI →',
    ctaResource: 'Apri Risorsa →',
    cliWarningTitle: 'Strumento da Terminale (CLI):',
    cliWarningBody:
      'Questo programma si usa digitando comandi nel Terminale (Prompt dei comandi, PowerShell o Terminale Mac/Linux), senza finestra grafica con pulsanti. Se cerchi un programma visivo, esplora le alternative Desktop nella barra laterale.',
    selfHostedWarningTitle: 'Applicazione Self-Hosted:',
    selfHostedWarningBody:
      'Pensata per essere installata sul tuo PC, rete locale o server privato (non è un sito pubblico già pronto). Apri la documentazione ufficiale per installarla.',
    jumpLiveSearch: 'Non trovi un progetto? Cerca su tutto GitHub più in basso ↓',
    submitTitle: "Proponi un'app",
    submitDesc: 'Incolla un link GitHub per aggiungere una guida chiara su HubHum',
    submitPlaceholder: 'https://github.com/autore/nome-app',
    submitBtn: 'Invia app',
    submitSuccess: "L'app è in elaborazione e sarà online tra poco.",
    submitInvalidUrl: 'Inserisci un indirizzo valido nel formato https://github.com/autore/nome-app.',
    backAllApps: '← Torna a tutte le app',
    saveFavorite: 'Salva nei preferiti',
    savedFavorite: 'Salvata nei preferiti',
    partnerTipBadge: 'Partner Sponsorizzato (#ad)',
    partnerHeadingPrefix: 'Servizio Partner:',
    partnerFallbackHeading: 'Migliora la tua esperienza',
    partnerFallbackDesc: 'Soluzione commerciale opzionale.',
    partnerCloudBtn: 'Avvia su Hosting Cloud (#ad)',
    partnerDiscoverPrefix: 'Scopri',
    detailsHeading: 'Dettagli rapidi',
    detailCategory: 'Categoria:',
    detailMode: 'Modalità:',
    detailModeCloud: 'Applicazione web nel cloud',
    detailModeSelfHosted: 'Installabile sul tuo server o PC (Self-Hosted)',
    detailModeDesktop: 'App desktop con installazione',
    detailModeCli: 'Strumento da riga di comando (CLI)',
    detailModeResource: 'Lista curata o risorsa informativa',
    detailLicense: 'Licenza:',
    detailOfficialPage: 'Fonte Ufficiale:',
    detailOpenSource: 'Apri sorgente GitHub',
    clusterSidebarHeading: 'Guide del Topic Cluster',
    clusterPillarLabel: 'Guida Principale:',
    clusterSubpillarLabel: 'Sotto-categoria:',
    clusterComparisonLabel: 'Confronta le alternative →',
    relatedGuidesHeading: 'Guide Correlate in Questo Tema',
    reviewTitlePrefix: 'Hai provato',
    reviewDesc: 'Aiuta altri utenti a scegliere lasciando un parere veloce.',
    reviewBtn: 'Lascia una recensione',
    disclosureTitle: 'Trasparenza affiliazioni (#ad):',
    disclosureBody:
      'I link nella sezione Sponsored Partner Tools (#ad) e nel riquadro laterale sono link di affiliazione: se attivi un servizio potremmo ricevere una commissione senza costi aggiuntivi.',
    footerDisclaimer: 'HubHum è un catalogo indipendente e non è affiliato con GitHub, Inc.',
    footerAffiliate:
      'Trasparenza affiliazioni (#ad): I link sponsorizzati sono confinati nelle aree dedicate (#ad). La selezione dei software e le stelle GitHub non sono mai a pagamento.',
    footerCredits:
      'Tutti i software rimandano esclusivamente ai canali ufficiali dei rispettivi autori nel rispetto delle licenze open-source.',
    aboutLink: 'Chi Siamo & Trasparenza',
    privacyLink: 'Privacy Policy',
    dashboardLink: 'Dashboard',
    sitemapLink: 'Mappa del sito',
    dialogTitle: 'I tuoi Preferiti',
    dialogDescLocal: 'Le tue app preferite sono salvate qui nel tuo browser.',
    dialogDescAuth: 'Accesso effettuato con GitHub. Gestisci i tuoi preferiti qui sotto.',
    dialogNoFavs: 'Non hai ancora salvato nessuna app. Premi il cuore su una qualsiasi scheda!',
    dialogClose: 'Chiudi',
    dialogLogout: 'Esci',
    detailSummaryNotice: 'Sintesi chiara nella tua lingua:',
    oauthSignInBtn: 'Accedi con GitHub',
    oauthSignInDesc: 'Accedi in 1 click per collegare il tuo profilo GitHub ai tuoi preferiti.',
    oauthConnecting: 'Collegamento account GitHub in corso...',
    filterFormatLabel: 'Filtra per formato',
    filterFormatAll: 'Tutti i Formati',
    filterFormatDesktop: 'App Desktop (GUI)',
    filterFormatSelfHosted: 'App Self-Hosted',
    filterFormatCli: 'Strumenti per Sviluppatori / CLI',
    filterOsLabel: 'Filtra per sistema operativo',
    filterOsAll: 'Tutti i Sistemi',
    filterOsBrowser: 'Browser / Cloud',
    secWhatItDoes: 'Cosa fa in parole semplici',
    secWhoItsFor: 'A chi è utile',
    secKeyFeatures: 'Funzionalità principali',
    secHowToInstall: 'Come installarlo (Download ufficiale)',
    secProsAndCons: 'Pro e Contro',
    secSponsoredTools: 'Strumenti Partner Sponsorizzati (#ad)',
    secSponsoredNote:
      'Servizi commerciali opzionali non affiliati allo sviluppatore open-source. I link #ad aiutano a sostenere HubHum senza costi extra.',
    secOfficialSource: 'Fonte Ufficiale e Crediti:',
    labelPros: 'Pro',
    labelCons: 'Contro',
    guideLevelPillar: 'Guida Principale di Categoria',
    guideLevelSubpillar: 'Focus Tematico',
    guideLevelComparison: 'Guida Comparativa',
    guideLevelFoundations: 'Guida per Principianti',
    guideLevelTroubleshooting: 'Risoluzione Problemi',
    guideSubpillarsHeading: 'Argomenti in Questa Categoria',
    guideArticlesHeading: 'Guide Pratiche e Confronti',
    guideGuidesSub: 'Scegli una guida qui sotto per confrontare le alternative passo dopo passo',
    guideFeaturedAppsHeading: 'Software Gratuiti Verificati in Questa Guida',
    guideFeaturedAppsSub: 'Apri qualsiasi scheda per leggere la guida semplice e scaricare dai canali ufficiali',
    guideToolsCoveredSuffix: 'strumenti analizzati',
  },
  es: {
    brandSub: 'Software libre para todos',
    navGuides: 'Guías Temáticas',
    navTopPicks: 'Destacados',
    navSubmit: 'Enviar una app',
    navSignIn: 'Iniciar sesión',
    navFavorites: 'Favoritos',
    themeToggleAria: 'Cambiar tema claro o oscuro',
    eyebrow: 'Selección cuidada del mejor software gratuito',
    heroTitle: 'Software gratuito y potente, sin jerga técnica',
    heroSubtitle:
      'Sin términos complicados. Descubre para qué sirve realmente cada programa y descarga la versión oficial al instante.',
    searchPlaceholder: 'Busca por nombre o tarea (ej. video, contraseñas...)',
    searchAriaLabel: 'Buscar aplicaciones',
    categoriesLabel: 'Filtrar por categoría',
    catAll: 'Todas',
    catProductivity: 'Productividad',
    catSecurity: 'Seguridad y Privacidad',
    catGraphics: 'Gráficos y Diseño',
    catVideo: 'Video y Audio',
    catWebApps: 'Apps Web y Nube',
    catUtilities: 'Utilidades y Herramientas',
    catWebsites: 'Sitios Web y SEO',
    liveSearchEyebrow: '¿No encuentras tu app de código abierto favorita?',
    liveSearchPlaceholder: 'Busca entre millones de proyectos abiertos en GitHub...',
    liveSearchAria: 'Buscar proyectos en vivo en GitHub',
    liveSearchLoading: 'Buscando en el índice abierto...',
    liveSearchEmpty: 'No se encontraron proyectos. Prueba otra palabra clave.',
    liveSearchRateLimit: 'Has hecho búsquedas muy rápidas. Espera unos segundos o pega la URL abajo.',
    liveSearchRateHint: 'Pega la URL abajo',
    btnAlreadyOnHubHum: 'Ya en HubHum →',
    btnGoWithHubHum: 'Traducir con HubHum ⚡',
    convTitle: 'Generando guía de la aplicación',
    convStep1: 'Obteniendo información desde GitHub...',
    convStep2: 'Creando guía sencilla con IA...',
    convStep3: 'Verificando enlaces oficiales de descarga...',
    convStep4: 'Publicando la ficha en el catálogo...',
    convDone: '¡Listo! Redirigiendo a tu nueva guía...',
    convPollingHint: 'Normalmente tarda 35–60 segundos. Comprobación automática activa...',
    convErrorMsg: 'No se pudo iniciar la conversión ahora mismo. Inténtalo de nuevo.',
    convTimeoutMsg: 'La publicación está tardando un poco más. Pulsa Reintentar para comprobar.',
    convRetryBtn: 'Reintentar',
    topPicksHeading: 'Lo Mejor de la Semana',
    topPicksSub: 'Los proyectos con más estrellas en GitHub',
    allSoftwareHeading: 'Todo el Catálogo',
    appsAvailableSuffix: 'apps disponibles',
    emptySearch: 'No hay aplicaciones que coincidan con tu búsqueda. Prueba otra palabra clave.',
    pagePrev: 'Anterior',
    pageNext: 'Siguiente',
    loadMoreBtn: 'Cargar 24 más',
    pageLabel: 'Página',
    ofLabel: 'de',
    guidesHeading: 'Guías Temáticas y Comparativas',
    guidesSub: 'Guías prácticas, comparativas y soluciones por tema',
    guideReadMore: 'Ver guía →',
    guideAppsIncluded: 'apps analizadas',
    guidesAllCta: 'Explorar todas las Guías →',
    badgeCloud: 'App Web Cloud',
    badgeSelfHosted: 'App Autoalojada',
    badgeDesktop: 'App de Escritorio',
    badgeCli: 'Herramienta CLI',
    badgeResource: 'Guía y Recurso',
    badgeNew: 'Nuevo',
    starsSuffix: 'estrellas en GitHub',
    chosenByPrefix: '★',
    chosenBySuffix: 'estrellas en GitHub',
    ctaDesktop: 'Explorar y Descargar →',
    ctaCloud: 'Abrir en la Nube →',
    ctaSelfHosted: 'Guía e Instalación →',
    ctaCli: 'Ver Herramienta CLI →',
    ctaResource: 'Abrir Referencia →',
    cliWarningTitle: 'Herramienta de Línea de Comandos (CLI):',
    cliWarningBody:
      'Este programa funciona escribiendo comandos en la terminal sin ventanas gráficas. Si prefieres botones visuales, revisa alternativas Desktop App en la barra lateral.',
    selfHostedWarningTitle: 'Software Autoalojado (Self-Hosted):',
    selfHostedWarningBody:
      'Pensado para instalarse en tu propio servidor o equipo local, no es un sitio público alojado por nosotros.',
    jumpLiveSearch: '¿Buscas otro proyecto? Búscalo en GitHub más abajo ↓',
    submitTitle: 'Enviar una app',
    submitDesc: 'Pega cualquier enlace de GitHub para añadir una guía clara en HubHum',
    submitPlaceholder: 'https://github.com/autor/nombre-app',
    submitBtn: 'Enviar app',
    submitSuccess: 'Tu aplicación se está procesando y estará en línea en breve.',
    submitInvalidUrl: 'Introduce un enlace válido con el formato https://github.com/autor/nombre-app.',
    backAllApps: '← Volver a todo el catálogo',
    saveFavorite: 'Guardar en favoritos',
    savedFavorite: 'Guardada en favoritos',
    partnerTipBadge: 'Socio Patrocinado (#ad)',
    partnerHeadingPrefix: 'Servicio Asociado:',
    partnerFallbackHeading: 'Mejora tu configuración',
    partnerFallbackDesc: 'Solución comercial opcional.',
    partnerCloudBtn: 'Lanzar en Hosting Cloud (#ad)',
    partnerDiscoverPrefix: 'Explorar',
    detailsHeading: 'Ficha rápida',
    detailCategory: 'Categoría:',
    detailMode: 'Formato:',
    detailModeCloud: 'Funciona en tu navegador / nube',
    detailModeSelfHosted: 'Se instala en tu propio servidor o equipo',
    detailModeDesktop: 'Instalador de escritorio',
    detailModeCli: 'Herramienta de línea de comandos (CLI)',
    detailModeResource: 'Lista curada o recurso de referencia',
    detailLicense: 'Licencia:',
    detailOfficialPage: 'Fuente Oficial:',
    detailOpenSource: 'Visitar GitHub',
    clusterSidebarHeading: 'Guías de este Tema',
    clusterPillarLabel: 'Guía Principal:',
    clusterSubpillarLabel: 'Subtema:',
    clusterComparisonLabel: 'Comparar alternativas →',
    relatedGuidesHeading: 'Guías Relacionadas sobre este Tema',
    reviewTitlePrefix: '¿Has probado',
    reviewDesc: 'Ayuda a otros usuarios compartiendo una breve reseña.',
    reviewBtn: 'Escribir reseña',
    disclosureTitle: 'Transparencia de afiliados (#ad):',
    disclosureBody:
      'Los enlaces dentro de Sponsored Partner Tools (#ad) y el bloque lateral son enlaces de afiliados sin coste adicional para ti.',
    footerDisclaimer: 'HubHum es un directorio independiente y no está afiliado con GitHub, Inc.',
    footerAffiliate:
      'Transparencia de afiliados (#ad): Los enlaces patrocinados están separados en su bloque dedicado (#ad). Las estrellas proceden directamente de GitHub.',
    footerCredits:
      'Todas las aplicaciones enlazan directamente con los canales oficiales de sus autores respetando las licencias de código abierto.',
    aboutLink: 'Acerca de y Transparencia',
    privacyLink: 'Política de Privacidad',
    dashboardLink: 'Panel',
    sitemapLink: 'Mapa del sitio',
    dialogTitle: 'Tus Favoritos Guardados',
    dialogDescLocal: 'Tus aplicaciones favoritas se guardan al instante en este navegador.',
    dialogDescAuth: 'Sesión iniciada con GitHub. Administra tus favoritos abajo.',
    dialogNoFavs: 'Aún no has guardado aplicaciones favoritas.',
    dialogClose: 'Cerrar',
    dialogLogout: 'Cerrar sesión',
    detailSummaryNotice: 'Resumen claro en tu idioma:',
    oauthSignInBtn: 'Iniciar sesión con GitHub',
    oauthSignInDesc: 'Inicia sesión en 1 clic para conectar tu cuenta de GitHub y tus favoritos.',
    oauthConnecting: 'Conectando tu cuenta de GitHub...',
    filterFormatLabel: 'Filtrar por formato',
    filterFormatAll: 'Todos los Formatos',
    filterFormatDesktop: 'Apps de Escritorio (GUI)',
    filterFormatSelfHosted: 'Apps Autoalojadas',
    filterFormatCli: 'Herramientas CLI / Dev',
    filterOsLabel: 'Filtrar por sistema operativo',
    filterOsAll: 'Todos los Sistemas',
    filterOsBrowser: 'Navegador / Nube',
    secWhatItDoes: 'Qué hace explicado de forma sencilla',
    secWhoItsFor: 'Para quién es útil',
    secKeyFeatures: 'Funciones principales',
    secHowToInstall: 'Cómo instalarlo (Descarga oficial)',
    secProsAndCons: 'Pros y Contras',
    secSponsoredTools: 'Herramientas Asociadas Patrocinadas (#ad)',
    secSponsoredNote:
      'Servicios comerciales opcionales ajenos al autor original. Los enlaces #ad ayudan a mantener HubHum gratis sin coste adicional.',
    secOfficialSource: 'Fuente Oficial y Créditos:',
    labelPros: 'Pros',
    labelCons: 'Contras',
    guideLevelPillar: 'Guía Principal de Categoría',
    guideLevelSubpillar: 'Tema Específico',
    guideLevelComparison: 'Guía Comparativa',
    guideLevelFoundations: 'Guía para Principiantes',
    guideLevelTroubleshooting: 'Solución de Problemas',
    guideSubpillarsHeading: 'Temas en Esta Categoría',
    guideArticlesHeading: 'Guías Prácticas y Comparativas',
    guideGuidesSub: 'Elige una guía para comparar alternativas paso a paso',
    guideFeaturedAppsHeading: 'Software Gratuito Verificado en Esta Guía',
    guideFeaturedAppsSub: 'Abre cualquier ficha para ver el resumen sencillo y enlaces oficiales',
    guideToolsCoveredSuffix: 'herramientas analizadas',
  },
  fr: {
    brandSub: 'Logiciels libres pour tous',
    navGuides: 'Guides Thématiques',
    navTopPicks: 'Sélection',
    navSubmit: 'Proposer une app',
    navSignIn: 'Connexion',
    navFavorites: 'Favoris',
    themeToggleAria: 'Changer de thème clair ou sombre',
    eyebrow: 'Sélection soignée des meilleurs logiciels gratuits',
    heroTitle: 'Des logiciels gratuits puissants, sans jargon technique',
    heroSubtitle:
      'Fini les termes compliqués. Découvrez à quoi sert vraiment chaque programme et téléchargez la version officielle immédiatement.',
    searchPlaceholder: 'Rechercher par nom ou usage (ex. vidéo, mots de passe...)',
    searchAriaLabel: 'Rechercher un logiciel',
    categoriesLabel: 'Filtrer par catégorie',
    catAll: 'Toutes',
    catProductivity: 'Productivité',
    catSecurity: 'Sécurité et Confidentialité',
    catGraphics: 'Graphisme et Design',
    catVideo: 'Vidéo et Audio',
    catWebApps: 'Apps Web et Cloud',
    catUtilities: 'Utilitaires & Outils',
    catWebsites: 'Sites Web et SEO',
    liveSearchEyebrow: 'Vous ne trouvez pas votre logiciel libre favori ?',
    liveSearchPlaceholder: 'Recherchez parmi des millions de projets sur GitHub...',
    liveSearchAria: 'Rechercher en direct sur GitHub',
    liveSearchLoading: 'Recherche en cours dans le catalogue ouvert...',
    liveSearchEmpty: 'Aucun projet trouvé. Essayez un autre mot-clé.',
    liveSearchRateLimit: 'Recherches trop rapides. Patientez quelques secondes ou collez le lien ci-dessous.',
    liveSearchRateHint: 'Collez le lien ci-dessous',
    btnAlreadyOnHubHum: 'Déjà sur HubHum →',
    btnGoWithHubHum: 'Traduire avec HubHum ⚡',
    convTitle: 'Traduction de la fiche en cours',
    convStep1: 'Récupération des informations depuis GitHub...',
    convStep2: 'Rédaction du guide simple avec IA...',
    convStep3: 'Vérification des liens de téléchargement officiels...',
    convStep4: 'Publication de la fiche dans le catalogue...',
    convDone: 'Terminé ! Redirection vers votre guide...',
    convPollingHint: 'Prêt généralement en 35–60 secondes. Vérification automatique...',
    convErrorMsg: 'Impossible de démarrer la conversion. Veuillez réessayer.',
    convTimeoutMsg: 'La publication prend un peu plus de temps. Cliquez sur Réessayer.',
    convRetryBtn: 'Réessayer',
    topPicksHeading: 'Sélection de la Semaine',
    topPicksSub: 'Les logiciels libres les plus étoilés sur GitHub',
    allSoftwareHeading: 'Tout le Catalogue',
    appsAvailableSuffix: 'apps disponibles',
    emptySearch: 'Aucune application ne correspond à votre recherche.',
    pagePrev: 'Précédent',
    pageNext: 'Suivant',
    loadMoreBtn: 'Charger 24 de plus',
    pageLabel: 'Page',
    ofLabel: 'sur',
    guidesHeading: 'Guides Thématiques & Comparatifs',
    guidesSub: 'Guides pratiques, comparatifs et solutions organisés par thème',
    guideReadMore: 'Lire le guide →',
    guideAppsIncluded: 'apps analysées',
    guidesAllCta: 'Tous les Guides Thématiques →',
    badgeCloud: 'App Web Cloud',
    badgeSelfHosted: 'App Auto-hébergée',
    badgeDesktop: 'App Bureau',
    badgeCli: 'Outil CLI',
    badgeResource: 'Guide & Référence',
    badgeNew: 'Nouveau',
    starsSuffix: 'étoiles sur GitHub',
    chosenByPrefix: '★',
    chosenBySuffix: 'étoiles sur GitHub',
    ctaDesktop: 'Découvrir & Télécharger →',
    ctaCloud: 'Ouvrir dans le Cloud →',
    ctaSelfHosted: 'Installation & Docs →',
    ctaCli: "Voir l'Outil CLI →",
    ctaResource: 'Consulter le Guide →',
    cliWarningTitle: 'Outil en Ligne de Commande (CLI) :',
    cliWarningBody:
      'Ce programme fonctionne par commandes texte dans un terminal plutôt que via des boutons graphiques.',
    selfHostedWarningTitle: 'Application Auto-hébergée (Self-Hosted) :',
    selfHostedWarningBody:
      'Conçue pour être installée sur votre propre ordinateur ou serveur privé (et non un service web hébergé par défaut).',
    jumpLiveSearch: 'Projet introuvable ? Cherchez sur GitHub plus bas ↓',
    submitTitle: 'Proposer une app',
    submitDesc: 'Collez un lien GitHub pour ajouter un guide clair sur HubHum',
    submitPlaceholder: 'https://github.com/auteur/nom-app',
    submitBtn: 'Envoyer',
    submitSuccess: "L'application est en cours de traitement et sera en ligne très bientôt.",
    submitInvalidUrl: 'Veuillez saisir un lien valide au format https://github.com/auteur/nom-app.',
    backAllApps: '← Retour au catalogue',
    saveFavorite: 'Ajouter aux favoris',
    savedFavorite: 'Enregistrée en favoris',
    partnerTipBadge: 'Partenaire Sponsorisé (#ad)',
    partnerHeadingPrefix: 'Service Partenaire :',
    partnerFallbackHeading: 'Optimisez votre usage',
    partnerFallbackDesc: 'Solution commerciale optionnelle.',
    partnerCloudBtn: 'Héberger dans le Cloud (#ad)',
    partnerDiscoverPrefix: 'Découvrir',
    detailsHeading: 'Détails rapides',
    detailCategory: 'Catégorie :',
    detailMode: 'Format :',
    detailModeCloud: 'Application web dans le cloud',
    detailModeSelfHosted: 'Installation sur votre serveur ou PC (Self-Hosted)',
    detailModeDesktop: 'Application de bureau installable',
    detailModeCli: 'Outil en ligne de commande (CLI)',
    detailModeResource: 'Répertoire de ressources ou guide',
    detailLicense: 'Licence :',
    detailOfficialPage: 'Source Officielle :',
    detailOpenSource: 'Voir sur GitHub',
    clusterSidebarHeading: 'Guides du Thème',
    clusterPillarLabel: 'Guide Principal :',
    clusterSubpillarLabel: 'Sous-thème :',
    clusterComparisonLabel: 'Comparer les alternatives →',
    relatedGuidesHeading: 'Guides Associés sur ce Thème',
    reviewTitlePrefix: 'Avez-vous essayé',
    reviewDesc: 'Aidez les autres utilisateurs en partageant votre avis.',
    reviewBtn: 'Laisser un avis',
    disclosureTitle: "Transparence d'affiliation (#ad) :",
    disclosureBody:
      "Les liens situés dans Sponsored Partner Tools (#ad) et le bloc latéral sont des liens d'affiliation sans frais supplémentaires.",
    footerDisclaimer: "HubHum est un répertoire indépendant et n'est pas affilié à GitHub, Inc.",
    footerAffiliate:
      "Transparence d'affiliation (#ad) : Les liens sponsorisés sont isolés dans les blocs dédiés (#ad). Les classements et étoiles proviennent de GitHub.",
    footerCredits:
      'Tous les logiciels renvoient exclusivement vers les canaux officiels de leurs auteurs.',
    aboutLink: 'À Propos & Transparence',
    privacyLink: 'Confidentialité',
    dashboardLink: 'Tableau de bord',
    sitemapLink: 'Plan du site',
    dialogTitle: 'Vos Favoris Enregistrés',
    dialogDescLocal: 'Vos applications favorites sont enregistrées instantanément dans ce navigateur.',
    dialogDescAuth: 'Connecté avec GitHub. Gérez vos favoris ci-dessous.',
    dialogNoFavs: "Vous n'avez pas encore enregistré de favoris.",
    dialogClose: 'Fermer',
    dialogLogout: 'Déconnexion',
    detailSummaryNotice: 'Résumé clair dans votre langue :',
    oauthSignInBtn: 'Se connecter avec GitHub',
    oauthSignInDesc: 'Connectez-vous en 1 clic pour associer votre compte GitHub et vos favoris.',
    oauthConnecting: 'Connexion à GitHub en cours...',
    filterFormatLabel: 'Filtrer par format',
    filterFormatAll: 'Tous les Formats',
    filterFormatDesktop: 'Apps Bureau (GUI)',
    filterFormatSelfHosted: 'Apps Auto-hébergées',
    filterFormatCli: 'Outils Développeurs / CLI',
    filterOsLabel: 'Filtrer par système',
    filterOsAll: 'Tous les Systèmes',
    filterOsBrowser: 'Navigateur / Cloud',
    secWhatItDoes: 'À quoi ça sert en termes simples',
    secWhoItsFor: 'Pour qui est-ce adapté',
    secKeyFeatures: 'Fonctionnalités clés',
    secHowToInstall: "Comment l'installer (Téléchargement)",
    secProsAndCons: 'Avantages et Inconvénients',
    secSponsoredTools: 'Outils Partenaires Sponsorisés (#ad)',
    secSponsoredNote:
      'Services commerciaux optionnels sans lien avec le développeur open-source. Ces liens #ad soutiennent HubHum sans surcoût.',
    secOfficialSource: 'Source Officielle et Crédits :',
    labelPros: 'Avantages',
    labelCons: 'Limites',
    guideLevelPillar: 'Guide Principal de Catégorie',
    guideLevelSubpillar: 'Thème Ciblé',
    guideLevelComparison: 'Comparatif Détaillé',
    guideLevelFoundations: 'Guide Débutant',
    guideLevelTroubleshooting: 'Dépannage & Solutions',
    guideSubpillarsHeading: 'Sous-thèmes dans Cette Catégorie',
    guideArticlesHeading: 'Guides Pratiques & Comparatifs',
    guideGuidesSub: 'Choisissez un guide ci-dessous pour comparer les options étape par étape',
    guideFeaturedAppsHeading: 'Logiciels Gratuits Vérifiés dans Ce Guide',
    guideFeaturedAppsSub: 'Cliquez sur une fiche pour consulter l’explication simple et le lien officiel',
    guideToolsCoveredSuffix: 'outils couverts',
  },
  de: {
    brandSub: 'Freie Software für alle',
    navGuides: 'Themen-Guides',
    navTopPicks: 'Top-Auswahl',
    navSubmit: 'App vorschlagen',
    navSignIn: 'Anmelden',
    navFavorites: 'Favoriten',
    themeToggleAria: 'Helles oder dunkles Design wechseln',
    eyebrow: 'Handverlesene Auswahl der besten kostenlosen Software',
    heroTitle: 'Starke kostenlose Software, ganz ohne Fachjargon',
    heroSubtitle:
      'Keine komplizierten Begriffe. Erfahren Sie sofort, wofür jedes Programm gedacht ist, und laden Sie das Original herunter.',
    searchPlaceholder: 'Nach Name oder Aufgabe suchen (z. B. Video, Passwörter...)',
    searchAriaLabel: 'Softwarekatalog durchsuchen',
    categoriesLabel: 'Nach Kategorie filtern',
    catAll: 'Alle',
    catProductivity: 'Produktivität',
    catSecurity: 'Sicherheit & Datenschutz',
    catGraphics: 'Grafik & Design',
    catVideo: 'Video & Audio',
    catWebApps: 'Web-Apps & Cloud',
    catUtilities: 'System- & Power-Tools',
    catWebsites: 'Websites & SEO',
    liveSearchEyebrow: 'Ihre Lieblings-App noch nicht dabei?',
    liveSearchPlaceholder: 'Millionen Open-Source-Projekte auf GitHub durchsuchen...',
    liveSearchAria: 'Live auf GitHub nach Projekten suchen',
    liveSearchLoading: 'Suche läuft...',
    liveSearchEmpty: 'Keine passenden Projekte gefunden. Probieren Sie einen anderen Begriff.',
    liveSearchRateLimit: 'Zu viele schnelle Suchanfragen. Bitte kurz warten oder URL direkt einfügen.',
    liveSearchRateHint: 'URL direkt unten einfügen',
    btnAlreadyOnHubHum: 'Bereits auf HubHum →',
    btnGoWithHubHum: 'Mit HubHum laden ⚡',
    convTitle: 'App-Anleitung wird erstellt',
    convStep1: 'Informationen werden von GitHub abgerufen...',
    convStep2: 'Verständliche Anleitung wird mit KI erstellt...',
    convStep3: 'Offizielle Download-Links werden geprüft...',
    convStep4: 'Seite wird im HubHum-Katalog veröffentlicht...',
    convDone: 'Fertig! Weiterleitung zur neuen Anleitung...',
    convPollingHint: 'Dauert meist 35–60 Sekunden. Automatische Prüfung läuft...',
    convErrorMsg: 'Konvertierung konnte gerade nicht gestartet werden. Bitte erneut versuchen.',
    convTimeoutMsg: 'Die Veröffentlichung dauert etwas länger. Klicken Sie auf Erneut versuchen.',
    convRetryBtn: 'Erneut versuchen',
    topPicksHeading: 'Top-Tipps der Woche',
    topPicksSub: 'Beliebte Open-Source-Projekte nach GitHub-Sternen',
    allSoftwareHeading: 'Alle Programme',
    appsAvailableSuffix: 'Apps verfügbar',
    emptySearch: 'Keine passenden Apps gefunden. Versuchen Sie einen anderen Suchbegriff.',
    pagePrev: 'Zurück',
    pageNext: 'Weiter',
    loadMoreBtn: 'Weitere 24 laden',
    pageLabel: 'Seite',
    ofLabel: 'von',
    guidesHeading: 'Themen-Guides & Vergleiche',
    guidesSub: 'Praxisnahe Ratgeber, Vergleiche und Problemlösungen nach Thema',
    guideReadMore: 'Ratgeber öffnen →',
    guideAppsIncluded: 'Apps enthalten',
    guidesAllCta: 'Alle Themen-Guides ansehen →',
    badgeCloud: 'Cloud Web-App',
    badgeSelfHosted: 'Self-Hosted-App',
    badgeDesktop: 'Desktop-App',
    badgeCli: 'CLI-Tool',
    badgeResource: 'Leitfaden & Referenz',
    badgeNew: 'Neu',
    starsSuffix: 'Sterne auf GitHub',
    chosenByPrefix: '★',
    chosenBySuffix: 'Sterne auf GitHub',
    ctaDesktop: 'Entdecken & Laden →',
    ctaCloud: 'In der Cloud öffnen →',
    ctaSelfHosted: 'Setup & Doku →',
    ctaCli: 'CLI-Tool öffnen →',
    ctaResource: 'Referenz öffnen →',
    cliWarningTitle: 'Kommandozeilen-Programm (CLI):',
    cliWarningBody:
      'Dieses Tool wird über Textbefehle im Terminal ohne klassische grafische Oberfläche bedient.',
    selfHostedWarningTitle: 'Self-Hosted Software:',
    selfHostedWarningBody:
      'Für den Betrieb auf Ihrem eigenen Server oder lokalen Rechner gedacht – kein direkt nutzbarer öffentlicher Cloud-Dienst.',
    jumpLiveSearch: 'Nicht dabei? Millionen GitHub-Projekte unten durchsuchen ↓',
    submitTitle: 'App vorschlagen',
    submitDesc: 'Fügen Sie einen GitHub-Link ein, um eine verständliche Anleitung auf HubHum zu erstellen',
    submitPlaceholder: 'https://github.com/autor/app-name',
    submitBtn: 'Absenden',
    submitSuccess: 'Die App wird verarbeitet und ist in Kürze online.',
    submitInvalidUrl: 'Bitte geben Sie eine gültige URL im Format https://github.com/autor/app-name ein.',
    backAllApps: '← Zurück zur Übersicht',
    saveFavorite: 'Als Favorit speichern',
    savedFavorite: 'Als Favorit gespeichert',
    partnerTipBadge: 'Gesponserter Partner (#ad)',
    partnerHeadingPrefix: 'Partner-Dienst:',
    partnerFallbackHeading: 'Einrichtung erweitern',
    partnerFallbackDesc: 'Optionale kommerzielle Partnerlösung.',
    partnerCloudBtn: 'Auf Cloud-Hosting starten (#ad)',
    partnerDiscoverPrefix: 'Entdecken:',
    detailsHeading: 'Kurzinfos',
    detailCategory: 'Kategorie:',
    detailMode: 'Format:',
    detailModeCloud: 'Läuft im Browser / in der Cloud',
    detailModeSelfHosted: 'Betrieb auf eigenem Server / PC (Self-Hosted)',
    detailModeDesktop: 'Desktop-Programm zum Installieren',
    detailModeCli: 'Kommandozeilen-Werkzeug (CLI)',
    detailModeResource: 'Kuratierte Liste oder Leitfaden',
    detailLicense: 'Lizenz:',
    detailOfficialPage: 'Offizielle Quelle:',
    detailOpenSource: 'GitHub-Quelle öffnen',
    clusterSidebarHeading: 'Themen-Cluster-Ratgeber',
    clusterPillarLabel: 'Hauptkategorie:',
    clusterSubpillarLabel: 'Unterthema:',
    clusterComparisonLabel: 'Alternativen vergleichen →',
    relatedGuidesHeading: 'Verwandte Ratgeber zu diesem Thema',
    reviewTitlePrefix: 'Schon ausprobiert:',
    reviewDesc: 'Helfen Sie anderen Nutzern mit einer kurzen Bewertung.',
    reviewBtn: 'Bewertung schreiben',
    disclosureTitle: 'Affiliate-Hinweis (#ad):',
    disclosureBody:
      'Links im Bereich Sponsored Partner Tools (#ad) und in der Seitenleiste sind Affiliate-Links ohne Mehrkosten für Sie.',
    footerDisclaimer: 'HubHum ist ein unabhängiges Verzeichnis und nicht mit GitHub, Inc. verbunden.',
    footerAffiliate:
      'Affiliate-Hinweis (#ad): Gesponserte Links befinden sich ausschließlich in klar markierten Partner-Bereichen (#ad).',
    footerCredits:
      'Alle Programme verweisen direkt auf die offiziellen Kanäle der Entwickler gemäß Open-Source-Lizenz.',
    aboutLink: 'Über HubHum & Transparenz',
    privacyLink: 'Datenschutz',
    dashboardLink: 'Dashboard',
    sitemapLink: 'Sitemap',
    dialogTitle: 'Ihre gespeicherten Favoriten',
    dialogDescLocal: 'Ihre Favoriten werden direkt in diesem Browser gespeichert.',
    dialogDescAuth: 'Mit GitHub angemeldet. Verwalten Sie Ihre Favoriten unten.',
    dialogNoFavs: 'Sie haben noch keine Favoriten gespeichert.',
    dialogClose: 'Schließen',
    dialogLogout: 'Abmelden',
    detailSummaryNotice: 'Verständliche Zusammenfassung:',
    oauthSignInBtn: 'Mit GitHub anmelden',
    oauthSignInDesc: 'Melden Sie sich mit 1 Klick an, um Ihr GitHub-Konto zu verbinden.',
    oauthConnecting: 'GitHub-Konto wird verbunden...',
    filterFormatLabel: 'Nach Format filtern',
    filterFormatAll: 'Alle Formate',
    filterFormatDesktop: 'Desktop-Apps (GUI)',
    filterFormatSelfHosted: 'Self-Hosted-Apps',
    filterFormatCli: 'Entwickler- & CLI-Tools',
    filterOsLabel: 'Nach System filtern',
    filterOsAll: 'Alle Systeme',
    filterOsBrowser: 'Browser / Cloud',
    secWhatItDoes: 'Was es einfach erklärt macht',
    secWhoItsFor: 'Für wen es geeignet ist',
    secKeyFeatures: 'Hauptfunktionen',
    secHowToInstall: 'Installation & Download',
    secProsAndCons: 'Vorteile & Nachteile',
    secSponsoredTools: 'Gesponserte Partner-Tools (#ad)',
    secSponsoredNote:
      'Optionale kommerzielle Dienste ohne Verbindung zum Open-Source-Autor. Mit #ad markierte Links finanzieren HubHum ohne Aufpreis.',
    secOfficialSource: 'Offizielle Quelle & Credits:',
    labelPros: 'Vorteile',
    labelCons: 'Nachteile',
    guideLevelPillar: 'Hauptkategorie-Ratgeber',
    guideLevelSubpillar: 'Themen-Hub',
    guideLevelComparison: 'Vergleichsratgeber',
    guideLevelFoundations: 'Einsteiger-Grundlagen',
    guideLevelTroubleshooting: 'Fehlerbehebung',
    guideSubpillarsHeading: 'Schwerpunkte in dieser Kategorie',
    guideArticlesHeading: 'Praxisratgeber & Vergleiche',
    guideGuidesSub: 'Wählen Sie unten einen Ratgeber für Vergleiche und Schritt-für-Schritt-Tipps',
    guideFeaturedAppsHeading: 'Geprüfte kostenlose Software in diesem Ratgeber',
    guideFeaturedAppsSub: 'Öffnen Sie eine Karte für verständliche Infos und offizielle Download-Links',
    guideToolsCoveredSuffix: 'Programme behandelt',
  },
};

export const CATEGORY_I18N_KEY: Record<string, keyof TranslationDict> = {
  All: 'catAll',
  Productivity: 'catProductivity',
  'Security & Privacy': 'catSecurity',
  'Graphics & Design': 'catGraphics',
  'Video & Audio': 'catVideo',
  'Web Apps & Cloud': 'catWebApps',
  'Utilities & Power Tools': 'catUtilities',
  'Websites & SEO': 'catWebsites',
};
