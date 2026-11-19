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
  convPollingHint: string;
  convErrorMsg: string;
  convTimeoutMsg: string;
  convRetryBtn: string;
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
  oauthSignInBtn: string;
  oauthSignInDesc: string;
  oauthConnecting: string;
}

export const TRANSLATIONS: Record<SupportedLang, TranslationDict> = {
  en: {
    brandSub: 'Free software for humans',
    navTopPicks: 'Top Picks',
    navSubmit: 'Submit an App',
    navSignIn: 'Sign In',
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
    submitSuccess: 'Your app is being processed and will be live shortly.',
    submitInvalidUrl: 'Please enter a valid URL formatted as https://github.com/author/app-name.',
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
      'Your favorite apps are saved right here in this browser.',
    dialogDescAuth: 'Signed in with GitHub. Manage your saved favorites below.',
    dialogNoFavs: 'You have not saved any favorite apps yet. Click the heart button on any app page!',
    dialogClose: 'Close',
    dialogLogout: 'Sign Out',
    detailSummaryNotice: 'Plain-language summary in your language:',
    oauthSignInBtn: 'Sign in with GitHub',
    oauthSignInDesc: 'Sign in with one click to link your GitHub profile and sync favorites.',
    oauthConnecting: 'Connecting your GitHub account...',
  },
  it: {
    brandSub: 'App libere per tutti',
    navTopPicks: 'Top della settimana',
    navSubmit: "Proponi un'app",
    navSignIn: 'Accedi',
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
    submitSuccess: "L'app è in elaborazione e sarà online tra poco.",
    submitInvalidUrl: 'Inserisci un indirizzo valido nel formato https://github.com/autore/nome-app.',
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
    dialogDescLocal: 'Le tue app preferite sono salvate qui nel tuo browser.',
    dialogDescAuth: 'Accesso effettuato con GitHub. Gestisci i tuoi preferiti qui sotto.',
    dialogNoFavs: 'Non hai ancora salvato nessuna app. Premi il cuore su una qualsiasi scheda!',
    dialogClose: 'Chiudi',
    dialogLogout: 'Esci',
    detailSummaryNotice: 'Sintesi chiara nella tua lingua:',
    oauthSignInBtn: 'Accedi con GitHub',
    oauthSignInDesc: 'Accedi in 1 click per collegare il tuo profilo GitHub ai tuoi preferiti.',
    oauthConnecting: 'Collegamento account GitHub in corso...',
  },
  es: {
    brandSub: 'Software libre para todos',
    navTopPicks: 'Destacados',
    navSubmit: 'Enviar una app',
    navSignIn: 'Iniciar sesión',
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
    submitSuccess: 'Tu aplicación se está procesando y estará en línea en breve.',
    submitInvalidUrl: 'Introduce un enlace válido con el formato https://github.com/autor/nombre-app.',
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
    dialogDescAuth: 'Sesión iniciada con GitHub. Administra tus favoritos abajo.',
    dialogNoFavs: 'Aún no has guardado aplicaciones favoritas.',
    dialogClose: 'Cerrar',
    dialogLogout: 'Cerrar sesión',
    detailSummaryNotice: 'Resumen claro en tu idioma:',
    oauthSignInBtn: 'Iniciar sesión con GitHub',
    oauthSignInDesc: 'Inicia sesión en 1 clic para conectar tu cuenta de GitHub y tus favoritos.',
    oauthConnecting: 'Conectando tu cuenta de GitHub...',
  },
  fr: {
    brandSub: 'Logiciels libres pour tous',
    navTopPicks: 'Sélection',
    navSubmit: 'Proposer une app',
    navSignIn: 'Connexion',
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
    submitSuccess: "L'application est en cours de traitement et sera en ligne très bientôt.",
    submitInvalidUrl: 'Veuillez saisir un lien valide au format https://github.com/auteur/nom-app.',
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
    dialogDescAuth: 'Connecté avec GitHub. Gérez vos favoris ci-dessous.',
    dialogNoFavs: "Vous n'avez pas encore enregistré de favoris.",
    dialogClose: 'Fermer',
    dialogLogout: 'Déconnexion',
    detailSummaryNotice: 'Résumé clair dans votre langue :',
    oauthSignInBtn: 'Se connecter avec GitHub',
    oauthSignInDesc: 'Connectez-vous en 1 clic pour associer votre compte GitHub et vos favoris.',
    oauthConnecting: 'Connexion à GitHub en cours...',
  },
  de: {
    brandSub: 'Freie Software für alle',
    navTopPicks: 'Top-Auswahl',
    navSubmit: 'App vorschlagen',
    navSignIn: 'Anmelden',
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
    submitSuccess: 'Die App wird verarbeitet und ist in Kürze online.',
    submitInvalidUrl: 'Bitte geben Sie eine gültige URL im Format https://github.com/autor/app-name ein.',
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
    dialogDescAuth: 'Mit GitHub angemeldet. Verwalten Sie Ihre Favoriten unten.',
    dialogNoFavs: 'Sie haben noch keine Favoriten gespeichert.',
    dialogClose: 'Schließen',
    dialogLogout: 'Abmelden',
    detailSummaryNotice: 'Verständliche Zusammenfassung:',
    oauthSignInBtn: 'Mit GitHub anmelden',
    oauthSignInDesc: 'Melden Sie sich mit 1 Klick an, um Ihr GitHub-Konto zu verbinden.',
    oauthConnecting: 'GitHub-Konto wird verbunden...',
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
