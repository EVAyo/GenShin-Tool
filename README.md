# 原神抽卡记录导出 JS 版

NGA原帖：[https://bbs.nga.cn/read.php?tid=25441042](https://bbs.nga.cn/read.php?tid=25441042)  
强烈建议使用本项目导出的xlsx配合[抽卡记录分析工具](https://github.com/voderl/genshin-gacha-analyzer)使用，可查看分析饼图、成就表  

### 安卓导出工具apk版

https://sunfkny.lanzous.com/b074k600d  密码:5fin  

### 安卓有root获取链接

 
> 在终端中执行
> ```
> sudo logcat -e "https.*#/log" -m 1 | grep -o "https.*#/log"
> ```
> 然后打开抽卡历史记录

# 安卓无root获取链接

> 打开ADB调试，连接电脑  
> 使用在线adb提取 [https://sunfkny.github.io/genshin-gacha-export-js/adb.html](https://sunfkny.github.io/genshin-gacha-export-js/adb.html)  
> [视频教程](https://www.bilibili.com/video/BV1tr4y1K7Ea?p=3)  

### 安卓导出

https://sunfkny.lanzous.com/b074ju1ob 密码:fgta  下载安装kiwi浏览器及Tampermonkey插件  
打开kiwi浏览器，右上角菜单，扩展程序，开发者模式，Load，找到下载的 Tampermonkey_4_11_0_0.crx ，右下角打开，确定，[从Github安装脚本](https://sunfkny.github.io/genshin-gacha-export-js/index.user.js) / [从fastgit安装脚本](https://hub.fastgit.org/sunfkny/genshin-gacha-export-js/raw/main/index.user.js)，打开上面获取的链接，右上角就有导出按钮  

### PC获取链接

确保最近在游戏内打开过抽卡历史记录页面，把`geturl.ps1`的内容复制到 PowerShell 里执行  

### PC导出

方法1. PC浏览器有Tampermonkey插件的情况下，[从Github安装脚本](https://sunfkny.github.io/genshin-gacha-export-js/index.user.js) / [从fastgit安装脚本](	https://hub.fastgit.org/sunfkny/genshin-gacha-export-js/raw/main/index.user.js)，打开上面获取的链接，右上角就有导出按钮  
方法2. 没有Tampermonkey插件的情况下，打开上面获取的链接，按 F12 打开控制台，把`index.js`的内容复制到控制台回车执行，等待执行完成  
