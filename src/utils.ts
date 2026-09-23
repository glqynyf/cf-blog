import type { CollectionEntry } from 'astro:content';
import { getCollection } from 'astro:content';

/**
 * 获取所有文章，按发布时间倒序。
 * 自动剔除草稿（仅在生产环境）。
 */
export async function getSortedPosts(): Promise<CollectionEntry<'posts'>[]> {
  const all = await getCollection('posts', ({ data }) => {
    return import.meta.env.DEV || data.draft !== true;
  });
  return all.sort(
    (a, b) => b.data.pubDate.getTime() - a.data.pubDate.getTime()
  );
}

/**
 * 提取所有用到的标签，并统计出现次数。
 */
export async function getAllTags(): Promise<Map<string, number>> {
  const posts = await getSortedPosts();
  const map = new Map<string, number>();
  for (const post of posts) {
    for (const tag of post.data.tags) {
      map.set(tag, (map.get(tag) ?? 0) + 1);
    }
  }
  return map;
}

/**
 * 中文日期格式化。
 */
export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(date);
}

/**
 * 估算阅读时长（按每分钟 400 个中文字符粗略估算）。
 */
export function estimateMinutes(
  body: string | undefined,
  fallback = 5
): string {
  if (!body) return `${fallback} 分钟`;
  const chineseChars = (body.match(/[\u4e00-\u9fa5]/g) ?? []).length;
  const englishWords = (body.match(/[a-zA-Z]+/g) ?? []).length;
  // 中文按字数 / 400，英文按词数 / 200，取整并至少 1 分钟
  const minutes = Math.max(1, Math.ceil(chineseChars / 400 + englishWords / 200));
  return `${minutes} 分钟`;
}