"""
文章内文配图共用配置与工具函数。

设计原则：
- 配色与 OG 图一致（与 src/styles/global.css CSS 变量对齐）
- A 股特色：红涨绿跌
- 中文用 macOS 系统字体（PingFang SC / Hiragino Sans GB）
- 输出 1200x800 PNG（16:10，适合文章内嵌阅读）
"""
from __future__ import annotations
import os
import matplotlib
matplotlib.use("Agg")  # 非 GUI 模式
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rcParams

# ---------- 站点色值（与 OG 脚本、global.css 一致） ----------
BG_PAGE = "#fbfbfa"          # 主背景
BG_SURFACE = "#ffffff"       # 卡片/图表区背景
TEXT_PRIMARY = "#1a1a1a"
TEXT_SECONDARY = "#525252"
TEXT_MUTED = "#737373"
ACCENT = "#0f766e"           # 薄荷绿/teal 强调色
ACCENT_SUBTLE = "#ccfbf1"
UP = "#dc2626"               # 红涨
DOWN = "#16a34a"             # 绿跌
BORDER = "#e7e5e4"
GRID = "#f0eeec"

W, H = 1200, 800  # 标准图尺寸
DPI = 100  # → 像素 1200x800


# ---------- 中文字体 ----------
_CN_FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/Library/Fonts/Songti.ttc",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
]

_CN_FONT_NAME: str | None = None


def setup_chinese_font() -> str:
    """注册中文字体到 matplotlib，返回字体名称。失败时回退到默认。"""
    global _CN_FONT_NAME
    if _CN_FONT_NAME is not None:
        return _CN_FONT_NAME

    for path in _CN_FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                # 直接通过路径注册
                fm.fontManager.addfont(path)
                # 获取字体名
                prop = fm.FontProperties(fname=path)
                name = prop.get_name()
                _CN_FONT_NAME = name
                # 全局 rcParams
                rcParams["font.family"] = [name, "DejaVu Sans", "sans-serif"]
                rcParams["font.sans-serif"] = [name, "DejaVu Sans"]
                rcParams["axes.unicode_minus"] = False
                return name
            except Exception:
                continue

    # 回退
    rcParams["axes.unicode_minus"] = False
    return "DejaVu Sans"


# ---------- 输出 ----------
ROOT = "/Users/uno/Documents/workspace/CF-blog"
OUTPUT_DIR = f"{ROOT}/public/images/posts"


def save(fig, slug: str, idx: int, tight: bool = True) -> str:
    """保存图到 public/images/posts/<slug>-<idx:02d>.png。返回绝对路径。"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = f"{OUTPUT_DIR}/{slug}-{idx:02d}.png"
    if tight:
        fig.savefig(path, dpi=DPI, bbox_inches="tight",
                     facecolor=fig.get_facecolor(), edgecolor="none")
    else:
        fig.savefig(path, dpi=DPI, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    return path


# ---------- 通用画图样式 ----------
def new_fig(aspect: tuple[int, int] = (W, H), bg: str = BG_PAGE):
    """建一张带统一背景色的图。aspect=(w,h) 控制宽高。"""
    fig, ax = plt.subplots(figsize=(aspect[0] / DPI, aspect[1] / DPI), dpi=DPI)
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    return fig, ax


def style_axes(ax, *, hide_spines: tuple = ("top", "right"),
               grid: bool = True, grid_axis: str = "y"):
    """统一坐标轴样式：去上右框线、淡灰网格。"""
    for spine in hide_spines:
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(BORDER)
        ax.spines[spine].set_linewidth(0.8)
    if grid:
        ax.grid(True, axis=grid_axis, color=GRID, linewidth=0.8, alpha=0.9)
        ax.set_axisbelow(True)
    ax.tick_params(colors=TEXT_MUTED, labelsize=10)


def add_title(fig, title: str, *, fontsize: int = 22, y: float = 0.96):
    """图标题（顶部居中）"""
    fig.text(0.5, y, title, ha="center", va="top",
             fontsize=fontsize, fontweight="bold", color=TEXT_PRIMARY)


def add_subtitle(fig, subtitle: str, *, fontsize: int = 13, y: float = 0.91,
                 color: str = TEXT_SECONDARY):
    """副标题（图标题下方）"""
    fig.text(0.5, y, subtitle, ha="center", va="top",
             fontsize=fontsize, color=color, style="italic")


def add_footer(fig, slug: str, idx: int, total: int):
    """页脚水印"""
    fig.text(0.99, 0.02,
             f"盘面机记 · stock-blog.duckuno.com  |  {slug}  ({idx}/{total})",
             ha="right", va="bottom", fontsize=9, color=TEXT_MUTED)
