$logLocation = "%userprofile%\AppData\LocalLow\miHoYo\$([char]0x539f)$([char]0x795e)\output_log.txt";
$path = [System.Environment]::ExpandEnvironmentVariables($logLocation);
dir -Path $path |
    ForEach-Object -Process {
        $length = $_.length/1MB
        if ($length -gt 15){
        $ws = New-Object -ComObject WScript.Shell  
        $wsr = $ws.popup("当前日志文件已达{0:n2}MB，请清空后重新提取" -f $length,0,"文件过大警告",1 + 16)
        if ($wsr -eq 1){
            $logLocation = "%userprofile%\AppData\LocalLow\miHoYo\$([char]0x539f)$([char]0x795e)\output_log.txt";
            $path = [System.Environment]::ExpandEnvironmentVariables($logLocation);
            Clear-Content $path
            }
        }
     }
if (-Not [System.IO.File]::Exists($path)) {
    $ws = New-Object -ComObject WScript.Shell  
    $wsr = $ws.popup("未获取到链接请重新打开祈愿记录",0,"提示",0 + 16)
    exit
}
$logs = Get-Content -Path $path
$match = $logs -match "^OnGetWebViewPageFinish.*log$"
if (-Not $match) {
    $ws = New-Object -ComObject WScript.Shell  
    $wsr = $ws.popup("未获取到链接请重新打开祈愿记录",0,"提示",0 + 16)
    exit
}
[string] $wishHistoryUrl = $match -replace 'OnGetWebViewPageFinish:', ''
[string] $wishHistoryUrl = $wishHistoryUrl -replace 'https.*\s', ''
#Write-Host $wishHistoryUrl.length
Set-Clipboard -Value $wishHistoryUrl

$out = $wishHistoryUrl -replace "event.*game", "event/...&game"
$ws = New-Object -ComObject WScript.Shell  
$wsr = $ws.popup($out + '需要展示完整链接请点击"确定"，直接复制点击"取消"',0,"预览",1 + 64)
if ($wsr -eq 1){
    $ws = New-Object -ComObject WScript.Shell  
    $wsr = $ws.popup($wishHistoryUrl,0,"完整链接如下",1 + 64)
}

