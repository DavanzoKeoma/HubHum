/**
 * HubHum Chrome Extension — Popup Controller.
 * Detects current tab repo, checks HubHum catalog-index.json via background worker,
 * triggers 1-click conversion, and mirrors real-time background progress.
 */

const HUBHUM_HOME = 'https://davanzokeoma.github.io/HubHum/';
const STORAGE_KEY = 'hubhum_conversions_v1';

const el = {
  repoCard: document.getElementById('repo-card'),
  repoAvatar: document.getElementById('repo-avatar'),
  repoFullname: document.getElementById('repo-fullname'),
  repoStars: document.getElementById('repo-stars'),
  repoLang: document.getElementById('repo-lang'),
  stateLoading: document.getElementById('state-loading'),
  stateOutside: document.getElementById('state-outside'),
  stateExists: document.getElementById('state-exists'),
  stateConvert: document.getElementById('state-convert'),
  stateProgress: document.getElementById('state-progress'),
  existsDesc: document.getElementById('exists-desc'),
  repoDescription: document.getElementById('repo-description'),
  progressPct: document.getElementById('progress-pct'),
  progressBar: document.getElementById('progress-bar'),
  progressFill: document.getElementById('progress-fill'),
  progressStage: document.getElementById('progress-stage'),
  progressHint: document.getElementById('progress-hint'),
  btnOpenCatalog: document.getElementById('btn-open-catalog'),
  btnOpenGuide: document.getElementById('btn-open-guide'),
  btnHumanize: document.getElementById('btn-humanize'),
  btnProgressOpen: document.getElementById('btn-progress-open'),
  btnProgressRetry: document.getElementById('btn-progress-retry'),
};

let activeRepo = null;
let activeGuideUrl = null;

function showPanel(panelName) {
  [
    el.stateLoading,
    el.stateOutside,
    el.stateExists,
    el.stateConvert,
    el.stateProgress,
  ].forEach((node) => node?.classList.add('hidden'));

  const targetMap = {
    loading: el.stateLoading,
    outside: el.stateOutside,
    exists: el.stateExists,
    convert: el.stateConvert,
    progress: el.stateProgress,
  };
  targetMap[panelName]?.classList.remove('hidden');
}

function formatStars(count) {
  if (!Number.isFinite(count) || count <= 0) return '★ —';
  if (count >= 1000) return `★ ${(count / 1000).toFixed(1)}k`;
  return `★ ${count}`;
}

async function hydrateGitHubMeta(owner, repo) {
  if (el.repoAvatar) {
    el.repoAvatar.src = `https://github.com/${encodeURIComponent(owner)}.png?size=80`;
  }
  try {
    const res = await fetch(
      `https://api.github.com/repos/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}`,
      { headers: { Accept: 'application/vnd.github+json' } }
    );
    if (!res.ok) return;
    const data = await res.json();
    if (el.repoStars) {
      el.repoStars.textContent = formatStars(Number(data.stargazers_count || 0));
    }
    if (el.repoLang && data.language) {
      el.repoLang.textContent = data.language;
      el.repoLang.classList.remove('hidden');
    }
    if (el.repoAvatar && data.owner?.avatar_url) {
      el.repoAvatar.src = `${data.owner.avatar_url}&s=80`;
    }
    if (el.repoDescription && data.description) {
      el.repoDescription.textContent = data.description;
    }
  } catch {
    // Public rate-limit safe fallback already populated above
  }
}

function renderProgressState(convState) {
  if (!convState) return;
  showPanel('progress');

  const pct = Math.max(10, Math.min(100, Number(convState.progress || 15)));
  if (el.progressPct) el.progressPct.textContent = `${pct}%`;
  if (el.progressBar) el.progressBar.setAttribute('aria-valuenow', String(pct));
  if (el.progressFill) el.progressFill.style.width = `${pct}%`;
  if (el.progressStage) el.progressStage.textContent = convState.stage || 'Elaborazione...';

  if (convState.status === 'ready') {
    activeGuideUrl = convState.guideUrl || activeGuideUrl;
    el.progressHint?.classList.add('hidden');
    el.btnProgressRetry?.classList.add('hidden');
    el.btnProgressOpen?.classList.remove('hidden');
  } else if (convState.status === 'error' || convState.status === 'timeout') {
    el.progressHint?.classList.add('hidden');
    el.btnProgressOpen?.classList.add('hidden');
    el.btnProgressRetry?.classList.remove('hidden');
  } else {
    el.progressHint?.classList.remove('hidden');
    el.btnProgressOpen?.classList.add('hidden');
    el.btnProgressRetry?.classList.add('hidden');
  }
}

async function triggerConversion() {
  if (!activeRepo) return;
  renderProgressState({
    status: 'converting',
    progress: 10,
    stage: '10%: Invio richiesta a HubHum AI...',
  });

  try {
    const resp = await chrome.runtime.sendMessage({
      type: 'open_conversion',
      repoUrl: activeRepo.repoUrl,
      autoOpenTab: true,
    });
    if (resp?.conversion) {
      renderProgressState(resp.conversion);
    } else {
      renderProgressState({
        status: 'error',
        progress: 0,
        stage: resp?.error || 'Impossibile avviare la conversione.',
      });
    }
  } catch (err) {
    renderProgressState({
      status: 'error',
      progress: 0,
      stage: String(err?.message || 'Errore di comunicazione con il background worker.'),
    });
  }
}

async function initPopup() {
  showPanel('loading');

  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  const activeTab = tabs[0];
  const tabUrl = activeTab?.url || '';

  const statusResp = await chrome.runtime.sendMessage({
    type: 'check_status',
    repoUrl: tabUrl,
  });

  if (!statusResp?.ok || !statusResp.isRepo) {
    el.repoCard?.classList.add('hidden');
    showPanel('outside');
    return;
  }

  activeRepo = statusResp.repo;
  activeGuideUrl = statusResp.guideUrl;

  if (el.repoCard) el.repoCard.classList.remove('hidden');
  if (el.repoFullname) el.repoFullname.textContent = activeRepo.fullName;
  hydrateGitHubMeta(activeRepo.owner, activeRepo.repo);

  if (statusResp.conversion?.status === 'converting') {
    renderProgressState(statusResp.conversion);
    return;
  }

  if (statusResp.inCatalog || statusResp.conversion?.status === 'ready') {
    if (statusResp.catalogEntry?.name && el.existsDesc) {
      el.existsDesc.textContent = `${statusResp.catalogEntry.name} (${statusResp.catalogEntry.category || 'App'}) è già pronto nel catalogo con guida in linguaggio semplice e link ufficiali.`;
    }
    showPanel('exists');
    return;
  }

  showPanel('convert');
}

chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName !== 'local' || !changes[STORAGE_KEY] || !activeRepo) return;
  const map = changes[STORAGE_KEY].newValue || {};
  const nextState = map[activeRepo.slug];
  if (nextState) {
    renderProgressState(nextState);
  }
});

el.btnOpenCatalog?.addEventListener('click', () => {
  chrome.tabs.create({ url: HUBHUM_HOME });
});

el.btnOpenGuide?.addEventListener('click', () => {
  if (activeGuideUrl) {
    chrome.tabs.create({ url: activeGuideUrl });
  }
});

el.btnHumanize?.addEventListener('click', triggerConversion);
el.btnProgressRetry?.addEventListener('click', triggerConversion);

el.btnProgressOpen?.addEventListener('click', () => {
  if (activeGuideUrl) {
    chrome.tabs.create({ url: activeGuideUrl });
  }
});

document.addEventListener('DOMContentLoaded', initPopup);
