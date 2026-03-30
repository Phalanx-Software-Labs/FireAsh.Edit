# FireAsh cheat engine (developer notes)

Android helper for **Pokémon Fire Ash**: patch `Data/Scripts.rxdata`, restore from backup, with on-screen progress and success feedback.

## Download for users

At the **repository root** (outside this folder): **`FireAshCheatEngine.apk`**.

Raw link (for direct installs):

**https://github.com/Phalanx-Software-Labs/FireAsh-CheatEngine/raw/main/FireAshCheatEngine.apk**

Install on your device, grant folder access, pick the game folder that contains **`Data`**, then use **Add mods** or **Remove mods**.

---

## Developers

Gradle root folder: `fireash-scripatcher/` (kept locally; not all paths are tracked in git).

1. Update mod Ruby sources under `bag_cheat_mod/`, run `package_mod.rb`, inject into `Scripts.rxdata`, copy to `fireash-scripatcher/app/src/main/assets/patched_Scripts.rxdata`.
2. Build **Build → Build APK** in Android Studio.
3. Copy `fireash-scripatcher/app/build/outputs/apk/debug/app-debug.apk` to the repo root as **`FireAshCheatEngine.apk`**, commit, and push.
