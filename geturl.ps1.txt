# 拼接日志路径
# 外服需要把 原神 改成 Genshin Impact
$output_log_path = "$env:USERPROFILE\AppData\LocalLow\miHoYo\原神\output_log.txt"
# 读取文件
$log = Get-Content $output_log_path
# 提取链接，去除不需要的OnGetWebViewPageFinish:
$urls = $log -match "OnGetWebViewPageFinish:" -match "#/log" -replace "OnGetWebViewPageFinish:",""
# 取最后一个链接
$url = $urls[$urls.Length-1]
# 输出到控制台
Write-Host $url
# 浏览器打开
Start-Process -FilePath $url
# 如果运行ps1脚本
# write-host "按任意键退出..."
# [void][System.Console]::ReadKey($true)
