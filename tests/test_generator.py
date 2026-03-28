from daily_ai_skill.models import DailyReport, ReportItem
from daily_ai_skill.generator import DailyReportGenerator


def test_highlights_generation() -> None:
    report = DailyReport(
        date_str="2026-03-28",
        highlights=[],
        news_items=[ReportItem("n1", "s", "l", "hf")],
        repo_items=[ReportItem("r1", "s", "l", "gh", score=99)],
        paper_items=[ReportItem("p1", "s", "l", "arxiv")],
    )
    g = DailyReportGenerator(template_dir="templates")
    try:
        markdown = g.render_markdown(report)
    finally:
        g.close()
    assert "每日 AI 日报" in markdown
    assert "r1" in markdown
