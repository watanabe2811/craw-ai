from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.parsers.html_parser import HtmlParser


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract normalized main text from a local HTML file."
    )
    parser.add_argument(
        "--html-file",
        required=True,
        help="Path to the local HTML file.",
    )
    parser.add_argument(
        "--base-url",
        default="https://example.com",
        help="Base URL used to resolve relative links.",
    )
    parser.add_argument(
        "--output-file",
        help="Optional output text file path.",
    )
    parser.add_argument(
        "--mode",
        choices=("main", "full"),
        default="main",
        help="Extraction mode: main content only or nearly all visible body text.",
    )
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()

    html = Path(args.html_file).read_text(encoding="utf-8")
    parser = HtmlParser()
    if args.mode == "full":
        main_text = parser.extract_full_text(html)
    else:
        result = parser.parse(html, args.base_url)
        main_text = result["main_text"] if isinstance(result["main_text"], str) else ""

    if args.output_file:
        Path(args.output_file).write_text(main_text, encoding="utf-8")
        print(f"Saved text to: {args.output_file}")

    print(main_text)


if __name__ == "__main__":
    main()
