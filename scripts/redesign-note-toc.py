#!/usr/bin/env python3
"""
重做 115 篇笔记正文里的「本文目录」区块（<nav class="toc">）。

设计目标：层级更分明 + 更有设计感
  1. 卡片化：渐变底 + 顶部强调线 + 阴影
  2. 标题行：左侧强调竖条 + 右上角章节数徽章
  3. 编号徽章：26px 圆角方块，取代原来裸奔的 "01" 数字
  4. 时间轴引导线：一条贯穿列表的竖线，连接所有编号
  5. 滚动高亮：把原本只作用于左侧悬浮目录的 scroll-spy 扩展到本文目录

实现要点：
  - 各笔记的 .toc 样式块有 5 种细微变体，不能按字面量替换，
    改用花括号深度扫描找出所有以 .toc 开头的顶层规则并整体重建。
  - 严格幂等：检测到 toc__count 即跳过。
"""
import io
import os
import re
import sys

NOTES_DIR = 'public/notes'

NEW_CSS = """
  /* 本文目录：卡片 + 编号徽章 + 时间轴引导线 */
  .toc {
    position: relative;
    margin-bottom: 48px;
    padding: 20px 24px 18px;
    background:
      radial-gradient(120% 130% at 0% 0%, var(--accent-soft), transparent 55%),
      var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    box-shadow: var(--shadow);
    overflow: hidden;
  }
  .toc::before {
    content: '';
    position: absolute;
    left: 0; right: 0; top: 0; height: 2px;
    background: linear-gradient(90deg, var(--accent), transparent 72%);
  }
  .toc h4 {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent);
  }
  .toc h4::before {
    content: '';
    width: 4px; height: 14px;
    flex-shrink: 0;
    border-radius: 2px;
    background: var(--accent);
  }
  .toc__count {
    margin-left: auto;
    padding: 2px 9px;
    border-radius: 999px;
    background: var(--accent-soft);
    border: 1px solid rgba(240, 136, 62, 0.3);
    color: var(--accent);
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: none;
  }
  .toc ol {
    position: relative;
    list-style: none;
    counter-reset: toc-counter;
    margin: 0;
    padding: 0;
  }
  .toc ol::before {
    content: '';
    position: absolute;
    left: 25px; top: 20px; bottom: 20px;
    width: 1px;
    background: linear-gradient(180deg, var(--border) 0%, var(--border) 72%, transparent 100%);
  }
  .toc li {
    counter-increment: toc-counter;
    position: relative;
    margin: 0;
    padding: 0;
    border-bottom: none;
  }
  .toc a {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 7px 12px;
    border-radius: 8px;
    color: var(--text-dim);
    font-size: 14.5px;
    line-height: 1.5;
    text-decoration: none;
    transition: background 0.18s, color 0.18s;
  }
  .toc a::before {
    content: counter(toc-counter, decimal-leading-zero);
    position: relative;
    z-index: 1;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    width: 26px; height: 26px;
    border-radius: 7px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    color: var(--text-mute);
    font-size: 11.5px;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    transition: background 0.18s, color 0.18s, border-color 0.18s;
  }
  .toc a:hover {
    background: var(--surface-2);
    color: var(--text);
    text-decoration: none;
  }
  .toc a:hover::before {
    border-color: var(--accent);
    color: var(--accent);
  }
  .toc a.is-active {
    background: var(--accent-soft);
    box-shadow: inset 3px 0 0 var(--accent);
    color: var(--text);
  }
  .toc a.is-active::before {
    background: var(--accent);
    border-color: var(--accent);
    color: #0f1419;
  }
"""

