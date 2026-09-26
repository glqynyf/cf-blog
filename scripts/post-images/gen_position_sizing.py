"""
position-sizing-matters-more.md 的 3 张配图。
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
SLUG = "position-sizing-matters-more"
TOTAL = 3


# ============ 图 1: 凯利公式曲线 + 半凯利/四分之一凯利 ============
def fig1_kelly_curve():
    fig, ax = new_fig()
    add_title(fig, "凯利公式 f* = (b·p − q) / b：半凯利和四分之一凯利才是普通人能用的")
    add_subtitle(fig, "胜赔比 b = 2：满仓凯利 → 财富速度最快但破产风险最大；半凯利 → 牺牲速度换安全")

    b = 2.0
    p = np.linspace(0, 1, 400)
    f_full = (b * p - (1 - p)) / b
    f_half = f_full / 2
    f_quarter = f_full / 4

    ax.plot(p, f_full * 100, color=DOWN, lw=2.5, label="满仓凯利 f*（破产风险最大）")
    ax.plot(p, f_half * 100, color=ACCENT, lw=2.8, label="半凯利 f*/2（实战首选）")
    ax.plot(p, f_quarter * 100, color=TEXT_SECONDARY, lw=2.2, ls="--",
            label="四分之一凯利 f*/4（保守起步）")

    ax.axhline(0, color=TEXT_MUTED, lw=1.0)
    ax.axhline(100, color=DOWN, ls=":", lw=1.2, alpha=0.7, label="满仓 100%")

    # 临界点
    critical = 1 / (b + 1)
    ax.axvline(critical, color=DOWN, ls=":", lw=1.0, alpha=0.6)
    ax.text(critical, 110, f"  p = {critical:.2f}",
            fontsize=10, color=DOWN, va="bottom", ha="left")

    # 阴影区
    ax.fill_between(p[p > 0.7], 0, 100, color=DOWN, alpha=0.10, label="满仓危险区")

    # 关键场景标注
    ax.scatter([0.6], [20], color=ACCENT, s=150, zorder=10, edgecolor=TEXT_PRIMARY, lw=2)
    ax.annotate("实战常用点\np=60%, b=1 → f*=20%",
                xy=(0.6, 20), xytext=(0.7, 70),
                fontsize=11, color=ACCENT, ha="left", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.2),
                bbox=dict(boxstyle="round,pad=0.3", fc=BG_SURFACE, ec=ACCENT, lw=1.0))

    ax.set_xlabel("胜率 p", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("最优下注比例 (%)", fontsize=11, color=TEXT_SECONDARY)
    ax.set_xlim(0, 1)
    ax.set_ylim(-20, 130)
    ax.legend(loc="upper left", fontsize=10, frameon=False)
    style_axes(ax)

    fig.text(0.5, 0.04,
             "凯利公式的核心价值：在贪婪和破产之间用数学画出一条绝对安全的红线",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")

    add_footer(fig, SLUG, 1, TOTAL)
    return save(fig, SLUG, 1)


# ============ 图 2: 2% 法则 + 6% 法则 ============
def fig2_two_six_rule():
    fig, ax = new_fig()
    add_title(fig, "2% 法则 + 6% 法则：把仓位管理装进普通人能用的两条铁律")
    add_subtitle(fig, "单笔风险 ≤ 2%（防致命伤）+ 月度累计 ≤ 6%（防连续伤害），合起来就是强制断路器")

    # 四张卡片
    cards = [
        ("① 账户总额", "100,000 元", ACCENT, "你的本金上限\n所有仓位管理的起点", 0.10, 0.55),
        ("② 单笔最大风险", "≤ 2,000 元 (2%)", UP, "跌破止损时\n你最多能亏这么多", 0.38, 0.55),
        ("③ 月度最大累计", "≤ 6,000 元 (6%)", DOWN, "触发即当天停手\n直到下个月才允许再战", 0.66, 0.55),
    ]

    card_w = 0.24
    card_h = 0.28
    for title, value, color, desc, x, y in cards:
        # 卡片背景
        ax.add_patch(plt.Rectangle((x, y - card_h), card_w, card_h,
                                    facecolor=BG_SURFACE, edgecolor=color, lw=2.0,
                                    transform=ax.transAxes))
        # 标题条
        ax.add_patch(plt.Rectangle((x, y - card_h), card_w, 0.06,
                                    facecolor=color, edgecolor=BG_PAGE, lw=0,
                                    transform=ax.transAxes))
        # 标题
        ax.text(x + card_w / 2, y - card_h + 0.03, title,
                transform=ax.transAxes, ha="center", va="center",
                fontsize=12, color="white", fontweight="bold")
        # 数值
        ax.text(x + card_w / 2, y - card_h + 0.13, value,
                transform=ax.transAxes, ha="center", va="center",
                fontsize=14, color=color, fontweight="bold")
        # 说明
        ax.text(x + card_w / 2, y - card_h + 0.21, desc,
                transform=ax.transAxes, ha="center", va="center",
                fontsize=10, color=TEXT_PRIMARY)

    # 底部强调
    ax.text(0.5, 0.16,
            "2% 法则 = 防「单次致命伤」  ·  6% 法则 = 防「连续伤害」",
            transform=ax.transAxes, ha="center", fontsize=14,
            color=TEXT_PRIMARY, fontweight="bold")
    ax.text(0.5, 0.08,
            "触发 6% 即当天无条件停止开新仓 —— 保护剩下 94% 的元气",
            transform=ax.transAxes, ha="center", fontsize=12,
            color=DOWN, fontweight="bold", style="italic")

    # 实操示例 - 放在卡片上方
    ax.text(0.5, 0.20,
            "实操示例：账户 10 万 + 止损 5 元/股 → 最大可买 400 股（投入 2 万）",
            transform=ax.transAxes, ha="center", fontsize=11,
            color=TEXT_SECONDARY, style="italic")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    add_footer(fig, SLUG, 2, TOTAL)
    return save(fig, SLUG, 2)


# ============ 图 3: 核心-卫星策略 + 动态再平衡 ============
def fig3_core_satellite_rebalance():
    fig, axes = new_fig(aspect=(W, H))
    add_title(fig, "核心-卫星 + 动态再平衡 = 自动化的反脆弱系统")
    add_subtitle(fig, "70%-80% 核心压舱石 + 20%-30% 卫星博收益；再平衡 = 机械式的「低买高卖」")

    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_PAGE)
    for ax in axes:
        ax.set_facecolor(BG_PAGE)

    fig.suptitle("核心-卫星 + 动态再平衡 = 自动化的反脆弱系统",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.985)
    fig.text(0.5, 0.94,
             "70%-80% 核心压舱石 + 20%-30% 卫星博收益；再平衡 = 机械式的「低买高卖」",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")

    # ---- 左图：核心-卫星结构（同心圆/分层）----
    ax1 = axes[0]
    from matplotlib.patches import Wedge
    ax1.add_patch(Wedge((0.5, 0.5), 0.42, 0, 360, width=0.18,
                         facecolor=ACCENT, edgecolor=BG_PAGE, lw=2,
                         transform=ax1.transAxes))
    ax1.add_patch(Wedge((0.5, 0.5), 0.22, 0, 360, width=0.18,
                         facecolor=UP, edgecolor=BG_PAGE, lw=2,
                         transform=ax1.transAxes))
    # 中心标签
    ax1.text(0.5, 0.5, "100 万\n总资金", transform=ax1.transAxes,
             ha="center", va="center", fontsize=13, fontweight="bold",
             color=TEXT_PRIMARY)

    # 外圈 - 核心
    ax1.text(0.5, 0.83, "核心 75%", transform=ax1.transAxes,
             ha="center", va="center", fontsize=13, fontweight="bold",
             color="white")
    ax1.text(0.5, 0.73, "沪深300 + 高股息\n国债 + 货币基金", transform=ax1.transAxes,
             ha="center", va="center", fontsize=10, color="white")

    # 内圈 - 卫星
    ax1.text(0.5, 0.30, "卫星 25%", transform=ax1.transAxes,
             ha="center", va="center", fontsize=13, fontweight="bold",
             color="white")
    ax1.text(0.5, 0.20, "高弹性个股\n行业主题基金", transform=ax1.transAxes,
             ha="center", va="center", fontsize=10, color="white")

    # 下方说明
    ax1.text(0.5, 0.05,
             "卫星暴击 -50% → 整体仅伤 12.5%",
             transform=ax1.transAxes, ha="center", va="bottom",
             fontsize=11, color=TEXT_SECONDARY, style="italic")

    ax1.set_title("① 核心-卫星：化解「既想要安全、又渴望暴利」的人性冲突",
                  fontsize=12, color=TEXT_PRIMARY, loc="left", pad=10)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_xticks([])
    ax1.set_yticks([])
    for spine in ax1.spines.values():
        spine.set_visible(False)

    # ---- 右图：动态再平衡 50:50 示意 ----
    ax2 = axes[1]
    quarters = ["起点", "Q1\n指数涨", "再平衡", "Q2\n指数跌", "再平衡"]
    index_vals = [50, 75, 50, 30, 50]
    cash_vals = [50, 50, 75, 70, 50]

    x = np.arange(len(quarters))
    width = 0.35
    bars1 = ax2.bar(x - width / 2, index_vals, width, color=UP, label="指数 (万元)")
    bars2 = ax2.bar(x + width / 2, cash_vals, width, color=ACCENT, label="现金 (万元)")

    for i, (b1, b2) in enumerate(zip(bars1, bars2)):
        ax2.text(b1.get_x() + b1.get_width() / 2, b1.get_height() + 1,
                 f"{index_vals[i]}", ha="center", fontsize=10, color=UP, fontweight="bold")
        ax2.text(b2.get_x() + b2.get_width() / 2, b2.get_height() + 1,
                 f"{cash_vals[i]}", ha="center", fontsize=10, color=ACCENT, fontweight="bold")

    # 标注关键动作
    ax2.annotate("高位自动减仓\n卖出 25 万指数",
                 xy=(2, 75), xytext=(2.0, 95),
                 ha="center", fontsize=10, color=UP, fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color=UP, lw=1.0))
    ax2.annotate("底部自动加仓\n买入 20 万指数",
                 xy=(4, 50), xytext=(4.0, 95),
                 ha="center", fontsize=10, color=ACCENT, fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.0))

    ax2.set_title("② 50:50 再平衡：机械式的「低买高卖」",
                  fontsize=12, color=TEXT_PRIMARY, loc="left", pad=10)
    ax2.set_xticks(x)
    ax2.set_xticklabels(quarters, fontsize=9)
    ax2.set_ylabel("金额（万元）", fontsize=10, color=TEXT_SECONDARY)
    ax2.set_ylim(0, 110)
    ax2.legend(loc="upper right", fontsize=9, frameon=False)
    style_axes(ax2, grid_axis="y")

    fig.subplots_adjust(left=0.04, right=0.97, top=0.88, bottom=0.06, wspace=0.25)

    add_footer(fig, SLUG, 3, TOTAL)
    return save(fig, SLUG, 3, tight=False)


if __name__ == "__main__":
    paths = []
    paths.append(fig1_kelly_curve())
    paths.append(fig2_two_six_rule())
    paths.append(fig3_core_satellite_rebalance())
    for p in paths:
        print(f"  ✓ {p}")
    print(f"\nGenerated {len(paths)} images for {SLUG}")