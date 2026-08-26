#!/usr/bin/env bash
# Pack Chromium extension for release (zip + tar.gz, Load unpacked).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON="${PYTHON:-python3}"
"$PYTHON" scripts/sync_extension_manifest.py
"$PYTHON" extension/icons/generate_icons.py

PACK_NAME="YVPClipper-extension"
STAGE="$ROOT/dist/$PACK_NAME"
rm -rf "$STAGE"
mkdir -p "$STAGE"

rsync -a extension/ "$STAGE/" --exclude='icons/generate_icons.py'

mkdir -p dist
rm -f "dist/$PACK_NAME.zip" "dist/$PACK_NAME.tar.gz"
(
  cd dist
  zip -r "$PACK_NAME.zip" "$PACK_NAME"
  tar -czf "$PACK_NAME.tar.gz" "$PACK_NAME"
)

echo "Wrote dist/$PACK_NAME.zip"
echo "Wrote dist/$PACK_NAME.tar.gz"
