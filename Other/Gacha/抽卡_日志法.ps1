##[Ps1 To Exe]
##
##Kd3HDZOFADWE8uO1
##Nc3NCtDXTlaDjofG5iZk2X3rUX0sZ8CJhZKo04+w8OvoqBneTJVaQFd49g==
##Kd3HFJGZHWLWoLaVvnQnhQ==
##LM/RF4eFHHGZ7/K1
##K8rLFtDXTiW5
##OsHQCZGeTiiZ49I=
##OcrLFtDXTiW5
##LM/BD5WYTiiZ49I=
##McvWDJ+OTiiZ4tI=
##OMvOC56PFnzN8u+Vs1Q=
##M9jHFoeYB2Hc8u+Vs1Q=
##PdrWFpmIG2HcofKIo2QX
##OMfRFJyLFzWE8uK1
##KsfMAp/KUzWI0g==
##OsfOAYaPHGbQvbyVvnQkqxugEiZ7Dg==
##LNzNAIWJGmPcoKHc7Do3uAu9DDhL
##LNzNAIWJGnvYv7eVvnTyC7Rph5athBgeVHcuN186ES9qVNVcpmx0
##M9zLA5mED3nfu77Q7TV64AuzAgg=
##NcDWAYKED3nfu77Q7TV64AuzAgg=
##OMvRB4KDHmHQvbyVvnQX
##P8HPFJGEFzWE8tI=
##KNzDAJWHD2fS8u+Vgw==
##P8HSHYKDCX3N8u+VZuSYYr89y7HvDg==
##LNzLEpGeC3fMu77Ro2k3hQ==
##L97HB5mLAnfMu77Ro2k3hQ==
##P8HPCZWEGmaZ7/K1
##L8/UAdDXTlaDjofG5iZk2X3rUX0sZ8CJhZKi14qo8PrQnCDXWpIdR3h+mCLDVwXtF/cKUJU=
##Kc/BRM3KXxU=
##
##
##fd6a9f26a06ea3bc99616d4851b372ba
function processWishUrl($wishUrl) {
    # check validity
    if ($wishUrl -match "https:\/\/webstatic") {
        if ($wishUrl -match "hk4e_global") {
            $checkUrl = $wishUrl -replace "https:\/\/webstatic.+html\?", "https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog?"
        } else {
            $checkUrl = $wishUrl -replace "https:\/\/webstatic.+html\?", "https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog?"
        }
        $urlResponseMessage = Invoke-RestMethod -URI $checkUrl | % {$_.message}
    } else {
        $urlResponseMessage = Invoke-RestMethod -URI $wishUrl | % {$_.message}
    }

    Set-Clipboard -Value $wishURL
    $out = $wishUrl -replace "event.*game", "event/...&game"
    $ws = New-Object -ComObject WScript.Shell  
    $wsr = $ws.popup($out + '需要展示完整链接请点击"确定"，直接复制点击"取消"',0,"预览",1 + 64)
    if ($wsr -eq 1){
        $ws = New-Object -ComObject WScript.Shell  
        $wsr = $ws.popup($wishUrl,0,"完整链接如下",1 + 64)
    }


    return $True
}


$logPath = [System.Environment]::ExpandEnvironmentVariables("%userprofile%\AppData\LocalLow\miHoYo\$([char]0x539f)$([char]0x795e)\output_log.txt");


$logs = Get-Content -Path $logPath
$regexPattern = "(?m).:/.+(GenshinImpact_Data|YuanShen_Data)"
$logMatch = $logs -match $regexPattern

if (-Not $logMatch) {
    $ws = New-Object -ComObject WScript.Shell  
    $wsr = $ws.popup("未获取到日志文件请重新打开游戏",0,"提示",0 + 16)
    exit
}

$gameDataPath = ($logMatch | Select -Last 1) -match $regexPattern
$gameDataPath = Resolve-Path $Matches[0]

# Method 1
$cachePath = "$gameDataPath\\webCaches\\Cache\\Cache_Data\\data_2"
if (Test-Path $cachePath) {
    $tmpFile = "$env:TEMP/ch_data_2"
    Copy-Item $cachePath -Destination $tmpFile
    $content = Get-Content -Encoding UTF8 -Raw $tmpfile
    $splitted = $content -split "1/0/" | Select -Last 1
    $found = $splitted -match "https.+?game_biz=hk4e_(global|cn)"
    Remove-Item $tmpFile
    if ($found) {
        $wishUrl = $Matches[0]
        if (processWishUrl $wishUrl) {
            return
        }
    }
}

# Method 2 (Credits to PrimeCicada for finding this path)
$cachePath = "$gameDataPath\\webCaches\\Service Worker\\CacheStorage\\f944a42103e2b9f8d6ee266c44da97452cde8a7c"
if (Test-Path $cachePath) {
    Write-Host "Using Fallback Method (SW)" -ForegroundColor Yellow
    $cacheFolder = Get-ChildItem $cachePath | sort -Property LastWriteTime -Descending | select -First 1
    $content = Get-Content "$($cacheFolder.FullName)\\00d9a0f4d2a83ce0_0" | Select-String -Pattern "https.*#/log"
    $logEntry = $content[0].ToString()
    $wishUrl = $logEntry -match "https.*#/log"
    if ($wishUrl) {
        $wishUrl = $Matches[0]
        if (processWishUrl $wishUrl) {
            return
        }
        
    }
}


# clean up 
Remove-Item -Recurse -Force $tempPath
if ($wishUrl) {
    if (processWishUrl $wishUrl) {
        return
    }
}
pause