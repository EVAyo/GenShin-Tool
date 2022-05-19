# GenshinTools

#### 介绍
用来搞原神ios小组件

#### 咋用呢

拢共分两步, 分别是 获取Cookie, 然后导入运行

##### 获取Cookie

感谢[这个github](https://github.com/Womsxd/AutoMihoyoBBS/) , 打不开也没事

1. 打开你的浏览器,进入**无痕/隐身模式**

2. 由于米哈游修改了bbs可以获取的Cookie，导致一次获取的Cookie缺失，所以需要增加步骤

3. 打开`http://bbs.mihoyo.com/ys/`并进行登入操作

4. 按下键盘上的`F12`或右键检查,打开开发者工具,点击Console

5. 输入

   ```javascript
   var cookie=document.cookie;var ask=confirm('Cookie:'+cookie+'\n\nDo you want to copy the cookie to the clipboard?');if(ask==true){copy(cookie);msg=cookie}else{msg='Cancel'}
   ```

   回车执行，并在确认无误后点击确定。

7. **此时Cookie已经复制到你的粘贴板上了**

##### 导入运行

1. 去 app store 下载 scriptable , 把 [scriptable_note.js](https://gitee.com/muuuj1an/GenshinTools/raw/main/scriptable_note.js)里面的内容放到 scriptable 应用里, 然后将上一步获取的 Cookie 粘贴到第5行,  

更多壁纸背景样式:

[芭芭拉背景scriptable_note.js](https://gitee.com/muuuj1an/GenshinTools/raw/main/scriptable_note_barbara.js)  

[原神大门背景scriptable_note.js](https://gitee.com/muuuj1an/GenshinTools/raw/main/scriptable_note_yuanshenDoor.js) 

`` const mihoyoCookie = "xxxxx" ``

2. 先运行一下, 看看好使不, 好使的话, 点击左上角的 'Done', 再给这个重新起个名儿, 比如 yuanshen small+

3. 好使的话, 在桌面添加 scriptable 小组件, 得最小号的, 然后长摁小组件, 点击'编辑小组件' , script => 选择刚才保存的

##### 我觉得屎黄色不好看, 想改个色, 咋整?

1. 请翻到第311行, 第322行 代码, 这两个颜色代表了背景渐变色, 你可以随便找网上好看的配色方案, 自己改一下, 记得改完后要点击左上角的 'Done'

##### 纯纯背景色已经不能满足我了, 我要背景图!

1. 把 第308~第314行 代码注释掉, 放开 第304行, 306行, 然后把你找到的图片进行base64编码 可以到[这个网址](http://www.jsons.cn/img2base64/)

2. 将得到的base64编码粘贴到 第540行 

`` const url = "data:imagexxxxxxx"

3. 记得改完后要点击左上角的 'Done'

##### 能不能点击这个小组件, 直接打开原神?

1. 长摁小组件, 点击'编辑小组件' , When Interacting => 选择 Open URL

2. URL => 输入 `` yuanshengame:// `` 就OK啦
