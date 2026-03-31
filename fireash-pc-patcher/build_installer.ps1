# Build FireAsh.Edit.exe (Python + tkinter bundled via PyInstaller) and optional Inno Setup installer.
# Run from repo root OR from this folder. Requires: Python 3 on PATH.
#
# Before first build, refresh script assets:
#   .\scripts\sync_patched_scripts_to_apk.ps1
#
$ErrorActionPreference = "Stop"
$Here = $PSScriptRoot
Set-Location $Here

Write-Host "==> FireAsh.Edit Windows build (PyInstaller one-file exe + tkinter)" -ForegroundColor Cyan

$assets = Join-Path (Split-Path $Here -Parent) "fireash-scripatcher\app\src\main\assets\patched_Scripts.rxdata"
if (-not (Test-Path $assets)) {
    Write-Error "Missing $assets — run scripts\sync_patched_scripts_to_apk.ps1 from repo root first."
}

$venv = Join-Path $Here ".venv-build"
if (-not (Test-Path $venv)) {
    Write-Host "Creating $venv ..."
    python -m venv $venv
}
$py = Join-Path $venv "Scripts\python.exe"
$pip = Join-Path $venv "Scripts\pip.exe"
& $pip install -q -r (Join-Path $Here "requirements-windows-build.txt")

Write-Host "==> PyInstaller (this may take a minute) ..."
& $py -m PyInstaller --noconfirm (Join-Path $Here "FireAsh.Edit.spec")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$exe = Join-Path $Here "dist\FireAsh.Edit.exe"
if (-not (Test-Path $exe)) {
    Write-Error "Expected output missing: $exe"
}
Write-Host "OK: $exe" -ForegroundColor Green
(Get-Item $exe).Length | ForEach-Object { Write-Host "    bytes: $_" }

$iscc = @(
    "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles}\Inno Setup 6\ISCC.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $iscc) {
    Write-Warning "Inno Setup 6 not found — skipping Setup.exe. Install from https://jrsoftware.org/isdl.php then re-run this script."
    Write-Host "You can ship dist\FireAsh.Edit.exe alone; it already includes Python and tkinter."
    exit 0
}

Write-Host "==> Inno Setup: $iscc" -ForegroundColor Cyan
$iss = Join-Path $Here "installer\FireAsh.Edit.iss"
& $iscc $iss
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$setup = Join-Path $Here "dist-installer\FireAsh.Edit-Setup-1.0.0.exe"
if (Test-Path $setup) {
    Write-Host "OK: $setup" -ForegroundColor Green
}
