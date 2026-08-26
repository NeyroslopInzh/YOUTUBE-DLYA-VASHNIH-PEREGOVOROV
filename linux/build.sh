#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "[Build Linux] Installing dependencies..."
python3 -m pip install -r src/requirements.txt -r linux/requirements.txt -r linux/requirements-build.txt

echo "[Build Linux] PyInstaller..."
python3 -m PyInstaller linux/app.spec --noconfirm --distpath dist/linux --workpath build/linux

APP_NAME="YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL"
chmod +x "dist/linux/${APP_NAME}"
echo "Done: dist/linux/${APP_NAME}"
