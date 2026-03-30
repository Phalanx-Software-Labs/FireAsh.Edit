# FireAsh.Edit (developer notes)

**FireAsh.Edit** is a **Party Management and Data Visualization Tool** for **Pokémon Fire Ash v3.6 Part 2.2** only. It adds an in-game **Mods** hub (pause menu) to inspect and adjust party Pokémon, trainer and bag data, and related options, and includes an Android helper that applies the matching script bundle to your game’s `Data/Scripts.rxdata`.

## Supported game version (required)

**Pokémon Fire Ash v3.6 Part 2.2 only.** Any other game version is **unsupported**; scripts and the APK may not match your `Scripts.rxdata` and can break the game or saves.

- **PC inject / `scripts/sync_patched_scripts_to_apk.ps1`** runs `scripts/verify_fire_ash_scripts_version.rb` first (unless you pass **`-SkipVersionCheck`**).
- **Android app** shows a confirmation before **Add mods**; it cannot fully parse `Scripts.rxdata` on-device, so you must only use it with the supported build.

**Existing saves:** The patch is **script-only** and works through normal trainer, bag, party, and switch data. It is **theoretically safe** to continue an existing save or to load that save on a **vanilla** copy of the **same** supported build — see **`bag_cheat_mod/README.md`** (“Existing saves”) for scope and caveats. Back up saves first.

---

## Download for users

At the **repository root**: **`FireAsh.Edit.apk`**.

Raw link (for direct installs):

**https://github.com/Phalanx-Software-Labs/FireAsh-CheatEngine/raw/main/FireAsh.Edit.apk**

Install on your device, grant folder access, pick the game folder that contains **`Data`**, then use **Add mods** or **Remove mods**.

**In-game (after Add mods):** **Pause → Mods** — **Party** (shiny, IV, EV, stats, Pokémon details, moves), **Bag** (quantities, add items), **Trainer** (money), and related options.

---

## Developers

Gradle project (local): `fireash-scripatcher/` — build the Android app there after refreshing assets.

**After any change under `bag_cheat_mod/`**, refresh the bundled script **before** building the APK:

```powershell
cd "path\to\project Vespa"
.\scripts\sync_patched_scripts_to_apk.ps1
```

Optional: `-GameScriptsRxdata "D:\path\to\Fire Ash\Data\Scripts.rxdata"` if your game is not at the default path inside this workspace layout.

Optional: **`-SkipVersionCheck`** only if you intentionally inject against a different build (not recommended).

That runs version verify (unless skipped), `package_mod.rb`, `inject_mod.rb`, and copies the result to `fireash-scripatcher/app/src/main/assets/patched_Scripts.rxdata`.

Then:

1. **Build → Build APK** in Android Studio.
2. Copy `fireash-scripatcher/app/build/outputs/apk/debug/app-debug.apk` to the repo root as **`FireAsh.Edit.apk`**, commit, and push.
