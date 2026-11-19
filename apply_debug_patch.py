"""
================================================================================
 Pokemon Fire Ash - Universal Debug & Quality-of-Life Patcher
================================================================================
 Compatible across Windows, Linux, macOS, Android (JoiPlay/Termux), and
 all modern versions of Pokemon Fire Ash (v3.4, v3.5, v3.6, v3.6p2, v3.7, v3.7.1).
================================================================================
"""

import os
import sys
import shutil
import zlib
import subprocess

# ------------------------------------------------------------------------------
# Dependency Auto-Installer (rubymarshal)
# ------------------------------------------------------------------------------
try:
    import rubymarshal.reader
    import rubymarshal.writer
except ImportError:
    print("[*] Installing required dependency 'rubymarshal'...")
    installed = False
    for cmd in [
        [sys.executable, "-m", "pip", "install", "--user", "rubymarshal"],
        [sys.executable, "-m", "pip", "install", "rubymarshal"]
    ]:
        try:
            subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            installed = True
            break
        except Exception:
            continue

    if installed:
        import rubymarshal.reader
        import rubymarshal.writer
    else:
        print("[!] Error: Could not automatically install 'rubymarshal'.")
        print("[!] Please run manually in your terminal: pip install rubymarshal")
        sys.exit(1)

# ------------------------------------------------------------------------------
# Enhanced Ruby Code Snippets (Universal Smart Fuzzy Search)
# ------------------------------------------------------------------------------

