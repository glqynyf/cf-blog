"""
frequent-trading.md 的 3 张配图。
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
SLUG = "frequent-trading"
TOTAL = 3


# ============ 图 1: Barber & Odean 研究 —— 换手率 vs 净收益 ============
def fig1_barber_odean():
    fig, ax = new_fig()
    add_title(fig, "Barber & Odean (2000)：换手率越高的散户，业绩惩罚越大")
    add_subtitle(fig, "美国 66,465 个家庭账户 1991–1996 年实证：换手率最高 20% 的散户每年少赚 6.5%")

    # 分组数据（论文结果）
    groups = ["最低 20%", "次低 20%", "中间 20%", "次高 20%", "最高 20%"]
    returns = np.array([18.5, 17.4, 16.0, 14.0, 11.4])
    turnover = np.array([0, 50, 100, 175, 258])  # 年换手率近似值
    colors = [ACCENT, ACCENT, TEXT_PRIMARY, UP, DOWN]

    bars = ax.bar(groups, returns, color=colors, edgecolor=BG_PAGE, lw=1.5, width=0.65)

    # 大盘基准线
    sp500 = 17.9
    ax.axhline(sp500, color=ACCENT, ls="--", lw=1.8, label=f"标普 500 同期 {sp500:.1f}%")
    ax.text(len(groups) - 1, sp500 + 0.4, f"大盘 {sp500:.1f}%",
            fontsize=10, color=ACCENT, fontweight="bold", ha="right")

    # 业绩惩罚箭头
    ax.annotate("业绩惩罚\n每年 -6.5%",
                xy=(4, 11.4), xytext=(3.0, 7.5),
                fontsize=13, color=DOWN, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.5),
                bbox=dict(boxstyle="round,pad=0.4", fc=BG_SURFACE, ec=DOWN, lw=1.2))

    # 标签
    for bar, val, t in zip(bars, returns, turnover):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.4,
                f"{val:.1f}%",
                ha="center", fontsize=12, color=TEXT_PRIMARY, fontweight="bold")
        ax.text(bar.get_x() + bar.get_width() / 2, 0.6,
                f"换手率\n{t}%" if t > 0 else "换手率\n≈ 0",
                ha="center", fontsize=9, color=TEXT_SECONDARY)

    ax.set_xlabel("按换手率分组的 66,465 个美国家庭账户", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("年化净收益率 (%)", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylim(0, 22)
    ax.legend(loc="upper right", fontsize=10, frameon=False)
    style_axes(ax)

    fig.text(0.5, 0.04,
             "论文标题：「Trading Is Hazardous to Your Wealth」——交易有害于你的财富",
             ha="center", fontsize=11, color=TEXT_MUTED, style="italic")

    add_footer(fig, SLUG, 1, TOTAL)
    return save(fig, SLUG, 1)


# ============ 图 2: 摩擦成本的指数衰减 ============
def fig2_friction_decay():
    fig, ax = new_fig()
    add_title(fig, "摩擦成本 (1 − 0.5%)ⁿ：交易 100 次，本金被磨掉 40%")
    add_subtitle(fig, "每周交易 2 次 × 一年 50 周 = 100 次；股价完全不动，本金也会从 10 万跌到 6.05 万")

    n_trades = np.arange(0, 251)
    cost = 0.005  # 0.5% 单次综合摩擦

    # 不同频率下的剩余资金比例
    f_yearly = (1 - cost) ** (n_trades / 250 * 1)  # 一年 1 次
    f_monthly = (1 - cost) ** (n_trades / 250 * 12)  # 一年 12 次
    f_weekly = (1 - cost) ** (n_trades / 250 * 52)  # 一年 52 次
    f_daily = (1 - cost) ** (n_trades / 250 * 250)  # 一年 250 次

    capital_yearly = 10.0 * f_yearly
    capital_monthly = 10.0 * f_monthly
    capital_weekly = 10.0 * f_weekly
    capital_daily = 10.0 * f_daily

    ax.plot(n_trades, capital_yearly, color=ACCENT, lw=2.5, label="年交易 1 次")
    ax.plot(n_trades, capital_monthly, color=TEXT_PRIMARY, lw=2.5, label="月交易 1 次")
    ax.plot(n_trades, capital_weekly, color=UP, lw=2.5, label="周交易 2 次（剩 60.5%）")
    ax.plot(n_trades, capital_daily, color=DOWN, lw=3.0, label="日交易 1 次（剩 28.4%）")

    ax.fill_between(n_trades, 2.0, capital_weekly, color=UP, alpha=0.10)
    ax.fill_between(n_trades, 2.0, capital_daily, color=DOWN, alpha=0.10)

    ax.annotate("(1 − 0.005)¹⁰⁰ ≈ 0.605\n10 万 → 6.05 万（磨掉 40%）",
                xy=(100, capital_weekly[100]), xytext=(140, 7.5),
                fontsize=12, color=UP, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=UP, lw=1.2),
                bbox=dict(boxstyle="round,pad=0.4", fc=BG_SURFACE, ec=UP, lw=1.0))

    ax.axhline(10.0, color=TEXT_MUTED, ls=":", lw=0.8, alpha=0.5)
    ax.text(250, 10.2, "起点 10 万", fontsize=10, color=TEXT_MUTED, ha="right", va="bottom")

    ax.set_xlabel("一年内的交易次数", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("剩余本金（万元）", fontsize=11, color=TEXT_SECONDARY)
    ax.set_xlim(0, 250)
    ax.set_ylim(2, 11)
    ax.legend(loc="upper right", fontsize=10, frameon=False)
    style_axes(ax)

    fig.text(0.5, 0.04,
             "还没开始判断方向，摩擦就已经悄悄偷走了本金；越频繁，偷得越快",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")

    add_footer(fig, SLUG, 2, TOTAL)
    return save(fig, SLUG, 2)


# ============ 图 3: 处置效应 —— 截利润 + 让亏损奔跑 ============
def fig3_disposition_effect():
    fig, axes = new_fig(aspect=(W, H))
    add_title(fig, "处置效应：散户的「截利润、让亏损奔跑」交易模式")
    add_subtitle(fig, "盈利的票拿不住，亏损的票死扛——大脑避痛本能让你把所有好票卖飞，把坏票留到最后")

    np.random.seed(99)
    n_bars = 30

    plt.close(fig)
    fig, axes = plt.subplots(2, 1, figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_PAGE)
    for ax in axes:
        ax.set_facecolor(BG_PAGE)

    # 真实上涨的优质股
    x1 = np.arange(n_bars)
    p1 = 10 + np.linspace(0, 8, n_bars) + np.random.randn(n_bars) * 0.5
    sells1 = [4, 9, 14, 22]  # 频繁止盈的卖出点

    axes[0].plot(x1, p1, color=ACCENT, lw=2.5, label="真实走势（持续上涨）")
    for s in sells1:
        axes[0].scatter([s], [p1[s]], color=UP, s=200, zorder=5, marker="v",
                         edgecolor=TEXT_PRIMARY, lw=1.5)
    axes[0].scatter([sells1], [p1[sells1]], color=UP, s=200, zorder=5,
                    marker="v", edgecolor=TEXT_PRIMARY, lw=1.5,
                    label="散户止盈点位（每次小赚就跑）")

    axes[0].plot([sells1[-1], 29], [p1[sells1[-1]], p1[-1]],
                 color=DOWN, lw=2.5, ls="--", label="卖飞后涨幅")
    axes[0].annotate("卖飞后\n继续涨 60%+",
                     xy=(29, p1[-1]), xytext=(22, p1.min() - 1.5),
                     fontsize=12, color=DOWN, ha="center", fontweight="bold",
                     arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.0))

    axes[0].set_title("① 好票拿不住：小赚就止盈，错过主升浪",
                     fontsize=13, color=DOWN, loc="left", pad=8)
    axes[0].set_xlim(0, 29)
    axes[0].set_ylim(p1.min() - 2, p1.max() + 1)
    axes[0].legend(loc="upper left", fontsize=10, frameon=False)
    axes[0].set_ylabel("股价", fontsize=10, color=TEXT_SECONDARY)
    style_axes(axes[0])

    # 真实下跌的劣质股
    x2 = np.arange(n_bars)
    p2 = 10 - np.linspace(0, 5, n_bars) + np.random.randn(n_bars) * 0.3
    buys2 = [5, 12, 20]  # 越跌越买的补仓点

    axes[1].plot(x2, p2, color=DOWN, lw=2.5, label="真实走势（持续阴跌）")
    for b in buys2:
        axes[1].scatter([b], [p2[b]], color=UP, s=200, zorder=5, marker="^",
                         edgecolor=TEXT_PRIMARY, lw=1.5)
    axes[1].scatter([buys2], [p2[buys2]], color=UP, s=200, zorder=5,
                    marker="^", edgecolor=TEXT_PRIMARY, lw=1.5,
                    label="散户补仓点位（越跌越买）")

    axes[1].annotate("最终深套\n浮亏 50%",
                     xy=(29, p2[-1]), xytext=(20, p2.max() + 1.5),
                     fontsize=12, color=DOWN, ha="center", fontweight="bold",
                     arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.0))

    axes[1].set_title("② 坏票死扛：不卖就当没亏 → 越跌越补 → 最终套牢",
                     fontsize=13, color=DOWN, loc="left", pad=8)
    axes[1].set_xlim(0, 29)
    axes[1].set_ylim(p2.min() - 1, p2.max() + 2)
    axes[1].legend(loc="upper right", fontsize=10, frameon=False)
    axes[1].set_xlabel("交易日", fontsize=11, color=TEXT_SECONDARY)
    axes[1].set_ylabel("股价", fontsize=10, color=TEXT_SECONDARY)
    style_axes(axes[1])

    fig.suptitle("处置效应：散户的「截利润、让亏损奔跑」交易模式",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.985)
    fig.text(0.5, 0.94,
             "盈利的票拿不住，亏损的票死扛——大脑避痛本能让你把所有好票卖飞，把坏票留到最后",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")
    fig.subplots_adjust(left=0.06, right=0.97, top=0.88, bottom=0.06, hspace=0.40)

    add_footer(fig, SLUG, 3, TOTAL)
    return save(fig, SLUG, 3, tight=False)


if __name__ == "__main__":
    paths = []
    paths.append(fig1_barber_odean())
    paths.append(fig2_friction_decay())
    paths.append(fig3_disposition_effect())
    for p in paths:
        print(f"  ✓ {p}")
    print(f"\nGenerated {len(paths)} images for {SLUG}")