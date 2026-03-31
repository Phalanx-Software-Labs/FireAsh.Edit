@echo off
set "HERE=%~dp0"
if exist "%HERE%dist\FireAsh.Edit.exe" (
  start "" "%HERE%dist\FireAsh.Edit.exe"
  exit /b 0
)
cd /d "%HERE%"
where py >nul 2>&1 && py -3 fireash_edit_ui.py && exit /b 0
where python >nul 2>&1 && python fireash_edit_ui.py && exit /b 0
echo Python 3 was not found. Install from https://www.python.org/downloads/
echo Or run build_installer.ps1 to create dist\FireAsh.Edit.exe (no Python needed to run).
pause
exit /b 1
