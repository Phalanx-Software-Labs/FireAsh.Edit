# Regenerate mod.json, inject into Fire Ash Scripts.rxdata, copy to Android assets.
# Run after any change under bag_cheat_mod/ so the next APK build includes the mod.
# Requires: Ruby on PATH.
#
# By default, verifies the game Scripts.rxdata is Pokémon Fire Ash 3.6 Part 2.2 (see scripts/verify_fire_ash_scripts_version.rb).
# Injector defaults to bag_cheat_mod\inject_mod.rb; pass -InjectModRb to use another inject_mod.rb.
param(
    [string]$GameScriptsRxdata = "C:\PSL Phalanx Software Labs\Game Studio\fireash\Data\Scripts.rxdata",
    [string]$InjectModRb = "",
    [switch]$SkipVersionCheck
)

$ErrorActionPreference = "Stop"
# This script lives in <repo>\scripts\
$RepoRoot = Split-Path $PSScriptRoot -Parent
if (-not (Test-Path (Join-Path $RepoRoot "bag_cheat_mod\package_mod.rb"))) {
    Write-Error "Could not find repo root (bag_cheat_mod\package_mod.rb). PSScriptRoot=$PSScriptRoot"
}

$packageMod = Join-Path $RepoRoot "bag_cheat_mod\package_mod.rb"
$modJson = Join-Path $RepoRoot "bag_cheat_mod\mod.json"
if (-not $InjectModRb -or $InjectModRb.Trim().Length -eq 0) {
    $InjectModRb = Join-Path $RepoRoot "bag_cheat_mod\inject_mod.rb"
}
$stagingParent = Join-Path $RepoRoot "_inject_rxdata_staging"
$staging = Join-Path $stagingParent "Data"
$stagingRx = Join-Path $staging "Scripts.rxdata"
$assetOut = Join-Path $RepoRoot "fireash-scripatcher\app\src\main\assets\patched_Scripts.rxdata"

if (-not (Test-Path $GameScriptsRxdata)) {
    Write-Error "Game Scripts.rxdata not found: $GameScriptsRxdata`nPass -GameScriptsRxdata 'path\to\Data\Scripts.rxdata'"
}
if (-not (Test-Path $InjectModRb)) {
    Write-Error "inject_mod.rb not found: $InjectModRb"
}

$verifyRb = Join-Path $RepoRoot "scripts\verify_fire_ash_scripts_version.rb"
if (-not $SkipVersionCheck) {
    Write-Host "==> verify_fire_ash_scripts_version.rb"
    ruby $verifyRb $GameScriptsRxdata
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} else {
    Write-Warning "Skipping Fire Ash version check (-SkipVersionCheck). Unsupported game versions may break."
}

Write-Host "==> package_mod.rb"
ruby $packageMod
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

New-Item -ItemType Directory -Force -Path $staging | Out-Null
Copy-Item -LiteralPath $GameScriptsRxdata -Destination $stagingRx -Force

Write-Host "==> inject_mod.rb"
ruby $InjectModRb $stagingParent $modJson
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Copy-Item -LiteralPath $stagingRx -Destination $assetOut -Force
Write-Host "==> OK: $assetOut"
(Get-Item $assetOut).Length | ForEach-Object { Write-Host "    bytes: $_" }
