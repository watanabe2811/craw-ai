from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.parsers.cafef_sections_parser import CafeFSectionsParser


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract important structured sections from a CafeF du-lieu HTML file."
    )
    parser.add_argument("--html-file", required=True, help="Path to the local HTML file.")
    parser.add_argument(
        "--base-url",
        default="https://cafef.vn/du-lieu.chn",
        help="Base URL used to resolve relative links.",
    )
    parser.add_argument("--output-file", help="Optional output JSON file path.")
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    html = Path(args.html_file).read_text(encoding="utf-8")
    result = CafeFSectionsParser().parse(html, args.base_url)
    payload = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output_file:
        Path(args.output_file).write_text(payload, encoding="utf-8")
        print(f"Saved JSON to: {args.output_file}")

    print(payload)


if __name__ == "__main__":
    main()
