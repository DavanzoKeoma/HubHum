import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

const siteUrl = process.env.SITE_URL || 'https://davanzokeoma.github.io';
const basePath = process.env.SITE_BASE || '/HubHum';

export default defineConfig({
  site: siteUrl,
  base: basePath,
  integrations: [sitemap()],
  output: 'static',
  trailingSlash: 'ignore',
  build: {
    inlineStylesheets: 'always',
  },
});
