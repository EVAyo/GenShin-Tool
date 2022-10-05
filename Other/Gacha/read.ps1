Set-ExecutionPolicy Bypass -Scope Process -Force;
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;

#Ô­ÎÄ¼þ¡ý
$code = @"
using System;
using System.Runtime.InteropServices;
using System.Text;

public class ClipboardGetter
{
    #region Win32 Native PInvoke

    [DllImport("User32.dll", SetLastError = true)]
    private static extern uint RegisterClipboardFormatA(string lpszFormat);

    [DllImport("User32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool IsClipboardFormatAvailable(uint format);

    [DllImport("User32.dll", SetLastError = true)]
    private static extern IntPtr GetClipboardData(uint uFormat);

    [DllImport("User32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool OpenClipboard(IntPtr hWndNewOwner);

    [DllImport("User32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool CloseClipboard();

    [DllImport("Kernel32.dll", SetLastError = true)]
    private static extern IntPtr GlobalLock(IntPtr hMem);

    [DllImport("Kernel32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool GlobalUnlock(IntPtr hMem);

    [DllImport("Kernel32.dll", SetLastError = true)]
    private static extern int GlobalSize(IntPtr hMem);

    #endregion

    public static string GetHTML()
    {

        string strHTMLUTF8 = string.Empty; 
        uint CF_HTML = RegisterClipboardFormatA("HTML Format");

        if (!IsClipboardFormatAvailable(CF_HTML))
            return null;

        try
        {
            if (!OpenClipboard(IntPtr.Zero))
                return null;

            IntPtr handle = GetClipboardData(CF_HTML);
            if (handle == IntPtr.Zero)
                return null;

            IntPtr pointer = IntPtr.Zero;

            try
            {
                pointer = GlobalLock(handle);
                if (pointer == IntPtr.Zero)
                    return null;

                int size = GlobalSize(handle);
                byte[] buff = new byte[size];

                Marshal.Copy(pointer, buff, 0, (int)size);

            strHTMLUTF8 = System.Text.Encoding.UTF8.GetString(buff);
            }
            finally
            {
                if (pointer != IntPtr.Zero)
                    GlobalUnlock(handle);
            }
        }
        finally
        {
            CloseClipboard();
        }

        return strHTMLUTF8; 
    }
}
"@

Add-Type -TypeDefinition $code	

Write-Host "Copy the wish history table!";
while(1) {
  $c = iex "[ClipboardGetter]::GetHTML()"
  if ($c -match "SourceURL:https:/.+log") {
    break;
  }
  for($i=5; $i -gt 0; $i--) { Write-Host "`rChecking in $i" -NoNewline; Sleep 1; }
}
Write-Host " OK"
$result = iex "[ClipboardGetter]::GetHTML()"
$link = ($result | Select-String "(https:/.+log)").Matches[0].Value
Write-Host $link
$link | Clip.exe

