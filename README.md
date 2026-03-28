# Daily AI Open Source (Skill Project)

这是一个 **全 Python 实现** 的 skill 项目，用于自动生成“每日 AI 日报”。

## 项目目标
每日聚合并输出：
- GitHub 热门 AI 开源项目
- Hugging Face Blog 最新动态
- arXiv cs.AI 最新论文

最终生成结构化 Markdown 日报，便于发布到仓库、飞书、Notion 或邮件。

## 项目结构

```text
.
├── SKILL.md
├── pyproject.toml
├── src/
│   └── daily_ai_skill/
│       ├── __init__.py
│       ├── cli.py
│       ├── generator.py
│       ├── models.py
│       └── sources.py
├── templates/
│   └── daily_report.md.j2
├── reports/
└── tests/
    └── test_generator.py
```

## 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## 生成日报

```bash
daily-ai-report --output reports/daily_ai_report.md
```

指定日期：

```bash
daily-ai-report --date 2026-03-28 --output reports/2026-03-28.md
```

## 测试

```bash
pytest
```

## 后续建议（可选）
- 增加 LLM 总结层（对聚合内容做 3~5 条中文摘要）。
- 增加去重与评分机制（按关键词、来源权重、热度）。
- 接入定时任务（GitHub Actions / cron）实现每日自动提交。
