# How to publish (two simple tracks)

## Windows (PC)

1. Open your repo on GitHub.
2. Go to **Actions**.
3. Open **Publish Windows release**.
4. Click **Run workflow**.
5. Type a version (example: `1.0.0`) and run it.

GitHub creates a **release** whose name includes **Windows**. Users open **Releases**, open that one, and download **FireAsh.Edit.exe** under **Assets**. They do **not** use **Code → Download ZIP**.

## Android

After **Android Studio** builds the debug APK, it lives at:

`fireash-scripatcher\app\build\outputs\apk\debug\app-debug.apk`

Copy it to the repo root as **`FireAsh.Edit.apk`** (or run **`fireash-pc-patcher\copy_debug_apk_to_repo_root.ps1`**), then commit and push so `main` matches what you attach to Releases.

1. On GitHub go to **Releases** → **Draft a new release**.
2. Create a tag (example: `v1.0.0-android`) and a title that says **Android**.
3. Upload **FireAsh.Edit.apk** under **Attach binaries**.
4. In the description, tell users to download the **APK** only (not the source zip).

Users install the APK on their phone like any other sideloaded app.
