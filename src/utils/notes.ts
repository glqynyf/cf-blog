/**
 * 笔记（notes）数据读取工具。
 *
 * 笔记正文是 115 个独立 HTML 文件，存放在 public/notes/ 下，命名规则：
 *   S00-01-为什么散户总在市场里亏钱.html
 *   └──┬─┘ └┬┘ └──────────────┬─────────────┘
 *    章节   序号                标题
 *
 * 笔记不经过 Astro 处理（不读 frontmatter、不做 Markdown 转换），
 * Astro 只负责：扫描文件名生成目录页（/notes/），并支持 ?stage=S00 单章筛选。
 */
import { readdirSync } from 'node:fs';
import { join } from 'node:path';

export interface Note {
  /** 完整 slug（不含 .html），用于拼接 /notes/{slug} */
  slug: string;
  /** 章节 ID，如 "S00" */
  stage: string;
  /** 章节内序号，如 "01" */
  num: string;
  /** 章节内排序序号（数字），用于稳定排序 */
  order: number;
  /** 笔记标题（从文件名解析，去掉 S00-01- 前缀） */
  title: string;
}

export interface Stage {
  /** 章节 ID，如 "S00" */
  id: string;
  /** 章节显示标题 */
  title: string;
  /** 该章节的笔记列表（已按序号排序） */
  notes: Note[];
}

/** 章节标题映射（按文件名 SXX 前缀匹配） */
const STAGE_TITLES: Record<string, string> = {
  S00: '认知重塑 · 破除散户思维',
  S01: '心态纪律 · 交易心理与情绪管理',
  S02: 'K线基础 · 单根与组合形态',
  S03: '量价关系 · 量是因价是果',
  S04: '均线趋势 · 趋势线与周期选择',
  S05: '技术指标 · MA / KDJ / MACD / RSI / BOLL',
  S06: '形态学 · 双重顶底与底部反转',
  S07: '左侧右侧 · 进出场时机与分时盘口',
  S08: '止盈止损 · 卖出判断标准',
  S09: '仓位管理 · 532 法则与凯利公式',
  S10: '选股方法 · 自上而下与自下而上',
  S11: '分红回购 · 除权除息与税务',
  S12: '筹码主力 · 资金面与涨跌停规则',
  S13: '跨市场配置 · A 股 / 美股 / 黄金 / 债券',
};

function getNotesDir(): string {
  return join(process.cwd(), 'public', 'notes');
}

let cached: { stages: Stage[]; all: Note[] } | null = null;

/** 扫描 public/notes/ 并按章节分组。同一次构建内只读一次磁盘。 */
export function getAllNotes(): { stages: Stage[]; all: Note[] } {
  if (cached) return cached;

  const files = readdirSync(getNotesDir())
    .filter((f) => f.endsWith('.html'))
    .sort();

  const all: Note[] = files.map((filename) => {
    const stem = filename.replace(/\.html$/, '');
    const stage = stem.slice(0, 3);
    const num = stem.slice(4, 6);
    return {
      slug: stem,
      stage,
      num,
      order: Number.parseInt(num, 10) || 0,
      title: stem.replace(/^S\d{2}-\d{2}-/, ''),
    };
  });

  const byStage = new Map<string, Note[]>();
  for (const note of all) {
    if (!byStage.has(note.stage)) byStage.set(note.stage, []);
    byStage.get(note.stage)!.push(note);
  }

  const stages: Stage[] = [...byStage.keys()]
    .sort()
    .map((id) => ({
      id,
      title: STAGE_TITLES[id] ?? id,
      notes: byStage.get(id)!.sort((a, b) => a.order - b.order),
    }));

  cached = { stages, all };
  return cached;
}
