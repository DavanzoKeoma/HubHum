/**
 * GitHub OAuth & Dispatch Client Adapter for HubHum.
 * Zero raw alert() dialogs: works with localStorage favorites out of the box and
 * upgrades seamlessly to GitHub OAuth when PUBLIC_GITHUB_OAUTH_CLIENT_ID is set.
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

export const HUBHUM_CONFIG = {
  owner: 'DavanzoKeoma',
  repo: 'HubHum',
  oauthAuthorizeUrl: 'https://github.com/login/oauth/authorize',
  oauthScopes: 'read:user public_repo',
  clientId: import.meta.env.PUBLIC_GITHUB_OAUTH_CLIENT_ID || '',
  oauthProxyUrl: import.meta.env.PUBLIC_GITHUB_OAUTH_PROXY_URL || '',
};

const SESSION_KEY = 'hubhum_user_session_v1';
const FAVORITES_KEY = 'hubhum_favorites_v1';

export function isOAuthConfigured(): boolean {
  return Boolean(HUBHUM_CONFIG.clientId && HUBHUM_CONFIG.oauthProxyUrl);
}

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

export function buildGitHubOAuthUrl(redirectUri: string): string | null {
  if (!HUBHUM_CONFIG.clientId) return null;
  const params = new URLSearchParams({
    client_id: HUBHUM_CONFIG.clientId,
    redirect_uri: redirectUri,
    scope: HUBHUM_CONFIG.oauthScopes,
  });
  return `${HUBHUM_CONFIG.oauthAuthorizeUrl}?${params.toString()}`;
}

export async function handleOAuthCallbackIfPresent(): Promise<GitHubUserSession | null> {
  if (typeof window === 'undefined' || !isOAuthConfigured()) return null;
  const params = new URLSearchParams(window.location.search);
  const code = params.get('code');
  if (!code) return null;

  try {
    const cleanRedirect = `${window.location.origin}${window.location.pathname}`;
    const tokenRes = await fetch(HUBHUM_CONFIG.oauthProxyUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, redirect_uri: cleanRedirect }),
    });
    const tokenData = await tokenRes.json();
    const accessToken = tokenData?.access_token;
    if (!accessToken) return null;

    const userRes = await fetch('https://api.github.com/user', {
      headers: { Authorization: `Bearer ${accessToken}`, Accept: 'application/vnd.github+json' },
    });
    if (!userRes.ok) return null;
    const userJson = await userRes.json();
    const session: GitHubUserSession = {
      login: userJson.login,
      avatarUrl: userJson.avatar_url || '',
      accessToken,
      authenticatedAt: new Date().toISOString(),
    };
    window.localStorage.setItem(SESSION_KEY, JSON.stringify(session));
    window.history.replaceState({}, document.title, cleanRedirect);
    return session;
  } catch {
    return null;
  }
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

export async function requestAsyncTranslation(projectUrl: string): Promise<TranslationDispatchResult> {
  const parsed = normalizeGitHubProjectUrl(projectUrl);
  if (!parsed) {
    return { accepted: false, mode: 'invalid' };
  }

  const session = getSavedSession();
  const dispatchEndpoint = `https://api.github.com/repos/${HUBHUM_CONFIG.owner}/${HUBHUM_CONFIG.repo}/dispatches`;

  if (session?.accessToken) {
    try {
      const response = await fetch(dispatchEndpoint, {
        method: 'POST',
        headers: {
          Accept: 'application/vnd.github+json',
          Authorization: `Bearer ${session.accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          event_type: 'translate-app',
          client_payload: {
            repo_url: parsed.url,
            requested_by: session.login,
          },
        }),
      });
      if (response.status === 204 || response.ok) {
        return { accepted: true, mode: 'dispatch' };
      }
    } catch {
      // Fallback to issue submission URL
    }
  }

  const issueParams = new URLSearchParams({
    title: `[Translate] ${parsed.owner}/${parsed.repo}`,
    labels: 'translate-request',
    body: `HubHum app guide request:\n\nURL: ${parsed.url}`,
  });
  const issueUrl = `https://github.com/${HUBHUM_CONFIG.owner}/${HUBHUM_CONFIG.repo}/issues/new?${issueParams.toString()}`;

  return {
    accepted: true,
    mode: 'issue_redirect',
    targetUrl: issueUrl,
  };
}
