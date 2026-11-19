/**
 * Native 1-Click GitHub Web OAuth & Unified Cloudflare Worker Bridge Adapter for HubHum.
 * Zero manual tokens, zero GitHub Issue redirects, zero CORS friction.
 */

export interface GitHubUserSession {
  login: string;
  avatarUrl: string;
  accessToken?: string;
  authenticatedAt: string;
}

export interface ConvertApiResult {
  status: string;
  slug: string;
  repo_url: string;
}

export const HUBHUM_CONFIG = {
  owner: 'DavanzoKeoma',
  repo: 'HubHum',
  clientId: import.meta.env.PUBLIC_GITHUB_OAUTH_CLIENT_ID || 'Ov23liZDnU0mNqCrMEj9',
  workerUrl: (import.meta.env.PUBLIC_WORKER_URL || 'https://hubhum-api-bridge.keomadavanzo.workers.dev').replace(/\/+$/, ''),
  oauthRedirectUri: 'https://davanzokeoma.github.io/HubHum/',
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

export function startGitHubWebOAuth(): void {
  if (typeof window === 'undefined') return;
  const params = new URLSearchParams({
    client_id: HUBHUM_CONFIG.clientId,
    scope: 'read:user',
    redirect_uri: HUBHUM_CONFIG.oauthRedirectUri,
  });
  window.location.href = `https://github.com/login/oauth/authorize?${params.toString()}`;
}

export async function exchangeOAuthCode(code: string): Promise<GitHubUserSession> {
  const tokenRes = await fetch(`${HUBHUM_CONFIG.workerUrl}/api/oauth/token`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify({ code }),
  });

  if (!tokenRes.ok) {
    throw new Error(`OAuth token exchange failed (${tokenRes.status})`);
  }
  const tokenData = await tokenRes.json();
  const accessToken = String(tokenData?.access_token || '').trim();
  if (!accessToken) {
    throw new Error(tokenData?.error_description || 'Missing access_token');
  }

  const userRes = await fetch('https://api.github.com/user', {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      Accept: 'application/vnd.github+json',
    },
  });
  if (!userRes.ok) {
    throw new Error(`GitHub user fetch failed (${userRes.status})`);
  }
  const userJson = await userRes.json();
  const session: GitHubUserSession = {
    login: userJson.login,
    avatarUrl: userJson.avatar_url || '',
    accessToken,
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

export async function triggerAppConversion(repoUrl: string): Promise<ConvertApiResult> {
  const res = await fetch(`${HUBHUM_CONFIG.workerUrl}/api/convert`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify({ repo_url: repoUrl }),
  });

  if (!res.ok) {
    throw new Error(`Conversion dispatch failed (${res.status})`);
  }
  const data = (await res.json()) as ConvertApiResult;
  if (!data?.slug) {
    throw new Error('Missing slug from conversion response');
  }
  return data;
}
