/**
 * 持仓规划（planning）文档列表。
 *
 * 与笔记（notes）一样，文档正文是自包含的独立 HTML，存放在
 * public/planning/ 下，命名规则：
 *   猪周期-投资计划-2026-10-04.html
 *   └──┬──┘ └────┬─────┘ └──┬──┘
 *      分组      标题       基准日
 *
 * 约定：
 *   - 「分组」可省略。省略时（如 `深套30%解套-2026-09-30.html`）整段都算标题，
 *     归入「未分类」组——标题里带连字符不受影响，因为只按**第一个**连字符切分。
 *   - 基准日可省略，省略时排在最前。
 *   - 同一分组同一主题的不同基准日会并存，索引页因此天然成为「历史版本列表」。
 *
 * 往 public/planning/ 丢一个符合命名的 HTML 即可，索引页自动收录，
 * 不需要改任何配置。
 */
import { readdirSync } from 'node:fs';
import { join } from 'node:path';

export interface PlanDoc {
  /** 完整 slug（不含 .html），用于拼接 /planning/{slug} */
  slug: string;
  /** 标题（不含分组前缀与日期后缀） */
  title: string;
  /** 分组名，如「猪周期」；文件名无分组前缀时为空串 */
  group: string;
  /** 基准日，如 "2026-09-30"；文件名无日期后缀时为空串 */
  date: string;
  /** 排序用时间戳，文件名无日期时为 0 */
  order: number;
}

export interface PlanGroup {
  /** 分组名；无分组的文档归入「未分类」 */
  name: string;
  /** 该分组的文档，已按基准日倒序 */
  docs: PlanDoc[];
}

/** 归入未分组文档的分组名 */
export const UNCATEGORIZED = '未分类';

/** 文件名末尾的 `-YYYY-MM-DD` */
const DATE_SUFFIX = /-(\d{4}-\d{2}-\d{2})$/;

function getPlanningDir(): string {
  return join(process.cwd(), 'public', 'planning');
}

let cached: { groups: PlanGroup[]; all: PlanDoc[] } | null = null;

function parseName(filename: string): PlanDoc {
  const slug = filename.replace(/\.html$/, '');
  const m = DATE_SUFFIX.exec(slug);
  const base = m ? slug.slice(0, m.index) : slug;
  const date = m ? m[1] : '';
  // 只按第一个连字符切分，标题内部可以继续带连字符
  const cut = base.indexOf('-');
  return {
    slug,
    title: cut > 0 ? base.slice(cut + 1) : base,
    group: cut > 0 ? base.slice(0, cut) : '',
    date,
    order: date ? Date.parse(`${date}T00:00:00Z`) || 0 : 0,
  };
}

/**
 * 扫描 public/planning/，按分组归类，组内按基准日倒序（新的在前）。
 * 组与组之间按「组内最新文档的基准日」倒序，保证多次构建输出稳定。
 */
export function getPlans(): { groups: PlanGroup[]; all: PlanDoc[] } {
  if (cached) return cached;

  const files = readdirSync(getPlanningDir())
    .filter((f) => f.endsWith('.html'))
    .sort();

  const all: PlanDoc[] = files
    .map(parseName)
    .sort((a, b) => b.order - a.order || a.slug.localeCompare(b.slug));

  const byGroup = new Map<string, PlanDoc[]>();
  for (const doc of all) {
    const key = doc.group || UNCATEGORIZED;
    if (!byGroup.has(key)) byGroup.set(key, []);
    byGroup.get(key)!.push(doc);
  }

  const groups: PlanGroup[] = [...byGroup.entries()]
    .map(([name, docs]) => ({ name, docs }))
    // 组间：看组内最新的一条；同日期再按组名正序
    .sort(
      (a, b) =>
        b.docs[0].order - a.docs[0].order || a.name.localeCompare(b.name, 'zh')
    );

  cached = { groups, all };
  return cached;
}
