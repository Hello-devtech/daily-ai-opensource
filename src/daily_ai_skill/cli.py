from __future__ import annotations

import argparse

from .generator import DailyReportGenerator
from .image_generation import ImageGenConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate daily AI report (Markdown).")
    parser.add_argument("--date", help="Report date, format YYYY-MM-DD. Defaults to UTC today.")
    parser.add_argument(
        "--output",
        default="reports/daily_ai_report.md",
        help="Output markdown path. Default: reports/daily_ai_report.md",
    )
    parser.add_argument(
        "--image-provider",
        default="none",
        choices=["none", "openai", "custom"],
        help="Image generation provider.",
    )
    parser.add_argument("--image-model", default="gpt-image-1", help="Image model name.")
    parser.add_argument(
        "--image-api-base",
        default="https://api.openai.com",
        help="Image API base url, e.g. https://api.openai.com",
    )
    parser.add_argument(
        "--image-endpoint",
        default="/v1/images/generations",
        help="Image generation endpoint path.",
    )
    parser.add_argument(
        "--image-api-key-env",
        default="OPENAI_API_KEY",
        help="Environment variable that stores API key.",
    )
    parser.add_argument(
        "--image-output-dir",
        default="reports/images",
        help="Directory for generated images.",
    )
    parser.add_argument(
        "--max-images",
        type=int,
        default=6,
        help="Max number of report items to generate images for.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    image_config = ImageGenConfig(
        provider=args.image_provider,
        model=args.image_model,
        output_dir=args.image_output_dir,
        api_base=args.image_api_base,
        api_key_env=args.image_api_key_env,
        endpoint=args.image_endpoint,
    )
    generator = DailyReportGenerator(template_dir="templates", image_config=image_config, max_images=args.max_images)
    try:
        report = generator.build_report(date_str=args.date)
        content = generator.render_markdown(report)
        path = generator.save_markdown(args.output, content)
    finally:
        generator.close()

    print(f"Daily AI report generated: {path}")


if __name__ == "__main__":
    main()
