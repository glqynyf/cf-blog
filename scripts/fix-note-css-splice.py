#!/usr/bin/env python3
"""修复笔记 <style> 里被注释截断的选择器拼接错误。

起因：批量美化脚本把注释插在选择器与左花括号之间，产生

    .toc   /* 本文目录：卡片 + 编号徽章 + 时间轴引导线 */
    .toc {

浏览器会把它解析成后代选择器 `.toc .toc`，永不匹配，于是独立的
`.toc { }` 顶层规则根本不存在，卡片的背景 / 边框 / 圆角 / 阴影全丢。
`.note-sidenav__title` 那一处同理，导致悬浮目录顶部渐变线消失。

修复：只删掉多余的那一行选择器，保留 `<indent>.toc {`，
不做任何其他样式改动。脚本幂等，可重复运行。
"""

import re
import sys
from pathlib import Path

NOTES = Path(__file__).resolve().parent.parent / "public" / "notes"

# 悬空行：`选择器 + 注释` 且本行没有 `{` —— 这是拼接错误的现场
DANGLING = re.compile(
    r"^([ \t]*)(\.[A-Za-z0-9_:-]+[ \t]+(?:/\*(?:[^*]|\*(?!/))*\*/[ \t]*)+\n)"
    r"([ \t]*\.[A-Za-z0-9_:.-]+[^{}\n]*\{)",
    re.M,
)
COMMENT = re.compile(r"/\*((?:[^*]|\*(?!/))*)\*/")


def fix_css(text: str) -> tuple[str, int]:
    """把被注释截断的拼接选择器还原为单条规则，返回 (新文本, 修复数)。"""
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        count += 1
        indent, dangling, rule = m.group(1), m.group(2), m.group(3)
        # 注释保留，但挪到规则上方独立成行；抽不出注释就整行丢弃
        note = COMMENT.search(dangling)
        comment = f"{indent}/* {note.group(1).strip()} */\n" if note else ""
        return f"{comment}{rule}"

    return DANGLING.sub(repl, text), count


def main() -> int:
    dry = "--dry-run" in sys.argv
    files = sorted(NOTES.glob("*.html"))
    if not files:
        print("找不到笔记目录:", NOTES)
        return 1

    changed = untouched = 0
    total_fixes = 0
    per_file: list[tuple[str, int]] = []

    for path in files:
        original = path.read_text(encoding="utf-8")
        fixed, n = fix_css(original)
        if n == 0:
            untouched += 1
            continue
        # 幂等：再跑一次不应再产生改动
        again, n2 = fix_css(fixed)
        if n2 != 0 or again != fixed:
            print(f"[FAIL-幂等] {path.name}: 二次修复仍有 {n2} 处")
            return 1
        # 安全：删除的只是注释+重复选择器行，保留的必须还是原选择器 + '{'
        assert fixed.count("{") == original.count("{"), path.name
        per_file.append((path.name, n))
        total_fixes += n
        changed += 1
        if not dry:
            path.write_text(fixed, encoding="utf-8")

    for name, n in per_file:
        print(f"  {n} 处  {name}")

    print(
        f"\n{'[dry-run] ' if dry else ''}共 {len(files)} 篇："
        f"修复 {changed} 篇 / 共 {total_fixes} 处，未命中 {untouched} 篇"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
