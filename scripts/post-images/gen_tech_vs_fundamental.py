"""
tech-vs-fundamental.md 的 3 张配图。
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
SLUG = "tech-vs-fundamental"
TOTAL = 3


# ============ 图 1: 两派对比总表 ============
def fig1_two_schools_compare():
    fig, ax = new_fig()
    add_title(fig, "技术派 vs 基本面派：一张表看清六大维度差异")
    add_subtitle(fig, "研究对象、时间尺度、关注焦点、适用信息、典型工具、致命硬伤——他们看的根本不是同一件事")

    # 6 维度对比
    rows = [
        ("维度", "技术派", "基本面派"),
        ("研究对象", "资金在做什么", "公司将来能赚多少钱"),
        ("时间尺度", "几天 ~ 几周", "几个季度 ~ 几年"),
        ("关注焦点", "价格、成交量、盘口", "ROE、现金流、行业空间"),
        ("适用信息", "所有公开信息（含小道）", "财报、研报、行业数据"),
        ("典型工具", "K 线、均线、MACD", "杜邦拆解、PEG、DCF"),
        ("致命硬伤", "拟合陷阱 + 画线被操控", "低估值陷阱 + 时间成本"),
    ]

    n_rows = len(rows)
    # 每行高度 0.10，从 0.82 到 0.22（避开底部注释）
    y_top = 0.85
    y_bot = 0.20
    row_h = (y_top - y_bot) / n_rows

    col_x = [0.18, 0.50, 0.82]
    col_w = 0.30  # 列宽（transAxes 单位）

    # 绘制整张表底色（先铺一层白底圆角矩形）
    table_rect = plt.Rectangle((0.05, y_bot), 0.90, y_top - y_bot,
                                facecolor=BG_SURFACE, edgecolor=BORDER, lw=1.0,
                                transform=ax.transAxes)
    ax.add_patch(table_rect)

    # 填充行背景（交替条纹）
    for i in range(1, n_rows):
        row_color = BG_PAGE if i % 2 == 1 else BG_SURFACE
        rect = plt.Rectangle((0.05, y_top - (i + 1) * row_h),
                              0.90, row_h,
                              facecolor=row_color, edgecolor="none",
                              transform=ax.transAxes)
        ax.add_patch(rect)

    # 表头行覆盖（ACCENT 底色）
    head_rect = plt.Rectangle((0.05, y_top - row_h), 0.90, row_h,
                               facecolor=ACCENT, edgecolor="none",
                               transform=ax.transAxes)
    ax.add_patch(head_rect)

    # 行间分隔线（浅）
    for i in range(1, n_rows):
        ax.plot([0.05, 0.95], [y_top - i * row_h, y_top - i * row_h],
                color=BORDER, lw=0.6, transform=ax.transAxes)

    # 列分隔线
    for j in [0.36, 0.64]:
        ax.plot([j, j], [y_bot, y_top],
                color=BORDER, lw=0.6, transform=ax.transAxes)

    # 表格文本
    for i, row in enumerate(rows):
        y = y_top - (i + 0.5) * row_h
        for j, val in enumerate(row):
            if i == 0:
                color = "white"
                weight = "bold"
                size = 16
            elif j == 1:
                color = UP
                weight = "bold"
                size = 14
            elif j == 2:
                color = ACCENT
                weight = "bold"
                size = 14
            else:
                color = TEXT_PRIMARY
                weight = "normal"
                size = 13

            ax.text(col_x[j], y, val, ha="center", va="center",
                    fontsize=size, color=color, fontweight=weight,
                    transform=ax.transAxes)

    # 底部注释
    ax.text(0.5, 0.13,
            "互相看不起不是偏见，是研究对象在时间尺度和信息结构上的本质错位",
            ha="center", fontsize=12, color=TEXT_SECONDARY, style="italic",
            transform=ax.transAxes)
    ax.text(0.5, 0.08,
            "融合 = 基本面选股（定方向）+ 技术面择时（找时机）+ 仓位管理（控风险）",
            ha="center", fontsize=11, color=UP, fontweight="bold",
            transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    add_footer(fig, SLUG, 1, TOTAL)
    return save(fig, SLUG, 1)


# ============ 图 2: 时间维度错位的横向时间轴 ============
def fig2_time_axis():
    fig, ax = new_fig()
    add_title(fig, "时间维度的错位：股票投资的六种时间尺度")
    add_subtitle(fig, "方法论不分对错，只看你站在哪一段——左端的人嘲笑右端的人，右端的人也嘲笑左端的人")

    # 横向时间轴
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 10)

    # 时间刻度
    stops = [
        (5, "分钟\n级别", DOWN, "看盘口\n做 T+0"),
        (25, "日内\n超短", DOWN, "换手率\n板块热度"),
        (45, "波段\n(几周)", UP, "均线、量价\n技术形态"),
        (65, "中线\n(几月)", TEXT_PRIMARY, "基本面护城河\n+ 技术择时"),
        (85, "长线\n(几年)", ACCENT, "DCF、ROE\n行业空间"),
    ]

    # 主轴
    ax.plot([0, 100], [5, 5], color=TEXT_PRIMARY, lw=2.5)

    # 标注
    for x, name, color, desc in stops:
        # 圆点
        ax.scatter(x, 5, s=200, color=color, edgecolor=BG_PAGE, lw=2, zorder=3)
        # 标签
        ax.text(x, 6.2, name, ha="center", va="bottom", fontsize=12,
                color=color, fontweight="bold")
        # 上下方法派
        ax.text(x, 7.5, desc, ha="center", va="bottom", fontsize=10, color=TEXT_SECONDARY)

    # 左端 - 技术派
    ax.text(25, 2.5, "【 技术派主场 】", ha="center", va="center",
            fontsize=14, color=DOWN, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc=BG_SURFACE, ec=DOWN, lw=1.2))

    # 右端 - 基本面派
    ax.text(75, 2.5, "【 基本面派主场 】", ha="center", va="center",
            fontsize=14, color=ACCENT, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc=BG_SURFACE, ec=ACCENT, lw=1.2))

    # 时间刻度数字（指数刻度）
    for i, t in enumerate(["分钟", "日", "周", "月", "季度", "年"]):
        x_pos = 5 + i * (95 / 5)
        ax.scatter(x_pos, 5, s=30, color=TEXT_MUTED, alpha=0.4, zorder=2)
        ax.text(x_pos, 4.0, t, ha="center", fontsize=9, color=TEXT_MUTED)

    # 底部金句
    ax.text(50, 0.5,
            "鸡同鸭讲 = 两个人站在不同的时间尺度上争论同一张 K 线",
            ha="center", fontsize=12, color=UP, style="italic", fontweight="bold")

    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    add_footer(fig, SLUG, 2, TOTAL)
    return save(fig, SLUG, 2)


# ============ 图 3: 融合框架流程图 ============
def fig3_fusion_framework():
    fig, ax = new_fig()
    add_title(fig, "融合框架：基本面选股 + 技术面择时 + 仓位管理")
    add_subtitle(fig, "三层级漏斗：上一步不过关就不要进入下一步，避免「框架很全、纪律为零」")

    # 三层（仅顶部色块标题，body 文本放到色块下方独立行）
    layers = [
        # y_top, y_bot, color, label
        (0.85, 0.78, ACCENT, "第一层 · 基本面"),
        (0.61, 0.54, ACCENT_SUBTLE, "第二层 · 技术面"),
        (0.37, 0.30, UP, "第三层 · 仓位管理"),
    ]
    layer_descriptions = [
        [
            "① ROE 稳定 > 15% + 杜邦拆解",
            "② 资产负债率 < 70% + 质押 < 50%",
            "③ 行业 1~3 年上升通道 + 上下游共振",
        ],
        [
            "① 形态筑底 + 放量突破",
            "② 均线多头 + 缩量回调到 10/20 日线",
            "③ 盈亏比 + 止损纪律（逻辑死 → 无条件离场）",
        ],
        [
            "① 单只仓位 ≤ 20%（避免情绪绑架）",
            "② 持有 3~5 只 + 行业分散",
            "③ 重仓单只 ≠ 价值投资，那叫赌",
        ],
    ]

    for (y_top, y_bot, color, label), descs in zip(layers, layer_descriptions):
        # 顶部色带（高度更窄）
        rect = plt.Rectangle((0.04, y_bot), 0.92, y_top - y_bot,
                              facecolor=color, edgecolor="none",
                              alpha=0.9 if color != ACCENT_SUBTLE else 0.7,
                              transform=ax.transAxes)
        ax.add_patch(rect)
        # 标题居中
        title_color = "white" if color in (ACCENT, UP) else ACCENT
        ax.text(0.5, (y_top + y_bot) / 2, label, ha="center", va="center",
                fontsize=18, fontweight="bold", color=title_color,
                transform=ax.transAxes)
        # 下方三行描述（独立行，不会拥挤）
        for i, d in enumerate(descs):
            ax.text(0.5, y_bot - 0.045 - i * 0.035, d, ha="center", va="top",
                    fontsize=11, color=TEXT_PRIMARY, transform=ax.transAxes)

    # 顶层入口
    ax.text(0.5, 0.95, "准备买入一只股票", ha="center", va="top",
            fontsize=12, color=TEXT_MUTED, style="italic", transform=ax.transAxes)

    # 顶部到第一层的向下箭头
    ax.annotate("", xy=(0.5, 0.86), xytext=(0.5, 0.93),
                arrowprops=dict(arrowstyle="->", color=TEXT_PRIMARY, lw=1.5),
                transform=ax.transAxes)

    # 层与层之间的箭头（向下）
    for y in [0.77, 0.53]:
        ax.annotate("", xy=(0.5, y - 0.01), xytext=(0.5, y + 0.05),
                    arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.5),
                    transform=ax.transAxes)

    # 底部心法
    ax.text(0.5, 0.10,
            "知行合一的核心 = 门槛不在方法，而在能否严格遵守",
            ha="center", fontsize=12, color=UP, fontweight="bold",
            transform=ax.transAxes)
    ax.text(0.5, 0.05,
            "先基本面防雷 → 再技术面择时 → 最后仓位管理锁边界",
            ha="center", fontsize=11, color=TEXT_SECONDARY,
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
    paths.append(fig1_two_schools_compare())
    paths.append(fig2_time_axis())
    paths.append(fig3_fusion_framework())
    for p in paths:
        print(f"  ✓ {p}")
    print(f"\nGenerated {len(paths)} images for {SLUG}")
