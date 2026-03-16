from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.exporters.report_renderer import render_cafef_report

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render a human-readable report from CafeF sections JSON."
    )
    parser.add_argument(
        "--sections-file",
        required=True,
        help="Path to the structured sections JSON file.",
    )
    parser.add_argument(
        "--output-file",
        help="Optional output text report file path.",
    )
    return parser

def main() -> None:
    args = build_arg_parser().parse_args()
    data = json.loads(Path(args.sections_file).read_text(encoding="utf-8"))
    report = render_cafef_report(data)

    if args.output_file:
        Path(args.output_file).write_text(report, encoding="utf-8")
        print(f"Saved report to: {args.output_file}")

    print(report)


if __name__ == "__main__":
    main()
