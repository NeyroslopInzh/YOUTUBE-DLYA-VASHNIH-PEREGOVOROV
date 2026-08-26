@echo off
chcp 65001 >nul
cd /d "%~dp0"

set APP_NAME=YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL

echo [Build] Installing dependencies...
py -m pip install -r requirements.txt -r requirements-build.txt -q
if errorlevel 1 (
    echo Build failed: pip install error.
    pause
    exit /b 1
)

echo [Build] Running PyInstaller...
py -m PyInstaller app.spec --noconfirm
if errorlevel 1 (
    echo Build failed: PyInstaller error.
    pause
    exit /b 1
)

if not exist "release\windows" mkdir "release\windows"
copy /Y "dist\%APP_NAME%.exe" "release\windows\%APP_NAME%.exe" >nul
copy /Y "dist\%APP_NAME%.exe" "%APP_NAME%.exe" >nul

echo.
echo Done: release\windows\%APP_NAME%.exe
pause
