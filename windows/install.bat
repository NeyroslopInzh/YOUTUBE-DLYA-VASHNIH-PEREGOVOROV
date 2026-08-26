@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM Install YVP Clipper (app + extension + yvp://) — dev / manual fallback

set "INSTALL_DIR=%LOCALAPPDATA%\YVPClipper"
set "EXE_NAME=YVPClipper.exe"

if not "%~1"=="" (
  set "SOURCE=%~1"
) else (
  set "SOURCE="
  for %%F in ("%~dp0..\dist\windows\*.exe") do (
    echo %%~nxF | findstr /i "Setup" >nul
    if errorlevel 1 set "SOURCE=%%~fF"
  )
)

if not defined SOURCE (
  echo EXE not found. Build first: windows\build.bat
  exit /b 1
)

echo Installing from: %SOURCE%
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
copy /Y "%SOURCE%" "%INSTALL_DIR%\%EXE_NAME%" >nul

echo Copying extension...
if not exist "%INSTALL_DIR%\extension" mkdir "%INSTALL_DIR%\extension"
xcopy /E /I /Y "%~dp0..\extension\*" "%INSTALL_DIR%\extension\" >nul

echo 1>"%INSTALL_DIR%\.yvp_installed"

set "CMD=\"%INSTALL_DIR%\%EXE_NAME%\" \"%%1\""
reg add "HKCU\Software\Classes\yvp" /ve /d "URL:YVP Clipper Protocol" /f >nul
reg add "HKCU\Software\Classes\yvp" /v "URL Protocol" /d "" /f >nul
reg add "HKCU\Software\Classes\yvp\DefaultIcon" /ve /d "%INSTALL_DIR%\%EXE_NAME%,0" /f >nul
reg add "HKCU\Software\Classes\yvp\shell\open\command" /ve /d "%CMD%" /f >nul

echo OK: %INSTALL_DIR%
echo Extension: %INSTALL_DIR%\extension
echo Run the app once for extension setup instructions.
