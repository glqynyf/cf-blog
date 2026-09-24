// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// Cloudflare Pages 部署配置
// 输出目录保持默认 dist/，Cloudflare Pages 会自动识别
// 站点 URL 用真实自定义域名（影响 og:image / canonical / RSS 的绝对链接生成）
export default defineConfig({
  site: 'https://stock-blog.duckuno.com',
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