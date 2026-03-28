from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .models import DailyReport, ReportItem
from .sources import ARXIV_RSS, HF_BLOG_RSS, SourceClient


class DailyReportGenerator:
    def __init__(self, template_dir: str = "templates") -> None:
        self.client = SourceClient()
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(disabled_extensions=("md",)),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def build_report(self, date_str: str | None = None) -> DailyReport:
        if date_str is None:
            date_str = datetime.now(timezone.utc).date().isoformat()

        repo_items = self.client.fetch_github_trending(limit=10)
        news_items = self.client.fetch_rss_items(HF_BLOG_RSS, "Hugging Face", limit=6)
        paper_items = self.client.fetch_rss_items(ARXIV_RSS, "arXiv cs.AI", limit=6)

        highlights = self._make_highlights(news_items, repo_items, paper_items)

        return DailyReport(
            date_str=date_str,
            highlights=highlights,
            news_items=news_items,
            repo_items=repo_items,
            paper_items=paper_items,
        )

    def render_markdown(self, report: DailyReport) -> str:
        template = self.env.get_template("daily_report.md.j2")
        return template.render(report=report)

    def save_markdown(self, output_path: str, content: str) -> Path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def close(self) -> None:
        self.client.close()

    @staticmethod
    def _make_highlights(
        news_items: list[ReportItem],
        repo_items: list[ReportItem],
        paper_items: list[ReportItem],
    ) -> list[str]:
        highlights: list[str] = []
        if repo_items:
            top_repo = repo_items[0]
            highlights.append(
                f"GitHub 热门项目：{top_repo.title}（⭐ {top_repo.score or 0}）"
            )
        if news_items:
            highlights.append(f"产业动态：{news_items[0].title}")
        if paper_items:
            highlights.append(f"研究焦点：{paper_items[0].title}")
        return highlights
