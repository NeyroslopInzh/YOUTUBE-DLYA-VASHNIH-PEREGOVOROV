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

echo "[Build Linux] Installing dependencies..."
python -m pip install -U pip
python -m pip install -r src/requirements.txt -r linux/requirements.txt -r linux/requirements-build.txt

if ! python -c "import tkinter" >/dev/null 2>&1; then
  echo "ERROR: Python cannot import tkinter (libtk missing)." >&2
  echo "  Arch:   sudo pacman -S tk" >&2
  echo "  Debian: sudo apt install python3-tk" >&2
  exit 1
fi

echo "[Build Linux] PyInstaller..."
python -m PyInstaller linux/app.spec --noconfirm --distpath dist/linux --workpath build/linux

APP_NAME="YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL"
chmod +x "dist/linux/${APP_NAME}"
echo "Done: dist/linux/${APP_NAME}"
