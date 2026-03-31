# -*- mode: python ; coding: utf-8 -*-
# Run from repo:  powershell -File fireash-pc-patcher\build_installer.ps1
# Or:  cd fireash-pc-patcher && pyinstaller FireAsh.Edit.spec

from pathlib import Path

from PyInstaller.utils.hooks import collect_all

spec_dir = Path(SPEC).resolve().parent
repo_root = spec_dir.parent
# Prefer fireash-pc-patcher/assets/ so a small GitHub folder can ship without the full Android tree.
local_a = spec_dir / "assets"
local_p = local_a / "patched_Scripts.rxdata"
local_v = local_a / "vanilla_Scripts.rxdata"
if local_p.is_file() and local_v.is_file():
    patched, vanilla = local_p, local_v
else:
    assets = repo_root / "fireash-scripatcher" / "app" / "src" / "main" / "assets"
    patched = assets / "patched_Scripts.rxdata"
    vanilla = assets / "vanilla_Scripts.rxdata"

if not patched.is_file():
    raise SystemExit(
        f"Missing patched asset. Either:\n"
        f"  Put files in {local_a}\\ (patched + vanilla Scripts.rxdata), or\n"
        f"  Run scripts\\sync_patched_scripts_to_apk.ps1 and use fireash-scripatcher assets.\n"
        f"Looked for: {patched}"
    )
if not vanilla.is_file():
    raise SystemExit(f"Missing vanilla asset: {vanilla}")

tk_datas, tk_binaries, tk_hidden = collect_all("tkinter")

a = Analysis(
    [str(spec_dir / "fireash_edit_ui.py")],
    pathex=[str(spec_dir)],
    binaries=tk_binaries,
    datas=[
        (str(patched), "."),
        (str(vanilla), "."),
    ]
    + tk_datas,
    hiddenimports=list(tk_hidden),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="FireAsh.Edit",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
