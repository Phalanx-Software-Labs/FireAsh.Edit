namespace FireAsh.Edit.Pc;

/// <summary>
/// Same rules as the Android app: backup once, replace Scripts.rxdata; remove restores from backup only.
/// </summary>
internal static class ScriptPatchOperations
{
    private const string PatchTempName = "patchtmp.rxdata";

    public static string ResolveDataDirectory(string gameRoot)
    {
        var root = Path.GetFullPath(gameRoot.Trim());
        var data = Path.Combine(root, "Data");
        if (!Directory.Exists(data))
        {
            var alt = Path.Combine(root, "data");
            if (Directory.Exists(alt))
                data = alt;
        }
        if (!Directory.Exists(data))
            throw new InvalidOperationException(
                "No Data folder here. Pick the folder that contains Data (next to Game.exe / mkxp).");
        return data;
    }

    public static void EnsureScriptsExists(string dataDir)
    {
        var scripts = Path.Combine(dataDir, "Scripts.rxdata");
        if (!File.Exists(scripts))
            throw new InvalidOperationException($"Missing Data file: {scripts}");
    }

    public static void InstallPatch(string gameRoot, byte[] patchedBytes, Action<string>? log)
    {
        if (patchedBytes.Length == 0)
            throw new InvalidOperationException("Patched script file is empty.");

        var dataDir = ResolveDataDirectory(gameRoot);
        EnsureScriptsExists(dataDir);

        var scriptsPath = Path.Combine(dataDir, "Scripts.rxdata");
        var backupPath = Path.Combine(dataDir, "Scripts.rxdata.backup");

        if (File.Exists(scriptsPath) && !File.Exists(backupPath))
        {
            log?.Invoke("Creating Scripts.rxdata.backup from your current Scripts.rxdata (one time).");
            File.Copy(scriptsPath, backupPath, overwrite: false);
        }
        else if (File.Exists(backupPath))
            log?.Invoke("Scripts.rxdata.backup already exists — not overwriting (keeps your first backup).");

        var tmpPath = Path.Combine(dataDir, PatchTempName);
        DeleteIfPresent(tmpPath, log);
        File.WriteAllBytes(tmpPath, patchedBytes);
        log?.Invoke($"Wrote temp {PatchTempName}.");

        TryDeleteWithRetry(scriptsPath, log);
        TryMoveOrReplace(tmpPath, scriptsPath, log);
        log?.Invoke("Add mods finished: Data/Scripts.rxdata is now the patched file.");
    }

    public static void RemoveMods(string gameRoot, Action<string>? log)
    {
        var dataDir = ResolveDataDirectory(gameRoot);
        var scriptsPath = Path.Combine(dataDir, "Scripts.rxdata");
        var backupPath = Path.Combine(dataDir, "Scripts.rxdata.backup");

        if (File.Exists(backupPath) && new FileInfo(backupPath).Length > 0)
        {
            log?.Invoke("Restoring from Scripts.rxdata.backup.");
            RestoreFromBackup(dataDir, scriptsPath, backupPath, log);
            log?.Invoke("Remove mods finished: restored from backup.");
            return;
        }

        throw new InvalidOperationException(
            "No Scripts.rxdata.backup found. Use Add mods once while Scripts.rxdata is still vanilla to create that backup.");
    }

    private static void RestoreFromBackup(
        string dataDir,
        string scriptsPath,
        string backupPath,
        Action<string>? log)
    {
        TryDeleteWithRetry(scriptsPath, log);
        try
        {
            File.Move(backupPath, scriptsPath);
            log?.Invoke("Renamed Scripts.rxdata.backup → Scripts.rxdata.");
        }
        catch (IOException)
        {
            File.Copy(backupPath, scriptsPath, overwrite: true);
            log?.Invoke("Copied backup to Scripts.rxdata (rename not available).");
            TryDeleteWithRetry(backupPath, log);
        }
    }

    private static void TryMoveOrReplace(string tmpPath, string scriptsPath, Action<string>? log)
    {
        try
        {
            File.Move(tmpPath, scriptsPath);
            log?.Invoke("Renamed temp file to Scripts.rxdata.");
        }
        catch (IOException)
        {
            File.Copy(tmpPath, scriptsPath, overwrite: true);
            log?.Invoke("Copied temp file to Scripts.rxdata.");
            DeleteIfPresent(tmpPath, log);
        }
    }

    private static void DeleteIfPresent(string path, Action<string>? log)
    {
        if (!File.Exists(path))
            return;
        TryDeleteWithRetry(path, log);
    }

    private static void TryDeleteWithRetry(string path, Action<string>? log)
    {
        const int attempts = 8;
        for (var i = 0; i < attempts; i++)
        {
            try
            {
                if (!File.Exists(path))
                    return;
                File.Delete(path);
                log?.Invoke($"Deleted {Path.GetFileName(path)}.");
                return;
            }
            catch (IOException ex)
            {
                if (i == attempts - 1)
                    throw new InvalidOperationException(
                        "Could not replace or delete Scripts.rxdata. Close the game and any launcher " +
                        "so the file is not in use, then try again.",
                        ex);
                Thread.Sleep(250 * (i + 1));
            }
            catch (UnauthorizedAccessException ex)
            {
                if (i == attempts - 1)
                    throw new InvalidOperationException(
                        "Access denied on Scripts.rxdata. Close the game and try again, or run as your normal user with folder permissions.",
                        ex);
                Thread.Sleep(250 * (i + 1));
            }
        }
    }
}
