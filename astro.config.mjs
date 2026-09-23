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
      langs: ['bash', 'python', 'javascript', 'typescript', 'json', 'yaml', 'md'],
      wrap: true,
    },
  },
  vite: {
    build: {
      cssCodeSplit: true,
    },
  },
});