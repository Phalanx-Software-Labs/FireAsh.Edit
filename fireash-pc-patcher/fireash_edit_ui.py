#!/usr/bin/env python3
"""
FireAsh.Edit for Windows — Python + tkinter / ttk (same spirit as NANDy-Man sentinel_ui.py).
"""

from __future__ import annotations

import ctypes
import json
import os
import sys
import threading
import time
from collections import deque
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

__version__ = "1.0.0"

PATCH_TEMP_NAME = "patchtmp.rxdata"
APP_TITLE = f"FireAsh.Edit {__version__}"


# --- settings ---


def _config_dir() -> Path:
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or str(Path.home())
    else:
        base = str(Path.home() / ".local" / "share")
    return Path(base) / "PhalanxLabs" / "FireAsh.Edit"


def _settings_path() -> Path:
    return _config_dir() / "settings.json"


def load_settings() -> dict:
    try:
        p = _settings_path()
        if p.is_file():
            return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        pass
    return {}


def save_settings(data: dict) -> None:
    d = _config_dir()
    d.mkdir(parents=True, exist_ok=True)
    _settings_path().write_text(json.dumps(data, indent=2), encoding="utf-8")


# --- Windows: Downloads (folder picker default) and C: drive game scan ---


def get_downloads_directory() -> str:
    if os.name != "nt":
        return str(Path.home() / "Downloads")

    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", ctypes.c_uint32),
            ("Data2", ctypes.c_uint16),
            ("Data3", ctypes.c_uint16),
            ("Data4", ctypes.c_uint8 * 8),
        ]

    guid = GUID()
    guid.Data1 = 0x374DE290
    guid.Data2 = 0x123F
    guid.Data3 = 0x4565
    guid.Data4 = (ctypes.c_uint8 * 8)(0x91, 0x64, 0x39, 0xC4, 0x92, 0x5E, 0x46, 0x7B)

    shell32 = ctypes.windll.shell32
    ole32 = ctypes.windll.ole32
    ptr = ctypes.c_void_p()
    hr = shell32.SHGetKnownFolderPath(ctypes.byref(guid), 0, None, ctypes.byref(ptr))
    if hr == 0 and ptr.value:
        try:
            return ctypes.wstring_at(ptr.value)
        finally:
            ole32.CoTaskMemFree(ptr)
    return str(Path.home() / "Downloads")


def looks_like_fire_ash_path(full_path: str) -> bool:
    s = full_path.lower()
    if "fireash" in s:
        return True
    return "fire" in s and "ash" in s


def looks_like_retail_pokemon_fire_ash_folder_name(name: str) -> bool:
    """
    True for real install folder titles like 'Pokemon Fire Ash 3.6 Part 2.2'.
    Excludes dev paths such as 'fireash', 'fireash workspace', 'fireash_backups'
    (those do not contain the word pokemon).
    """
    n = name.lower().replace("é", "e")
    if "pokemon" not in n:
        return False
    return "fire" in n and "ash" in n


def is_official_nested_retail_game_root(path: str) -> bool:
    """
    Official Windows layout for this game (what the installer uses):
    C:\\Pokemon Fire Ash ...\\Pokemon Fire Ash ...\\Game\\Data\\Scripts.rxdata

    Not the shallow C:\\Pokemon Fire Ash ...\\Game (only one folder before Game).
    """
    try:
        p = Path(path).resolve()
    except OSError:
        return False
    parts = p.parts
    # Windows: ('C:\\', 'Pokemon Fire Ash 3.6 Part 2.2', 'Pokemon Fire Ash 3.6 Part 2.2', 'Game')
    if len(parts) < 4:
        return False
    if parts[-1].lower() != "game":
        return False
    top = parts[1]
    inner = parts[-2]
    if not looks_like_retail_pokemon_fire_ash_folder_name(top):
        return False
    if not looks_like_retail_pokemon_fire_ash_folder_name(inner):
        return False
    return True


def find_fire_ash_top_level_folders_on_c_drive() -> list[str]:
    """
    Direct children of C:\\ whose names look like the retail 'Pokemon Fire Ash ...' folder only.
    """
    if os.name != "nt":
        return []
    c = Path("C:/")
    if not c.is_dir():
        return []
    out: list[str] = []
    try:
        for p in sorted(c.iterdir(), key=lambda x: x.name.lower()):
            if not p.is_dir():
                continue
            if looks_like_retail_pokemon_fire_ash_folder_name(p.name):
                try:
                    out.append(str(p.resolve()))
                except OSError:
                    continue
    except (OSError, PermissionError):
        pass
    return out


