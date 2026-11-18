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
  deviceFlowTitle: string;
  deviceFlowInstruction: string;
  deviceFlowOpenBtn: string;
  deviceFlowPolling: string;
  deviceFlowCopy: string;
  deviceFlowCopied: string;
  deviceFlowSuccess: string;
  deviceFlowBlocked: string;
  deviceFlowTokenPlaceholder: string;
  deviceFlowTokenBtn: string;
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
      'Your favorite apps are saved instantly in your browser. Click any saved app below to open its guide.',
    dialogDescAuth: 'Signed in with GitHub. Manage your saved favorites below.',
    dialogNoFavs: 'You have not saved any favorite apps yet. Click the heart button on any app card!',
    dialogClose: 'Close',
    dialogLogout: 'Sign Out',
    detailSummaryNotice: 'Plain-language summary in your language:',
    deviceFlowTitle: 'Sign in with GitHub',
    deviceFlowInstruction: 'Copy this code and enter it on GitHub to authorize your account:',
    deviceFlowOpenBtn: 'Open github.com/login/device →',
    deviceFlowPolling: 'Waiting for authorization on GitHub...',
    deviceFlowCopy: 'Copy',
    deviceFlowCopied: 'Copied!',
    deviceFlowSuccess: 'Signed in as',
    deviceFlowBlocked: 'Browser blocked direct cross-origin code request. Paste a read:user token or manage local favorites below.',
    deviceFlowTokenPlaceholder: 'Paste GitHub read:user token (optional)',
    deviceFlowTokenBtn: 'Connect',
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
    dialogTitle: 'I tuoi Preferiti Salvati',
    dialogDescLocal:
      'Le tue app preferite vengono salvate istantaneamente nel browser. Clicca su una scheda per aprirla.',
    dialogDescAuth: 'Accesso effettuato con GitHub. Gestisci i tuoi preferiti salvati qui sotto.',
    dialogNoFavs: 'Non hai ancora salvato nessuna app. Premi il cuore su una qualsiasi scheda!',
    dialogClose: 'Chiudi',
    dialogLogout: 'Esci',
    detailSummaryNotice: 'Sintesi chiara nella tua lingua:',
    deviceFlowTitle: 'Accedi con GitHub',
    deviceFlowInstruction: 'Copia questo codice e inseriscilo su GitHub per autorizzare il tuo account:',
    deviceFlowOpenBtn: 'Apri github.com/login/device →',
    deviceFlowPolling: 'In attesa di autorizzazione su GitHub...',
    deviceFlowCopy: 'Copia',
    deviceFlowCopied: 'Copiato!',
    deviceFlowSuccess: 'Accesso effettuato come',
    deviceFlowBlocked: 'Il browser ha bloccato la richiesta diretta cross-origin. Inserisci un token read:user o usa i preferiti locali qui sotto.',
    deviceFlowTokenPlaceholder: 'Incolla token GitHub read:user (opzionale)',
    deviceFlowTokenBtn: 'Collega',
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
    dialogDescLocal:
      'Tus aplicaciones favoritas se guardan al instante en tu navegador.',
    dialogDescAuth: 'Sesión iniciada con GitHub. Administra tus favoritos abajo.',
    dialogNoFavs: 'Aún no has guardado aplicaciones favoritas.',
    dialogClose: 'Cerrar',
    dialogLogout: 'Cerrar sesión',
    detailSummaryNotice: 'Resumen claro en tu idioma:',
    deviceFlowTitle: 'Iniciar sesión con GitHub',
    deviceFlowInstruction: 'Copia este código e introdúcelo en GitHub para autorizar tu cuenta:',
    deviceFlowOpenBtn: 'Abrir github.com/login/device →',
    deviceFlowPolling: 'Esperando autorización en GitHub...',
    deviceFlowCopy: 'Copiar',
    deviceFlowCopied: '¡Copiado!',
    deviceFlowSuccess: 'Sesión iniciada como',
    deviceFlowBlocked: 'El navegador bloqueó la solicitud directa. Pega un token read:user o usa tus favoritos locales.',
    deviceFlowTokenPlaceholder: 'Pega tu token GitHub read:user (opcional)',
    deviceFlowTokenBtn: 'Conectar',
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
    dialogDescLocal:
      'Vos applications favorites sont enregistrées instantanément dans votre navigateur.',
    dialogDescAuth: 'Connecté via GitHub. Gérez vos favoris ci-dessous.',
    dialogNoFavs: "Vous n'avez pas encore enregistré de favoris.",
    dialogClose: 'Fermer',
    dialogLogout: 'Déconnexion',
    detailSummaryNotice: 'Résumé clair dans votre langue :',
    deviceFlowTitle: 'Connexion avec GitHub',
    deviceFlowInstruction: 'Copiez ce code et saisissez-le sur GitHub pour autoriser votre compte :',
    deviceFlowOpenBtn: 'Ouvrir github.com/login/device →',
    deviceFlowPolling: "En attente d'autorisation sur GitHub...",
    deviceFlowCopy: 'Copier',
    deviceFlowCopied: 'Copié !',
    deviceFlowSuccess: 'Connecté en tant que',
    deviceFlowBlocked: 'Le navigateur a bloqué la requête directe. Collez un jeton read:user ou gérez vos favoris locaux.',
    deviceFlowTokenPlaceholder: 'Collez un jeton GitHub read:user (optionnel)',
    deviceFlowTokenBtn: 'Connecter',
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
    dialogDescLocal: 'Ihre Favoriten werden direkt im Browser gespeichert.',
    dialogDescAuth: 'Mit GitHub angemeldet. Verwalten Sie Ihre Favoriten unten.',
    dialogNoFavs: 'Sie haben noch keine Favoriten gespeichert.',
    dialogClose: 'Schließen',
    dialogLogout: 'Abmelden',
    detailSummaryNotice: 'Verständliche Zusammenfassung:',
    deviceFlowTitle: 'Mit GitHub anmelden',
    deviceFlowInstruction: 'Kopieren Sie diesen Code und geben Sie ihn auf GitHub ein, um Ihr Konto zu autorisieren:',
    deviceFlowOpenBtn: 'github.com/login/device öffnen →',
    deviceFlowPolling: 'Warte auf Bestätigung bei GitHub...',
    deviceFlowCopy: 'Kopieren',
    deviceFlowCopied: 'Kopiert!',
    deviceFlowSuccess: 'Angemeldet als',
    deviceFlowBlocked: 'Der Browser hat die direkte Anfrage blockiert. Token (read:user) einfügen oder lokale Favoriten nutzen.',
    deviceFlowTokenPlaceholder: 'GitHub read:user Token einfügen (optional)',
    deviceFlowTokenBtn: 'Verbinden',
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
