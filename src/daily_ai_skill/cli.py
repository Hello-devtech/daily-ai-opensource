from __future__ import annotations

import argparse

from .generator import DailyReportGenerator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate daily AI report (Markdown).")
    parser.add_argument("--date", help="Report date, format YYYY-MM-DD. Defaults to UTC today.")
    parser.add_argument(
        "--output",
        default="reports/daily_ai_report.md",
        help="Output markdown path. Default: reports/daily_ai_report.md",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    generator = DailyReportGenerator(template_dir="templates")
    try:
        report = generator.build_report(date_str=args.date)
        content = generator.render_markdown(report)
        path = generator.save_markdown(args.output, content)
    finally:
        generator.close()

    print(f"Daily AI report generated: {path}")


if __name__ == "__main__":
    main()
