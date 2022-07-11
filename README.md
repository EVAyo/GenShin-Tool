# GenshinTools

#### 介绍
用来搞原神ios小组件

#### 咋用呢

拢共分两步, 分别是 获取Cookie, 然后导入运行

##### 获取Cookie

感谢[这个github](https://github.com/Womsxd/AutoMihoyoBBS/) , 打不开也没事

1. 打开你的浏览器,进入**无痕/隐身模式**

2. 打开`http://bbs.mihoyo.com/ys/`并进行登入操作

3. 按下键盘上的`F12`或右键检查,打开开发者工具,点击Console

4. 输入

   ```javascript
   var cookie=document.cookie;var ask=confirm('Cookie:'+cookie+'\n\nDo you want to copy the cookie to the clipboard?');if(ask==true){copy(cookie);msg=cookie}else{msg='Cancel'}
   ```

   回车执行，并在确认无误后点击确定。

5. **此时Cookie已经复制到你的粘贴板上了**

##### 导入运行

1. 去 app store 下载 scriptable , 把 [scriptable_note_2.1.js](https://gitee.com/muuuj1an/GenshinTools/raw/main/genshin2.1.js) 里面的内容放到 scriptable 应用里, 然后将上一步获取的 Cookie 粘贴到第5行,  `` const mihoyoCookie = "xxxxx" ``

默认是蓝色渐变背景~ 更多壁纸背景样式:

![preview2.0](https://gitee.com/muuuj1an/GenshinTools/raw/main/img/preview2.0.jpg)

![preview](https://gitee.com/muuuj1an/GenshinTools/raw/main/img/preview.jpg)

[还没来得及改到2.0版,芭芭拉背景版]

[还没来得及改到2.0版,原神大门背景版]

[还没来得及改到2.0版,蓝色渐变背景 中号组件 临时版](https://gitee.com/muuuj1an/GenshinTools/raw/main/scriptable_note_medium.js)

2. 先运行一下, 看看好使不, 好使的话, 点击左上角的 'Done', 再给这个重新起个名儿, 比如 yuanshen small+

3. 好使的话, 在桌面添加 scriptable 小组件, 得最小号的, 然后长摁小组件, 点击'编辑小组件' , script => 选择刚才保存的 (如果用的是中号组件版, 那就选择中号)

#### Q&A
- 该QA针对的是 [scriptable_note_2.0.js](https://gitee.com/muuuj1an/GenshinTools/raw/main/scriptable_note_2.0.js) , 对2.1版,行数可能有变化, 请在代码里找找关键词或者注释, 再修改~

##### 我觉得蓝色不好看, 想改个色, 咋整?

1. 请翻到第273行, 第274行 代码, 这两个颜色代表了背景渐变色, 你可以随便找网上好看的配色方案, 自己改一下, 记得改完后要点击左上角的 'Done'

##### 纯纯背景色已经不能满足我了, 我要背景图!

1. 把 第270~第276行 代码注释掉, 放开 第266行, 267行, 然后把你找到的图片进行base64编码 可以到[这个网址](http://www.jsons.cn/img2base64/)

2. 将得到的base64编码粘贴到 第266行 

`` let background = await loadImageFromUrl("data:imagexxxxxxx") ``

3. 记得改完后要点击左上角的 'Done'

##### 背景图base64好难搞哦, 我直接引入图片行不行?

可以是可以, 首先是你一定要有图片的在线地址哦

1. 把 第270~第276行 代码注释掉, 放开 第266行, 267行, 

2. 将图片链接粘贴到第266行, 比如: 

`` let background = await loadImageFromUrl("https://gitee.com/muuuj1an/GenshinTools/raw/main/img/background/barbara.png") ``

3. 记得改完后要点击左上角的 'Done'

##### 能不能点击这个小组件, 直接打开原神?

1. 长摁小组件, 点击'编辑小组件' , When Interacting => 选择 Open URL

2. URL => 输入 `` yuanshengame:// `` 就OK啦
