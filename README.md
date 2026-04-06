developed on windows with help from Cursor AI, tested on retroid pocket 6 and windows.

## Live repository — development vs. stable releases

This repository is an **active working copy** of the project: files are updated frequently while features are still being designed and tested.

 ⚠️ Disclaimer & Save Safety
Due to the massive scale of Pokémon Fire Ash, the base game and its engine are under constant stress. Even "Stable" releases of these mods may carry inherent risks:
Risk of Corruption: Any outside influence on your game scripts carries a risk of save file corruption. Always back up your save data before applying updates.
"Stable" vs. "Bug-Free": A stable release means features are tested and working as intended under normal conditions. It does not guarantee they won't interact unpredictably with the game's massive event library.
Support: Bugs are addressed as they are discovered. By using these mods, you accept that you do so at your own risk.

- **Unreleased work in the tree:** Anything in the repo may include **features that are not part of an official release yet**. Those features may be **incomplete**, **unstable**, or **changed or removed** before they ever ship.
- **Where stable builds live:** **Reliable, release-tested versions** are the ones published on **[Releases](https://github.com/Phalanx-Software-Labs/FireAsh.Edit/releases)**. The **`.apk`** and **`.exe`** attached to a **Release** are what we treat as **stable** for that version.
- **Binaries inside the repo are not the same as Releases:** Any **`.apk`**, **`.exe`**, or other packaged output that appears **inside project folders** (for example under development or build paths) may be **newer than a Release**, **experimental**, or **not fully tested**. Do **not** assume they match the quality of a Release download.
- **Risk if you skip Releases:** Installing or running an **`.apk`** or **`.exe`** obtained **outside** the **Releases** page—for example by grabbing a file from a folder in this repo, or by building the project yourself from the latest source—may **break your game**, **corrupt your save**, or behave in ways we have not signed off on. **You use those at your own risk.** For everyday play, **always use the downloads on the Releases page**.

---

📂 FireAsh.Edit

A real-time, script-injected editor for Fire Ash v3.6 Part 2.2.

FireAsh.Edit is a specialized tool for Android and Windows that injects a custom interface directly into the game. It functions as an in-game editor, allowing you to modify internal values (Party, Bag, Trainer stats) while you play.

## ⚙️ How it Works

- **Script injection:** The tool updates **`Data/Scripts.rxdata`**, creates a backup (**`Scripts.rxdata.backup`**), and injects custom code to provide a new functional menu.
- **Live editing:** Modify your bag contents, party levels, or trainer data without leaving the game or using external save-file editors.
- **Safe reversal:** Removing the tool deletes the modified script and restores your original backup.
- **Save persistence:** Any changes made to your data (items added, stats changed) remain on your save file even after the editor is removed.

## 📥 Download & Installation

> [!IMPORTANT]
> Do not use the green **Code** button or **Download ZIP** expecting a finished app. That gives **source and project files** for developers, which may include **in-progress** work (see **Live repository** above). **Do not** hunt through the repo for an **`.apk`** or **`.exe`**—only the **Releases** downloads are promoted as **stable**.

1. Go to **[Releases](https://github.com/Phalanx-Software-Labs/FireAsh.Edit/releases)**.
2. Download the asset for your platform:
   - **Android:** `FireAsh.Edit.apk`
   - **Windows:** `FireAsh.Edit.exe`

### 📱 Android

- Install the APK (allow “Unknown sources” if prompted).
- Point the app to the game folder containing the **Data** directory. this is the folder named "Game" in the standard download. it contains the game.exe the audio, data, graphics, etc. folders.
- Select **Add mods** to inject the editor or **Remove mods** to revert.

### 💻 Windows

- Run **FireAsh.Edit.exe** (no Python installation required).
- If Windows shows **“Windows protected your PC”**, click **More info** → **Run anyway**.
- Use **Scan C: for game** or **Choose game folder**, then **Add mods** or **Remove mods**. when selecting the folder, chose the folder named "Game" in the standard instal of the game. this is the folder that contains the game.exe, audio, data, etc. folders.

**In-game:** After **Add mods**, use **Pause → Mods** to open the editor.

## ⚠️ Critical compatibility & warnings

- **Version specific:** Built exclusively for **Fire Ash v3.6 Part 2.2.** Do not use on other versions.
- **Stuck toggles:** Some options (such as “Always Shiny”) behave like a switch. If you **Remove mods** while a toggle is still ON, the effect can stay active because the vanilla game has no menu to turn it OFF. **Fix:** Add mods again, turn the option off in-game, then remove mods.
- **Data restoration:** Removing the tool restores the original game **scripts**; it does **not** undo changes already written to your save (items, stats, etc.).

## 🛡️ Disclaimer & liability

This software is provided **“as-is”** without warranty of any kind, express or implied. By using this tool, you acknowledge and agree that:

- **Development copies:** If you use builds or binaries **other than** those from **[Releases](https://github.com/Phalanx-Software-Labs/FireAsh.Edit/releases)**, you accept the extra risk described under **Live repository** above.
- **User responsibility:** You are solely responsible for any modifications made to your game files.
- **Data loss:** The tool creates backups, but modifying scripts always carries some risk. **Back up your save files** before use.
- **No liability:** The authors and copyright holders are not liable for any claim, damages, or other liability arising from use of this software.
- **Non-official:** This is an independent fan-made tool. It is not affiliated with, endorsed by, or approved by the creators of Fire Ash or related IP holders.

## 🛠️ Project info

Maintained by **Phalanx Software Labs.** Fire Ash content and related assets are owned by their respective rights holders.
