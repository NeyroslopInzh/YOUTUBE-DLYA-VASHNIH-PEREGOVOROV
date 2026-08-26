@echo off
chcp 65001 >nul
cd /d "%~dp0\..\.."
echo [Companion] Starting on http://127.0.0.1:8765
py extension\companion\server.py
pause
