# script version 0.9
# author: jogerj

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
    if ($urlResponseMessage -ne "OK") {
        Write-Host "$([char]0x627e)$([char]0x5230)$([char]0x7684)$([char]0x94fe)$([char]0x63a5)$([char]0x5df2)$([char]0x7ecf)$([char]0x8fc7)$([char]0x671f)$([char]0x6216)$([char]0x8005)$([char]0x635f)$([char]0x574f)$([char]0x002c)$([char]0x8bf7)$([char]0x91cd)$([char]0x65b0)$([char]0x6253)$([char]0x5f00)$([char]0x7948)$([char]0x613f)$([char]0x5386)$([char]0x53f2)$([char]0x6765)$([char]0x83b7)$([char]0x53d6)$([char]0x65b0)$([char]0x94fe)$([char]0x63a5)$([char]0xff01)" -ForegroundColor Yellow
        return $False
    }
    # OK
    Write-Host $wishURL
    Set-Clipboard -Value $wishURL
    Write-Host "$([char]0x94fe)$([char]0x63a5)$([char]0x5df2)$([char]0x590d)$([char]0x5236)$([char]0x5230)$([char]0x526a)$([char]0x8d34)$([char]0x677f)$([char]0x002c)$([char]0x8bf7)$([char]0x7c98)$([char]0x8d34)$([char]0x5230)$([char]0x0066)$([char]0x0065)$([char]0x0069)$([char]0x0078)$([char]0x0069)$([char]0x0061)$([char]0x006f)$([char]0x0071)$([char]0x0069)$([char]0x0075)$([char]0x002e)$([char]0x0063)$([char]0x006f)$([char]0x006d)" -ForegroundColor Green
    return $True
}

$reg = $args[0]
$logPath = [System.Environment]::ExpandEnvironmentVariables("%userprofile%\AppData\LocalLow\miHoYo\Genshin Impact\output_log.txt");
if (!(Test-Path $logPath) -or $reg -eq "china") {
    $logPath = [System.Environment]::ExpandEnvironmentVariables("%userprofile%\AppData\LocalLow\miHoYo\$([char]0x539f)$([char]0x795e)\output_log.txt");
    if (!(Test-Path $logPath)) {
        Write-Host "$([char]0xe689)" -ForegroundColor Red
        if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {  
            Write-Host "$([char]0x662f)$([char]0x5426)$([char]0x4ee5)$([char]0x7ba1)$([char]0x7406)$([char]0x5458)$([char]0x8eab)$([char]0x4efd)$([char]0x6765)$([char]0x8fd0)$([char]0x884c)$([char]0x811a)$([char]0x672c)$([char]0x003f)$([char]0x6309)$([char]0x0045)$([char]0x006e)$([char]0x0074)$([char]0x0065)$([char]0x0072)$([char]0x952e)$([char]0x6765)$([char]0x7ee7)$([char]0x7eed)$([char]0x6216)$([char]0x6309)$([char]0x5176)$([char]0x4ed6)$([char]0x952e)$([char]0x6765)$([char]0x53d6)$([char]0x6d88)"
            $keyInput = [Console]::ReadKey($true).Key
            if ($keyInput -ne "13") {
                return
            }
            $arguments = "& '" +$myinvocation.mycommand.definition + "'"
            Start-Process powershell -Verb runAs -ArgumentList "-noexit $arguments $reg"
            break
        }
        return
    }
}

$logs = Get-Content -Path $logPath
$regexPattern = "(?m).:/.+(GenshinImpact_Data|YuanShen_Data)"
$logMatch = $logs -match $regexPattern

if (-Not $logMatch) {
    Write-Host "$([char]0x627e)$([char]0x4e0d)$([char]0x5230)$([char]0x539f)$([char]0x795e)$([char]0x65e5)$([char]0x5fd7)$([char]0x6587)$([char]0x4ef6)$([char]0x8bf7)$([char]0x81f3)$([char]0x5c11)$([char]0x6253)$([char]0x5f00)$([char]0x7948)$([char]0x613f)$([char]0x5386)$([char]0x53f2)$([char]0x754c)$([char]0x9762)$([char]0x4e00)$([char]0x6b21)" -ForegroundColor Red
    pause
    return
}

