# 盘面札记 · Trading Notes

一个用 [Astro](https://astro.build) 构建的静态投资笔记站，收录 **115 篇** A 股投资复盘笔记，分 **14 个章节**。托管在 GitHub，通过 [Cloudflare Pages](https://pages.cloudflare.com) 自动部署。

线上地址：<https://stock-blog.duckuno.com>

> ⚠️ 本站所有内容均为个人复盘与学习笔记，**不构成任何投资建议**。入市有风险，决策需谨慎。

---

## 🧩 这个站点是怎么组成的

这是本项目最需要先理解的一点，它和常规 Astro 博客**不一样**：

```
内容层：public/notes/*.html     ← 115 篇笔记，自包含的独立 HTML 文件
                                    不经过 Astro 路由、不套用 BaseLayout
                                    自带深色主题 + 内联 <style> / <script>
                                    ────────────────────────────────
外壳层：src/pages/*.astro        ← 仅 3 个页面：首页 / 笔记目录 / 关于
                                    这些才走 Astro 构建、共享 Header/Footer
```

也就是说：**Astro 在这个项目里不是内容系统，而是列表页的渲染器**。

笔记放在 `public/` 而不是 `src/content/`，是因为它们是成品 HTML——直接被原样拷贝进 `dist/`，不走内容集合、没有 frontmatter、没有 Markdown 编译。代价是内容层与外壳层是两套独立的样式体系：

| | 外壳页（3 个 `.astro`） | 笔记（115 个 `.html`） |
|---|---|---|
| 布局 | `BaseLayout.astro`（Header / Footer / SEO） | 各自内联，无 Header/Footer |
| 主题变量 | `src/styles/global.css` | 每篇自带一份 `:root` 变量 |
| 目录 | 无 | `.note-sidenav`（≥1440px 悬浮）+ `.toc`（窄屏） |
| 路由 | Astro 路由 | `public/` 直出 |

**改外壳页样式不会影响笔记，改笔记 HTML 也不会影响外壳页。** 两者要分别改。

## ✨ 站点现状

- 📚 **115 篇笔记 / 14 章节**——按 `S00`–`S13` 编号排列，文件名即标题
- 🗂️ **五个板块**——首页、目录页、关于页共用同一套分组
- 📖 **单页双目录**——宽屏左侧悬浮目录 + 窄屏正文目录，滚动高亮当前章节
- 🔍 **手写 sitemap**——`/sitemap.xml` 为唯一规范入口（见下文「为什么不用 @astrojs/sitemap」）
- 🎨 **固定深色主题**——`BaseLayout` 内联写入 `data-theme="dark"`，无主题切换
- 🚀 **零 JS 框架运行时**——页面无 React/Vue 等 hydration，只用少量原生脚本
- ⚡ **零配置部署**——推送到 `main`，Cloudflare Pages 自动构建发布

## 📁 笔记命名规范

文件名本身就是全部元数据，**没有 frontmatter**：

```
public/notes/S12-07-北向资金是什么.html
              │  │  └─ 标题，同时也是 slug 和链接
              │  └──── 章节内序号（两位数字，决定排序）
              └─────── 章节号（S00–S13，决定归属板块）
```

`src/utils/notes.ts` 在构建时扫描该目录，按前缀解析出章节与序号，**同一次构建只读一次磁盘**。因此：

- 新增笔记 = 往 `public/notes/` 丢一个符合命名的 HTML，**不需要改任何配置**
- 章节显示名在 `src/utils/notes.ts` 的 `STAGE_TITLES` 里维护
- 章节增删会自动反映到首页、目录页、关于页和 sitemap

### 章节一览

| 章节 | 主题 | 篇数 |
|---|---|---|
| S00 | 认知重塑 · 破除散户思维 | 9 |
| S01 | 心态纪律 · 交易心理与情绪管理 | 5 |
| S02 | K线基础 · 单根与组合形态 | 3 |
| S03 | 量价关系 · 量是因价是果 | 3 |
| S04 | 均线趋势 · 趋势线与周期选择 | 3 |
| S05 | 技术指标 · MA / KDJ / MACD / RSI / BOLL | 11 |
| S06 | 形态学 · 双重顶底与底部反转 | 10 |
| S07 | 左侧右侧 · 进出场时机与分时盘口 | 6 |
| S08 | 止盈止损 · 卖出判断标准 | 6 |
| S09 | 仓位管理 · 532 法则与凯利公式 | 13 |
| S10 | 选股方法 · 自上而下与自下而上 | 13 |
| S11 | 分红回购 · 除权除息与税务 | 6 |
| S12 | 筹码主力 · 资金面与涨跌停规则 | 16 |
| S13 | 市场周期 · 政策底到出货的情绪演绎 | 11 |

### 五个板块

外壳页把这 14 章归为 5 个板块，篇数**在构建时从实际数据算出**，不手写：

| 板块 | 章节 | 篇数 |
|---|---|---|
| 认知与心态 | S00–S01 | 14 |
| 技术分析 | S02–S07 | 36 |
| 风控与仓位 | S08–S09 | 19 |
| 基本面与选股 | S10–S11 | 19 |
| 资金面与市场周期 | S12–S13 | 27 |

## 🛠️ 本地开发

需要 Node.js 20+（根目录有 `.nvmrc`，推荐用 [fnm](https://github.com/Schniz/fnm) 或 [nvm](https://github.com/nvm-sh/nvm)）。

```bash
npm install        # 安装依赖
npm run dev        # 开发服务器（http://localhost:4321）
npm run build      # 类型检查 + 构建到 dist/
npm run preview    # 本地预览构建产物
```

`build` 脚本是 `astro check && astro build`，**类型检查失败会阻断构建**。

## ✍️ 如何新增一篇笔记

1. 新建 `public/notes/S{章}-{序号}-{标题}.html`，沿用现有笔记的完整结构（可直接复制 `S12-07-北向资金是什么.html` 作为骨架，它包含 stage-bar、summary-card、toc、note-sidenav、canonical 等全部构件）
2. 写完后确认**没有** Astro frontmatter——笔记不走内容集合
3. 跑一次 `python3 scripts/check-note-css.py`，确认内联 CSS 没有被静默吃掉（见下文「已知约束」）
4. `npm run build` 后检查 `/notes/` 与 `/sitemap.xml` 是否都出现新条目

新增**章节**时才需要改代码：在 `src/utils/notes.ts` 的 `STAGE_TITLES` 里补一条显示名。

## 📂 项目结构

```
.
├── astro.config.mjs          # Astro 配置（site / MDX / Shiki 双主题）
├── src/
│   ├── consts.ts             # 站点元数据（标题、描述、作者、GitHub 地址）
│   ├── utils/notes.ts        # 笔记扫描 + 章节分组 + STAGE_TITLES
│   ├── components/           # Header（导航） / Footer
│   ├── layouts/              # BaseLayout（外壳页统一布局 + SEO）
│   ├── pages/
│   │   ├── index.astro       # 首页
│   │   ├── notes/index.astro # 笔记总目录（可按章节筛选）
│   │   ├── about.astro       # 关于页
│   │   └── sitemap.xml.ts    # 自定义 sitemap 端点
│   └── styles/global.css     # 设计令牌 + 外壳页全局样式
├── public/
│   ├── notes/                # 👈 115 篇笔记，自包含 HTML
│   ├── robots.txt            # 指向 /sitemap.xml
│   ├── og-default.png
│   └── favicon.svg
└── scripts/                  # 批量维护脚本（Python）
```

## 🔧 维护脚本

115 篇笔记需要成批改动时，用 `scripts/` 下的 Python 脚本处理，**改完逐篇抽查**。除 `rewrite-note-commits.py` 外都是幂等的，可重复执行。

| 脚本 | 作用 |
|---|---|
| `redesign-note-toc.py` | 重做正文目录 `<nav class="toc">`（编号徽章 + 时间轴引导线 + 滚动高亮） |
| `redesign-note-sidenav.py` | 重做宽屏悬浮目录 `.note-sidenav`（≥1440px 显示） |
| `add-note-toc.py` | 为笔记批量生成左侧悬浮目录（从 `<section id>` + `<h2>` 提取） |
| `add-note-nav.py` | 注入「返回」入口（笔记脱离 Astro，没有站点 Header） |
| `add-note-canonical.py` | 注入 `<link rel="canonical">` |
| `fix-note-css-splice.py` | 修「注释插在选择器与 `{` 之间」导致的后代选择器失效 |
| `fix-note-css-badstring.py` | 修 `content: """` 未闭合字符串吞掉 `}` 导致的整段 CSS 失效 |
| `check-note-css.py` | **只读检查**：抓上面两类静默失效 + 关键规则缺失，改完 CSS 跑一次 |
| `generate-og-images.py` | 批量生成 OG 分享图 |
| `post-images/` | 单篇文章配图生成 |
| `push-via-api.py` | **`github.com` 主站不可达时的应急推送**，改走 `api.github.com` |
| `rewrite-note-commits.py` | 一次性工具：把批量 commit 拆成每篇笔记一个（**不幂等**，需完整 git 对象链，只能走 `git push`） |

> ⚠️ `generate-og-images.py` 与 `post-images/` 读取的是**已不存在的** `src/content/posts/`，属于旧内容结构的遗留，当前跑不通。
>
> 站点目前只有一张 `public/og-default.png` 作为默认 OG 图，`public/og/` 是空目录——115 篇笔记**没有各自的分享图**，全部回落到默认图。

## 🔍 SEO

### 为什么不用 @astrojs/sitemap

改用自己写的 `src/pages/sitemap.xml.ts`，两个原因：

1. `@astrojs/sitemap` 固定生成 `sitemap-0.xml` + `sitemap-index.xml`，而爬虫、Search Console、绝大多数工具默认找的是 **`/sitemap.xml`**。本项目原先没有这个路径，请求它会被 SPA fallback 返回首页 HTML（HTTP 200 + `text/html`），看起来就像「sitemap 内容完全不对」。
2. 它只枚举 Astro 自己构建出的路由。`public/notes/` 下的 115 篇静态 HTML 一篇都进不去，得额外用 `customPages` 手工补。

改为自己生成后：单一入口、无分片、路径符合惯例，且能直接扫 `public/notes/`。

### 静态页的 canonical

笔记是独立 HTML、不经 `BaseLayout`，默认没有 canonical。Cloudflare 对 `/notes/X` 和 `/notes/X.html` **都返回 200**，搜索引擎会当成两份重复内容。`add-note-canonical.py` 负责补齐。

## 🌐 部署

Cloudflare Pages 已通过 Git 集成配置好，**推送到 `main` 即自动部署**：

| 配置项 | 值 |
|---|---|
| Framework preset | Astro |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Node version | `20`（Environment variable `NODE_VERSION=20`） |

部署耗时约 100 秒。**验证线上更新时务必给 URL 加 cache-buster**（如 `?cb=1234`）—— Cloudflare 边缘对静态 HTML 有长达 7 天的 `s-maxage` 缓存，不加会读到旧内容，误判成「新构建没生效」。

### 推送失败：`Error in the HTTP2 framing layer`

某些网络下 `github.com` 主站不可达（DNS 解析到的 IP 连不上，备用 anycast 入口也分钟级波动），表现为 `git push` 报 `Error in the HTTP2 framing layer`。此时 **`api.github.com` 通常仍然可用**，且用的是同一份账号凭据：

```bash
python3 scripts/push-via-api.py --dry-run   # 先比对，确认要推什么
python3 scripts/push-via-api.py             # 走 Git Data API 推送
```

⚠️ 这会留下**本地与远端 SHA 不一致**（内容完全一致，只是 commit 元数据不同）。网络恢复后收敛一次即可，不会丢内容：

```bash
git fetch origin && git reset --hard origin/main
```

## ⚠️ 已知约束

维护这个项目时容易踩的坑：

- **文件名含 `%` 必须编码**。有 4 篇笔记标题里带「10%」「30%」这类 ASCII 百分号。生成链接时一律走 `encodeURIComponent(slug)`，裸 `%` 会构成非法 URL，Cloudflare 直接返回 **400**。（中文和全角 `？` 没问题，只有 ASCII `%` 会炸）
- **笔记 CSS 坏了，肉眼和 grep 都看不出来**。本项目已经被同一类问题咬过两次：注释插在选择器与 `{` 之间（变成永不匹配的后代选择器）、`content: """` 未闭合字符串吞掉行尾 `}`（让解析器卡在前一个 `{` 里，后续规则全部嵌套失效，78 篇的宽屏侧栏就是这样整体变回浏览器默认样式）。两种情况**源码都写得清清楚楚**，`count('{') == count('}')` 也全部「通过」——因为整体是配平的，只是深度错位。
  改完笔记 CSS 务必跑一次检查，它能同时抓住这两类：
  ```bash
  python3 scripts/check-note-css.py            # 全部笔记
  python3 scripts/check-note-css.py --verbose  # 列出每个问题
  ```
  退出码 0 = 通过。词法校验按 CSS Syntax L3 规范处理注释、字符串、以及「字符串内遇换行 → bad-string 在换行处恢复」——**换行位置决定了整条规则压在一行时会不会连带吞掉闭合括号**，所以 `grep` 计数完全判断不出影响面（115 篇都含 `content: """`，但只有 78 篇真的坏）。
- **站点没有 404 页**。任何未知路径都会被 SPA fallback 返回**首页 HTML + HTTP 200**。诊断时不能靠状态码判断文件是否存在，要看内容特征；删除文件后边缘缓存还可能继续返回旧页面最长 7 天。
- **内容层与外壳页样式互不影响**。改 `global.css` 不会改变任何一篇笔记的外观，反之亦然。
- **`build` 会跑类型检查**。`build` = `astro check && astro build`，strict 模式带 `noImplicitAny`，**类型错误会直接中断构建**，而本机没有 node 跑不了 build 验证、构建日志又只在 Cloudflare 后台面板里拿不到，所以任何新增的 `.ts` **函数参数必须写显式类型注解**——只写 JSDoc `@param {string}` 不会被采纳（`sitemap.xml.ts` 的 `staticUrls(dirName)` 就因此挂掉过一次，排查花了三轮二分）。
  排查手段：用 `git log` 逐次比对该提交在 GitHub 上的 Cloudflare check-run（`conclusion: failure/success`）做二分，一轮约 2 分钟。
- **`scripts/` 里的 Python 脚本在本机 Python 3.9 上跑**。别用 `str | None` 这类 3.10+ 的注解语法，会在导入时直接 `TypeError`。

## 🔧 常用配置位置

| 想要修改的内容 | 文件 |
|---|---|
| 站点标题、描述、作者、GitHub 地址 | `src/consts.ts` |
| 章节显示名 | `src/utils/notes.ts` 的 `STAGE_TITLES` |
| 导航菜单项 | `src/components/Header.astro` 的 `navItems` |
| 外壳页配色与间距令牌 | `src/styles/global.css` 顶部的 `:root` |
| 关于页的板块分组 | `src/pages/about.astro` 的 `BOARDS` |
| 站点 URL | `astro.config.mjs` 的 `SITE_URL` + `src/pages/sitemap.xml.ts` 的 `SITE` |

## 📄 License

代码部分（不含笔记内容）采用 [MIT License](LICENSE)。笔记内容采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)——署名、非商业、相同方式共享。

---

Made with ☕ & 📈
