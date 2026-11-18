export type SupportedLang = 'en' | 'it' | 'es' | 'fr' | 'de';

export const SUPPORTED_LANGS: SupportedLang[] = ['en', 'it', 'es', 'fr', 'de'];

export interface TranslationDict {
  brandSub: string;
  navTopPicks: string;
  navSubmit: string;
  navSignIn: string;
  navFavorites: string;
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
  convTriggerHint: string;
  convTriggerBtn: string;
  convPollingHint: string;
  topPicksHeading: string;
  topPicksSub: string;
  allSoftwareHeading: string;
  appsAvailableSuffix: string;
  emptySearch: string;
  guidesHeading: string;
  guidesSub: string;
  guideReadMore: string;
  guideAppsIncluded: string;
  badgeCloud: string;
  badgeDesktop: string;
  badgeNew: string;
  chosenByPrefix: string;
  chosenBySuffix: string;
  ctaDesktop: string;
  ctaCloud: string;
  submitTitle: string;
  submitDesc: string;
  submitPlaceholder: string;
  submitBtn: string;
  submitSuccess: string;
  submitInvalidUrl: string;
  submitConfirmLink: string;
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
  detailModeDesktop: string;
  detailLicense: string;
  detailOfficialPage: string;
  detailOpenSource: string;
  reviewTitlePrefix: string;
  reviewDesc: string;
  reviewBtn: string;
  disclosureTitle: string;
  disclosureBody: string;
  footerAffiliate: string;
  footerCredits: string;
  dialogTitle: string;
  dialogDescLocal: string;
  dialogDescAuth: string;
  dialogNoFavs: string;
  dialogClose: string;
  dialogLogout: string;
  detailSummaryNotice: string;
  syncOptionalTitle: string;
  syncOptionalDesc: string;
  syncTokenPlaceholder: string;
  syncConnectBtn: string;
  syncSuccess: string;
  syncInvalidToken: string;
}

