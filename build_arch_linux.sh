#!/usr/bin/env bash
# Сборка бинарника на Arch Linux (pacman)
set -euo pipefail

cd "$(dirname "$0")"

APP_NAME="YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL"

echo "[Arch] Checking dependencies..."
missing=()
for pkg in python python-pip tk; do
    if ! pacman -Qi "$pkg" &>/dev/null; then
        missing+=("$pkg")
    fi
done

if ((${#missing[@]})); then
    echo "[Arch] Install: sudo pacman -S --needed ${missing[*]} python-pip"
    sudo pacman -S --needed --noconfirm python python-pip tk
fi

echo "[Arch] Installing Python packages..."
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-build.txt

echo "[Arch] Building with PyInstaller..."
python -m PyInstaller app.spec --noconfirm

mkdir -p "release/arch-linux"
cp -f "dist/${APP_NAME}" "release/arch-linux/${APP_NAME}"
chmod +x "release/arch-linux/${APP_NAME}"

echo
echo "Done: release/arch-linux/${APP_NAME}"
