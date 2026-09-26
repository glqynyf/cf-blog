"""
ma20-ma60-moving-average-strategy.md 的 5 张配图。
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
SLUG = "ma20-ma60-moving-average-strategy"
TOTAL = 5


# ============ 图 1: 均线是"成本重力场"，不是一堵墙 ============
def fig1_gravity_field():
    fig, ax = new_fig()
    add_title(fig, "均线不是一堵静止的墙，而是流动的成本重力场")
    add_subtitle(fig, "均线 = 过去 N 天的市场平均成本，价格偏离越大，重力牵引越强")

    np.random.seed(11)
    days = np.arange(80)
    mid = 10 + np.sin(days / 12) * 0.8
    price = mid + np.sin(days / 4) * 1.2 + np.random.randn(80) * 0.4
    # 让几次偏离特别夸张：演示"橡皮筋被拉紧"
    price[30:35] += 3
    price[60:65] -= 3

    ax.plot(days, mid, color=TEXT_PRIMARY, lw=2.0, ls="--", label="20 日均线 = 成本重心")

    # 填充重力场示意（淡色背景）
    ax.fill_between(days, mid - 2, mid + 2, color=ACCENT_SUBTLE, alpha=0.4, label="重力场范围")

    ax.plot(days, price, color=UP, lw=1.4, label="价格")

    # 标注被拉紧的橡皮筋
    ax.annotate("橡皮筋拉紧\n（乖离率过大）",
                xy=(32, price[32]), xytext=(40, price[32] + 1.5),
                fontsize=12, color=UP, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=UP, lw=1.2))
    ax.annotate("橡皮筋拉紧\n（向下偏离）",
                xy=(62, price[62]), xytext=(66, price[62] + 1.8),
                fontsize=12, color=DOWN, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.2))

    ax.set_xlabel("交易日", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("价格", fontsize=11, color=TEXT_SECONDARY)
    ax.set_xlim(0, 80)
    ax.legend(loc="upper left", fontsize=10, frameon=False)
    style_axes(ax)

    add_footer(fig, SLUG, 1, TOTAL)
    return save(fig, SLUG, 1)


# ============ 图 2: 均线走平 vs 均线倾斜 ============
def fig2_flat_vs_tilted():
    fig, axes = new_fig(aspect=(W, H))
    add_title(fig, "均线走平 = 闭眼掷骰子，均线倾斜 = 真正可出手的时机")
    add_subtitle(fig, "走平时价格反复穿越均线 → 假突破陷阱；倾斜时价格顺势 → 主升浪")

    np.random.seed(3)
    days = np.arange(60)

    plt.close(fig)
    fig, axes = plt.subplots(2, 1, figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_PAGE)
    for ax in axes:
        ax.set_facecolor(BG_PAGE)

    # 上图：走平
    mid_flat = np.full_like(days, 10.0, dtype=float)
    price_flat = 10 + np.sin(days / 3) * 1.0 + np.random.randn(60) * 0.25
    axes[0].plot(days, mid_flat, color=TEXT_PRIMARY, lw=1.8, ls="--", label="20 日均线（走平）")
    axes[0].plot(days, price_flat, color=UP, lw=1.4, label="价格")
    axes[0].set_title("❌ 走平：反复穿越 → 假突破陷阱（碰均线就交易 = 给市场交手续费）",
                       fontsize=13, color=DOWN, pad=10, loc="left")

    # 下图：倾斜向上
    mid_tilt = 10 + days * 0.08
    price_tilt = mid_tilt + np.sin(days / 6) * 0.5 + np.random.randn(60) * 0.3
    axes[1].plot(days, mid_tilt, color=TEXT_PRIMARY, lw=1.8, ls="--", label="20 日均线（向上倾斜）")
    axes[1].plot(days, price_tilt, color=UP, lw=1.4, label="价格")
    axes[1].set_title("✓ 倾斜向上：均线自己抬头 → 真正的多头动能，回踩就是黄金上车点",
                       fontsize=13, color=ACCENT, pad=10, loc="left")

    for ax in axes:
        ax.set_xlim(0, 59)
        ax.set_xlabel("交易日", fontsize=11, color=TEXT_SECONDARY)
        ax.set_ylabel("价格", fontsize=11, color=TEXT_SECONDARY)
        ax.legend(loc="upper left", fontsize=10, frameon=False)
        style_axes(ax)

    fig.suptitle("均线走平 = 闭眼掷骰子，均线倾斜 = 真正可出手的时机",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.97)
    fig.text(0.5, 0.94, "走平时价格反复穿越均线 → 假突破陷阱；倾斜时价格顺势 → 主升浪",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")
    fig.subplots_adjust(left=0.06, right=0.97, top=0.88, bottom=0.06, hspace=0.35)

    add_footer(fig, SLUG, 2, TOTAL)
    return save(fig, SLUG, 2, tight=False)


# ============ 图 3: 20 日进攻线三大条件（信号流程图）============
def fig3_three_conditions():
    fig, ax = new_fig()
    add_title(fig, "20 日进攻线的三大条件：缺一不可")
    add_subtitle(fig, "斜率抬头 → 缩量悬空 → 放量反包，按顺序凑齐才出手")

    # 三个圆角矩形 + 箭头
    boxes = [
        (0.10, 0.55, "① 斜率抬头", "20 日均线\n连续 5 天\n数值逐日抬高", ACCENT_SUBTLE, ACCENT),
        (0.40, 0.55, "② 缩量悬空", "回踩 20 日线时\n成交量萎缩到\n放量时一半以下", BG_SURFACE, TEXT_PRIMARY),
        (0.70, 0.55, "③ 放量反包", "一根放量阳线\n吃掉回踩 K 线\n启动冲锋号", ACCENT_SUBTLE, UP),
    ]

    for x, y, title, body, fc, ec in boxes:
        box = plt.Rectangle((x, y), 0.18, 0.30,
                             facecolor=fc, edgecolor=ec, lw=2.0,
                             transform=ax.transAxes)
        ax.add_patch(box)
        ax.text(x + 0.09, y + 0.25, title, ha="center", va="center",
                fontsize=15, fontweight="bold", color=ec, transform=ax.transAxes)
        ax.text(x + 0.09, y + 0.13, body, ha="center", va="center",
                fontsize=11, color=TEXT_PRIMARY, transform=ax.transAxes)

    # 箭头
    for x in [0.29, 0.59]:
        ax.annotate("", xy=(x + 0.10, 0.70), xytext=(x, 0.70),
                    arrowprops=dict(arrowstyle="->", color=ACCENT, lw=2.5),
                    transform=ax.transAxes)

    # 底部说明
    ax.text(0.5, 0.30, "三个条件凑齐 → 进场点止损 = 回踩 K 线最低点 或 20 日线略下方",
            ha="center", fontsize=13, color=TEXT_SECONDARY, style="italic", transform=ax.transAxes)
    ax.text(0.5, 0.20, "⚠️ 缺任何一个条件都不动手，否则就是被均线反复绞杀的命",
            ha="center", fontsize=13, color=UP, fontweight="bold", transform=ax.transAxes)

    ax.text(0.5, 0.06, "用小止损切进主升浪里最快最暴力的一段",
            ha="center", fontsize=12, color=TEXT_MUTED, transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    add_footer(fig, SLUG, 3, TOTAL)
    return save(fig, SLUG, 3)


# ============ 图 4: 双线四种形态 ============
def fig4_four_patterns():
    fig, axes = new_fig(aspect=(W, H))
    add_title(fig, "20 日 + 60 日双均线：四种标准形态决定你的打法")

    np.random.seed(5)
    days = np.arange(60)

    plt.close(fig)
    fig, axes = plt.subplots(2, 2, figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_PAGE)
    for ax in axes.flat:
        ax.set_facecolor(BG_PAGE)

    patterns = [
        ("① 双线多头共振（最健康）",  "顺势做多 + 回踩加仓 + 死拿不放",
         lambda d: (8 + d * 0.15, 8 + d * 0.10, 1.5), ACCENT, "最佳"),
        ("② 进攻转折预警",  "减进攻仓 + 防守线提到 60 日 + 进入观察期",
         lambda d: (8 + d * 0.15, 8 + d * 0.13 - 0.5 + np.where(d < 30, 0, -0.6 * (d - 30) / 30), 1.5), TEXT_MUTED, "警告"),
        ("③ 双线空头共振（杀伤最大）",  "空仓等冰雹化完，不动就是最高明",
         lambda d: (8 - d * 0.12, 8 - d * 0.10, 1.5), DOWN, "危险"),
        ("④ 生命复苏试探",  "派侦察仓试水 + 回踩确认再加仓",
         lambda d: (8 + np.where(d < 30, 0, (d - 30) * 0.10), 8 + d * 0.05, np.where(d < 30, 1.2, 1.5)), ACCENT, "复苏"),
    ]

    for ax, (title, advice, gen, color, icon) in zip(axes.flat, patterns):
        ma20, ma60, vol = gen(days)
        upper = ma60 + 2 * vol
        lower = ma60 - 2 * vol
        price = ma20 + np.random.randn(60) * vol * 0.3

        ax.fill_between(days, lower, upper, color=ACCENT_SUBTLE, alpha=0.4)
        ax.plot(days, ma20, color=color, lw=2.0, label="20 日线")
        ax.plot(days, ma60, color=TEXT_PRIMARY, lw=2.0, ls="--", label="60 日线")
        ax.plot(days, price, color=UP, lw=1.2, alpha=0.85)
        ax.set_title(f"{icon} {title}", fontsize=13, color=color, pad=8, loc="left", fontweight="bold")
        ax.text(0.02, 0.05, f"打法：{advice}", transform=ax.transAxes,
                fontsize=10, color=TEXT_SECONDARY, va="bottom")
        ax.set_xlim(0, 59)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(BORDER)
        ax.legend(loc="upper left", fontsize=8, frameon=False)

    fig.suptitle("20 日 + 60 日双均线：四种标准形态决定你的打法",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.98)
    fig.subplots_adjust(left=0.04, right=0.98, top=0.92, bottom=0.04, wspace=0.15, hspace=0.35)

    add_footer(fig, SLUG, 4, TOTAL)
    return save(fig, SLUG, 4, tight=False)


# ============ 图 5: 60 日生命线 + 三三法则 ============
def fig5_three_three_rule():
    fig, ax = new_fig()
    add_title(fig, "60 日生命线真破位的「三三法则」：3% 空间 + 3 天时间")
    add_subtitle(fig, "两道关卡同时被突破，才是真正的中期破位；否则都是诱空假摔")

    # 模拟价格走势：先上行站稳 60 日线，再跌破
    np.random.seed(17)
    days = np.arange(80)
    ma60 = 10 + np.where(days < 50, days * 0.04, 2.0 - (days - 50) * 0.10)
    price = ma60 + np.where(
        days < 50,
        1.5 + np.sin(days / 5) * 0.5 + np.random.randn(80) * 0.3,
        -1.0 * (days - 50) * 0.04 + np.random.randn(80) * 0.4  # 跌破过程
    )

    # 找出真正跌破 3% 且连续 3 天的位置
    ratio = (price - ma60) / ma60
    breach_persistent = (ratio < -0.03).astype(int)
    # 滑动窗口 3 天
    persistent_3d = np.convolve(breach_persistent, np.ones(3), mode="same") >= 3

    ax.plot(days, price, color=UP, lw=1.6, label="价格")
    ax.plot(days, ma60, color=ACCENT, lw=2.5, label="60 日生命线")

    # 标注真破位开始
    first_breach = np.where(persistent_3d)[0]
    if len(first_breach) > 0:
        idx = first_breach[0]
        ax.axvline(idx, color=DOWN, ls=":", lw=1.5)
        ax.annotate(f"真破位确认\n（第 {idx} 天起）",
                    xy=(idx, price[idx]), xytext=(idx - 10, price[idx] - 1.5),
                    fontsize=12, color=DOWN, ha="center", fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.2))

    # 早期假跌破标注
    ax.annotate("假跌破 1.5%\n（诱空，未触发三三）",
                xy=(20, ma60[20] - 0.15), xytext=(15, ma60[20] - 1.8),
                fontsize=11, color=TEXT_MUTED, ha="center",
                arrowprops=dict(arrowstyle="->", color=TEXT_MUTED, lw=1.0))

    ax.set_xlabel("交易日", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("价格", fontsize=11, color=TEXT_SECONDARY)
    ax.set_xlim(0, 80)
    ax.legend(loc="upper left", fontsize=10, frameon=False)
    style_axes(ax)

    # 右下角规则说明
    rule_text = (
        "三三法则 = 两道硬关卡\n"
        "① 空间关：跌破 60 日线 ≥ 3%\n"
        "② 时间关：连续 3 天收不回 60 日线"
    )
    ax.text(0.98, 0.55, rule_text, transform=ax.transAxes,
            fontsize=11, color=TEXT_PRIMARY, ha="right", va="top",
            bbox=dict(boxstyle="round,pad=0.5", fc=ACCENT_SUBTLE, ec=ACCENT, lw=1.0))

    add_footer(fig, SLUG, 5, TOTAL)
    return save(fig, SLUG, 5)


if __name__ == "__main__":
    paths = []
    paths.append(fig1_gravity_field())
    paths.append(fig2_flat_vs_tilted())
    paths.append(fig3_three_conditions())
    paths.append(fig4_four_patterns())
    paths.append(fig5_three_three_rule())
    for p in paths:
        print(f"  ✓ {p}")
    print(f"\nGenerated {len(paths)} images for {SLUG}")
