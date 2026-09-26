"""
kelly-formula-shannon-devil-532.md 的 5 张配图。
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
SLUG = "kelly-formula-shannon-devil-532"
TOTAL = 5


# ============ 图 1: 波动性损耗 ============
def fig1_volatility_drag():
    fig, ax = new_fig()
    add_title(fig, "波动性损耗：第一年翻倍 + 第二年腰斩 = 白干两年")
    add_subtitle(fig, "哪怕你每一年都买对了方向，只要波动大，复利收益就被悄悄吞噬")

    np.random.seed(101)
    days = np.arange(20)
    # 三种策略对比
    # A：稳定 15% 年化
    a = np.cumprod(np.full(20, 1.15) ** (1 / 19))
    # B：大波动后归零（+100% / -50% / +100% / -50%）
    returns_b = np.array([1.0] + [1.5, 0.5] * 9 + [0.83])  # 头尾调整
    b = np.cumprod(returns_b[:20])
    # C：先涨 100% 后跌 50%
    c = np.array([1.0] + [2.0 if i == 1 else 0.5 if i == 2 else 1.0 for i in range(1, 20)])

    ax.plot(days, a, color=ACCENT, lw=2.5, marker="o", label="稳定 15% 年化（A）", markersize=4)
    ax.plot(days, b, color=UP, lw=2.5, marker="s", label="大涨大跌交替（B）", markersize=4)
    ax.plot(days, c, color=DOWN, lw=2.5, marker="^", label="先涨 100% 再跌 50%（C）", markersize=4)

    # 标注
    ax.axhline(1.0, color=TEXT_MUTED, ls=":", lw=0.8, alpha=0.6)
    ax.text(19, 1.0, "起点 1.0", fontsize=10, color=TEXT_MUTED, va="bottom", ha="right")

    ax.annotate("C 两年回到原点\n（先 +100% 再 -50% = 0）",
                xy=(2, 0.5), xytext=(5, 0.3),
                fontsize=11, color=DOWN, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.2))

    ax.set_xlabel("年份", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("资金曲线（起点 = 1.0）", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylim(0.3, 1.6)
    ax.set_xlim(0, 19)
    ax.legend(loc="upper left", fontsize=10, frameon=False)
    style_axes(ax)

    add_footer(fig, SLUG, 1, TOTAL)
    return save(fig, SLUG, 1)


# ============ 图 2: 凯利公式曲线 ============
def fig2_kelly_curve():
    fig, ax = new_fig()
    add_title(fig, "凯利公式 f* = (bp − q) / b：胜率 + 赔率决定最优下注比例")
    add_subtitle(fig, "横轴 = 胜率 p，纵轴 = 最优下注比例 f*（红线 = 满仓 = 100% 仓位）")

    # 例：胜赔比 b = 2（赢了赚 2 倍，输了亏光）
    b = 2.0
    p = np.linspace(0, 1, 200)
    f = (b * p - (1 - p)) / b  # 凯利公式

    ax.plot(p, f * 100, color=ACCENT, lw=2.5, label="凯利最优仓位 f*（%）")
    ax.axhline(0, color=TEXT_MUTED, lw=1.0)
    ax.axhline(100, color=DOWN, ls=":", lw=1.5, label="满仓 100%（危险）")
    ax.axhline(50, color=UP, ls=":", lw=1.0, label="半凯利 50%（稳健）")

    # 临界点 p = 1/(b+1)
    critical = 1 / (b + 1)
    ax.axvline(critical, color=DOWN, ls=":", lw=1.0, alpha=0.7)
    ax.text(critical, 105, f"  临界点 p = {critical:.2f}\n  (低于此胜率应空仓)",
            fontsize=10, color=DOWN, va="bottom", ha="left")

    # 阴影区（满仓危险区）
    ax.fill_between(p[p > 0.7], 0, 100, color=DOWN, alpha=0.10, label="满仓危险区")

    ax.set_xlabel("胜率 p", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("最优下注比例 f* (%)", fontsize=11, color=TEXT_SECONDARY)
    ax.set_xlim(0, 1)
    ax.set_ylim(-20, 130)
    ax.legend(loc="upper left", fontsize=10, frameon=False)
    style_axes(ax)

    add_footer(fig, SLUG, 2, TOTAL)
    return save(fig, SLUG, 2)


# ============ 图 3: 香农恶魔 / 再平衡 ============
def fig3_shannon_rebalance():
    fig, axes = new_fig(aspect=(W, H))
    add_title(fig, "香农恶魔：波动本身就能印钱，再平衡就是那根吸管")
    add_subtitle(fig, "两份等额资产，波动越大 + 再平衡频率越高，长期收益越显著超过 buy-and-hold")

    np.random.seed(7)
    days = np.arange(252)  # 一年交易日
    # 两只股票，价格随机游走但均值回归（用正负波动）
    s1 = 10 * np.cumprod(1 + np.random.randn(252) * 0.02)
    s2 = 10 * np.cumprod(1 + np.random.randn(252) * 0.02)

    # 组合 A：buy-and-hold（50/50 不再平衡）
    bh_value = (s1 + s2) / 2 * np.ones_like(s1)

    # 组合 B：每月再平衡到 50/50
    rb_value = np.zeros_like(s1)
    shares1, shares2 = 0.5 / s1[0], 0.5 / s2[0]
    rb_value[0] = 1.0
    last_rebalance = 0
    for i in range(1, len(s1)):
        port_value = shares1 * s1[i] + shares2 * s2[i]
        rb_value[i] = port_value
        # 每月（21 天）再平衡
        if (i - last_rebalance) >= 21:
            target1 = port_value * 0.5 / s1[i]
            target2 = port_value * 0.5 / s2[i]
            shares1 = target1
            shares2 = target2
            last_rebalance = i

    plt.close(fig)
    fig, ax = plt.subplots(figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_PAGE)
    ax.set_facecolor(BG_PAGE)

    ax.plot(days, bh_value, color=TEXT_MUTED, lw=2.0, label="Buy & Hold（不再平衡）")
    ax.plot(days, rb_value, color=ACCENT, lw=2.5, label="每月再平衡 → 50/50")

    # 差异填充
    ax.fill_between(days, bh_value, rb_value,
                     where=(rb_value > bh_value), color=ACCENT_SUBTLE, alpha=0.5,
                     label="再平衡多赚的")

    ax.set_xlabel("交易日（一年）", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("组合价值（起点 1.0）", fontsize=11, color=TEXT_SECONDARY)
    ax.legend(loc="upper left", fontsize=10, frameon=False)
    style_axes(ax)

    fig.suptitle("香农恶魔：波动本身就能印钱，再平衡就是那根吸管",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.97)
    fig.text(0.5, 0.93,
             "两份等额资产，波动越大 + 再平衡频率越高，长期收益越显著超过 buy-and-hold",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")
    fig.subplots_adjust(left=0.07, right=0.97, top=0.88, bottom=0.08)

    add_footer(fig, SLUG, 3, TOTAL)
    return save(fig, SLUG, 3, tight=False)


# ============ 图 4: 全凯利 vs 半凯利财富曲线 ============
def fig4_full_vs_half_kelly():
    fig, ax = new_fig()
    add_title(fig, "半凯利策略：财富速度降 25%，波动风险减 50%")
    add_subtitle(fig, "1000 次重复博弈下：满仓凯利（红线）波动巨大；半凯利（绿线）曲线更平稳")

    np.random.seed(2024)
    trials = 200
    rounds = 50
    p, b = 0.55, 2.0
    f_full = (b * p - (1 - p)) / b
    f_half = f_full / 2

    final_results = {"满仓凯利": [], "半凯利": [], "保守 25% 凯利": []}
    sample_curves = {"满仓凯利": [], "半凯利": [], "保守 25% 凯利": []}

    for _ in range(trials):
        for label, f in [("满仓凯利", f_full), ("半凯利", f_half), ("保守 25% 凯利", f_half / 2)]:
            wealth = [1.0]
            for _ in range(rounds):
                if np.random.rand() < p:
                    wealth.append(wealth[-1] * (1 + f * b))
                else:
                    wealth.append(wealth[-1] * (1 - f))
            final_results[label].append(wealth[-1])
            if len(sample_curves[label]) < 5:
                sample_curves[label].append(wealth)

    # 画多条样本曲线
    for label, color, lw in [("满仓凯利", DOWN, 1.0), ("半凯利", ACCENT, 1.0), ("保守 25% 凯利", TEXT_MUTED, 1.0)]:
        for curve in sample_curves[label]:
            ax.plot(curve, color=color, lw=lw, alpha=0.25)

    # 画中位数
    for label, color, ls in [("满仓凯利", DOWN, "-"), ("半凯利", ACCENT, "-"), ("保守 25% 凯利", TEXT_MUTED, "-")]:
        medians = np.median([c for c in [s for s in sample_curves[label]]], axis=0) if sample_curves[label] else []
        if len(medians) > 0:
            ax.plot(medians, color=color, lw=2.5, ls=ls, label=label)

    ax.axhline(1.0, color=TEXT_MUTED, ls=":", lw=0.8, alpha=0.6)
    ax.set_yscale("log")
    ax.set_xlabel("博弈轮数", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("财富（对数坐标）", fontsize=11, color=TEXT_SECONDARY)
    ax.legend(loc="upper left", fontsize=10, frameon=False)
    style_axes(ax, grid_axis="both")

    fig.text(0.5, 0.04,
             "红线（满凯利）可能中途爆仓；绿线（半凯利）波动收窄，长期复利稳健",
             ha="center", fontsize=11, color=TEXT_SECONDARY, style="italic")

    add_footer(fig, SLUG, 4, TOTAL)
    return save(fig, SLUG, 4)


# ============ 图 5: 532 仓位框架 ============
def fig5_532_framework():
    fig, ax = new_fig()
    add_title(fig, "532 仓位框架：50% 核心底仓 + 30% 弹性波段 + 20% 战备现金")
    add_subtitle(fig, "把数学武器翻译成一套可执行的纪律（本文作者对 5:3:2 比例的口语简称）")

    # 三层饼图（横向 stacked bar 风格更清晰）
    layers = [
        ("50%", "核心底仓", ACCENT, "沪深 300 / 上证 50\n红利低波 ETF\n压舱石，跟大势"),
        ("30%", "弹性波段", UP, "行业景气度高的赛道\n凯利思路控仓\n止损要快、狠、准"),
        ("20%", "战备现金", DOWN, "熊市黑天鹅时刻\n黑铁价的弹药库\n一份没有到期日的看涨期权"),
    ]

    # 横向 stacked bar
    bar_y = 0.5
    bar_h = 0.3
    cum_x = 0.05
    total = 0.95

    for pct_str, name, color, desc in layers:
        pct_num = float(pct_str.rstrip("%")) / 100
        seg_w = total * pct_num
        ax.add_patch(plt.Rectangle((cum_x, bar_y), seg_w, bar_h,
                                    facecolor=color, edgecolor=BG_PAGE, lw=2,
                                    transform=ax.transAxes))
        # 百分比文字
        ax.text(cum_x + seg_w / 2, bar_y + bar_h / 2 + 0.05, pct_str,
                ha="center", va="center", fontsize=22, fontweight="bold",
                color="white", transform=ax.transAxes)
        # 名称
        ax.text(cum_x + seg_w / 2, bar_y + bar_h / 2 - 0.06, name,
                ha="center", va="center", fontsize=13, color="white",
                transform=ax.transAxes)
        cum_x += seg_w

    # 详细说明区
    cum_x = 0.05
    for pct_str, name, color, desc in layers:
        pct_num = float(pct_str.rstrip("%")) / 100
        seg_w = total * pct_num
        # 描述
        ax.text(cum_x + seg_w / 2, bar_y - 0.08, desc,
                ha="center", va="top", fontsize=10, color=TEXT_PRIMARY,
                transform=ax.transAxes)
        cum_x += seg_w

    # 顶部免责说明
    ax.text(0.5, 0.92,
            "⚠️ 免责：'532' 是本文对 5:3:2 仓位分配的口语简称，并非投资学既有术语",
            ha="center", va="top", fontsize=10, color=TEXT_MUTED, style="italic",
            transform=ax.transAxes)

    # 底部心法
    ax.text(0.5, 0.18,
            "三段互为犄角，在牛熊周期里可以动态切换：\n"
            "熊市底部左侧 T 度加仓 → 6:3:1；牛市高位收缩战线 → 现金补回 20%",
            ha="center", va="top", fontsize=11, color=TEXT_SECONDARY,
            transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    add_footer(fig, SLUG, 5, TOTAL)
    return save(fig, SLUG, 5)


if __name__ == "__main__":
    paths = []
    paths.append(fig1_volatility_drag())
    paths.append(fig2_kelly_curve())
    paths.append(fig3_shannon_rebalance())
    paths.append(fig4_full_vs_half_kelly())
    paths.append(fig5_532_framework())
    for p in paths:
        print(f"  ✓ {p}")
    print(f"\nGenerated {len(paths)} images for {SLUG}")
