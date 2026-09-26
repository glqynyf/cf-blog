"""
bollinger-bands-probability-not-bottom-fishing.md 的 4 张配图。
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib.pyplot as plt
from _helpers import (
    setup_chinese_font, new_fig, save, style_axes, add_title, add_subtitle, add_footer,
    BG_PAGE, BG_SURFACE, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    ACCENT, ACCENT_SUBTLE, UP, DOWN, BORDER, GRID, W, H
)

setup_chinese_font()
SLUG = "bollinger-bands-probability-not-bottom-fishing"
TOTAL = 4


# ============ 图 1: 布林带结构示意 ============
def fig1_band_structure():
    fig, ax = new_fig()
    add_title(fig, "布林带结构：一条中轨 + 两倍标准差的上下通道")

    # 模拟价格 + 中轨 + 上下轨
    np.random.seed(42)
    days = np.arange(60)
    mid = 10 + 0.02 * days + np.sin(days / 8) * 0.3
    vol = 0.5 + np.abs(np.sin(days / 12)) * 0.4
    price = mid + np.random.randn(60) * vol * 0.4
    upper = mid + 2 * vol
    lower = mid - 2 * vol

    # 填充通道（淡色）
    ax.fill_between(days, lower, upper, color=ACCENT_SUBTLE, alpha=0.6, label="95.4% 区间（±2σ）")

    # 三条线
    ax.plot(days, upper, color=ACCENT, lw=1.6, label="上轨（中轨 + 2σ）")
    ax.plot(days, mid, color=TEXT_PRIMARY, lw=1.6, ls="--", label="中轨（20 日均线）")
    ax.plot(days, lower, color=ACCENT, lw=1.6, label="下轨（中轨 − 2σ）")

    # 价格（用 K 线效果更直观，但线图先做）
    ax.plot(days, price, color=UP, lw=1.4, alpha=0.9, label="价格")

    # 标注几个关键点
    ax.annotate("下轨抄底陷阱\n（继续下跌）",
                xy=(45, lower[45]), xytext=(48, lower[45] - 1.5),
                fontsize=11, color=DOWN, ha="center",
                arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.2))

    # 右侧标注线
    ax.text(61, mid[30], "中轨\n20 日均线", color=TEXT_PRIMARY,
            fontsize=11, va="center", ha="left",
            bbox=dict(boxstyle="round,pad=0.3", fc=BG_SURFACE, ec=BORDER, lw=0.8))
    ax.text(61, upper[30], "上轨", color=ACCENT, fontsize=11, va="center", ha="left", fontweight="bold")
    ax.text(61, lower[30], "下轨", color=ACCENT, fontsize=11, va="center", ha="left", fontweight="bold")

    ax.set_xlim(-2, 70)
    ax.set_ylim(lower.min() - 2, upper.max() + 2)
    ax.set_xlabel("交易日", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("价格", fontsize=11, color=TEXT_SECONDARY)
    style_axes(ax)
    ax.legend(loc="upper left", fontsize=10, frameon=False, ncol=2)

    add_footer(fig, SLUG, 1, TOTAL)
    return save(fig, SLUG, 1)


# ============ 图 2: 正态分布 + 概率表 ============
def fig2_normal_distribution():
    fig, ax = new_fig()
    add_title(fig, "正态分布的黄金法则：±2σ 对应 95.4% 的覆盖率")

    x = np.linspace(-4, 4, 500)
    y = np.exp(-x**2 / 2) / np.sqrt(2 * np.pi)

    ax.plot(x, y, color=TEXT_PRIMARY, lw=1.8, label="正态分布密度")

    # 填充区间
    ax.fill_between(x, y, where=(x >= -3) & (x <= 3), color=ACCENT_SUBTLE, alpha=0.4)
    ax.fill_between(x, y, where=(x >= -2) & (x <= 2), color=ACCENT, alpha=0.25)
    ax.fill_between(x, y, where=(x >= -1) & (x <= 1), color=ACCENT, alpha=0.45)

    # 标注区间
    for mu, label, color in [
        (-3, "−3σ", TEXT_MUTED), (-2, "−2σ", ACCENT),
        (-1, "−1σ", ACCENT), (1, "+1σ", ACCENT),
        (2, "+2σ", ACCENT), (3, "+3σ", TEXT_MUTED)]:
        ax.axvline(mu, color=color, ls=":", lw=0.9, alpha=0.7)
        ax.text(mu, -0.04, label, ha="center", va="top",
                fontsize=11, color=color, fontweight="bold")

    # 概率注释
    ax.annotate("±1σ ≈ 68.27%", xy=(0, 0.35), xytext=(-2.5, 0.42),
                fontsize=12, color=ACCENT, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=0.8))
    ax.annotate("±2σ ≈ 95.44%\n（布林带默认）", xy=(1.5, 0.12), xytext=(2.4, 0.32),
                fontsize=13, color=UP, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=UP, lw=1.0))
    ax.annotate("±3σ ≈ 99.74%", xy=(2.7, 0.05), xytext=(3.0, 0.20),
                fontsize=11, color=TEXT_SECONDARY,
                arrowprops=dict(arrowstyle="->", color=TEXT_SECONDARY, lw=0.8))

    ax.set_xlim(-4, 4)
    ax.set_ylim(-0.06, 0.45)
    ax.set_xlabel("标准差倍数（σ）", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("概率密度", fontsize=11, color=TEXT_SECONDARY)
    ax.set_yticks([])
    style_axes(ax, grid=False)
    ax.spines["left"].set_visible(False)

    add_footer(fig, SLUG, 2, TOTAL)
    return save(fig, SLUG, 2)


# ============ 图 3: 三种实战形态 ============
def fig3_three_patterns():
    fig, axes = new_fig(aspect=(W, H))
    add_title(fig, "布林带实战三大形态：震荡 / 收口变盘 / 走边")

    np.random.seed(7)

    def draw_one(ax, name, generator):
        days = np.arange(60)
        mid, upper, lower, price = generator(days)
        ax.fill_between(days, lower, upper, color=ACCENT_SUBTLE, alpha=0.5)
        ax.plot(days, upper, color=ACCENT, lw=1.2)
        ax.plot(days, mid, color=TEXT_PRIMARY, lw=1.2, ls="--")
        ax.plot(days, lower, color=ACCENT, lw=1.2)
        ax.plot(days, price, color=UP, lw=1.4)
        ax.set_title(name, fontsize=14, color=TEXT_PRIMARY, pad=10)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(BORDER)
        ax.set_xlim(0, 59)

    # 形态 1: 震荡市
    def gen_range(days):
        mid = np.full_like(days, 10.0, dtype=float)
        upper = mid + 1.5
        lower = mid - 1.5
        price = 10 + np.sin(days / 5) * 1.3 + np.random.randn(60) * 0.15
        return mid, upper, lower, price

    # 形态 2: 收口后变盘
    def gen_squeeze_breakout(days):
        mid = 10 + np.where(days < 35, 0, (days - 35) * 0.18)
        vol = np.where(days < 35, 0.4 - days * 0.005, 0.25 + (days - 35) * 0.04)
        upper = mid + 2 * vol
        lower = mid - 2 * vol
        price = mid + np.where(days < 35, np.random.randn(60) * vol * 0.4,
                               np.random.randn(60) * vol * 0.6 + (days - 35) * 0.25)
        return mid, upper, lower, price

    # 形态 3: 沿轨行走
    def gen_walking(days):
        mid = 10 + days * 0.15
        vol = np.full_like(days, 1.5, dtype=float)
        upper = mid + 2 * vol
        lower = mid - 2 * vol
        # 价格贴上轨走
        price = upper - np.abs(np.random.randn(60)) * 0.4
        return mid, upper, lower, price

    # 三张子图竖排
    plt.close(fig)
    fig, axes = plt.subplots(3, 1, figsize=(W / 100, H / 100), dpi=100)
    fig.patch.set_facecolor(BG_PAGE)

    for ax in axes:
        ax.set_facecolor(BG_PAGE)

    draw_one(axes[0], "① 震荡市：上下轨为支撑压力（可逆势做）", gen_range)
    draw_one(axes[1], "② 收口 → 变盘：通道收窄后突破，跟随新趋势", gen_squeeze_breakout)
    draw_one(axes[2], "③ 沿轨行走（走边）：强势趋势，别逆势抄顶/底", gen_walking)

    fig.suptitle("布林带实战三大形态：震荡 / 收口变盘 / 走边",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.97)
    fig.text(0.5, 0.92,
             "用错场景，再好的工具也会害你——震荡市 vs 趋势市要区分清楚",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")
    fig.subplots_adjust(left=0.05, right=0.97, top=0.86, bottom=0.06, hspace=0.55)

    add_footer(fig, SLUG, 3, TOTAL)
    return save(fig, SLUG, 3, tight=False)


# ============ 图 4: 参数调整表 ============
def fig4_params_table():
    fig, ax = new_fig()
    add_title(fig, "布林格本人的调参对应法则")
    add_subtitle(fig, "周期拉长，标准差倍数也对应微调——周期 10/20/50 → 倍数 1.9/2.0/2.1")

    # 表格式数据
    rows = [
        ("中轨周期", "标准差倍数", "适用场景"),
        ("10 日", "1.9", "短线 / 当冲"),
        ("20 日（默认）", "2.0", "波段 / 日线"),
        ("50 日", "2.1", "中长线 / 周线"),
    ]
    cell_colors = [
        [BG_SURFACE, BG_SURFACE, BG_SURFACE],
        [BG_SURFACE, BG_SURFACE, BG_SURFACE],
        [ACCENT_SUBTLE, ACCENT_SUBTLE, ACCENT_SUBTLE],  # 默认高亮
        [BG_SURFACE, BG_SURFACE, BG_SURFACE],
    ]
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            weight = "bold" if (i == 0 or i == 2) else "normal"
            color = TEXT_PRIMARY if i == 0 else (ACCENT if i == 2 else TEXT_PRIMARY)
            ax.text(j, 3 - i, val, ha="center", va="center",
                    fontsize=16 if i == 0 else 18, color=color, fontweight=weight)

    # 表格边框
    for i in range(4):
        ax.axhline(3 - i + 0.5, color=BORDER, lw=0.8)
    ax.axhline(-0.5, color=BORDER, lw=0.8)
    for j in range(4):
        ax.axvline(j - 0.5, color=BORDER, lw=0.8)

    # 规律提示
    fig.text(0.5, 0.18,
             "规律：周期越长 → 数据越平滑 → 需要略大的标准差来覆盖正常波动",
             ha="center", fontsize=13, color=TEXT_SECONDARY, style="italic")
    fig.text(0.5, 0.13,
             "⚠️ 新手建议：先用默认 20 日 + 2.0 倍，吃透再谈微调",
             ha="center", fontsize=12, color=UP, fontweight="bold")

    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.8, 3.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    add_footer(fig, SLUG, 4, TOTAL)
    return save(fig, SLUG, 4)


if __name__ == "__main__":
    paths = []
    paths.append(fig1_band_structure())
    paths.append(fig2_normal_distribution())
    paths.append(fig3_three_patterns())
    paths.append(fig4_params_table())
    for p in paths:
        print(f"  ✓ {p}")
    print(f"\nGenerated {len(paths)} images for {SLUG}")
