#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "[Build] Installing dependencies..."
python3 -m pip install -r requirements.txt -r requirements-build.txt

echo "[Build] Running PyInstaller..."
python3 -m PyInstaller "YouTube Clipper.spec" --noconfirm

mkdir -p "release/linux"
cp -f "dist/YouTube Clipper" "release/linux/youtube-clipper"

chmod +x "release/linux/youtube-clipper"

echo
echo "Done: release/linux/youtube-clipper"
