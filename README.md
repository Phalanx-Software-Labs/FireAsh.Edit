# Mimic

Pokémon **Fire Ash** bag-quantity mod (pause menu → **Mods**) plus an **Android installer** APK project.

## Contents

| Folder | What it is |
|--------|------------|
| `bag_cheat_mod/` | Ruby sources and `package_mod.rb` → `mod.json` for PC injection (see its README). |
| `fireash-scripatcher/` | Android Studio project: copies bundled `patched_Scripts.rxdata` into the game `Data` folder you pick. |

## PC: inject the mod

From your **modcentral** (or any) machine with Ruby:

```text
ruby bag_cheat_mod/package_mod.rb
ruby path/to/inject_mod.rb "C:\...\Game" bag_cheat_mod/mod.json
```

Then refresh the Android asset:

```text
copy Game\Data\Scripts.rxdata fireash-scripatcher\app\src\main\assets\patched_Scripts.rxdata
```

## Android: build the installer

Open **`fireash-scripatcher`** in Android Studio → **Build → Generate App Bundles or APKs → Generate APKs**. Install the debug APK on your device, grant folder access, select the game folder that contains **`Data`**, tap install.

A prebuilt debug installer is also committed as **`fireash-scripatcher/releases/FireAshModInstaller-debug.apk`** (same as `app/build/outputs/apk/debug/app-debug.apk` after a local build).

**Note:** `patched_Scripts.rxdata` in assets must match the game version you play.