export const TRANSLATIONS: Record<SupportedLang, TranslationDict> = {
  en: {
    brandSub: 'Free software for humans',
    navTopPicks: 'Top Picks',
    navSubmit: 'Submit an App',
    navSignIn: 'Favorites',
    navFavorites: 'Favorites',
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
    convStep1: 'Fetching repository structure & latest releases...',
    convStep2: 'Translating into plain English & mapping features with AI...',
    convStep3: 'Generating human-friendly guide & checking official download links...',
    convStep4: 'Publishing static page to HubHum catalog...',
    convDone: 'Done! Redirecting to your new guide...',
    convTriggerHint: 'Click below to start automatic conversion in a new tab—this page will redirect automatically as soon as it goes live.',
    convTriggerBtn: 'Confirm & Start Conversion →',
    convPollingHint: 'Checking catalog every 4 seconds for the published page...',
    topPicksHeading: 'Top Picks This Week',
    topPicksSub: 'Most trusted apps chosen by the community',
    allSoftwareHeading: 'All Software',
    appsAvailableSuffix: 'apps available',
    emptySearch: 'No apps match your search. Try another keyword or submit a link below.',
    guidesHeading: 'Curated Guides',
    guidesSub: 'Practical roundups to help you pick the right free tool',
    guideReadMore: 'Read guide →',
    guideAppsIncluded: 'apps included',
    badgeCloud: 'Cloud Web App',
    badgeDesktop: 'Free Desktop App',
    badgeNew: 'New',
    chosenByPrefix: 'Chosen by',
    chosenBySuffix: 'users',
    ctaDesktop: 'Explore & Download →',
    ctaCloud: 'Open in Cloud →',
    submitTitle: 'Submit an App',
    submitDesc: 'Paste any GitHub URL to add a plain-English guide to HubHum',
    submitPlaceholder: 'https://github.com/author/app-name',
    submitBtn: 'Submit App',
    submitSuccess: 'Your app is being processed and will be live in about 2 minutes.',
    submitInvalidUrl: 'Please enter a valid URL formatted as https://github.com/author/app-name.',
    submitConfirmLink: 'Confirm submission →',
    backAllApps: '← Back to all software',
    saveFavorite: 'Save to Favorites',
    savedFavorite: 'Saved in Favorites',
    partnerTipBadge: 'Recommended Add-on (#ad)',
    partnerHeadingPrefix: 'Recommended:',
    partnerFallbackHeading: 'Enhance your setup',
    partnerFallbackDesc: 'Curated partner solution suited for this software category.',
    partnerCloudBtn: 'Open in Cloud (1-Click)',
    partnerDiscoverPrefix: 'Explore',
    detailsHeading: 'Quick Specs',
    detailCategory: 'Category:',
    detailMode: 'Format:',
    detailModeCloud: 'Runs in your browser / cloud',
    detailModeDesktop: 'Installs on your device',
    detailLicense: 'License:',
    detailOfficialPage: 'Official Page:',
    detailOpenSource: 'Visit source',
    reviewTitlePrefix: 'Have you tried',
    reviewDesc: 'Help everyday users decide by sharing a quick review.',
    reviewBtn: 'Write a review',
    disclosureTitle: 'Affiliate transparency (#ad):',
    disclosureBody:
      'Some links on this page are affiliate links. If you choose to activate a service through them, we may earn a commission at no extra cost to you.',
    footerAffiliate:
      'Affiliate transparency (#ad): Some links on HubHum are affiliate links. If you purchase a service through them, we may earn a commission at no extra cost to you.',
    footerCredits:
      'All listed software links strictly to official creator channels in full respect of open-source licenses.',
    dialogTitle: 'Your Saved Favorites',
    dialogDescLocal:
      'Your favorite apps are saved instantly in this browser—no account needed.',
    dialogDescAuth: 'Connected to GitHub. Manage your saved favorites below.',
    dialogNoFavs: 'You have not saved any favorite apps yet. Click the heart button on any app page!',
    dialogClose: 'Close',
    dialogLogout: 'Disconnect',
    detailSummaryNotice: 'Plain-language summary in your language:',
    syncOptionalTitle: 'Optional: Sync & Direct Submission',
    syncOptionalDesc:
      'Want to sync your favorites across devices or trigger instant conversions? Enter your GitHub Personal Token or connect your account.',
    syncTokenPlaceholder: 'GitHub Personal Token (optional)',
    syncConnectBtn: 'Connect',
    syncSuccess: 'Connected as',
    syncInvalidToken: 'Could not verify that token. Local favorites remain saved.',
  },
  it: {
    brandSub: 'App libere per tutti',
    navTopPicks: 'Top della settimana',
    navSubmit: "Proponi un'app",
    navSignIn: 'Preferiti',
    navFavorites: 'Preferiti',
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
    convTitle: 'Traduzione scheda in corso',
    convStep1: 'Analisi della struttura del progetto e delle versioni ufficiali...',
    convStep2: 'Traduzione in linguaggio semplice e analisi delle funzioni con AI...',
    convStep3: 'Creazione della guida e verifica dei link di download ufficiali...',
    convStep4: 'Pubblicazione della nuova pagina nel catalogo HubHum...',
    convDone: 'Fatto! Reindirizzamento alla nuova guida in corso...',
    convTriggerHint: 'Clicca qui sotto per avviare la conversione automatica in una nuova scheda: questa pagina ti porterà alla guida appena pronta.',
    convTriggerBtn: 'Conferma e Avvia Conversione →',
    convPollingHint: 'Controllo automatico del catalogo ogni 4 secondi...',
    topPicksHeading: 'Migliori della Settimana',
    topPicksSub: 'I software più apprezzati dalla community',
    allSoftwareHeading: 'Tutto il Catalogo',
    appsAvailableSuffix: 'app disponibili',
    emptySearch: "Nessuna app corrisponde alla ricerca. Prova un'altra parola o proponi un link qui sotto.",
    guidesHeading: 'Guide e Raccolte',
    guidesSub: 'Selezioni pratiche per scegliere lo strumento gratuito giusto',
    guideReadMore: 'Leggi la guida →',
    guideAppsIncluded: 'app incluse',
    badgeCloud: 'Web App Cloud',
    badgeDesktop: 'App Gratuita',
    badgeNew: 'Novità',
    chosenByPrefix: 'Scelto da',
    chosenBySuffix: 'utenti',
    ctaDesktop: 'Scopri & Scarica →',
    ctaCloud: 'Apri nel Cloud →',
    submitTitle: "Proponi un'app",
    submitDesc: 'Incolla un link GitHub per aggiungere una guida chiara su HubHum',
    submitPlaceholder: 'https://github.com/autore/nome-app',
    submitBtn: 'Invia app',
    submitSuccess: "L'app è in elaborazione e sarà online tra circa 2 minuti.",
    submitInvalidUrl: 'Inserisci un indirizzo valido nel formato https://github.com/autore/nome-app.',
    submitConfirmLink: 'Conferma invio →',
    backAllApps: '← Torna a tutte le app',
    saveFavorite: 'Salva nei preferiti',
    savedFavorite: 'Salvata nei preferiti',
    partnerTipBadge: 'Consiglio pratico (#ad)',
    partnerHeadingPrefix: 'Consigliato:',
    partnerFallbackHeading: 'Migliora la tua esperienza',
    partnerFallbackDesc: 'Soluzione partner selezionata per questa categoria.',
    partnerCloudBtn: 'Apri nel Cloud (1-Click)',
    partnerDiscoverPrefix: 'Scopri',
    detailsHeading: 'Dettagli rapidi',
    detailCategory: 'Categoria:',
    detailMode: 'Modalità:',
    detailModeCloud: 'Applicazione web nel cloud',
    detailModeDesktop: 'Installazione diretta sul dispositivo',
    detailLicense: 'Licenza:',
    detailOfficialPage: 'Pagina ufficiale:',
    detailOpenSource: 'Apri fonte',
    reviewTitlePrefix: 'Hai provato',
    reviewDesc: 'Aiuta altri utenti a scegliere lasciando un parere veloce.',
    reviewBtn: 'Lascia una recensione',
    disclosureTitle: 'Trasparenza affiliazioni (#ad):',
    disclosureBody:
      'Alcuni link su questa pagina sono di affiliazione: se attivi un servizio tramite questi link potremmo ricevere una commissione, senza costi aggiuntivi per te.',
    footerAffiliate:
      'Trasparenza affiliazioni (#ad): Alcuni link su HubHum sono link di affiliazione. Se acquisti un servizio tramite questi link potremmo ricevere una commissione, senza costi aggiuntivi per te.',
    footerCredits:
      'Tutti i software rimandano esclusivamente ai canali ufficiali dei rispettivi autori nel rispetto delle licenze open-source.',
    dialogTitle: 'I tuoi Preferiti',
    dialogDescLocal:
      'I tuoi preferiti restano salvati subito in questo browser, senza bisogno di registrazione.',
    dialogDescAuth: 'Account GitHub collegato. Gestisci i tuoi preferiti qui sotto.',
    dialogNoFavs: 'Non hai ancora salvato nessuna app. Premi il cuore su una qualsiasi scheda!',
    dialogClose: 'Chiudi',
    dialogLogout: 'Scollega',
    detailSummaryNotice: 'Sintesi chiara nella tua lingua:',
    syncOptionalTitle: 'Opzionale: Sincronizzazione GitHub',
    syncOptionalDesc:
      'Vuoi sincronizzare i tuoi preferiti tra dispositivi diversi? Inserisci il tuo GitHub Personal Token o collega il tuo account.',
    syncTokenPlaceholder: 'GitHub Personal Token (opzionale)',
    syncConnectBtn: 'Collega',
    syncSuccess: 'Collegato come',
    syncInvalidToken: 'Impossibile verificare questo token. I preferiti locali restano al sicuro.',
  },
  es: {
    brandSub: 'Software libre para todos',
    navTopPicks: 'Destacados',
    navSubmit: 'Enviar una app',
    navSignIn: 'Favoritos',
    navFavorites: 'Favoritos',
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
    convStep1: 'Analizando la estructura y las versiones oficiales...',
    convStep2: 'Traduciendo a lenguaje sencillo con IA...',
    convStep3: 'Generando la guía y verificando enlaces oficiales...',
    convStep4: 'Publicando página estática en el catálogo de HubHum...',
    convDone: '¡Listo! Redirigiendo a tu nueva guía...',
    convTriggerHint: 'Haz clic abajo para iniciar la conversión automática en una nueva pestaña; esta ventana te redirigirá en cuanto esté lista.',
    convTriggerBtn: 'Confirmar e Iniciar Conversión →',
    convPollingHint: 'Comprobando el catálogo cada 4 segundos...',
    topPicksHeading: 'Lo Mejor de la Semana',
    topPicksSub: 'Las aplicaciones más valoradas por la comunidad',
    allSoftwareHeading: 'Todo el Catálogo',
    appsAvailableSuffix: 'apps disponibles',
    emptySearch: 'No hay aplicaciones que coincidan con tu búsqueda. Prueba otra palabra clave.',
    guidesHeading: 'Guías Prácticas',
    guidesSub: 'Selecciones para elegir la herramienta gratuita adecuada',
    guideReadMore: 'Leer guía →',
    guideAppsIncluded: 'apps incluidas',
    badgeCloud: 'App Web en la Nube',
    badgeDesktop: 'App Gratuita',
    badgeNew: 'Nuevo',
    chosenByPrefix: 'Elegido por',
    chosenBySuffix: 'usuarios',
    ctaDesktop: 'Explorar y Descargar →',
    ctaCloud: 'Abrir en la Nube →',
    submitTitle: 'Enviar una app',
    submitDesc: 'Pega cualquier enlace de GitHub para añadir una guía clara en HubHum',
    submitPlaceholder: 'https://github.com/autor/nombre-app',
    submitBtn: 'Enviar app',
    submitSuccess: 'Tu aplicación se está procesando y estará en línea en unos 2 minutos.',
    submitInvalidUrl: 'Introduce un enlace válido con el formato https://github.com/autor/nombre-app.',
    submitConfirmLink: 'Confirmar envío →',
    backAllApps: '← Volver a todo el catálogo',
    saveFavorite: 'Guardar en favoritos',
    savedFavorite: 'Guardada en favoritos',
    partnerTipBadge: 'Recomendación (#ad)',
    partnerHeadingPrefix: 'Recomendado:',
    partnerFallbackHeading: 'Mejora tu configuración',
    partnerFallbackDesc: 'Solución asociada ideal para esta categoría de software.',
    partnerCloudBtn: 'Abrir en la Nube (1-Clic)',
    partnerDiscoverPrefix: 'Explorar',
    detailsHeading: 'Ficha rápida',
    detailCategory: 'Categoría:',
    detailMode: 'Formato:',
    detailModeCloud: 'Funciona en tu navegador / nube',
    detailModeDesktop: 'Se instala en tu equipo',
    detailLicense: 'Licencia:',
    detailOfficialPage: 'Página oficial:',
    detailOpenSource: 'Visitar fuente',
    reviewTitlePrefix: '¿Has probado',
    reviewDesc: 'Ayuda a otros usuarios compartiendo una breve reseña.',
    reviewBtn: 'Escribir reseña',
    disclosureTitle: 'Transparencia de afiliados (#ad):',
    disclosureBody:
      'Algunos enlaces en esta página son de afiliados. Si contratas un servicio mediante ellos, podemos recibir una comisión sin costo adicional para ti.',
    footerAffiliate:
      'Transparencia de afiliados (#ad): Algunos enlaces en HubHum son de afiliados. Si compras un servicio mediante ellos, podemos recibir una comisión sin coste adicional para ti.',
    footerCredits:
      'Todas las aplicaciones enlazan directamente con los canales oficiales de sus autores respetando las licencias de código abierto.',
    dialogTitle: 'Tus Favoritos Guardados',
    dialogDescLocal: 'Tus aplicaciones favoritas se guardan al instante en este navegador.',
    dialogDescAuth: 'Cuenta de GitHub conectada. Administra tus favoritos abajo.',
    dialogNoFavs: 'Aún no has guardado aplicaciones favoritas.',
    dialogClose: 'Cerrar',
    dialogLogout: 'Desconectar',
    detailSummaryNotice: 'Resumen claro en tu idioma:',
    syncOptionalTitle: 'Opcional: Sincronización con GitHub',
    syncOptionalDesc:
      '¿Quieres sincronizar tus favoritos entre dispositivos? Introduce tu GitHub Personal Token o conecta tu cuenta.',
    syncTokenPlaceholder: 'GitHub Personal Token (opcional)',
    syncConnectBtn: 'Conectar',
    syncSuccess: 'Conectado como',
    syncInvalidToken: 'No se pudo verificar el token. Tus favoritos locales siguen guardados.',
  },
  fr: {
    brandSub: 'Logiciels libres pour tous',
    navTopPicks: 'Sélection',
    navSubmit: 'Proposer une app',
    navSignIn: 'Favoris',
    navFavorites: 'Favoris',
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
    convStep1: 'Analyse du projet et des versions officielles...',
    convStep2: 'Traduction en langage clair avec notre IA...',
    convStep3: 'Création du guide et contrôle des liens officiels...',
    convStep4: 'Publication de la page sur le catalogue HubHum...',
    convDone: 'Terminé ! Redirection vers votre guide...',
    convTriggerHint: 'Cliquez ci-dessous pour lancer la conversion automatique dans un nouvel onglet ; cette page vous redirigera dès que possible.',
    convTriggerBtn: 'Confirmer et Lancer la Conversion →',
    convPollingHint: 'Vérification du catalogue toutes les 4 secondes...',
    topPicksHeading: 'Sélection de la Semaine',
    topPicksSub: 'Les applications les plus appréciées par la communauté',
    allSoftwareHeading: 'Tout le Catalogue',
    appsAvailableSuffix: 'apps disponibles',
    emptySearch: 'Aucune application ne correspond à votre recherche.',
    guidesHeading: 'Guides Pratiques',
    guidesSub: 'Sélections pour choisir le bon outil gratuit',
    guideReadMore: 'Lire le guide →',
    guideAppsIncluded: 'apps incluses',
    badgeCloud: 'App Web Cloud',
    badgeDesktop: 'App Gratuite',
    badgeNew: 'Nouveau',
    chosenByPrefix: 'Choisi par',
    chosenBySuffix: 'utilisateurs',
    ctaDesktop: 'Découvrir & Télécharger →',
    ctaCloud: 'Ouvrir dans le Cloud →',
    submitTitle: 'Proposer une app',
    submitDesc: 'Collez un lien GitHub pour ajouter un guide clair sur HubHum',
    submitPlaceholder: 'https://github.com/auteur/nom-app',
    submitBtn: 'Envoyer',
    submitSuccess: "L'application est en cours de traitement et sera en ligne dans environ 2 minutes.",
    submitInvalidUrl: 'Veuillez saisir un lien valide au format https://github.com/auteur/nom-app.',
    submitConfirmLink: "Confirmer l'envoi →",
    backAllApps: '← Retour au catalogue',
    saveFavorite: 'Ajouter aux favoris',
    savedFavorite: 'Enregistrée en favoris',
    partnerTipBadge: 'Recommandation (#ad)',
    partnerHeadingPrefix: 'Recommandé :',
    partnerFallbackHeading: 'Optimisez votre usage',
    partnerFallbackDesc: 'Solution partenaire sélectionnée pour cette catégorie.',
    partnerCloudBtn: 'Ouvrir dans le Cloud (1-Clic)',
    partnerDiscoverPrefix: 'Découvrir',
    detailsHeading: 'Détails rapides',
    detailCategory: 'Catégorie :',
    detailMode: 'Format :',
    detailModeCloud: 'Application web dans le cloud',
    detailModeDesktop: 'Installation directe sur votre appareil',
    detailLicense: 'Licence :',
    detailOfficialPage: 'Page officielle :',
    detailOpenSource: 'Voir la source',
    reviewTitlePrefix: 'Avez-vous essayé',
    reviewDesc: 'Aidez les autres utilisateurs en partageant votre avis.',
    reviewBtn: 'Laisser un avis',
    disclosureTitle: "Transparence d'affiliation (#ad) :",
    disclosureBody:
      "Certains liens sur cette page sont des liens d'affiliation. Si vous souscrivez un service via ces liens, nous pouvons percevoir une commission sans surcoût pour vous.",
    footerAffiliate:
      "Transparence d'affiliation (#ad) : Certains liens sur HubHum sont affiliés. Si vous achetez un service via ces liens, nous pouvons percevoir une commission sans frais supplémentaires.",
    footerCredits:
      'Tous les logiciels renvoient exclusivement vers les canaux officiels de leurs auteurs.',
    dialogTitle: 'Vos Favoris Enregistrés',
    dialogDescLocal: 'Vos applications favorites sont enregistrées instantanément dans ce navigateur.',
    dialogDescAuth: 'Compte GitHub connecté. Gérez vos favoris ci-dessous.',
    dialogNoFavs: "Vous n'avez pas encore enregistré de favoris.",
    dialogClose: 'Fermer',
    dialogLogout: 'Déconnecter',
    detailSummaryNotice: 'Résumé clair dans votre langue :',
    syncOptionalTitle: 'Optionnel : Synchronisation GitHub',
    syncOptionalDesc:
      'Vous souhaitez synchroniser vos favoris entre appareils ? Saisissez votre GitHub Personal Token ou connectez votre compte.',
    syncTokenPlaceholder: 'GitHub Personal Token (optionnel)',
    syncConnectBtn: 'Connecter',
    syncSuccess: 'Connecté en tant que',
    syncInvalidToken: 'Jeton invalide. Vos favoris locaux restent sauvegardés.',
  },
  de: {
    brandSub: 'Freie Software für alle',
    navTopPicks: 'Top-Auswahl',
    navSubmit: 'App vorschlagen',
    navSignIn: 'Favoriten',
    navFavorites: 'Favoriten',
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
    convStep1: 'Projektstruktur und aktuelle Releases werden geladen...',
    convStep2: 'Verständliche Übersetzung mit KI läuft...',
    convStep3: 'Leitfaden und offizielle Download-Links werden geprüft...',
    convStep4: 'Statische Seite wird im HubHum-Katalog veröffentlicht...',
    convDone: 'Fertig! Weiterleitung zur neuen Anleitung...',
    convTriggerHint: 'Klicken Sie unten, um die automatische Konvertierung in einem neuen Tab zu starten; diese Seite leitet danach automatisch weiter.',
    convTriggerBtn: 'Bestätigen & Konvertierung starten →',
    convPollingHint: 'Prüfe Katalog alle 4 Sekunden...',
    topPicksHeading: 'Top-Tipps der Woche',
    topPicksSub: 'Beliebte Programme aus der Community',
    allSoftwareHeading: 'Alle Programme',
    appsAvailableSuffix: 'Apps verfügbar',
    emptySearch: 'Keine passenden Apps gefunden. Versuchen Sie einen anderen Suchbegriff.',
    guidesHeading: 'Kuratiere Ratgeber',
    guidesSub: 'Praktische Empfehlungen für kostenlose Alternativen',
    guideReadMore: 'Ratgeber lesen →',
    guideAppsIncluded: 'Apps enthalten',
    badgeCloud: 'Cloud Web-App',
    badgeDesktop: 'Kostenlose App',
    badgeNew: 'Neu',
    chosenByPrefix: 'Gewählt von',
    chosenBySuffix: 'Nutzern',
    ctaDesktop: 'Entdecken & Laden →',
    ctaCloud: 'In der Cloud öffnen →',
    submitTitle: 'App vorschlagen',
    submitDesc: 'Fügen Sie einen GitHub-Link ein, um eine verständliche Anleitung auf HubHum zu erstellen',
    submitPlaceholder: 'https://github.com/autor/app-name',
    submitBtn: 'Absenden',
    submitSuccess: 'Die App wird verarbeitet und ist in etwa 2 Minuten online.',
    submitInvalidUrl: 'Bitte geben Sie eine gültige URL im Format https://github.com/autor/app-name ein.',
    submitConfirmLink: 'Einsendung bestätigen →',
    backAllApps: '← Zurück zur Übersicht',
    saveFavorite: 'Als Favorit speichern',
    savedFavorite: 'Als Favorit gespeichert',
    partnerTipBadge: 'Empfehlung (#ad)',
    partnerHeadingPrefix: 'Empfohlen:',
    partnerFallbackHeading: 'Einrichtung erweitern',
    partnerFallbackDesc: 'Passende Partnerlösung für diese Softwarekategorie.',
    partnerCloudBtn: 'In der Cloud öffnen (1-Klick)',
    partnerDiscoverPrefix: 'Entdecken:',
    detailsHeading: 'Kurzinfos',
    detailCategory: 'Kategorie:',
    detailMode: 'Format:',
    detailModeCloud: 'Läuft im Browser / in der Cloud',
    detailModeDesktop: 'Installation auf Ihrem Gerät',
    detailLicense: 'Lizenz:',
    detailOfficialPage: 'Offizielle Seite:',
    detailOpenSource: 'Quelle öffnen',
    reviewTitlePrefix: 'Schon ausprobiert:',
    reviewDesc: 'Helfen Sie anderen Nutzern mit einer kurzen Bewertung.',
    reviewBtn: 'Bewertung schreiben',
    disclosureTitle: 'Affiliate-Hinweis (#ad):',
    disclosureBody:
      'Einige Links auf dieser Seite sind Affiliate-Links. Bei einer Buchung erhalten wir ggf. eine Provision ohne Mehrkosten für Sie.',
    footerAffiliate:
      'Affiliate-Hinweis (#ad): Einige Links auf HubHum sind Partnerlinks. Bei einem Kauf erhalten wir ggf. eine Provision ohne Aufpreis.',
    footerCredits:
      'Alle Programme verweisen direkt auf die offiziellen Kanäle der Entwickler gemäß Open-Source-Lizenz.',
    dialogTitle: 'Ihre gespeicherten Favoriten',
    dialogDescLocal: 'Ihre Favoriten werden direkt in diesem Browser gespeichert.',
    dialogDescAuth: 'Mit GitHub verbunden. Verwalten Sie Ihre Favoriten unten.',
    dialogNoFavs: 'Sie haben noch keine Favoriten gespeichert.',
    dialogClose: 'Schließen',
    dialogLogout: 'Trennen',
    detailSummaryNotice: 'Verständliche Zusammenfassung:',
    syncOptionalTitle: 'Optional: GitHub-Synchronisierung',
    syncOptionalDesc:
      'Möchten Sie Favoriten geräteübergreifend synchronisieren? Geben Sie ein GitHub Personal Token ein oder verbinden Sie Ihr Konto.',
    syncTokenPlaceholder: 'GitHub Personal Token (optional)',
    syncConnectBtn: 'Verbinden',
    syncSuccess: 'Verbunden als',
    syncInvalidToken: 'Token konnte nicht geprüft werden. Lokale Favoriten bleiben gespeichert.',
  },
};

export const CATEGORY_I18N_KEY: Record<string, keyof TranslationDict> = {
  All: 'catAll',
  Productivity: 'catProductivity',
  'Security & Privacy': 'catSecurity',
  'Graphics & Design': 'catGraphics',
  'Video & Audio': 'catVideo',
  'Web Apps & Cloud': 'catWebApps',
  'Websites & SEO': 'catWebsites',
};
