"""
为每篇文章单独生成 OG 分享图。

设计：
- 1200×630 标准 OG 尺寸
- 与站点设计系统同色值（CSS 变量值）
- 文章标题居中突出，左上小品牌、右下域名
- 右侧装饰一组 K 线呼应股票主题

用法：
    python3 scripts/generate-og-images.py          # 生成所有
    python3 scripts/generate-og-images.py welcome # 只生成指定 slug

输出：
    public/og-default.png                ← 全站默认（无文章页用）
    public/og/<slug>.png                 ← 每篇文章一张
"""
import os
import re
import sys
import glob
import random
from PIL import Image, ImageDraw, ImageFont

# ---------- 站点色值（与 src/styles/global.css 一致） ----------
BG_PAGE = (251, 251, 250)         # #fbfbfa
BG_SURFACE = (255, 255, 255)      # #ffffff
TEXT_PRIMARY = (26, 26, 26)       # #1a1a1a
TEXT_SECONDARY = (82, 82, 82)     # #525252
TEXT_MUTED = (115, 115, 115)      # #737373
ACCENT = (15, 118, 110)           # #0f766e
ACCENT_SUBTLE = (204, 251, 241)   # #ccfbf1
UP = (220, 38, 38)                # #dc2626
DOWN = (22, 163, 74)              # #16a34a
BORDER = (231, 229, 228)          # #e7e5e4

W, H = 1200, 630

ROOT = "/Users/mba/Documents/CF-blog"
POSTS_DIR = f"{ROOT}/src/content/posts"
PUBLIC_DIR = f"{ROOT}/public"
OG_DIR = f"{PUBLIC_DIR}/og"


def load_chinese_font(size, weight="regular"):
    """macOS 中文字体加载（带优先级回退）"""
    candidates = [
        ("/System/Library/Fonts/Hiragino Sans GB.ttc", 0 if weight == "regular" else 1),
        ("/System/Library/Fonts/STHeiti Medium.ttc", 0),
        ("/System/Library/Fonts/STHeiti Light.ttc", 0),
    ]
    for path, idx in candidates:
        try:
            return ImageFont.truetype(path, size, index=idx)
        except (OSError, TypeError):
            continue
    return ImageFont.load_default()


# ---------- Frontmatter 解析 ----------
def parse_frontmatter(content):
    """解析 Markdown 文件的 frontmatter，返回 dict"""
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    fm_text = parts[1].strip()
    fm = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        # 处理 tags: ["a", "b"]
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1]
            fm[key] = [v.strip().strip('"').strip("'") for v in inner.split(",") if v.strip()]
        else:
            fm[key] = value.strip('"').strip("'")
    return fm


def get_posts(filter_slugs=None):
    """读取所有文章，返回 [{slug, title, summary, tags}, ...]"""
    posts = []
    for path in sorted(glob.glob(f"{POSTS_DIR}/*.md")):
        slug = os.path.splitext(os.path.basename(path))[0]
        if filter_slugs and slug not in filter_slugs:
            continue
        with open(path, encoding="utf-8") as f:
            fm = parse_frontmatter(f.read())
        if fm.get("draft", "false") in ("true", True):
            continue
        posts.append({
            "slug": slug,
            "title": fm.get("title", slug),
            "summary": fm.get("summary", ""),
            "tags": fm.get("tags", []) if isinstance(fm.get("tags"), list) else [],
        })
    return posts


