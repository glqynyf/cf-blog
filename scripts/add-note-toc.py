#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给 public/notes/ 下 115 篇独立 HTML 笔记批量添加「左侧悬浮目录」。

数据来源：每篇正文里已有的 <section class="section" id="..."> + <h2>，
不新增、不修改任何正文内容，只把已有目录数据复制一份到左侧悬浮栏。

做法：
1. 解析出该篇所有 (section id, h2 标题)，生成 <nav class="note-sidenav">
2. 正文用 <div class="note-shell"> 包一层，左侧目录用 position:fixed 悬浮，
   不改变正文 880px 居中布局
3. 注入配套 CSS + 原生 JS（滚动高亮当前章节 / 回到顶部）
4. CSS 用内联 style 兜底关键属性，避免个别笔记 <style> 解析异常导致错乱

幂等：已存在 note-sidenav 的文件会跳过。
"""
import os
import re
import sys

NOTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public', 'notes')

# 左侧悬浮目录的静态外观内联在标签上：即使 <style> 解析异常也能正确定位。
SIDENAV_STYLE = (
    "position:fixed;left:24px;top:96px;width:210px;z-index:20;"
    "max-height:calc(100vh - 140px);overflow-y:auto;"
    "background:var(--surface);border:1px solid var(--border);"
    "border-radius:8px;padding:14px 12px;font-size:12.5px;line-height:1.6;"
    "box-shadow:var(--shadow);"
)

NAV_CSS = """  /* 左侧悬浮目录（由 add-note-toc.py 注入） */
  .note-sidenav { display: none; }
  .note-sidenav__title {
    margin: 0 0 10px; font-size: 11px; font-weight: 700;
    color: var(--accent); letter-spacing: 1.5px; text-transform: uppercase;
  }
  .note-sidenav ol { list-style: none; margin: 0; padding: 0; counter-reset: snav; }
  .note-sidenav li { margin: 0; }
  .note-sidenav a {
    display: block; padding: 5px 8px; border-radius: 5px;
    color: var(--text-dim); text-decoration: none;
    border-left: 2px solid transparent; transition: all 0.2s;
  }
  .note-sidenav a::before {
    counter-increment: snav; content: counter(snav, decimal-leading-zero) "  ";
    color: var(--text-mute); font-weight: 700; font-size: 10px;
  }
  .note-sidenav a:hover { background: var(--surface-2); color: var(--text); text-decoration: none; }
  .note-sidenav a.is-active {
    background: var(--accent-soft); color: var(--accent);
    border-left-color: var(--accent); font-weight: 600;
  }
  .note-sidenav__foot {
    margin-top: 10px; padding-top: 10px; border-top: 1px solid var(--border);
  }
  .note-sidenav__top {
    display: block; text-align: center; padding: 5px 0; border-radius: 5px;
    color: var(--text-mute); text-decoration: none; font-size: 11.5px;
  }
  .note-sidenav__top:hover { background: var(--surface-2); color: var(--accent); text-decoration: none; }
  /* 宽屏才显示；窄屏继续用正文里原有的目录块 */
  @media (min-width: 1280px) {
    .note-sidenav { display: block; }
  }
"""

NAV_JS = """
(function () {
  var nav = document.querySelector('.note-sidenav');
  if (!nav) return;
  var links = nav.querySelectorAll('a[href^="#"]');
  if (!links.length) return;
  var map = {};
  var targets = [];
  links.forEach(function (a) {
    var id = a.getAttribute('href').slice(1);
    var el = document.getElementById(id);
    if (el) { map[id] = a; targets.push(el); }
  });
  function clear() {
    links.forEach(function (a) { a.classList.remove('is-active'); });
  }
  function onScroll() {
    var best = null, bestTop = -Infinity;
    for (var i = 0; i < targets.length; i++) {
      var t = targets[i].getBoundingClientRect().top;
      if (t <= 120 && t > bestTop) { bestTop = t; best = targets[i]; }
    }
    if (!best && targets.length) best = targets[0];
    if (!best) return;
    var active = map[best.id];
    if (!active) return;
    clear();
    active.classList.add('is-active');
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
"""


def escape(text: str) -> str:
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def build_sidenav(sections) -> str:
    items = ''.join(
        f'\n      <li><a href="#{sid}">{escape(title)}</a></li>'
        for sid, title in sections
    )
    # 不以换行开头：调用方紧接在 <body> 之后插入，多一个前导 \n 会多出空行
    return (
        f'<nav class="note-sidenav" style="{SIDENAV_STYLE}" aria-label="本文目录">\n'
        '  <h4 class="note-sidenav__title">本文目录</h4>\n'
        '  <ol>'
        f'{items}\n'
        '  </ol>\n'
        '  <div class="note-sidenav__foot">\n'
        '    <a class="note-sidenav__top" href="#">↑ 回到顶部</a>\n'
        '  </div>\n'
        '</nav>\n'
    )


def main() -> int:
    if not os.path.isdir(NOTES_DIR):
        print(f"错误：找不到目录 {NOTES_DIR}")
        return 1

    files = sorted(f for f in os.listdir(NOTES_DIR) if f.endswith('.html'))
    changed = skipped = failed = 0

    for name in files:
        path = os.path.join(NOTES_DIR, name)
        with open(path, encoding='utf-8') as fh:
            html = fh.read()

        if 'note-sidenav' in html:
            skipped += 1
            continue

        # 1) 解析章节（id + h2 标题）
        #    re.findall 返回 [(id, h2_inner), ...]，保持这个顺序不要反
        sections = [
            (sid, ' '.join(title.split()))
            for sid, title in re.findall(
                r'<section class="section" id="([^"]+)">\s*<h2[^>]*>(.*?)</h2>',
                html, re.S
            )
        ]
        if len(sections) < 2:
            print(f"  ✗ 章节不足，跳过：{name}（{len(sections)} 个）")
            failed += 1
            continue

        # 2) 插到 <body> 之后、stage-bar 之前
        m = re.search(r'<body>\s*\n', html)
        if not m:
            print(f"  ✗ 未找到 <body>：{name}")
            failed += 1
            continue
        html = html[:m.end()] + build_sidenav(sections) + html[m.end():]

        # 3) CSS 注入到最后一个 </style> 之前（保留原缩进前缀）
        idx = html.rfind('</style>')
        if idx == -1:
            print(f"  ✗ 未找到 </style>：{name}")
            failed += 1
            continue
        line_start = html.rfind('\n', 0, idx) + 1
        indent = html[line_start:idx]
        html = html[:line_start] + indent + NAV_CSS + html[line_start:]

        # 4) JS 放在 </body> 之前；少数笔记源文件本身缺 </body>（浏览器会自动补全），
        #    这里顺带补齐成完整文档，让结构与其余 113 篇一致。
        idx = html.rfind('</body>')
        script = '<script>\n' + NAV_JS + '</script>\n'
        if idx == -1:
            html = html.rstrip() + '\n\n' + script + '</body>\n</html>\n'
        else:
            html = html[:idx] + script + html[idx:]

        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(html)
        changed += 1

    print(f"\n完成：注入 {changed} 篇，跳过（已存在）{skipped} 篇，失败 {failed} 篇")
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
