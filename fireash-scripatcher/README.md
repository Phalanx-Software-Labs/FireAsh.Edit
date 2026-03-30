# Fire Ash Mod Installer (Android)

Installs a **pre-patched** `Data/Scripts.rxdata` (bag-cheat mod) into a copy of Pokémon Fire Ash that you select with the system folder picker.

## Before you build the APK (on PC)

1. Run `bag_cheat_mod/package_mod.rb` and `inject_mod.rb` against your **exact** game version (see `modcentral/bag_cheat_mod/README.md`).
2. Copy the resulting `Game/Data/Scripts.rxdata` over this file:

   `app/src/main/assets/patched_Scripts.rxdata`

3. Open this folder in **Android Studio**, sync Gradle, **Build → Build Bundle(s) / APK(s) → Build APK(s)**.

The asset file is **large** (~1 MB) and is **version-specific**. If the game updates, regenerate it on PC and replace the asset, then rebuild the APK.

## On the phone

Install the APK, tap **Choose game folder**, select the directory that **contains** `Data` (the same tree JoiPlay uses for that game), then **Install bag-cheat mod**.

Revert: delete `Scripts.rxdata`, rename `Scripts.rxdata.backup` to `Scripts.rxdata`.
