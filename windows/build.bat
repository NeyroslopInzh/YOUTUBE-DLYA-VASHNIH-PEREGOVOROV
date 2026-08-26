@echo off
chcp 65001 >nul
cd /d "%~dp0\.."

echo [Build Windows] Installing dependencies...
py -m pip install -r src/requirements.txt -r windows/requirements.txt -r windows/requirements-build.txt -q
if errorlevel 1 exit /b 1

echo [Build Windows] PyInstaller...
py -m PyInstaller windows\app.spec --noconfirm --distpath dist\windows --workpath build\windows
if errorlevel 1 exit /b 1

echo Done: dist\windows\
pause
