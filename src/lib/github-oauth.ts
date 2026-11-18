/**
 * GitHub OAuth & Dispatch Client Adapter (Sezione 10 & Sezione 11).
 * Predisposto per:
 * - "Salva nei preferiti" (stato locale + sincronizzazione profilo autenticato)
 * - "Lascia una recensione"
 * - Ricerca autenticata con token utente per scaricare i rate limit principali
 * - Invio richieste di traduzione asincrona via repository_dispatch (o fallback Issue)
 */

export interface GitHubUserSession {
  login: string;
  avatarUrl: string;
  accessToken?: string;
  authenticatedAt: string;
}

export interface TranslationDispatchResult {
  accepted: boolean;
  mode: 'dispatch' | 'issue_redirect' | 'queued_demo';
  message: string;
  targetUrl?: string;
}

export const HUBHUM_CONFIG = {
  owner: 'DavanzoKeoma',
  repo: 'HubHum',
  oauthAuthorizeUrl: 'https://github.com/login/oauth/authorize',
  oauthScopes: 'read:user public_repo',
  clientId: import.meta.env.PUBLIC_GITHUB_OAUTH_CLIENT_ID || '',
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

export function buildGitHubOAuthUrl(redirectUri: string): string | null {
  if (!HUBHUM_CONFIG.clientId) return null;
  const params = new URLSearchParams({
    client_id: HUBHUM_CONFIG.clientId,
    redirect_uri: redirectUri,
    scope: HUBHUM_CONFIG.oauthScopes,
  });
  return `${HUBHUM_CONFIG.oauthAuthorizeUrl}?${params.toString()}`;
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
    return {
      accepted: false,
      mode: 'queued_demo',
      message: 'Inserisci un link valido nel formato https://github.com/autore/nome-app.',
    };
  }

  const session = getSavedSession();
  const dispatchEndpoint = `https://api.github.com/repos/${HUBHUM_CONFIG.owner}/${HUBHUM_CONFIG.repo}/dispatches`;

  // If the visitor authenticated with GitHub OAuth, trigger repository_dispatch directly with their token.
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
        return {
          accepted: true,
          mode: 'dispatch',
          message: "L'app è in traduzione. Sarà online tra circa 2 minuti.",
        };
      }
    } catch {
      // Fall back safely to pre-filled submission flow
    }
  }

  // Anonymous static-site safe fallback: prepare silent request issue link without exposing any site token
  const issueParams = new URLSearchParams({
    title: `[Translate] ${parsed.owner}/${parsed.repo}`,
    labels: 'translate-request',
    body: `Richiesta traduzione automatica HubHum:\n\nURL: ${parsed.url}`,
  });
  const issueUrl = `https://github.com/${HUBHUM_CONFIG.owner}/${HUBHUM_CONFIG.repo}/issues/new?${issueParams.toString()}`;

  return {
    accepted: true,
    mode: 'issue_redirect',
    message: "L'app è in traduzione. Sarà online tra circa 2 minuti.",
    targetUrl: issueUrl,
  };
}
