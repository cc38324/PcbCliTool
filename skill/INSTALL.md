# easyedatool 安装和使用

嘉立创EDA专业版（EasyEDA Pro）文件夹工程的离线命令行工具：从设计文件生成工程、自动布线、算铺铜、DRC、核对，出效果图、原理图 PDF / 网表 / BOM、Gerber / 钻孔 / 贴片坐标。

## 安装

0.2.0 每个系统的命令写在仓库根目录的 `README.md`（中文）和 `README.en.md`。装好后命令都是 `easyedatool`。

- Windows：`winget install --id Miyue.PcbCliTool --version 0.2.0`。还没进 winget 源时，用 Release 里的 `easyedatool-0.2.0-windows-x64.zip`，或双击 `easyedatool-0.2.0-windows-x64-setup.exe`（装到 `%USERPROFILE%\.claude\skills\easyedatool`；没有签名，第一次运行选「更多信息」→「仍要运行」）。
- macOS（Apple 芯片）：`brew tap cc38324/pcbclitool https://github.com/cc38324/PcbCliTool.git`，然后 `brew install cc38324/pcbclitool/easyedatool`。
- Ubuntu 22.04 / 24.04 / 26.04：`sudo apt-get update && sudo apt-get install easyedatool`。源还没公开时，`dpkg -i easyedatool_0.2.0-1_amd64.deb`。
- Debian 12 / 13：和 Ubuntu 同一份 deb，命令相同。
- 鸿蒙电脑：0.2.0 没有安装包。

也可以用同名的 zip：解压到任意位置就能用，解压出来就是下面这些文件。

## 文件

```
easyedatool/
  bin/easyedatool.exe   程序（Windows x64，单个文件，C 运行库编译在里面，不用装别的）
  viewer/               实时预览窗口 easyeda_view.exe（Flutter 桌面程序，Flutter 和 VC++ 运行库都带着）：easyedatool view <工程> 打开，
                        看 PCB / 原理图，布线进度和新画的线实时显示；和 bin/ 放在一起它们才找得到对方
  SKILL.md              给 AI 的使用说明（也是 Claude Code 的 skill 入口）
  references/           AI 说明书的参考：全部命令参数、设计文件、规则文件、和 EDA 客户端配合
  examples/             设计文件和规则文件的例子
  AGENTS.md             指给别的 AI 工具：先读 SKILL.md
  README.md             给人看的完整说明（功能、速度、核对记录、已知限制）
  VERSION               版本和对应的源码提交
  LICENSE-easyeda-eprj3-skill   程序里内置的模板的许可（MIT）
```

## 自己用

macOS（Apple 芯片）的包：程序是 `bin/easyedatool`，窗口是 `viewer/easyeda_view.app`。从网上下载的 zip 解压后第一次运行会被 macOS 拦下（没有苹果公证），在终端里 `xattr -dr com.apple.quarantine <解压出来的 easyedatool 文件夹>` 一次就好。

解压到任意位置，在命令行里跑 `bin\easyedatool.exe --help`，每个命令也有 `--help`。上手看 `SKILL.md` 里「画一块新板」和「快速自测」。

想看着画：`bin\easyedatool.exe view <工程>` 打开预览窗口（或者直接双击 `viewer\easyeda_view.exe`，在界面里选工程文件夹）。窗口只读文件：谁改了工程（这个工具、EDA、手改）它都跟着重画；AI 跑 route、gen、pour --write、drc、check 时进度和结果实时显示。

## 给 Claude Code 用（skill）

用安装程序装的已经在这个位置；用 zip 的话，把解压出来的 `easyedatool` 文件夹放到 `%USERPROFILE%\.claude\skills\` 下（得到 `…\.claude\skills\easyedatool\SKILL.md`）。然后重开 Claude Code。之后说「画板」「生成嘉立创工程」「布线」「出 Gerber / BOM」这类话，Claude 会自动读 SKILL.md 再用这个工具。Claude Code 换别的模型当后端（比如 DeepSeek 的 Anthropic 兼容接口）时 skill 照样列出来，但那个模型会不会按说明用，要拿「快速自测」试一下。

## 给别的 AI 用（DeepSeek、Cursor、Cline……）

这些工具不认 skill，让它**先读 `SKILL.md`**：在对话开头说「先读 <解压路径>\easyedatool\SKILL.md 再干活」，或者把 SKILL.md 的内容放进它的规则文件 / 系统提示里（Cursor 的 rules、Cline 的 .clinerules 之类），`references/` 按需让它读。

对 AI 来说，这个工具比直接操作 EDA 客户端（easyeda-api 那种写 JavaScript 调几百个接口的方式）容易得多：它只需要写一个设计文件（器件、网络、位置），跑几条命令，按文字报告改。电气上对不对（引脚功能、极性、选型）工具查不出来，原理图出来以后要人看一遍。
