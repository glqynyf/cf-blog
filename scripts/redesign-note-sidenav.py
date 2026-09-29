#!/usr/bin/env python3
"""
重做 115 篇笔记的「左侧悬浮目录」(.note-sidenav)。

背景：正文里的 <nav class="toc"> 已在 redesign-note-toc.py 中重做，
但左侧悬浮目录的标题同样叫「本文目录」，且在 >=1440px 宽屏上常驻显示，
样式仍是旧的（内联 "01 " 纯文本数字、左侧 2px 指示条），与正文目录割裂。

本脚本只替换 .note-sidenav 的后代选择器规则与 __* 组件类，
严格保留：
  - .note-sidenav { display: none; }        （默认隐藏）
  - @media (min-width: 1440px) 里的 display: block  （宽屏显示）
以及导航容器上的内联定位 style（position/left/top/width 等）。

严格幂等：检测到标记注释即跳过。
"""
import io
import os
import re
import sys

NOTES_DIR = 'public/notes'
MARKER = '/* 左侧悬浮目录：编号徽章 + 时间轴引导线 */'

NEW_CSS = MARKER + """
  .note-sidenav::before {
    content: '';
    position: absolute;
    left: 0; right: 0; top: 0; height: 2px;
    border-radius: 8px 8px 0 0;
    background: linear-gradient(90deg, var(--accent), transparent 78%);
  }
  .note-sidenav__title {
    display: flex;
    align-items: center;
    gap: 6px;
    margin: 0 0 10px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
    font-size: 11px;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 1.5px;
    text-transform: uppercase;
  }
  .note-sidenav__title::before {
    content: '';
    width: 3px; height: 11px;
    flex-shrink: 0;
    border-radius: 2px;
    background: var(--accent);
  }
  .note-sidenav__count {
    margin-left: auto;
    padding: 1px 7px;
    border-radius: 999px;
    background: var(--accent-soft);
    border: 1px solid rgba(240, 136, 62, 0.3);
    color: var(--accent);
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: none;
  }
  .note-sidenav ol {
    position: relative;
    list-style: none;
    margin: 0;
    padding: 0;
    counter-reset: snav;
  }
  .note-sidenav ol::before {
    content: '';
    position: absolute;
    left: 9px; top: 12px; bottom: 12px;
    width: 1px;
    background: linear-gradient(180deg, var(--border) 0%, var(--border) 70%, transparent 100%);
  }
  .note-sidenav li {
    margin: 0;
  }
  .note-sidenav ol a {
    position: relative;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 5px 6px;
    border-radius: 6px;
    border-left: 2px solid transparent;
    color: var(--text-dim);
    font-size: 12.5px;
    line-height: 1.5;
    text-decoration: none;
    transition: background 0.18s, color 0.18s, border-color 0.18s;
  }
  .note-sidenav ol a::before {
    counter-increment: snav;
    content: counter(snav, decimal-leading-zero);
    position: relative;
    z-index: 1;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    width: 18px; height: 18px;
    border-radius: 5px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    color: var(--text-mute);
    font-size: 9.5px;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    transition: background 0.18s, color 0.18s, border-color 0.18s;
  }
  .note-sidenav ol a:hover {
    background: var(--surface-2);
    color: var(--text);
    text-decoration: none;
  }
  .note-sidenav ol a:hover::before {
    border-color: var(--accent);
    color: var(--accent);
  }
  .note-sidenav ol a.is-active {
    background: var(--accent-soft);
    color: var(--accent);
    border-left-color: var(--accent);
    font-weight: 600;
  }
  .note-sidenav ol a.is-active::before {
    background: var(--accent);
    border-color: var(--accent);
    color: #0f1419;
  }
  .note-sidenav__foot {
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid var(--border);
  }
  .note-sidenav__top {
    display: block;
    text-align: center;
    padding: 5px 0;
    border-radius: 5px;
    color: var(--text-mute);
    text-decoration: none;
    font-size: 11.5px;
  }
  .note-sidenav__top:hover {
    background: var(--surface-2);
    color: var(--accent);
    text-decoration: none;
  }"""


def top_level_spans(css):
    """返回 [(去注释后的选择器, start, end)]，end 为规则结束右花括号后一位。"""
    spans, depth, start, buf = [], 0, None, []
    for i, ch in enumerate(css):
        if ch == '{':
            if depth == 0:
                start = i
                sel = re.sub(r'/\*.*?\*/', '', ''.join(buf), flags=re.S).strip()
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


def rewrite_style_block(css):
    """替换 .note-sidenav 的后代/组件类规则，保留裸 .note-sidenav 与 @media。"""
    spans = top_level_spans(css)
    hits = []
    for sel, a, b in spans:
        if '@media' in sel or not sel.startswith('.note-sidenav'):
            continue
        # 裸 .note-sidenav（display:none / display:block）必须保留
        if sel == '.note-sidenav' or sel.startswith('.note-sidenav a'):
            continue
        hits.append((a, b))
    if not hits:
        return css, 0
    start, end = hits[0][0], hits[-1][1]
    return css[:start] + NEW_CSS + '\n' + css[end:], len(hits)


def process(path):
    html = io.open(path, encoding='utf-8').read()
    if MARKER in html:
        return 'skip'

    total = 0

    # 1) 所有 style 块都过一遍（少数笔记的侧栏样式在第二个块里）
    def sub_style(m):
        nonlocal total
        new, n = rewrite_style_block(m.group(2))
        total += n
        return m.group(1) + new + m.group(3)

    html = re.sub(r'(<style[^>]*>)(.*?)(</style>)', sub_style, html, flags=re.S)
    if total == 0:
        return 'no-sidenav-rule'

    # 2) 标题行加章节数徽章
    tm = re.search(r'<h4 class="note-sidenav__title">本文目录</h4>', html)
    if tm:
        nav = re.search(r'<nav class="note-sidenav".*?<ol>(.*?)</ol>', html, re.S)
        cnt = len(re.findall(r'<li><a href="#', nav.group(1))) if nav else 0
        html = html.replace(
            '<h4 class="note-sidenav__title">本文目录</h4>',
            '<h4 class="note-sidenav__title">本文目录'
            '<span class="note-sidenav__count">%d</span></h4>' % cnt, 1)

    # 3) 容器内联样式换成渐变底，与正文目录一致
    html = html.replace(
        'background:var(--surface);border:1px solid var(--border);border-radius:8px;',
        'background:radial-gradient(130% 120% at 0% 0%, var(--accent-soft), transparent 60%), var(--surface);'
        'border:1px solid var(--border);border-radius:10px;')

    io.open(path, 'w', encoding='utf-8').write(html)
    return 'ok:%d' % total


def main():
    files = sorted(f for f in os.listdir(NOTES_DIR) if f.endswith('.html'))
    tally, failures = {}, []
    for name in files:
        r = process(os.path.join(NOTES_DIR, name))
        k = r.split(':')[0]
        tally[k] = tally.get(k, 0) + 1
        if k not in ('ok', 'skip'):
            failures.append((name, r))
    print('总数 %d' % len(files))
    for k, v in sorted(tally.items()):
        print('  %-18s %d' % (k, v))
    if failures:
        print('\n失败:')
        for n, r in failures[:10]:
            print('  %s -> %s' % (n, r))
        sys.exit(1)


if __name__ == '__main__':
    main()
