"""
weekly-k-line-vs-daily.md 的 4 张配图。
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
SLUG = "weekly-k-line-vs-daily"
TOTAL = 4


# ============ 图 1: 日线 vs 周线 vs 月线 同段行情对比 ============
def fig1_three_timeframes():
    fig, axes = new_fig(aspect=(W, H))
    add_title(fig, "同一段行情：日线噪音 vs 周线骨架 vs 月线迟缓")
    add_subtitle(fig, "K 线本质上是对交易数据的有损压缩，时间容器越短 → 噪音越多")

    np.random.seed(31)
    daily_days = np.arange(120)
    base_price = 10 + np.cumsum(np.random.randn(120) * 0.3)

    # 日线：每天一根 K 线
    daily = base_price + np.random.randn(120) * 0.4

    # 周线：每 5 天聚合
    weekly = np.array([np.mean(base_price[i:i + 5]) for i in range(0, 120, 5)])
    weekly_days = np.arange(0, 120, 5)

    # 月线：每 20 天聚合
    monthly = np.array([np.mean(base_price[i:i + 20]) for i in range(0, 120, 20)])
    monthly_days = np.arange(0, 120, 20)

    plt.close(fig)
    fig, axes = plt.subplots(3, 1, figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_PAGE)
    for ax in axes:
        ax.set_facecolor(BG_PAGE)

    # 日线
    axes[0].plot(daily_days, daily, color=UP, lw=1.0, alpha=0.7)
    axes[0].set_title("日 K 线（120 根）— 噪音最多，散户被绞杀的战场", fontsize=13, color=DOWN, pad=8, loc="left")

    # 周线
    axes[1].plot(weekly_days, weekly, color=UP, lw=2.0)
    axes[1].set_title("周 K 线（24 根）— 过滤 4/5 的噪音，趋势骨架清晰可见", fontsize=13, color=ACCENT, pad=8, loc="left")

    # 月线
    axes[2].plot(monthly_days, monthly, color=UP, lw=2.5)
    axes[2].set_title("月 K 线（6 根）— 最稳但最迟，散户的船扛不住航空母舰的航程", fontsize=13, color=TEXT_MUTED, pad=8, loc="left")

    for ax in axes:
        ax.set_xlim(0, 119)
        ax.set_ylabel("价格", fontsize=10, color=TEXT_SECONDARY)
        style_axes(ax)

    axes[-1].set_xlabel("时间（120 个交易日）", fontsize=11, color=TEXT_SECONDARY)

    fig.suptitle("同一段行情：日线噪音 vs 周线骨架 vs 月线迟缓",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.97)
    fig.text(0.5, 0.93,
             "K 线本质上是对交易数据的有损压缩，时间容器越短 → 噪音越多",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")
    fig.subplots_adjust(left=0.06, right=0.97, top=0.88, bottom=0.06, hspace=0.45)

    add_footer(fig, SLUG, 1, TOTAL)
    return save(fig, SLUG, 1, tight=False)


# ============ 图 2: 流动性猎杀示意 ============
def fig2_liquidity_hunt():
    fig, ax = new_fig()
    add_title(fig, "日线的流动性猎杀：主力借假跌破吸筹，你交出带血的筹码")
    add_subtitle(fig, "经典双底陷阱：散户止损位挂在支撑下沿 → 主力砸穿 → 散户割肉 → 主力反向拉升")

    np.random.seed(45)
    days = np.arange(60)

    # 构造假双底形态
    price = np.zeros(60)
    # 阶段 1：第一次下探（20-30）
    price[0:20] = 10 + np.random.randn(20) * 0.3
    price[20:25] = 10 - np.linspace(0, 1.5, 5) + np.random.randn(5) * 0.2  # 下到 8.5
    price[25:30] = 8.5 + np.linspace(0, 1.2, 5) + np.random.randn(5) * 0.2  # 反弹

    # 阶段 2：第二次下探（30-50）—— 假跌破
    price[30:40] = 10 + np.random.randn(10) * 0.2
    price[40:45] = 9.7 - np.linspace(0, 1.0, 5) + np.random.randn(5) * 0.15  # 下到 8.0（跌破 8.5 支撑）
    price[45:50] = 8.0 + np.linspace(0, 0.5, 5) + np.random.randn(5) * 0.15

    # 阶段 3：拉升
    price[50:60] = 8.5 + np.linspace(0, 3, 10) + np.random.randn(10) * 0.3

    ax.plot(days, price, color=UP, lw=1.6, label="价格")

    # 支撑线
    support = 8.5
    ax.axhline(support, color=TEXT_MUTED, ls="--", lw=1.0, label="散户挂的支撑位 8.5")
    ax.axhline(8.0, color=DOWN, ls=":", lw=1.0, alpha=0.7, label="假跌破 8.0")

    # 标注
    ax.annotate("散户止损\n集中挂在这里", xy=(43, 8.0), xytext=(20, 6.5),
                fontsize=11, color=DOWN, ha="center",
                arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.2))
    ax.annotate("主力砸穿 → 触发止损\n→ 散户割肉 → 主力接盘",
                xy=(43, 8.0), xytext=(45, 5.5),
                fontsize=10, color=TEXT_PRIMARY, ha="center",
                arrowprops=dict(arrowstyle="->", color=TEXT_PRIMARY, lw=1.0))
    ax.annotate("主力反向拉升\n散户已下车",
                xy=(56, price[56]), xytext=(55, 12.5),
                fontsize=11, color=UP, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=UP, lw=1.2))

    # 散户标记
    ax.scatter([22, 42], [8.5, 8.0], color=DOWN, s=80, zorder=5, label="散户止损点", alpha=0.7, marker="x")

    ax.set_xlabel("交易日", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("价格", fontsize=11, color=TEXT_SECONDARY)
    ax.set_xlim(0, 60)
    ax.set_ylim(5.5, 14)
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    style_axes(ax)

    add_footer(fig, SLUG, 2, TOTAL)
    return save(fig, SLUG, 2)


# ============ 图 3: 月线深水困境 ============
def fig3_monthly_pain():
    fig, ax = new_fig()
    add_title(fig, "月线深水困境：止损空间 20%-30%，散户本金扛不住")
    add_subtitle(fig, "按月线建仓 → 止损必然设在月线低点 → 满仓一次回撤就击穿账户承受底线")

    # 单根月 K 线（突破大阳线）示意
    fig_height = 0.4  # 振幅占 Y 轴比例
    open_p, close_p, high_p, low_p = 8.5, 11.5, 12.0, 8.0
    body_bottom = min(open_p, close_p)
    body_top = max(open_p, close_p)

    # 画 K 线
    ax.add_patch(plt.Rectangle((0.45, body_bottom), 0.10, body_top - body_bottom,
                                 facecolor=UP, edgecolor=UP))
    ax.plot([0.50, 0.50], [low_p, high_p], color=UP, lw=1.5)

    # 止损线
    stop_loss = low_p
    ax.axhline(stop_loss, color=DOWN, ls="--", lw=1.5, label=f"月线止损位 = {low_p} 元")

    # 标注
    ax.annotate("月线大阳线突破\n上下振幅 40%（8.0~12.0）",
                xy=(0.50, 10.0), xytext=(0.65, 11.0),
                fontsize=11, color=TEXT_PRIMARY, ha="center",
                arrowprops=dict(arrowstyle="->", color=TEXT_PRIMARY, lw=1.0))

    ax.annotate("满仓买入 → 必须承担\n至少 20%-30% 的浮亏",
                xy=(0.50, 9.0), xytext=(0.20, 8.0),
                fontsize=11, color=DOWN, fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.2))

    ax.text(0.20, 6.5, "本金 10 万 → 单笔止损 2 万起\n（按 1% 风险规则需要 100 万本金）",
            fontsize=11, color=TEXT_SECONDARY, ha="center",
            bbox=dict(boxstyle="round,pad=0.5", fc=ACCENT_SUBTLE, ec=ACCENT, lw=1.0))

    ax.text(0.5, 4.5, "小舢板无法在月线的深水港里航行",
            fontsize=14, color=TEXT_MUTED, ha="center", style="italic")

    ax.set_xlim(0, 1)
    ax.set_ylim(4, 13)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("一根月 K 线（振幅 40%）", fontsize=11, color=TEXT_SECONDARY)
    for spine in ax.spines.values():
        spine.set_color(BORDER)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    add_footer(fig, SLUG, 3, TOTAL)
    return save(fig, SLUG, 3)


# ============ 图 4: 月定势 / 周定眼 / 日定点 ============
def fig4_three_layer_system():
    fig, ax = new_fig()
    add_title(fig, "月定势 / 周定眼 / 日定点：三维一体的多周期共振系统")
    add_subtitle(fig, "大周期定方向、中周期找信号、小周期定入场")

    layers = [
        (0.85, "月 定 势", "看大势  ·  20 月均线定方向\n判断春夏秋冬", ACCENT, ACCENT),
        (0.55, "周 定 眼", "找信号  ·  周线平台突破 / 周线均线支撑\n狙击镜", ACCENT_SUBTLE, TEXT_PRIMARY),
        (0.25, "日 定 点", "定入场  ·  日线缩量回踩 / 微型旗形\n精准打击点", ACCENT_SUBTLE, UP),
    ]

    for y, label, desc, fc, ec in layers:
        box = plt.Rectangle((0.10, y), 0.80, 0.18,
                             facecolor=fc, edgecolor=ec, lw=2.5,
                             transform=ax.transAxes)
        ax.add_patch(box)
        ax.text(0.50, y + 0.13, label, ha="center", va="center",
                fontsize=18, fontweight="bold", color=ec, transform=ax.transAxes)
        ax.text(0.50, y + 0.05, desc, ha="center", va="center",
                fontsize=11, color=TEXT_PRIMARY, transform=ax.transAxes)

    # 向下箭头连接
    for y_top in [0.85, 0.55]:
        ax.annotate("", xy=(0.5, y_top - 0.02), xytext=(0.5, y_top - 0.17),
                    arrowprops=dict(arrowstyle="->", color=TEXT_PRIMARY, lw=2.5),
                    transform=ax.transAxes)

    # 底部说明
    ax.text(0.5, 0.05,
            "用日线小止损博取周线大波段 → 多周期共振的精髓",
            ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic", transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    add_footer(fig, SLUG, 4, TOTAL)
    return save(fig, SLUG, 4)


if __name__ == "__main__":
    paths = []
    paths.append(fig1_three_timeframes())
    paths.append(fig2_liquidity_hunt())
    paths.append(fig3_monthly_pain())
    paths.append(fig4_three_layer_system())
    for p in paths:
        print(f"  ✓ {p}")
    print(f"\nGenerated {len(paths)} images for {SLUG}")
