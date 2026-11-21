import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

const escapeXml = (str: string): string =>
  String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');

export const GET: APIRoute = async ({ site }) => {
  const origin = (site?.toString() || 'https://davanzokeoma.github.io').replace(/\/$/, '');
  const rawBase = import.meta.env.BASE_URL || '/HubHum';
  const base = rawBase.endsWith('/') ? rawBase.slice(0, -1) : rawBase;
  const siteRoot = `${origin}${base}`;

  const apps = await getCollection('apps');
  const guides = await getCollection('guides');

  const recentApps = [...apps]
    .sort((a, b) => (b.data.updated_at || '').localeCompare(a.data.updated_at || '') || (b.data.stars || 0) - (a.data.stars || 0))
    .slice(0, 60);

  const recentGuides = guides.filter((g) => g.data.level <= 2).slice(0, 20);

  const appItems = recentApps.map((app) => {
    const url = `${siteRoot}/apps/${app.data.slug}/`;
    const dateStr = app.data.updated_at ? new Date(`${app.data.updated_at}T12:00:00Z`).toUTCString() : new Date().toUTCString();
    const desc = `${app.data.summary} (${app.data.app_type} | ${app.data.operatingSystem || 'Cross-platform'} | ${app.data.license || 'Open Source'})`;
    return [
      '    <item>',
      `      <title>${escapeXml(app.data.title)}</title>`,
      `      <link>${escapeXml(url)}</link>`,
      `      <guid isPermaLink="true">${escapeXml(url)}</guid>`,
      `      <pubDate>${dateStr}</pubDate>`,
      `      <category>${escapeXml(app.data.category)}</category>`,
      `      <description>${escapeXml(desc)}</description>`,
      '    </item>',
    ].join('\n');
  });

  const guideItems = recentGuides.map((g) => {
    const url = `${siteRoot}/guides/${g.data.slug}/`;
    const dateStr = g.data.updated_at ? new Date(`${g.data.updated_at}T12:00:00Z`).toUTCString() : new Date().toUTCString();
    return [
      '    <item>',
      `      <title>${escapeXml(g.data.title)}</title>`,
      `      <link>${escapeXml(url)}</link>`,
      `      <guid isPermaLink="true">${escapeXml(url)}</guid>`,
      `      <pubDate>${dateStr}</pubDate>`,
      `      <category>${escapeXml(g.data.macro_category)}</category>`,
      `      <description>${escapeXml(g.data.summary)}</description>`,
      '    </item>',
    ].join('\n');
  });

  const xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
    '  <channel>',
    '    <title>HubHum — Free Open-Source Software Explained Simply</title>',
    `    <link>${escapeXml(`${siteRoot}/`)}</link>`,
    `    <atom:link href="${escapeXml(`${siteRoot}/feed.xml`)}" rel="self" type="application/rss+xml" />`,
    '    <description>Plain-English guides, official downloads, and topic comparisons for vetted free and open-source software.</description>',
    '    <language>en-us</language>',
    `    <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>`,
    ...guideItems,
    ...appItems,
    '  </channel>',
    '</rss>',
    '',
  ].join('\n');

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/rss+xml; charset=utf-8',
    },
  });
};
