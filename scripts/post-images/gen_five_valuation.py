"""
five-valuation-models-no-dcf-myth.md 的 5 张配图。
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
SLUG = "five-valuation-models-no-dcf-myth"
TOTAL = 5


# ============ 图 1: 周期股 PE 陷阱 ============
def fig1_pe_cycle_trap():
    fig, ax = new_fig()
    add_title(fig, "周期股的 PE 陷阱：景气高峰 PE 看着便宜，其实是顶部信号")
    add_subtitle(fig, "某航运公司盈利：景气顶 → 利润暴增 5 倍 → PE 看似 2 倍 → 一年后利润缩水九成 → 实际 PE 变 20 倍")

    # 模拟一个完整周期（5 年）
    years = np.arange(0, 5)
    # 利润曲线（景气周期）
    profit = np.array([1.0, 2.0, 5.0, 3.0, 0.5])  # 高峰在第 3 年
    # 股价（滞后于利润）
    price = np.array([1.0, 1.3, 1.8, 2.2, 1.5])

    ax.plot(years, profit, color=UP, lw=2.5, marker="o", markersize=10, label="公司净利润（亿元）")
    ax.plot(years, price, color=TEXT_PRIMARY, lw=2.5, marker="s", markersize=10, label="股价（元）")

    # 标注 PE
    for i, (p, q) in enumerate(zip(price, profit)):
        pe = p / q
        ax.annotate(f"PE ≈ {pe:.1f}",
                    xy=(i, price[i] + 0.15), xytext=(i, price[i] + 0.5),
                    ha="center", fontsize=11,
                    color=DOWN if pe < 2.5 else UP,
                    fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=TEXT_MUTED, lw=0.8))

    # 警示
    ax.annotate("PE = 2 倍看似'便宜'\n实际是景气顶！\n一年后利润缩水九成",
                xy=(2, price[2]), xytext=(2, 3.0),
                fontsize=12, color=DOWN, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.5),
                bbox=dict(boxstyle="round,pad=0.4", fc=BG_SURFACE, ec=DOWN, lw=1.5))

    ax.set_xlabel("年份（一个完整景气周期）", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("归一化值", fontsize=11, color=TEXT_SECONDARY)
    ax.set_xticks(years)
    ax.set_xticklabels(["第1年", "第2年\n（复苏）", "第3年\n（景气顶）", "第4年\n（衰退）", "第5年\n（底部）"])
    ax.set_xlim(-0.3, 4.3)
    ax.set_ylim(0, 3.5)
    ax.legend(loc="upper left", fontsize=10, frameon=False)
    style_axes(ax)

    add_footer(fig, SLUG, 1, TOTAL)
    return save(fig, SLUG, 1)


# ============ 图 2: PEG 矩阵 ============
def fig2_peg_matrix():
    fig, ax = new_fig()
    add_title(fig, "PEG 矩阵：把 PE 静态数字升级为动态视角")
    add_subtitle(fig, "横轴 = 净利润年增长率，纵轴 = PE；圆圈颜色代表 PEG 估值档位")

    growth = np.array([5, 10, 15, 20, 25, 30, 40, 50, 60, 80])
    pe_levels = np.array([10, 15, 20, 25, 30, 40, 50, 70, 100])

    # 画 3 条 PEG 等值线
    for peg_target in [0.5, 1.0, 2.0]:
        pe_line = peg_target * growth
        valid = pe_line <= pe_levels.max()
        ax.plot(growth[valid], pe_line[valid], lw=2.0, ls="--", alpha=0.6,
                label=f"PEG = {peg_target}" + ("（低估）" if peg_target == 0.5 else "（合理）" if peg_target == 1.0 else "（高估）"))

    # 标注几个公司类型示例
    examples = [
        (5, 12, "成熟大盘股\nPE 12, 增 5%\nPEG=2.4（偏贵）", DOWN),
        (15, 25, "稳健成长股\nPE 25, 增 15%\nPEG=1.7（合理）", TEXT_PRIMARY),
        (40, 40, "高成长股\nPE 40, 增 40%\nPEG=1.0（便宜）", UP),
        (60, 60, "超高速成长\nPE 60, 增 60%\nPEG=1.0（平衡）", ACCENT),
    ]
    for g, p, label, color in examples:
        ax.scatter([g], [p], s=300, color=color, edgecolor=TEXT_PRIMARY, lw=2, zorder=10)
        ax.annotate(label, xy=(g, p), xytext=(g + 5, p + 8),
                    fontsize=10, color=color, ha="left", fontweight="bold")

    ax.set_xlabel("净利润年增长率（%）", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("PE（倍）", fontsize=11, color=TEXT_SECONDARY)
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 110)
    ax.legend(loc="upper left", fontsize=10, frameon=False)
    style_axes(ax)

    add_footer(fig, SLUG, 2, TOTAL)
    return save(fig, SLUG, 2)


# ============ 图 3: 40 法则矩阵 ============
def fig3_rule_of_40():
    fig, ax = new_fig()
    add_title(fig, "40 法则：增长率 + 利润率 ≥ 40% = 健康 SaaS 公司")
    add_subtitle(fig, "横轴 = 营收增长率，纵轴 = 利润率（FCF 或 EBITDA Margin）")

    # 40% 等值线
    growth = np.linspace(0, 80, 100)
    margin_40 = 40 - growth
    ax.plot(growth, margin_40, color=DOWN, lw=2.5, ls="--", label="40 法则等值线（≥40% 为通过）")

    ax.fill_between(growth, margin_40, 80, color=ACCENT_SUBTLE, alpha=0.4, label="通过区（健康）")
    ax.fill_between(growth, -50, margin_40, color="#fde8e8", alpha=0.4, label="不通过区（成长性不足）")

    # 标注 4 类公司
    examples = [
        (50, -8, "高速增长 SaaS\n战略性亏损中", ACCENT),
        (20, 25, "成熟 SaaS\n现金流良好", UP),
        (10, -5, "伪成长\n烧钱换收入", DOWN),
        (60, 10, "顶尖 SaaS\n收入+利润双高", ACCENT),
    ]
    for g, m, label, color in examples:
        ax.scatter([g], [m], s=300, color=color, edgecolor=TEXT_PRIMARY, lw=2, zorder=10)
        ax.annotate(label, xy=(g, m), xytext=(g + 3, m - 12),
                    fontsize=10, color=color, ha="left", fontweight="bold")

    # 40% 等值线上的关键点
    for g in [20, 40, 60]:
        m = 40 - g
        ax.plot(g, m, "o", color=DOWN, markersize=8)

    ax.set_xlabel("营收增长率（%）", fontsize=11, color=TEXT_SECONDARY)
    ax.set_ylabel("利润率（%，FCF 或 EBITDA Margin）", fontsize=11, color=TEXT_SECONDARY)
    ax.set_xlim(0, 80)
    ax.set_ylim(-50, 80)
    ax.axhline(0, color=TEXT_MUTED, lw=0.8)
    ax.legend(loc="upper right", fontsize=10, frameon=False)
    style_axes(ax)

    add_footer(fig, SLUG, 3, TOTAL)
    return save(fig, SLUG, 3)


# ============ 图 4: DCF 敏感性 ============
def fig4_dcf_sensitivity():
    fig, axes = new_fig(aspect=(W, H))
    add_title(fig, "DCF 的致命软肋：折现率/永续增长率微调 → 估值大幅变化")
    add_subtitle(fig, "调一点点输入参数，就像调哈勃望远镜，看到的可能是完全不同的星系")

    # 左侧：折现率敏感度
    ax1 = axes
    discount = np.linspace(6, 12, 50)
    npv_8pct_g = 100  # 永续增长率 2%
    npv_9pct_g = 95
    npv_10pct_g = 88

    ax1.plot(discount, npv_8pct_g * (1 / discount) ** 2, color=UP, lw=2.5, label="永续增 2%")
    ax1.plot(discount, npv_9pct_g * (1 / discount) ** 2, color=ACCENT, lw=2.5, label="永续增 2.5%")
    ax1.plot(discount, npv_10pct_g * (1 / discount) ** 2, color=TEXT_MUTED, lw=2.5, label="永续增 3%")

    # 标注：折现率从 8% → 9%
    ax1.annotate("折现率从 8% 调到 9%\n（看似只动 1 个百分点）\n估值可能掉 15%-20%",
                 xy=(8.5, 110), xytext=(8.5, 200),
                 fontsize=11, color=UP, ha="center", fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color=UP, lw=1.2),
                 bbox=dict(boxstyle="round,pad=0.4", fc=BG_SURFACE, ec=UP, lw=1.2))

    ax1.set_xlabel("折现率（%）", fontsize=11, color=TEXT_SECONDARY)
    ax1.set_ylabel("企业估值（亿元）", fontsize=11, color=TEXT_SECONDARY)
    ax1.set_xlim(6, 12)
    ax1.legend(loc="upper right", fontsize=10, frameon=False)
    style_axes(ax1)

    fig.suptitle("DCF 的致命软肋：折现率/永续增长率微调 → 估值大幅变化",
                 fontsize=20, fontweight="bold", color=TEXT_PRIMARY, y=0.96)
    fig.text(0.5, 0.92,
             "调一点点输入参数，就像调哈勃望远镜，看到的可能是完全不同的星系",
             ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic")
    fig.subplots_adjust(left=0.07, right=0.97, top=0.86, bottom=0.08)

    add_footer(fig, SLUG, 4, TOTAL)
    return save(fig, SLUG, 4, tight=False)


# ============ 图 5: 五把尺子适用场景矩阵 ============
def fig5_five_models():
    fig, ax = new_fig()
    add_title(fig, "五把尺子的适用场景矩阵：不同行业用不同的估值公式")
    add_subtitle(fig, "公式只是计算器，真正输入的是你对商业模式和护城河的理解")

    # 矩阵表
    matrix = [
        ["", "适用行业", "关键陷阱", "配合指标"],
        ["PE + PEG", "白酒 / 家电 / 消费", "低 PE 周期股陷阱", "PEG 修正成长"],
        ["PB + RNAV", "银行 / 保险 / 地产", "账面净资产高估", "重估净资产"],
        ["PS + 40 法则\n+ LTV/CAC", "SaaS / AI / 互联网", "毒药收入 / 不健康获客", "LTV ≥ 3×CAC"],
        ["EV / EBITDA", "跨国并购 / 重资产", "穿透资本结构", "调整后 EBITDA"],
        ["DCF + 所有者收益", "商业模式简单 / 现金流稳", "输入变量敏感", "安全边际折扣"],
    ]

    n_rows = len(matrix)
    n_cols = len(matrix[0])
    cell_h = 0.85 / n_rows
    cell_w = 0.95 / n_cols

    colors = [BG_SURFACE, ACCENT_SUBTLE, BG_SURFACE, BG_SURFACE, BG_SURFACE, ACCENT_SUBTLE]
    ec_colors = [BORDER, ACCENT, BORDER, BORDER, BORDER, ACCENT]

    for i, row in enumerate(matrix):
        y = 0.92 - (i + 1) * cell_h
        for j, val in enumerate(row):
            x = 0.025 + j * cell_w
            is_header = (i == 0)
            is_left = (j == 0)
            color = TEXT_PRIMARY if is_header else TEXT_PRIMARY
            weight = "bold" if (is_header or is_left) else "normal"
            ax.add_patch(plt.Rectangle((x, y), cell_w * 0.97, cell_h * 0.92,
                                        facecolor=colors[i] if not is_header else TEXT_PRIMARY,
                                        edgecolor=ec_colors[i] if not is_header else TEXT_PRIMARY,
                                        lw=1.0, transform=ax.transAxes))
            text_color = "white" if is_header else TEXT_PRIMARY
            ax.text(x + cell_w * 0.485, y + cell_h * 0.46, val,
                    ha="center", va="center", fontsize=11 if not is_header else 12,
                    color=text_color, fontweight=weight, transform=ax.transAxes)

    # 底部提示
    ax.text(0.5, 0.04,
            "⚠️ 同一公司最好用多把尺子交叉验证；只用一把容易陷入估值陷阱",
            ha="center", fontsize=12, color=UP, fontweight="bold", transform=ax.transAxes)

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
    paths.append(fig1_pe_cycle_trap())
    paths.append(fig2_peg_matrix())
    paths.append(fig3_rule_of_40())
    paths.append(fig4_dcf_sensitivity())
    paths.append(fig5_five_models())
    for p in paths:
        print(f"  ✓ {p}")
    print(f"\nGenerated {len(paths)} images for {SLUG}")
