#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

APP_NAME="YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL"

echo "[Build] Installing dependencies..."
python3 -m pip install -r requirements.txt -r requirements-build.txt

echo "[Build] Running PyInstaller..."
python3 -m PyInstaller app.spec --noconfirm

mkdir -p "release/linux"
cp -f "dist/${APP_NAME}" "release/linux/${APP_NAME}"
chmod +x "release/linux/${APP_NAME}"

echo
echo "Done: release/linux/${APP_NAME}"
