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
> Do not use the green **Code** button or **Download ZIP.** Those are source files for developers.

1. Go to **[Releases](https://github.com/Phalanx-Software-Labs/FireAsh.Edit/releases)**.
2. Download the asset for your platform:
   - **Android:** `FireAsh.Edit.apk`
   - **Windows:** `FireAsh.Edit.exe`

### 📱 Android

- Install the APK (allow “Unknown sources” if prompted).
- Point the app to the game folder containing the **Data** directory.
- Select **Add mods** to inject the editor or **Remove mods** to revert.

### 💻 Windows

- Run **FireAsh.Edit.exe** (no Python installation required).
- If Windows shows **“Windows protected your PC”**, click **More info** → **Run anyway**.
- Use **Scan C: for game** or **Choose game folder**, then **Add mods** or **Remove mods**.

**In-game:** After **Add mods**, use **Pause → Mods** to open the editor.

## ⚠️ Critical compatibility & warnings

- **Version specific:** Built exclusively for **Fire Ash v3.6 Part 2.2.** Do not use on other versions.
- **Stuck toggles:** Some options (such as “Always Shiny”) behave like a switch. If you **Remove mods** while a toggle is still ON, the effect can stay active because the vanilla game has no menu to turn it OFF. **Fix:** Add mods again, turn the option off in-game, then remove mods.
- **Data restoration:** Removing the tool restores the original game **scripts**; it does **not** undo changes already written to your save (items, stats, etc.).

## 🛡️ Disclaimer & liability

This software is provided **“as-is”** without warranty of any kind, express or implied. By using this tool, you acknowledge and agree that:

- **User responsibility:** You are solely responsible for any modifications made to your game files.
- **Data loss:** The tool creates backups, but modifying scripts always carries some risk. **Back up your save files** before use.
- **No liability:** The authors and copyright holders are not liable for any claim, damages, or other liability arising from use of this software.
- **Non-official:** This is an independent fan-made tool. It is not affiliated with, endorsed by, or approved by the creators of Fire Ash or related IP holders.

## 🛠️ Project info

Maintained by **Phalanx Software Labs.** Fire Ash content and related assets are owned by their respective rights holders.

Publishing builds: **[RELEASING.md](RELEASING.md)** · Technical notes: **[developer/README.md](developer/README.md)**
