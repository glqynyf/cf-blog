#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给笔记批量嵌入 B 站视频讲解卡片（与 S00-01 同一套样式）。

插入点固定在 `<nav class="toc">` 之前，也就是「本文目录」正上方；
CSS 注入到最后一个 `</style>` 之前，保留原有缩进。

两条硬性约束（都是踩过的坑）：
1. 幂等：已存在 video-embed 就跳过，重复跑不会插两份。
2. 内容完整性：注入只允许「新增」，一旦原文件的非空行在结果里消失就判失败、
   不写盘。只验增量不验存量是批处理脚本最危险的盲区。

用法：
    python3 scripts/add-note-video.py              # 处理内置清单
    python3 scripts/add-note-video.py --dry-run    # 只报告不写盘
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTES_DIR = os.path.join(ROOT, 'public', 'notes')

# (文件名前缀, aid, bvid, cid) —— 已用 B 站公开 API 逐条核对过
VIDEOS = [
    ('S00-02', '117374208509616', 'BV1xQHh6sECA', '42412804998'),
    ('S00-03', '117374225221919', 'BV1KSHh6dEi5', '42412869111'),
    ('S00-04', '117374225222062', 'BV1KSHh6dEeX', '42412871180'),
    ('S00-05', '117374241999396', 'BV1PRHh6pEak', '42412934751'),
    ('S00-06', '117374241999771', 'BV1PRHh6pEYS', '42412936267'),
    ('S00-07', '117374258774856', 'BV1NXHh69ERV', '42413000890'),
    ('S00-08', '117374258776982', 'BV1NXHh69Ejk', '42413001848'),
    ('S00-09', '117374258776538', 'BV1NXHh69EKe', '42413064504'),
]

# 与 S00-01 逐字一致的样式，不要随意改动（已上线验证过）
VIDEO_CSS = '''  /* 视频讲解：B 站播放器外链嵌入
     B 站给的 iframe 不带宽高（默认 300×150），必须用 aspect-ratio 容器 + absolute
     撑满才能自适应；直接把 iframe 放进正文在窄屏会撑破版面。 */
  .video-embed {
    margin-bottom: 48px;
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface-2) 100%);
    box-shadow: var(--shadow);
  }
  .video-embed__head {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 16px;
    border-bottom: 1px solid var(--border);
  }
  .video-embed__label {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--accent);
    background: var(--accent-soft);
    border-radius: 4px;
    padding: 3px 8px;
    white-space: nowrap;
  }
  .video-embed__title {
    font-size: 13.5px;
    color: var(--text-dim);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .video-embed__frame {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 9;
    background: #000;
  }
  .video-embed__frame iframe {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    border: 0;
    display: block;
  }
  @media (max-width: 640px) {
    .video-embed { border-radius: 6px; }
    .video-embed__head { padding: 10px 12px; gap: 8px; }
    .video-embed__title { font-size: 12.5px; }
  }
'''


def build_embed(aid: str, bvid: str, cid: str, title: str) -> str:
    src = (
        '//player.bilibili.com/player.html?isOutside=true'
        f'&amp;aid={aid}&amp;bvid={bvid}&amp;cid={cid}&amp;p=1'
    )
    return (
        '<div class="video-embed">\n'
        '  <div class="video-embed__head">\n'
        '    <span class="video-embed__label">▶ 视频讲解</span>\n'
        f'    <span class="video-embed__title">{title}</span>\n'
        '  </div>\n'
        '  <div class="video-embed__frame">\n'
        f'    <iframe src="{src}" scrolling="no" frameborder="no"'
        ' framespacing="0" allowfullscreen="true"'
        f' title="{title}（视频讲解）"></iframe>\n'
        '  </div>\n'
        '</div>\n\n'
    )


def process(path: str, aid: str, bvid: str, cid: str, dry_run: bool) -> str:
    with open(path, encoding='utf-8') as fh:
        html = fh.read()

    if 'video-embed' in html:
        return 'skip'

    original = html

    m_title = re.search(r'<h1 class="note-title">(.*?)</h1>', html, re.S)
    if not m_title:
        return 'error: 未找到 <h1 class="note-title">'
    title = re.sub(r'<[^>]+>', '', m_title.group(1)).strip()

    # 1) HTML 插到 <nav class="toc"> 之前（目录正上方）
    m_toc = re.search(r'<nav class="toc">', html)
    if not m_toc:
        return 'error: 未找到 <nav class="toc">'
    embed = build_embed(aid, bvid, cid, title)
    html = html[:m_toc.start()] + embed + html[m_toc.start():]

    # 2) CSS 插到最后一个 </style> 之前，沿用该行缩进
    idx = html.rfind('</style>')
    if idx == -1:
        return 'error: 未找到 </style>'
    line_start = html.rfind('\n', 0, idx) + 1
    indent = html[line_start:idx]
    html = html[:line_start] + indent + VIDEO_CSS + html[line_start:]

    # 3) 内容完整性断言：原有每一行都还在
    old_lines = [l.rstrip() for l in original.splitlines() if l.strip()]
    new_lines = set(l.rstrip() for l in html.splitlines() if l.strip())
    lost = [l for l in old_lines if l not in new_lines]
    if lost:
        return 'error: 内容丢失 %d 行，例如 %r' % (len(lost), lost[0][:70])

    if dry_run:
        return 'ok'

    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(html)
    return 'ok'


def main() -> int:
    dry_run = '--dry-run' in sys.argv

    by_prefix = {}
    for name in os.listdir(NOTES_DIR):
        if name.endswith('.html'):
            # 文件名形如 S00-02-标题.html，编号本身含一个 '-'
            # （split('-', 1) 会得到 'S00' 而不是 'S00-02'，必须取前两段）
            by_prefix['-'.join(name.split('-')[:2])] = name

    ok = skipped = failed = 0
    for prefix, aid, bvid, cid in VIDEOS:
        name = by_prefix.get(prefix)
        if not name:
            print('  ✗ %s: 找不到对应文件' % prefix)
            failed += 1
            continue

        result = process(os.path.join(NOTES_DIR, name), aid, bvid, cid, dry_run)
        if result == 'ok':
            ok += 1
            print('  ✓ %s%s' % (name, '（dry-run，未写盘）' if dry_run else ''))
        elif result == 'skip':
            skipped += 1
            print('  · %s（已有播放器，跳过）' % name)
        else:
            failed += 1
            print('  ✗ %s: %s' % (name, result))

    print('\n完成：注入 %d 篇，跳过 %d 篇，失败 %d 篇' % (ok, skipped, failed))
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
