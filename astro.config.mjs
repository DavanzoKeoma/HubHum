import { defineConfig } from 'astro/config';

const siteUrl = process.env.SITE_URL || 'https://DavanzoKeoma.github.io';
const basePath = process.env.SITE_BASE || '/';

export default defineConfig({
  site: siteUrl,
  base: basePath,
  output: 'static',
  trailingSlash: 'ignore',
});