$gameDataPath = ($logMatch | Select -Last 1) -match $regexPattern
[bool] $gameDataPathFetchSuccess = $True
try {
    $gameDataPath = Resolve-Path $Matches[0] -ErrorAction Stop
} catch {
    Write-Host "$([char]0x68c0)$([char]0x6d4b)$([char]0x5230)$([char]0x4e2d)$([char]0x6587)$([char]0x8def)$([char]0x5f84)$([char]0xff0c)$([char]0x4f7f)$([char]0x7528)$([char]0x5907)$([char]0x7528)$([char]0x65b9)$([char]0x6cd5)$([char]0x002e)$([char]0x002e)$([char]0x002e)" -ForegroundColor Red
    $gameDataPathFetchSuccess = $False
}
if($gameDataPathFetchSuccess){
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
        Write-Host "$([char]0x4f7f)$([char]0x7528)$([char]0x5907)$([char]0x7528)$([char]0x65b9)$([char]0x6cd5)$([char]0x91cd)$([char]0x8bd5)$([char]0x4e2d)..." -ForegroundColor Red
    }

    # Method 2 (Credits to PrimeCicada for finding this path)
    $cachePath = "$gameDataPath\\webCaches\\Service Worker\\CacheStorage\\f944a42103e2b9f8d6ee266c44da97452cde8a7c"
    if (Test-Path $cachePath) {
        Write-Host "$([char]0x4f7f)$([char]0x7528)$([char]0x5907)$([char]0x7528)$([char]0x65b9)$([char]0x6cd5)$([char]0x0020)$([char]0x0028)$([char]0x0053)$([char]0x0057)$([char]0x0029)" -ForegroundColor Yellow
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
        Write-Host "$([char]0x5907)$([char]0x7528)$([char]0x65b9)$([char]0x6cd5)$([char]0x0028)$([char]0x0053)$([char]0x0057)$([char]0x0029)$([char]0x5931)$([char]0x8d25)$([char]0x002c)$([char]0x4f7f)$([char]0x7528)$([char]0x5907)$([char]0x7528)$([char]0x65b9)$([char]0x6cd5)$([char]0x5c1d)$([char]0x8bd5)$([char]0x4e2d)$([char]0x002e)$([char]0x002e)$([char]0x002e)" -ForegroundColor Red
    }

    # Method 3
    Write-Host "$([char]0x4f7f)$([char]0x7528)$([char]0x5907)$([char]0x7528)$([char]0x65b9)$([char]0x6cd5)$([char]0x0020)$([char]0x0028)$([char]0x0043)$([char]0x0043)$([char]0x0056)$([char]0x0029)" -ForegroundColor Yellow
    $cachePath = "$gameDataPath\\webCaches\\Cache\\Cache_Data"
    $tempPath = mkdir "$env:TEMP\\feixiaoqiu" -Force
    # downloads ChromeCacheView
    Invoke-WebRequest -Uri "https://www.nirsoft.net/utils/chromecacheview.zip" -OutFile "$tempPath\\chromecacheview.zip"
    Expand-Archive "$tempPath\\chromecacheview.zip" -DestinationPath "$tempPath\\chromecacheviewer" -Force
    & "$tempPath\chromecacheviewer\\ChromeCacheView.exe" -folder $cachePath /scomma "$tempPath\\cache_data.csv"
    # processing cache takes a while
    while (!(Test-Path "$tempPath\\cache_data.csv")) { Start-Sleep 1 }
    $wishLog = Import-Csv "$tempPath\\cache_data.csv" | select  "Last Accessed", "URL" | ? URL -like "*event/gacha_info/api/getGachaLog*" | Sort-Object -Descending { $_."Last Accessed" -as [datetime] } | select -first 1
    $wishUrl = $wishLog | % {$_.URL.Substring(4)}
    # clean up
    Remove-Item -Recurse -Force $tempPath
    if ($wishUrl) {
        if (processWishUrl $wishUrl) {
            return
        }
    }

    Write-Host "$([char]0x94fe)$([char]0x63a5)$([char]0x5df2)$([char]0x590d)$([char]0x5236)$([char]0x5230)$([char]0x526a)$([char]0x8d34)$([char]0x677f)$([char]0x002c)$([char]0x8bf7)$([char]0x7c98)$([char]0x8d34)$([char]0x5230)$([char]0x0066)$([char]0x0065)$([char]0x0069)$([char]0x0078)$([char]0x0069)$([char]0x0061)$([char]0x006f)$([char]0x0071)$([char]0x0069)$([char]0x0075)$([char]0x002e)$([char]0x0063)$([char]0x006f)$([char]0x006d)" -ForegroundColor Red
    pause
} else {
    Write-Host "$([char]0x8bf7)$([char]0x8fd4)$([char]0x56de)$([char]0x5386)$([char]0x53f2)$([char]0x8bb0)$([char]0x5f55)$([char]0x9875)$([char]0x9762)$([char]0x5e76)$([char]0x5168)$([char]0x9009)$([char]0x0028)$([char]0x0043)$([char]0x0074)$([char]0x0072)$([char]0x006c)$([char]0x0020)$([char]0x0041)$([char]0x0029)$([char]0x590d)$([char]0x5236)$([char]0x5168)$([char]0x90e8)$([char]0x0028)$([char]0x0043)$([char]0x0074)$([char]0x0072)$([char]0x006c)$([char]0x0020)$([char]0x0043)$([char]0x0029)$([char]0x7136)$([char]0x540e)$([char]0x8fd4)$([char]0x56de)$([char]0x8fd9)$([char]0x91cc)$([char]0x7c98)$([char]0x8d34)$([char]0x0028)$([char]0x0043)$([char]0x0074)$([char]0x0072)$([char]0x006c)$([char]0x0020)$([char]0x0056)$([char]0x0029)" -ForegroundColor Green
    pause
    $m=(((Get-Clipboard -TextFormatType Html) | sls "(https:/.+log)").Matches[0].Value)
    $m
    Set-Clipboard -Value $m
    Write-Host "$([char]0x62bd)$([char]0x5361)$([char]0x94fe)$([char]0x63a5)$([char]0x5df2)$([char]0x590d)$([char]0x5236)$([char]0x5230)$([char]0x526a)$([char]0x8d34)$([char]0x677f)" -ForegroundColor Green
}