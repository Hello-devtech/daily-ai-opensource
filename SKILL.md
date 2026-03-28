# Daily AI Report Skill

## Purpose
生成“每日 AI 日报”，聚合：
1. GitHub 热门 AI 开源项目
2. Hugging Face Blog 最新动态
3. arXiv cs.AI 最新论文

## Input
- `date`（可选，`YYYY-MM-DD`）
- `output`（可选，默认 `reports/daily_ai_report.md`）

## Workflow
1. 运行 Python CLI 抓取数据源。
2. 聚合并生成结构化 `DailyReport`。
3. 基于 Jinja2 模板渲染 Markdown。
4. 输出到 `reports/` 目录。

## Run
```bash
python -m daily_ai_skill.cli --date 2026-03-28 --output reports/2026-03-28.md
```

或安装后：
```bash
daily-ai-report --output reports/daily_ai_report.md
```

## Notes
- GitHub API 为匿名访问，速率受限。
- 数据源不可用时请重试。
