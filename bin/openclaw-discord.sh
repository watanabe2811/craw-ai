#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

URL="${1:-https://cafef.vn/du-lieu.chn}"
OUTPUT_FORMAT="${2:-report}"
MAX_CHARS="${3:-1900}"
SAVE_RAW_FLAG="${4:-}"

PYTHON_BIN="${PROJECT_ROOT}/.venv/bin/python"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "Missing virtualenv Python at ${PYTHON_BIN}. Create .venv and install requirements first." >&2
  exit 1
fi

cd "${PROJECT_ROOT}"

CMD=(
  "${PYTHON_BIN}"
  "main.py"
  "crawl"
  "--url"
  "${URL}"
  "--output-format"
  "${OUTPUT_FORMAT}"
  "--stdout-only"
  "--max-chars"
  "${MAX_CHARS}"
)

if [[ "${SAVE_RAW_FLAG}" == "--save-raw" ]]; then
  CMD+=("--save-raw")
fi

"${CMD[@]}"
