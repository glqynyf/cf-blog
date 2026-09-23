import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { SITE } from '../consts';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = await getCollection('posts', ({ data }) => {
    return import.meta.env.DEV || data.draft !== true;
  });

  return rss({
    title: SITE.title,
    description: SITE.description,
    site: context.site ?? 'https://example.pages.dev',
    items: posts
      .sort((a, b) => b.data.pubDate.getTime() - a.data.pubDate.getTime())
      .map((post) => ({
        title: post.data.title,
        description: post.data.summary,
        pubDate: post.data.pubDate,
        link: `/posts/${post.slug}/`,
        categories: [...post.data.tags],
      })),
    customData: `<language>zh-CN</language>`,
    stylesheet: false,
  });
}