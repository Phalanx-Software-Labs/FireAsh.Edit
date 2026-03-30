# FireAsh cheat engine

Android helper for **Pokémon Fire Ash**: patch `Data/Scripts.rxdata`, restore from backup, with on-screen progress and success feedback.

This repository only ships the **debug APK** at the root. Cloning the default zip does not include the Android Studio project — keep that project locally (Gradle root folder: `fireash-scripatcher/`; you can rename it to `fireash-cheat-engine` on disk if nothing has the folder open).

## Download

**[FireAshCheatEngine-debug.apk](https://github.com/Phalanx-Software-Labs/Mimic/raw/main/FireAshCheatEngine-debug.apk)**

Install on your device, grant folder access, pick the game folder that contains **`Data`**, then use **Install bag-cheat mod** or **Restore original scripts**.

If you rename the GitHub repository (for example away from the old **Mimic** name), update the raw link above to match `https://github.com/Phalanx-Software-Labs/<repo>/raw/main/FireAshCheatEngine-debug.apk`.

---

**Developers:** Rebuild the APK from `fireash-scripatcher/` after updating `app/src/main/assets/patched_Scripts.rxdata`. Replace **`FireAshCheatEngine-debug.apk`** at the repository root, commit, and push.
