@echo off
setlocal
cd /d "%~dp0"
echo.
echo Master Logo/Icon Library Online Updater
echo =======================================
echo This ADDS/UPDATES icons. Existing unrelated files are NOT deleted.
echo Internet connection is required.
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Online_Master_Logo_Updater.ps1"
echo.
pause
