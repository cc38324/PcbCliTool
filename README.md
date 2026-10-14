# EasyEdaTool

[English](README.en.md)

离线命令行工具，读写嘉立创 EDA 专业版（EasyEDA Pro）的文件夹工程。从设计文件生成原理图和 PCB，自动布线，按 EDA 的规则算铺铜，做 DRC 和逐脚核对，并导出原理图 PDF、网表、BOM、Gerber、钻孔和贴片坐标。不依赖浏览器，也不依赖 EDA 客户端。

## 安装

仓库是 [cc38324/PcbCliTool](https://github.com/cc38324/PcbCliTool)。装好以后命令都是 `easyedatool`。下面按系统写 0.2.0 的装法。发布附件在 `https://github.com/cc38324/PcbCliTool/releases/tag/v0.2.0`。

| 系统 | 0.2.0 |
|---|---|
| Windows | `winget install --id Miyue.PcbCliTool --version 0.2.0` |
| macOS（Apple 芯片） | `brew install cc38324/pcbclitool/easyedatool` |
| Ubuntu 22.04 / 24.04 / 26.04 | 加上 `www.miyue.asia` 的源后 `sudo apt-get install easyedatool` |
| Debian 12 / 13 | 同一个源，命令和 Ubuntu 一样 |
| 鸿蒙电脑 | 0.2.0 还没有鸿蒙安装包 |

### Windows

清单进了 winget 源之后：

```powershell
winget install --id Miyue.PcbCliTool --version 0.2.0
easyedatool --version
```

这一版还没进 winget 源时，下载 Release 里的 `easyedatool-0.2.0-windows-x64.zip`，解压后运行 `easyedatool\bin\easyedatool.exe`。`easyedatool-0.2.0-windows-x64-setup.exe` 双击安装，默认放到 `%USERPROFILE%\.claude\skills\easyedatool`。安装程序没有签名，第一次运行时 Windows 可能要选「更多信息」→「仍要运行」。

### macOS（Apple 芯片）

```bash
brew tap cc38324/pcbclitool https://github.com/cc38324/PcbCliTool.git
brew install cc38324/pcbclitool/easyedatool
easyedatool --version
```

公式是 `Formula/easyedatool.rb`，下载 `easyedatool-0.2.0-macos-arm64.tar.gz`。SHA256：`70f2eff5ff7128aacb2eee2653167b967632004df2680625ce76d1449b475e38`。Intel 的 Mac 这一版没有包。

### Ubuntu

22.04、24.04、26.04，amd64。程序链的 glibc 最高是 2.35。源是 `https://www.miyue.asia/apt`，和 rtsp-ai 同一个。第一次先加上公钥和源：

```bash
sudo mkdir -p /usr/share/keyrings
curl -fsSL https://www.miyue.asia/apt/miyue.gpg | sudo tee /usr/share/keyrings/miyue.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/miyue.gpg] https://www.miyue.asia/apt stable main" | sudo tee /etc/apt/sources.list.d/miyue.list
sudo apt-get update
sudo apt-get install easyedatool
easyedatool --version
```

已经加过这个源（例如装过 rtsp-ai）就只要后两行。装好后程序在 `/usr/bin/easyedatool`。升级也是 `sudo apt-get update && sudo apt-get install easyedatool`。

### Debian

12 和 13，amd64。和 Ubuntu 是同一份 deb、同一个源。第一次：

```bash
sudo mkdir -p /usr/share/keyrings
curl -fsSL https://www.miyue.asia/apt/miyue.gpg | sudo tee /usr/share/keyrings/miyue.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/miyue.gpg] https://www.miyue.asia/apt stable main" | sudo tee /etc/apt/sources.list.d/miyue.list
sudo apt-get update
sudo apt-get install easyedatool
easyedatool --version
```

已经加过这个源就只要 `sudo apt-get update && sudo apt-get install easyedatool`。

### 鸿蒙电脑

0.2.0 没有能在 HiShell 里跑的程序，下面这条现在装不上。有了鸿蒙包之后，先装 [Harmonybrew](https://harmonybrew.atomgit.com)，再：

```bash
brew install easyedatool
```

## 例子：STM32MP157

例子是一块 STM32MP157 单板电脑，板框 100 × 80 mm，四层，叠层 `JLC04161H-3313`。生成出来的工程约 238 个器件（正面 130、背面 108）、1307 个焊盘、851 个过孔、210 个网络。

| 文件 | 内容 |
|---|---|
| `skill/examples/mp157demo.toml` | 设计文件。`easyedatool gen` 用它生成工程 |
| `skill/examples/mp157demo.rules.toml` | 布线、DRC、核对的规则 |
| `skill/examples/mp157demo.constraints.toml` | 差分对（USB、MIPI DSI、网口、DDR） |

设计文件里的 STM32MP157D、DDR、PMIC、eMMC 等写的是元件库料号（`part = "STM32MP157DAB1"` 这一类）。生成前在设计文件旁边放 `easyedatool.toml`，把库的路径写进去。没有库时，用已经生成好的工程文件夹跑下面的查看和检查命令。

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
