# How to publish (two simple tracks)

## Windows (PC)

1. Open your repo on GitHub.
2. Go to **Actions**.
3. Open **Publish Windows release**.
4. Click **Run workflow**.
5. Type a version (example: `1.0.0`) and run it.

GitHub creates a **release** whose name includes **Windows**. Users open **Releases**, open that one, and download **FireAsh.Edit.exe** under **Assets**. They do **not** use **Code → Download ZIP**.

## Android

1. On GitHub go to **Releases** → **Draft a new release**.
2. Create a tag (example: `v1.0.0-android`) and a title that says **Android**.
3. Upload **FireAsh.Edit.apk** under **Attach binaries**.
4. In the description, tell users to download the **APK** only (not the source zip).

Users install the APK on their phone like any other sideloaded app.
