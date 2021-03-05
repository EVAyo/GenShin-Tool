# 原神导出抽卡记录 JS 版

 - [抽卡记录分析工具](https://voderl.github.io/genshin-gacha-analyzer/) from [@笑沐泽](https://bbs.nga.cn/read.php?tid=25004616&page=16#pid491033187Anchor)  
 - [抽卡记录导出工具python版](https://github.com/sunfkny/genshin-gacha-export)，导出后含有抽卡报告

## 获取链接

### PC

确保最近在游戏内打开过抽卡历史记录页面，把`geturl.ps1`的内容复制到 PowerShell 里执行  

### 安卓
 -  有root  

> 在终端中执行
> ```
> sudo logcat -e "https.*#/log" -m 1 | grep -o "https.*#/log"
> ```
> 然后打开抽卡历史记录

 - 无root  

> 打开ADB调试，连接电脑  
> 使用在线adb提取 [https://sunfkny.github.io/genshin-gacha-export-js/adb.html](https://sunfkny.github.io/genshin-gacha-export-js/adb.html)  
> [视频教程](https://www.bilibili.com/video/BV1tr4y1K7Ea?p=3)  

## 导出

### PC

方法1. PC浏览器有Tampermonkey插件的情况下，[点击安装index.user.js](https://cdn.jsdelivr.net/gh/sunfkny/genshin-gacha-export-js/index.user.js)，打开上面获取的链接，右上角就有导出按钮  
方法2. 没有Tampermonkey插件的情况下，打开上面获取的链接，按 F12 打开控制台，把`index.js`的内容复制到控制台回车执行，等待执行完成  

### 安卓

https://sunfkny.lanzous.com/b074ju1ob 密码:fgta  下载安装kiwi浏览器及Tampermonkey插件  
打开kiwi浏览器，右上角菜单，扩展程序，开发者模式，Load，找到下载的 Tampermonkey_4_11_0_0.crx ，右下角打开，确定，[点击安装index.user.js](https://cdn.jsdelivr.net/gh/sunfkny/genshin-gacha-export-js/index.user.js)，打开上面获取的链接，右上角就有导出按钮  
