@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo [YouTube Clipper] Installing dependencies...
py -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo [YouTube Clipper] Starting...
py main.py