def find_game_roots_under_directory(
    start_dir: str, max_depth: int = 24, max_dirs: int = 50_000
) -> list[str]:
    """
    BFS under start_dir for folders that contain Data/Scripts.rxdata.
    Returns each game root (the folder that directly contains Data/), e.g. ...\\Game.
    """
    results: list[str] = []
    if not Path(start_dir).is_dir():
        return results
    visited = 0
    q: deque[tuple[str, int]] = deque([(start_dir, 0)])
    while q and visited < max_dirs:
        dir_path, depth = q.popleft()
        visited += 1
        try:
            resolved = str(Path(dir_path).resolve())
        except OSError:
            continue
        scripts = Path(dir_path) / "Data" / "Scripts.rxdata"
        if scripts.is_file():
            results.append(resolved)
        if depth >= max_depth:
            continue
        try:
            for sub in Path(dir_path).iterdir():
                if sub.is_dir():
                    q.append((str(sub), depth + 1))
        except (OSError, PermissionError):
            pass
    uniq: list[str] = []
    for r in results:
        if r not in uniq:
            uniq.append(r)
    return uniq


def find_fire_ash_installs_from_c_drive_branches() -> tuple[list[str], list[str]]:
    """
    Returns (top_level_branch_paths, game_roots).
    game_roots are only official nested retail paths:
    C:\\Pokemon Fire Ash...\\Pokemon Fire Ash...\\Game
    """
    branches = find_fire_ash_top_level_folders_on_c_drive()
    roots: list[str] = []
    for b in branches:
        for r in find_game_roots_under_directory(b):
            if is_official_nested_retail_game_root(r) and r not in roots:
                roots.append(r)
    return branches, roots


# --- patch files (same rules as Android) ---


def resolve_data_dir(game_root: str) -> Path:
    root = Path(game_root).expanduser().resolve()
    data = root / "Data"
    if not data.is_dir():
        data = root / "data"
    if not data.is_dir():
        raise OSError(
            "No Data folder here. Pick the folder that contains Data (next to Game.exe / mkxp)."
        )
    return data


def _delete_retry(path: Path, log, attempts: int = 8) -> None:
    for i in range(attempts):
        try:
            if not path.is_file():
                return
            path.unlink()
            log(f"Deleted {path.name}.")
            return
        except PermissionError as e:
            if i == attempts - 1:
                raise OSError(
                    "Access denied on Scripts.rxdata. Close the game and try again."
                ) from e
            time.sleep(0.25 * (i + 1))
        except OSError as e:
            if i == attempts - 1:
                raise OSError(
                    "Could not replace or delete Scripts.rxdata. Close the game and any launcher "
                    "so the file is not in use, then try again."
                ) from e
            time.sleep(0.25 * (i + 1))


def _move_or_replace(tmp: Path, dest: Path, log) -> None:
    try:
        tmp.replace(dest)
        log("Renamed temp file to Scripts.rxdata.")
    except OSError:
        dest.write_bytes(tmp.read_bytes())
        log("Copied temp file to Scripts.rxdata.")
        try:
            tmp.unlink()
        except OSError:
            pass


def install_patch(game_root: str, patched_bytes: bytes, log) -> None:
    if not patched_bytes:
        raise OSError("Patched script file is empty.")
    data_dir = resolve_data_dir(game_root)
    scripts = data_dir / "Scripts.rxdata"
    backup = data_dir / "Scripts.rxdata.backup"
    if not scripts.is_file():
        raise OSError(f"Missing Data file: {scripts}")

    if scripts.is_file() and not backup.is_file():
        log("Creating Scripts.rxdata.backup from your current Scripts.rxdata (one time).")
        backup.write_bytes(scripts.read_bytes())
    elif backup.is_file():
        log("Scripts.rxdata.backup already exists — not overwriting (keeps your first backup).")

    tmp = data_dir / PATCH_TEMP_NAME
    if tmp.is_file():
        _delete_retry(tmp, log)
    tmp.write_bytes(patched_bytes)
    log(f"Wrote temp {PATCH_TEMP_NAME}.")

    _delete_retry(scripts, log)
    _move_or_replace(tmp, scripts, log)
    log("Add mods finished: Data/Scripts.rxdata is now the patched file.")


