@echo off
chcp 65001 >nul
cd /d "%~dp0"

set PROJECT=/mnt/e/videos for VAZHNIE PEREGOVORI program creation
set APP_NAME=YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL

echo [WSL] Building Linux binary via Ubuntu WSL...
wsl bash -lc "set -euo pipefail; cd '%PROJECT%'; sudo apt-get update -qq; sudo apt-get install -y -qq python3 python3-pip python3-tk python3-venv; python3 -m pip install -r requirements.txt -r requirements-build.txt; python3 -m PyInstaller app.spec --noconfirm; mkdir -p release/arch-linux; cp -f \"dist/%APP_NAME%\" \"release/arch-linux/%APP_NAME%\"; chmod +x \"release/arch-linux/%APP_NAME%\"; echo DONE"

if errorlevel 1 (
    echo Build failed.
    pause
    exit /b 1
)

echo.
echo Binary: release\arch-linux\%APP_NAME%
pause