# ---------- K 线装饰 ----------
def draw_kline_decoration(draw, x, y, w, h, seed):
    """右侧 K 线装饰卡片"""
    # 卡片背景
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=16, fill=BG_SURFACE, outline=BORDER)

    # 标签
    font_mark = load_chinese_font(24)
    draw.text((x + w - 110, y + 22), "〔 K-LINE 〕", fill=TEXT_MUTED, font=font_mark)

    # 8 根 K 线
    random.seed(seed)
    candle_count = 8
    candle_w = 24
    spacing = (w - 80) / candle_count
    baseline = y + h * 0.55

    for i in range(candle_count):
        cx = x + 40 + i * spacing
        is_up = random.random() > 0.45
        color = UP if is_up else DOWN
        body_h = random.randint(40, 140)
        body_top = baseline - body_h // 2
        body_bottom = baseline + body_h // 2
        upper_wick = random.randint(10, 35)
        lower_wick = random.randint(10, 35)
        # 影线
        draw.line([(cx, body_top - upper_wick), (cx, body_top)], fill=color, width=2)
        draw.line([(cx, body_bottom), (cx, body_bottom + lower_wick)], fill=color, width=2)
        # 实体
        draw.rectangle(
            [(cx - candle_w // 2, body_top), (cx + candle_w // 2, body_bottom)],
            fill=color, outline=color
        )


def wrap_text(draw, text, font, max_width, max_lines=2, ellipsis="..."):
    """将文本按 max_width 像素拆成多行，最多 max_lines 行。
    如果超出限制，最后一行末尾加省略号。"""
    lines = []
    current = ""
    for ch in text:
        test = current + ch
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] > max_width and current:
            lines.append(current)
            current = ch
        else:
            current = test
    if current:
        lines.append(current)

    # 超出限制：截断并在最后一行加省略号（仅当省略后能容纳时）
    if len(lines) > max_lines:
        kept = lines[:max_lines]
        last = kept[-1]
        # 如果最后一行加上省略号会超宽，去掉最后一个字符再补省略号
        while last and draw.textbbox((0, 0), last + ellipsis, font=font)[2] > max_width:
            last = last[:-1]
        kept[-1] = (last + ellipsis) if last else ellipsis
        return kept
    return lines


# ---------- 渲染单张 OG 图 ----------
def render_og_image(title, summary, tags, slug):
    """为单篇文章生成 OG 图"""
    img = Image.new("RGB", (W, H), BG_PAGE)
    draw = ImageDraw.Draw(img)

    # 顶部品牌色条
    draw.rectangle([(0, 0), (W, 8)], fill=ACCENT)

    # ---------- 左上：品牌行 ----------
    LEFT_PAD = 80
    font_brand = load_chinese_font(28)
    draw.text((LEFT_PAD, 80), "盘面札记  ·  Trading Notes", fill=ACCENT, font=font_brand)

    # ---------- 主标题（核心元素）----------
    font_title = load_chinese_font(96, weight="bold")
    title_lines = wrap_text(draw, title, font_title, 660, max_lines=2)
    title_y = 170
    title_block_height = 110 * len(title_lines)
    for line in title_lines:
        draw.text((LEFT_PAD, title_y), line, fill=TEXT_PRIMARY, font=font_title)
        title_y += 110

    # ---------- 装饰分隔线 ----------
    sep_y = max(title_y - title_block_height * 0 + 110, 0) + 110
    # 固定 sep_y：标题结束后下移 14px
    sep_y = 170 + title_block_height + 14
    draw.rectangle([(LEFT_PAD, sep_y), (LEFT_PAD + 80, sep_y + 4)], fill=ACCENT)

    # ---------- 摘要（最多 1 行，控制整体高度）----------
    sy = sep_y + 22
    if summary:
        font_summary = load_chinese_font(28)
        summary_lines = wrap_text(draw, summary, font_summary, 660, max_lines=1)
        for line in summary_lines:
            draw.text((LEFT_PAD, sy), line, fill=TEXT_SECONDARY, font=font_summary)
            sy += 38

    # ---------- 标签 chips ----------
    if tags:
        chip_y = sy + 8
        font_chip = load_chinese_font(22)
        chip_x = LEFT_PAD
        for label in tags[:4]:
            text_bbox = draw.textbbox((0, 0), label, font=font_chip)
            chip_w = text_bbox[2] - text_bbox[0] + 28
            chip_h = 38
            draw.rounded_rectangle(
                [(chip_x, chip_y), (chip_x + chip_w, chip_y + chip_h)],
                radius=19, fill=BG_SURFACE, outline=BORDER
            )
            draw.text((chip_x + 14, chip_y + 7), label, fill=TEXT_SECONDARY, font=font_chip)
            chip_x += chip_w + 10
        sy = chip_y + chip_h

    # ---------- 右下：域名（保证在 tags 下方不重叠）----------
    font_url = load_chinese_font(26)
    url_y = max(sy + 18, H - 60)  # 至少在底部 60px 以内
    draw.text((LEFT_PAD, url_y), "stock-blog.duckuno.com", fill=TEXT_MUTED, font=font_url)

    # ---------- 右侧 K 线装饰 ----------
    KX, KY = 760, 130
    KW, KH = 360, 370
    draw_kline_decoration(draw, KX, KY, KW, KH, seed=hash(slug) & 0xFFFF)

    # ---------- 底部品牌色条 ----------
    draw.rectangle([(0, H - 6), (W, H)], fill=ACCENT)

    return img


# ---------- 主流程 ----------
def main():
    os.makedirs(OG_DIR, exist_ok=True)
    posts = get_posts(filter_slugs=sys.argv[1:] or None)

    if not posts:
        print("没有找到任何文章")
        return

    print(f"开始为 {len(posts)} 篇文章生成 OG 图...\n")
    for post in posts:
        img = render_og_image(
            title=post["title"],
            summary=post["summary"],
            tags=post["tags"],
            slug=post["slug"],
        )
        out_path = f"{OG_DIR}/{post['slug']}.png"
        img.save(out_path, "PNG", optimize=True)
        size_kb = os.path.getsize(out_path) / 1024
        print(f"  ✓ {post['slug']}.png  ({size_kb:.1f} KB)  「{post['title'][:30]}...」")

    print(f"\n完成。共 {len(posts)} 张，输出目录：{OG_DIR}/")


if __name__ == "__main__":
    main()