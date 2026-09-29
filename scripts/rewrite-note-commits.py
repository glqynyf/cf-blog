#!/usr/bin/env python3
"""把「批量改全部 115 篇笔记」的 commit 拆成「每篇笔记一个 commit」。

## 为什么要拆
GitHub 仓库目录页在每个文件下方显示 **Last commit message**，取自
git 记录里「该文件最后一次被改动的那个 commit 的 message 首行」。
本项目 115 篇笔记此前全部被 8 个批量 commit 覆盖，导致目录页每一行
下面都是同一句「feat(notes): 左侧悬浮目录同步重做…」，与该篇内容无关。
拆分后每篇笔记的 Last commit message 变成它自己的概括。

## 拆分原则（保证「历史保留」）
- **不删除任何 commit**，只把一个批量 commit 展开成多个语义更细的 commit。
- 展开后的最后一个 commit，其 tree 与原 commit **完全相同**（用 SHA 校验）。
- 后续 commit 沿用新链继续重建，因此提交顺序与相对时间线不变。

## 拆分粒度
对每个触碰多篇笔记的 commit C：
  - 按 `public/notes/*.html` 分组，每篇笔记一个 commit，
    message = 该篇概括（形如 `S05-03 · 用 MACD 定方向、KDJ 找精确买点`）
  - C 里的非笔记文件归入一个 commit，message 沿用 C 的原 message
  - 若 C 只改一篇笔记，则不拆

## 用法
    python3 scripts/rewrite-note-commits.py --dry-run     # 只演练，不写
    python3 scripts/rewrite-note-commits.py --branch rewritten
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

NOTES_RE = re.compile(r"^public/notes/.*\.html$")
# 笔记标识，如 S05-03。目录移动（notes/ → public/notes/）时，
# 同一篇笔记会同时出现「旧路径删除」和「新路径新增」两条记录，
# 两者都必须落进同一个 commit，否则中间状态会缺文件或多文件。
NOTE_KEY_RE = re.compile(r"S\d{2}-\d{2}-")


def git(*a, check=True, env=None):
    p = subprocess.run(["git", *a], capture_output=True, text=True, env=env)
    if check and p.returncode != 0:
        sys.exit(f"git {' '.join(a)} 失败:\n{p.stderr}")
    return p.stdout


def note_key(path):
    """从任意路径里取出笔记标识 SXX-NN；不是笔记返回 None。"""
    m = NOTE_KEY_RE.search(path)
    return m.group(0)[:-1] if m else None


def load_summaries(path):
    """{ 'S05-03': 'S05-03 · 用 MACD 定方向…' }"""
    data = json.load(open(path, encoding="utf-8"))
    out = {}
    for item in data:
        key = note_key(item["file"])
        if not key:
            sys.exit(f"无法从文件名解析笔记标识: {item['file']}")
        out[key] = item["summary"]
    return out


class TreeBuilder:
    """用临时索引把若干文件改动叠加到一个基线 tree 上，逐组产出中间 tree。"""

    def __init__(self, base_tree):
        self.base_tree = base_tree
        self.idx = tempfile.mktemp(prefix="rewrite-idx-")
        env = dict(os.environ, GIT_INDEX_FILE=self.idx)
        subprocess.run(["git", "read-tree", base_tree], check=True, env=env)
        self.env = env

    def apply(self, changes):
        """changes: [(mode, sha, path), ...]

        `--index-info` 必须从 stdin 读，不能把内容作为命令行参数跟在后面。
        """
        if changes:
            payload = "".join(
                f"{mode} {sha}\t{path}\n" for mode, sha, path in changes)
            subprocess.run(["git", "update-index", "--add", "--index-info"],
                           input=payload, text=True, check=True, env=self.env)
        return git("write-tree", env=self.env).strip()

    def cleanup(self):
        try:
            os.unlink(self.idx)
        except OSError:
            pass


def build_commit(parent_commit, tree_sha, message, author, committer):
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": author["name"], "GIT_AUTHOR_EMAIL": author["email"],
        "GIT_AUTHOR_DATE": author["date"],
        "GIT_COMMITTER_NAME": committer["name"],
        "GIT_COMMITTER_EMAIL": committer["email"],
        "GIT_COMMITTER_DATE": committer["date"],
    })
    args = ["git", "commit-tree", tree_sha]
    if parent_commit:
        args += ["-p", parent_commit]
    p = subprocess.run(args, input=message + "\n", capture_output=True,
                       text=True, env=env)
    if p.returncode != 0:
        sys.exit(f"commit-tree 失败: {p.stderr}")
    return p.stdout.strip()


def parse_ident(raw):
    """'Name <email> 1234567890 +0800' -> {name,email,date}"""
    name, rest = raw.split(" <", 1)
    email, rest = rest.split("> ", 1)
    ts, tz = rest.split()
    sign = "-" if tz[0] == "-" else "+"
    stamp = f"{ts} {sign}{tz[1:3]}{tz[3:5]}"
    return {"name": name, "email": email, "date": stamp}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--branch", default="rewritten")
    ap.add_argument("--summaries", default="/tmp/summary-work/summaries.json")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    summaries = load_summaries(args.summaries)
    print(f"已载入概括 {len(summaries)} 条")

    commits = git("rev-list", "--reverse", "--topo-order", "main").split()
    print(f"待处理 commit {len(commits)} 个")

    new_parent = None
    created = 0
    plan = []

    for i, c in enumerate(commits, 1):
        parents = git("rev-list", "--parents", "-n", "1", c).split()[1:]
        # 只处理单 parent 的线性历史
        orig_parent = parents[0] if parents else None
        raw = git("cat-file", "-p", c)
        tree = raw.split("\n")[0].split()[1]
        message = raw.split("\n\n", 1)[1].rstrip("\n")
        author = parse_ident(
            [l for l in raw.splitlines() if l.startswith("author ")][0][7:])
        committer = parse_ident(
            [l for l in raw.splitlines() if l.startswith("committer ")][0][10:])

        # 相对第一个 parent 的文件改动
        if orig_parent:
            files = [f for f in git(
                "-c", "core.quotePath=false", "diff-tree", "-r", "--name-only",
                "--no-commit-id", orig_parent, c).splitlines() if f]
        else:
            files = [f for f in git(
                "-c", "core.quotePath=false", "ls-tree", "-r", "--name-only",
                tree).splitlines() if f]

        # 按笔记标识分组：一篇笔记的「删除旧路径 + 新增新路径」必须同 commit
        groups, others = {}, []
        for f in files:
            key = note_key(f)
            if key:
                groups.setdefault(key, []).append(f)
            else:
                others.append(f)

        if len(groups) < 2:
            # 不用拆，原样重建（只是 parent 变了）
            if args.dry_run:
                plan.append((c, "原样", 1))
            new_parent = c if new_parent is None else build_commit(
                new_parent, tree, message, author, committer)
            continue

        plan.append((c, "拆分", len(groups) + (1 if others else 0)))

        base_tree = (git("rev-parse", f"{orig_parent}^{{tree}}").strip()
                     if orig_parent else None)
        if base_tree is None:
            sys.exit("❌ 根 commit 改到了笔记，本脚本未覆盖该情形")
        if not args.dry_run:
            builder = TreeBuilder(base_tree)

        for key, paths in groups.items():
            changes = [_entry(c, orig_parent, p) for p in paths]
            summary = summaries.get(key)
            if not summary:
                sys.exit(f"缺少概括: {key}")
            if not summary.startswith(key + " · "):
                sys.exit(f"概括前缀与文件不符: {key} vs {summary[:20]}")
            # 该 commit 若还含非笔记文件，其原 message 会由末尾那个 commit 承载；
            # 若全是笔记文件（无处安放），就把原 message 降为正文保留操作语义。
            msg = summary if others else f"{summary}\n\n{message}"
            if not args.dry_run:
                t = builder.apply(changes)
                new_parent = build_commit(new_parent, t, msg, author, committer)
                created += 1

        if others:
            changes = [_entry(c, orig_parent, p) for p in others]
            if not args.dry_run:
                t = builder.apply(changes)
                new_parent = build_commit(new_parent, t, message, author, committer)
                created += 1

        if not args.dry_run:
            builder.cleanup()
            final = git("rev-parse", f"{new_parent}^{{tree}}").strip()
            if final != tree:
                sys.exit(f"❌ tree 不一致 @{c}: {final} != {tree}")

    if args.dry_run:
        print("\n拆分计划：")
        for c, kind, n in plan:
            if kind == "拆分":
                print(f"  {c[:7]} → {n} 个 commit")
        return

    git("update-ref", f"refs/heads/{args.branch}", new_parent)
    print(f"\n✅ 新分支 {args.branch} = {new_parent[:7]}，新增 {created} 个 commit")
    print(f"   总 commit: {len(commits)} → {git('rev-list', '--count', args.branch).strip()}")


def _entry(commit, parent, path):
    """返回 --index-info 需要的一行要素 (mode, sha, path)。

    文件在 commit 的 tree 中存在 → 取其 (mode, sha)；
    不存在说明这个 commit 删除了它 → mode 给 0、sha 给全 0，
    `--index-info` 即按「删除」处理（真实 sha 从 parent 取，仅作校验）。
    """
    out = git("-c", "core.quotePath=false", "ls-tree", commit, "--", path)
    if out.strip():
        mode, _t, sha = out.split("\t", 1)[0].split()
        return mode, sha, path
    if not parent:
        sys.exit(f"❌ 无法判定 {path} 的新增/删除状态")
    old = git("-c", "core.quotePath=false", "ls-tree", parent, "--", path)
    if not old.strip():
        sys.exit(f"❌ {path} 在父提交中也不存在，diff-tree 结果异常")
    return "0", "0" * 40, path


if __name__ == "__main__":
    main()
