"""
holdings-vs-trapped-chips.md 的 3 张配图。
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
SLUG = "holdings-vs-trapped-chips"
TOTAL = 3


# ============ 图 1: 筹码分布图 CYQ 原理 + 套牢盘压力演示 ============
def fig1_cyq_principle():
    fig, axes = new_fig(aspect=(W, H))
    add_title(fig, "筹码分布图 (CYQ)：一张图看穿「谁在什么价格买走了多少股票」")
    add_subtitle(fig, "横轴 = 价格，纵轴 = 在该价格堆积的持股人数；山峰越厚，那里的阻力 / 支撑就越强")

    np.random.seed(5)

    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_PAGE)
    for ax in axes:
        ax.set_facecolor(BG_PAGE)

    fig.suptitle("筹码分布图 (CYQ)：一张图看穿「谁在什么价格买走了多少股票」",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.985)
    fig.text(0.5, 0.94,
             "横轴 = 价格，纵轴 = 在该价格堆积的持股人数；山峰越厚，那里的阻力 / 支撑就越强",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")

    # ---- 左图：典型 CYQ 山峰 ----
    prices = np.linspace(8, 22, 200)
    # 两个峰：低位的吸筹峰 + 高位的套牢峰
    peak1 = 35 * np.exp(-((prices - 11) ** 2) / 0.6)
    peak2 = 25 * np.exp(-((prices - 17.5) ** 2) / 0.5)
    cyq = peak1 + peak2

    axes[0].fill_between(prices, 0, cyq, color=ACCENT, alpha=0.55, edgecolor=ACCENT, lw=1.5)
    axes[0].plot(prices, cyq, color=ACCENT, lw=1.8)

    # 标注峰
    axes[0].annotate("低位吸筹峰\n（主力底仓）",
                     xy=(11, 35), xytext=(11.5, 45),
                     fontsize=11, color=TEXT_PRIMARY, fontweight="bold", ha="center",
                     arrowprops=dict(arrowstyle="->", color=TEXT_PRIMARY, lw=1.0),
                     bbox=dict(boxstyle="round,pad=0.3", fc=BG_SURFACE, ec=ACCENT, lw=1.0))
    axes[0].annotate("高位套牢峰\n（散户接盘）",
                     xy=(17.5, 25), xytext=(17.5, 38),
                     fontsize=11, color=DOWN, fontweight="bold", ha="center",
                     arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.0),
                     bbox=dict(boxstyle="round,pad=0.3", fc=BG_SURFACE, ec=DOWN, lw=1.0))

    axes[0].set_xlabel("价格 (元)", fontsize=11, color=TEXT_SECONDARY)
    axes[0].set_ylabel("持股人数（堆积量）", fontsize=11, color=TEXT_SECONDARY)
    axes[0].set_xlim(8, 22)
    axes[0].set_ylim(0, 50)
    axes[0].set_title("① 筹码分布 CYQ：双峰形态", fontsize=13, color=TEXT_PRIMARY, loc="left")
    style_axes(axes[0])

    # ---- 右图：套牢盘的解套抛压演示 ----
    days = np.arange(60)
    np.random.seed(7)
    # 价格试图涨回 17.5 → 遭遇套牢盘抛压
    part1 = 11 + days * 0.05
    part2 = 12 - (days - 20) * 0.1 + np.random.randn(60) * 0.3
    part3 = 12 + (days - 40) * 0.55 + np.random.randn(60) * 0.3
    price_try = np.where(days < 20, part1,
                         np.where(days < 40, part2,
                                  np.where(days < 50, part3, 17.5)))

    axes[1].plot(days, price_try, color=UP, lw=2.2, label="价格曲线")
    # 套牢峰位置
    axes[1].axhline(17.5, color=DOWN, ls="--", lw=1.5, alpha=0.7, label="套牢峰 17.5 元")
    axes[1].fill_between(days, 16.5, 18.5, color=DOWN, alpha=0.15, label="抛压密集区")

    # 散户解套卖出标注
    axes[1].annotate("终于解套了！\n一群人同时抛售",
                     xy=(50, 17.5), xytext=(38, 13.5),
                     fontsize=12, color=DOWN, ha="center", fontweight="bold",
                     arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.2),
                     bbox=dict(boxstyle="round,pad=0.4", fc=BG_SURFACE, ec=DOWN, lw=1.2))

    axes[1].set_xlabel("交易日", fontsize=11, color=TEXT_SECONDARY)
    axes[1].set_ylabel("价格 (元)", fontsize=11, color=TEXT_SECONDARY)
    axes[1].set_xlim(0, 59)
    axes[1].set_ylim(10, 20)
    axes[1].set_title("② 套牢盘阻力：涨到那里就被压回", fontsize=13, color=TEXT_PRIMARY, loc="left")
    axes[1].legend(loc="lower left", fontsize=9, frameon=False)
    style_axes(axes[1])

    fig.suptitle("筹码分布图 (CYQ)：一张图看穿「谁在什么价格买走了多少股票」",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.97)
    fig.text(0.5, 0.93,
             "横轴 = 价格，纵轴 = 在该价格堆积的持股人数；山峰越厚，那里的阻力 / 支撑就越强",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")
    fig.subplots_adjust(left=0.06, right=0.97, top=0.86, bottom=0.08, wspace=0.22)

    add_footer(fig, SLUG, 1, TOTAL)
    return save(fig, SLUG, 1, tight=False)


# ============ 图 2: 4 阶段演化 —— 山顶散乱 → 极度缩量 → 放量突破 ============
def fig2_four_stage_evolution():
    fig, axes = new_fig(aspect=(W, H))
    add_title(fig, "大底部四步演化：山顶散乱 → 缓慢下移 → 极度缩量 → 放量突破")
    add_subtitle(fig, "复盘翻倍牛股，几乎都经历过漫长磨底；筹码从高位向低位完整迁移 = 行情酝酿信号")

    np.random.seed(13)
    prices = np.linspace(5, 25, 200)

    plt.close(fig)
    fig, axes = plt.subplots(2, 2, figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_PAGE)
    for ax in axes.flat:
        ax.set_facecolor(BG_PAGE)

    stages = [
        ("① 山顶散乱：上方到处是套牢小峰", "风险最大", DOWN,
         0.20 * np.exp(-((prices - 22) ** 2) / 0.5) +
         0.20 * np.exp(-((prices - 18) ** 2) / 0.4) +
         0.15 * np.exp(-((prices - 14) ** 2) / 0.3) +
         0.15 * np.exp(-((prices - 10) ** 2) / 0.3) +
         0.15 * np.exp(-((prices - 7) ** 2) / 0.3)),
        ("② 缓慢下移：上方峰消融，底部堆筹码", "主力可能在悄悄吸筹", TEXT_PRIMARY,
         0.40 * np.exp(-((prices - 11) ** 2) / 1.0) +
         0.18 * np.exp(-((prices - 16) ** 2) / 0.4) +
         0.10 * np.exp(-((prices - 21) ** 2) / 0.4)),
        ("③ 极度缩量：底部收成一个尖锐点", "该卖的都卖光了", ACCENT,
         0.95 * np.exp(-((prices - 9) ** 2) / 0.15)),
        ("④ 放量突破：冲破密集区，进入真空带", "可能是行情启动", UP,
         0.50 * np.exp(-((prices - 9) ** 2) / 0.3) +
         0.30 * np.exp(-((prices - 18) ** 2) / 1.2)),
    ]

    titles = []
    for ax, (title, subtitle, color, dist) in zip(axes.flat, stages):
        ax.fill_between(prices, 0, dist, color=color, alpha=0.55, edgecolor=color, lw=1.5)
        ax.plot(prices, dist, color=color, lw=1.8)
        ax.text(0.5, 0.95, title, transform=ax.transAxes,
                fontsize=12, color=color, fontweight="bold", ha="center", va="top")
        ax.text(0.5, 0.88, subtitle, transform=ax.transAxes,
                fontsize=10, color=TEXT_SECONDARY, style="italic", ha="center", va="top")
        ax.set_xlim(5, 25)
        ax.set_ylim(0, 1.1)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(BORDER)

    fig.suptitle("大底部四步演化：山顶散乱 → 缓慢下移 → 极度缩量 → 放量突破",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.985)
    fig.text(0.5, 0.94,
             "复盘翻倍牛股，几乎都经历过漫长磨底；筹码从高位向低位完整迁移 = 行情酝酿信号",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")
    fig.subplots_adjust(left=0.04, right=0.98, top=0.88, bottom=0.04, wspace=0.18, hspace=0.35)

    add_footer(fig, SLUG, 2, TOTAL)
    return save(fig, SLUG, 2, tight=False)


# ============ 图 3: 筹码真空区（高速路效应）+ 假跌破识别 ============
def fig3_vacuum_zone():
    fig, axes = new_fig(aspect=(W, H))
    add_title(fig, "真空区 = 股价高速公路；假跌破 = 主力的诱空烟雾弹")
    add_subtitle(fig, "两个常见陷阱：上方无阻挡 = 向上是电梯；下方无托举 = 向下是滑梯；K 线破位但筹码不动 = 诱空")

    np.random.seed(23)
    n = 80
    days = np.arange(n)

    plt.close(fig)
    fig, axes = plt.subplots(2, 1, figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_PAGE)
    for ax in axes:
        ax.set_facecolor(BG_PAGE)

    # ---- 上图：真空区高速路 ----
    price_up = np.zeros(n)
    price_up[0:30] = 10 + np.random.randn(30) * 0.3
    price_up[30:40] = 10 + np.linspace(0, 3.5, 10) + np.random.randn(10) * 0.3  # 突破上轨
    price_up[40:60] = 13.5 + np.linspace(0, 1.5, 20) + np.random.randn(20) * 0.2  # 真空中快速上行
    price_up[60:80] = 15 - np.linspace(0, 1.0, 20) + np.random.randn(20) * 0.3  # 顶部回落

    # 标注真空区
    axes[0].fill_between([30, 60], 10, 18, color=ACCENT_SUBTLE, alpha=0.4, label="筹码真空区")
    axes[0].plot(days, price_up, color=UP, lw=2.0)

    axes[0].annotate("真空区 = 高速路\n（上方无套牢盘阻挡）",
                     xy=(45, 14.5), xytext=(45, 17),
                     fontsize=12, color=ACCENT, ha="center", fontweight="bold",
                     arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.2),
                     bbox=dict(boxstyle="round,pad=0.4", fc=BG_SURFACE, ec=ACCENT, lw=1.2))

    axes[0].annotate("向上是电梯",
                     xy=(50, 15), xytext=(50, 11.5),
                     fontsize=11, color=UP, ha="center", fontweight="bold")
    axes[0].annotate("向下是滑梯",
                     xy=(70, 14.5), xytext=(70, 11.5),
                     fontsize=11, color=DOWN, ha="center", fontweight="bold")

    axes[0].set_title("① 真空区：双向都是高速路 — 顺势而为才能借力",
                     fontsize=13, color=TEXT_PRIMARY, loc="left", pad=8)
    axes[0].set_xlim(0, 79)
    axes[0].set_ylim(8.5, 18)
    axes[0].legend(loc="upper left", fontsize=10, frameon=False)
    axes[0].set_ylabel("价格", fontsize=10, color=TEXT_SECONDARY)
    style_axes(axes[0])

    # ---- 下图：假跌破识别 ----
    price_down = np.zeros(n)
    price_down[0:30] = 10 + np.random.randn(30) * 0.3
    price_down[30:50] = 10 - np.linspace(0, 0.5, 20) + np.random.randn(20) * 0.2  # 横盘
    price_down[50:55] = 9.5 - np.linspace(0, 0.8, 5) + np.random.randn(5) * 0.1  # 假跌破
    price_down[55:65] = 8.7 + np.linspace(0, 0.3, 10) + np.random.randn(10) * 0.1  # 弱势整理
    price_down[65:80] = 9 + np.linspace(0, 3, 15) + np.random.randn(15) * 0.2  # 反向拉升

    support = 9.5
    axes[1].plot(days, price_down, color=UP, lw=2.0, label="价格")
    axes[1].axhline(support, color=TEXT_MUTED, ls="--", lw=1.2, label="支撑位 9.5")
    axes[1].axhline(8.7, color=DOWN, ls=":", lw=1.2, alpha=0.7, label="假跌破低点 8.7")

    axes[1].scatter([52], [8.7], color=DOWN, s=120, zorder=5, marker="x",
                    label="散户止损点")
    axes[1].scatter([52, 72], [8.7, 11.8], color=UP, s=120, zorder=5, marker="^")

    axes[1].annotate("K 线破位\n（看似支撑崩了）",
                     xy=(52, 8.7), xytext=(35, 7.5),
                     fontsize=11, color=DOWN, ha="center",
                     arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.0),
                     bbox=dict(boxstyle="round,pad=0.3", fc=BG_SURFACE, ec=DOWN, lw=1.0))
    axes[1].annotate("但下方筹码\n纹丝不动 = 诱空",
                     xy=(52, 8.7), xytext=(20, 8.0),
                     fontsize=11, color=ACCENT, ha="center",
                     arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.0),
                     bbox=dict(boxstyle="round,pad=0.3", fc=BG_SURFACE, ec=ACCENT, lw=1.0))
    axes[1].annotate("反向拉升\n散户已割肉下车",
                     xy=(75, 12), xytext=(60, 13.5),
                     fontsize=11, color=UP, ha="center", fontweight="bold",
                     arrowprops=dict(arrowstyle="->", color=UP, lw=1.0))

    axes[1].set_title("② 假跌破：K 线破位 ≠ 真的破位 — 看筹码才知真相",
                     fontsize=13, color=TEXT_PRIMARY, loc="left", pad=8)
    axes[1].set_xlim(0, 79)
    axes[1].set_ylim(7, 14)
    axes[1].legend(loc="lower right", fontsize=9, frameon=False)
    axes[1].set_xlabel("交易日", fontsize=11, color=TEXT_SECONDARY)
    axes[1].set_ylabel("价格", fontsize=10, color=TEXT_SECONDARY)
    style_axes(axes[1])

    fig.suptitle("真空区 = 股价高速公路；假跌破 = 主力的诱空烟雾弹",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.985)
    fig.text(0.5, 0.94,
             "两个常见陷阱：上方无阻挡 = 向上是电梯；下方无托举 = 向下是滑梯；K 线破位但筹码不动 = 诱空",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")
    fig.subplots_adjust(left=0.06, right=0.97, top=0.88, bottom=0.06, hspace=0.40)

    add_footer(fig, SLUG, 3, TOTAL)
    return save(fig, SLUG, 3, tight=False)


if __name__ == "__main__":
    paths = []
    paths.append(fig1_cyq_principle())
    paths.append(fig2_four_stage_evolution())
    paths.append(fig3_vacuum_zone())
    for p in paths:
        print(f"  ✓ {p}")
    print(f"\nGenerated {len(paths)} images for {SLUG}")