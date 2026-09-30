// 自定义 sitemap 端点，输出到规范路径 /sitemap.xml。
//
// 为什么不用 @astrojs/sitemap：
//   1. 它固定生成 `sitemap-0.xml` + `sitemap-index.xml`，而爬虫、
//      Search Console、绝大多数工具默认找的是 `/sitemap.xml`。
//      本项目原先没有 /sitemap.xml，请求它会被 SPA fallback 返回首页 HTML
//      （HTTP 200 + text/html），看起来就是「sitemap 内容完全不对」。
//   2. 它只枚举 Astro 自己构建出的路由，public/notes/ 下的 115 篇
//      静态 HTML 一篇都进不去，得额外用 customPages 手工补。
//
// 改为自己生成后：单一规范入口、无分片、路径符合惯例，
// 且能直接把 public/ 下的静态笔记与规划文档一并纳入。
//
// ⚠️ build 脚本是 `astro check && astro build`，strict 模式带 noImplicitAny。
// 这个文件虽是 .ts，但**函数参数必须写显式 TS 类型注解**——只靠 JSDoc 的
// `@param {string}` 不被采纳，会报 “Parameter 'dirName' implicitly has an
// 'any' type” 直接中断构建。本机没有 node，跑不了 build 验证，只能靠约定。

import { existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const SITE = 'https://stock-blog.duckuno.com';

export const prerender = true;

/** 枚举 public/ 下某个目录里的静态 HTML，返回排序后的站点绝对 URL */
function staticUrls(dirName: string): string[] {
  const dir = join(process.cwd(), 'public', dirName);
  if (!existsSync(dir)) {
    console.warn('[sitemap] 未找到 public/%s：%s', dirName, dir);
    return [];
  }
  return readdirSync(dir)
    .filter((f) => f.endsWith('.html'))
    // slug 必须 encodeURIComponent：文件名含「10%」「30%」这类 ASCII 百分号，
    // 未编码会构成非法 URL，Cloudflare 直接返回 400。
    .map((f) => `${SITE}/${dirName}/${encodeURIComponent(f.slice(0, -'.html'.length))}`)
    .sort();
}

/** @type {import('astro').APIRoute} */
export const GET = () => {
  const locs = [
    `${SITE}/`,
    `${SITE}/about/`,
    `${SITE}/notes/`,
    `${SITE}/planning/`,
    ...staticUrls('notes'),
    ...staticUrls('planning'),
  ];

  const body =
    '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    locs.map((loc) => `  <url><loc>${loc}</loc></url>`).join('\n') +
    '\n</urlset>\n';

  return new Response(body, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' },
  });
};
