#!/usr/bin/env python3
'''检查 115 篇笔记的内联 CSS 是否存在「静默失效」。

肉眼和 `count('{') == count('}')` 都测不出来——本项目已经被同一类问题咬过两次：

  1) `content: """` 未闭合字符串把行尾的 `}` 一起吞掉，解析器从此卡在前一个
     `{` 里，后续规则全部嵌套失效（曾导致 78 篇的宽屏侧栏整体变回浏览器默认样式）。
     整体花括号仍是配平的，只是**深度错位**。
  2) 注释被插在选择器与左花括号之间：
         .toc   /* 注释 */
         .toc {
     浏览器拼成后代选择器 `.toc .toc`，永不匹配，独立的 `.toc { }` 规则
     根本不存在。语法合法，所以词法校验查不出来。

用法：
    python3 scripts/check-note-css.py                        # 检查全部笔记（默认）
    python3 scripts/check-note-css.py public/planning        # 检查规划文档
    python3 scripts/check-note-css.py public/notes --verbose # 列出每个问题文件
退出码 0 = 全部通过，1 = 有问题。
注意：关键规则那组（.toc / .note-sidenav*）是**笔记专用**，只对 public/notes/ 生效；
规划文档是另一种自包含页面，不含目录构件，不套用。
'''

import re
import sys
from pathlib import Path

NOTES = Path(__file__).resolve().parent.parent / "public" / "notes"

STYLE = re.compile(r"<style[^>]*>(.*?)</style>", re.S)

# 选择器 + 注释，且本行没有 `{` —— 拼接错误的现场
DANGLING = re.compile(
    r"^[ \t]*\.[A-Za-z0-9_:-]+[ \t]+(?:/\*(?:[^*]|\*(?!/))*\*/[ \t]*)+\n"
    r"[ \t]*\.[A-Za-z0-9_:.-]+[^{}\n]*\{",
    re.M,
)

BAD_STRING = re.compile(r'content:\s*"""')

# 每篇**笔记**必须存在的关键规则（缺失说明样式被整段吞掉）
NOTE_REQUIRED = (
    ".toc {",
    ".note-sidenav__title {",
    ".note-sidenav__count {",
    ".note-sidenav ol a {",
    ".note-sidenav ol a::before {",
)


def scan(css):
    """按 CSS Syntax L3 词法规范扫描单个 style 块。

    返回 (致命错误, 末花括号深度, 坏字符串行数)。字符串内遇换行 → bad-string，
    解析器在换行处恢复，这一点很关键：它决定了「整条规则压在一行」是否会
    连带吞掉闭合括号。
    """
    depth = 0
    bad_lines = 0
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
                return "注释未闭合", depth, bad_lines
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
                bad_lines += 1
            i = j + 1
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth < 0:
                return "出现孤立的右花括号", 0, bad_lines
        i += 1
    return None, depth, bad_lines


def main():
    # 用法：check-note-css.py [目录] [--verbose]
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    verbose = "--verbose" in sys.argv
    target = Path(args[0]) if args else NOTES
    is_notes = target.resolve() == NOTES.resolve()
    required = NOTE_REQUIRED if is_notes else ()

    files = sorted(target.glob("*.html"))
    if not files:
        print("找不到 HTML 目录:", target)
        return 1

    problems = []
    multi_style = 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        blocks = STYLE.findall(text)
        if not blocks:
            problems.append((path.name, "文件里没有 <style> 块"))
            continue
        if len(blocks) > 1:
            multi_style += 1

        for idx, css in enumerate(blocks):
            fatal, depth, bad = scan(css)
            if fatal:
                problems.append((path.name, "style 块 #%d %s" % (idx, fatal)))
            if depth != 0:
                problems.append(
                    (path.name, "style 块 #%d 括号未配平（末深度=%d，CSS 被未闭合字符串吞掉）" % (idx, depth))
                )
            m = DANGLING.search(css)
            if m:
                problems.append(
                    (path.name, "style 块 #%d 第 %d 行选择器被注释截断：%s"
                     % (idx, css[: m.start()].count("\n") + 1, m.group(0).split("\n")[0].strip()))
                )

        joined = "\n".join(blocks)
        if BAD_STRING.search(joined):
            problems.append((path.name, "残留 content:\"\"\" 未闭合字符串"))
        missing = [r for r in required if r not in joined]
        if missing:
            problems.append((path.name, "缺关键规则：" + "、".join(missing)))

    total_blocks = sum(len(STYLE.findall(p.read_text(encoding="utf-8"))) for p in files)
    print("检查 %s：%d 个 HTML / %d 个 <style> 块（%d 个含多块）"
          % (target, len(files), total_blocks, multi_style))

    if not problems:
        print("✅ 全部通过：无括号失衡、无选择器截断、无未闭合字符串、关键规则齐全")
        return 0

    print("❌ 发现 %d 个问题：" % len(problems))
    for name, why in problems[: (len(problems) if verbose else 20)]:
        print("   %-46s %s" % (name[:46], why))
    if len(problems) > 20 and not verbose:
        print("   …… 还有 %d 个，加 --verbose 查看全部" % (len(problems) - 20))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
