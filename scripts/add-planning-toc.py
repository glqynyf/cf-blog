#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给 public/planning/ 下的持仓规划文档批量添加「本文目录」+「返回规划」+ 左侧悬浮目录。

与笔记的差异：
  1. 规划文档原本只有裸 <h2>，没有 <section id>。这里给每个 <h2> 补 id 作为锚点，
     不改动任何正文文字。
  2. 配色跟随文档自身（GitHub 深色调，强调色是蓝色 #58a6ff），
     而不是站点的橙色 —— 文档里满屏都是蓝色 h2 和蓝色描边，塞橙色会打架。
     规划文档没有定义任何 CSS 变量，所以这里用硬编码色值。
  3. 正文宽 1200px（笔记是 880px），左侧要空出 200px 侧栏需要视口 ≥1680px，
     断点比笔记的 1440px 更高。

幂等：已存在 doc-sidenav 的文件会跳过。
"""
import os
import re
import sys

PLANNING_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'public', 'planning'
)

# 规划文档自身配色（硬编码，因该文档未定义 CSS 变量）
C_BG = '#0d1117'
C_SURFACE = '#161b22'
C_SURFACE2 = '#21262d'
C_BORDER = '#30363d'
C_TEXT = '#e6edf3'
C_DIM = '#c9d1d9'
C_MUTE = '#8b949e'
C_ACCENT = '#58a6ff'
C_SOFT = 'rgba(56,139,253,.12)'

# 正文 1200px 居中 → 内容占 50vw±600，侧栏宽 200 + 间隙 24 → 左边线在 50vw-824
# 该值 ≥0 需要视口 ≥1648px，断点取 1680 留一点余量
SIDENAV_STYLE = (
    'position:fixed;left:calc(50vw - 824px);top:96px;width:200px;z-index:20;'
    'max-height:calc(100vh - 140px);overflow-y:auto;'
    f'background:{C_SURFACE};border:1px solid {C_BORDER};'
    'border-radius:8px;padding:14px 12px;font-size:12.5px;line-height:1.6;'
    'box-shadow:0 8px 30px rgba(0,0,0,.4);'
)

BACK_STYLE = (
    'display:inline-flex;align-items:center;gap:6px;padding:5px 12px;'
    f'border-radius:6px;background:{C_SURFACE2};border:1px solid {C_BORDER};'
    f'color:{C_DIM};text-decoration:none;font-size:13px;font-weight:600;'
    'line-height:1.4;transition:all .2s;'
)

NAV_CSS = f'''  /* ---------- 返回入口（由 add-planning-toc.py 注入） ---------- */
  .doc-nav {{ margin-bottom: 18px; }}
  .doc-nav__back:hover {{
    background: {C_SOFT} !important;
    border-color: {C_ACCENT} !important;
    color: {C_ACCENT} !important;
    text-decoration: none !important;
  }}

  /* ---------- 本文目录（窄屏主力，宽屏与侧栏并存） ---------- */
  .doc-toc {{
    position: relative; margin-bottom: 40px; padding: 18px 22px 16px;
    background: radial-gradient(120% 130% at 0% 0%, {C_SOFT}, transparent 55%), {C_SURFACE};
    border: 1px solid {C_BORDER}; border-radius: 10px;
  }}
  .doc-toc::before {{
    content: ''; position: absolute; left: 0; right: 0; top: 0; height: 2px;
    background: linear-gradient(90deg, {C_ACCENT}, transparent 72%);
  }}
  .doc-toc h4 {{
    display: flex; align-items: center; gap: 10px; margin-bottom: 14px;
    font-size: 12px; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: {C_ACCENT};
  }}
  .doc-toc h4::before {{
    content: ''; width: 4px; height: 13px; flex-shrink: 0;
    border-radius: 2px; background: {C_ACCENT};
  }}
  .doc-toc__count {{
    margin-left: auto; padding: 2px 9px; border-radius: 999px;
    background: {C_SOFT}; border: 1px solid rgba(56,139,253,.3);
    color: {C_ACCENT}; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 10px; font-weight: 700; letter-spacing: .5px; text-transform: none;
  }}
  .doc-toc ol {{
    position: relative; list-style: none; counter-reset: dtoc;
    margin: 0; padding: 0;
  }}
  .doc-toc ol::before {{
    content: ''; position: absolute; left: 25px; top: 18px; bottom: 18px; width: 1px;
    background: linear-gradient(180deg, {C_BORDER} 0%, {C_BORDER} 70%, transparent 100%);
  }}
  .doc-toc li {{ counter-increment: dtoc; position: relative; margin: 0; padding: 0; }}
  .doc-toc a {{
    display: flex; align-items: center; gap: 12px; padding: 6px 12px;
    border-radius: 8px; color: {C_DIM}; font-size: 14px; line-height: 1.5;
    text-decoration: none; transition: background .18s, color .18s, box-shadow .18s;
  }}
  .doc-toc a::before {{
    content: counter(dtoc, decimal-leading-zero);
    position: relative; z-index: 1; display: inline-flex;
    align-items: center; justify-content: center; flex-shrink: 0;
    width: 24px; height: 18px; border-radius: 5px;
    background: {C_SURFACE2}; border: 1px solid {C_BORDER};
    color: {C_MUTE}; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 10px; font-weight: 700;
  }}
  .doc-toc a:hover {{ background: {C_SURFACE2}; color: {C_TEXT}; text-decoration: none; }}
  .doc-toc a:hover::before {{ border-color: {C_ACCENT}; color: {C_ACCENT}; }}
  .doc-toc a.is-active {{
    background: {C_SOFT}; box-shadow: inset 3px 0 0 {C_ACCENT}; color: {C_TEXT};
  }}
  .doc-toc a.is-active::before {{
    background: {C_ACCENT}; border-color: {C_ACCENT}; color: {C_BG};
  }}

  /* ---------- 左侧悬浮目录（视口足够宽才显示，否则会压住正文） ---------- */
  .doc-sidenav {{ display: none; }}
  .doc-sidenav::before {{
    content: ''; position: absolute; left: 0; right: 0; top: 0; height: 2px;
    border-radius: 8px 8px 0 0;
    background: linear-gradient(90deg, {C_ACCENT}, transparent 78%);
  }}
  .doc-sidenav__title {{
    display: flex; align-items: center; gap: 6px;
    margin: 0 0 10px; padding-bottom: 8px;
    border-bottom: 1px solid {C_BORDER};
    font-size: 11px; font-weight: 700; color: {C_ACCENT};
    letter-spacing: 1.5px; text-transform: uppercase;
  }}
  .doc-sidenav__title::before {{
    content: ''; width: 3px; height: 11px; flex-shrink: 0;
    border-radius: 2px; background: {C_ACCENT};
  }}
  .doc-sidenav__count {{
    margin-left: auto; padding: 1px 7px; border-radius: 999px;
    background: {C_SOFT}; border: 1px solid rgba(56,139,253,.3);
    color: {C_ACCENT};
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 10px; font-weight: 700; letter-spacing: .5px; text-transform: none;
  }}
  .doc-sidenav ol {{
    position: relative; list-style: none; margin: 0; padding: 0;
    counter-reset: dsnav;
  }}
  .doc-sidenav ol::before {{
    content: ''; position: absolute; left: 9px; top: 12px; bottom: 12px; width: 1px;
    background: linear-gradient(180deg, {C_BORDER} 0%, {C_BORDER} 70%, transparent 100%);
  }}
  .doc-sidenav li {{ margin: 0; }}
  .doc-sidenav ol a {{
    position: relative; display: flex; align-items: center; gap: 8px;
    padding: 5px 6px; border-radius: 6px;
    border-left: 2px solid transparent; color: {C_DIM};
    font-size: 12.5px; line-height: 1.5; text-decoration: none;
    transition: background .18s, color .18s, border-color .18s;
  }}
  .doc-sidenav ol a::before {{
    counter-increment: dsnav; content: counter(dsnav, decimal-leading-zero);
    position: relative; z-index: 1;
    display: inline-flex; align-items: center; justify-content: center;
    flex-shrink: 0; width: 18px; height: 18px; border-radius: 5px;
    background: {C_SURFACE2}; border: 1px solid {C_BORDER};
    color: {C_MUTE}; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 9.5px; font-weight: 700;
  }}
  .doc-sidenav ol a:hover {{
    background: {C_SURFACE2}; color: {C_TEXT}; text-decoration: none;
  }}
  .doc-sidenav ol a.is-active {{
    background: {C_SOFT}; border-left-color: {C_ACCENT}; color: {C_TEXT};
  }}
  .doc-sidenav ol a.is-active::before {{
    background: {C_ACCENT}; border-color: {C_ACCENT}; color: {C_BG};
  }}
  .doc-sidenav__foot {{
    margin-top: 10px; padding-top: 10px; border-top: 1px solid {C_BORDER};
  }}
  .doc-sidenav__top {{
    display: block; text-align: center; padding: 5px 0; border-radius: 5px;
    color: {C_MUTE}; text-decoration: none; font-size: 11.5px;
  }}
  .doc-sidenav__top:hover {{ background: {C_SURFACE2}; color: {C_ACCENT}; text-decoration: none; }}

  /* 锚点跳转时给标题留出上方余量 */
  h2[id] {{ scroll-margin-top: 24px; }}

  @media (max-width: 640px) {{
    .doc-toc {{ padding: 14px 14px 12px; }}
    .doc-toc a {{ font-size: 13.5px; padding: 5px 8px; gap: 8px; }}
    .doc-toc ol::before {{ left: 21px; }}
  }}
  /* 正文 1200px 居中，留出 200px 侧栏 + 24px 间隙需要视口 ≥1680px */
  @media (min-width: 1680px) {{
    .doc-sidenav {{ display: block; }}
  }}
'''

NAV_JS = """
(function () {
  var groups = [document.querySelector('.doc-sidenav'), document.querySelector('.doc-toc')];
  var targets = [];
  var map = {};
  groups.forEach(function (nav) {
    if (!nav) return;
    nav.querySelectorAll('a[href^="#"]').forEach(function (a) {
      var id = a.getAttribute('href').slice(1);
      if (map[id]) return;
      var el = document.getElementById(id);
      if (el) { map[id] = a; targets.push(el); }
    });
  });
  if (!targets.length) return;

  function clear() {
    Object.keys(map).forEach(function (id) { map[id].classList.remove('is-active'); });
  }
  function onScroll() {
    var best = null, bestTop = -Infinity;
    for (var i = 0; i < targets.length; i++) {
      var t = targets[i].getBoundingClientRect().top;
      if (t <= 140 && t > bestTop) { bestTop = t; best = targets[i]; }
    }
    if (!best && targets.length) best = targets[0];
    if (!best) return;
    var active = map[best.id];
    if (!active) return;
    clear();
    active.classList.add('is-active');
    // 同一个 id 在两个目录里各有一个链接，上面只记了第一个
    var links = document.querySelectorAll('a[href="#' + best.id + '"]');
    links.forEach(function (a) { a.classList.add('is-active'); });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
"""


def escape(text: str) -> str:
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def slug_for(index: int, title: str) -> str:
    """sec-1 … sec-13，编号即目录序号，和正文顺序一一对应且稳定。"""
    return 'sec-%d' % index


def build_toc(sections) -> str:
    items = ''.join(
        f'\n    <li><a href="#{sid}">{escape(title)}</a></li>'
        for sid, title in sections
    )
    return (
        '<nav class="doc-toc" aria-label="本文目录">\n'
        f'  <h4>本文目录<span class="doc-toc__count">{len(sections)}</span></h4>\n'
        '  <ol>'
        f'{items}\n'
        '  </ol>\n'
        '</nav>\n'
    )


def build_sidenav(sections) -> str:
    items = ''.join(
        f'\n      <li><a href="#{sid}">{escape(title)}</a></li>'
        for sid, title in sections
    )
    return (
        f'<nav class="doc-sidenav" style="{SIDENAV_STYLE}" aria-label="本文目录">\n'
        f'  <h4 class="doc-sidenav__title">本文目录<span class="doc-sidenav__count">{len(sections)}</span></h4>\n'
        '  <ol>'
        f'{items}\n'
        '  </ol>\n'
        '  <div class="doc-sidenav__foot">\n'
        '    <a class="doc-sidenav__top" href="#">↑ 回到顶部</a>\n'
        '  </div>\n'
        '</nav>\n'
    )


def build_backnav() -> str:
    return (
        '<div class="doc-nav">\n'
        f'  <a class="doc-nav__back" href="/planning/" style="{BACK_STYLE}">← 返回规划</a>\n'
        '</div>\n'
    )


def main() -> int:
    if not os.path.isdir(PLANNING_DIR):
        print(f'错误：找不到目录 {PLANNING_DIR}')
        return 1

    files = sorted(f for f in os.listdir(PLANNING_DIR) if f.endswith('.html'))
    changed = skipped = failed = 0

    for name in files:
        path = os.path.join(PLANNING_DIR, name)
        with open(path, encoding='utf-8') as fh:
            html = fh.read()

        if 'doc-sidenav' in html:
            skipped += 1
            continue

        original_html = html

        # 1) 解析 <h2>，同时给它们补 id 作为锚点（不动任何文字）
        #
        # 必须用单次 re.sub 原子完成，不能「先 finditer 记位置、再循环里改字符串」：
        # 每插入一次 ' id="sec-N"' 都会改变长度，后续 m.start() 全部前移，
        # 切分点错位会把分区注释和正文一起吞掉（踩过，见下方 assert）。
        headings = list(re.finditer(r'<h2([^>]*)>(.*?)</h2>', html, re.S))
        if len(headings) < 2:
            print(f'  ✗ 章节不足，跳过：{name}（{len(headings)} 个）')
            failed += 1
            continue

        sections = []
        for i, m in enumerate(headings, 1):
            title = ' '.join(re.sub(r'<[^>]+>', '', m.group(2)).split())
            sid = slug_for(i, title)
            sections.append((sid, title))

        counter = {'n': 0}

        def add_id(m):
            """给没有 id 的 <h2> 补锚点；已有 id 的原样返回。"""
            attrs = m.group(1)
            if 'id=' in attrs:
                return m.group(0)
            counter['n'] += 1
            return '<h2 id="sec-%d"%s>%s</h2>' % (
                counter['n'], attrs, m.group(2)
            )

        html = re.sub(r'<h2([^>]*)>(.*?)</h2>', add_id, html, flags=re.S)
        assert counter['n'] == len(headings), (
            'h2 计数不符：预期 %d，实际补 id %d' % (len(headings), counter['n'])
        )

        # 2) 返回入口插到第一个 <h1> 之前
        m_h1 = re.search(r'<h1[^>]*>', html)
        if not m_h1:
            print(f'  ✗ 未找到 <h1>：{name}')
            failed += 1
            continue
        html = html[:m_h1.start()] + build_backnav() + html[m_h1.start():]

        # 3) 本文目录插到第一个 <h2> 之前
        first_h2 = re.search(r'<h2[^>]*>', html)
        if not first_h2:
            print(f'  ✗ 未找到 <h2>：{name}')
            failed += 1
            continue
        html = html[:first_h2.start()] + build_toc(sections) + html[first_h2.start():]

        # 4) 悬浮侧栏插到 <body> 之后
        m_body = re.search(r'<body>\s*\n', html)
        if not m_body:
            print(f'  ✗ 未找到 <body>：{name}')
            failed += 1
            continue
        html = html[:m_body.end()] + build_sidenav(sections) + html[m_body.end():]

        # 5) CSS 注入到最后一个 </style> 之前，保留原有缩进
        idx = html.rfind('</style>')
        if idx == -1:
            print(f'  ✗ 未找到 </style>：{name}')
            failed += 1
            continue
        line_start = html.rfind('\n', 0, idx) + 1
        indent = html[line_start:idx]
        html = html[:line_start] + indent + NAV_CSS + html[line_start:]

        # 6) JS 放在 </body> 之前
        idx = html.rfind('</body>')
        script = '<script>\n' + NAV_JS + '</script>\n'
        if idx == -1:
            html = html.rstrip() + '\n\n' + script + '</body>\n</html>\n'
        else:
            html = html[:idx] + script + html[idx:]

        # 7) 内容完整性断言：注入只应「新增」，绝不能吞掉原有行。
        #    唯一允许的改写是 <h2> 增加 id 属性（正文文字必须逐字不变）。
        #    这道断言是为了防住 finditer 位置漂移那类静默破坏 —— 校验不报错、
        #    页面也能打开，只有逐行比对才发现正文被切碎了。
        original = [l.rstrip() for l in original_html.splitlines() if l.strip()]
        now = set(l.rstrip() for l in html.splitlines() if l.strip())
        lost = []
        for line in original:
            if line in now:
                continue
            m = re.match(r'^<h2([^>]*)>(.*)</h2>$', line)
            # 纯 h2 行：只要文字还在、且现在带上了 id，就算正常改写
            if m and any(
                l.startswith('<h2 id="') and m.group(2) in l for l in now
            ):
                continue
            lost.append(line)
        if lost:
            print(f'  ✗ 内容完整性校验失败：{name}')
            for line in lost[:5]:
                print(f'      丢失：{line[:100]}')
            failed += 1
            continue

        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(html)
        changed += 1
        print(f'  ✓ {name}（{len(sections)} 个章节）')

    print(f'\n完成：注入 {changed} 篇，跳过（已存在）{skipped} 篇，失败 {failed} 篇')
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
