namespace FireAsh.Edit.Pc;

internal sealed class MainForm : Form
{
    private readonly AppSettings _settings = AppSettings.Load();
    private Label _folderLabel = null!;
    private TextBox _log = null!;
    private Button _btnPick = null!;
    private Button _btnScan = null!;
    private Button _btnAdd = null!;
    private Button _btnRemove = null!;
    private bool _busy;

    public MainForm()
    {
        Text = "FireAsh.Edit (Windows)";
        Width = 720;
        Height = 520;
        StartPosition = FormStartPosition.CenterScreen;
        MinimumSize = new Size(560, 400);

        var padding = 10;
        var y = padding;

        _folderLabel = new Label
        {
            AutoSize = false,
            Left = padding,
            Top = y,
            Width = ClientSize.Width - 2 * padding,
            Height = 40,
            Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right,
        };
        y += _folderLabel.Height + 6;

        _btnPick = new Button
        {
            Text = "Choose game folder",
            Left = padding,
            Top = y,
            Width = 160,
        };
        _btnPick.Click += (_, _) => PickGameFolder();
        _btnScan = new Button
        {
            Text = "Scan Downloads",
            Left = _btnPick.Right + 8,
            Top = y,
            Width = 140,
        };
        _btnScan.Click += (_, _) => ScanDownloads(manual: true);
        y += _btnPick.Height + 10;

        _btnAdd = new Button
        {
            Text = "Add mods",
            Left = padding,
            Top = y,
            Width = 120,
        };
        _btnAdd.Click += async (_, _) => await RunAddModsAsync();
        _btnRemove = new Button
        {
            Text = "Remove mods",
            Left = _btnAdd.Right + 8,
            Top = y,
            Width = 120,
        };
        _btnRemove.Click += async (_, _) => await RunRemoveModsAsync();
        y += _btnAdd.Height + 10;

        var hint = new Label
        {
            Text =
                "Supported game: Pokémon Fire Ash 3.6 Part 2.2 only. Pick the folder that contains the Data folder " +
                "(same as on Android). Add mods creates Data/Scripts.rxdata.backup once. Remove mods restores only " +
                "from that backup.",
            Left = padding,
            Top = y,
            Width = ClientSize.Width - 2 * padding,
            Height = 56,
            Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right,
        };
        y += hint.Height + 6;

        var logCaption = new Label
        {
            Text = "Log (for troubleshooting):",
            Left = padding,
            Top = y,
            AutoSize = true,
        };
        y += logCaption.Height + 4;

        _log = new TextBox
        {
            Multiline = true,
            ReadOnly = true,
            ScrollBars = ScrollBars.Vertical,
            Font = new Font(FontFamily.GenericMonospace, 9f),
            Left = padding,
            Top = y,
            Width = ClientSize.Width - 2 * padding,
            Height = ClientSize.Height - y - padding,
            Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right,
            TabStop = false,
        };

        Controls.AddRange(new Control[]
        {
            _folderLabel, _btnPick, _btnScan, _btnAdd, _btnRemove, hint, logCaption, _log,
        });

        Load += (_, _) => OnFirstShown();
    }

    private void OnFirstShown()
    {
        UpdateFolderDisplay();
        Log("Started. This PC build only searches your Windows Downloads folder for a game with Data/Scripts.rxdata.");
        if (string.IsNullOrWhiteSpace(_settings.GameRootPath))
            ScanDownloads(manual: false);
        else
            Log($"Using saved game folder from last time. Use \"Scan Downloads\" or \"Choose game folder\" to change.");
    }

    private void UpdateFolderDisplay()
    {
        var p = _settings.GameRootPath;
        _folderLabel.Text = string.IsNullOrWhiteSpace(p)
            ? "Game folder: (none — choose a folder or scan Downloads)"
            : $"Game folder: {p}";
    }

    private void Log(string line)
    {
        var t = $"{DateTime.Now:HH:mm:ss}  {line}";
        if (_log.TextLength == 0)
            _log.Text = t;
        else
            _log.AppendText(Environment.NewLine + t);
        _log.SelectionStart = _log.TextLength;
        _log.ScrollToCaret();
    }

