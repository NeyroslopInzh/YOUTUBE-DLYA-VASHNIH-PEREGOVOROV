#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

py scripts/sync_extension_manifest.py
py scripts/generate_app_icon.py 2>/dev/null || true
bash linux/build.sh

STAGE="$ROOT/dist/linux-installer"
rm -rf "$STAGE"
mkdir -p "$STAGE"

APP="YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL"
cp "dist/linux/$APP" "$STAGE/"
cp -r extension "$STAGE/"
cp linux/install.sh "$STAGE/"
chmod +x "$STAGE/install.sh" "$STAGE/$APP"

tar -czf "dist/YVPClipper-linux-installer.tar.gz" -C "$STAGE" .
echo "Wrote dist/YVPClipper-linux-installer.tar.gz"