def remove_mods(game_root: str, vanilla_bytes: bytes | None, log) -> None:
    data_dir = resolve_data_dir(game_root)
    scripts = data_dir / "Scripts.rxdata"
    backup = data_dir / "Scripts.rxdata.backup"

    if backup.is_file() and backup.stat().st_size > 0:
        log("Restoring from Scripts.rxdata.backup.")
        _delete_retry(scripts, log)
        try:
            backup.replace(scripts)
            log("Renamed Scripts.rxdata.backup → Scripts.rxdata.")
        except OSError:
            scripts.write_bytes(backup.read_bytes())
            log("Copied backup to Scripts.rxdata (rename not available).")
            try:
                backup.unlink()
            except OSError:
                pass
        log("Remove mods finished: restored from backup.")
        return

    if vanilla_bytes:
        log("No usable backup — restoring from bundled vanilla_Scripts.rxdata.")
        tmp = data_dir / PATCH_TEMP_NAME
        if tmp.is_file():
            _delete_retry(tmp, log)
        tmp.write_bytes(vanilla_bytes)
        _delete_retry(scripts, log)
        _move_or_replace(tmp, scripts, log)
        log("Remove mods finished: restored vanilla scripts from app bundle.")
        return

    raise OSError(
        "No Scripts.rxdata.backup found. Use Add mods once while Scripts.rxdata is still vanilla "
        "to create that backup."
    )


