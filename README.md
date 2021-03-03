# 原神导出抽卡记录 JS 版

 - [抽卡记录分析工具](https://voderl.github.io/genshin-gacha-analyzer/) from [@笑沐泽](https://bbs.nga.cn/read.php?tid=25004616&page=16#pid491033187Anchor)  
 - [抽卡记录导出工具python版](https://github.com/sunfkny/genshin-gacha-export)，导出后含有抽卡报告

## 使用方法
### PC获取链接
确保最近在游戏内打开过抽卡记录页面，把`geturl.ps1`的内容复制到 PowerShell 里执行  
### 安卓获取链接
 -  有root  
> 在终端中执行
> ```
> sudo logcat -e "https.*#/log" -m 1 | grep -o "https.*#/log"
> ```
> 然后打开历史记录
 - 无root  
> 打开ADB调试，连接电脑  
> 使用在线adb提取 https://sunfkny.github.io/genshin-gacha-export-js/adb.html  
### 导出
方法1. 安卓端可以下载 [index.user.js](https://cdn.jsdelivr.net/gh/sunfkny/genshin-gacha-export-js@main/) ，使用 kiwi浏览器右上角-扩展程序-Load-选择下载的`index.user.js` 安装用户脚本，打开上面获取的链接，右上角就有导出按钮  
方法2. PC浏览器安装[油猴脚本](https://cdn.jsdelivr.net/gh/sunfkny/genshin-gacha-export-js@main/index.user.js)，打开上面获取的链接，右上角就有导出按钮  
方法3. 打开上面获取的链接，按 F12 打开控制台，把`index.js`的内容复制到控制台回车执行，等待执行完成  
