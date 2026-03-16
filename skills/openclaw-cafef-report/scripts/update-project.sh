#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${OPENCLAW_CRAWLER_REPO:-$(cd "${SCRIPT_DIR}/../../.." && pwd)}"

exec "${PROJECT_ROOT}/bin/openclaw-update.sh" "${@}"
