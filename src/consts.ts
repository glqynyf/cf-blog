/**
 * 站点级常量。在此处修改站点标题、描述、作者、社交链接。
 * 部署到 Cloudflare Pages 后，可以再为不同环境覆写。
 */
export const SITE = {
  title: '盘面札记',
  titleEn: 'Trading Notes',
  description: '一个散户的炒股心得与常用技术指标实战记录——K 线、均线、MACD、KDJ 等指标的系统性整理，以及复盘中的反思。',
  author: '盘面札记',
  authorEmail: 'hello@example.com',
  /** 默认 OG 图片相对路径（建议 1200×630）。放在 public/ 下。 */
  defaultOgImage: '/og-default.png',
  /** 主语言 */
  lang: 'zh-CN',
  /** GitHub 仓库地址，用于显示徽章和订阅按钮 */
  github: 'https://github.com/your-username/cf-blog',
} as const;

export const NAV = [
  { href: '/', label: '首页' },
  { href: '/posts', label: '文章' },
  { href: '/tags', label: '标签' },
  { href: '/about', label: '关于' },
] as const;

/**
 * 推荐的内置标签（不在此处出现的标签依然可以正常使用，只是不会显示在首页 chip 中）。
 */
export const FEATURED_TAGS = [
  '入门',
  '技术指标',
  '交易心得',
  '风险控制',
  '复盘',
] as const;