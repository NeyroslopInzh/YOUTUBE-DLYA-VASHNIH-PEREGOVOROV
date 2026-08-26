@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo [Build] Installing dependencies...
py -m pip install -r requirements.txt -r requirements-build.txt -q
if errorlevel 1 (
    echo Build failed: pip install error.
    pause
    exit /b 1
)

echo [Build] Running PyInstaller...
py -m PyInstaller "YouTube Clipper.spec" --noconfirm
if errorlevel 1 (
    echo Build failed: PyInstaller error.
    pause
    exit /b 1
)

if not exist "release\windows" mkdir "release\windows"
copy /Y "dist\YouTube Clipper.exe" "release\windows\YouTube Clipper.exe" >nul
copy /Y "dist\YouTube Clipper.exe" "YouTube Clipper.exe" >nul

echo.
echo Done: release\windows\YouTube Clipper.exe
pause
