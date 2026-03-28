from daily_ai_skill.generator import DailyReportGenerator
from daily_ai_skill.models import DailyReport, ReportItem


def test_markdown_render_with_images() -> None:
    report = DailyReport(
        date_str="2026-03-28",
        highlights=[],
        news_items=[ReportItem("n1", "s", "l", "hf", image_path="reports/images/n1.png")],
        repo_items=[ReportItem("r1", "s", "l", "gh", score=99, image_path="reports/images/r1.png")],
        paper_items=[ReportItem("p1", "s", "l", "arxiv")],
    )
    g = DailyReportGenerator(template_dir="templates")
    try:
        markdown = g.render_markdown(report)
    finally:
        g.close()
    assert "每日 AI 日报" in markdown
    assert "![r1](reports/images/r1.png)" in markdown
