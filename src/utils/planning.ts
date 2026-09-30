/**
 * 持仓规划（planning）文档列表。
 *
 * 与笔记（notes）一样，文档正文是自包含的独立 HTML，存放在
 * public/planning/ 下，命名规则：
 *   猪周期配置方案-2026-09-30.html
 *   └──────────┬─────────┘ └───┬──┘
 *      主题名称                  基准日
 *
 * 与笔记的差别：
 *   - 不按章节分组，纯粹按日期倒序列出
 *   - 不含 frontmatter，标题也从文件名解析（不读文件内容）
 *   - 同一主题的不同基准日会并存，索引页因此天然成为「历史版本列表」
 *
 * 往 public/planning/ 丢一个符合命名的 HTML 即可，索引页自动收录，
 * 不需要改任何配置。
 */
import { readdirSync } from 'node:fs';
import { join } from 'node:path';

export interface PlanDoc {
  /** 完整 slug（不含 .html），用于拼接 /planning/{slug} */
  slug: string;
  /** 主题名称（去掉日期后缀） */
  title: string;
  /** 基准日，如 "2026-09-30"；文件名无日期后缀时为空串 */
  date: string;
  /** 排序用时间戳，文件名无日期时为 0 */
  order: number;
}

/** 文件名末尾的 `-YYYY-MM-DD` */
const DATE_SUFFIX = /-(\d{4}-\d{2}-\d{2})$/;

function getPlanningDir(): string {
  return join(process.cwd(), 'public', 'planning');
}

let cached: PlanDoc[] | null = null;

/** 扫描 public/planning/，按基准日倒序（新的在前）。同一次构建内只读一次磁盘。 */
export function getPlans(): PlanDoc[] {
  if (cached) return cached;

  const files = readdirSync(getPlanningDir())
    .filter((f) => f.endsWith('.html'))
    .sort();

  cached = files
    .map((filename) => {
      const slug = filename.replace(/\.html$/, '');
      const m = DATE_SUFFIX.exec(slug);
      return {
        slug,
        title: m ? slug.slice(0, m.index) : slug,
        date: m ? m[1] : '',
        order: m ? Date.parse(`${m[1]}T00:00:00Z`) || 0 : 0,
      };
    })
    // 日期倒序；同日按文件名正序，保证多次构建输出稳定
    .sort((a, b) => b.order - a.order || a.slug.localeCompare(b.slug));

  return cached;
}
