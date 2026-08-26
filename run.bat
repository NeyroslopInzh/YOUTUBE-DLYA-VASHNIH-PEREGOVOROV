@echo off
chcp 65001 >nul
cd /d "%~dp0"

set APP_NAME=YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL

echo [%APP_NAME%] Installing dependencies...
py -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo [%APP_NAME%] Starting...
py main.py
