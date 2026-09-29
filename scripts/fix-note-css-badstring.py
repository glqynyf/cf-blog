#!/usr/bin/env python3
'''修复笔记 style 里 `content: """` 造成的未闭合字符串。

`content: """` 会被 CSS 词法分析成「空字符串 + 开启一个新字符串」。
若该规则整条压在一行，未闭合的字符串会把行尾的 `}` 一起吞掉，
解析器从此停留在上一个 `{` 里，后续所有规则全部变成嵌套而失效
（本项目 115 篇里 78 篇的 note-sidenav / toc 样式就是这样整体失效的）。

改成合法的 `content: "\\201C"`（U+201C 开引号，即这条规则本来想要的
48px 橙色装饰大字）。不能简单改成 `content: ""`：那样 display:block
配 48px 行高会在每条引用横幅上方留下约 36px 空白。
'''

import re
import sys
from pathlib import Path
from typing import Optional, List, Tuple

NOTES = Path(__file__).resolve().parent.parent / "public" / "notes"

BAD = re.compile(r'content:\s*"""')


def css_span(text: str):
    s = text.index("<style>") + len("<style>")
    e = text.index("</style>")
    return s, e


def scan(css: str) -> Tuple[int, int, List[int], Optional[str]]:
    """按 CSS 词法规范扫描：返回 (末深度, 负深度次数, 坏字符串行号, 致命错误)。"""
    bad_lines = []  # type: List[int]
    depth = 0
    negative = 0
    line = 1
    i, n = 0, len(css)
    while i < n:
        c = css[i]
        if c == "\n":
            line += 1
            i += 1
            continue
        if c == "/" and i + 1 < n and css[i + 1] == "*":
            j = css.find("*/", i + 2)
            if j == -1:
                return depth, negative, bad_lines, "注释未闭合"
            line += css.count("\n", i, j)
            i = j + 2
            continue
        if c in "\"'":
            q = c
            j = i + 1
            while j < n and css[j] != q and css[j] != "\n":
                if css[j] == "\\":
                    j += 1
                j += 1
            if j < n and css[j] == "\n":
                bad_lines.append(line)
            i = j + 1
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth < 0:
                negative += 1
                depth = 0
        i += 1
    return depth, negative, bad_lines, None


def main() -> int:
    dry = "--dry-run" in sys.argv
    files = sorted(NOTES.glob("*.html"))
    if not files:
        print("找不到笔记目录:", NOTES)
        return 1

    changed = untouched = 0
    repaired = 0
    for path in files:
        original = path.read_text(encoding="utf-8")
        fixed = BAD.sub(r'content: "\\201C";', original)
        if fixed == original:
            untouched += 1
            continue
        # 修复前是否括号失衡（用于统计「真正被吞掉 CSS」的篇数）
        so, eo = css_span(original)
        was_broken = scan(original[so:eo])[0] != 0

        # 校验：修复后 style 块必须括号配平、无致命词法错误
        s, e = css_span(fixed)
        depth, neg, bad, fatal = scan(fixed[s:e])
        if depth != 0 or neg or fatal:
            print(f"[FAIL] {path.name}: 修复后 depth={depth} neg={neg} fatal={fatal}")
            return 1
        if not dry:
            path.write_text(fixed, encoding="utf-8")
        changed += 1
        if was_broken:
            repaired += 1

    verb = "[dry-run] " if dry else ""
    print(
        f"{verb}共 {len(files)} 篇：替换 {changed} 篇"
        f"（其中 CSS 曾被吞掉 {repaired} 篇），未命中 {untouched} 篇"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
