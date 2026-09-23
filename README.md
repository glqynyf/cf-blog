# 盘面札记 · Trading Notes

一个用 [Astro](https://astro.build) 构建的静态博客，记录炒股心得与技术指标实战笔记。托管在 GitHub，通过 [Cloudflare Pages](https://pages.cloudflare.com) 自动部署。

> ⚠️ 本站所有内容均为个人复盘与学习笔记，**不构成任何投资建议**。入市有风险，决策需谨慎。

## ✨ 特性

- 📝 **纯 Markdown/MDX 写作**——文章存放在 `src/content/posts/`，Frontmatter 校验
- 🎨 **A 股配色 + 明暗双主题**——红涨绿跌，符合中国交易者直觉；支持一键切换深色模式
- 🏷️ **标签系统 + 标签聚合页**——自动统计、自动路由
- 📡 **RSS 订阅 + sitemap**——`/rss.xml`、`/sitemap-index.xml`
- ⚡ **零配置部署**——推送到 GitHub，Cloudflare Pages 自动构建并发布
- 🚀 **零 JS 框架运行时**——首屏只有少量交互脚本（主题切换），加载极快

## 🛠️ 本地开发

需要 Node.js 20+（项目根目录有 `.nvmrc`，推荐用 [fnm](https://github.com/Schniz/fnm) 或 [nvm](https://github.com/nvm-sh/nvm) 管理版本）。

```bash
# 安装依赖
npm install

# 启动开发服务器（默认 http://localhost:4321）
npm run dev

# 构建生产版本（输出到 dist/）
npm run build

# 本地预览构建产物
npm run preview
```

## 📁 项目结构

```
.
├── astro.config.mjs       # Astro 配置（集成 MDX + sitemap）
├── src/
│   ├── consts.ts          # 站点元数据（标题、描述、社交链接等）
│   ├── content.config.ts  # 文章集合的 schema 定义
│   ├── utils.ts           # 排序、标签统计、阅读时长等工具函数
│   ├── components/        # Header / Footer / PostCard / TagList / ThemeToggle
│   ├── layouts/           # BaseLayout / PostLayout
│   ├── pages/             # 路由（首页 / 文章 / 标签 / RSS / sitemap）
│   ├── content/posts/     # 👈 所有 Markdown 文章放在这里
│   └── styles/global.css  # 全局样式 + 设计系统变量
├── public/                # 静态资源（favicon、og 图等）
└── README.md
```

## ✍️ 如何写新文章

在 `src/content/posts/` 下新建一个 `.md` 或 `.mdx` 文件，按下面的格式填写 Frontmatter：

```markdown
---
title: "你的文章标题"
summary: "一段不超过 200 字的导语，会显示在首页和 RSS 中。"
pubDate: 2026-03-15          # 必填，YYYY-MM-DD
updatedDate: 2026-03-20      # 可选
tags: ["技术指标", "交易心得"]  # 可选，建议 1~5 个
draft: false                 # true 时仅开发模式可见
featured: true               # 是否在首页精选区显示
---

文章正文使用标准 Markdown 语法。支持代码块、表格、引用、列表、数学公式等。
```

保存后，刷新浏览器即可在首页和对应标签页看到新内容。

## 🌐 部署到 Cloudflare Pages（Git 集成）

### 第一步：推送到 GitHub

```bash
# 在 GitHub 上新建一个空仓库（不要勾选 README / .gitignore / License）
# 然后在本地执行：

git init                                  # 已经初始化过可跳过
git add .
git commit -m "chore: initial commit"
git branch -M main
git remote add origin git@github.com:你的用户名/你的仓库名.git
git push -u origin main
```

### 第二步：在 Cloudflare 控制台创建 Pages 项目

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 左侧菜单 **Workers & Pages** → **Create application** → **Pages** → **Connect to Git**
3. 选择刚才创建的 GitHub 仓库
4. **Build settings** 按如下填写：

   | 配置项 | 值 |
   |--------|-----|
   | Framework preset | **Astro** |
   | Build command | `npm run build` |
   | Build output directory | `dist` |
   | Root directory | *(留空)* |
   | Node version | `20`（在 Environment variables 中设置 `NODE_VERSION=20`） |

5. **Environment variables**（可选，但推荐）：
   - `NODE_VERSION` = `20`

6. 点击 **Save and Deploy**，Cloudflare 会自动拉取代码并构建。

### 第三步：自定义域名（可选）

部署完成后，Cloudflare 会给你一个 `xxx.pages.dev` 的默认域名。如果你有自己的域名：

1. 在 Cloudflare Pages 项目里 **Custom domains** → **Set up a custom domain**
2. 按提示在 DNS 里添加 CNAME 记录

### 第四步：每次更新

之后只需要在本地写文章、提交、推送即可。Cloudflare Pages 会监听 `main` 分支的 push，**自动触发部署**。

```bash
git add .
git commit -m "post: 新增 XXX 一文"
git push
```

## 🔧 常用配置位置

| 想要修改的内容 | 文件 |
|----------------|------|
| 站点标题、描述、社交链接 | `src/consts.ts` |
| 主题色（红涨绿跌 / 主青绿色） | `src/styles/global.css` 顶部的 `:root` 变量 |
| 文章 schema（强制字段） | `src/content.config.ts` |
| 导航菜单项 | `src/components/Header.astro` 中的 `navItems` |
| Cloudflare Pages 构建配置 | `wrangler.toml`（如有）或 Cloudflare 控制台 |

## 📝 写作约定

为了让站点风格统一，建议：

- **每篇文章都有 `summary`**，决定它在首页和 RSS 中的第一印象。
- **`tags` 控制在 5 个以内**，复用已有标签，避免出现过多同义近义词。
- **正文尽量给出可操作结论**——读者读完后应该知道"下一步能做什么"。
- **风险提示**：每篇涉及具体操作的复盘文章，文末保留一段"风险提示"提醒。

## 📄 License

代码部分（不含文章内容）采用 [MIT License](LICENSE)。文章内容采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)——署名、非商业、相同方式共享。

---

Made with ☕ & 📈