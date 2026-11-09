# easyedatool 安装和使用

嘉立创 EDA 专业版（EasyEDA Pro）文件夹工程的离线工具：从设计文件生成工程、自动布线、铺铜、DRC、核对，出效果图、原理图 PDF / 网表 / BOM、Gerber / 钻孔 / 贴片坐标。完整安装包带 PCB / 原理图桌面预览窗口。

## 安装 0.3.0

下载入口：[GitHub Release v0.3.0](https://github.com/cc38324/PcbCliTool/releases/tag/v0.3.0)。详细步骤见[中文说明](https://github.com/cc38324/PcbCliTool/blob/main/README.md)和[英文说明](https://github.com/cc38324/PcbCliTool/blob/main/README.en.md)。

| 平台 | 文件 | 窗口 |
|---|---|---|
| Windows x64 | `easyedatool-0.3.0-windows-x64.zip` 或 `easyedatool-0.3.0-windows-x64-setup.exe` | 包含 |
| macOS Apple 芯片 | `easyedatool-0.3.0-macos-arm64.zip` | 包含 |
| macOS Apple 芯片，仅 CLI | `easyedatool-0.3.0-macos-arm64.tar.gz` 或 Homebrew | 不包含 |
| Ubuntu / Debian amd64 | `easyedatool_0.3.0-1_amd64.deb` | 包含 |

Windows 安装程序默认放到 `%USERPROFILE%\.claude\skills\easyedatool`；ZIP 可解压到任意目录。安装程序未签名。winget 官方源状态请实际查询；本次使用 Release 附件，不声称官方源已经收录 0.3.0。

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
sudo apt install ./easyedatool_0.3.0-1_amd64.deb
easyedatool --version
easyedatool view <工程>
```

APT 源的添加方法见中文说明。先用 `apt-cache policy easyedatool` 确认有 `0.3.0-1`，没有时安装 Release 的 DEB；不能把源里的旧版当成升级成功。Linux 窗口需要图形桌面。Intel Mac 和鸿蒙电脑本版没有安装包。

## 完整 ZIP 的文件

```text
easyedatool/
  bin/easyedatool.exe    Windows 命令行程序；macOS 对应 bin/easyedatool
  viewer/               窗口及运行文件；不要单独移动里面的 exe 或 app
  SKILL.md              给 AI 的使用说明
  references/           全部命令参数、设计格式、规则格式、与 EDA 配合
  examples/             简单自测、MP157 参考示例、规则及所需元件库
  build/st/board.PcbDoc  MP157 示例引用的 AN5122 参考板
  AGENTS.md             引导 AI 先读 SKILL.md
  README.md             人看的安装和使用说明
  VERSION               包版本和构建来源
```

CLI tar.gz 和 DEB 的布局不同，不要把上述 ZIP 目录结构套用到它们。

## 自己用

Windows ZIP 解压后运行 `bin\easyedatool.exe --help`；macOS ZIP 运行 `bin/easyedatool --help`。使用包管理器安装的 CLI 直接运行 `easyedatool --help`。每个子命令也支持 `--help`，输出为中文。

`easyedatool view <工程>` 打开预览，显示 PCB / 原理图、布线过程和检查结果。放大后可显示网络名，Ctrl + 单击走线、焊盘或过孔追加或取消网络高亮；Esc 清空。窗口的「开始改」会进入编辑回合，修改由工具服务写入工程；「改完了，交给 AI」后再继续命令行改板。使用前先提交工程，修改后运行检查并核对实际画面。

上手看 `SKILL.md` 的「画一块新板」和「快速自测」。MP157 是已布线的完整例子，包含本地元件库、原始屏 PDF 和参考板，应保留相对位置。从0.2.7起不附Python辅助源码，按 `examples/README.md` 的原生命令恢复并检查：

```powershell
bin/easyedatool.exe --no-drc gen examples/mp157demo.toml --out MP157Demo
bin/easyedatool.exe view MP157Demo
```

macOS / Linux 将工具路径改为 `bin/easyedatool`。继续按例子README恢复约束与标注，执行通用检查，再单独核对显示、触摸、电源及BGA例外；通过后导出图纸和生产文件，实物验证状态见 `examples/README.md`。

## 给 AI 使用

Windows 安装程序会放到 Claude Code 的 skill 目录。使用完整 ZIP 时，也可把整个 `easyedatool` 文件夹放到 `%USERPROFILE%\.claude\skills\`；macOS 对应 `~/.claude/skills/`。重开客户端后，让 AI 先读 `SKILL.md`，再按说明调用工具。

其他 AI 工具可直接指定 `SKILL.md` 路径，在规则文件中要求先读它；`references/` 按需读取。不要只复制一个 SKILL.md，遗漏命令说明、示例和元件库。

工具可以检查文件结构、铜连接和配置规则，器件引脚功能、极性、选型及实际电气设计仍须核对。不能把布通或 DRC 通过等同于已具备生产条件。

新画板和布局/封装修改必须保留元件本体丝印、1脚及极性标记。冲突须调整位置/方向并重接，不能删框；交付前核对实际Gerber和PCB预览。见 `references/silkscreen.md`。

整板3D：`render3d <工程> -o board.glb` 或 `view <工程> --3d`；无模型时明确显示外形估算。

0.3.0各安装包均可直接运行天线仿真。macOS CLI包也须保留 `easyedatool`、`VERSION` 与 `runtime/` 的相对位置，不能只拷贝单个程序。完整包同时保留 `bin/`、`viewer/` 与 `runtime/`。PFC/LLC专项规则见 `references/smps-pfc-llc.md`。