RUBY_LISTERS_CODE = '''def pbListScreen(title, lister)
  viewport = Viewport.new(0, 0, Graphics.width, Graphics.height)
  viewport.z = 99999
  list = pbListWindow([])
  list.viewport = viewport
  list.z = 2
  title_win = Window_UnformattedTextPokemon.newWithSize("",
     Graphics.width / 2, 0, Graphics.width / 2, 64, viewport)
  title_win.z = 2
  lister.setViewport(viewport)
  raw_commands = lister.commands
  if raw_commands.length == 0
    val = lister.value(-1)
    lister.dispose; title_win.dispose; list.dispose; viewport.dispose
    return val
  end
  search_query = ""
  update_title = proc do
    if search_query.empty?
      title_win.text = _INTL("{1}\\n[Z] Search", title)
    else
      title_win.text = _INTL("{1}\\n[Z] \\"{2}\\"", title, search_query)
    end
  end
  rebuild = proc do
    display_cmds = []
    map_indices = []
    if search_query.empty?
      display_cmds.push("[-- SEARCH / FILTER... --]")
    else
      display_cmds.push("[-- CLEAR SEARCH: \\"" + search_query + "\\" --]")
    end
    map_indices.push(-1)
    q_low = search_query.downcase
    q_norm = q_low.gsub(/[^a-z0-9]/, "")
    tokens = q_low.split
    raw_commands.each_with_index do |cmd, s_idx|
      cname = (cmd.is_a?(Array) ? cmd[1] : cmd).to_s
      if search_query.empty?
        display_cmds.push(cmd)
        map_indices.push(s_idx)
      else
        c_low = cname.downcase
        c_norm = c_low.gsub(/[^a-z0-9]/, "")
        if c_low.include?(q_low) ||
           (!q_norm.empty? && c_norm.include?(q_norm)) ||
           (!tokens.empty? && tokens.all? { |t| c_low.include?(t) || c_norm.include?(t.gsub(/[^a-z0-9]/, "")) })
          display_cmds.push(cmd)
          map_indices.push(s_idx)
        end
      end
    end
    update_title.call
    [display_cmds, map_indices]
  end
  commands, map_indices = rebuild.call
  list.commands = commands
  list.index = 0
  selectedmap = -1
  loop do
    Graphics.update
    Input.update
    list.update
    cur_idx = list.index
    if cur_idx != selectedmap
      real_idx = map_indices[cur_idx] || -1
      if real_idx >= 0
        lister.refresh(real_idx)
      end
      selectedmap = cur_idx
    end
    if Input.trigger?(Input::BACK)
      selectedmap = -1
      break
    elsif Input.trigger?(Input::ACTION) || Input.trigger?(Input::SPECIAL)
      entered = pbEnterText(_INTL("Search:"), 0, 24, search_query)
      search_query = entered ? entered.strip : ""
      commands, map_indices = rebuild.call
      list.commands = commands
      list.index = (commands.length > 1 && !search_query.empty?) ? 1 : 0
      selectedmap = -1
    elsif Input.trigger?(Input::USE)
      if cur_idx == 0
        if search_query.empty?
          entered = pbEnterText(_INTL("Search:"), 0, 24, "")
          search_query = entered ? entered.strip : ""
        else
          search_query = ""
        end
        commands, map_indices = rebuild.call
        list.commands = commands
        list.index = (commands.length > 1 && !search_query.empty?) ? 1 : 0
        selectedmap = -1
      else
        selectedmap = map_indices[cur_idx] || -1
        break
      end
    end
  end
  val = lister.value(selectedmap)
  lister.dispose; title_win.dispose; list.dispose; viewport.dispose
  Input.update
  return val
end

def pbListScreenBlock(title, lister)
  viewport = Viewport.new(0, 0, Graphics.width, Graphics.height)
  viewport.z = 99999
  list = pbListWindow([], Graphics.width / 2)
  list.viewport = viewport
  list.z = 2
  title_win = Window_UnformattedTextPokemon.newWithSize("",
     Graphics.width / 2, 0, Graphics.width / 2, 64, viewport)
  title_win.z = 2
  lister.setViewport(viewport)
  raw_commands = lister.commands
  if raw_commands.length == 0
    val = lister.value(-1)
    lister.dispose; title_win.dispose; list.dispose; viewport.dispose
    return val
  end
  search_query = ""
  update_title = proc do
    if search_query.empty?
      title_win.text = _INTL("{1}\\n[Z] Search", title)
    else
      title_win.text = _INTL("{1}\\n[Z] \\"{2}\\"", title, search_query)
    end
  end
  rebuild = proc do
    display_cmds = []
    map_indices = []
    if search_query.empty?
      display_cmds.push("[-- SEARCH / FILTER... --]")
    else
      display_cmds.push("[-- CLEAR SEARCH: \\"" + search_query + "\\" --]")
    end
    map_indices.push(-1)
    q_low = search_query.downcase
    q_norm = q_low.gsub(/[^a-z0-9]/, "")
    tokens = q_low.split
    raw_commands.each_with_index do |cmd, s_idx|
      cname = (cmd.is_a?(Array) ? cmd[1] : cmd).to_s
      if search_query.empty?
        display_cmds.push(cmd)
        map_indices.push(s_idx)
      else
        c_low = cname.downcase
        c_norm = c_low.gsub(/[^a-z0-9]/, "")
        if c_low.include?(q_low) ||
           (!q_norm.empty? && c_norm.include?(q_norm)) ||
           (!tokens.empty? && tokens.all? { |t| c_low.include?(t) || c_norm.include?(t.gsub(/[^a-z0-9]/, "")) })
          display_cmds.push(cmd)
          map_indices.push(s_idx)
        end
      end
    end
    update_title.call
    [display_cmds, map_indices]
  end
  commands, map_indices = rebuild.call
  list.commands = commands
  list.index = 0
  selectedmap = -1
  loop do
    Graphics.update
    Input.update
    list.update
    cur_idx = list.index
    if cur_idx != selectedmap
      real_idx = map_indices[cur_idx] || -1
      if real_idx >= 0
        lister.refresh(real_idx)
      end
      selectedmap = cur_idx
    end
    if Input.trigger?(Input::BACK)
      break
    elsif Input.trigger?(Input::ACTION) || Input.trigger?(Input::SPECIAL)
      entered = pbEnterText(_INTL("Search:"), 0, 24, search_query)
      search_query = entered ? entered.strip : ""
      commands, map_indices = rebuild.call
      list.commands = commands
      list.index = (commands.length > 1 && !search_query.empty?) ? 1 : 0
      selectedmap = -1
    elsif Input.trigger?(Input::USE)
      if cur_idx == 0
        if search_query.empty?
          entered = pbEnterText(_INTL("Search:"), 0, 24, "")
          search_query = entered ? entered.strip : ""
        else
          search_query = ""
        end
        commands, map_indices = rebuild.call
        list.commands = commands
        list.index = (commands.length > 1 && !search_query.empty?) ? 1 : 0
        selectedmap = -1
      else
        real_idx = map_indices[cur_idx] || -1
        if real_idx >= 0
          yield(Input::USE, lister.value(real_idx))
          raw_commands = lister.commands
          commands, map_indices = rebuild.call
          list.commands = commands
          list.index = [cur_idx, list.commands.length - 1].min
          selectedmap = -1
        end
      end
    end
  end
  lister.dispose; title_win.dispose; list.dispose; viewport.dispose
  Input.update
end'''

