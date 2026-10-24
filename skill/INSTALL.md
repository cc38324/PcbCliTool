# easyedatool 安装和使用

嘉立创 EDA 专业版（EasyEDA Pro）文件夹工程的离线工具：从设计文件生成工程、自动布线、铺铜、DRC、核对，出效果图、原理图 PDF / 网表 / BOM、Gerber / 钻孔 / 贴片坐标。完整安装包带 PCB / 原理图桌面预览窗口。

## 安装 0.2.1

下载入口：[GitHub Release v0.2.1](https://github.com/cc38324/PcbCliTool/releases/tag/v0.2.1)。详细步骤见[中文说明](https://github.com/cc38324/PcbCliTool/blob/main/README.md)和[英文说明](https://github.com/cc38324/PcbCliTool/blob/main/README.en.md)。

| 平台 | 文件 | 窗口 |
|---|---|---|
| Windows x64 | `easyedatool-0.2.1-windows-x64.zip` 或 `easyedatool-0.2.1-windows-x64-setup.exe` | 包含 |
| macOS Apple 芯片 | `easyedatool-0.2.1-macos-arm64.zip` | 包含 |
| macOS Apple 芯片，仅 CLI | `easyedatool-0.2.1-macos-arm64.tar.gz` 或 Homebrew | 不包含 |
| Ubuntu / Debian amd64 | `easyedatool_0.2.1-1_amd64.deb` | 包含 |

Windows 安装程序默认放到 `%USERPROFILE%\.claude\skills\easyedatool`；ZIP 可解压到任意目录。安装程序未签名。**尚未确认本版进入 winget 官方源，请直接使用 Release 安装包。**

macOS 完整 ZIP 的程序在 `bin/easyedatool`，窗口在 `viewer/easyeda_view.app`，保留两者的相对位置。安装包未经 Apple 公证；系统拦截时先核对来源与校验和，再从系统安全设置允许打开。

Homebrew 仅安装命令行程序：

```bash
brew tap cc38324/pcbclitool https://github.com/cc38324/PcbCliTool.git
brew update
brew install cc38324/pcbclitool/easyedatool
easyedatool --version
```

已安装则用 `brew upgrade cc38324/pcbclitool/easyedatool`。Linux 在下载目录执行：

```bash
sudo apt install ./easyedatool_0.2.1-1_amd64.deb
easyedatool --version
easyedatool view <工程>
```

APT 源的添加方法见中文说明。先用 `apt-cache policy easyedatool` 确认有 `0.2.1-1`，没有时安装 Release 的 DEB；不能把源里的旧版当成升级成功。Linux 窗口需要图形桌面。Intel Mac 和鸿蒙电脑本版没有安装包。

## 完整 ZIP 的文件

```text
easyedatool/
  bin/easyedatool.exe    Windows 命令行程序；macOS 对应 bin/easyedatool
  viewer/               窗口及运行文件；不要单独移动里面的 exe 或 app
  SKILL.md              给 AI 的使用说明
  references/           全部命令参数、设计格式、规则格式、与 EDA 配合
  examples/             MP157 示例、规则及所需元件库
  build/st/board.PcbDoc  MP157 示例引用的 AN5122 参考板
  AGENTS.md             引导 AI 先读 SKILL.md
  README.md             人看的安装和使用说明
  VERSION               包版本和构建来源
```

CLI tar.gz 和 DEB 的布局不同，不要把上述 ZIP 目录结构套用到它们。

## 自己用

Windows ZIP 解压后运行 `bin\easyedatool.exe --help`；macOS ZIP 运行 `bin/easyedatool --help`。使用包管理器安装的 CLI 直接运行 `easyedatool --help`。每个子命令也支持 `--help`，输出为中文。

`easyedatool view <工程>` 打开预览，显示 PCB / 原理图、布线过程和检查结果。放大后可显示网络名，Ctrl + 单击走线、焊盘或过孔追加或取消网络高亮；Esc 清空。窗口的「开始改」会进入编辑回合，修改由工具服务写入工程；「改完了，交给 AI」后再继续命令行改板。使用前先提交工程，修改后运行检查并核对实际画面。

上手看 `SKILL.md` 的「画一块新板」和「快速自测」。MP157 示例自带元件库和参考板，应保留示例文件的相对位置。

## 给 AI 使用

Windows 安装程序会放到 Claude Code 的 skill 目录。使用完整 ZIP 时，也可把整个 `easyedatool` 文件夹放到 `%USERPROFILE%\.claude\skills\`；macOS 对应 `~/.claude/skills/`。重开客户端后，让 AI 先读 `SKILL.md`，再按说明调用工具。

其他 AI 工具可直接指定 `SKILL.md` 路径，在规则文件中要求先读它；`references/` 按需读取。不要只复制一个 SKILL.md，遗漏命令说明、示例和元件库。

工具可以检查文件结构、铜连接和配置规则，器件引脚功能、极性、选型及实际电气设计仍须核对。不能把布通或 DRC 通过等同于已具备生产条件。
