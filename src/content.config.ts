import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/**
 * 文章集合：Markdown 文件存放在 src/content/posts/ 下。
 * - tags：用于分类与筛选，建议控制在 5 个以内。
 * - summary：首页和 RSS 中展示的导语。
 * - pubDate / updatedDate：发布日期与最后更新日期。
 * - draft：草稿状态，true 时不会出现在生产构建中（dev 下仍可见）。
 * - featured：是否在首页精选区展示。
 */
const posts = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/posts' }),
  schema: z.object({
    title: z.string().max(120),
    summary: z.string().max(800),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
    featured: z.boolean().default(false),
    cover: z.string().optional(),
  }),
});

export const collections = { posts };