RUBY_CHOOSELIST_CODE = '''def pbChooseList(commands, default = 0, cancelValue = -1, sortType = 1)
  cmdwin = pbListWindow([])
  orig_commands = commands.clone
  search_query = ""
  itemID = default
  itemIndex = 0
  sortMode = (sortType >= 0) ? sortType : 0
  sorting = true
  filtered_commands = []
  loop do
    if sorting
      q_low = search_query.downcase
      q_norm = q_low.gsub(/[^a-z0-9]/, "")
      tokens = q_low.split
      active_pool = orig_commands.select do |c|
        if search_query.empty?
          true
        else
          c_low = c[1].to_s.downcase
          c_norm = c_low.gsub(/[^a-z0-9]/, "")
          id_str = sprintf("%03d", c[0])
          c_low.include?(q_low) ||
          (!q_norm.empty? && (c_norm.include?(q_norm) || id_str.include?(q_norm))) ||
          (!tokens.empty? && tokens.all? { |t| c_low.include?(t) || c_norm.include?(t.gsub(/[^a-z0-9]/, "")) || id_str.include?(t) })
        end
      end
      if sortMode == 0
        active_pool.sort! { |a, b| a[0] <=> b[0] }
      elsif sortMode == 1
        active_pool.sort! { |a, b| a[1] <=> b[1] }
      end
      filtered_commands = active_pool
      realcommands = []
      if search_query.empty?
        realcommands.push("[-- SEARCH / FILTER (Z) --]")
      else
        realcommands.push("[-- CLEAR SEARCH: \\"" + search_query + "\\" --]")
      end
      for command in filtered_commands
        if sortType <= 0
          realcommands.push(sprintf("%03d: %s", command[0], command[1]))
        else
          realcommands.push(command[1])
        end
      end
      if search_query.empty?
        itemIndex = 0
        if itemID.is_a?(Symbol)
          filtered_commands.each_with_index { |c, i| itemIndex = i + 1 if c[2] == itemID }
        elsif itemID && itemID > 0
          filtered_commands.each_with_index { |c, i| itemIndex = i + 1 if c[0] == itemID }
        end
      else
        itemIndex = (filtered_commands.length > 0) ? 1 : 0
      end
      sorting = false
    end
    cmd = pbCommandsSortable(cmdwin, realcommands, -1, itemIndex, (sortType < 0))
    if cmd[0] == 0
      if cmd[1] < 0
        itemID = cancelValue
        break
      elsif cmd[1] == 0
        if search_query.empty?
          entered = pbEnterText(_INTL("Search:"), 0, 24, "")
          search_query = entered ? entered.strip : ""
        else
          search_query = ""
        end
        sorting = true
      else
        chosen = filtered_commands[cmd[1] - 1]
        itemID = chosen[2] || chosen[0]
        break
      end
    elsif cmd[0] == 1
      if cmd[1] > 0
        chosen = filtered_commands[cmd[1] - 1]
        itemID = chosen[2] || chosen[0]
      end
      sortMode = (sortMode + 1) % 2
      sorting = true
    end
  end
  cmdwin.dispose
  return itemID
end'''

# ------------------------------------------------------------------------------
# Universal Cross-Platform Path Helpers
# ------------------------------------------------------------------------------

def find_case_insensitive_path(base_dir, *parts):
    """Resolves a relative path case-insensitively from base_dir."""
    current = base_dir
    for part in parts:
        if not os.path.exists(current):
            return None
        target = part.lower()
        found = None
        try:
            for entry in os.listdir(current):
                if entry.lower() == target:
                    found = os.path.join(current, entry)
                    break
        except OSError:
            return None
        if not found:
            return None
        current = found
    return current

def has_scripts_file(game_dir):
    """Checks if game_dir contains Data/Scripts.rxdata (case-insensitive)."""
    if not game_dir or not os.path.isdir(game_dir):
        return False
    rx = find_case_insensitive_path(game_dir, "data", "scripts.rxdata")
    return rx is not None and os.path.isfile(rx)

def normalize_game_dir(path):
    """
    Intelligently resolves any provided path (root folder, Data folder,
    or Scripts.rxdata file) into the canonical game root directory.
    """
    if not path:
        return None
    clean = os.path.abspath(path.strip().strip('"').strip("'"))
    if not os.path.exists(clean):
        return None

    # If the user selected Scripts.rxdata directly
    if os.path.isfile(clean) and os.path.basename(clean).lower() == "scripts.rxdata":
        parent = os.path.dirname(clean)
        if os.path.basename(parent).lower() == "data":
            return os.path.dirname(parent)
        return parent

    # If the user selected the Data folder
    if os.path.isdir(clean) and os.path.basename(clean).lower() == "data":
        root = os.path.dirname(clean)
        if has_scripts_file(root):
            return root

    # If the user selected the Game root folder
    if os.path.isdir(clean) and has_scripts_file(clean):
        return clean

    return None

