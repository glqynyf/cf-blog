#!/usr/bin/env python3
"""当 github.com 主站不可达时，通过 api.github.com 推送。

背景
----
本机 DNS 把 github.com 解析到 20.205.243.166，该 IP 单独不可达；
备用 anycast 入口（140.82.11x.3 / 20.27.177.x）可达性也在分钟级波动，
而 github.com 主站随时可能整体连不上。此时 git push 会报
``Error in the HTTP2 framing layer``，但 api.github.com 始终可达，
且用的是同一份账号凭据（``git credential fill`` → osxkeychain）。

原理
----
复刻一次普通 push：blob → tree → commit → ref，
全部走 GitHub Git Data API。

为什么不用本地 ``origin/main`` 作为 parent
------------------------------------------
API 创建的 commit 与本地 commit 的 SHA 必然不同（author/committer 的
内部字节表示无法通过 API 精确控制），所以本地没有远端那些 object，
``git diff <远端>..HEAD`` 这类命令用不了。本脚本改为：
  1. 用 API 查远端 ref 拿到 parent
  2. 用 API 递归列出远端 tree 已有的全部 blob SHA
  3. 本地 ``git ls-tree -r HEAD`` 拿到完整清单，只上传远端没有的 blob
  4. 以远端 parent 构造 commit 并更新 ref

注意：这会留下**本地与远端 SHA 不一致**（内容一致，SHA 不同）。
网络恢复后执行一次 ``git fetch origin && git reset --hard origin/main``
即可收敛，不会丢内容。

用法
----
    python3 scripts/push-via-api.py              # 推送当前 HEAD
    python3 scripts/push-via-api.py --dry-run    # 只比对，不写入
    python3 scripts/push-via-api.py --force      # 允许非快进更新
"""
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

REPO = os.environ.get("GITHUB_REPO", "glqynyf/cf-blog")
BRANCH = os.environ.get("GITHUB_BRANCH", "main")
API = "https://api.github.com"


def token() -> str:
    out = subprocess.run(
        ["git", "credential", "fill"],
        input="protocol=https\nhost=github.com\n\n",
        capture_output=True, text=True, timeout=30,
    ).stdout
    for line in out.splitlines():
        if line.startswith("password="):
            return line[len("password="):]
    sys.exit("❌ osxkeychain 中取不到 GitHub 凭据（先跑一次 git push 触发认证）")


TOK = token()


def api(path, method="GET", data=None):
    req = urllib.request.Request(f"{API}{path}", method=method)
    req.add_header("Authorization", f"Bearer {TOK}")
    req.add_header("Accept", "application/vnd.github+json")
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, body, timeout=60) as r:
        raw = r.read().decode()
        return json.loads(raw) if raw else None


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True,
                          check=True).stdout.rstrip("\n")


def local_tree_entries():
    """本地 HEAD 的完整文件清单：[{mode,type,path,sha}, ...]

    必须加 core.quotePath=false：git 默认会把含中文的路径转义成
    \\344\\270\\272 并整体加引号，那样既匹配不上 API 返回的原始路径，
    读文件时也会因引号而 FileNotFoundError。本仓库 115 篇笔记全是中文名。
    """
    entries = []
    raw = git("-c", "core.quotePath=false", "ls-tree", "-r", "HEAD")
    for line in raw.splitlines():
        meta, path = line.split("\t", 1)
        mode, otype, sha = meta.split()
        if otype == "blob":          # 只推文件；子树会被 -r 展开
            entries.append({"mode": mode, "type": "blob",
                            "path": path, "sha": sha})
    return entries


def main():
    dry = "--dry-run" in sys.argv
    force = "--force" in sys.argv

    local_entries = local_tree_entries()
    message = git("log", "-1", "--pretty=%B")
    local_head = git("rev-parse", "HEAD")
    local_tree = git("rev-parse", "HEAD^{tree}")

    parent = api(f"/repos/{REPO}/git/ref/heads/{BRANCH}")["object"]["sha"]
    print(f"远端 {BRANCH} : {parent[:7]}")
    print(f"本地 HEAD    : {local_head[:7]}")
    print(f"本地文件数   : {len(local_entries)}")

    remote_tree = api(f"/repos/{REPO}/git/commits/{parent}")["tree"]["sha"]
    if remote_tree == local_tree:
        print(f"\n✅ 远端 tree 与本地完全一致，无需推送")
        return

    have = {e["path"]: e["sha"]
            for e in api(f"/repos/{REPO}/git/trees/{remote_tree}?recursive=1")["tree"]
            if e["type"] == "blob"}
    missing = [e for e in local_entries if have.get(e["path"]) != e["sha"]]
    print(f"需上传 {len(missing)} 个 blob: "
          f"{', '.join(e['path'] for e in missing) or '（无）'}")

    if dry:
        print("\n[dry-run] 未写入任何内容")
        return

    for e in missing:
        blob = api(f"/repos/{REPO}/git/blobs", "POST", {
            "content": base64.b64encode(open(e["path"], "rb").read()).decode(),
            "encoding": "base64",
        })
        if blob["sha"] != e["sha"]:
            sys.exit(f"❌ blob 上传后 SHA 不一致: {e['path']}")
        print(f"  blob {blob['sha'][:7]}  {e['path']}")

    tree = api(f"/repos/{REPO}/git/trees", "POST", {"tree": local_entries})
    if tree["sha"] != local_tree:
        sys.exit(f"❌ 构造出的 tree 与本地不一致: {tree['sha']} != {local_tree}")
    print(f"tree 校验通过: {tree['sha'][:7]}")

    commit = api(f"/repos/{REPO}/git/commits", "POST", {
        "message": message, "tree": tree["sha"], "parents": [parent],
    })
    api(f"/repos/{REPO}/git/refs/heads/{BRANCH}", "PATCH",
        {"sha": commit["sha"], "force": force})
    print(f"\n✅ 远端 {BRANCH} → {commit['sha'][:7]}")
    print(f"⚠️  本地 {local_head[:7]} 与远端 SHA 不同（内容一致）。")
    print(f"   网络恢复后执行: git fetch origin && git reset --hard origin/{BRANCH}")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as e:
        sys.exit(f"❌ GitHub API {e.code}: {e.read().decode()[:400]}")
