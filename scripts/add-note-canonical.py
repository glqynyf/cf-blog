#!/usr/bin/env python3
"""
给 115 篇笔记注入 <link rel="canonical">。

背景：Cloudflare Pages 对 /notes/X 与 /notes/X.html 两种形式都返回 200，
而笔记是独立 HTML、原本没有任何 canonical，搜索引擎会把同一篇当成两份
重复内容，sitemap 里的条目也就失去了「指向唯一版本」的意义。

统一指向无扩展名形式 /notes/{slug}：
  - 与 /notes/ 索引页的 115 条站内链接形式一致
  - 与 astro.config.mjs 里 sitemap customPages 生成的 URL 完全一致

严格幂等：已存在 rel="canonical" 即跳过。
"""
import io
import os
import re
import sys
import urllib.parse

SITE = 'https://stock-blog.duckuno.com'
NOTES_DIR = 'public/notes'


def main():
    names = sorted(f for f in os.listdir(NOTES_DIR) if f.endswith('.html'))
    done = skipped = failed = 0

    for name in names:
        path = os.path.join(NOTES_DIR, name)
        html = io.open(path, encoding='utf-8').read()

        if 'rel="canonical"' in html:
            skipped += 1
            continue

        # 115 篇笔记的 head 收尾写法不统一：17 篇有 </head>，
        # 98 篇直接 </style> 后就是 <body>（浏览器会自动补 head 闭合）。
        # 两种情况都要能插入，且要落在 head 内、body 外。
        m = re.search(r'</head>', html, re.I)
        if m:
            at = m.start()
        else:
            m = re.search(r'<body[^>]*>', html, re.I)
            if not m:
                failed += 1
                print('  ❌ 找不到 </head> 或 <body>: %s' % name)
                continue
            at = m.start()

        slug = name[:-len('.html')]
        url = '%s/notes/%s' % (SITE, urllib.parse.quote(slug, safe=''))
        tag = '  <link rel="canonical" href="%s">\n' % url

        html = html[:at] + tag + html[at:]
        io.open(path, 'w', encoding='utf-8').write(html)
        done += 1

    print('笔记总数 %d' % len(names))
    print('  注入 canonical  %d' % done)
    print('  已存在跳过      %d' % skipped)
    if failed:
        print('  失败            %d' % failed)
        sys.exit(1)


if __name__ == '__main__':
    main()
