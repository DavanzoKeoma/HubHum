/**
 * Cloudflare Worker OAuth Token Exchange Proxy for HubHum (Static GitHub Pages).
 * Store GITHUB_OAUTH_CLIENT_ID and GITHUB_OAUTH_CLIENT_SECRET via `wrangler secret put`.
 */
const ALLOWED_ORIGIN = 'https://davanzokeoma.github.io';

function corsHeaders(origin) {
  const allow = origin === ALLOWED_ORIGIN ? origin : ALLOWED_ORIGIN;
  return {
    'Access-Control-Allow-Origin': allow,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Vary': 'Origin',
  };
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders(origin) });
    }
    if (request.method !== 'POST') {
      return new Response('Method Not Allowed', { status: 405, headers: corsHeaders(origin) });
    }
    if (origin && origin !== ALLOWED_ORIGIN) {
      return new Response('Forbidden Origin', { status: 403, headers: corsHeaders(origin) });
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return new Response('Invalid JSON', { status: 400, headers: corsHeaders(origin) });
    }

    const code = (body?.code || '').trim();
    if (!code) {
      return new Response('Missing code', { status: 400, headers: corsHeaders(origin) });
    }

    const tokenRes = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        client_id: env.GITHUB_OAUTH_CLIENT_ID,
        client_secret: env.GITHUB_OAUTH_CLIENT_SECRET,
        code,
        redirect_uri: body.redirect_uri || `${ALLOWED_ORIGIN}/HubHum/`,
      }),
    });

    const data = await tokenRes.json();
    return new Response(JSON.stringify(data), {
      status: tokenRes.ok ? 200 : 400,
      headers: {
        'Content-Type': 'application/json',
        ...corsHeaders(origin),
      },
    });
  },
};