def resolve_asset_paths() -> tuple[Path, Path]:
    """patched + vanilla rxdata paths (PyInstaller bundle, local assets/, or repo)."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS)
        return base / "patched_Scripts.rxdata", base / "vanilla_Scripts.rxdata"
    here = Path(__file__).resolve().parent
    local = here / "assets"
    p1 = local / "patched_Scripts.rxdata"
    v1 = local / "vanilla_Scripts.rxdata"
    if p1.is_file():
        return p1, v1
    repo_assets = here.parent / "fireash-scripatcher" / "app" / "src" / "main" / "assets"
    return repo_assets / "patched_Scripts.rxdata", repo_assets / "vanilla_Scripts.rxdata"


# --- UI (NANDy-Man style: ttk.Frame, threading, root.after) ---


class FireAshEditUI:
    def __init__(self) -> None:
        self.settings = load_settings()
        self.operation_running = False

        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.minsize(480, 380)
        self.root.geometry("720x520")

        self.folder_var = tk.StringVar(value="")
        self._build_ui()
        self._update_folder_label()
        self.root.after(100, self._on_first_show)

    def _build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=15)
        main.pack(fill=tk.BOTH, expand=True)

        self.folder_label = ttk.Label(main, textvariable=self.folder_var, wraplength=640)
        self.folder_label.pack(anchor=tk.W, pady=(0, 8))

        row1 = ttk.Frame(main)
        row1.pack(fill=tk.X, pady=(0, 8))
        self.btn_pick = ttk.Button(row1, text="Choose game folder", command=self._on_pick_folder)
        self.btn_pick.pack(side=tk.LEFT, padx=(0, 8))
        self.btn_scan = ttk.Button(
            row1, text="Scan C: for game", command=lambda: self._scan_game_on_c(manual=True)
        )
        self.btn_scan.pack(side=tk.LEFT)

        row2 = ttk.Frame(main)
        row2.pack(fill=tk.X, pady=(0, 8))
        self.btn_add = ttk.Button(row2, text="Add mods", command=self._on_add_mods)
        self.btn_add.pack(side=tk.LEFT, padx=(0, 8))
        self.btn_remove = ttk.Button(row2, text="Remove mods", command=self._on_remove_mods)
        self.btn_remove.pack(side=tk.LEFT)

        ttk.Label(
            main,
            text=(
                "Supported game: Pokémon Fire Ash 3.6 Part 2.2 only. Pick the folder that contains Data "
                "(same as Android). Add mods creates Data/Scripts.rxdata.backup once. Remove mods uses that backup, "
                "or bundled vanilla if no backup."
            ),
            wraplength=640,
            font=("", 8),
            foreground="gray",
        ).pack(anchor=tk.W, pady=(0, 8))

        ttk.Label(main, text="Log (troubleshooting):", font=("", 9, "bold")).pack(anchor=tk.W)
        log_frame = ttk.Frame(main)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(4, 0))
        scroll = ttk.Scrollbar(log_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text = tk.Text(
            log_frame,
            wrap=tk.WORD,
            height=14,
            font=("Consolas", 9),
            yscrollcommand=scroll.set,
            state=tk.DISABLED,
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=self.log_text.yview)

        ttk.Label(
            main,
            text=(
                "Requires Python 3 with tkinter. Scan C: only finds the retail install: "
                "C:\\Pokemon Fire Ash...\\Pokemon Fire Ash...\\Game (ignores C:\\fireash-style dev folders)."
            ),
            font=("", 8),
            foreground="gray",
            wraplength=640,
        ).pack(anchor=tk.W, pady=(10, 0))

    def _log(self, line: str) -> None:
        ts = time.strftime("%H:%M:%S")
        text = f"{ts}  {line}\n"

        def append() -> None:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, text)
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)

        self.root.after(0, append)

    def _update_folder_label(self) -> None:
        p = (self.settings.get("game_root_path") or "").strip()
        if not p:
            self.folder_var.set("Game folder: (none - choose folder or Scan C: for game)")
        else:
            self.folder_var.set(f"Game folder: {p}")

    def _set_game_root(self, path: str, save: bool) -> None:
        path = str(Path(path).resolve())
        self.settings["game_root_path"] = path
        if save:
            save_settings(self.settings)
        self._update_folder_label()

    def _set_buttons_busy(self, busy: bool) -> None:
        state = ("disabled",) if busy else ("!disabled",)
        self.btn_pick.state(state)
        self.btn_scan.state(state)
        self.btn_add.state(state)
        self.btn_remove.state(state)

    def _on_first_show(self) -> None:
        self._log(
            "Started. Scan C: only accepts the retail path: "
            "C:\\Pokemon Fire Ash...\\Pokemon Fire Ash...\\Game (with Data inside Game)."
        )
        if not (self.settings.get("game_root_path") or "").strip():
            self._scan_game_on_c(manual=False)
        else:
            self._log('Using saved folder. Use "Scan C: for game" or "Choose game folder" to change.')

    def _on_pick_folder(self) -> None:
        if self.operation_running:
            return
        initial = (self.settings.get("game_root_path") or "").strip()
        if not initial or not Path(initial).is_dir():
            initial = get_downloads_directory()
        path = filedialog.askdirectory(
            parent=self.root,
            title="Select the folder that contains the Data folder",
            initialdir=initial if Path(initial).is_dir() else None,
        )
        if path:
            self._set_game_root(path, save=True)
            self._log(f"You chose: {path}")

    def _show_folder_picker(self, paths: list[str], title: str) -> str | None:
        chosen: list[str | None] = [None]
        top = tk.Toplevel(self.root)
        top.title("Choose folder")
        top.transient(self.root)
        top.grab_set()
        top.minsize(400, 280)
        ttk.Label(top, text=title, wraplength=520).pack(padx=12, pady=(10, 6))
        frame = ttk.Frame(top)
        frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)
        scroll = ttk.Scrollbar(frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        lb = tk.Listbox(frame, height=12, width=80, yscrollcommand=scroll.set)
        lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=lb.yview)
        for p in paths:
            lb.insert(tk.END, p)
        if paths:
            lb.selection_set(0)

        def ok_click() -> None:
            sel = lb.curselection()
            if sel:
                chosen[0] = paths[int(sel[0])]
            top.destroy()

        def cancel_click() -> None:
            top.destroy()

        btns = ttk.Frame(top)
        btns.pack(fill=tk.X, pady=(0, 12))
        ttk.Button(btns, text="OK", command=ok_click).pack(side=tk.RIGHT, padx=6)
        ttk.Button(btns, text="Cancel", command=cancel_click).pack(side=tk.RIGHT)
        top.protocol("WM_DELETE_WINDOW", cancel_click)
        top.wait_window()
        return chosen[0]

    def _scan_game_on_c(self, manual: bool) -> None:
        if self.operation_running:
            return
        if os.name != "nt":
            self._log("Scan C: is for Windows only. Use Choose game folder.")
            if manual:
                messagebox.showinfo(APP_TITLE, "This scan only runs on Windows. Use Choose game folder.", parent=self.root)
            return

        branches, roots = find_fire_ash_installs_from_c_drive_branches()
        self._log(
            "Scanning C:\\ for a top-level folder named like 'Pokemon Fire Ash ...' "
            "(not generic fireash dev folders), then only the nested ...\\\\...\\\\Game install."
        )

        if not branches:
            self._log(
                "No retail folder directly under C:\\ (name must include pokemon, fire, and ash, e.g. "
                "'Pokemon Fire Ash 3.6 Part 2.2'). Dev folders like C:\\fireash are ignored."
            )
            if manual:
                messagebox.showinfo(
                    APP_TITLE,
                    "No retail Pokemon Fire Ash folder was found directly under C:\\.\n\n"
                    "The scan only looks for names like: Pokemon Fire Ash 3.6 Part 2.2\n\n"
                    "Use Choose game folder if your install is elsewhere.",
                    parent=self.root,
                )
            return

        for b in branches:
            self._log(f"Found branch: {b}")

        if not roots:
            self._log(
                "Found C:\\Pokemon Fire Ash... but no official nested Game folder "
                "(expect ...\\\\Pokemon Fire Ash...\\\\Pokemon Fire Ash...\\\\Game\\\\Data\\\\Scripts.rxdata)."
            )
            if manual:
                messagebox.showinfo(
                    APP_TITLE,
                    "The retail Pokemon Fire Ash folder was found on C:\\ but the expected nested "
                    "install was not detected.\n\n"
                    "Official layout:\n"
                    "C:\\Pokemon Fire Ash 3.6 Part 2.2\\Pokemon Fire Ash 3.6 Part 2.2\\Game\\\n\n"
                    "Use Choose game folder if yours differs.",
                    parent=self.root,
                )
            return

        preferred = [r for r in roots if looks_like_fire_ash_path(r)]
        pool = preferred if preferred else roots
        self._log(
            f"Found {len(roots)} folder(s) with Data/Scripts.rxdata under those branches"
            + (f" ({len(preferred)} have fire/ash in the full path)." if preferred else ".")
        )

        if len(pool) == 1:
            chosen = pool[0]
            self._log(f"Using the only match: {chosen}")
        else:
            pick = self._show_folder_picker(
                pool, "More than one game folder was found. Pick the folder that contains Data:"
            )
            if not pick:
                self._log("Scan cancelled.")
                return
            chosen = pick
            self._log(f"You selected: {chosen}")

        self._set_game_root(chosen, save=True)
        if manual:
            messagebox.showinfo(APP_TITLE, "Game folder set. You can use Add mods or Remove mods.", parent=self.root)

    def _on_add_mods(self) -> None:
        if self.operation_running:
            return
        root = (self.settings.get("game_root_path") or "").strip()
        if not root:
            messagebox.showwarning(APP_TITLE, "Choose the game folder first (or Scan C: for game).", parent=self.root)
            return
        if not messagebox.askokcancel(
            "Supported version",
            "This app only supports Pokémon Fire Ash 3.6 Part 2.2. Installing on any other version "
            "can break the game or saves.\n\nContinue only if that is exactly what you are playing.",
            parent=self.root,
            icon="warning",
        ):
            return

        patched_path, _ = resolve_asset_paths()
        if not patched_path.is_file():
            self._log(f"ERROR: Missing {patched_path}")
            messagebox.showerror(
                APP_TITLE,
                "patched_Scripts.rxdata not found. Run scripts/sync_patched_scripts_to_apk.ps1 from the repo, "
                "or put patched_Scripts.rxdata in fireash-pc-patcher/assets/.",
                parent=self.root,
            )
            return

        data = patched_path.read_bytes()

        def work() -> None:
            try:
                install_patch(root, data, lambda m: self.root.after(0, lambda: self._log(m)))
                self.root.after(0, lambda: self._log("Done."))
                self.root.after(
                    0,
                    lambda: messagebox.showinfo(APP_TITLE, "Add mods completed.", parent=self.root),
                )
            except Exception as e:
                self.root.after(0, lambda: self._log(f"ERROR: {e}"))
                self.root.after(
                    0,
                    lambda: messagebox.showerror(APP_TITLE, str(e), parent=self.root),
                )
            finally:
                self.root.after(0, self._finish_op)

        self._start_op(work)

    def _on_remove_mods(self) -> None:
        if self.operation_running:
            return
        root = (self.settings.get("game_root_path") or "").strip()
        if not root:
            messagebox.showwarning(APP_TITLE, "Choose the game folder first (or Scan C: for game).", parent=self.root)
            return

        _, vanilla_path = resolve_asset_paths()
        vanilla: bytes | None = None
        if vanilla_path.is_file():
            vanilla = vanilla_path.read_bytes()

        def work() -> None:
            try:
                remove_mods(root, vanilla, lambda m: self.root.after(0, lambda: self._log(m)))
                self.root.after(0, lambda: self._log("Done."))
                self.root.after(
                    0,
                    lambda: messagebox.showinfo(APP_TITLE, "Remove mods completed.", parent=self.root),
                )
            except Exception as e:
                self.root.after(0, lambda: self._log(f"ERROR: {e}"))
                self.root.after(
                    0,
                    lambda: messagebox.showerror(APP_TITLE, str(e), parent=self.root),
                )
            finally:
                self.root.after(0, self._finish_op)

        self._start_op(work)

    def _start_op(self, target) -> None:
        self.operation_running = True
        self._set_buttons_busy(True)
        t = threading.Thread(target=target, daemon=True)
        t.start()

    def _finish_op(self) -> None:
        self.operation_running = False
        self._set_buttons_busy(False)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = FireAshEditUI()
    app.run()


if __name__ == "__main__":
    main()
