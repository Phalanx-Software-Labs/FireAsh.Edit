# FireAsh cheat engine

Android helper for **Pokémon Fire Ash**: patch `Data/Scripts.rxdata`, restore from backup, with on-screen progress and success feedback.

This repository ships the **debug APK** from the normal Android build output path (`fireash-scripatcher/app/build/outputs/apk/debug/app-debug.apk`). Cloning the default zip does not include the Android Studio project — keep that project locally (Gradle root folder: `fireash-scripatcher/`; you can rename it to `fireash-cheat-engine` on disk if nothing has the folder open).

## Download

**[app-debug.apk](https://github.com/Phalanx-Software-Labs/FireAsh-CheatEngine/raw/main/fireash-scripatcher/app/build/outputs/apk/debug/app-debug.apk)**

Install on your device, grant folder access, pick the game folder that contains **`Data`**, then use **Add mods** or **Remove mods**.

---

**Developers:** Rebuild the APK from `fireash-scripatcher/` after updating `app/src/main/assets/patched_Scripts.rxdata`, then commit and push **`fireash-scripatcher/app/build/outputs/apk/debug/app-debug.apk`** (no copy step).
