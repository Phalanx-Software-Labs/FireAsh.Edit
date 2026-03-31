using System.Runtime.InteropServices;

namespace FireAsh.Edit.Pc;

/// <summary>
/// Locates the game only under the Windows Downloads known folder (the default place
/// browsers store files from the internet — one folder tree on one drive).
/// </summary>
internal static class DownloadsGameLocator
{
    private static readonly Guid DownloadsFolderId = new("374DE290-123F-4565-9164-39C4925E467B");

    [DllImport("shell32.dll", CharSet = CharSet.Unicode, ExactSpelling = true)]
    private static extern int SHGetKnownFolderPath(
        [MarshalAs(UnmanagedType.LPStruct)] Guid rfid,
        uint dwFlags,
        IntPtr hToken,
        out IntPtr pszPath);

    public static string? GetDownloadsDirectory()
    {
        var hr = SHGetKnownFolderPath(DownloadsFolderId, 0, IntPtr.Zero, out var ptr);
        if (hr != 0 || ptr == IntPtr.Zero)
            return null;
        try
        {
            return Marshal.PtrToStringUni(ptr);
        }
        finally
        {
            Marshal.FreeCoTaskMem(ptr);
        }
    }

    /// <summary>File name looks like a Fire Ash archive (zip/rar/7z).</summary>
    public static bool LooksLikeFireAshArchive(string fileName)
    {
        var n = Path.GetFileNameWithoutExtension(fileName).ToLowerInvariant();
        return n.Contains("fire") && n.Contains("ash");
    }

    /// <summary>Folder segment suggests Fire Ash (loose match for fan releases).</summary>
    public static bool LooksLikeFireAshPath(string fullPath)
    {
        var s = fullPath.ToLowerInvariant();
        if (s.Contains("fireash"))
            return true;
        return s.Contains("fire") && s.Contains("ash");
    }

    /// <summary>
    /// Top-level archives in Downloads that look like Fire Ash.
    /// </summary>
    public static IReadOnlyList<string> FindFireAshArchivesInDownloadsRoot(string downloadsRoot)
    {
        var list = new List<string>();
        if (!Directory.Exists(downloadsRoot))
            return list;
        foreach (var ext in new[] { "*.zip", "*.rar", "*.7z" })
        {
            foreach (var f in Directory.EnumerateFiles(downloadsRoot, ext, SearchOption.TopDirectoryOnly))
            {
                if (LooksLikeFireAshArchive(f))
                    list.Add(f);
            }
        }
        return list;
    }

    /// <summary>
    /// Folders under Downloads that contain Data/Scripts.rxdata. Search stays inside Downloads only.
    /// </summary>
    public static IReadOnlyList<string> FindGameRootsUnderDownloads(
        string downloadsRoot,
        int maxDepth = 12,
        int maxDirectoriesVisited = 25_000)
    {
        var results = new List<string>();
        if (!Directory.Exists(downloadsRoot))
            return results;

        var visited = 0;
        var queue = new Queue<(string Path, int Depth)>();
        queue.Enqueue((downloadsRoot, 0));

        while (queue.Count > 0 && visited < maxDirectoriesVisited)
        {
            var (dir, depth) = queue.Dequeue();
            visited++;

            var scripts = Path.Combine(dir, "Data", "Scripts.rxdata");
            if (File.Exists(scripts))
                results.Add(dir);

            if (depth >= maxDepth)
                continue;

            try
            {
                foreach (var sub in Directory.EnumerateDirectories(dir))
                    queue.Enqueue((sub, depth + 1));
            }
            catch (UnauthorizedAccessException)
            {
                /* skip */
            }
            catch (IOException)
            {
                /* skip */
            }
        }

        return results.Distinct(StringComparer.OrdinalIgnoreCase).ToList();
    }
}
