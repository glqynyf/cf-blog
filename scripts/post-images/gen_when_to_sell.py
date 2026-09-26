"""
when-to-sell-stock.md 的 3 张配图。
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
SLUG = "when-to-sell-stock"
TOTAL = 3


# ============ 图 1: 处置效应 Odean 数据（柱状对比）============
def fig1_disposition_effect():
    fig, ax = new_fig()
    add_title(fig, "处置效应：散户把浮盈卖得太快，浮亏死扛不敢认")
    add_subtitle(fig, "Odean (1998) 10,000 个美国券商账户实证——盈利股实现率 14.8% vs 亏损股实现率 9.8%")

    # 柱状图
    categories = ["盈利股\n实现比例", "亏损股\n实现比例"]
    rates = [14.8, 9.8]
    colors = [UP, ACCENT]

    bars = ax.bar(categories, rates, color=colors, edgecolor="none", width=0.55)

    # 每根柱子上的数值
    for bar, rate in zip(bars, rates):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                f"{rate}%", ha="center", va="bottom",
                fontsize=22, fontweight="bold", color=TEXT_PRIMARY)

    # 中间连线和差距标注
    ax.annotate("", xy=(1, 9.8), xytext=(1, 14.8),
                arrowprops=dict(arrowstyle="<->", color=DOWN, lw=2.0))
    ax.text(1.15, 12.3, "差距 5 个百分点\n(1.5 倍关系)", fontsize=12,
            color=DOWN, ha="left", va="center", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc=BG_SURFACE, ec=DOWN, lw=1.2))

    # 越下放大 / 越上紧握 标注
    ax.text(0, 17, "早早锁利", ha="center", fontsize=12,
            color=UP, fontweight="bold")
    ax.text(1, 17, "死死扛单", ha="center", fontsize=12,
            color=ACCENT, fontweight="bold")

    ax.set_ylim(0, 22)
    ax.set_ylabel("实现比例 (%)", fontsize=12, color=TEXT_SECONDARY)
    style_axes(ax, grid_axis="y")

    # 在绘图区域内部上方留一段信息条
    info_box = plt.Rectangle((0.05, 0.85), 0.90, 0.05,
                              facecolor=ACCENT_SUBTLE, edgecolor="none", alpha=0.5,
                              transform=fig.transFigure)
    ax.add_patch(info_box)
    ax.text(0.5, 0.875,
            "盈利 vs 亏损 = 14.8% vs 9.8%   →   卖出盈利的可能性是卖出亏损的 1.5 倍",
            transform=fig.transFigure,
            ha="center", va="center", fontsize=12, color=TEXT_PRIMARY, fontweight="bold")

    # 底部解释（用 fig 坐标，放在 axes 下方）
    fig.text(0.5, 0.05,
            "Kahneman & Tversky 前景理论：损失带来的痛苦约为同等收益快乐的 2~2.5 倍 — 这就是为什么我们把汗血宝马卖掉，把病马留在马圈里继续喂草",
            ha="center", fontsize=10, color=TEXT_SECONDARY, style="italic")

    add_footer(fig, SLUG, 1, TOTAL)
    return save(fig, SLUG, 1)


# ============ 图 2: 4 个卖出标准卡片网格（2x2）============
def fig2_four_sell_standards():
    fig, ax = new_fig()
    add_title(fig, "4 个卖出标准 + 1 个验证工具：把模糊感觉翻译成纪律")
    add_subtitle(fig, "任何一个标准被触发都该考虑减仓；多个同时触发 → 必须行动")

    standards = [
        # (pos_y, pos_x, color, num, name, sub, criteria, action)
        (0.56, 0.06, UP, "01", "买入逻辑物理死亡",
         "彼得·林奇「两分钟独白」",
         "核心支柱断裂\n(对手颠覆 / 模式崩塌)",
         "第一时间\n无条件卖出"),
        (0.56, 0.53, DOWN, "02", "估值过载",
         "PEG > 2 + 历史分位 > 90%",
         "PE 分位 > 90%\n回撤 10%~15%",
         "系统化减仓\n1/3 + 移动止损"),
        (0.18, 0.06, ACCENT, "03", "机会成本",
         "芒格：放弃的最佳资产就是真实成本",
         "同等资金\n可买更优资产？",
         "认真考虑\n换股 / 持币"),
        (0.18, 0.53, TEXT_MUTED, "04", "睡眠指数",
         "J.P. Morgan：一直卖到能睡着觉",
         "波动率过载\n心跳失控 / 频繁看盘",
         "强制减仓\n买回睡眠"),
    ]

    card_w, card_h = 0.41, 0.30

    for y, x, color, num, name, sub, criteria, action in standards:
        # 卡片背景
        rect = plt.Rectangle((x, y), card_w, card_h, facecolor=BG_SURFACE,
                              edgecolor=color, lw=1.5,
                              transform=ax.transAxes)
        ax.add_patch(rect)

        # 顶部色条（占 0.05）
        bar_h = 0.05
        bar = plt.Rectangle((x, y + card_h - bar_h), card_w, bar_h,
                            facecolor=color, edgecolor="none",
                            transform=ax.transAxes)
        ax.add_patch(bar)

        # 编号圆（在色条上的左侧）
        circle_r = 0.022
        circle = plt.Circle((x + 0.04, y + card_h - bar_h / 2), circle_r,
                             facecolor="white", edgecolor=color, lw=2.0,
                             transform=ax.transAxes)
        ax.add_patch(circle)
        ax.text(x + 0.04, y + card_h - bar_h / 2, num, ha="center", va="center",
                fontsize=10, fontweight="bold", color=color,
                transform=ax.transAxes)

        # 主标题（在色条的右侧）
        ax.text(x + 0.08, y + card_h - bar_h / 2, name, ha="left", va="center",
                fontsize=14, fontweight="bold", color="white",
                transform=ax.transAxes)

        # 副标（引用）
        ax.text(x + 0.03, y + card_h - bar_h - 0.035, sub, ha="left", va="center",
                fontsize=9, color=TEXT_SECONDARY, style="italic",
                transform=ax.transAxes)

        # 触发条件
        ax.text(x + 0.03, y + card_h - bar_h - 0.085,
                "触发条件：", ha="left", va="center",
                fontsize=10, fontweight="bold", color=color,
                transform=ax.transAxes)
        ax.text(x + 0.03, y + card_h - bar_h - 0.115, criteria,
                ha="left", va="center", fontsize=10, color=TEXT_PRIMARY,
                transform=ax.transAxes)

        # 行动
        ax.text(x + 0.03, y + 0.05,
                f"执行：{action.replace(chr(10), ' / ')}",
                ha="left", va="center", fontsize=11, fontweight="bold",
                color=color, transform=ax.transAxes)

    # 第五个验证工具 - 横跨
    ver_h = 0.10
    ver_y = 0.05
    rect = plt.Rectangle((0.06, ver_y), 0.88, ver_h,
                          facecolor=ACCENT, edgecolor="none", alpha=0.85,
                          transform=ax.transAxes)
    ax.add_patch(rect)
    # 编号圆
    circle = plt.Circle((0.10, ver_y + ver_h / 2), 0.022,
                         facecolor="white", edgecolor="white", lw=1.5,
                         transform=ax.transAxes)
    ax.add_patch(circle)
    ax.text(0.10, ver_y + ver_h / 2, "05", ha="center", va="center",
            fontsize=10, fontweight="bold", color=ACCENT,
            transform=ax.transAxes)
    ax.text(0.14, ver_y + ver_h - 0.025,
            "隔夜重置测试 · 持有 = 当日全价买入",
            ha="left", va="center", fontsize=12, fontweight="bold",
            color="white", transform=ax.transAxes)
    ax.text(0.14, ver_y + 0.020,
            "「今晚全部清仓按收盘价 → 明天你还会用同样价格把它买回来吗？」",
            ha="left", va="center", fontsize=10, color="white",
            style="italic", transform=ax.transAxes)
    ax.text(0.14, ver_y + ver_h - 0.025,
            "",
            ha="left", va="center", fontsize=11, color="white",
            transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    add_footer(fig, SLUG, 2, TOTAL)
    return save(fig, SLUG, 2)


# ============ 图 3: 隔夜重置测试 - 决策流程 ============
def fig3_overnight_reset():
    fig, ax = new_fig()
    add_title(fig, "隔夜重置测试：剥离路径依赖和损失厌恶的思维工具")
    add_subtitle(fig, "「今天的持有」在决策逻辑上 =「今天用开盘价重新全额买入」")

    # 顶部 - 起点
    start_y = 0.85
    start_rect = plt.Rectangle((0.20, start_y), 0.60, 0.07,
                                facecolor=TEXT_PRIMARY, edgecolor="none",
                                transform=ax.transAxes)
    ax.add_patch(start_rect)
    ax.text(0.5, start_y + 0.035,
            "闭上眼睛：今晚所有交易所被不可修复的灾难击穿",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color="white", transform=ax.transAxes)

    # 流程
    step_y = 0.66
    step1_rect = plt.Rectangle((0.20, step_y), 0.60, 0.10,
                                facecolor=ACCENT, edgecolor="none",
                                transform=ax.transAxes)
    ax.add_patch(step1_rect)
    ax.text(0.5, step_y + 0.05,
            "你名下的所有持仓在收盘瞬间被强制按收盘价卖出",
            ha="center", va="center", fontsize=12, fontweight="bold",
            color="white", transform=ax.transAxes)

    step2_rect = plt.Rectangle((0.20, step_y - 0.13), 0.60, 0.10,
                                facecolor=ACCENT, edgecolor="none",
                                transform=ax.transAxes)
    ax.add_patch(step2_rect)
    ax.text(0.5, step_y - 0.08,
            "账户里只剩下等额的现金，热气腾腾",
            ha="center", va="center", fontsize=12, fontweight="bold",
            color="white", transform=ax.transAxes)

    # 关键提问
    ask_y = 0.36
    ask_rect = plt.Rectangle((0.10, ask_y), 0.80, 0.13,
                              facecolor=UP, edgecolor="none", alpha=0.90,
                              transform=ax.transAxes)
    ax.add_patch(ask_rect)
    ax.text(0.5, ask_y + 0.085,
            "你会愿意按昨晚的收盘价",
            ha="center", va="center", fontsize=12,
            color="white", transform=ax.transAxes)
    ax.text(0.5, ask_y + 0.045,
            "把那只让你纠结、痛苦、又爱又恨的股票",
            ha="center", va="center", fontsize=14, fontweight="bold",
            color="white", transform=ax.transAxes)
    ax.text(0.5, ask_y + 0.005,
            "原封不动地全部买回来吗？",
            ha="center", va="center", fontsize=14, fontweight="bold",
            color="white", transform=ax.transAxes)

    # 两个分支
    branch_y = 0.20
    yes_rect = plt.Rectangle((0.06, branch_y), 0.40, 0.10,
                              facecolor=DOWN, edgecolor="none", alpha=0.85,
                              transform=ax.transAxes)
    ax.add_patch(yes_rect)
    ax.text(0.26, branch_y + 0.07,
            "是 —> 继续持有",
            ha="center", va="center", fontsize=14, fontweight="bold",
            color="white", transform=ax.transAxes)
    ax.text(0.26, branch_y + 0.025,
            "这笔资产在你的投资体系里依然有一席之地",
            ha="center", va="center", fontsize=9, color="white",
            style="italic", transform=ax.transAxes)

    no_rect = plt.Rectangle((0.54, branch_y), 0.40, 0.10,
                             facecolor=UP, edgecolor="none", alpha=0.85,
                             transform=ax.transAxes)
    ax.add_patch(no_rect)
    ax.text(0.74, branch_y + 0.07,
            "否 —> 当日卖出",
            ha="center", va="center", fontsize=14, fontweight="bold",
            color="white", transform=ax.transAxes)
    ax.text(0.74, branch_y + 0.025,
            "为什么还每天死守着？ 立刻换成你更想持有的资产或持币",
            ha="center", va="center", fontsize=9, color="white",
            style="italic", transform=ax.transAxes)

    # 箭头
    for from_y, to_y in [(0.85, 0.76), (0.66, 0.53), (0.53, 0.49)]:
        ax.annotate("", xy=(0.5, to_y), xytext=(0.5, from_y),
                    arrowprops=dict(arrowstyle="->", color=TEXT_PRIMARY, lw=2.0),
                    transform=ax.transAxes)

    # 决策箭头到分支
    ax.annotate("", xy=(0.26, 0.30), xytext=(0.40, 0.36),
                arrowprops=dict(arrowstyle="->", color=DOWN, lw=2.0),
                transform=ax.transAxes)
    ax.annotate("", xy=(0.74, 0.30), xytext=(0.60, 0.36),
                arrowprops=dict(arrowstyle="->", color=UP, lw=2.0),
                transform=ax.transAxes)

    # 底部金句
    ax.text(0.5, 0.12,
            "这个测试瞬间剥离了人性两大黑洞：路径依赖 + 损失厌恶",
            ha="center", va="top", fontsize=12, color=TEXT_SECONDARY,
            style="italic", transform=ax.transAxes)
    ax.text(0.5, 0.06,
            "※ 在股票市场里，持有 = 当日开盘重新全额买入一次",
            ha="center", va="top", fontsize=13, color=UP, fontweight="bold",
            transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    add_footer(fig, SLUG, 3, TOTAL)
    return save(fig, SLUG, 3)


if __name__ == "__main__":
    paths = []
    paths.append(fig1_disposition_effect())
    paths.append(fig2_four_sell_standards())
    paths.append(fig3_overnight_reset())
    for p in paths:
        print(f"  ✓ {p}")
    print(f"\nGenerated {len(paths)} images for {SLUG}")
