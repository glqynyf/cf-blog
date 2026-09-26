"""
why-retail-always-lose.md 的 3 张配图。
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
SLUG = "why-retail-always-lose"
TOTAL = 3


# ============ 图 1: 席勒过度波动之谜 ============
def fig1_excess_volatility():
    fig, ax = new_fig()
    add_title(fig, "席勒的「过度波动之谜」：真实股价围绕理性价格做数倍剧烈震荡")
    add_subtitle(fig, "Shiller (1981) 用 S&P 综合指数 1871-1979 年数据反证——EMH 在百年尺度被打脸")

    np.random.seed(1981)
    years = np.arange(108)  # 108 年

    # 真实股利/理性价格（平滑曲线）
    rational_price = 100 + 30 * np.sin(years / 15) + years * 1.5 + np.random.randn(108) * 2

    # 真实股价（在理性基础上剧烈波动，倍数关系）
    actual_price = rational_price + 35 * np.sin(years / 5) + 25 * np.cos(years / 8) + np.random.randn(108) * 3

    # 画线
    ax.plot(years, actual_price, color=UP, lw=1.6, label="真实股价", alpha=0.85)
    ax.plot(years, rational_price, color=ACCENT, lw=2.5, ls="--", label="理性价格（股利折现算出）")

    # 标注差异区域
    ax.fill_between(years, rational_price, actual_price,
                     where=(actual_price > rational_price), color=UP, alpha=0.15, label="情绪过热（价 > 理）")
    ax.fill_between(years, rational_price, actual_price,
                     where=(actual_price < rational_price), color=ACCENT, alpha=0.15, label="情绪过冷（价 < 理）")

    # 关键节点标注
    ax.annotate("理性价格曲线\n（股利决定）",
                xy=(80, rational_price[80]), xytext=(95, 70),
                fontsize=11, color=ACCENT, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.2))
    ax.annotate("真实股价\n（市场情绪驱动）",
                xy=(85, actual_price[85]), xytext=(95, 220),
                fontsize=11, color=UP, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=UP, lw=1.2))

    ax.set_xlabel("年份（1871 - 1979）", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("价格（指数化）", fontsize=11, color=TEXT_SECONDARY)
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 250)
    ax.legend(loc="upper left", fontsize=10, frameon=False)
    style_axes(ax)

    # 底部注解
    fig.text(0.5, 0.04,
            "真实股价方差是理性价格的数倍  →  这种「过度波动」用股利变化根本解释不了",
            transform=fig.transFigure, ha="center", fontsize=11,
            color=TEXT_SECONDARY, style="italic")

    add_footer(fig, SLUG, 1, TOTAL)
    return save(fig, SLUG, 1)


# ============ 图 2: 杏仁核劫持示意图 ============
def fig2_amygdala_hijack():
    fig, ax = new_fig()
    add_title(fig, "杏仁核劫持：你以为的冷静决策，其实是 20 万年前的大脑在劫持")
    add_subtitle(fig, "屏幕下跌 3% 与草丛里跳出剑齿虎——在你杏仁核眼里，是同一个等级的危险信号")

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_facecolor(BG_PAGE)

    # 左侧：远古祖先（刺激源）
    ancestor = plt.Circle((2, 5.2), 0.85, facecolor=TEXT_MUTED, edgecolor=TEXT_PRIMARY, lw=2,
                          alpha=0.3)
    ax.add_patch(ancestor)
    ax.text(2, 5.4, "远古祖先", ha="center", va="center", fontsize=12,
            color=TEXT_PRIMARY, fontweight="bold")
    ax.text(2, 4.85, "20 万年前", ha="center", va="center", fontsize=10,
            color=TEXT_SECONDARY)
    ax.text(2, 3.8, "草丛窸窣声响\n→ 立刻拔腿就跑",
            ha="center", va="top", fontsize=10, color=TEXT_MUTED, style="italic")

    # 中间：箭头
    ax.annotate("", xy=(4.7, 5.2), xytext=(2.9, 5.2),
                arrowprops=dict(arrowstyle="->", color=TEXT_PRIMARY, lw=2.5))
    ax.text(3.8, 5.6, "20 万年", ha="center", fontsize=10, color=TEXT_MUTED, fontweight="bold")
    ax.text(3.8, 4.85, "时光隧道", ha="center", fontsize=10, color=TEXT_MUTED)

    # 右侧：杏仁核（情绪雷达）
    amygdala_outer = plt.Circle((7, 5.2), 1.5, facecolor=BG_SURFACE,
                                  edgecolor=DOWN, lw=2.5, alpha=0.95)
    ax.add_patch(amygdala_outer)
    # 杏仁核 标题
    ax.text(7, 5.95, "杏仁核", ha="center", va="center", fontsize=13,
            color=DOWN, fontweight="bold")
    ax.text(7, 5.65, "（情绪雷达）", ha="center", va="center", fontsize=9,
            color=DOWN)

    # 前额叶（理性）- 小圆放在杏仁核内偏下方
    prefrontal = plt.Circle((7, 4.3), 0.55, facecolor=UP,
                             edgecolor="white", lw=2, alpha=0.85)
    ax.add_patch(prefrontal)
    ax.text(7, 4.3, "前额叶", ha="center", va="center", fontsize=9,
            color="white", fontweight="bold")
    # 箭头指向劫持
    ax.annotate("", xy=(6.6, 4.1), xytext=(6.2, 3.5),
                arrowprops=dict(arrowstyle="->", color=UP, lw=2.0))
    ax.text(6.0, 3.2, "劫持！", ha="center", fontsize=10, color=UP,
            fontweight="bold")

    # 杏仁核说明（放在左下，避免和前额叶重叠）
    ax.text(7, 6.4, "毫秒级响应 + 强制接管身体",
            ha="center", va="center", fontsize=9, color=TEXT_MUTED,
            style="italic")

    # 输出：下单按键（右侧）
    reaction_box = plt.Rectangle((8.5, 1.0), 1.4, 1.0,
                                  facecolor=BG_SURFACE, edgecolor=UP, lw=2)
    ax.add_patch(reaction_box)
    ax.text(9.2, 1.5, "下单按键", ha="center", va="center", fontsize=12,
            color=UP, fontweight="bold")

    # 杏仁核 → 下单按键 的箭头
    ax.annotate("", xy=(8.7, 2.0), xytext=(7.8, 4.5),
                arrowprops=dict(arrowstyle="->", color=DOWN, lw=2.5,
                                 connectionstyle="arc3,rad=0.2"))

    # "立即行动" 文字（水平放在箭头旁）
    ax.text(8.85, 3.3, "立即行动", ha="left", va="center",
            fontsize=11, color=DOWN, fontweight="bold")

    # 底部说明
    ax.text(5, 0.4,
            "你以为自己是司机，其实你只是副驾驶\n"
            "握方向盘的，是那个住在山洞里的远古猎人",
            ha="center", va="center", fontsize=12, color=TEXT_PRIMARY,
            fontweight="bold")

    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    add_footer(fig, SLUG, 2, TOTAL)
    return save(fig, SLUG, 2)


# ============ 图 3: 前景理论 S 型价值曲线 ============
def fig3_prospect_theory():
    fig, ax = new_fig()
    add_title(fig, "前景理论：损失带来的痛苦是同等收益快乐的 2~2.5 倍")
    add_subtitle(fig, "Kahneman & Tversky (1979) 价值函数：盈利区凹、亏损区凸、损失端更陡——这就是散户被精准收割的物理学基础")

    np.random.seed(99)
    # 横坐标：从 -3000 到 +3000
    x = np.linspace(-3000, 3000, 500)

    alpha = 0.88
    lam = 2.25
    v = np.where(x >= 0, x ** alpha, -lam * (-x) ** alpha)

    ax.plot(x, v, color=UP, lw=3.0)
    ax.scatter([0], [0], s=120, color=TEXT_PRIMARY, zorder=5)

    # 参考线
    ax.axhline(0, color=TEXT_MUTED, lw=0.8, ls=":")
    ax.axvline(0, color=TEXT_MUTED, lw=0.8, ls=":")

    # 标注关键区域
    ax.fill_between(x, v, where=(x < 0), color=UP, alpha=0.10)
    ax.fill_between(x, v, where=(x > 0), color=ACCENT, alpha=0.10)

    # 关键点：+1000 vs -1000
    ax.scatter([1000], [1000 ** alpha], s=140, color=ACCENT, edgecolor="white", lw=2, zorder=5)
    ax.scatter([-1000], [-lam * 1000 ** alpha], s=140, color=UP, edgecolor="white", lw=2, zorder=5)

    # 标注 +1000
    ax.annotate("收益 +1000\n价值 ≈ +1000",
                xy=(1000, 1000 ** alpha), xytext=(1100, 2000),
                fontsize=12, color=ACCENT, ha="left", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", fc=BG_SURFACE, ec=ACCENT, lw=1.0),
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.5))

    # 标注 -1000
    ax.annotate("损失 −1000\n价值 ≈ −2250\n（绝对值更大）",
                xy=(-1000, -lam * 1000 ** alpha), xytext=(-2700, -2300),
                fontsize=12, color=UP, ha="center", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", fc=BG_SURFACE, ec=UP, lw=1.0),
                arrowprops=dict(arrowstyle="->", color=UP, lw=1.5))

    # α 和 λ 标注（在曲线旁）
    ax.text(2400, 800,
            "α ≈ 0.88\n（敏感性递减）",
            fontsize=12, color=ACCENT, ha="left", va="center", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc=BG_SURFACE, ec=ACCENT, lw=1.0))

    ax.text(-2000, -1900,
            "λ ≈ 2.25\n（损失厌恶系数）",
            fontsize=12, color=UP, ha="left", va="center", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc=BG_SURFACE, ec=UP, lw=1.0))

    ax.set_xlabel("实际盈亏金额（元）", fontsize=12, color=TEXT_SECONDARY)
    ax.set_ylabel("心理价值（参考量纲）", fontsize=12, color=TEXT_SECONDARY)

    ax.set_xticks([-3000, -2000, -1000, 0, 1000, 2000, 3000])
    ax.set_xticklabels(["-3000", "-2000", "-1000", "0", "+1000", "+2000", "+3000"])
    ax.set_xlim(-3500, 3500)
    ax.set_ylim(-3300, 3300)

    style_axes(ax, grid_axis="both")

    # 区域框（用 axes 相对位置，但严守 0-1 范围）
    ax.text(0.55, 0.95, "盈利区（凹函数）",
            transform=ax.transAxes,
            fontsize=12, color=ACCENT, ha="left", va="top", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc=BG_SURFACE, ec=ACCENT, lw=1.0))
    ax.text(0.55, 0.12, "亏损区（凸函数、更陡）",
            transform=ax.transAxes,
            fontsize=12, color=UP, ha="left", va="bottom", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc=BG_SURFACE, ec=UP, lw=1.0))

    # 底部说明（放在 axes 内，避开 footer）
    ax.text(0.5, -0.16,
            "通俗翻译：你赚 1000 块的快乐，远远无法弥补你亏 1000 块的痛苦",
            transform=ax.transAxes, ha="center", fontsize=11,
            color=TEXT_SECONDARY, style="italic")

    add_footer(fig, SLUG, 3, TOTAL)
    return save(fig, SLUG, 3)


if __name__ == "__main__":
    paths = []
    paths.append(fig1_excess_volatility())
    paths.append(fig2_amygdala_hijack())
    paths.append(fig3_prospect_theory())
    for p in paths:
        print(f"  ✓ {p}")
    print(f"\nGenerated {len(paths)} images for {SLUG}")
