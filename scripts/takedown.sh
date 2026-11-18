#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Uso: /scripts/takedown.sh <slug-app> [motivo]"
  exit 2
fi

SLUG="$1"
REASON="${2:-compliance}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

python3 "${SCRIPT_DIR}/takedown.py" "${SLUG}" --reason "${REASON}" --no-commit

cd "${ROOT_DIR}"
git add content/apps data/takedown_blocklist.json
git commit -m "Remove: [${SLUG}] per compliance" || echo "Nessuna modifica da committare"

if [ -f "${ROOT_DIR}/package.json" ]; then
  npm run build
fi

echo "Rimozione completata per ${SLUG}."
