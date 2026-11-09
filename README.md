# EasyEdaTool

[English](README.en.md)

离线命令行工具，读写嘉立创 EDA 专业版（EasyEDA Pro）的文件夹工程。从设计文件生成原理图和 PCB，自动布线，按 EDA 的规则算铺铜，做 DRC 和逐脚核对，并导出原理图 PDF、网表、BOM、Gerber、钻孔和贴片坐标。嘉立创工程与已导出的 PADS ASCII 无需浏览器或 EDA 客户端。原生 PADS 二进制 `.pcb` 导入需 Windows 和本机已授权的 PADS Layout。

0.3.0 增加内置天线电磁仿真、冻结模型多端口求解及 PFC/LLC 电源版图专项检查；支持多候选布局和局部重布。多板项目编辑、FPC补强生产资料、3D局部查看和完整MP157示例继续随包提供。

`em <工程> --config antenna.toml -o output/em`只导出模型，追加`--run`调用随包提供的原生openEMS，无需另外安装Python或求解器。求解完成、频带匹配达标及网格收敛分别记录，详见[电磁仿真说明](skill/references/antenna-em.md)。元件的CAD、尺寸简模与占位体分别标记，裸板显示和模型来源核对见[3D模型说明](skill/references/models-and-pads.md)。

3D模型清单提供眼睛开关（支持逐位号搜索、临时隐藏罩体及全部恢复），导出遵循当前可见性；FR4切边与非金属孔壁改为棕色，镀通孔及邮票孔保留金属色。补齐严格转弯、分支、绕行和悬空检查，并要求实际Gerber全层复查。采购与模型须逐最终料号核对，优先已确认的基础库物料。

## 安装

