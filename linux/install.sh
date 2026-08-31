#!/usr/bin/env bash
# Linux installer — YVP Clipper + browser extension folder + yvp://
set -euo pipefail

APP_NAME="YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/yvp-clipper"
BIN_DIR="${HOME}/.local/bin"
BIN_NAME="yvp-clipper"
DESKTOP_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
MIME_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/mime/packages"
CACHE_TMP_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/yvp-clipper/tmp"

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
    ru:steps) echo "Chrome / Chromium / Opera / Edge: режим разработчика → Load unpacked → эта папка." ;;
    ru:as_root) echo "Не запускай установщик от root — yvp:// пропишется не тому пользователю." ;;
    en:title) echo "YVP Clipper — install" ;;
    en:need_ffmpeg) echo "ffmpeg required. Arch: sudo pacman -S ffmpeg · Debian/Ubuntu: sudo apt install ffmpeg" ;;
    en:copying) echo "Installing to $INSTALL_DIR" ;;
    en:done) echo "Done. Run: $BIN_NAME or yvp://start" ;;
    en:extension) echo "Extension (Load unpacked): $INSTALL_DIR/extension" ;;
    en:steps) echo "Chrome / Chromium / Opera / Edge: Developer mode → Load unpacked → that folder." ;;
    en:as_root) echo "Do not run as root — yvp:// would register for the wrong user." ;;
    he:title) echo "YVP Clipper — התקנה" ;;
    he:need_ffmpeg) echo "נדרש ffmpeg. Arch: sudo pacman -S ffmpeg · Debian/Ubuntu: sudo apt install ffmpeg" ;;
    he:copying) echo "מתקין ל- $INSTALL_DIR" ;;
    he:done) echo "הושלם. הרצה: $BIN_NAME או yvp://start" ;;
    he:extension) echo "תוסף (Load unpacked): $INSTALL_DIR/extension" ;;
    he:steps) echo "Chrome / Chromium / Opera / Edge: מצב מפתח → Load unpacked → תיקייה זו." ;;
    he:as_root) echo "אל תריץ כ-root." ;;
    hi:title) echo "YVP Clipper — install" ;;
    hi:need_ffmpeg) echo "ffmpeg चाहिए. Arch: sudo pacman -S ffmpeg · Debian/Ubuntu: sudo apt install ffmpeg" ;;
    hi:copying) echo "Install: $INSTALL_DIR" ;;
    hi:done) echo "पूर्ण. चलाएँ: $BIN_NAME या yvp://start" ;;
    hi:extension) echo "Extension (Load unpacked): $INSTALL_DIR/extension" ;;
    hi:steps) echo "Chrome / Chromium / Opera / Edge: Developer mode → Load unpacked → यह folder." ;;
    hi:as_root) echo "root से मत चलाओ।" ;;
    uz:title) echo "YVP Clipper — o'rnatish" ;;
    uz:need_ffmpeg) echo "ffmpeg kerak. Arch: sudo pacman -S ffmpeg · Debian/Ubuntu: sudo apt install ffmpeg" ;;
    uz:copying) echo "O'rnatilmoqda: $INSTALL_DIR" ;;
    uz:done) echo "Tayyor. Ishga tushirish: $BIN_NAME yoki yvp://start" ;;
    uz:extension) echo "Kengaytma (Load unpacked): $INSTALL_DIR/extension" ;;
    uz:steps) echo "Chrome / Chromium / Opera / Edge: Dasturchi rejimi → Load unpacked → shu papka." ;;
    uz:as_root) echo "root ostida ishlatmang." ;;
    *) echo "$1" ;;
  esac
}

echo "$(msg title)"

if [[ "$(id -u)" -eq 0 ]]; then
  echo "$(msg as_root)" >&2
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "$(msg need_ffmpeg)" >&2
  exit 1
fi

# Tarball: binary + extension/ next to install.sh
# Repo: linux/install.sh, dist/linux/<bin>, extension/ at repo root
ROOT=""
if [[ -f "$SCRIPT_DIR/$APP_NAME" && -d "$SCRIPT_DIR/extension" ]]; then
  ROOT="$SCRIPT_DIR"
elif [[ -f "$SCRIPT_DIR/dist/linux/$APP_NAME" && -d "$SCRIPT_DIR/extension" ]]; then
  ROOT="$SCRIPT_DIR"
elif [[ -f "$SCRIPT_DIR/../dist/linux/$APP_NAME" && -d "$SCRIPT_DIR/../extension" ]]; then
  ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
elif [[ -f "$SCRIPT_DIR/../$APP_NAME" && -d "$SCRIPT_DIR/../extension" ]]; then
  ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

SRC_BIN=""
if [[ -n "$ROOT" && -f "$ROOT/dist/linux/$APP_NAME" ]]; then
  SRC_BIN="$ROOT/dist/linux/$APP_NAME"
elif [[ -n "$ROOT" && -f "$ROOT/$APP_NAME" ]]; then
  SRC_BIN="$ROOT/$APP_NAME"
else
  echo "Binary not found. Run linux/build.sh first or run this script from the release tarball." >&2
  exit 1
fi

echo "$(msg copying)"
mkdir -p "$INSTALL_DIR/extension" "$BIN_DIR" "$DESKTOP_DIR" "$MIME_DIR" "$CACHE_TMP_DIR"

install -m755 "$SRC_BIN" "$INSTALL_DIR/$APP_NAME"

WRAPPER="$INSTALL_DIR/$BIN_NAME-run"
cat >"$WRAPPER" <<EOF
#!/usr/bin/env bash
set -euo pipefail
# PyInstaller onefile extracts under TMPDIR. Keep it off /tmp.
export TMPDIR="\${XDG_CACHE_HOME:-\$HOME/.cache}/yvp-clipper/tmp"
export TEMP="\$TMPDIR"
export TMP="\$TMPDIR"
mkdir -p "\$TMPDIR"
exec "$INSTALL_DIR/$APP_NAME" "\$@"
EOF
chmod 755 "$WRAPPER"

ln -sfn "$WRAPPER" "$BIN_DIR/$BIN_NAME"
if [[ -d "${HOME}/bin" ]]; then
  ln -sfn "$WRAPPER" "${HOME}/bin/$BIN_NAME"
fi

if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete "$ROOT/extension/" "$INSTALL_DIR/extension/"
else
  rm -rf "$INSTALL_DIR/extension"
  mkdir -p "$INSTALL_DIR/extension"
  cp -a "$ROOT/extension/." "$INSTALL_DIR/extension/"
fi

echo '1' >"$INSTALL_DIR/.yvp_installed"

DESKTOP_FILE="$DESKTOP_DIR/yvp-clipper.desktop"
cat >"$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=$APP_NAME
GenericName=YouTube segment clipper
Comment=YouTube clipper + browser extension bridge
Exec=$WRAPPER %u
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