def find_game_directory():
    """
    Locates the Pokemon Fire Ash root directory automatically across all environments.
    Checks CLI arguments, script parent/child dirs, cwd, common locations,
    and provides a native GUI folder chooser or interactive console prompt fallback.
    """
    # 1. Command-line argument (supports drag-and-drop onto script or .exe)
    for arg in sys.argv[1:]:
        if not arg.startswith("-"):
            resolved = normalize_game_dir(arg)
            if resolved:
                return resolved

    # 2. Check script directory hierarchy and current working directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        script_dir,
        os.path.dirname(script_dir),
        os.path.dirname(os.path.dirname(script_dir)),
        os.getcwd(),
        os.path.dirname(os.getcwd())
    ]
    for d in candidates:
        resolved = normalize_game_dir(d)
        if resolved:
            return resolved

    # 3. Check immediate subfolders of cwd and script_dir
    search_roots = [os.getcwd(), script_dir, os.path.dirname(script_dir)]
    for root in search_roots:
        if os.path.exists(root):
            try:
                for entry in os.listdir(root):
                    full_p = os.path.join(root, entry)
                    if os.path.isdir(full_p):
                        resolved = normalize_game_dir(full_p)
                        if resolved:
                            return resolved
            except OSError:
                pass

    # 4. Check common user locations (Downloads, Desktop, Games)
    user_home = os.path.expanduser("~")
    common_folders = [
        os.path.join(user_home, "Downloads"),
        os.path.join(user_home, "Desktop"),
        os.path.join(user_home, "Documents"),
        os.path.join(user_home, "Games"),
        "C:\\Games", "D:\\Games", "E:\\Games"
    ]
    for folder in common_folders:
        if os.path.exists(folder):
            try:
                for entry in os.listdir(folder):
                    if any(k in entry.lower() for k in ["fire ash", "fireash", "pokemon"]):
                        full_p = os.path.join(folder, entry)
                        resolved = normalize_game_dir(full_p)
                        if resolved:
                            return resolved
            except OSError:
                pass

    # 5. Interactive Fallback: Try native GUI folder selector, then console input
    print("\n[*] Could not detect Pokemon Fire Ash directory automatically.")
    
    # Try Tkinter GUI dialog
    try:
        import tkinter as tk
        from tkinter import filedialog
        root_win = tk.Tk()
        root_win.withdraw()
        root_win.attributes("-topmost", True)
        selected_dir = filedialog.askdirectory(title="Select your Pokemon Fire Ash game folder")
        root_win.destroy()
        if selected_dir:
            resolved = normalize_game_dir(selected_dir)
            if resolved:
                return resolved
            else:
                print(f"[!] '{selected_dir}' does not contain Data/Scripts.rxdata.")
    except Exception:
        pass

    # Interactive console prompt
    while True:
        try:
            user_input = input("\nPlease enter or paste the path to your Pokemon Fire Ash folder (or 'q' to quit): ").strip()
        except (EOFError, KeyboardInterrupt):
            return None
        if not user_input or user_input.lower() in ("q", "quit", "exit"):
            return None
        resolved = normalize_game_dir(user_input)
        if resolved:
            return resolved
        print(f"[!] Could not find 'Data/Scripts.rxdata' in '{user_input}'. Please try again.")

def match_newlines(text, reference):
    """Ensures replacement text matches the reference file's newline format."""
    if "\r\n" in reference:
        return text.replace("\r\n", "\n").replace("\n", "\r\n")
    return text.replace("\r\n", "\n")

# ------------------------------------------------------------------------------
# Modular Patch Engine
# ------------------------------------------------------------------------------

