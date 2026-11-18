/**
 * Local-First Favorites & Zero-Friction GitHub Integration for HubHum.
 * Zero CORS errors: uses only CORS-enabled GitHub REST API endpoints (`api.github.com`)
 * and instant browser localStorage persistence.
 */

export interface GitHubUserSession {
  login: string;
  avatarUrl: string;
  accessToken?: string;
  authenticatedAt: string;
}

export interface TranslationDispatchResult {
  accepted: boolean;
  mode: 'dispatch' | 'issue_redirect' | 'invalid';
  targetUrl?: string;
}

export interface ConversionTriggerResult {
  triggered: boolean;
  mode: 'dispatch' | 'issue_api' | 'issue_url';
  issueUrl?: string;
}

export const HUBHUM_CONFIG = {
  owner: 'DavanzoKeoma',
  repo: 'HubHum',
  siteBaseUrl: 'https://davanzokeoma.github.io/HubHum',
};

const SESSION_KEY = 'hubhum_user_session_v1';
const FAVORITES_KEY = 'hubhum_favorites_v1';

export function getSavedSession(): GitHubUserSession | null {
  if (typeof window === 'undefined') return null;
  try {
    const raw = window.localStorage.getItem(SESSION_KEY);
    return raw ? (JSON.parse(raw) as GitHubUserSession) : null;
  } catch {
    return null;
  }
}

export function clearSavedSession(): void {
  if (typeof window === 'undefined') return;
  window.localStorage.removeItem(SESSION_KEY);
}

export async function verifyAndSaveUserToken(accessToken: string): Promise<GitHubUserSession> {
  const cleanToken = accessToken.trim();
  if (!cleanToken) {
    throw new Error('Empty token');
  }
  const userRes = await fetch('https://api.github.com/user', {
    headers: {
      Authorization: `Bearer ${cleanToken}`,
      Accept: 'application/vnd.github+json',
    },
  });
  if (!userRes.ok) {
    throw new Error(`GitHub verification returned ${userRes.status}`);
  }
  const userJson = await userRes.json();
  const session: GitHubUserSession = {
    login: userJson.login,
    avatarUrl: userJson.avatar_url || '',
    accessToken: cleanToken,
    authenticatedAt: new Date().toISOString(),
  };
  if (typeof window !== 'undefined') {
    window.localStorage.setItem(SESSION_KEY, JSON.stringify(session));
  }
  return session;
}

export function getFavorites(): string[] {
  if (typeof window === 'undefined') return [];
  try {
    const raw = window.localStorage.getItem(FAVORITES_KEY);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

export function toggleFavorite(slug: string): { favorites: string[]; saved: boolean } {
  const current = new Set(getFavorites());
  let saved = false;
  if (current.has(slug)) {
    current.delete(slug);
  } else {
    current.add(slug);
    saved = true;
  }
  const next = Array.from(current);
  if (typeof window !== 'undefined') {
    window.localStorage.setItem(FAVORITES_KEY, JSON.stringify(next));
  }
  return { favorites: next, saved };
}

export function normalizeGitHubProjectUrl(input: string): { owner: string; repo: string; url: string } | null {
  const trimmed = input.trim();
  const match = trimmed.match(/^https?:\/\/github\.com\/([A-Za-z0-9_.-]+)\/([A-Za-z0-9_.-]+?)(?:\.git|\/.*)?$/i);
  if (!match) return null;
  return {
    owner: match[1],
    repo: match[2],
    url: `https://github.com/${match[1]}/${match[2]}`,
  };
}

export function buildTranslateIssueUrl(owner: string, repo: string, repoUrl: string): string {
  const issueParams = new URLSearchParams({
    title: `[Translate] ${owner}/${repo}`,
    labels: 'hubhum-translate',
    body: `HubHum plain-English guide request:\n\nURL: ${repoUrl}`,
  });
  return `https://github.com/${HUBHUM_CONFIG.owner}/${HUBHUM_CONFIG.repo}/issues/new?${issueParams.toString()}`;
}

export async function triggerAppConversion(
  repoUrl: string,
  owner: string,
  repo: string
): Promise<ConversionTriggerResult> {
  const session = getSavedSession();
  const issueUrl = buildTranslateIssueUrl(owner, repo, repoUrl);

  if (session?.accessToken) {
    try {
      const dispatchEndpoint = `https://api.github.com/repos/${HUBHUM_CONFIG.owner}/${HUBHUM_CONFIG.repo}/dispatches`;
      const dispRes = await fetch(dispatchEndpoint, {
        method: 'POST',
        headers: {
          Accept: 'application/vnd.github+json',
          Authorization: `Bearer ${session.accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          event_type: 'translate_app',
          client_payload: {
            repo_url: repoUrl,
            requested_by: session.login,
          },
        }),
      });
      if (dispRes.status === 204 || dispRes.ok) {
        return { triggered: true, mode: 'dispatch' };
      }

      const issueEndpoint = `https://api.github.com/repos/${HUBHUM_CONFIG.owner}/${HUBHUM_CONFIG.repo}/issues`;
      const issueRes = await fetch(issueEndpoint, {
        method: 'POST',
        headers: {
          Accept: 'application/vnd.github+json',
          Authorization: `Bearer ${session.accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: `[Translate] ${owner}/${repo}`,
          labels: ['hubhum-translate'],
          body: `HubHum plain-English guide request:\n\nURL: ${repoUrl}`,
        }),
      });
      if (issueRes.status === 201 || issueRes.ok) {
        return { triggered: true, mode: 'issue_api' };
      }
    } catch {
      // Fall back cleanly to 1-click issue link
    }
  }

  return {
    triggered: false,
    mode: 'issue_url',
    issueUrl,
  };
}

export async function requestAsyncTranslation(projectUrl: string): Promise<TranslationDispatchResult> {
  const parsed = normalizeGitHubProjectUrl(projectUrl);
  if (!parsed) {
    return { accepted: false, mode: 'invalid' };
  }

  const res = await triggerAppConversion(parsed.url, parsed.owner, parsed.repo);
  if (res.triggered) {
    return { accepted: true, mode: 'dispatch' };
  }
  return {
    accepted: true,
    mode: 'issue_redirect',
    targetUrl: res.issueUrl,
  };
}
