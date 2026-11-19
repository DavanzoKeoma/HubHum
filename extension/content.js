/**
 * HubHum Chrome Extension — GitHub Repository Content Script.
 * Injects the discreet "⚡ Humanize with HubHum" action button next to
 * GitHub's native Watch / Fork / Star controls and mirrors live conversion status.
 */

(() => {
  const BUTTON_ID = 'hubhum-humanize-btn';
  const ITEM_ID = 'hubhum-humanize-item';
  const STORAGE_KEY = 'hubhum_conversions_v1';

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
  ]);

  let currentRepoInfo = null;
  let currentGuideUrl = null;
  let observerTimer = null;

  function parseCurrentRepo() {
    const cleanUrl = window.location.href.split('#')[0].split('?')[0];
    const match = cleanUrl.match(
      /^https:\/\/github\.com\/([a-zA-Z0-9_.-]+)\/([a-zA-Z0-9_.-]+)(\/)?$/
    );
    if (!match) return null;
    const owner = match[1];
    const repo = match[2].replace(/\.git$/i, '');
    if (RESERVED_OWNERS.has(owner.toLowerCase())) return null;
    return {
      owner,
      repo,
      repoUrl: `https://github.com/${owner}/${repo}`,
      slug: repo.toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/^-+|-+$/g, ''),
    };
  }

  function boltSvg() {
    return (
      '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">' +
      '<path d="M13 2L4.09 12.69A1 1 0 0 0 4.86 14.3H11l-1 7.7 8.91-10.69A1 1 0 0 0 18.14 9.7H12l1-7.7z"/>' +
      '</svg>'
    );
  }

  function applyButtonState(btn, state, guideUrl) {
    if (!btn) return;
    btn.classList.remove('is-converting', 'is-ready');
    btn.disabled = false;

    if (state?.status === 'ready' || guideUrl) {
      const targetUrl = state?.guideUrl || guideUrl;
      btn.classList.add('is-ready');
      btn.dataset.guideUrl = targetUrl;
      btn.innerHTML = `${boltSvg()}<span>Open HubHum Guide →</span>`;
      btn.title = 'Questa app è già tradotta su HubHum: apri la guida';
      return;
    }

    if (state?.status === 'converting') {
      btn.classList.add('is-converting');
      btn.disabled = true;
      btn.removeAttribute('data-guide-url');
      btn.innerHTML = `${boltSvg()}<span>Converting with AI... (${state.progress || 15}%)</span>`;
      btn.title = state.stage || 'Conversione in corso su HubHum...';
      return;
    }

    btn.removeAttribute('data-guide-url');
    btn.innerHTML = `${boltSvg()}<span>⚡ Humanize with HubHum</span>`;
    btn.title = 'Traduci questo repository in una guida semplice su HubHum';
  }

  function findActionsList() {
    return (
      document.querySelector('#repository-details-container ul.pagehead-actions') ||
      document.querySelector('ul.pagehead-actions') ||
      document.querySelector('#repository-container-header .d-flex ul')
    );
  }

  async function refreshStatusForRepo(repoInfo) {
    const btn = document.getElementById(BUTTON_ID);
    if (!btn || !repoInfo) return;

    try {
      const resp = await chrome.runtime.sendMessage({
        type: 'check_status',
        repoUrl: repoInfo.repoUrl,
      });
      if (!resp?.ok) return;
      currentGuideUrl = resp.inCatalog ? resp.guideUrl : null;
      applyButtonState(btn, resp.conversion, currentGuideUrl);
    } catch {
      // Service worker may reload silently
    }
  }

  function injectButton() {
    const repoInfo = parseCurrentRepo();
    const existingItem = document.getElementById(ITEM_ID);

    if (!repoInfo) {
      if (existingItem) existingItem.remove();
      currentRepoInfo = null;
      return;
    }

    const actionsList = findActionsList();
    if (!actionsList) return;

    const alreadySameRepo =
      existingItem && currentRepoInfo?.repoUrl === repoInfo.repoUrl;
    if (alreadySameRepo) return;

    if (existingItem) existingItem.remove();
    currentRepoInfo = repoInfo;
    currentGuideUrl = null;

    const li = document.createElement('li');
    li.id = ITEM_ID;
    li.className = 'hubhum-actions-item';

    const btn = document.createElement('button');
    btn.id = BUTTON_ID;
    btn.type = 'button';
    btn.className = 'hubhum-humanize-btn';
    applyButtonState(btn, null, null);

    btn.addEventListener('click', async () => {
      const readyUrl = btn.dataset.guideUrl;
      if (readyUrl) {
        chrome.runtime.sendMessage({ type: 'open_tab', url: readyUrl });
        return;
      }

      applyButtonState(btn, { status: 'converting', progress: 10 }, null);
      try {
        const res = await chrome.runtime.sendMessage({
          type: 'open_conversion',
          repoUrl: repoInfo.repoUrl,
          autoOpenTab: true,
        });
        if (res?.conversion) {
          applyButtonState(btn, res.conversion, null);
        }
      } catch {
        applyButtonState(btn, null, null);
      }
    });

    li.appendChild(btn);
    actionsList.prepend(li);
    refreshStatusForRepo(repoInfo);
  }

  chrome.storage.onChanged.addListener((changes, areaName) => {
    if (areaName !== 'local' || !changes[STORAGE_KEY] || !currentRepoInfo) return;
    const map = changes[STORAGE_KEY].newValue || {};
    const state = map[currentRepoInfo.slug];
    if (state) {
      const btn = document.getElementById(BUTTON_ID);
      applyButtonState(btn, state, currentGuideUrl);
    }
  });

  // Initial injection + GitHub Turbo SPA navigation support
  injectButton();
  document.addEventListener('turbo:load', injectButton);
  document.addEventListener('pjax:end', injectButton);

  const observer = new MutationObserver(() => {
    if (observerTimer) clearTimeout(observerTimer);
    observerTimer = setTimeout(injectButton, 250);
  });
  if (document.body) {
    observer.observe(document.body, { childList: true, subtree: true });
  }
})();