def apply_patches(scripts):
    """
    Applies all enhancements to the scripts collection in memory.
    Returns a list of (feature_name, status, details).
    """
    report = []

    def get_section(name):
        for i, s in enumerate(scripts):
            sname = s[1]
            if isinstance(sname, bytes):
                sname = sname.decode("utf-8", errors="ignore")
            if sname == name:
                raw = zlib.decompress(s[2])
                return i, raw.decode("utf-8", errors="replace")
        return None, None

    def set_section(idx, code_str):
        scripts[idx][2] = zlib.compress(code_str.encode("utf-8", errors="replace"))

    # 1. UI_PauseMenu: Debug & One-Click Party Heal
    idx, code = get_section("UI_PauseMenu")
    if idx is not None:
        patched_any = False
        target_dbg = 'commands[cmdDebug = commands.length]     = _INTL("Debug") if $DEBUG'
        repl_dbg   = 'commands[cmdDebug = commands.length]     = _INTL("Debug") if true'
        if target_dbg in code:
            code = code.replace(target_dbg, repl_dbg, 1)
            patched_any = True

        for target_decl, repl_decl in [
            ("cmdPokemon  = -1\r\n", "cmdPokemon  = -1\r\n    cmdHeal     = -1\r\n"),
            ("cmdPokemon  = -1\n",   "cmdPokemon  = -1\n    cmdHeal     = -1\n")
        ]:
            if target_decl in code and "cmdHeal" not in code:
                code = code.replace(target_decl, repl_decl, 1)
                patched_any = True
                break

        pos_pkmn = code.find("commands[cmdPokemon = commands.length]")
        if pos_pkmn != -1 and "cmdHeal = commands.length" not in code:
            eol = code.find("\n", pos_pkmn)
            is_crlf = (code[eol-1] == "\r") if eol > 0 else False
            heal_cmd = "    commands[cmdHeal = commands.length]      = _INTL(\"Heal Party\") if $Trainer.party_count > 0" + ("\r\n" if is_crlf else "\n")
            code = code[:eol+1] + heal_cmd + code[eol+1:]
            patched_any = True

        target_handler = "elsif cmdBag>=0 && command==cmdBag"
        if target_handler in code and "cmdHeal>=0" not in code:
            repl_handler = match_newlines("""elsif cmdHeal>=0 && command==cmdHeal
        pbPlayDecisionSE
        $Trainer.party.each { |pkmn| pkmn.heal }
        pbMEPlay("Pokemon Healing") rescue nil
        pbMessage(_INTL("Your party was fully healed!"))
        @scene.pbRefresh
      elsif cmdBag>=0 && command==cmdBag""", code)
            code = code.replace(target_handler, repl_handler, 1)
            patched_any = True

        set_section(idx, code)
        report.append(("UI_PauseMenu (Debug & Party Heal)", "APPLIED" if patched_any else "ALREADY_PRESENT", "Heal Party + Debug entry"))
    else:
        report.append(("UI_PauseMenu", "SKIPPED", "Section not found"))

    # 2. UI_Party: Debug option on party Pokemon
    idx, code = get_section("UI_Party")
    if idx is not None:
        target = 'commands[cmdDebug = commands.length]        = _INTL("Debug") if $DEBUG'
        repl   = 'commands[cmdDebug = commands.length]        = _INTL("Debug") if true'
        if target in code:
            code = code.replace(target, repl, 1)
            set_section(idx, code)
            report.append(("UI_Party (Debug Option)", "APPLIED", "Debug on party slots"))
        else:
            report.append(("UI_Party (Debug Option)", "ALREADY_PRESENT", "Debug already enabled"))
    else:
        report.append(("UI_Party", "SKIPPED", "Section not found"))

    # 3. UI_PokemonStorage: Debug option on PC box Pokemon
    idx, code = get_section("UI_PokemonStorage")
    if idx is not None:
        target = 'commands[cmdDebug=commands.length]    = _INTL("Debug") if $DEBUG'
        repl   = 'commands[cmdDebug=commands.length]    = _INTL("Debug") if true'
        if target in code:
            code = code.replace(target, repl, 1)
            set_section(idx, code)
            report.append(("UI_PokemonStorage (PC Debug)", "APPLIED", "Debug on PC storage boxes"))
        else:
            report.append(("UI_PokemonStorage (PC Debug)", "ALREADY_PRESENT", "PC Debug already enabled"))
    else:
        report.append(("UI_PokemonStorage", "SKIPPED", "Section not found"))

    # 4. StartGame: Safe $DEBUG = true activation
    idx, code = get_section("StartGame")
    if idx is not None:
        patched = False
        for needle, repl in [
            ("SaveData.load_all_values(save_data)\r\n    self.load_map",
             "SaveData.load_all_values(save_data)\r\n    self.load_map\r\n    $DEBUG = true"),
            ("SaveData.load_all_values(save_data)\n    self.load_map",
             "SaveData.load_all_values(save_data)\n    self.load_map\n    $DEBUG = true"),
            ("self.load_map\r\n    pbMapInterpreter&.setup_starting_event",
             "self.load_map\r\n    $DEBUG = true\r\n    pbMapInterpreter&.setup_starting_event"),
            ("self.load_map\n    pbMapInterpreter&.setup_starting_event",
             "self.load_map\n    $DEBUG = true\n    pbMapInterpreter&.setup_starting_event"),
        ]:
            if needle in code:
                code = code.replace(needle, repl, 1)
                patched = True
                break
        if patched:
            set_section(idx, code)
            report.append(("StartGame (Safe $DEBUG Boot)", "APPLIED", "Activates during save load"))
        else:
            report.append(("StartGame (Safe $DEBUG Boot)", "ALREADY_PRESENT", "Hook already active"))
    else:
        report.append(("StartGame", "SKIPPED", "Section not found"))

    # 5. Pokemon: Always Shiny hook
    idx, code = get_section("Pokemon")
    if idx is not None:
        patched = False
        for needle, repl in [
            ("def shiny?\r\n    return true if square_shiny?\r\n",
             "def shiny?\r\n    return true if square_shiny?\r\n    return true if $ALWAYS_SHINY\r\n"),
            ("def shiny?\n    return true if square_shiny?\n",
             "def shiny?\n    return true if square_shiny?\n    return true if $ALWAYS_SHINY\n")
        ]:
            if needle in code:
                code = code.replace(needle, repl, 1)
                patched = True
                break
        if patched:
            set_section(idx, code)
            report.append(("Pokemon (Always Shiny Hook)", "APPLIED", "Global $ALWAYS_SHINY support"))
        else:
            report.append(("Pokemon (Always Shiny Hook)", "ALREADY_PRESENT", "Hook already present"))
    else:
        report.append(("Pokemon", "SKIPPED", "Section not found"))

    # 6. Overworld_WildEncounters: Infinite Repel hook
    idx, code = get_section("Overworld_WildEncounters")
    if idx is not None:
        patched = False
        for target_repel, repl_repel in [
            ("return false if $DEBUG && Input.press?(Input::CTRL)\r\n",
             "return false if $DEBUG && Input.press?(Input::CTRL)\r\n    return false if $INFINITE_REPEL\r\n"),
            ("return false if $DEBUG && Input.press?(Input::CTRL)\n",
             "return false if $DEBUG && Input.press?(Input::CTRL)\n    return false if $INFINITE_REPEL\n")
        ]:
            if target_repel in code and "$INFINITE_REPEL" not in code:
                code = code.replace(target_repel, repl_repel, 1)
                patched = True
                break
        if patched:
            set_section(idx, code)
            report.append(("Overworld_WildEncounters (Infinite Repel)", "APPLIED", "Global $INFINITE_REPEL support"))
        else:
            report.append(("Overworld_WildEncounters (Infinite Repel)", "ALREADY_PRESENT", "Hook already present"))
    else:
        report.append(("Overworld_WildEncounters", "SKIPPED", "Section not found"))

    # 7. UI_EggHatching: 1-Step Egg Hatching hook
    idx, code = get_section("UI_EggHatching")
    if idx is not None:
        patched = False
        for target_egg, repl_egg in [
            ("next if egg.steps_to_hatch <= 0\r\n    egg.steps_to_hatch -= 1",
             "next if egg.steps_to_hatch <= 0\r\n    egg.steps_to_hatch = 1 if $FAST_EGG_HATCH\r\n    egg.steps_to_hatch -= 1"),
            ("next if egg.steps_to_hatch <= 0\n    egg.steps_to_hatch -= 1",
             "next if egg.steps_to_hatch <= 0\n    egg.steps_to_hatch = 1 if $FAST_EGG_HATCH\n    egg.steps_to_hatch -= 1")
        ]:
            if target_egg in code and "$FAST_EGG_HATCH" not in code:
                code = code.replace(target_egg, repl_egg, 1)
                patched = True
                break
        if patched:
            set_section(idx, code)
            report.append(("UI_EggHatching (1-Step Egg Hatch)", "APPLIED", "Global $FAST_EGG_HATCH support"))
        else:
            report.append(("UI_EggHatching (1-Step Egg Hatch)", "ALREADY_PRESENT", "Hook already present"))
    else:
        report.append(("UI_EggHatching", "SKIPPED", "Section not found"))

    # 8. Debug_MenuCommands: Toggles for Shiny, 1-Step Hatch, Infinite Repel, Game Speed
    idx, code = get_section("Debug_MenuCommands")
    if idx is not None:
        patched = False
        target_warp = 'DebugMenuCommands.register("warp", {'
        field_toggles = match_newlines('''DebugMenuCommands.register("infiniterepel", {
  "parent"      => "fieldmenu",
  "name"        => _INTL("Infinite Repel: [Toggle]"),
  "description" => _INTL("Toggle whether all wild Pokemon encounters are prevented."),
  "effect"      => proc {
    $INFINITE_REPEL = !$INFINITE_REPEL
    pbMessage(_INTL("Infinite Repel is now {1}.", $INFINITE_REPEL ? "ON" : "OFF"))
  }
})

DebugMenuCommands.register("gamespeed", {
  "parent"      => "fieldmenu",
  "name"        => _INTL("Game Speed: [Toggle]"),
  "description" => _INTL("Cycle speed between 1x, 2x, and 3x (also toggled via F7 or M)."),
  "effect"      => proc {
    $GameSpeed = ($GameSpeed || 1) + 1
    $GameSpeed = 1 if $GameSpeed >= 4
    save_speed_setting($GameSpeed) if defined?(save_speed_setting)
    pbMessage(_INTL("Game Speed is now {1}x.", $GameSpeed))
  }
})

DebugMenuCommands.register("warp", {''', code)
        if target_warp in code and 'infiniterepel' not in code:
            code = code.replace(target_warp, field_toggles, 1)
            patched = True

        target_pkmn = 'DebugMenuCommands.register("addpokemon", {'
        pkmn_toggles = match_newlines('''DebugMenuCommands.register("alwaysshiny", {
  "parent"      => "pokemonmenu",
  "name"        => _INTL("Always Shiny: [Toggle]"),
  "description" => _INTL("Toggle whether all wild Pokemon and gifts are guaranteed to be shiny."),
  "effect"      => proc {
    $ALWAYS_SHINY = !$ALWAYS_SHINY
    pbMessage(_INTL("Always Shiny mode is now {1}.", $ALWAYS_SHINY ? "ON" : "OFF"))
  }
})

DebugMenuCommands.register("fastegghatch", {
  "parent"      => "pokemonmenu",
  "name"        => _INTL("1-Step Egg Hatch: [Toggle]"),
  "description" => _INTL("Toggle whether eggs in your party hatch in a single step."),
  "effect"      => proc {
    $FAST_EGG_HATCH = !$FAST_EGG_HATCH
    pbMessage(_INTL("1-Step Egg Hatching is now {1}.", $FAST_EGG_HATCH ? "ON" : "OFF"))
  }
})

DebugMenuCommands.register("addpokemon", {''', code)
        if target_pkmn in code and 'alwaysshiny' not in code:
            code = code.replace(target_pkmn, pkmn_toggles, 1)
            patched = True

        if patched:
            set_section(idx, code)
            report.append(("Debug_MenuCommands (Custom Toggles)", "APPLIED", "Field & Pokemon debug toggles"))
        else:
            report.append(("Debug_MenuCommands (Custom Toggles)", "ALREADY_PRESENT", "Toggles already registered"))
    else:
        report.append(("Debug_MenuCommands", "SKIPPED", "Section not found"))

    # 9. Editor_Listers: Smart fuzzy search for Add Item & Warp to Map
    idx, code = get_section("Editor_Listers")
    if idx is not None:
        start_needle = "def pbListScreen(title,lister)"
        if start_needle not in code:
            start_needle = "def pbListScreen(title, lister)"
        end_needle = "#===============================================================================\r\n#\r\n#===============================================================================\r\nclass GraphicsLister"
        if end_needle not in code:
            end_needle = "#===============================================================================\n#\n#===============================================================================\nclass GraphicsLister"
        p1 = code.find(start_needle)
        p2 = code.find(end_needle, p1)
        if p1 != -1 and p2 != -1:
            nl = "\r\n" if "\r\n" in code else "\n"
            injected = match_newlines(RUBY_LISTERS_CODE, code)
            code = code[:p1] + injected + (nl * 2) + code[p2:]
            set_section(idx, code)
            report.append(("Editor_Listers (Smart Search)", "APPLIED", "Warp to Map & Add Item search"))
        else:
            report.append(("Editor_Listers (Smart Search)", "ALREADY_PRESENT", "Search already active"))
    else:
        report.append(("Editor_Listers", "SKIPPED", "Section not found"))

    # 10. Editor_Utilities: Smart fuzzy search for Add Pokemon, Moves, Abilities
    idx, code = get_section("Editor_Utilities")
    if idx is not None:
        start_needle = "def pbChooseList(commands, default = 0, cancelValue = -1, sortType = 1)"
        p1 = code.find(start_needle)
        if p1 != -1:
            p2 = code.find("\nend\r\n", p1)
            end_offset = 6
            if p2 == -1:
                p2 = code.find("\nend\n", p1)
                end_offset = 5
            if p2 != -1:
                injected = match_newlines(RUBY_CHOOSELIST_CODE, code)
                code = code[:p1] + injected + code[p2 + end_offset:]
                set_section(idx, code)
                report.append(("Editor_Utilities (Smart Search)", "APPLIED", "Add Pokemon/Moves/Abilities search"))
            else:
                report.append(("Editor_Utilities (Smart Search)", "SKIPPED", "Could not locate end marker"))
        else:
            report.append(("Editor_Utilities (Smart Search)", "ALREADY_PRESENT", "Search already active"))
    else:
        report.append(("Editor_Utilities", "SKIPPED", "Section not found"))

    # 11. Debug_PokemonCommands: Safe Shadow Pokemon error rescue
    idx, code = get_section("Debug_PokemonCommands")
    if idx is not None:
        safe_shadow = match_newlines('''when 0   # Make Shadow
        if !pkmn.shadowPokemon?
          begin
            pkmn.makeShadow
            screen.pbRefreshSingle(pkmnid)
            screen.pbDisplay(_INTL("{1} became a Shadow Pokemon.", pkmn.name))
          rescue => e
            pkmn.shadow = false
            pkmn.heart_gauge = nil
            pkmn.shadow_moves = nil
            screen.pbDisplay(_INTL("This Pokemon cannot be converted into a Shadow Pokemon."))
          end
        else
          screen.pbDisplay(_INTL("{1} is already a Shadow Pokemon.", pkmn.name))
        end''', code)
        patched = False
        for needle in [
            "when 0   # Make Shadow\r\n        if !pkmn.shadowPokemon?\r\n          pkmn.makeShadow\r\n          screen.pbRefreshSingle(pkmnid)\r\n        else\r\n          screen.pbDisplay(_INTL(\"{1} is already a Shadow",
            "when 0   # Make Shadow\n        if !pkmn.shadowPokemon?\n          pkmn.makeShadow\n          screen.pbRefreshSingle(pkmnid)\n        else\n          screen.pbDisplay(_INTL(\"{1} is already a Shadow"
        ]:
            pos = code.find(needle)
            if pos != -1:
                end_pos = code.find("end", pos + len(needle))
                if end_pos != -1:
                    code = code[:pos] + safe_shadow + code[end_pos + 3:]
                    set_section(idx, code)
                    patched = True
                    break
        if patched:
            report.append(("Debug_PokemonCommands (Shadow Catch)", "APPLIED", "Safe in-game dialog"))
        else:
            report.append(("Debug_PokemonCommands (Shadow Catch)", "ALREADY_PRESENT", "Rescue already active"))
    else:
        report.append(("Debug_PokemonCommands", "SKIPPED", "Section not found"))

    # 12. Pokemon_ShadowPokemon: Pre-validate moves before mutating Pokemon state
    idx, code = get_section("Pokemon_ShadowPokemon")
    if idx is not None:
        safe_make_shadow = match_newlines('''  def makeShadow
    # Retrieve Shadow moveset for this Pokemon
    shadow_moveset = pbLoadShadowMovesets[species_data.id]
    shadow_moveset = pbLoadShadowMovesets[@species] if !shadow_moveset || shadow_moveset.length == 0
    # Record this Pokemon's Shadow moves
    temp_moves = []
    if shadow_moveset && shadow_moveset.length > 0
      for i in 0...[shadow_moveset.length, MAX_MOVES].min
        temp_moves[i] = shadow_moveset[i]
      end
    elsif GameData::Move.exists?(:SHADOWRUSH)
      # No Shadow moveset defined; just use Shadow Rush
      temp_moves[0] = :SHADOWRUSH
    else
      raise _INTL("Expected Shadow moves or Shadow Rush to be defined, but they weren't.")
    end
    @shadow       = true
    @heart_gauge  = HEART_GAUGE_SIZE
    @hyper_mode   = false
    @saved_exp    = 0
    @saved_ev     = {}
    GameData::Stat.each_main { |s| @saved_ev[s.id] = 0 }
    @shadow_moves = temp_moves''', code)
        pos = code.find("def makeShadow")
        needle_end = "raise _INTL(\"Expected Shadow moves or Shadow Rush to be defined, but they weren't.\")\r\n    end"
        if needle_end not in code:
            needle_end = "raise _INTL(\"Expected Shadow moves or Shadow Rush to be defined, but they weren't.\")\n    end"
        pos2 = code.find(needle_end, pos)
        if pos != -1 and pos2 != -1:
            code = code[:pos] + safe_make_shadow + code[pos2 + len(needle_end):]
            set_section(idx, code)
            report.append(("Pokemon_ShadowPokemon (Fallback)", "APPLIED", "Shadow Rush fallback handler"))
        else:
            report.append(("Pokemon_ShadowPokemon (Fallback)", "ALREADY_PRESENT", "Fallback already in place"))
    else:
        report.append(("Pokemon_ShadowPokemon", "SKIPPED", "Section not found"))

    return report

