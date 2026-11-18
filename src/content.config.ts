import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const appsCollection = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './content/apps' }),
  schema: z.object({
    title: z.string().min(1),
    slug: z.string().regex(/^[a-z0-9-]+$/),
    tags: z.array(z.string().min(1)).min(1),
    is_webapp: z.boolean(),
    category: z.string().default('Produttività'),
    summary: z.string().default(''),
    stars: z.number().int().nonnegative().default(0),
    source_url: z.string().url().optional(),
    download_url: z.string().url().optional(),
    download_label: z.string().optional(),
    license: z.string().optional(),
    affiliate_merchant_id: z.string().optional(),
    affiliate_name: z.string().optional(),
    affiliate_url: z.string().url().optional(),
    affiliate_pitch: z.string().optional(),
    featured_weekly: z.boolean().default(false),
    updated_at: z.string().optional(),
  }),
});

const bundlesCollection = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './content/bundles' }),
  schema: z.object({
    title: z.string().min(1),
    slug: z.string().regex(/^[a-z0-9-]+$/),
    category: z.string().default('Raccolte'),
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
