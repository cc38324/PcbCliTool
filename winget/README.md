# winget 发布状态

包标识为 `Miyue.PcbCliTool`，命令为 `easyedatool`。

2026-10-28 刷新并查询官方源，未找到该包。[已有收录申请 #452460](https://github.com/microsoft/winget-pkgs/pull/452460) 为0.2.0，自动验证已完成、命名误报已豁免，目前等待维护者批准；不能把自动验证通过当成官方源可安装。

本目录的0.2.3清单沿用已验证的包标识和ZIP便携布局，引用本版完整Windows ZIP及其真实SHA256。执行：

```powershell
winget validate --manifest winget/Miyue.PcbCliTool/0.2.3
```

本机格式验证通过。当前系统未启用LocalManifestFiles，本轮未声称本地清单安装通过，也未改变该管理员设置。Windows发行包另已完成直接安装、逐文件核对及PCB/原理图/3D窗口验证。

官方收录前请用[本版Release](https://github.com/cc38324/PcbCliTool/releases/tag/v0.2.3)。合入后仍应刷新官方源，查询目标版本再测试安装；只找到旧版不代表0.2.3可用。本目录不是独立的软件源。
