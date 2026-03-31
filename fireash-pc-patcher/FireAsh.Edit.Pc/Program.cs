using System.Windows.Forms;

namespace FireAsh.Edit.Pc;

internal static class Program
{
    [STAThread]
    private static void Main()
    {
        ApplicationConfiguration.Initialize();
        Application.Run(new MainForm());
    }
}
