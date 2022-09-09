# version 0.1
# author: jogerj

$tempDir = "$env:TEMP\\paimonmoe"

Try {
    $tempDir = mkdir $tempDir -Force
    Write-Host "Fetching adb... please wait" -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://dl.google.com/android/repository/platform-tools-latest-windows.zip" -OutFile "$tempDir\\platform-tools.zip"
    Expand-Archive "$tempDir\\platform-tools.zip" -DestinationPath "$tempDir"
    $adb = "$tempDir\\platform-tools\\adb.exe"

    Write-Host "Please connect your phone via USB and turn on USB debugging on your phone"  -ForegroundColor Yellow
    Write-Host "Go to Developer options -> Allow USB debugging" -ForegroundColor Yellow
    Write-Host "Guide:" -ForegroundColor Yellow
    Write-Host "https://developer.android.com/studio/debug/dev-options#enable" -ForegroundColor Cyan
    pause

    $listDevices = & $adb devices
    echo $listDevices
    if ($listDevices -match "unauthorized$") {
        Write-Host "Please authorize USB debugging on your phone!" -ForegroundColor Yellow
        Write-Host "Make sure `"Always allow from this computer`" is checked!" -ForegroundColor Yellow
        pause
        $listDevices = & $adb devices
        echo $listDevices
    }
   
    if ($listDevices -match "device$") {
        Write-Host "Please open Genshin Impact and open Wish History" -ForegroundColor Yellow
        & $adb logcat -m 1 -e "OnGetWebViewPageFinish" | % {
            if ($_ -match "https.+/log") {
                $wishUrl = $Matches[0]
                Write-Host $wishUrl
                Set-Clipboard -Value $wishUrl
                Write-Host "Link copied to clipboard, paste it back to paimon.moe" -ForegroundColor Green
            }
        }
    }
} Finally {
    Remove-Item $tempDir -Recurse -Force
}