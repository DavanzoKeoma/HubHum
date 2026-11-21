import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const localizedTextSchema = z.object({
  tagline: z.string().min(1),
  summary: z.string().min(1),
});

const appsCollection = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './content/apps' }),
  schema: z.object({
    title: z.string().min(1),
    slug: z.string().regex(/^[a-z0-9-]+$/),
    tagline: z.string().default(''),
    summary: z.string().default(''),
    tags: z.array(z.string().min(1)).min(1),
    is_webapp: z.boolean(),
    app_type: z.enum(['desktop', 'webapp', 'cli']).default('desktop'),
    category: z.string().default('Productivity'),
    icon: z.string().default('/icons/hubhum.svg'),
    stars: z.number().int().nonnegative().default(0),
    source_url: z.string().url().optional(),
    download_url: z.string().url().optional(),
    downloadUrl: z.string().url().optional(),
    download_label: z.string().optional(),
    license: z.string().optional(),
    scouting_tier: z.string().optional(),
    operatingSystem: z.string().optional(),
    applicationCategory: z.string().optional(),
    fileSize: z.string().optional(),
    priceCurrency: z.string().default('USD'),
    price: z.string().default('0'),
    affiliate_merchant_id: z.string().optional(),
    affiliate_name: z.string().optional(),
    affiliate_url: z.string().url().optional(),
    affiliate_pitch: z.string().optional(),
    ai_provider: z.string().optional(),
    featured_weekly: z.boolean().default(false),
    updated_at: z.string().optional(),
    i18n: z
      .object({
        it: localizedTextSchema.optional(),
        es: localizedTextSchema.optional(),
        fr: localizedTextSchema.optional(),
        de: localizedTextSchema.optional(),
      })
      .optional(),
  }),
});

const bundlesCollection = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './content/bundles' }),
  schema: z.object({
    title: z.string().min(1),
    slug: z.string().regex(/^[a-z0-9-]+$/),
    category: z.string().default('Curated Guides'),
    summary: z.string().default(''),
    tags: z.array(z.string()).default([]),
    app_slugs: z.array(z.string()).default([]),
    updated_at: z.string().optional(),
  }),
});

export const collections = {
  apps: appsCollection,
  bundles: bundlesCollection,
};
