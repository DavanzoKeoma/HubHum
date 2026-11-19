/**
 * HubHum Chrome Extension (Manifest V3) — Background Service Worker.
 * Tracks valid GitHub repository tabs, handles catalog status lookups,
 * dispatches conversions via the Cloudflare Worker, polls until GitHub Pages
 * is live, fires native desktop notifications, and opens ready guides.
 */

const HUBHUM_SITE = 'https://davanzokeoma.github.io/HubHum';
const CATALOG_INDEX_URL = `${HUBHUM_SITE}/catalog-index.json`;
const WORKER_CONVERT_URL = 'https://hubhum-api-bridge.keomadavanzo.workers.dev/api/convert';
const STORAGE_KEY = 'hubhum_conversions_v1';
const NOTIFICATION_PREFIX = 'hubhum-ready-';

const RESERVED_OWNERS = new Set([
  'settings',
  'explore',
  'trending',
  'notifications',
  'marketplace',
  'pulls',
  'issues',
  'codespaces',
  'sponsors',
  'orgs',
  'organizations',
  'users',
  'login',
  'signup',
  'search',
  'new',
  'features',
  'pricing',
  'enterprise',
  'topics',
  'collections',
  'events',
  'security',
  'about',
  'contact',
  'apps',
  'blog',
  'docs',
  'join',
  'account',
  'stars',
  'watching',
]);

const activePollers = new Set();

function slugifyRepoName(repoName) {
  return String(repoName || '')
    .toLowerCase()
    .replace(/[^a-z0-9-]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function parseGitHubRepoUrl(rawUrl) {
  if (!rawUrl || typeof rawUrl !== 'string') return null;
  const withoutHashOrQuery = rawUrl.split('#')[0].split('?')[0];
  const match = withoutHashOrQuery.match(
    /^https:\/\/github\.com\/([a-zA-Z0-9_.-]+)\/([a-zA-Z0-9_.-]+)(\/)?$/
  );
  if (!match) return null;

  const owner = match[1];
  const repo = match[2].replace(/\.git$/i, '');
  if (RESERVED_OWNERS.has(owner.toLowerCase())) return null;

  return {
    owner,
    repo,
    fullName: `${owner}/${repo}`,
    fullNameLower: `${owner}/${repo}`.toLowerCase(),
    repoUrl: `https://github.com/${owner}/${repo}`,
    slug: slugifyRepoName(repo),
  };
}

async function updateBadgeForTab(tabId, url) {
  if (!tabId || tabId < 0) return;
  const parsed = parseGitHubRepoUrl(url);
  try {
    if (parsed) {
      await chrome.action.setBadgeText({ text: 'HUM', tabId });
      await chrome.action.setBadgeBackgroundColor({ color: '#7c3aed', tabId });
    } else {
      await chrome.action.setBadgeText({ text: '', tabId });
    }
  } catch {
    // Tab might close concurrently
  }
}

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.url || changeInfo.status === 'complete') {
    updateBadgeForTab(tabId, changeInfo.url || tab.url || '');
  }
});

chrome.tabs.onActivated.addListener(async ({ tabId }) => {
  try {
    const tab = await chrome.tabs.get(tabId);
    await updateBadgeForTab(tabId, tab.url || '');
  } catch {
    // Ignore transient tab errors
  }
});

chrome.notifications.onClicked.addListener((notificationId) => {
  if (!notificationId || !notificationId.startsWith(NOTIFICATION_PREFIX)) return;
  const slug = notificationId.slice(NOTIFICATION_PREFIX.length);
  const guideUrl = `${HUBHUM_SITE}/apps/${slug}/`;
  chrome.tabs.create({ url: guideUrl });
  chrome.notifications.clear(notificationId);
});

async function getConversionsMap() {
  const res = await chrome.storage.local.get(STORAGE_KEY);
  return res[STORAGE_KEY] && typeof res[STORAGE_KEY] === 'object' ? res[STORAGE_KEY] : {};
}

async function saveConversionState(slug, patch) {
  const map = await getConversionsMap();
  const prev = map[slug] || {};
  map[slug] = { ...prev, ...patch, slug, updatedAt: Date.now() };
  await chrome.storage.local.set({ [STORAGE_KEY]: map });
  return map[slug];
}

async function fetchCatalogMatch(parsed) {
  const res = await fetch(`${CATALOG_INDEX_URL}?t=${Date.now()}`, { cache: 'no-store' });
  if (!res.ok) return null;
  const items = await res.json();
  if (!Array.isArray(items)) return null;

  return (
    items.find(
      (item) =>
        String(item.full_name || '').toLowerCase() === parsed.fullNameLower ||
        String(item.repo_url || '').toLowerCase() === parsed.repoUrl.toLowerCase() ||
        String(item.slug || '').toLowerCase() === parsed.slug
    ) || null
  );
}

