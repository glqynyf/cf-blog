/**
 * 站点级常量。在此处修改站点标题、描述、作者、社交链接。
 * 部署到 Cloudflare Pages 后，可以再为不同环境覆写。
 */
export const SITE = {
  title: '盘面札记',
  titleEn: 'Trading Notes',
  description: '一个散户的炒股心得与常用技术指标实战记录——K 线、均线、MACD、KDJ 等指标的系统性整理，以及复盘中的反思。',
  author: '盘面札记',
  authorEmail: 'service@duckuno.com',
  /** 默认 OG 图片（首页 / 笔记目录等无专属图时使用）。放在 public/ 下。 */
  defaultOgImage: '/og-default.png',
  /** 主语言 */
  lang: 'zh-CN',
  /** GitHub 仓库地址，用于显示徽章和订阅按钮 */
  github: 'https://github.com/glqynyf/cf-blog',
} as const;
