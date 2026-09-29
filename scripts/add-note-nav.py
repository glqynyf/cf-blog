#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给 public/notes/ 下 115 篇独立 HTML 笔记批量注入「返回」入口。

背景：笔记是脱离 Astro 的独立 HTML（自带深色主题），没有站点 Header，
点进去之后没有任何回到目录的入口。

做法：
1. 把返回链接直接追加到已有的 <div class="stage-bar"> 内（同一行右侧），
   不新增独立行 —— 避免与上方 STAGE 标签栏重复显示章节信息、版面冗余。
2. 链接带上所属章节：/notes/?stage=S00（与站点单章筛选一致）。
3. 每个 <style> 末尾注入配套 CSS（复用笔记自身的深色变量）。

幂等：已存在 note-nav__back 的文件会跳过。
"""
import os
import re
import sys

NOTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public', 'notes')

# 注入到最后一个 </style> 之前的 CSS。
# 不以换行开头：调用方已把 </style> 所在行的原始缩进放在最前面，
# 若这里再带一个前导 \n 就会多插一个空行。
# margin-left:auto 把按钮推到 stage-bar 行末右侧；
# stage-bar 本身已是 flex + flex-wrap，窄屏时按钮会自然换行到下一行。
NAV_CSS = """  /* 返回入口（由 add-note-nav.py 注入） */
  .note-nav__back {
    display: inline-flex; align-items: center; gap: 6px;
    margin-left: auto; padding: 5px 12px; border-radius: 6px;
    background: var(--surface-2); border: 1px solid var(--border);
    color: var(--text-dim); text-decoration: none;
    font-size: 13px; font-weight: 600; line-height: 1.4;
    transition: all 0.2s;
  }
  .note-nav__back:hover {
    background: var(--accent-soft); border-color: var(--accent);
    color: var(--accent); text-decoration: none;
  }
  /* 窄屏：按钮不再右推，改为独占一行左侧 */
  @media (max-width: 640px) {
    .note-nav__back { margin-left: 0; }
  }
"""


def build_back(stage: str) -> str:
    # 前置换行让缩进自然；闭合 </div> 由调用方在自己的行首补回
    return f'\n  <a class="note-nav__back" href="/notes/?stage={stage}">← 返回笔记</a>\n'


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

        if 'note-nav__back' in html:
            skipped += 1
            continue

        # 1) 在 stage-bar 的 </div> 之前插入返回链接（保持同一行）
        pattern = re.compile(r'(<div class="stage-bar">.*?)(</div>)', re.S)
        new_html, n = pattern.subn(
            lambda m: m.group(1) + build_back(stage) + m.group(2), html, count=1
        )
        if n == 0:
            print(f"  ✗ 未找到 stage-bar：{name}")
            failed += 1
            continue

        # 2) 在最后一个 </style> 前注入 CSS（保留该 </style> 原有缩进前缀）
        idx = new_html.rfind('</style>')
        if idx == -1:
            print(f"  ✗ 未找到 </style>：{name}")
            failed += 1
            continue
        line_start = new_html.rfind('\n', 0, idx) + 1
        indent = new_html[line_start:idx]  # 保留原缩进（部分文件是 "  "）
        new_html = new_html[:line_start] + indent + NAV_CSS + new_html[line_start:]

        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(new_html)
        changed += 1

    print(f"\n完成：注入 {changed} 篇，跳过（已存在）{skipped} 篇，失败 {failed} 篇")
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