# ------------------------------------------------------------------------------
# Main Entry Point
# ------------------------------------------------------------------------------

def main():
    print("=" * 68)
    print("  Pokemon Fire Ash - Universal Debug & QoL Patcher")
    print("=" * 68)

    # Check for restore / uninstall argument
    is_restore = any(arg in sys.argv for arg in ("--restore", "--uninstall", "-r"))

    # Locate game directory
    game_dir = find_game_directory()
    if not game_dir:
        print("[!] Error: Could not locate Pokemon Fire Ash folder.")
        print("[!] Usage: python apply_debug_patch.py [path_to_game_folder]")
        sys.exit(1)

    print(f"[+] Target Game Folder: {game_dir}")

    # Case-insensitive script resolution
    rx_path = find_case_insensitive_path(game_dir, "data", "scripts.rxdata")
    if not rx_path:
        print(f"[!] Error: Could not find 'Data/Scripts.rxdata' in '{game_dir}'.")
        sys.exit(1)

    data_dir = os.path.dirname(rx_path)
    backup_path = os.path.join(data_dir, "Scripts_original_backup.rxdata")

    # Handle Restore / Uninstall
    if is_restore:
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, rx_path)
            print(f"[+] Successfully restored vanilla Scripts.rxdata from backup!")
            print(f"[+] Restored: {rx_path}")
        else:
            print(f"[!] No backup file found at: {backup_path}")
        return

    # 1. Ensure original backup exists before any modifications
    if not os.path.exists(backup_path):
        shutil.copy2(rx_path, backup_path)
        print(f"[+] Original backup created: {backup_path}")
    else:
        print(f"[*] Preserving existing original backup: {backup_path}")

    # 2. Always patch from clean backup to guarantee idempotency and no duplicates
    with open(backup_path, "rb") as f:
        scripts = rubymarshal.reader.load(f)

    # 3. Apply all patches
    report = apply_patches(scripts)

    # 4. Serialize and write back
    dumped = rubymarshal.writer.writes(scripts)
    assert len(rubymarshal.reader.loads(dumped)) == len(scripts), "Integrity verification failed!"

    with open(rx_path, "wb") as f:
        f.write(dumped)
    print(f"[+] Successfully patched: {rx_path} ({len(dumped):,} bytes)")

    # 5. Fix missing custom Lucarionite2 icon if present
    items_dir = find_case_insensitive_path(game_dir, "graphics", "items")
    if items_dir:
        src_icon = find_case_insensitive_path(items_dir, "lucarionite.png")
        dst_icon = find_case_insensitive_path(items_dir, "lucarionite2.png")
        if src_icon and not dst_icon:
            target_dst = os.path.join(items_dir, "LUCARIONITE2.png")
            shutil.copy2(src_icon, target_dst)
            print("[+] Fixed custom Lucarionite2 sprite icon.")

    # 6. Detailed Patch Summary
    print("\n" + "=" * 68)
    print(" PATCH STATUS REPORT:")
    print("=" * 68)
    for name, status, detail in report:
        icon = "[+]" if status == "APPLIED" else ("[*]" if status == "ALREADY_PRESENT" else "[!]")
        print(f" {icon} {name:<42} : {status} ({detail})")

    print("\n" + "=" * 68)
    print(" ALL FEATURES & QoL ENHANCEMENTS READY!")
    print("=" * 68)
    print(" Controls & Features:")
    print("  - Pause Menu: 'Heal Party' for instant full restore (HP, PP, status).")
    print("  - Pause Menu / Party / PC Boxes: Click any Pokemon -> 'Debug'.")
    print("  - Search Filter: Press [Z] / [Shift] at any time to search.")
    print("  - Infinite Repel: Debug Menu -> Field options -> Infinite Repel.")
    print("  - 1-Step Egg Hatch: Debug Menu -> Pokemon options -> 1-Step Egg Hatch.")
    print("  - Game Speed: Debug Menu -> Field options -> Game Speed (or F7 / M).")
    print("  - Always Shiny: Debug Menu -> Pokemon options -> Always Shiny.")
    print("  - Walk Through Walls: Hold [Ctrl] in overworld.")
    print("  - To revert anytime: python apply_debug_patch.py --restore")
    print("=" * 68)

if __name__ == "__main__":
    main()