NEW_SCRIPT = """<script>

/* 目录滚动高亮：同时驱动左侧悬浮目录与正文「本文目录」 */
(function () {
  var groups = [document.querySelector('.note-sidenav'), document.querySelector('.toc')];
  var targets = [];
  var seen = {};
  var valid = false;

  groups.forEach(function (nav) {
    if (!nav) return;
    var links = nav.querySelectorAll('a[href^="#"]');
    valid = valid || links.length > 0;
    Array.prototype.forEach.call(links, function (a) {
      var id = a.getAttribute('href').slice(1);
      var el = document.getElementById(id);
      if (el && !seen[id]) { seen[id] = true; targets.push(el); }
    });
  });

  if (!valid || !targets.length) return;

  function onScroll() {
    var best = null;
    var bestTop = -Infinity;
    for (var i = 0; i < targets.length; i++) {
      var top = targets[i].getBoundingClientRect().top;
      if (top <= 120 && top > bestTop) { bestTop = top; best = targets[i]; }
    }
    if (!best) best = targets[0];
    var id = best.id;

    groups.forEach(function (nav) {
      if (!nav) return;
      Array.prototype.forEach.call(nav.querySelectorAll('a[href^="#"]'), function (a) {
        if (a.getAttribute('href').slice(1) === id) a.classList.add('is-active');
        else a.classList.remove('is-active');
      });
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
</script>"""


def top_level_spans(css):
    """返回 [(selector, start, end)]，end 为规则结束右花括号后一位。"""
    spans, depth, start, buf = [], 0, None, []
    for i, ch in enumerate(css):
        if ch == '{':
            if depth == 0:
                start = i
                sel = ''.join(buf).strip()
            depth += 1
            buf = []
        elif ch == '}':
            depth -= 1
            if depth == 0 and start is not None:
                spans.append((sel, start, i + 1))
            buf = []
        elif depth == 0:
            buf.append(ch)
    return spans


def rewrite_css(css):
    """删除所有 .toc* 顶层规则，原位插入新版样式。"""
    spans = top_level_spans(css)
    hits = [s for s in spans if re.match(r'\.toc\b', s[0].strip()) and 'sidenav' not in s[0]]
    if not hits:
        return None, 0
    start = hits[0][1]
    end = hits[-1][2]
    return css[:start] + NEW_CSS.strip('\n') + '\n' + css[end:], len(hits)


def process(path):
    html = io.open(path, encoding='utf-8').read()
    if 'toc__count' in html:
        return 'skip'

    n_rules = 0

    # 1) 样式块
    m = re.search(r'(<style[^>]*>)(.*?)(</style>)', html, re.S)
    if not m:
        return 'no-style'
    new_css, n_rules = rewrite_css(m.group(2))
    if new_css is None:
        return 'no-toc-rule'
    html = html[:m.start(2)] + new_css + html[m.end(2):]

    # 2) 标题行加章节数徽章
    toc_m = re.search(r'(<nav class="toc">\s*<h4>本文目录)(</h4>)', html)
    if not toc_m:
        return 'no-toc-nav'
    ol_m = re.search(r'<nav class="toc">.*?<ol>(.*?)</ol>', html, re.S)
    count = len(re.findall(r'<li><a href="#', ol_m.group(1))) if ol_m else 0
    html = (html[:toc_m.end(1)]
            + '<span class="toc__count">%d</span>' % count
            + html[toc_m.end(1):])

    # 3) 滚动高亮脚本扩展到本文目录
    sc = re.search(r'<script>(?:(?!</script>).)*?note-sidenav(?:(?!</script>).)*?</script>',
                   html, re.S)
    if not sc:
        return 'no-sidenav-script'
    html = html[:sc.start()] + NEW_SCRIPT + html[sc.end():]

    io.open(path, 'w', encoding='utf-8').write(html)
    return 'ok:%d' % n_rules


def main():
    files = sorted(f for f in os.listdir(NOTES_DIR) if f.endswith('.html'))
    tally = {}
    failures = []
    for name in files:
        r = process(os.path.join(NOTES_DIR, name))
        tally[r.split(':')[0]] = tally.get(r.split(':')[0], 0) + 1
        if not (r.startswith('ok') or r == 'skip'):
            failures.append((name, r))
    print('总数 %d' % len(files))
    for k, v in sorted(tally.items()):
        print('  %-14s %d' % (k, v))
    if failures:
        print('\n失败明细:')
        for n, r in failures:
            print('  %s -> %s' % (n, r))
        sys.exit(1)


if __name__ == '__main__':
    main()
