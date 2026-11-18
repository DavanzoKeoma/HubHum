/**
 * Native GitHub Device Authorization Flow & Favorites Adapter for HubHum.
 * Zero external proxies: uses GitHub's official Device Flow endpoints directly.
 */

export interface GitHubUserSession {
  login: string;
  avatarUrl: string;
  accessToken?: string;
  authenticatedAt: string;
}

export interface DeviceCodeResponse {
  device_code: string;
  user_code: string;
  verification_uri: string;
  expires_in: number;
  interval: number;
}

export interface TranslationDispatchResult {
  accepted: boolean;
  mode: 'dispatch' | 'issue_redirect' | 'invalid';
  targetUrl?: string;
}

export const HUBHUM_CONFIG = {
  owner: 'DavanzoKeoma',
  repo: 'HubHum',
  deviceCodeUrl: 'https://github.com/login/device/code',
  accessTokenUrl: 'https://github.com/login/oauth/access_token',
  deviceVerifyUrl: 'https://github.com/login/device',
  oauthScopes: 'read:user',
  clientId: import.meta.env.PUBLIC_GITHUB_OAUTH_CLIENT_ID || 'Ov23liZDnU0mNqCrMEj9',
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
    throw new Error(`GitHub user fetch failed (${userRes.status})`);
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

export async function startDeviceFlow(): Promise<DeviceCodeResponse> {
  const body = new URLSearchParams({
    client_id: HUBHUM_CONFIG.clientId,
    scope: HUBHUM_CONFIG.oauthScopes,
  });
  const res = await fetch(HUBHUM_CONFIG.deviceCodeUrl, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: body.toString(),
  });
  if (!res.ok) {
    throw new Error(`Device code request failed (${res.status})`);
  }
  const data = (await res.json()) as DeviceCodeResponse;
  if (!data.device_code || !data.user_code) {
    throw new Error('Invalid device flow payload');
  }
  return data;
}

function waitAbortable(ms: number, signal?: AbortSignal): Promise<void> {
  return new Promise((resolve, reject) => {
    if (signal?.aborted) {
      reject(new DOMException('Aborted', 'AbortError'));
      return;
    }
    const timer = window.setTimeout(() => {
      signal?.removeEventListener('abort', onAbort);
      resolve();
    }, ms);
    const onAbort = () => {
      window.clearTimeout(timer);
      reject(new DOMException('Aborted', 'AbortError'));
    };
    signal?.addEventListener('abort', onAbort, { once: true });
  });
}

export async function pollDeviceFlowToken(
  deviceCode: string,
  initialIntervalSec = 5,
  signal?: AbortSignal
): Promise<GitHubUserSession> {
  let intervalSec = Math.max(5, initialIntervalSec || 5);

  while (!signal?.aborted) {
    await waitAbortable(intervalSec * 1000, signal);

    const body = new URLSearchParams({
      client_id: HUBHUM_CONFIG.clientId,
      device_code: deviceCode,
      grant_type: 'urn:ietf:params:oauth:grant-type:device_code',
    });

    const res = await fetch(HUBHUM_CONFIG.accessTokenUrl, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: body.toString(),
      signal,
    });
    const data = await res.json();

    if (data.access_token) {
      return verifyAndSaveUserToken(data.access_token);
    }
    if (data.error === 'authorization_pending') {
      continue;
    }
    if (data.error === 'slow_down') {
      intervalSec += 5;
      continue;
    }
    throw new Error(data.error_description || data.error || 'Device authorization failed');
  }
  throw new DOMException('Aborted', 'AbortError');
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
