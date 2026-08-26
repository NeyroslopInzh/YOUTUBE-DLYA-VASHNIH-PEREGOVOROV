#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "[Linux] Installing dependencies..."
python3 -m pip install -r src/requirements.txt -r linux/requirements.txt

if ! command -v ffmpeg >/dev/null; then
  echo "ERROR: ffmpeg not found. Install it first."
  echo "  Arch:   sudo pacman -S ffmpeg"
  echo "  Debian: sudo apt install ffmpeg"
  echo "  Fedora: sudo dnf install ffmpeg"
  exit 1
fi

echo "[Linux] Starting..."
python3 src/main.py
