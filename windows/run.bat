@echo off
chcp 65001 >nul
cd /d "%~dp0\.."

echo [Windows] Installing dependencies...
py -m pip install -r src/requirements.txt -r windows/requirements.txt -q
if errorlevel 1 exit /b 1

echo [Windows] Starting...
py src\main.py
