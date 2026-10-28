# EasyEdaTool

[English](README.en.md)

离线命令行工具，读写嘉立创 EDA 专业版（EasyEDA Pro）的文件夹工程。从设计文件生成原理图和 PCB，自动布线，按 EDA 的规则算铺铜，做 DRC 和逐脚核对，并导出原理图 PDF、网表、BOM、Gerber、钻孔和贴片坐标。嘉立创工程与已导出的 PADS ASCII 无需浏览器或 EDA 客户端。原生 PADS 二进制 `.pcb` 导入需 Windows 和本机已授权的 PADS Layout。

0.2.3 合入 PADS 原生 `.pcb` 导入及混合公英制封装修正，并修复 3D 板体漏掉独立安装孔的问题。安装孔和槽孔真实挖穿并生成孔壁；支持 PNG、GLB 及 STL，Flutter 窗口可分别导出两种模型。完整元件丝印与避让约束继续保留。

## 安装

当前版本 **0.2.3**。安装包在 [GitHub Release v0.2.3](https://github.com/cc38324/PcbCliTool/releases/tag/v0.2.3)，改动见 [发布说明](https://github.com/cc38324/PcbCliTool/blob/main/CHANGELOG.md)。本仓库提供安装说明、AI 使用手册和示例，不包含工具源码。

| 系统 | 0.2.3 安装包 | PCB / 原理图窗口 |
|---|---|---|
| Windows x64 | [ZIP](https://github.com/cc38324/PcbCliTool/releases/download/v0.2.3/easyedatool-0.2.3-windows-x64.zip) / [安装程序](https://github.com/cc38324/PcbCliTool/releases/download/v0.2.3/easyedatool-0.2.3-windows-x64-setup.exe) | 包含 |
| macOS（Apple 芯片） | [完整 ZIP](https://github.com/cc38324/PcbCliTool/releases/download/v0.2.3/easyedatool-0.2.3-macos-arm64.zip) | 包含 |
| macOS（Apple 芯片）命令行 | [CLI tar.gz](https://github.com/cc38324/PcbCliTool/releases/download/v0.2.3/easyedatool-0.2.3-macos-arm64.tar.gz) / Homebrew | 不包含 |
| Ubuntu / Debian amd64 | [DEB](https://github.com/cc38324/PcbCliTool/releases/download/v0.2.3/easyedatool_0.2.3-1_amd64.deb) | 包含 |
| Intel Mac / 鸿蒙电脑 | 本版没有安装包 | — |

完整包包含命令行工具和桌面预览；`easyedatool view <工程>` 打开窗口。项目的线宽、间距、孔径和等长要求由设计文件或规则文件配置，升级不会替用户确认电气设计或生产可行性。

### Windows

推荐下载安装程序，或把 ZIP 解压到任意位置：

```powershell
.\easyedatool\bin\easyedatool.exe --version
.\easyedatool\bin\easyedatool.exe view <工程>
```

安装程序默认放到 `%USERPROFILE%\.claude\skills\easyedatool`。安装程序没有签名，Windows 可能显示 SmartScreen 提示。**2026-10-28 刷新官方源后，未查到 `Miyue.PcbCliTool`**。[0.2.0 收录申请 #452460](https://github.com/microsoft/winget-pkgs/pull/452460) 已通过自动验证，仍待维护者审核合入。0.2.3 的清单见 [winget/](winget/README.md)，已通过本地格式验证；这不代表官方源已可安装。当前请使用 Release 附件。

### macOS（Apple 芯片）

需要窗口时下载完整 ZIP，解压后运行：

```bash
./easyedatool/bin/easyedatool --version
./easyedatool/bin/easyedatool view <工程>
```

窗口位于 `easyedatool/viewer/easyeda_view.app`，应与 `bin/` 保持原有相对位置。安装包未经 Apple 公证；若系统阻止启动，先核对下载来源及校验和，再按 macOS 的安全设置允许打开。

只用命令行时可使用 Homebrew：

```bash
brew tap cc38324/pcbclitool https://github.com/cc38324/PcbCliTool.git
brew update
brew install cc38324/pcbclitool/easyedatool
easyedatool --version
```

已装过则用 `brew upgrade cc38324/pcbclitool/easyedatool`。公式位于 [Formula/easyedatool.rb](https://github.com/cc38324/PcbCliTool/blob/main/Formula/easyedatool.rb)，仅安装 CLI；版本以 `easyedatool --version` 为准。手动安装 CLI 时解开 tar.gz，根目录的 `easyedatool` 就是程序。

### Ubuntu / Debian

下载本版 DEB 后，在下载目录安装；`apt` 会处理窗口所需的系统依赖：

```bash
sudo apt install ./easyedatool_0.2.3-1_amd64.deb
easyedatool --version
easyedatool view <工程>
```

DEB 面向 amd64 的 Ubuntu / Debian。窗口需要图形桌面；无图形环境仍可使用 CLI。各平台实际验证范围见 [发布说明](https://github.com/cc38324/PcbCliTool/blob/main/CHANGELOG.md)。

也可使用现有 APT 源。它的更新进度可能晚于 GitHub Release，安装前检查候选版本：

```bash
sudo mkdir -p /usr/share/keyrings
curl -fsSL https://www.miyue.asia/apt/miyue.gpg | sudo tee /usr/share/keyrings/miyue.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/miyue.gpg] https://www.miyue.asia/apt stable main" | sudo tee /etc/apt/sources.list.d/miyue.list
sudo apt-get update
apt-cache policy easyedatool
sudo apt-get install easyedatool=0.2.3-1
easyedatool --version
```

候选列表没有 `0.2.3-1` 时使用 Release 的 DEB，不要把旧版安装成功当作本版已升级。

## 0.2.3：本体丝印、布局与整板3D

新画板、重新布局和修改封装时，必须保留元件本体轮廓、芯片1脚及二极管/LED负极标记。先列出全板丝印清单，冲突通过移动或转向元件并重接线路解决，不能删框、裁短或隐藏图层来消除报错。完成后检查丝印/元件间距DRC，并实际查看顶底层Gerber和最新预览。位号文字经用户允许可不印，本体与方向标记仍保留，BOM、坐标和装配图继续保留全部位号。通用配置与完整步骤见 [丝印与布局约束](skill/references/silkscreen.md)。

`render3d <工程> -o board.glb` 导出自包含彩色模型，`-o board.stl` 导出无颜色STL毫米网格（导入时选毫米），`-o board.png` 导出图片；`view <工程> --3d` 打开窗口3D页签。真实模型与外形估算分别标明，按焊盘对齐模型时不移动PCB铜。无模型碰撞检查，估算外形不能用于外壳尺寸验收。需要下载库模型时加 `--download-models`，之后可离线复用缓存。

本版还包括机械安装孔、完整外框/方向标记检查、跨焊盘及过孔的电源细颈复核、原生记录身份保护、项目预览规则读取，以及可配置的布线搜索预算。所有板尺寸、线宽、孔径、间距和筛查阈值仍来自项目设计/规则。

## 例子：STM32MP157

以下文件路径以本仓库根目录为起点。完整 ZIP 将 `skill/` 里的内容放在解压目录 `easyedatool/` 下；在包内执行示例时去掉路径中的 `skill/` 前缀，例如 `easyedatool gen examples/mp157demo.toml --out MP157Demo`。

例子是一块 STM32MP157 单板电脑，板框 100 × 80 mm，四层，叠层 `JLC04161H-3313`。生成出来的工程约 238 个器件（正面 130、背面 108）、1307 个焊盘、851 个过孔、210 个网络。

| 文件 | 内容 |
|---|---|
| `skill/examples/mp157demo.toml` | 设计文件。`easyedatool gen` 用它生成工程 |
| `skill/examples/mp157demo.rules.toml` | 布线、DRC、核对的规则 |
| `skill/examples/mp157demo.constraints.toml` | 差分对（USB、MIPI DSI、网口、DDR） |

设计文件里有 23 种元件库器件（30 处，`part = "STM32MP157DAB1"` 这一类）。每种都写了立创料号（`lcsc = "C1236721"` 这一类）。符号和封装在 `skill/examples/lib`（23 个符号、21 个封装，有的件共用一个封装），`skill/examples/easyedatool.toml` 指向这个库。

核心电路的参考布局是 `skill/build/st/board.PcbDoc`。它来自意法半导体 AN5122 的布线例程包 `stm32mp15x-series-ddr-memory-routing-guidelines-examples.zip`，里面 `STM32MP15XXAB/STM32MP15XXAB_1DDR3Lx16` 的 Altium 板文件，抽出来后改叫这个名字。设计文件的 `[[reuse]]` 用相对路径 `../build/st/board.PcbDoc` 指着它。

下面把工程文件夹写成 `<工程>`。`route` 会改写板子；这条规则里有 `keep = ["*"]`，已有走线留着，只补还没连上的。先提交 git，不满意就回滚。嘉立创开着这个工程时，先关掉 PCB 页再写文件，写完再打开。

```bash
easyedatool gen skill/examples/mp157demo.toml --out MP157Demo

easyedatool info   <工程>
easyedatool render <工程> --view top -o MP157_top.png
easyedatool render <工程> --view layers -o MP157_layers.png
easyedatool render <工程> --view sch -o MP157_sch.png

easyedatool check <工程> --rules skill/examples/mp157demo.rules.toml
easyedatool erc   <工程>
easyedatool drc   <工程> --rules skill/examples/mp157demo.rules.toml

easyedatool route <工程> --rules skill/examples/mp157demo.rules.toml
easyedatool constraints <工程> --from skill/examples/mp157demo.constraints.toml
easyedatool pair  <工程> --pair USBH
easyedatool pour  <工程>

easyedatool pdf     <工程> -o MP157_sch.pdf
easyedatool netlist <工程> -o MP157.net
easyedatool bom     <工程> -o MP157_bom.csv
easyedatool fab     <工程> -o MP157_fab
easyedatool view    <工程>
```

`drc`、`check`、`erc` 查出问题时退出码是 1，那是检查结果。每个命令加 `--help` 看全部参数。

## 给 AI 用

说明书在 `skill/SKILL.md`，命令、设计文件和规则文件的格式在 `skill/references/`。
