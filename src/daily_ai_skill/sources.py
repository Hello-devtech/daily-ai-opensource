from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any

import feedparser
import httpx
from tenacity import retry, stop_after_attempt, wait_fixed

from .models import ReportItem

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"
ARXIV_RSS = "https://rss.arxiv.org/rss/cs.AI"
HF_BLOG_RSS = "https://huggingface.co/blog/feed.xml"


class SourceClient:
    def __init__(self, timeout: float = 15.0) -> None:
        self._http = httpx.Client(timeout=timeout, headers={"User-Agent": "daily-ai-report/0.1"})

    def close(self) -> None:
        self._http.close()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def _get(self, url: str, *, params: dict[str, Any] | None = None) -> httpx.Response:
        response = self._http.get(url, params=params)
        response.raise_for_status()
        return response

    def fetch_github_trending(self, limit: int = 8) -> list[ReportItem]:
        one_week_ago = datetime.now(timezone.utc).date().toordinal() - 7
        created_from = datetime.fromordinal(one_week_ago).strftime("%Y-%m-%d")
        params = {
            "q": f"topic:ai created:>{created_from}",
            "sort": "stars",
            "order": "desc",
            "per_page": limit,
        }
        data = self._get(GITHUB_SEARCH_URL, params=params).json()
        items: list[ReportItem] = []
        for repo in data.get("items", []):
            items.append(
                ReportItem(
                    title=repo["full_name"],
                    summary=repo.get("description") or "No description.",
                    link=repo["html_url"],
                    source="GitHub",
                    published=_parse_datetime(repo.get("created_at")),
                    score=repo.get("stargazers_count"),
                )
            )
        return items

    def fetch_rss_items(self, url: str, source: str, limit: int = 6) -> list[ReportItem]:
        parsed = feedparser.parse(url)
        items: list[ReportItem] = []
        for entry in parsed.entries[:limit]:
            items.append(
                ReportItem(
                    title=entry.get("title", "Untitled"),
                    summary=_clean_summary(entry.get("summary", "")),
                    link=entry.get("link", ""),
                    source=source,
                    published=_parse_datetime(entry.get("published")),
                )
            )
        return items


def _clean_summary(summary: str, max_length: int = 240) -> str:
    summary = " ".join(summary.replace("\n", " ").split())
    if len(summary) <= max_length:
        return summary
    return summary[: max_length - 3] + "..."


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        if "T" in value:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsedate_to_datetime(value)
    except (ValueError, TypeError):
        return None
