# Run AFTER Android Studio: Build -> Build APK(s) -> debug.
# Copies the debug APK to repo root as FireAsh.Edit.apk (what GitHub raw link and Releases use).
$Root = Split-Path $PSScriptRoot -Parent
$Apk = Join-Path $Root "fireash-scripatcher\app\build\outputs\apk\debug\app-debug.apk"
$Out = Join-Path $Root "FireAsh.Edit.apk"
if (-not (Test-Path $Apk)) {
    Write-Error "APK not found. Build debug first:`n  $Apk"
    exit 1
}
Copy-Item -LiteralPath $Apk -Destination $Out -Force
$item = Get-Item $Out
Write-Host "OK: $($item.FullName) ($($item.Length) bytes, $($item.LastWriteTime))"
