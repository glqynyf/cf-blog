"""
welcome.md 的 1 张配图：博客内容地图。
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from _helpers import (
    setup_chinese_font, new_fig, save, style_axes, add_title, add_subtitle, add_footer,
    BG_PAGE, BG_SURFACE, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    ACCENT, ACCENT_SUBTLE, UP, DOWN, BORDER, GRID, W, H, DPI
)

setup_chinese_font()
SLUG = "welcome"
TOTAL = 1


# ============ 图 1: 博客内容地图 ============
def fig1_content_map():
    fig, ax = new_fig()
    add_title(fig, "博客内容地图：四条主线串联一个仓位循环")
    add_subtitle(fig, "从基础认知 → 工具箱 → 实战框架 → 风控纪律，读完这些相当于把零散的笔记串成一张网")

    # 中心圆 - 博客
    center = (0.5, 0.55)
    big_circle = plt.Circle(center, 0.13, facecolor=ACCENT, edgecolor="white", lw=2,
                              transform=ax.transAxes)
    ax.add_patch(big_circle)
    ax.text(*center, "盘面机记", ha="center", va="center",
            fontsize=20, fontweight="bold", color="white", transform=ax.transAxes)
    ax.text(center[0], center[1] - 0.04, "记录 · 复盘 · 升级",
            ha="center", va="center", fontsize=10, color="white",
            transform=ax.transAxes)

    # 四周四个象限
    quadrants = [
        # (x_offset, y_offset, color, label, sub_items)
        (0.18, 0.85, ACCENT, "① 交易心得",
         "选股逻辑\n买卖理由\n持仓心态"),
        (0.82, 0.85, UP, "② 技术指标",
         "K 线 / 均线\nMACD / 布林\n量价关系"),
        (0.18, 0.25, TEXT_MUTED, "③ 心态方法",
         "处置效应\n损失厌恶\n知行合一"),
        (0.82, 0.25, DOWN, "④ 读书笔记",
         "《股票作手回忆录》\n《专业投机原理》\n《海龟交易法则》"),
    ]

    for x, y, color, label, sub in quadrants:
        # 卡片
        rect = plt.Rectangle((x - 0.13, y - 0.10), 0.26, 0.20,
                              facecolor=BG_SURFACE, edgecolor=color, lw=2.0,
                              transform=ax.transAxes)
        ax.add_patch(rect)

        # 顶部色条
        bar = plt.Rectangle((x - 0.13, y + 0.05), 0.26, 0.05,
                            facecolor=color, edgecolor="none",
                            transform=ax.transAxes)
        ax.add_patch(bar)

        # 标签
        ax.text(x, y + 0.075, label, ha="center", va="center",
                fontsize=13, fontweight="bold", color="white",
                transform=ax.transAxes)
        # 子项
        ax.text(x, y - 0.04, sub, ha="center", va="center",
                fontsize=10, color=TEXT_PRIMARY,
                transform=ax.transAxes)

        # 连接线
        line_x = [x, center[0]]
        line_y = [y, center[1]]
        # 简化：用注释直接画线
        ax.annotate("", xy=(center[0], center[1]), xytext=(x, y),
                     arrowprops=dict(arrowstyle="-", color=color, lw=1.0, alpha=0.6),
                     xycoords="axes fraction")

    # 顶部说明
    ax.text(0.5, 0.95,
            "这个博客会写什么（四条主线）",
            ha="center", va="top", fontsize=14, color=TEXT_PRIMARY,
            fontweight="bold", transform=ax.transAxes)

    # 底部说明 - 不会写什么
    ax.text(0.5, 0.10,
            "不会写的东西：个股代码即时推荐 / 必胜指标 / 伪复盘",
            ha="center", va="center", fontsize=11,
            color=UP, fontweight="bold", transform=ax.transAxes)
    ax.text(0.5, 0.05,
            "写在白纸黑字上的卖出标准，胜过纸上谈兵的「大师预测」",
            ha="center", va="center", fontsize=10,
            color=TEXT_SECONDARY, style="italic", transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    add_footer(fig, SLUG, 1, TOTAL)
    return save(fig, SLUG, 1)


if __name__ == "__main__":
    paths = []
    paths.append(fig1_content_map())
    for p in paths:
        print(f"  ✓ {p}")
    print(f"\nGenerated {len(paths)} images for {SLUG}")
