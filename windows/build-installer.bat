@echo off
setlocal EnableExtensions

cd /d "%~dp0.."

echo [1/4] Sync extension manifest...
py scripts\sync_extension_manifest.py || exit /b 1

echo [2/4] Generate installer languages...
py scripts\generate_uzbek_isl.py || exit /b 1

echo [3/4] Build app exe...
py -m PyInstaller windows\app.spec --noconfirm --distpath dist\windows --workpath build\windows || exit /b 1

echo [4/4] Build installer (Inno Setup)...
where iscc >nul 2>&1
if errorlevel 1 (
  echo ISCC not found. Install Inno Setup: https://jrsoftware.org/isinfo.php
  echo Or build only the exe from step 2.
  exit /b 1
)
iscc windows\installer.iss || exit /b 1

echo Done: dist\windows\YVPClipper-Setup.exe