当前版本 **0.3.0**。安装包在 [GitHub Release v0.3.0](https://github.com/cc38324/PcbCliTool/releases/tag/v0.3.0)，改动见 [发布说明](https://github.com/cc38324/PcbCliTool/blob/main/CHANGELOG.md)。本仓库提供安装说明、AI 使用手册和示例，不包含工具源码。

| 系统 | 0.3.0 安装包 | PCB / 原理图窗口 |
|---|---|---|
| Windows x64 | [ZIP](https://github.com/cc38324/PcbCliTool/releases/download/v0.3.0/easyedatool-0.3.0-windows-x64.zip) / [安装程序](https://github.com/cc38324/PcbCliTool/releases/download/v0.3.0/easyedatool-0.3.0-windows-x64-setup.exe) | 包含 |
| macOS（Apple 芯片） | [完整 ZIP](https://github.com/cc38324/PcbCliTool/releases/download/v0.3.0/easyedatool-0.3.0-macos-arm64.zip) | 包含 |
| macOS（Apple 芯片）命令行 | [CLI tar.gz](https://github.com/cc38324/PcbCliTool/releases/download/v0.3.0/easyedatool-0.3.0-macos-arm64.tar.gz) / Homebrew | 不包含 |
| Ubuntu / Debian amd64 | [DEB](https://github.com/cc38324/PcbCliTool/releases/download/v0.3.0/easyedatool_0.3.0-1_amd64.deb) | 包含 |
| Intel Mac / 鸿蒙电脑 | 本版没有安装包 | — |

完整包包含命令行工具和桌面预览；`easyedatool view <工程>` 打开窗口。项目的线宽、间距、孔径和等长要求由设计文件或规则文件配置，升级不会替用户确认电气设计或生产可行性。

### Windows

推荐下载安装程序，或把 ZIP 解压到任意位置：

```powershell
.\easyedatool\bin\easyedatool.exe --version
.\easyedatool\bin\easyedatool.exe view <工程>
```

安装程序默认放到 `%USERPROFILE%\.claude\skills\easyedatool`。安装程序没有签名，Windows 可能显示 SmartScreen 提示。winget 官方源的收录和版本须以实际查询为准；本次发布不修改官方源，请使用本页 Release 附件。历史清单见 [winget/](winget/README.md)。

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

已装过则用 `brew upgrade cc38324/pcbclitool/easyedatool`。公式位于 [Formula/easyedatool.rb](https://github.com/cc38324/PcbCliTool/blob/main/Formula/easyedatool.rb)，安装 CLI及原生求解器、不含窗口；版本以 `easyedatool --version` 为准。手动安装 CLI 时解开 tar.gz，保留根目录的 `easyedatool`、`VERSION` 和 `runtime/` 相对位置。

### Ubuntu / Debian

下载本版 DEB 后，在下载目录安装；`apt` 会处理窗口所需的系统依赖：

```bash
sudo apt install ./easyedatool_0.3.0-1_amd64.deb
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
sudo apt-get install easyedatool=0.3.0-1
easyedatool --version
```

候选列表没有 `0.3.0-1` 时使用 Release 的 DEB，不要把旧版安装成功当作本版已升级。

## 多板项目、局部3D查看与FPC

`easyedatool view <工程文件夹或.eprj3>` 后，在 PCB / 3D / P1 页签左边的单个下拉中选择主板、功放或电源，对应的 PCB、3D 和原理图会一起切换，并保留查看模式。移动、旋转、翻面、锁定和改线只作用于所选PCB；编辑中先交还或撤销本轮，再切板。原理图逻辑编辑仍需相应设计文件，多板审核尚未实现。

3D中左键拖动旋转，中键或Shift加左键拖动平移，滚轮围绕鼠标位置缩放，双击恢复全板。先平移并放大到角落，再旋转检查该区域。

FPC可记录自定义物理叠层、顶/底面补强材质及局部区域，`fab` 将分材质/面别的补强Gerber和 `jlcpcb.json` 放入生产ZIP。按[设计格式](skill/references/design-format.md)和[FPC流程](skill/references/fpc.md)核对材料、厚度、面别及下单解析；实际优惠以嘉立创订单条件为准。

多网络布线见[整束布线](skill/references/bundle-routing.md)，严格检查见[项目质量门禁](skill/references/routing-quality-gates.md)。

## 本体丝印、布局与整板3D

新画板、重新布局和修改封装时，必须保留元件本体轮廓、芯片1脚及二极管/LED负极标记。先列出全板丝印清单，冲突通过移动或转向元件并重接线路解决，不能删框、裁短或隐藏图层来消除报错。完成后检查丝印/元件间距DRC，并实际查看顶底层Gerber和最新预览。位号文字经用户允许可不印，本体与方向标记仍保留，BOM、坐标和装配图继续保留全部位号。通用配置与完整步骤见 [丝印与布局约束](skill/references/silkscreen.md)。

`render3d <工程> -o board.glb` 导出自包含彩色模型，`-o board.stl` 导出无颜色STL毫米网格（导入时选毫米），`-o board.png` 导出图片；`view <工程> --3d` 打开窗口3D页签。真实模型与外形估算分别标明，按焊盘对齐模型时不移动PCB铜。无模型碰撞检查，估算外形不能用于外壳尺寸验收。需要下载库模型时加 `--download-models`，之后可离线复用缓存。

本版还包括机械安装孔、完整外框/方向标记检查、跨焊盘及过孔的电源细颈复核、原生记录身份保护、项目预览规则读取，以及可配置的布线搜索预算。所有板尺寸、线宽、孔径、间距和筛查阈值仍来自项目设计/规则。

## 例子：STM32MP157

100×80 mm 四层 `JLC04161H-3313`，289 个器件、8 页原理图，保留 ST 的 DDR / 电源核心布局。显示使用用户选定的 **AM319M262928ZS，3.19 英寸 262×928 AMOLED**，CO6300 显示驱动、CST3530 触摸，接 **DF40C-30DS-0.4V(51)（C424642）** 30 针座。MP157 配置一线 DSI；AMOLED 自发光，不需要 LED 背光电路。

[原始屏 PDF、逐脚接法及 1 脚方向](skill/examples/docs/display/README.md)：主板顶视 J6 的 1 脚在右下角、接地。屏图的背视图不能直接当作主板顶视图。提供受控 3.7V、1.8V、2.8V 电源和用于 VCI_EN 的受控 3.3V 输出，触摸、复位、TE 按 1.8V 信号转换。

显示和触摸供电芯片 U18、U16、U17、U28 集中在 J6 附近的底面，开关电源到电感的主干为 0.6 mm。电源检查覆盖 34 个实际网络，从 0.1 mm 起查并贯穿焊盘、过孔；不得抬高起查值漏掉较细分支。按用户确认，仅保留 U5.N2 约 0.09 mm × 0.50 mm 的必要 BGA 短出线，原另一处上拉支路已改为 0.3 mm 绕行。保持四层工艺与 ST 核心器件位置。

在仓库根目录按 `skill/examples/README.md` 的原生命令恢复；程序须支持 `body_silk.pin1.at` 和跨焊盘、过孔的细颈检查：

```powershell
easyedatool --no-drc gen skill/examples/mp157demo.toml --out MP157Demo
easyedatool view MP157Demo
```

完整包内去掉 `skill/` 前缀，程序位于 `bin/`。设计、已布布局、约束和本地库须一并保留，恢复流程见示例README；公开包不附Python构建与专项检查源码。通用DRC不能替代显示30针、封装补偿、供电位置及唯一BGA短出线的专项核对。

1262 个接网引脚逐脚一致，8 页版面无出界、标题栏碰撞或重叠。专项检查核对全部 30 针、未使用的 D1 / ID / VPP 和原始 PDF 哈希。时钟 PCB P/N 长度为 52.285 / 51.463 mm，D0 为 56.341 / 55.560 mm，分别补偿 LFBGA354 内部的 0.822 / 0.781 mm；补偿后的对内误差小于 0.001 mm，时钟与 D0 平均长度差 4.077 mm。11 组差分约束均检查。

按用户要求，ST 密集核心保留常规避焊盘丝印，外围阻容与芯片保留完整外框，方向标记不删。内层 1 是地参考层，另保留约 15 mm 的 PA10 局部连接。工艺警告和布线质量提示保留在 DRC JSON，通用 BOM 项仍需采购选型。

原始 ST AN5122 参考保留在 `skill/build/st/board.PcbDoc`，设计使用相对路径。本例尚未实物点屏；仍须 CO6300 初始化、CST3530 驱动、触摸坐标及模组上下电时序适配，也未完成负载、纹波、EMI 或射频验证。

## 给 AI 用

说明书在 `skill/SKILL.md`，命令、设计文件和规则文件的格式在 `skill/references/`。

工具不限定 AI 模型；支持本地文件和命令执行的 AI 代理可按说明调用。纯聊天界面只读取 GitHub 链接并不能直接运行本机程序。可把下面这段话交给 AI：

> 先读取 [SKILL.md](https://raw.githubusercontent.com/cc38324/PcbCliTool/main/skill/SKILL.md)，按 INSTALL.md 下载当前平台的完整工具包并运行 Demo 自测，再按说明处理工程；修改后提供网表、DRC 和实际预览结果。

完整包已包含 skill、参考文档、MP157 示例、本地库和原始 PDF；不要只复制一个 SKILL.md。GitHub 下载统计不显示使用者的 AI 模型，不能用下载次数判断某款模型的使用人数。
