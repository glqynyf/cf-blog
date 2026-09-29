/**
 * 站点级常量。在此处修改站点标题、描述、作者、社交链接。
 * 部署到 Cloudflare Pages 后，可以再为不同环境覆写。
 */
export const SITE = {
  title: '盘面札记',
  titleEn: 'Trading Notes',
  description: '一个散户写给自己的投资笔记——认知重塑、技术分析、仓位管理、基本面选股与市场周期，共 14 章 115 篇复盘记录，不构成任何投资建议。',
  author: '盘面札记',
  authorEmail: 'service@duckuno.com',
  /** 默认 OG 图片（首页 / 笔记目录等无专属图时使用）。放在 public/ 下。 */
  defaultOgImage: '/og-default.png',
  /** 主语言 */
  lang: 'zh-CN',
  /** GitHub 仓库地址，用于显示徽章和订阅按钮 */
  github: 'https://github.com/glqynyf/cf-blog',
} as const;
