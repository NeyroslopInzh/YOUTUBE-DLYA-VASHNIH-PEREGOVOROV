@echo off
setlocal EnableExtensions

cd /d "%~dp0.."

echo [1/3] Sync extension manifest...
py scripts\sync_extension_manifest.py || exit /b 1

echo [2/3] Build app exe...
py -m PyInstaller windows\app.spec --noconfirm --distpath dist\windows --workpath build\windows || exit /b 1

echo [3/3] Build installer (Inno Setup)...
where iscc >nul 2>&1
if errorlevel 1 (
  echo ISCC not found. Install Inno Setup: https://jrsoftware.org/isinfo.php
  echo Or build only the exe from step 2.
  exit /b 1
)
iscc windows\installer.iss || exit /b 1

echo Done: dist\windows\YVPClipper-Setup.exe
