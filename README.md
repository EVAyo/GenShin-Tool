![cover](https://file.xunkong.cc/static/repo/xunkong/cover.webp)

# 寻空

> Scighost 的原神工具箱，带给旅行者方便与乐趣。

**寻空**可以帮你统计和分析游戏中的各项数据，快速掌握账号的相关信息。在这里你可以：

- 欣赏由开发者精心挑选的同人图
- 快速浏览每日素材，活动攻略
- 查看你的祈愿，原石摩拉，深境螺旋等数据
- 启动游戏并解锁帧数上限
- ……

## 安装

寻空仅支持 x64 和 arm64 架构的 Windows 10 1809 及以上版本的系统，建议升级到最新版获得更稳定的体验。

> 商店版和侧载版可以共存，但是因为公用一个数据库，二者版本不同时可能存在冲突。

### 商店版（推荐）

[从应用商店安装](https://www.microsoft.com/store/apps/9N2SVG0JMT12)

应用商店的审核一般需要2个工作日，商店版无法做到实时更新。

### 侧载版

> 安装侧载版需要信任自签名证书，此证书仅用于寻空相关项目的代码签名。

- 首次安装侧载版时请从 [Releases](https://github.com/xunkong/xunkong/releases) 页面下载最新的 zip 文件并解压
- 脚本安装
  - 在系统设置中打开 [**开发者选项**](ms-settings:developers) 界面，勾选 **开发人员模式** 和 **允许 PowerShell 脚本**
  - 找到 `Install.ps1`，在该文件的右键菜单中选择 **使用 PowerShell 运行**
  - **安装完成后一定要关闭 允许 PowerShell 脚本**
- 手动安装
  - 将 cer 证书文件添加到 `本地计算机/受信任人`
  - 在 `Dependencies` 文件夹下安装符合 CPU 架构的依赖包
  - 双击 msixbundle 文件进行安装
- 后续更新时下载符合 CPU 架构的 msixbundle 文件即可

**开发者选项截图**

<details>
<summary>Windows 10</summary>

![dev-setting-win10-devmode](https://file.xunkong.cc/static/repo/xunkong/dev-setting-win10-devmode.webp)

![dev-setting-win10-powershell](https://file.xunkong.cc/static/repo/xunkong/dev-setting-win10-powershell.webp)

</details>

<details>
<summary>Windows 11</summary>

![dev-setting-win11](https://file.xunkong.cc/static/repo/xunkong/dev-setting-win11.webp)

</details>

## 开发指南

请移步 https://github.com/xunkong/dev

## 致谢

寻空的完善离不开以下开源项目：

- [.NET Platform](https://github.com/dotnet)
- [AngleSharp](https://github.com/AngleSharp/AngleSharp)
- [WindowsCommunityToolkit](https://github.com/CommunityToolkit/WindowsCommunityToolkit)
- [Dapper](https://github.com/DapperLib/Dapper)
- [LiteDB](https://github.com/mbdavid/LiteDB)
- [Mapster](https://github.com/MapsterMapper/Mapster)
- [WindowsAppSDK](https://github.com/microsoft/WindowsAppSDK)
- [MiniExcel](https://github.com/MiniExcel/MiniExcel)
- [Octokit](https://github.com/octokit/octokit.net)
- [Vanara](https://github.com/dahall/Vanara)

感谢微软提供的 Visual Studio 社区版 和 Visual Studio Code 开发工具

感谢 JetBrains 提供的开源许可证

<div>
    <img alt="Visual Studio" src="https://file.xunkong.cc/static/repo/xunkong/Visual_Studio_Icon_2019.svg" width="60" />
    <img alt="Visual Studio Code" src="https://file.xunkong.cc/static/repo/xunkong/Visual_Studio_Code_1.35_icon.svg" width="60" />
    <img alt="JetBrains" src="https://file.xunkong.cc/static/repo/xunkong/JetBrains_Logo_2016.svg" width="60" />
</div>
