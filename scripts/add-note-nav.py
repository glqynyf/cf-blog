#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给 public/notes/ 下 115 篇独立 HTML 笔记批量注入「返回」导航条。

背景：笔记是脱离 Astro 的独立 HTML（自带深色主题），没有站点 Header，
点进去之后没有任何回到目录的入口。

做法：
1. 在 <div class="stage-bar">…</div> 之后插入 note-nav 导航条
2. 链接带上所属章节：/notes/?stage=S00（与站点单章筛选一致）
3. 每个 <style> 末尾注入配套 CSS（跟随笔记自身的深色变量）

幂等：已存在 note-nav 的文件会跳过。
"""
import os
import re
import sys

NOTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public', 'notes')

NAV_CSS = """
  /* 返回导航条（由 add-note-nav.py 注入） */
  .note-nav {
    display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
    margin-bottom: 20px; padding: 10px 14px;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; font-size: 13px;
  }
  .note-nav a {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 5px 12px; border-radius: 6px;
    background: var(--surface-2); border: 1px solid var(--border);
    color: var(--text-dim); text-decoration: none;
    font-weight: 600; transition: all 0.2s;
  }
  .note-nav a:hover {
    background: var(--accent-soft); border-color: var(--accent);
    color: var(--accent); text-decoration: none;
  }
  .note-nav__sep { color: var(--text-mute); }
  .note-nav__cur { color: var(--text-mute); font-size: 12px; }
"""


def build_nav(stage: str) -> str:
    return (
        '\n<nav class="note-nav" aria-label="返回导航">\n'
        f'  <a href="/notes/?stage={stage}">← 返回本章目录</a>\n'
        '  <a href="/notes/">全部笔记</a>\n'
        '  <span class="note-nav__sep">·</span>\n'
        '  <a href="/">首页</a>\n'
        f'  <span class="note-nav__cur">{stage}</span>\n'
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
        stage = os.path.splitext(name)[0][:3]  # S00-01-xxx.html -> S00

        with open(path, encoding='utf-8') as fh:
            html = fh.read()

        if 'class="note-nav"' in html:
            skipped += 1
            continue

        # 1) 在 stage-bar 的 </div> 之后插入导航条
        pattern = re.compile(
            r'(<div class="stage-bar">.*?</div>)', re.S
        )
        new_html, n = pattern.subn(lambda m: m.group(1) + build_nav(stage), html, count=1)
        if n == 0:
            print(f"  ✗ 未找到 stage-bar：{name}")
            failed += 1
            continue

        # 2) 在最后一个 </style> 前注入 CSS
        idx = new_html.rfind('</style>')
        if idx == -1:
            print(f"  ✗ 未找到 </style>：{name}")
            failed += 1
            continue
        new_html = new_html[:idx] + NAV_CSS + new_html[idx:]

        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(new_html)
        changed += 1

    print(f"\n完成：注入 {changed} 篇，跳过（已存在）{skipped} 篇，失败 {failed} 篇")
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
