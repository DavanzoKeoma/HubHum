import { getSavedSession } from './github-oauth';
import { withBase } from './url';

export interface CatalogIndexEntry {
  slug: string;
  name: string;
  repo_url: string;
  full_name: string;
  category: string;
  icon: string;
}

export interface LiveGitHubAppResult {
  id: number;
  owner: string;
  repo: string;
  fullName: string;
  slug: string;
  htmlUrl: string;
  avatarUrl: string;
  description: string;
  starsFormatted: string;
  starsCount: number;
  humanCategory: string;
  humanTags: string[];
  existingSlug: string | null;
}

export interface LiveSearchOutcome {
  status: 'ok' | 'empty' | 'rate_limited' | 'error';
  items: LiveGitHubAppResult[];
}

const TECH_JARGON_TAGS = new Set([
  'react',
  'reactjs',
  'typescript',
  'javascript',
  'electron',
  'c-plus-plus',
  'cpp',
  'c',
  'csharp',
  'rust',
  'golang',
  'go',
  'python',
  'java',
  'kotlin',
  'swift',
  'vue',
  'vuejs',
  'svelte',
  'nodejs',
  'node',
  'webpack',
  'vite',
  'html',
  'css',
  'scss',
  'tailwind',
  'docker-compose',
  'api',
  'sdk',
  'library',
  'framework',
  'boilerplate',
  'qt',
  'gtk',
  'wxwidgets',
]);

const TOPIC_CATEGORY_MAP: Array<[string, Set<string>]> = [
  ['Audio & Video', new Set(['video-editor', 'video', 'audio', 'ffmpeg', 'recording', 'sound', 'media-player', 'podcast', 'music'])],
  ['Productivity & Office', new Set(['notes', 'markdown', 'todo', 'office', 'document', 'calendar', 'productivity', 'writing', 'pdf'])],
  ['Security & Privacy', new Set(['vpn', 'password-manager', 'passwords', 'encryption', 'privacy', 'security', 'firewall', 'adblock'])],
  ['System Utilities', new Set(['utility', 'utilities', 'downloader', 'system-tools', 'backup', 'file-manager', 'desktop', 'windows', 'macos', 'linux'])],
  ['Web & Cloud Apps', new Set(['cms', 'self-hosted', 'dashboard', 'docker', 'web-app', 'webapp', 'cloud', 'blog', 'newsletter', 'ai', 'automation'])],
];

let catalogCache: CatalogIndexEntry[] | null = null;

export function slugifyRepoName(repoName: string): string {
  return repoName
    .toLowerCase()
    .replace(/[^a-z0-9-]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

export function formatStarsCount(stars: number): string {
  if (stars >= 1000) {
    return `${(stars / 1000).toFixed(stars >= 10000 ? 1 : 1)}k`;
  }
  return String(stars);
}

export function normalizeTopicsToHuman(topics: string[], description: string): { category: string; tags: string[] } {
  const cleaned = topics
    .map((t) => String(t || '').trim().toLowerCase())
    .filter((t) => t.length > 0 && !TECH_JARGON_TAGS.has(t));

  const descWords = (description || '').toLowerCase().match(/[a-z0-9-]+/g) || [];
  const tokenSet = new Set([...cleaned, ...descWords]);

  let humanCategory = 'Productivity & Office';
  for (const [label, keywords] of TOPIC_CATEGORY_MAP) {
    for (const kw of keywords) {
      if (tokenSet.has(kw)) {
        humanCategory = label;
        break;
      }
    }
    if (humanCategory !== 'Productivity & Office') break;
  }

  return {
    category: humanCategory,
    tags: cleaned.slice(0, 2),
  };
}

export async function loadCatalogIndex(): Promise<CatalogIndexEntry[]> {
  if (catalogCache) return catalogCache;
  try {
    const res = await fetch(withBase('/catalog-index.json'));
    if (res.ok) {
      catalogCache = (await res.json()) as CatalogIndexEntry[];
      return catalogCache;
    }
  } catch {
    // Fallback empty
  }
  return [];
}

function findExistingSlug(
  catalog: CatalogIndexEntry[],
  fullName: string,
  htmlUrl: string,
  repoName: string
): string | null {
  const normFull = fullName.toLowerCase();
  const normUrl = htmlUrl.replace(/\/+$/, '').toLowerCase();
  const normSlug = slugifyRepoName(repoName);

  const match = catalog.find(
    (item) =>
      item.full_name === normFull ||
      item.repo_url === normUrl ||
      item.slug === normSlug
  );
  return match ? match.slug : null;
}

export async function searchGitHubProjects(query: string, signal?: AbortSignal): Promise<LiveSearchOutcome> {
  const clean = query.trim();
  if (clean.length < 2) {
    return { status: 'empty', items: [] };
  }

  const catalog = await loadCatalogIndex();
  const session = getSavedSession();
  const headers: Record<string, string> = {
    Accept: 'application/vnd.github+json',
  };
  if (session?.accessToken) {
    headers.Authorization = `Bearer ${session.accessToken}`;
  }

  const endpoint = `https://api.github.com/search/repositories?q=${encodeURIComponent(clean)}+stars:>50&sort=stars&order=desc&per_page=8`;

  try {
    const res = await fetch(endpoint, { headers, signal });
    if (res.status === 403 || res.status === 429) {
      return { status: 'rate_limited', items: [] };
    }
    if (!res.ok) {
      return { status: 'error', items: [] };
    }
    const payload = await res.json();
    const rawItems = Array.isArray(payload?.items) ? payload.items : [];
    if (rawItems.length === 0) {
      return { status: 'empty', items: [] };
    }

    const mapped: LiveGitHubAppResult[] = rawItems.map((item: Record<string, unknown>) => {
      const ownerObj = (item.owner as Record<string, unknown>) || {};
      const ownerLogin = String(ownerObj.login || '');
      const repoName = String(item.name || '');
      const fullName = String(item.full_name || `${ownerLogin}/${repoName}`);
      const htmlUrl = String(item.html_url || `https://github.com/${fullName}`);
      const rawDesc = String(item.description || 'Open-source application hosted on GitHub.');
      const topics = Array.isArray(item.topics) ? (item.topics as string[]) : [];
      const stars = Number(item.stargazers_count || 0);
      const avatarRaw = String(ownerObj.avatar_url || '');
      const avatarUrl = avatarRaw ? `${avatarRaw}${avatarRaw.includes('?') ? '&' : '?'}s=64` : withBase('/icons/hubhum.svg');
      const { category, tags } = normalizeTopicsToHuman(topics, rawDesc);

      return {
        id: Number(item.id || 0),
        owner: ownerLogin,
        repo: repoName,
        fullName,
        slug: slugifyRepoName(repoName),
        htmlUrl,
        avatarUrl,
        description: rawDesc,
        starsFormatted: formatStarsCount(stars),
        starsCount: stars,
        humanCategory: category,
        humanTags: tags,
        existingSlug: findExistingSlug(catalog, fullName, htmlUrl, repoName),
      };
    });

    return { status: 'ok', items: mapped };
  } catch (err) {
    if (err instanceof DOMException && err.name === 'AbortError') {
      throw err;
    }
    return { status: 'error', items: [] };
  }
}
