using System.Text.Json;

namespace FireAsh.Edit.Pc;

internal sealed class AppSettings
{
    public string? GameRootPath { get; set; }

    private static string SettingsPath =>
        Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "PhalanxLabs",
            "FireAsh.Edit",
            "settings.json");

    public static AppSettings Load()
    {
        try
        {
            var p = SettingsPath;
            if (!File.Exists(p))
                return new AppSettings();
            var json = File.ReadAllText(p);
            var s = JsonSerializer.Deserialize<AppSettings>(json);
            return s ?? new AppSettings();
        }
        catch
        {
            return new AppSettings();
        }
    }

    public void Save()
    {
        var dir = Path.GetDirectoryName(SettingsPath);
        if (!string.IsNullOrEmpty(dir))
            Directory.CreateDirectory(dir);
        var json = JsonSerializer.Serialize(this, new JsonSerializerOptions { WriteIndented = true });
        File.WriteAllText(SettingsPath, json);
    }
}
