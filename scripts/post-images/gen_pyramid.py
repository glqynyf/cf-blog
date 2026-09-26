"""
pyramid-vs-inverted-pyramid.md 的 3 张配图。
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
SLUG = "pyramid-vs-inverted-pyramid"
TOTAL = 3


# ============ 图 1: 正金字塔 vs 倒金字塔结构对比 ============
def fig1_pyramid_vs_inverted():
    fig, axes = new_fig(aspect=(W, H))
    add_title(fig, "正金字塔 vs 倒金字塔：底部买的少、顶部买的多 = 一推就倒")
    add_subtitle(fig, "票对、人亏的真正元凶：不是你选股差，而是持仓结构本身就是头重脚轻")

    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_PAGE)
    for ax in axes:
        ax.set_facecolor(BG_PAGE)

    fig.suptitle("正金字塔 vs 倒金字塔：底部买的少、顶部买的多 = 一推就倒",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.985)
    fig.text(0.5, 0.94,
             "票对、人亏的真正元凶：不是你选股差，而是持仓结构本身就是头重脚轻",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")

    # ---- 左图：倒金字塔（散户常犯） ----
    # 三段宽度从下到上递增：5/15/80
    layers_inv = [
        (0.10, 0.18, "5 千\n(5%)", "底部试探\n（心里没底）"),
        (0.14, 0.30, "1.5 万\n(15%)", "浮盈 20% 后\n（怕错过）"),
        (0.18, 0.34, "8 万\n(80%)", "顶部重仓\n（贪婪追涨）"),
    ]

    cum_y = 0.08
    base_x = 0.30  # 中心位置
    for w, h, val, desc in layers_inv:
        x0 = base_x - w / 2
        ax0 = axes[0]
        ax0.add_patch(plt.Rectangle((x0, cum_y), w, h,
                                    facecolor=DOWN, edgecolor=BG_PAGE, lw=2,
                                    alpha=0.8 - cum_y * 0.3,
                                    transform=ax0.transAxes))
        ax0.text(base_x, cum_y + h / 2, val,
                 transform=ax0.transAxes, ha="center", va="center",
                 fontsize=13, fontweight="bold", color="white")
        ax0.text(base_x + 0.32, cum_y + h / 2, desc,
                 transform=ax0.transAxes, ha="left", va="center",
                 fontsize=11, color=TEXT_PRIMARY)
        cum_y += h

    axes[0].text(0.5, 0.97, "倒金字塔（散户的常态）",
                 transform=axes[0].transAxes, ha="center", fontsize=14,
                 color=DOWN, fontweight="bold")
    axes[0].text(0.5, 0.03, "平均成本钉在高位 · 5% 洗盘就击穿",
                 transform=axes[0].transAxes, ha="center", fontsize=11,
                 color=DOWN, style="italic")

    # 标注危险
    axes[0].annotate("重心极高\n一推就倒",
                     xy=(0.30, 0.55), xytext=(0.05, 0.55),
                     transform=axes[0].transAxes,
                     ha="left", va="center", fontsize=12,
                     color=DOWN, fontweight="bold",
                     arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.2),
                     bbox=dict(boxstyle="round,pad=0.3", fc=BG_SURFACE, ec=DOWN, lw=1.2))

    axes[0].set_xlim(0, 1)
    axes[0].set_ylim(0, 1)
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    for spine in axes[0].spines.values():
        spine.set_visible(False)

    # ---- 右图：正金字塔（机构/老猎人的智慧） ----
    layers_pyr = [
        (0.45, 0.34, "40 万\n(40%)", "底部重仓\n（敢于出手）"),
        (0.30, 0.22, "30 万\n(30%)", "突破后\n（趋势初成）"),
        (0.20, 0.16, "20 万\n(20%)", "再加仓\n（确认趋势）"),
        (0.12, 0.10, "10 万\n(10%)", "机动队\n（按需打）"),
    ]

    cum_y = 0.08
    for w, h, val, desc in layers_pyr:
        x0 = base_x - w / 2
        ax1 = axes[1]
        ax1.add_patch(plt.Rectangle((x0, cum_y), w, h,
                                    facecolor=ACCENT, edgecolor=BG_PAGE, lw=2,
                                    alpha=0.85 - cum_y * 0.15,
                                    transform=ax1.transAxes))
        ax1.text(base_x, cum_y + h / 2, val,
                 transform=ax1.transAxes, ha="center", va="center",
                 fontsize=13, fontweight="bold", color="white")
        ax1.text(base_x + 0.35, cum_y + h / 2, desc,
                 transform=ax1.transAxes, ha="left", va="center",
                 fontsize=11, color=TEXT_PRIMARY)
        cum_y += h

    axes[1].text(0.5, 0.97, "正金字塔（职业选手的纪律）",
                 transform=axes[1].transAxes, ha="center", fontsize=14,
                 color=ACCENT, fontweight="bold")
    axes[1].text(0.5, 0.03, "平均成本钉在低位 · 10% 洗盘依然盈利",
                 transform=axes[1].transAxes, ha="center", fontsize=11,
                 color=ACCENT, style="italic")

    axes[1].annotate("重心极低\n任凭风吹雨打",
                     xy=(0.30, 0.35), xytext=(0.05, 0.35),
                     transform=axes[1].transAxes,
                     ha="left", va="center", fontsize=12,
                     color=ACCENT, fontweight="bold",
                     arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.2),
                     bbox=dict(boxstyle="round,pad=0.3", fc=BG_SURFACE, ec=ACCENT, lw=1.2))

    axes[1].set_xlim(0, 1)
    axes[1].set_ylim(0, 1)
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    for spine in axes[1].spines.values():
        spine.set_visible(False)

    fig.subplots_adjust(left=0.04, right=0.97, top=0.88, bottom=0.05, wspace=0.10)

    add_footer(fig, SLUG, 1, TOTAL)
    return save(fig, SLUG, 1, tight=False)


# ============ 图 2: 完整正金字塔买入流程 ============
def fig2_pyramid_buying():
    fig, axes = new_fig(aspect=(W, H))
    add_title(fig, "正金字塔建仓 4 阶段：底仓 40% → 加仓 30% → 再加 20% → 机动 10%")
    add_subtitle(fig, "每笔加仓只在浮盈 10%+ 后触发；加的不是价格，是确定性 — 这就是顺势加仓的核心")

    np.random.seed(31)
    n = 90
    days = np.arange(n)

    plt.close(fig)
    fig, axes = plt.subplots(2, 1, figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_PAGE)
    for ax in axes:
        ax.set_facecolor(BG_PAGE)

    fig.suptitle("正金字塔建仓 4 阶段：底仓 40% → 加仓 30% → 再加 20% → 机动 10%",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.985)
    fig.text(0.5, 0.94,
             "每笔加仓只在浮盈 10%+ 后触发；加的不是价格，是确定性 — 这就是顺势加仓的核心",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")

    # ---- 上图：价格走势 + 加仓点 ----
    np.random.seed(31)
    price = np.zeros(n)
    price[0:25] = 10 + np.linspace(0, 0.3, 25) + np.random.randn(25) * 0.15  # 筑底
    price[25:45] = 10.3 + np.linspace(0, 1.0, 20) + np.random.randn(20) * 0.25  # 第一波
    price[45:55] = 11.3 - np.linspace(0, 0.6, 10) + np.random.randn(10) * 0.2  # 洗盘
    price[55:80] = 10.7 + np.linspace(0, 2.5, 25) + np.random.randn(25) * 0.25  # 主升
    price[80:90] = 13.2 + np.linspace(0, 1.0, 10) + np.random.randn(10) * 0.2  # 加速

    axes[0].plot(days, price, color=TEXT_PRIMARY, lw=2.2, label="价格")

    # 4 个加仓点
    buy_points = [(20, "① 底仓 40万", ACCENT),
                  (40, "② 加仓 30万", ACCENT),
                  (62, "③ 再加 20万", ACCENT),
                  (85, "④ 机动 10万", ACCENT)]
    for d, label, c in buy_points:
        axes[0].scatter([d], [price[d]], color=c, s=180, zorder=5,
                        edgecolor=TEXT_PRIMARY, lw=2)
        axes[0].annotate(label,
                         xy=(d, price[d]), xytext=(d, price[d] - 1.5),
                         ha="center", fontsize=11, color=ACCENT, fontweight="bold",
                         arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.0))

    axes[0].set_title("① 4 笔加仓点：每笔只在趋势确认后触发",
                     fontsize=13, color=TEXT_PRIMARY, loc="left", pad=8)
    axes[0].set_xlim(0, 89)
    axes[0].set_ylim(9, 16)
    axes[0].legend(loc="upper left", fontsize=10, frameon=False)
    axes[0].set_ylabel("价格", fontsize=10, color=TEXT_SECONDARY)
    style_axes(axes[0])

    # ---- 下图：累计仓位 / 平均成本（双 Y 轴）----
    buys = [(20, 40, 10.0), (40, 30, 11.0), (62, 20, 11.5), (85, 10, 13.0)]
    total_cost = 0.0
    total_shares = 0.0
    avg_cost = np.zeros(n)

    # 累计仓位百分比 (step)
    cum_pct_arr = np.zeros(n)
    for i, (d, _, _) in enumerate(buys):
        mask = days >= d
        cum_pct_arr[mask] += [40, 30, 20, 10][i]

    # 加权平均成本
    for d in range(n):
        for bd, bv, bp in buys:
            if d == bd:
                total_shares += bv / bp
                total_cost += bv
        if total_shares > 0:
            avg_cost[d] = total_cost / total_shares

    ax2 = axes[1]
    # 左 Y 轴：加权平均成本
    ax2.plot(days, avg_cost, color=ACCENT, lw=2.5, ls="-",
             label="加权平均成本 (元)")
    ax2.set_ylim(9.5, 14)
    ax2.set_ylabel("成本 (元)", fontsize=10, color=TEXT_SECONDARY)

    # 右 Y 轴：累计仓位
    ax2b = ax2.twinx()
    ax2b.plot(days, cum_pct_arr, color=UP, lw=2.5, ls="--",
              label="累计仓位 (%)")
    ax2b.set_ylim(0, 110)
    ax2b.set_ylabel("仓位 (%)", fontsize=10, color=UP)
    ax2b.tick_params(axis="y", colors=UP, labelsize=9)
    ax2b.spines["top"].set_visible(False)

    # 标注 4 个阶段
    for d, _, _ in buys:
        ax2.axvline(d, color=TEXT_MUTED, ls=":", lw=0.8, alpha=0.5)

    # 合并图例
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2b.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2,
               loc="upper left", fontsize=10, frameon=False)

    ax2.set_title("② 加权平均成本 vs 累计仓位：成本在低位，仓位随趋势放大",
                  fontsize=13, color=TEXT_PRIMARY, loc="left", pad=8)
    ax2.set_xlim(0, 89)
    ax2.set_xlabel("交易日", fontsize=11, color=TEXT_SECONDARY)
    style_axes(ax2, grid_axis="y")

    fig.suptitle("正金字塔建仓 4 阶段：底仓 40% → 加仓 30% → 再加 20% → 机动 10%",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.985)
    fig.text(0.5, 0.94,
             "每笔加仓只在浮盈 10%+ 后触发；加的不是价格，是确定性 — 这就是顺势加仓的核心",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")
    fig.subplots_adjust(left=0.06, right=0.97, top=0.88, bottom=0.06, hspace=0.40)

    add_footer(fig, SLUG, 2, TOTAL)
    return save(fig, SLUG, 2, tight=False)


# ============ 图 3: 倒金字塔卖出 + 盈亏比 3:1 ============
def fig3_sell_and_risk_reward():
    fig, axes = new_fig(aspect=(W, H))
    add_title(fig, "倒金字塔卖出 + 盈亏比 3:1 = 完整的交易闭环")
    add_subtitle(fig, "越涨卖越多 = 胜利者落袋仪式；盈亏比 3:1 = 一笔交易最朴素的数学目标")

    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_PAGE)
    for ax in axes:
        ax.set_facecolor(BG_PAGE)

    fig.suptitle("倒金字塔卖出 + 盈亏比 3:1 = 完整的交易闭环",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.985)
    fig.text(0.5, 0.94,
             "越涨卖越多 = 胜利者落袋仪式；盈亏比 3:1 = 一笔交易最朴素的数学目标",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")

    # ---- 左图：倒金字塔卖出示意 ----
    # 三段宽度从下到上递减：60/30/10
    layers_sell = [
        (0.45, 0.40, "第一减仓\n30%", "浮盈 30%\n市场情绪高昂\n果断落袋"),
        (0.30, 0.26, "第二减仓\n40%", "浮盈 40%+\n市场狂热\n主力撤退"),
        (0.18, 0.16, "尾仓\n30%", "趋势未坏\n保留跟踪\n涨到哪算哪"),
    ]

    cum_y = 0.10
    base_x = 0.30
    for w, h, val, desc in layers_sell:
        x0 = base_x - w / 2
        axes[0].add_patch(plt.Rectangle((x0, cum_y), w, h,
                                        facecolor=UP, edgecolor=BG_PAGE, lw=2,
                                        alpha=0.85 - cum_y * 0.25,
                                        transform=axes[0].transAxes))
        axes[0].text(base_x, cum_y + h / 2, val,
                     transform=axes[0].transAxes, ha="center", va="center",
                     fontsize=13, fontweight="bold", color="white")
        axes[0].text(base_x + 0.36, cum_y + h / 2, desc,
                     transform=axes[0].transAxes, ha="left", va="center",
                     fontsize=10, color=TEXT_PRIMARY)
        cum_y += h

    axes[0].text(0.5, 0.97, "倒金字塔卖出（越涨卖越多）",
                 transform=axes[0].transAxes, ha="center", fontsize=14,
                 color=UP, fontweight="bold")
    axes[0].text(0.5, 0.04, "胜利者落袋仪式 — 利润保护下来才算赚",
                 transform=axes[0].transAxes, ha="center", fontsize=11,
                 color=UP, style="italic")

    axes[0].set_xlim(0, 1)
    axes[0].set_ylim(0, 1)
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    for spine in axes[0].spines.values():
        spine.set_visible(False)

    # ---- 右图：盈亏比 3:1 示意 ----
    # 一笔交易：止损 -1 元，止盈 +3 元
    entry = 10.0
    stop_loss = 9.0
    take_profit = 13.0

    # 价格线
    price_path = np.linspace(entry, 13.5, 100)

    # 关键水平线
    axes[1].axhline(entry, color=TEXT_PRIMARY, ls="-", lw=1.5, label="进场价 10.0")
    axes[1].axhline(stop_loss, color=DOWN, ls="--", lw=2.0, label="止损 -1")
    axes[1].axhline(take_profit, color=ACCENT, ls="--", lw=2.0, label="止盈 +3")

    # 风险/收益区
    axes[1].fill_between([0, 100], entry, stop_loss, color=DOWN, alpha=0.15, label="风险区 (-1)")
    axes[1].fill_between([0, 100], entry, take_profit, color=ACCENT, alpha=0.15, label="收益区 (+3)")

    # 盈亏比标注
    axes[1].annotate("风险 1", xy=(50, 9.5), xytext=(20, 9.0),
                     fontsize=14, color=DOWN, fontweight="bold", ha="center",
                     arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.0))
    axes[1].annotate("收益 3", xy=(50, 11.5), xytext=(80, 10.5),
                     fontsize=14, color=ACCENT, fontweight="bold", ha="center",
                     arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.0))

    # 大字盈亏比
    axes[1].text(50, 13.7, "盈亏比 = 3 : 1",
                 transform=axes[1].transData, ha="center", fontsize=20,
                 color=UP, fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.5", fc=BG_SURFACE, ec=UP, lw=2.0))

    axes[1].set_xlim(0, 100)
    axes[1].set_ylim(7.5, 15)
    axes[1].set_xlabel("价格走势", fontsize=10, color=TEXT_SECONDARY)
    axes[1].set_ylabel("价格", fontsize=10, color=TEXT_SECONDARY)
    axes[1].legend(loc="lower right", fontsize=9, frameon=False)
    axes[1].set_title("盈亏比 3:1：每笔交易最朴素的数学目标",
                     fontsize=12, color=TEXT_PRIMARY, loc="left", pad=10)
    style_axes(axes[1])

    fig.subplots_adjust(left=0.04, right=0.97, top=0.88, bottom=0.08, wspace=0.30)

    add_footer(fig, SLUG, 3, TOTAL)
    return save(fig, SLUG, 3, tight=False)


if __name__ == "__main__":
    paths = []
    paths.append(fig1_pyramid_vs_inverted())
    paths.append(fig2_pyramid_buying())
    paths.append(fig3_sell_and_risk_reward())
    for p in paths:
        print(f"  ✓ {p}")
    print(f"\nGenerated {len(paths)} images for {SLUG}")