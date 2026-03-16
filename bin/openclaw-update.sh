#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${PROJECT_ROOT}"

CURRENT_BRANCH="$(git branch --show-current)"

if [[ -z "${CURRENT_BRANCH}" ]]; then
  echo "Cannot detect current git branch." >&2
  exit 1
fi

git fetch --tags origin
git pull --ff-only origin "${CURRENT_BRANCH}"

if [[ -x "${PROJECT_ROOT}/.venv/bin/pip" ]]; then
  "${PROJECT_ROOT}/.venv/bin/pip" install -r "${PROJECT_ROOT}/requirements.txt"
fi

echo "Updated branch ${CURRENT_BRANCH} and refreshed dependencies."
