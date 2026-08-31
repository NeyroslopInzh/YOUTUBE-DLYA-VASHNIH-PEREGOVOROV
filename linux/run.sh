#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

export TMPDIR="${XDG_CACHE_HOME:-$HOME/.cache}/yvp-clipper/tmp"
mkdir -p "$TMPDIR"
export TEMP="$TMPDIR"
export TMP="$TMPDIR"

VENV="${YVP_BUILD_VENV:-.build-venv}"
if [[ ! -x "$VENV/bin/python" ]]; then
  python3 -m venv "$VENV"
fi
# shellcheck disable=SC1091
source "$VENV/bin/activate"

echo "[Linux] Installing dependencies..."
python -m pip install -U pip
python -m pip install -r src/requirements.txt -r linux/requirements.txt

if ! command -v ffmpeg >/dev/null; then
  echo "ERROR: ffmpeg not found. Install it first."
  echo "  Arch:   sudo pacman -S ffmpeg"
  echo "  Debian: sudo apt install ffmpeg"
  echo "  Fedora: sudo dnf install ffmpeg"
  exit 1
fi

echo "[Linux] Starting..."
python src/main.py