    private void PickGameFolder()
    {
        using var d = new FolderBrowserDialog
        {
            Description = "Select the folder that contains the Data folder (next to Game.exe).",
            UseDescriptionForTitle = true,
            InitialDirectory = TryGetInitialBrowsePath(),
        };
        if (d.ShowDialog(this) != DialogResult.OK)
            return;
        SetGameRoot(d.SelectedPath, save: true);
        Log($"You chose: {d.SelectedPath}");
    }

    private string? TryGetInitialBrowsePath()
    {
        if (!string.IsNullOrWhiteSpace(_settings.GameRootPath) && Directory.Exists(_settings.GameRootPath))
            return _settings.GameRootPath;
        return DownloadsGameLocator.GetDownloadsDirectory()
            ?? Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), "Downloads");
    }

    private void SetGameRoot(string path, bool save)
    {
        _settings.GameRootPath = path.TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
        if (save)
            _settings.Save();
        UpdateFolderDisplay();
    }

    private void ScanDownloads(bool manual)
    {
        var downloads = DownloadsGameLocator.GetDownloadsDirectory()
            ?? Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), "Downloads");
        Log($"Downloads folder (internet downloads location): {downloads}");

        if (!Directory.Exists(downloads))
        {
            Log("Downloads folder does not exist or is not reachable. Use \"Choose game folder\".");
            if (manual)
                MessageBox.Show(this,
                    "Your Downloads folder could not be opened. Use \"Choose game folder\" and point at the game.",
                    Text, MessageBoxButtons.OK, MessageBoxIcon.Information);
            return;
        }

        var archives = DownloadsGameLocator.FindFireAshArchivesInDownloadsRoot(downloads);
        var roots = DownloadsGameLocator.FindGameRootsUnderDownloads(downloads).ToList();

        if (archives.Count > 0)
            Log($"Found {archives.Count} archive(s) in Downloads that look like Fire Ash (by name): {string.Join("; ", archives.Select(Path.GetFileName))}");

        if (roots.Count == 0)
        {
            if (archives.Count > 0)
            {
                Log("No unzipped game (Data/Scripts.rxdata) found under Downloads.");
                MessageBox.Show(this,
                    "A compressed file that looks like Pokémon Fire Ash was found in your Downloads folder, " +
                    "but the game is not unzipped there yet.\n\n" +
                    "Please unzip the game into your Downloads folder first. Keep the zip file if you want a clean backup copy. " +
                    "Then click \"Scan Downloads\" again or use \"Choose game folder\".",
                    "Unzip the game first",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Information);
            }
            else
            {
                Log("No Fire Ash-style archive and no Data/Scripts.rxdata found under Downloads.");
                if (manual)
                    MessageBox.Show(this,
                        "Nothing that looks like Pokémon Fire Ash was found under Downloads. " +
                        "Use \"Choose game folder\" to select your install.",
                        Text,
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information);
            }
            return;
        }

        var preferred = roots.Where(DownloadsGameLocator.LooksLikeFireAshPath).ToList();
        var pool = preferred.Count > 0 ? preferred : roots;
        Log($"Found {roots.Count} folder(s) with Data/Scripts.rxdata under Downloads" +
            (preferred.Count > 0 ? $" ({preferred.Count} have \"fire\" and \"ash\" in the path)." : "."));

        string? chosen;
        if (pool.Count == 1)
        {
            chosen = pool[0];
            Log($"Using the only matching folder: {chosen}");
        }
        else
        {
            chosen = ShowFolderPicker(pool, "More than one game-like folder was found under Downloads. Pick one:");
            if (chosen == null)
            {
                Log("Scan cancelled — no folder selected.");
                return;
            }
            Log($"You selected: {chosen}");
        }

        SetGameRoot(chosen, save: true);
        if (archives.Count > 0)
            Log("Tip: Keeping the zip in Downloads is fine for a clean reinstall; the app uses the unzipped folder.");

        if (manual)
            MessageBox.Show(this, "Game folder set. You can use Add mods or Remove mods.", Text, MessageBoxButtons.OK, MessageBoxIcon.Information);
    }

    private static string? ShowFolderPicker(IReadOnlyList<string> paths, string title)
    {
        using var f = new Form
        {
            Text = "Choose folder",
            Width = 640,
            Height = 400,
            StartPosition = FormStartPosition.CenterParent,
            FormBorderStyle = FormBorderStyle.FixedDialog,
            MaximizeBox = false,
            MinimizeBox = false,
        };
        string? result = null;
        var lbl = new Label
        {
            Text = title,
            Dock = DockStyle.Top,
            AutoSize = false,
            Height = 52,
            Padding = new Padding(8),
        };
        var list = new ListBox { Dock = DockStyle.Fill, IntegralHeight = false };
        foreach (var p in paths)
            list.Items.Add(p);
        var panel = new FlowLayoutPanel
        {
            Dock = DockStyle.Bottom,
            Height = 44,
            FlowDirection = FlowDirection.RightToLeft,
            Padding = new Padding(8),
        };
        var ok = new Button { Text = "OK", DialogResult = DialogResult.OK, Width = 88 };
        var cancel = new Button { Text = "Cancel", DialogResult = DialogResult.Cancel, Width = 88 };
        panel.Controls.Add(ok);
        panel.Controls.Add(cancel);
        f.Controls.Add(panel);
        f.Controls.Add(lbl);
        f.Controls.Add(list);
        f.AcceptButton = ok;
        f.CancelButton = cancel;
        if (list.Items.Count > 0)
            list.SelectedIndex = 0;
        if (f.ShowDialog() == DialogResult.OK && list.SelectedItem is string s)
            result = s;
        return result;
    }

    private void SetBusy(bool busy)
    {
        _busy = busy;
        _btnPick.Enabled = !busy;
        _btnScan.Enabled = !busy;
        _btnAdd.Enabled = !busy;
        _btnRemove.Enabled = !busy;
        UseWaitCursor = busy;
    }

    private async Task RunAddModsAsync()
    {
        if (_busy)
            return;
        var root = _settings.GameRootPath;
        if (string.IsNullOrWhiteSpace(root))
        {
            MessageBox.Show(this, "Choose the game folder first (or scan Downloads).", Text, MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        var confirm = MessageBox.Show(this,
            "This app only supports Pokémon Fire Ash 3.6 Part 2.2. Installing on any other game version can break the game or saves.\n\n" +
            "Continue only if that is exactly what you are playing.",
            "Supported version",
            MessageBoxButtons.OKCancel,
            MessageBoxIcon.Warning);
        if (confirm != DialogResult.OK)
            return;

        var patchedPath = Path.Combine(AppContext.BaseDirectory, "patched_Scripts.rxdata");
        if (!File.Exists(patchedPath))
        {
            Log($"ERROR: Missing {patchedPath}. Rebuild the app from the repo after running sync_patched_scripts_to_apk.ps1.");
            MessageBox.Show(this,
                "patched_Scripts.rxdata was not found next to this program. Reinstall from a fresh build.",
                Text,
                MessageBoxButtons.OK,
                MessageBoxIcon.Error);
            return;
        }

        SetBusy(true);
        try
        {
            await Task.Run(() =>
            {
                var bytes = File.ReadAllBytes(patchedPath);
                ScriptPatchOperations.InstallPatch(root, bytes, msg => BeginInvoke(() => Log(msg)));
            });
            Log("Done.");
            MessageBox.Show(this, "Add mods completed successfully.", Text, MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
        catch (Exception ex)
        {
            Log("ERROR: " + ex.Message);
            MessageBox.Show(this, ex.Message, Text, MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
        finally
        {
            SetBusy(false);
        }
    }

    private async Task RunRemoveModsAsync()
    {
        if (_busy)
            return;
        var root = _settings.GameRootPath;
        if (string.IsNullOrWhiteSpace(root))
        {
            MessageBox.Show(this, "Choose the game folder first (or scan Downloads).", Text, MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        SetBusy(true);
        try
        {
            await Task.Run(() =>
            {
                ScriptPatchOperations.RemoveMods(root, msg => BeginInvoke(() => Log(msg)));
            });
            Log("Done.");
            MessageBox.Show(this, "Remove mods completed successfully.", Text, MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
        catch (Exception ex)
        {
            Log("ERROR: " + ex.Message);
            MessageBox.Show(this, ex.Message, Text, MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
        finally
        {
            SetBusy(false);
        }
    }

    protected override void OnResize(EventArgs e)
    {
        base.OnResize(e);
        if (_folderLabel != null)
            _folderLabel.Width = ClientSize.Width - 20;
    }
}