function progressForElapsed(elapsedMs) {
  if (elapsedMs >= 45000) {
    return { progress: 90, stage: '90%: Pubblicazione statica nel catalogo...' };
  }
  if (elapsedMs >= 28000) {
    return { progress: 75, stage: '75%: Iniezione raccomandazioni e link ufficiali...' };
  }
  if (elapsedMs >= 12000) {
    return { progress: 45, stage: '45%: Elaborazione guida senza gergo tecnico...' };
  }
  return { progress: 15, stage: '15%: Analisi README e ultime release...' };
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function pollGuideReady(slug, parsed, autoOpenTab) {
  if (activePollers.has(slug)) return;
  activePollers.add(slug);

  const guideUrl = `${HUBHUM_SITE}/apps/${slug}/`;
  const startedAt = Date.now();
  const maxWaitMs = 180000;

  try {
    while (Date.now() - startedAt <= maxWaitMs) {
      await sleep(4000);
      const elapsed = Date.now() - startedAt;
      const stagePatch = progressForElapsed(elapsed);

      try {
        const headRes = await fetch(`${guideUrl}?_=${Date.now()}`, {
          method: 'HEAD',
          cache: 'no-store',
        });

        if (headRes.ok) {
          await saveConversionState(slug, {
            status: 'ready',
            progress: 100,
            stage: '100%: Guida pubblicata su HubHum!',
            guideUrl,
            repoUrl: parsed.repoUrl,
            fullName: parsed.fullName,
          });

          try {
            await chrome.notifications.create(`${NOTIFICATION_PREFIX}${slug}`, {
              type: 'basic',
              iconUrl: chrome.runtime.getURL('icons/icon-128.png'),
              title: 'HubHum – Guida pronta!',
              message: `${parsed.repo} è ora disponibile in linguaggio semplice. Clicca per aprirla.`,
              priority: 2,
            });
          } catch {
            // Notification permissions may vary
          }

          if (autoOpenTab) {
            chrome.tabs.create({ url: guideUrl });
          }
          return;
        }
      } catch {
        // Keep polling every 4 seconds while GitHub Actions builds & deploys
      }

      await saveConversionState(slug, {
        status: 'converting',
        ...stagePatch,
        guideUrl,
        repoUrl: parsed.repoUrl,
        fullName: parsed.fullName,
      });
    }

    await saveConversionState(slug, {
      status: 'timeout',
      progress: 95,
      stage: 'La pubblicazione richiede più tempo del previsto. Riprova tra poco.',
      guideUrl,
      repoUrl: parsed.repoUrl,
      fullName: parsed.fullName,
    });
  } finally {
    activePollers.delete(slug);
  }
}

async function startConversion(repoUrl, autoOpenTab = true) {
  const parsed = parseGitHubRepoUrl(repoUrl);
  if (!parsed) {
    throw new Error('URL repository GitHub non valido.');
  }

  const existing = await getConversionsMap();
  const current = existing[parsed.slug];
  if (current?.status === 'converting' && Date.now() - (current.updatedAt || 0) < 180000) {
    pollGuideReady(parsed.slug, parsed, autoOpenTab);
    return current;
  }

  await saveConversionState(parsed.slug, {
    status: 'converting',
    progress: 10,
    stage: '10%: Invio richiesta a HubHum AI...',
    repoUrl: parsed.repoUrl,
    fullName: parsed.fullName,
    guideUrl: `${HUBHUM_SITE}/apps/${parsed.slug}/`,
  });

  const apiRes = await fetch(WORKER_CONVERT_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify({ repo_url: parsed.repoUrl }),
  });

  if (!apiRes.ok) {
    const errPayload = await apiRes.text();
    const errState = await saveConversionState(parsed.slug, {
      status: 'error',
      progress: 0,
      stage: `Errore avvio conversione (${apiRes.status}): ${errPayload.slice(0, 80)}`,
      repoUrl: parsed.repoUrl,
      fullName: parsed.fullName,
    });
    return errState;
  }

  const apiJson = await apiRes.json();
  const resolvedSlug = slugifyRepoName(apiJson?.slug || parsed.slug);
  const guideUrl = `${HUBHUM_SITE}/apps/${resolvedSlug}/`;

  const queuedState = await saveConversionState(resolvedSlug, {
    status: 'converting',
    progress: 15,
    stage: '15%: Analisi README e ultime release...',
    repoUrl: parsed.repoUrl,
    fullName: parsed.fullName,
    guideUrl,
  });

  pollGuideReady(resolvedSlug, parsed, autoOpenTab);
  return queuedState;
}

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  (async () => {
    try {
      if (message?.type === 'check_status') {
        const parsed = parseGitHubRepoUrl(message.repoUrl || '');
        if (!parsed) {
          sendResponse({ ok: true, isRepo: false });
          return;
        }
        const [catalogEntry, convMap] = await Promise.all([
          fetchCatalogMatch(parsed).catch(() => null),
          getConversionsMap(),
        ]);
        const conversion = convMap[parsed.slug] || null;
        if (conversion?.status === 'converting' && !activePollers.has(parsed.slug)) {
          pollGuideReady(parsed.slug, parsed, true);
        }
        sendResponse({
          ok: true,
          isRepo: true,
          repo: parsed,
          inCatalog: Boolean(catalogEntry),
          catalogEntry,
          conversion,
          guideUrl: `${HUBHUM_SITE}/apps/${catalogEntry?.slug || parsed.slug}/`,
        });
        return;
      }

      if (message?.type === 'open_conversion') {
        const state = await startConversion(
          message.repoUrl || '',
          message.autoOpenTab !== false
        );
        sendResponse({ ok: true, conversion: state });
        return;
      }

      if (message?.type === 'open_tab' && message.url) {
        await chrome.tabs.create({ url: message.url });
        sendResponse({ ok: true });
        return;
      }

      sendResponse({ ok: false, error: 'Unknown message type' });
    } catch (err) {
      sendResponse({ ok: false, error: String(err?.message || err) });
    }
  })();

  return true;
});
