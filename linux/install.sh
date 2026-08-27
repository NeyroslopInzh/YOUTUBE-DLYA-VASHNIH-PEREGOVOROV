#!/usr/bin/env bash
# Universal Linux installer — YVP Clipper + browser extension folder + yvp://
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_NAME="YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL"
INSTALL_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/yvp-clipper"
BIN_DIR="${HOME}/.local/bin"
BIN_NAME="yvp-clipper"
DESKTOP_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
MIME_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/mime/packages"

detect_lang() {
  local l="${LANG:-${LC_ALL:-en}}"
  case "${l%%.*}" in
    ru*) echo ru ;;
    he*|iw*) echo he ;;
    hi*) echo hi ;;
    uz*) echo uz ;;
    *) echo en ;;
  esac
}

LANG_CODE="$(detect_lang)"

msg() {
  case "$LANG_CODE:$1" in
    ru:title) echo "YVP Clipper — установка" ;;
    ru:need_ffmpeg) echo "Нужен ffmpeg в PATH. Arch: sudo pacman -S ffmpeg · Debian/Ubuntu: sudo apt install ffmpeg" ;;
    ru:copying) echo "Копирую файлы в $INSTALL_DIR" ;;
    ru:done) echo "Готово. Запуск: $BIN_NAME или yvp://start" ;;
    ru:extension) echo "Расширение (Load unpacked): $INSTALL_DIR/extension" ;;
    ru:steps) echo "Chrome / Opera / Edge: режим разработчика → Load unpacked → эта папка." ;;
    en:title) echo "YVP Clipper — install" ;;
    en:need_ffmpeg) echo "ffmpeg required. Arch: sudo pacman -S ffmpeg · Debian/Ubuntu: sudo apt install ffmpeg" ;;
    en:copying) echo "Installing to $INSTALL_DIR" ;;
    en:done) echo "Done. Run: $BIN_NAME or yvp://start" ;;
    en:extension) echo "Extension (Load unpacked): $INSTALL_DIR/extension" ;;
    en:steps) echo "Chrome / Opera / Edge: Developer mode → Load unpacked → that folder." ;;
    he:title) echo "YVP Clipper — התקנה" ;;
    he:need_ffmpeg) echo "נדרש ffmpeg. Arch: sudo pacman -S ffmpeg · Debian/Ubuntu: sudo apt install ffmpeg" ;;
    he:copying) echo "מתקין ל- $INSTALL_DIR" ;;
    he:done) echo "הושלם. הרצה: $BIN_NAME או yvp://start" ;;
    he:extension) echo "תוסף (Load unpacked): $INSTALL_DIR/extension" ;;
    he:steps) echo "Chrome / Opera / Edge: מצב מפתח → Load unpacked → תיקייה זו." ;;
    hi:title) echo "YVP Clipper — install" ;;
    hi:need_ffmpeg) echo "ffmpeg चाहिए. Arch: sudo pacman -S ffmpeg · Debian/Ubuntu: sudo apt install ffmpeg" ;;
    hi:copying) echo "Install: $INSTALL_DIR" ;;
    hi:done) echo "पूर्ण. चलाएँ: $BIN_NAME या yvp://start" ;;
    hi:extension) echo "Extension (Load unpacked): $INSTALL_DIR/extension" ;;
    hi:steps) echo "Chrome / Opera / Edge: Developer mode → Load unpacked → यह folder." ;;
    uz:title) echo "YVP Clipper — o'rnatish" ;;
    uz:need_ffmpeg) echo "ffmpeg kerak. Arch: sudo pacman -S ffmpeg · Debian/Ubuntu: sudo apt install ffmpeg" ;;
    uz:copying) echo "O'rnatilmoqda: $INSTALL_DIR" ;;
    uz:done) echo "Tayyor. Ishga tushirish: $BIN_NAME yoki yvp://start" ;;
    uz:extension) echo "Kengaytma (Load unpacked): $INSTALL_DIR/extension" ;;
    uz:steps) echo "Chrome / Opera / Edge: Dasturchi rejimi → Load unpacked → shu papka." ;;
    *) echo "$1" ;;
  esac
}

echo "$(msg title)"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "$(msg need_ffmpeg)" >&2
  exit 1
fi

SRC_BIN=""
if [[ -f "$ROOT/dist/linux/$APP_NAME" ]]; then
  SRC_BIN="$ROOT/dist/linux/$APP_NAME"
elif [[ -f "$ROOT/$APP_NAME" ]]; then
  SRC_BIN="$ROOT/$APP_NAME"
else
  echo "Binary not found. Run linux/build.sh first or run this script from the release tarball." >&2
  exit 1
fi

echo "$(msg copying)"
mkdir -p "$INSTALL_DIR/extension" "$BIN_DIR" "$DESKTOP_DIR" "$MIME_DIR"

install -m755 "$SRC_BIN" "$INSTALL_DIR/$APP_NAME"
ln -sf "$INSTALL_DIR/$APP_NAME" "$BIN_DIR/$BIN_NAME"

rsync -a --delete "$ROOT/extension/" "$INSTALL_DIR/extension/"

echo '1' >"$INSTALL_DIR/.yvp_installed"

DESKTOP_FILE="$DESKTOP_DIR/yvp-clipper.desktop"
cat >"$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=$APP_NAME
GenericName=YouTube segment clipper
Comment=YouTube clipper + browser extension bridge
Exec=$BIN_DIR/$BIN_NAME %u
Icon=$INSTALL_DIR/extension/icons/icon48.png
Terminal=false
Categories=AudioVideo;Video;Utility;
MimeType=x-scheme-handler/yvp;
StartupWMClass=yvp-clipper
EOF

MIME_FILE="$MIME_DIR/yvp-clipper.xml"
cat >"$MIME_FILE" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
  <mime-type type="x-scheme-handler/yvp">
    <comment>YVP Clipper URL</comment>
  </mime-type>
</mime-info>
EOF

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$DESKTOP_DIR" || true
fi
if command -v update-mime-database >/dev/null 2>&1; then
  update-mime-database "${XDG_DATA_HOME:-$HOME/.local/share}/mime" || true
fi
if command -v xdg-mime >/dev/null 2>&1; then
  xdg-mime default yvp-clipper.desktop x-scheme-handler/yvp || true
fi

echo
echo "$(msg done)"
echo "$(msg extension)"
echo "$(msg steps)"
