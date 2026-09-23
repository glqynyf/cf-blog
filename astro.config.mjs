// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// Cloudflare Pages 部署配置
// 输出目录保持默认 dist/，Cloudflare Pages 会自动识别
// 站点 URL 在部署到正式域名后填入，用于 sitemap 和 RSS 的绝对链接
export default defineConfig({
  site: 'https://example.pages.dev',
  trailingSlash: 'ignore',
  build: {
    format: 'directory',
  },
  integrations: [
    mdx(),
    sitemap(),
  ],
  markdown: {
    shikiConfig: {
      theme: 'github-light',
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