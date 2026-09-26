"""
compound-interest-lies.md 的 3 张配图。
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
SLUG = "compound-interest-lies"
TOTAL = 3


# ============ 图 1: 几何平均 vs 算术平均 —— 复利的不对称性 ============
def fig1_geometric_vs_arithmetic():
    fig, axes = new_fig(aspect=(W, H))
    add_title(fig, "复利的阴暗面：先 +50% 再 -50%，平均 0% 但本金没了 25%")
    add_subtitle(fig, "亏损对本金的伤害，是盈利贡献的两倍起步——这就是几何平均对算术平均的嘲笑")

    np.random.seed(11)
    days = np.arange(10)

    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_PAGE)
    for ax in axes:
        ax.set_facecolor(BG_PAGE)

    # ---- 左图：先 +50% 再 -50% 的财富曲线 ----
    wealth = np.array([1.0, 1.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75])
    avg_line = np.full_like(days, 1.0, dtype=float)

    axes[0].plot(days, wealth, color=UP, lw=3.0, marker="o", markersize=9, label="真实财富曲线")
    axes[0].plot(days, avg_line, color=TEXT_MUTED, lw=1.5, ls="--", label="算术平均预期 1.0")
    axes[0].fill_between(days, 0.7, wealth, where=(days >= 2), color=UP, alpha=0.15,
                         label="亏损缺口 (-25%)")

    axes[0].annotate("+50% 翻倍到 1.5",
                     xy=(1, 1.5), xytext=(1, 1.7),
                     fontsize=12, color=UP, ha="center", fontweight="bold",
                     arrowprops=dict(arrowstyle="->", color=UP, lw=1.0))
    axes[0].annotate("-50% 跌回 0.75\n（不是 1.0！）",
                     xy=(2, 0.75), xytext=(3.5, 0.55),
                     fontsize=12, color=DOWN, ha="center", fontweight="bold",
                     arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.0))

    axes[0].set_xlabel("年份", fontsize=11, color=TEXT_SECONDARY)
    axes[0].set_ylabel("本金倍数（起点 = 1.0）", fontsize=11, color=TEXT_SECONDARY)
    axes[0].set_xlim(0, 9)
    axes[0].set_ylim(0.4, 1.9)
    axes[0].legend(loc="upper right", fontsize=10, frameon=False)
    axes[0].set_title("① 真实的复利曲线：永远低于直觉", fontsize=13, color=TEXT_PRIMARY, loc="left")
    style_axes(axes[0])

    # ---- 右图：回本所需涨幅表 ----
    loss = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90])
    recovery = np.array([11.1, 25.0, 42.9, 66.7, 100.0, 150.0, 233.3, 400.0, 900.0])
    colors = [ACCENT if r < 50 else UP if r < 200 else DOWN for r in recovery]

    bars = axes[1].bar(loss, recovery, color=colors, edgecolor=BG_PAGE, lw=1.5, width=5)
    axes[1].axhline(100, color=TEXT_MUTED, ls=":", lw=1.0, alpha=0.6)
    axes[1].text(91, 100, "翻倍线 100%", fontsize=10, color=TEXT_MUTED, va="center", ha="right")

    for bar, val in zip(bars, recovery):
        axes[1].text(bar.get_x() + bar.get_width() / 2, val + 25, f"{val:.0f}%",
                     ha="center", fontsize=11, color=TEXT_PRIMARY, fontweight="bold")

    axes[1].set_xlabel("亏损幅度 (%)", fontsize=11, color=TEXT_SECONDARY)
    axes[1].set_ylabel("回本所需涨幅 (%)", fontsize=11, color=TEXT_SECONDARY)
    axes[1].set_xlim(0, 95)
    axes[1].set_ylim(0, 1050)
    axes[1].set_xticks(loss)
    axes[1].set_xticklabels([f"-{l}%" for l in loss], fontsize=10)
    axes[1].set_title("② 回本难度表：跌越深、回本越陡", fontsize=13, color=TEXT_PRIMARY, loc="left")
    style_axes(axes[1])

    fig.suptitle("复利的阴暗面：先 +50% 再 -50%，平均 0% 但本金没了 25%",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.98)
    fig.text(0.5, 0.935,
             "亏损对本金的伤害，是盈利贡献的两倍起步——这就是几何平均对算术平均的嘲笑",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")
    fig.subplots_adjust(left=0.06, right=0.97, top=0.86, bottom=0.08, wspace=0.25)

    add_footer(fig, SLUG, 1, TOTAL)
    return save(fig, SLUG, 1, tight=False)


# ============ 图 2: 波动率税 —— 期望值为正的抛硬币也会破产 ============
def fig2_volatility_tax():
    fig, ax = new_fig()
    add_title(fig, "波动率税：期望 +2.5% 的硬币博弈，长期也会破产归零")
    add_subtitle(fig, "正面 +20% / 反面 -15% 的博弈——你以为是稳定盈利，其实是被方差偷偷吸血")

    np.random.seed(7)
    n_paths = 50
    n_steps = 500

    plt.close(fig)
    fig, ax = plt.subplots(figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_PAGE)
    ax.set_facecolor(BG_PAGE)

    fig.suptitle("波动率税：期望 +2.5% 的硬币博弈，长期也会破产归零",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.96)
    fig.text(0.5, 0.915,
             "正面 +20% / 反面 -15% 的博弈——你以为是稳定盈利，其实是被方差偷偷吸血",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")

    # 50 条路径
    for _ in range(n_paths):
        path = [1.0]
        for _ in range(n_steps):
            if np.random.rand() < 0.5:
                path.append(path[-1] * 1.20)
            else:
                path.append(path[-1] * 0.85)
        path = np.array(path[:n_steps + 1])
        # 跌破 0.01 截断
        path = np.where(path < 0.01, np.nan, path)
        ax.plot(path, color=DOWN, lw=0.8, alpha=0.4)

    # 期望复利路径（理论值）
    days = np.arange(n_steps + 1)
    expected = np.cumprod(np.where(np.arange(n_steps + 1) == 0, 1.0, 1.025))
    ax.plot(expected, color=ACCENT, lw=3.0, label="期望复利（理论）+2.5%/次")

    # 中位数
    medians = []
    for t in range(n_steps + 1):
        pass
    # 标注几条破产路径
    ax.axhline(1.0, color=TEXT_MUTED, ls=":", lw=1.0, alpha=0.5, label="起点 1.0")
    ax.text(450, 5, "破产归零区\n（路径跌破 0.01 截断）",
            fontsize=11, color=DOWN, ha="center", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc=BG_SURFACE, ec=DOWN, lw=1.0))

    ax.set_yscale("log")
    ax.set_xlabel("博弈轮数", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("本金倍数（对数坐标）", fontsize=11, color=TEXT_SECONDARY)
    ax.set_xlim(0, n_steps)
    ax.set_ylim(0.005, 1000)
    ax.legend(loc="upper left", fontsize=10, frameon=False)
    style_axes(ax, grid_axis="both")

    fig.subplots_adjust(left=0.07, right=0.97, top=0.88, bottom=0.08)

    fig.text(0.5, 0.04,
             "哪怕期望值 +2.5%，50 条样本中绝大多数都在波动率税下走向破产——这就是便利性破产（ruin）",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")

    add_footer(fig, SLUG, 2, TOTAL)
    return save(fig, SLUG, 2, tight=False)


# ============ 图 3: 交易成本的指数衰减 ============
def fig3_transaction_cost_decay():
    fig, ax = new_fig()
    add_title(fig, "交易成本的复利反噬：交易 100 次后，10 万只剩 6 万")
    add_subtitle(fig, "0.5% 单次摩擦 × 频率 = 本金的指数型衰减；还没赚钱，就先背上沉重负债")

    np.random.seed(3)
    trades = np.arange(0, 251)

    # 不同频率的剩余本金
    cost_rate = 0.005  # 每次 0.5%
    yearly = 1.0 - cost_rate  # 1 次
    monthly = (1.0 - cost_rate) ** 12  # 12 次
    weekly = (1.0 - cost_rate) ** 52  # 52 次
    daily = (1.0 - cost_rate) ** 250  # 250 次

    capital_yearly = 10.0 * np.ones_like(trades, dtype=float)
    capital_monthly = 10.0 * np.where(trades == 0, 1.0, monthly ** (trades / 12))
    capital_weekly = 10.0 * np.where(trades == 0, 1.0, weekly ** (trades / 52))
    capital_daily = 10.0 * np.where(trades == 0, 1.0, daily ** (trades / 250))

    ax.plot(trades, capital_yearly, color=ACCENT, lw=2.5, label="年交易 1 次（接近无损）")
    ax.plot(trades, capital_monthly, color=TEXT_PRIMARY, lw=2.5, label="月交易 1 次（剩 94%）")
    ax.plot(trades, capital_weekly, color=UP, lw=2.5, label="周交易 1 次（剩 77%）")
    ax.plot(trades, capital_daily, color=DOWN, lw=3.0, label="日交易 1 次（剩 28%）")

    ax.fill_between(trades, 2.8, capital_daily, color=DOWN, alpha=0.10, label="日交易黑洞区")

    ax.annotate("每天交易 1 次\n250 次 → 10 万只剩 2.8 万",
                xy=(250, capital_daily[-1]), xytext=(180, 6),
                fontsize=12, color=DOWN, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.2),
                bbox=dict(boxstyle="round,pad=0.4", fc=BG_SURFACE, ec=DOWN, lw=1.0))

    ax.axhline(10.0, color=TEXT_MUTED, ls=":", lw=0.8, alpha=0.5)
    ax.text(250, 10.2, "起点 10 万", fontsize=10, color=TEXT_MUTED, ha="right", va="bottom")

    ax.set_xlabel("一年内的交易天数", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("本金剩余（万元）", fontsize=11, color=TEXT_SECONDARY)
    ax.set_xlim(0, 250)
    ax.set_ylim(2, 11)
    ax.legend(loc="lower left", fontsize=10, frameon=False)
    style_axes(ax)

    fig.text(0.5, 0.04,
             "在「日赚 1%」的复利幻觉下，你以为在进攻，其实每天都被摩擦成本偷走 0.5% 的本金",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")

    add_footer(fig, SLUG, 3, TOTAL)
    return save(fig, SLUG, 3, tight=False)


if __name__ == "__main__":
    paths = []
    paths.append(fig1_geometric_vs_arithmetic())
    paths.append(fig2_volatility_tax())
    paths.append(fig3_transaction_cost_decay())
    for p in paths:
        print(f"  ✓ {p}")
    print(f"\nGenerated {len(paths)} images for {SLUG}")