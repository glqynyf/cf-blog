// @ts-check
import { existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

const SITE_URL = 'https://stock-blog.duckuno.com';

/**
 * 115 篇笔记是 public/notes/ 下的独立 HTML，由 Cloudflare Pages 原样拷贝，
 * 不经过 Astro 路由，因此 @astrojs/sitemap 枚举不到它们，
 * 生成的 sitemap 里只剩首页/笔记/关于三条。
 * 这里用 customPages 把笔记补回去。
 *
 * slug 必须 encodeURIComponent：文件名里含「10%」「30%」这类 ASCII 百分号，
 * 未编码会构成非法 URL（Cloudflare 直接返回 400）。
 *
 * 用 process.cwd()（Astro 加载配置时即为项目根）而不是 import.meta.url，
 * 便于本地静态校验；读不到目录时只告警不抛错，避免整站构建失败。
 */
function noteCustomPages() {
  const dir = join(process.cwd(), 'public', 'notes');
  if (!existsSync(dir)) {
    console.warn('[sitemap] 未找到 public/notes，本次不补充笔记 URL：%s', dir);
    return [];
  }
  return readdirSync(dir)
    .filter((f) => f.endsWith('.html'))
    .map((f) => `${SITE_URL}/notes/${encodeURIComponent(f.slice(0, -'.html'.length))}`)
    .sort();
}

// Cloudflare Pages 部署配置
// 输出目录保持默认 dist/，Cloudflare Pages 会自动识别
// 站点 URL 用真实自定义域名（影响 og:image / canonical / RSS 的绝对链接生成）
export default defineConfig({
  site: SITE_URL,
  trailingSlash: 'ignore',
  build: {
    format: 'directory',
  },
  integrations: [
    mdx(),
    sitemap({ customPages: noteCustomPages() }),
  ],
  markdown: {
    shikiConfig: {
      // 双主题模式：Shiki 同时输出 light/dark 两套 token 颜色，
      // 通过 CSS 变量自动跟随站点主题切换，避免暗色模式下出现刺眼白底
      themes: {
        light: 'github-light',
        dark: 'github-dark',
      },
      // 不指定 langs：Shiki 默认已经覆盖 bash/python/js/ts/json/yaml 等常用语言
      // 如需扩展冷门语言，再用 shiki/bundle/web 的导入式 API
      wrap: true,
    },
  },
  vite: {
    build: {
      cssCodeSplit: true,
    },
  },
});