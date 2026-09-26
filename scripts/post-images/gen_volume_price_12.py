"""
volume-price-12-patterns.md 的 3 张配图。
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from _helpers import (
    setup_chinese_font, new_fig, save, style_axes, add_title, add_subtitle, add_footer,
    BG_PAGE, BG_SURFACE, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    ACCENT, ACCENT_SUBTLE, UP, DOWN, BORDER, GRID, W, H, DPI
)

setup_chinese_font()
SLUG = "volume-price-12-patterns"
TOTAL = 3


# ============ 图 1: 12 种量价关系总矩阵（2x6 网格）============
def fig1_twelve_patterns_grid():
    fig, ax = new_fig()
    add_title(fig, "量价关系 12 形态总览：一张图建立全景索引")
    add_subtitle(fig, "红 = 上涨/健康（A 股传统），绿 = 下跌/危险；位置决定一切，死记硬背毫无意义")

    patterns = [
        ("1. 量增价升", "健康上涨", UP, "健康"),
        ("2. 量增价平", "高位漏气", DOWN, "危险"),
        ("3. 量增价跌", "位置决定", DOWN, "危险"),
        ("4. 量平价升", "中继稳健", UP, "待确认"),
        ("5. 量平价跌", "温水青蛙", DOWN, "危险"),
        ("6. 量缩价升", "高位背离", DOWN, "危险"),
        ("7. 量缩价平", "蓄势待发", TEXT_MUTED, "待确认"),
        ("8. 量缩价跌", "底部征兆", UP, "底部"),
        ("9. 天量天价", "顶部信号", DOWN, "危险"),
        ("10. 地量地价", "黎明前夜", UP, "底部"),
        ("11. 量价背离", "反转预警", DOWN, "警惕"),
        ("12. 放量突破", "趋势启动", UP, "健康"),
    ]

    cols = 6
    rows = 2
    cell_w = 0.95 / cols
    cell_h = 0.28
    y_top = 0.82
    y_spacing = 0.04

    for idx, (name, sub, dot_color, marker) in enumerate(patterns):
        col = idx % cols
        row = idx // cols
        x_left = 0.025 + col * cell_w
        y_top_row = y_top - row * (cell_h + y_spacing)

        rect = plt.Rectangle((x_left, y_top_row - cell_h), cell_w - 0.025, cell_h,
                              facecolor=BG_SURFACE, edgecolor=BORDER, lw=0.8,
                              transform=ax.transAxes)
        ax.add_patch(rect)

        # 状态点（top-right）
        circle = plt.Circle((x_left + cell_w - 0.075, y_top_row - 0.05), 0.022,
                             facecolor=dot_color, edgecolor="white", lw=1.5,
                             transform=ax.transAxes)
        ax.add_patch(circle)

        # 名称
        ax.text(x_left + 0.02, y_top_row - 0.075, name,
                ha="left", va="center", fontsize=13, fontweight="bold",
                color=TEXT_PRIMARY, transform=ax.transAxes)
        # 副标
        ax.text(x_left + 0.02, y_top_row - 0.14, sub,
                ha="left", va="center", fontsize=11,
                color=dot_color, transform=ax.transAxes)
        # 标记
        ax.text(x_left + cell_w - 0.075, y_top_row - 0.17, marker,
                ha="center", va="center", fontsize=10,
                color=dot_color, fontweight="bold", transform=ax.transAxes)

    # 底部图例
    ax.text(0.5, 0.13,
            "图例：上涨（红）/ 下跌（绿）—— 按 A 股传统配色，与「健康/危险」语义并行",
            ha="center", fontsize=10, color=TEXT_SECONDARY,
            transform=ax.transAxes)
    ax.text(0.5, 0.09,
            "1~8 是基础组合形态（量 × 价的四种状态），9~12 是单一形态的进阶演化",
            ha="center", fontsize=11, color=TEXT_SECONDARY, style="italic",
            transform=ax.transAxes)

    ax.text(0.5, 0.04,
            "⚠️ 同样的形态放在山顶 vs 山脚，含义完全相反——位置、位置、还是位置",
            ha="center", fontsize=12, color=UP, fontweight="bold",
            transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    add_footer(fig, SLUG, 1, TOTAL)
    return save(fig, SLUG, 1)


# ============ 图 2: 8 种基础形态（2x4 网格，每格上下：量+价）============
def fig2_eight_basic_patterns():
    plt.close("all")
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_PAGE)

    np.random.seed(99)

    panels = [
        # (name, sub, status_color, price_fn, vol_fn, takeaway)
        ("1. 量增价升", "健康上涨", UP,
         lambda d: 10 + np.cumsum(np.random.randn(40) * 0.2 + 0.05),
         lambda d: 5 + 1.5 * (d / 39) + np.random.randn(40) * 0.3,
         "上涨 + 量温和放大 = 健康"),
        ("2. 量增价平", "高位漏气", DOWN,
         lambda d: np.full(40, 13.0) + np.random.randn(40) * 0.2,
         lambda d: 5 + np.where(d < 25, 0.3, 2.0 + (d - 25) * 0.15),
         "放量但涨不动 → 主力派发"),
        ("3. 量增价跌", "位置决定", DOWN,
         lambda d: 13 - d * 0.13 + np.random.randn(40) * 0.3,
         lambda d: 5 + np.where(d < 20, 0.3, 2.0 + (d - 20) * 0.1),
         "高位=出货 · 低位=末期恐慌"),
        ("4. 量平价升", "中继稳健", UP,
         lambda d: 10 + d * 0.08 + np.sin(d / 6) * 0.3,
         lambda d: np.full(40, 4.5) + np.random.randn(40) * 0.3,
         "稳步爬坡 · 但动能衰减需警惕"),
        ("5. 量平价跌", "温水青蛙", DOWN,
         lambda d: 12 - d * 0.06 + np.sin(d / 8) * 0.2,
         lambda d: np.full(40, 4.0) + np.random.randn(40) * 0.2,
         "无人接盘，惯性阴跌"),
        ("6. 量缩价升", "高位背离", DOWN,
         lambda d: 10 + d * 0.12 + np.sin(d / 5) * 0.3,
         lambda d: 6 - d * 0.12 + np.random.randn(40) * 0.3,
         "价新高 + 量萎缩 = 危险背离"),
        ("7. 量缩价平", "蓄势待发", TEXT_MUTED,
         lambda d: np.full(40, 11.0) + np.sin(d / 8) * 0.3,
         lambda d: 6 - d * 0.10 + np.random.randn(40) * 0.2 + 0.5,
         "双方观望，等方向选"),
        ("8. 量缩价跌", "底部征兆", UP,
         lambda d: 13 - d * 0.10 + np.sin(d / 6) * 0.3,
         lambda d: 5 - d * 0.10 + np.random.randn(40) * 0.2 + 0.5,
         "底部酝酿（仅是必要条件）"),
    ]

    gs_outer = GridSpec(2, 4, figure=fig, left=0.04, right=0.97,
                        top=0.86, bottom=0.10,
                        hspace=0.85, wspace=0.20)

    for i, (name, sub, color, p_fn, v_fn, takeaway) in enumerate(panels):
        row, col = i // 4, i % 4
        days = np.arange(40)
        price = p_fn(days)
        vol = v_fn(days)

        gs_inner = gs_outer[row, col].subgridspec(2, 1, hspace=0.0,
                                                   height_ratios=[1.0, 2.0])
        ax_v = fig.add_subplot(gs_inner[0])
        ax_p = fig.add_subplot(gs_inner[1], sharex=ax_v)

        # 量
        ax_v.bar(days, vol, color=color, alpha=0.85, width=0.85, edgecolor="none")
        ax_v.set_xlim(-1, 40)
        ax_v.set_xticks([])
        ax_v.set_yticks([])
        for spine in ["top", "right", "left", "bottom"]:
            ax_v.spines[spine].set_visible(False)
        ax_v.set_facecolor(BG_SURFACE)

        # 价
        ax_p.plot(days, price, color=UP, lw=1.6)
        ax_p.set_xlim(-1, 40)
        ax_p.set_xticks([])
        ax_p.set_yticks([])
        for spine in ax_p.spines.values():
            spine.set_visible(False)
        ax_p.set_facecolor(BG_SURFACE)

        # 在每个 cell 顶部用 ax.text 写标题（放在 cell 上方空间）
        ax_v.text(0.0, 1.22, f"{name}  ·  {sub}",
                  ha="left", va="bottom", fontsize=12, fontweight="bold",
                  color=color, transform=ax_v.transAxes)
        ax_p.text(0.5, -0.30, takeaway, ha="center", va="top",
                  fontsize=10, color=TEXT_SECONDARY,
                  transform=ax_p.transAxes)

        if col == 0:
            ax_v.set_ylabel("量", fontsize=9, color=TEXT_MUTED)
            ax_p.set_ylabel("价", fontsize=9, color=TEXT_MUTED)

    # 大标题（用 fig.text 而不是 suptitle，避免与 panels 重叠）
    fig.text(0.5, 0.965, "8 种基础量价形态：模拟 K 线帮你形成直觉",
             ha="center", va="top", fontsize=20, fontweight="bold", color=TEXT_PRIMARY)
    fig.text(0.5, 0.925,
             "上方柱 = 成交量，下方曲线 = 价格。颜色编码：红 = 上涨/健康 · 绿 = 下跌/危险 · 灰 = 待确认",
             ha="center", va="top", fontsize=11, color=TEXT_SECONDARY, style="italic")

    add_footer(fig, SLUG, 2, TOTAL)
    return save(fig, SLUG, 2, tight=False)


# ============ 图 3: 4 种终极形态（2x2，每格：量+价）============
def fig3_four_ultimate_patterns():
    plt.close("all")
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_PAGE)

    np.random.seed(2024)

    panels = [
        ("9. 天量天价",
         "高位巨量 = 见顶",
         DOWN,
         lambda d: 10 + d * 0.18 + np.sin(d / 3) * 0.5,
         lambda d: 5 + np.where(d < 30, 0.5 + d * 0.05, 6 + np.exp(-(d - 34) ** 2 / 8) * 10),
         "散户最容易做反的信号\n看见天量 → 不是要冲，反而该跑"),
        ("10. 地量地价",
         "成交冷到冰点",
         UP,
         lambda d: 12 - d * 0.06 + np.where(d < 35, np.sin(d / 8) * 0.3, 0.0),
         lambda d: 5 - d * 0.10 + np.where(d < 30, 0.3, 0.5 + np.random.randn(40) * 0.1),
         "卖无可卖，抛压枯竭\n但地量 ≠ 立刻涨，等放量确认"),
        ("11. 量价背离（顶）",
         "最危险的信号",
         DOWN,
         lambda d: 10 + np.where(d < 20, d * 0.10, 2.0 + (d - 20) * 0.08) + np.sin(d / 4) * 0.3,
         lambda d: 6 - np.where(d < 20, d * 0.10, 1.5 + np.maximum(0, (d - 25)) * 0.05) + np.random.randn(40) * 0.2,
         "价创新高，量一次比一次小\n强弩之末，反转之前"),
        ("12. 放量突破",
         "真破 vs 假破",
         UP,
         lambda d: 10 + np.where(d < 25, np.sin(d / 5) * 0.3, 0.3 + (d - 25) * 0.20),
         lambda d: 4 + np.where(d < 25, 0.5, 0.3 + np.exp(-(d - 27) ** 2 / 6) * 10),
         "突破 + 回踩缩量 = 健康\n突破 + 巨量砸下 = 诱多陷阱"),
    ]

    gs_outer = GridSpec(2, 2, figure=fig, left=0.04, right=0.97,
                        top=0.84, bottom=0.10,
                        hspace=0.90, wspace=0.20)

    for i, (name, sub, color, p_fn, v_fn, takeaway) in enumerate(panels):
        row, col = i // 2, i % 2
        days = np.arange(40)
        price = p_fn(days)
        vol = v_fn(days)

        gs_inner = gs_outer[row, col].subgridspec(2, 1, hspace=0.0,
                                                   height_ratios=[1.0, 2.0])
        ax_v = fig.add_subplot(gs_inner[0])
        ax_p = fig.add_subplot(gs_inner[1], sharex=ax_v)

        ax_v.bar(days, vol, color=color, alpha=0.85, width=0.85, edgecolor="none")
        ax_v.set_xlim(-1, 40)
        ax_v.set_xticks([])
        ax_v.set_yticks([])
        for spine in ["top", "right", "left", "bottom"]:
            ax_v.spines[spine].set_visible(False)
        ax_v.set_facecolor(BG_SURFACE)

        ax_p.plot(days, price, color=UP, lw=1.8)
        ax_p.set_xlim(-1, 40)
        ax_p.set_xticks([])
        ax_p.set_yticks([])
        for spine in ax_p.spines.values():
            spine.set_visible(False)
        ax_p.set_facecolor(BG_SURFACE)

        # cell 顶部标题
        ax_v.text(0.0, 1.25, f"{name}  ·  {sub}",
                  ha="left", va="bottom", fontsize=14, fontweight="bold",
                  color=color, transform=ax_v.transAxes)
        # cell 底部 takeaway
        ax_p.text(0.5, -0.30, takeaway, ha="center", va="top",
                  fontsize=11, color=color,
                  transform=ax_p.transAxes)

        if col == 0:
            ax_v.set_ylabel("量", fontsize=9, color=TEXT_MUTED)
            ax_p.set_ylabel("价", fontsize=9, color=TEXT_MUTED)

    fig.text(0.5, 0.965, "4 种终极量价形态：决定买卖的关键信号",
             ha="center", va="top", fontsize=20, fontweight="bold", color=TEXT_PRIMARY)
    fig.text(0.5, 0.92,
             "天量 / 地量 / 背离 / 放量突破 —— 拼起来就是一个完整故事：建仓 → 拉抬 → 派发 → 离场",
             ha="center", va="top", fontsize=11, color=TEXT_SECONDARY, style="italic")

    add_footer(fig, SLUG, 3, TOTAL)
    return save(fig, SLUG, 3, tight=False)


if __name__ == "__main__":
    paths = []
    paths.append(fig1_twelve_patterns_grid())
    paths.append(fig2_eight_basic_patterns())
    paths.append(fig3_four_ultimate_patterns())
    for p in paths:
        print(f"  ✓ {p}")
    print(f"\nGenerated {len(paths)} images for {SLUG}")
