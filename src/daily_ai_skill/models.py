from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class ReportItem:
    title: str
    summary: str
    link: str
    source: str
    published: datetime | None = None
    score: int | None = None
    image_path: str | None = None


@dataclass(slots=True)
class DailyReport:
    date_str: str
    highlights: list[str]
    news_items: list[ReportItem]
    repo_items: list[ReportItem]
    paper_items: list[ReportItem]
