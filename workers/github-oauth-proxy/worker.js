/**
 * HubHum Unified API Bridge on Cloudflare Workers.
 * Endpoints:
 * - GET  /api/health       -> Worker health check
 * - POST /api/oauth/token  -> Exchanges GitHub Web OAuth `code` for `access_token`
 * - POST /api/convert      -> Validates GitHub URL & dispatches `translate_app` workflow
 */

const ALLOWED_ORIGIN = 'https://davanzokeoma.github.io';
const TARGET_GITHUB_REPO = 'DavanzoKeoma/HubHum';
const DEFAULT_CLIENT_ID = 'Ov23liZDnU0mNqCrMEj9';

function isAllowedOrigin(origin, pathname) {
  if (!origin) return true;
  if (origin === ALLOWED_ORIGIN) return true;
  if (pathname === '/api/oauth/token') return false;
  if (origin === 'https://github.com') return true;
  if (/^chrome-extension:\/\/[a-z0-9-]+$/i.test(origin)) return true;
  return false;
}

function resolveCorsOrigin(origin, pathname) {
  return origin && isAllowedOrigin(origin, pathname) ? origin : ALLOWED_ORIGIN;
}

function buildCorsHeaders(origin, pathname = '/') {
  return {
    'Access-Control-Allow-Origin': resolveCorsOrigin(origin, pathname),
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Accept',
    'Access-Control-Max-Age': '86400',
    'Vary': 'Origin',
  };
}

function jsonResponse(payload, status, origin, pathname = '/') {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...buildCorsHeaders(origin, pathname),
    },
  });
}

function parseGitHubRepoUrl(rawUrl) {
  const trimmed = String(rawUrl || '').trim();
  const match = trimmed.match(/^https?:\/\/github\.com\/([A-Za-z0-9_.-]+)\/([A-Za-z0-9_.-]+?)(?:\.git|\/.*)?$/i);
  if (!match) return null;
  const owner = match[1];
  const repo = match[2];
  const slug = repo.toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/^-+|-+$/g, '');
  return {
    owner,
    repo,
    slug,
    cleanUrl: `https://github.com/${owner}/${repo}`,
  };
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = request.headers.get('Origin') || '';

    if (request.method === 'OPTIONS') {
      if (!isAllowedOrigin(origin, url.pathname)) {
        return jsonResponse({ error: 'Origin not allowed' }, 403, origin, url.pathname);
      }
      return new Response(null, {
        status: 204,
        headers: buildCorsHeaders(origin, url.pathname),
      });
    }

    if (!isAllowedOrigin(origin, url.pathname)) {
      return jsonResponse({ error: 'Origin not allowed' }, 403, origin, url.pathname);
    }

    if (request.method === 'GET' && url.pathname === '/api/health') {
      return jsonResponse({ status: 'ok', worker: 'hubhum-api-bridge' }, 200, origin, url.pathname);
    }

    if (request.method === 'POST' && url.pathname === '/api/oauth/token') {
      let body;
      try {
        body = await request.json();
      } catch {
        return jsonResponse({ error: 'Invalid JSON payload' }, 400, origin);
      }

      const code = String(body?.code || '').trim();
      if (!code) {
        return jsonResponse({ error: 'Missing OAuth code' }, 400, origin);
      }

      const clientId = env.GITHUB_OAUTH_CLIENT_ID || DEFAULT_CLIENT_ID;
      const clientSecret = env.GITHUB_OAUTH_CLIENT_SECRET || '';
      if (!clientSecret) {
        return jsonResponse({ error: 'OAuth client secret is not configured' }, 500, origin);
      }

      const ghRes = await fetch('https://github.com/login/oauth/access_token', {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
          'User-Agent': 'HubHum-API-Bridge/1.0',
        },
        body: JSON.stringify({
          client_id: clientId,
          client_secret: clientSecret,
          code,
          redirect_uri: `${ALLOWED_ORIGIN}/HubHum/`,
        }),
      });

      const ghData = await ghRes.json();
      return jsonResponse(ghData, ghRes.ok ? 200 : 400, origin);
    }

    if (request.method === 'POST' && url.pathname === '/api/convert') {
      let body;
      try {
        body = await request.json();
      } catch {
        return jsonResponse({ error: 'Invalid JSON payload' }, 400, origin, url.pathname);
      }

      const parsed = parseGitHubRepoUrl(body?.repo_url);
      if (!parsed) {
        return jsonResponse({ error: 'Invalid GitHub repository URL' }, 400, origin, url.pathname);
      }

      const pat = env.HUBHUM_PAT || '';
      if (!pat) {
        return jsonResponse({ error: 'Worker HUBHUM_PAT secret is not configured' }, 500, origin, url.pathname);
      }

      const dispatchRes = await fetch(`https://api.github.com/repos/${TARGET_GITHUB_REPO}/dispatches`, {
        method: 'POST',
        headers: {
          Accept: 'application/vnd.github+json',
          Authorization: `Bearer ${pat}`,
          'Content-Type': 'application/json',
          'User-Agent': 'HubHum-API-Bridge/1.0',
          'X-GitHub-Api-Version': '2022-11-28',
        },
        body: JSON.stringify({
          event_type: 'translate_app',
          client_payload: {
            repo_url: parsed.cleanUrl,
          },
        }),
      });

      if (dispatchRes.status === 204 || dispatchRes.ok) {
        return jsonResponse(
          {
            status: 'queued',
            slug: parsed.slug,
            repo_url: parsed.cleanUrl,
          },
          200,
          origin,
          url.pathname
        );
      }

      const errText = await dispatchRes.text();
      return jsonResponse(
        {
          error: 'GitHub dispatch failed',
          github_status: dispatchRes.status,
          detail: errText.slice(0, 200),
        },
        dispatchRes.status === 403 || dispatchRes.status === 429 ? 429 : 502,
        origin,
        url.pathname
      );
    }

    return jsonResponse({ error: 'Not Found' }, 404, origin, url.pathname);
  },
};
