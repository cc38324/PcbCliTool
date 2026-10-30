# 发布说明 / Release notes

## 0.2.5 — 2026-10-30

将射频核心板开发中可复用的能力加入工具与AI手册：

- `em`从原生PCB导出实际铜形、叠层与端口，`--run`调用另行安装的openEMS；窗口增加配置选择入口。求解完成、频带匹配、时间衰减和网格收敛分别记录，不把导出成功当作天线达标。
- 设计文件支持实体铜形和开窗；保存布局、重新生成及局部改线保留盲埋孔的实际铜层跨度。邮票孔板边规则只适用于显式配置且符合几何条件的镀半孔。
- 共用DRC空间索引，保留判定规则并稳定问题顺序；3D渲染与连续操作刷新优化保留几何、纹理、钻孔及遮挡。
- skill补充裸核心板显隐、立创/厂家模型获取边界、表面CAD转换、安装面与方向核对，以及整份模型配方的来源保留。板尺寸、器件料号、网络和模型覆盖均留在工程数据中。
- 完整包附30×20 mm四层原生天线流程示例。示例共用端口配置并校核生成几何，用户无需编译Rust即可导出模型。该示例尚未通过天线性能或网格收敛验收。

| 验证 | 本次结果 |
|---|---|
| Windows / macOS arm64 / Linux x64 | 各421项Rust测试通过、2项原有忽略；Flutter分析0问题、31项测试通过 |
| 最终安装包Demo | 三平台逐脚差异0、5/5布通、电气DRC通过；保留示例原有6条字高警告 |
| 实际窗口 | 三平台PCB、原理图、3D截图已查看；GLB/STL导出通过 |
| 安装与升级 | Windows安装文件逐项与ZIP一致；Ubuntu 22.04容器从0.2.4-1升级到0.2.5-1通过 |
| MP157完整示例 | 三平台冷启动重建、显示/电源/逐脚检查和导出通过；电气铜、元件位置及位号身份跨平台核对一致 |
| 电磁接口 | 三平台最终包均成功导出天线示例；Windows实际调用openEMS 0.37.0rc3完成流程冒烟测试，未确认时间及网格收敛，未配置匹配目标 |
| 裸板3D回归 | 71个可见元件、4个隐藏体，电气文件不变，效果图与先前版本逐字节一致 |
| 包内容 | 6个二进制附件及4个完整包中的169个公开文档/示例资产独立核对通过 |

CLI与窗口来源为`d16d7e1e5edc0308682c650321a6a588c479d16c`，安装器和可复用示例修正来源为`615ae374dab1833a93bef2eadc77e00c6bb369e0`；包内公开文档固定到`06839b51ef6f79880e0a9df88e8b6756f1e4866e`。具体版本、来源、验证及SHA256见附件`build-info.json`、`SHA256SUMS.txt`。

Homebrew Formula已更新到本版macOS CLI的真实URL及SHA256。本次未同步APT或winget官方源，使用[Release附件](https://github.com/cc38324/PcbCliTool/releases/tag/v0.2.5)安装。Windows包未签名，macOS包未公证。模型缺失或未完全匹配时继续标为近似；电气DRC及流程测试不代替装配、实物供电或射频验证。

### English

This release adds a configurable PCB-to-openEMS workflow, design-file copper shapes and mask openings, blind/buried-via span preservation, explicit castellation rules, deterministic DRC indexing and faster interactive 3D rendering. The AI manual covers bare-core views, model provenance, surface-CAD conversion and mechanical alignment. Board-specific dimensions, nets, part choices and model overrides remain project data. A native four-layer antenna workflow example ships in every full package; openEMS and its matching Python dependencies are installed separately.

Each platform passed 421 Rust tests (2 existing ignored tests), clean Flutter analysis and 31 widget tests. Final Windows/macOS/Linux packages passed Demo connectivity/routing, actual PCB/schematic/3D windows, GLB/STL and EM export. Windows installation matches its ZIP file for file; Linux upgrades from 0.2.4-1 in Ubuntu 22.04. The complete MP157 example rebuilds and exports on all platforms, with matching physical copper/component records and reference identities. A Windows openEMS smoke run completed, with no matching target and no verified time or mesh convergence. The bare-core regression preserves the electrical files and produces a byte-identical image. All six binaries and 169 public documentation/example assets in each full package were checked.

See build-info.json for component sources and actual verification. Homebrew is updated; APT and winget official sources are unchanged by this release. Windows binaries are unsigned and macOS is not notarized. Approximate models and unvalidated antenna geometry retain their stated limits.

## 0.2.4 — 2026-10-29

完整 STM32MP157 AMOLED / 触摸示例随三平台完整包提供：AM319M262928ZS 一线 MIPI、CST3530 触摸、DF40 30 针座，附原始屏 PDF、1 脚方向说明、已布线布局、本地元件库和构建检查。显示与触摸供电芯片集中在 J6 附近，全板电源加粗，检查覆盖 34 个电源网络并贯穿焊盘和过孔。普通中段细颈为 0；按用户确认，仅保留 U5.N2 约 0.09 mm × 0.50 mm 的必要 BGA 短出线，维持 ST 核心器件位置和四层工艺。

本版还提供 `holes` 安装孔孔径同步、`model3d` 参数建模与绑定、`pad-edit` 下载封装铜面编辑、无焊盘机械件和散热器示例，以及不贴装/近似 3D 模型标记。新增封装局部坐标的 1 脚标记位置，修正差分端部颈缩导致宽主干被误拒绝的问题。所有新功能均按当前工程的数据与规则运行。

公开 skill、安装说明、参数模型/焊盘/散热器/变压器参考已同步。支持具备文件和命令工具的 AI 代理；完整包包含所需参考、例子和库，不限定模型。MP157 构建脚本需要 Python 3.11 或更新版本。

| 验证 | 本次结果 |
|---|---|
| Windows / macOS arm64 / Linux x64 | 各 397 项 Rust 测试通过、2 项忽略；Flutter 分析 0 问题、30 项测试通过 |
| 三平台完整包 Demo | 13 脚差异 0、5/5 布通、电气 DRC 0；保留原有 6 条字高警告 |
| 实际窗口 | 三平台 PCB、原理图、3D 截图已查看，未见运行异常；GLB / STL 导出通过 |
| Windows 安装器 | 安装后的全部文件逐一与最终 ZIP 一致 |
| Linux 升级 | Ubuntu 22.04 独立容器验证 0.2.3-1 → 0.2.4-1 |
| 三平台 MP157 冷启动 | 289 器件、8 页、1262 接网脚差异 0；11 对差分、显示与电源专项通过，图纸和生产文件均导出 |
| 例子依赖 | 40 个本地元件清单引用完整，包含带 ℃ 字符的符号文件；原始 PDF 哈希一致 |
| 最终包内容 | 四个完整包的 163 个公开文档/示例文件逐项一致，无内部目录、地址、源码归档或凭据 |

CLI、窗口和 Windows 安装器来源为 `f2515a3519e27e607a6cbf870f7a62429a0052fc`，包内文档固定到公开提交 `9e2fa5ffac7db099fb6ece12b21ad7c3d2a07844`。SDK、附件大小与 SHA256 见 `build-info.json` 和 `SHA256SUMS.txt`。

跨平台比对确认电气铜、元件位置、引脚网络和约束一致；系统字体会影响常规丝印裁切和位号位置，库文档时间戳也受时区影响，不声称跨平台原始文件逐字节相同。MP157 尚未实物点屏，仍需 CO6300 初始化、CST3530 驱动、时序、负载、纹波、EMI 和射频验证；原有工艺提示保留在检查报告中。

Homebrew Formula 已更新到本版 CLI 的实际 URL 和 SHA256。本次未更新 APT 或 winget 官方源，安装使用 [v0.2.4 Release](https://github.com/cc38324/PcbCliTool/releases/tag/v0.2.4) 附件。Windows 包未签名，macOS 包未公证；近似 3D 模型不能用于机壳尺寸或碰撞验收。

### English

The complete STM32MP157 AMOLED/touch example now ships with the Windows, Apple-silicon macOS and Linux full packages, including saved copper, a local library, the original panel PDF, connector pin-1 notes and build checks. Display supplies are near J6; ordinary intermediate power necks are zero across 34 checked nets, with only the approved U5.N2 BGA escape retained. ST core placement and the four-layer process are preserved.

This version also adds mounting-hole diameter synchronization, parametric 3D modelling/binding, downloaded-footprint pad editing, mechanical/heatsink examples and assembly-model flags, plus pin-1 and differential-neck fixes. The public AI manual and all referenced guides are synchronized. The MP157 helper requires Python 3.11 or newer.

Each platform passed 397 Rust tests (2 ignored), clean Flutter analysis and 30 widget tests. Final-package Demo, PCB/schematic/3D windows and GLB/STL checks passed. The Windows installer matches its ZIP file for file, and Linux upgrades from 0.2.3-1 in Ubuntu 22.04. The MP157 example rebuilt and exported successfully on all three platforms: 1262 connected pins match, 11 differential pairs pass, and display/power checks pass. All 40 local part manifests resolve, including Unicode library filenames, and all four full packages contain the same 163 public documentation/example files.

Electrical copper, component positions, pin assignments and constraints match across platforms; system fonts affect silkscreen/designator layout and library metadata timestamps can reflect the time zone. Raw native-file byte identity across platforms is not claimed. Physical display/touch operation and electrical prototype testing remain unverified. Homebrew is updated; APT/winget official sources are unchanged by this release. Windows binaries are unsigned and the macOS app is not notarized.

## 0.2.3 — 2026-10-28

独立机械安装孔与槽孔现在真实挖穿3D板体正反面并生成孔壁；偏心通孔按钻孔中心定位，板体背面和孔壁使用一致向外的三角形方向。原先只处理焊盘孔与过孔，会把独立安装孔画成实心，这个问题已在共用几何层修复，PNG、GLB及Flutter预览一并生效。

新增二进制STL导出：`render3d <工程> -o board.stl`，Flutter 3D页也分别提供“导出 STL”和“导出 GLB”。STL坐标为毫米、z向上，不带颜色；导入CAD时选择毫米。GLB保留颜色和贴图，按glTF标准使用米和y向上。两种格式都保留同一份板体、安装孔和元件几何。元件模型仍可能是明确标注的外形估算，不能用估算件验收外壳尺寸。

合入PADS原生二进制`.pcb`导入：Windows通过本机已安装、已授权的PADS Layout，对私有副本执行官方ASCII导出后复用现有转换及自检；源文件不保存、不修改，也不接管已有PADS会话。非Windows或未安装授权PADS时使用已导出的`.asc`。同时修正METRIC导出混用英制/公制封装的尺寸；BASIC归一化数据保持原行为。

保留完整元件本体丝印、1脚/极性标记和避让约束。开发与发布使用主工作区，打包支持`CARGO_TARGET_DIR`；修复迁移构建缓存后的Windows安装器资源路径，以及缺少资源编译器时的备用UAC清单。

| 验证 | 本次结果 |
|---|---|
| 三平台Rust / Flutter | 各380项Rust通过、2项忽略；Flutter分析0问题、30项测试通过，全部重建 |
| 最终包Demo | 三平台13脚差异0、5/5布通、电气DRC 0；原有6条字高警告保留 |
| 实际窗口 | 三平台PCB、原理图、3D截图已查看，无运行异常；STL/GLB导出均通过 |
| Windows安装 | 正常与无资源编译器两条路径都可安装，文件逐一与ZIP一致 |
| Linux升级 | 独立Ubuntu 22.04容器验证0.2.2-1→0.2.3-1 |
| 实际模型 | 独立安装孔与NPTH钻孔吻合，STL/GLB孔位与毫米尺寸一致；预览接口与CLI输出逐字节一致 |
| PADS真实文件 | 180器件、473焊盘、949过孔几何自检无差异，源文件哈希不变；所配参考DSN的原版15处网络差异按原样报告 |
| 包内文档 | 四个完整包的86个公开文档/示例文件逐项一致，无内部说明或地址 |

CLI与窗口来源均为`c62d326daccdd371edd80adfff1bb854850e6f2f`，Windows安装器来源`770cc4dbfaee67ce9a2238ca01d105c8bf3373a2`，包内文档固定到`ecc370e31fd42027e42f0fb3b4a96c5fb2d36e4a`。构建SDK、完整验证和六个二进制附件的SHA256见`build-info.json`与`SHA256SUMS.txt`。

下载：[v0.2.3 Release](https://github.com/cc38324/PcbCliTool/releases/tag/v0.2.3)。Homebrew Formula使用本版CLI真实URL和SHA256。APT本轮未同步，仍为0.2.1-1，本版使用Release的0.2.3-1 DEB。

winget官方源尚未找到`Miyue.PcbCliTool`：[0.2.0收录申请 #452460](https://github.com/microsoft/winget-pkgs/pull/452460) 等待维护者批准。0.2.3清单引用最终Windows ZIP并通过本地格式验证；LocalManifestFiles未启用，未声称本地清单或官方源安装成功，未修改管理员设置。

### English

Mechanical mounting holes and routed slots now cut both PCB faces with real walls in the shared PNG, GLB and Flutter geometry. Offset pad drills use their actual drill origin; bottom and wall triangles face outwards.

STL export is available from the CLI and Flutter viewer alongside GLB. STL contains geometry in millimetres, z-up, without colours; import as mm. GLB preserves materials and follows glTF metre/y-up conventions. Both share the same component and drilled-board geometry. Approximate models remain labelled and cannot validate enclosure dimensions.

Native PADS binary PCB import uses an installed, licensed Windows PADS Layout to export a private copy through official automation. Original files and existing PADS sessions remain untouched. Other platforms use exported ASCII. Mixed metric/imperial decal units are corrected without changing normalized BASIC exports.

Each platform passed 380 Rust tests (2 ignored), clean Flutter analysis and 30 widget tests. Final packages passed the Demo, both model formats and actual PCB/schematic/3D window checks. Windows normal and manifest-fallback installers match the ZIP file for file; Linux upgrades from 0.2.2-1 in an isolated Ubuntu 22.04 container. The reference PADS PCB geometry matches; its paired schematic retains 15 pre-existing net differences. The legacy Demo retains 6 text-height warnings.

Source commits are recorded above and in build-info.json. Winget still awaits maintainer approval; schema validation does not establish installation availability. APT remains 0.2.1-1. Windows/macOS packages are unsigned/unnotarized.


## 0.2.2 — 2026-10-28

AI skill 将元件本体丝印完整性及避让作为交付约束：先列出全板元件及丝印清单，保留完整外框、芯片1脚和二极管/LED负极条。冲突通过移动/转向元件并重接线路解决，禁止删框、裁短或隐藏图层规避检查；交付核对DRC、实际顶底层Gerber与最新PCB预览。器件范围和参数均由项目设计/规则配置。

本版包含上次发布后的通用改进：整板3D PNG/GLB导出及Flutter 3D页签、模型与焊盘对齐、完整本体外框与方向标记检查、局部布局避让、机械安装孔、电源跨焊盘/过孔细颈检查、原生过孔身份保护、独立原理图文字更新、工程预览规则及可配置搜索预算。源代码未加入具体项目的固定坐标、板尺寸或网络参数。

| 验证 | 本次结果 |
|---|---|
| Windows / macOS arm64 / Linux x64 Rust | 各375项通过，2项忽略，0失败 |
| 三平台Flutter | 分析0问题，各30项测试通过；均重新构建 |
| 最终包内Demo | 三平台13脚差异0，5/5布通，电气DRC 0；示例原有6条字高警告保留 |
| 实际窗口 | 三平台PCB、原理图和3D均启动并实际查看截图，无运行异常 |
| Windows安装 | 安装程序解出的全部文件与最终ZIP逐一一致 |
| Linux升级 | 在独立Ubuntu 22.04容器验证0.2.1-1→0.2.2-1，依赖与动态库检查通过 |
| 丝印正反例 | 6个完整框、2个1脚标记、1条负极条，DRC错误/警告0；故意挤近电容时铜间距仍合格，但正确报告frame_clash；实际Gerber已查看 |
| 文档与产物 | 4个完整包内86个公开文档/示例文件逐项一致；CLI tar根目录正确；无内部说明、地址或源码归档 |

CLI与窗口来源均为 `fcebccdb742707de65829384e59d2aff8ca3815d`；包内文档固定到 `637c433135322b7a3e1fbd0eeb673d86b98d8b06`。Flutter 3.41.9 / Dart 3.11.5，锁文件不变；Rust为Windows/macOS 1.98.1、Linux 1.99.0。完整来源、测试和每个附件SHA256见Release附件 `build-info.json`、`SHA256SUMS.txt`。

Windows完整ZIP/安装程序、macOS arm64完整ZIP/CLI tar.gz、Linux amd64 DEB/完整tar.gz均在 [v0.2.2 Release](https://github.com/cc38324/PcbCliTool/releases/tag/v0.2.2)。Homebrew Formula已指向本版CLI及真实校验和。APT源本轮未同步，当前仍为0.2.1-1，安装本版请用Release的0.2.2-1 DEB。

winget官方源当前未查到 `Miyue.PcbCliTool`。[0.2.0收录申请 #452460](https://github.com/microsoft/winget-pkgs/pull/452460) 已通过自动验证、仍待维护者批准。0.2.2清单已用本版ZIP真实SHA256通过本地格式验证；本机LocalManifestFiles未启用，本轮未声称本地或官方源安装通过，也未改变管理员设置。

限制：3D缺模型会明确显示外形估算，无模型碰撞检查；不能用估算外形验收机壳。电气DRC通过不代替丝印、方向、装配空间或实物电气验证。Windows安装包未签名，macOS包未公证。

### English

The AI skill now requires complete component body silkscreen, pin-1 and polarity marks, and conflict-free placement. Inventory parts first; resolve clashes by moving or rotating parts and reconnecting copper, then inspect DRC, actual Gerbers and the latest preview. Do not delete or trim outlines to suppress findings. Dimensions and selection patterns remain project data.

This release adds the general 3D renderer and viewer tab, complete outline/orientation checks, placement clearance search, mounting holes, power-neck checks across pads/vias, native record preservation, independent schematic updates, project preview rules and configurable routing budgets.

Each platform passed 375 Rust tests (2 ignored), clean Flutter analysis and 30 widget tests. Final Windows/macOS/Linux packages passed the bundled Demo and actual PCB/schematic/3D window checks. Windows installation matches the ZIP file for file; Linux upgrades from 0.2.1-1 to 0.2.2-1 in an isolated Ubuntu 22.04 container. The dedicated silkscreen case preserves six complete frames, two pin-1 marks and one cathode bar with no errors or warnings; a deliberately crowded layout is detected even without a copper-clearance violation. The legacy Demo retains six existing text-height warnings.

Source and packaged-document commits are recorded above and in build-info.json. Homebrew uses the release's actual CLI SHA256. APT remains at 0.2.1-1; use the release DEB for 0.2.2. Winget's previous 0.2.0 submission still awaits maintainer approval; the new manifest passes schema validation, which does not establish installation or official availability. Models may be approximate, collision checking is not implemented, and the Windows/macOS packages remain unsigned/unnotarized.


## 0.2.1

本版改进通用 PCB 布线整理、检查和预览。板子的线宽、孔径、间距、调长范围等参数继续来自工程或规则文件，不内置特定板卡的坐标和例外。

- 差分出线同时规划芯片端和连接器端，多对布线预留出口；可按网络选择主干所在层。等长补线支持 `tune --layer` 和 `--window` 限定铜层及区域，放不下时报告剩余长度。
- 增加 `widen --uniform` 整网统一线宽、`--bridge-necks` 连续主干改道，并改进短鼓包、重复覆盖线及细颈的处理。受阻时保留原板并报告，不悄悄缩细整网。
- DRC 布线质量检查覆盖偏心过孔、过孔绕行、焊盘避孔、急弯、短鼓包、细颈及受约束网络的自身搭接。部分检查需在 `[drc.quality]` 启用；质量提示与电气 DRC 错误分开报告。
- `escape-vias` 联合重接各层引线；`clean --center-vias` 可在原铜环内补中心引线。移动、推挤和手工布线加强写盘前检查，保护原有焊盘、分支和跨层接点。
- 窗口放大显示网络名，Ctrl + 单击支持多网络高亮；高亮保留实际线宽和钻孔孔口。整网线宽编辑支持一步撤销，修改仍需按项目规则复查并核对最新画面。
- 修复使用 `--page` 打开原理图时，页面列表尚未异步加载完成导致的越界；增加两个窗口回归测试，覆盖指定第 1 页和第 99 页、页面列表尚未到达时的加载状态。
- 设计文件支持贴片焊盘间专用间距和本工程的库封装修孔；共享库保持原样。

完整 Windows 和 macOS ZIP、Linux DEB 带桌面预览；另附 [Linux x64 完整 tar.gz](https://github.com/cc38324/PcbCliTool/releases/download/v0.2.1/easyedatool-0.2.1-linux-x64.tar.gz)，同样包含 CLI、窗口及使用文档。macOS Homebrew / tar.gz 只提供 CLI。winget 官方源尚未确认收录本版，直接下载 [v0.2.1 附件](https://github.com/cc38324/PcbCliTool/releases/tag/v0.2.1)。APT 源已完成发布后核验：公网 `0.2.1-1` 包 SHA256 与发布产物一致，`InRelease` 和 `Release.gpg` 签名、索引哈希均通过；干净 Ubuntu 22.04 环境中 `apt-get update` 成功，候选版本为 `0.2.1-1`，依赖模拟安装可以解析。

### 验证记录

本版分别固定组件来源：`CLI_SOURCE = c573fe9cd0a8c3d4f9fc08ae005766cedba83df7`，`VIEWER_SOURCE = 518c439e681311b72623c9258a58716f75f38d1d`，包内文档来自公开仓库提交 `4219a05`。窗口提交只修改窗口及相关测试、说明，Rust 源码树相同；CLI 沿用已验证的构建，三个平台的窗口按修复后的提交重新构建。窗口 SDK 统一为 Flutter 3.41.9 / Dart 3.11.5，依赖锁文件未变。

| 项目 | 已确认结果 |
|---|---|
| 三平台 Rust release 测试 | Windows、macOS、Linux 均为 332 项通过，2 项忽略 |
| 三平台窗口静态分析及测试 | 均为 `flutter analyze` 0 问题，27 项测试通过 |
| 三平台最终包的简单 Demo | 均核对 13 个引脚、逐脚差异 0；5 个连接全部布通；电气 DRC 违规 0 |
| Windows x64 | 最终安装程序安装后的文件与 ZIP 逐文件一致；PCB 和原理图实际窗口截图已查看，显示正常，日志无 Dart 异常 |
| macOS arm64 | 最终 ZIP 的 Demo 自测通过；实际打开 PCB 和原理图窗口核对正常 |
| Linux x64 | 在 Ubuntu 22.04 / glibc 2.35 容器中，从 `0.2.0-2` 升级到 `0.2.1-1` 后完成同样自测；Xvfb 下 PCB 和原理图窗口正常，只有环境 ATK 提示 |
| Homebrew | macOS Homebrew 7.0.9 使用独立缓存 `brew fetch` 下载 0.2.1，SHA256 匹配；Formula Ruby 语法检查通过；未改动本机已安装版本 |
| GitHub Release 附件 | 全部 8 个公开附件已重新下载，逐个哈希核验通过 |

简单 Demo 的电气检查通过与原有 6 项丝印字高警告分开记录。不能把测试通过或示例布通等同于任意工程已经具备生产条件。

MP157 作为导入与布局复用的复杂参考示例，本次只做 `gen` / `check` 验证：生成得到 238 个器件、210 个网络，`check` 核对 1111 个引脚、网表差异 0 并通过，同时有 14 项布局距离提示。生成时版面自检仍报 10 项重叠，自动 DRC 有大量尚未布线的未连通项。未验证该示例完整布线后的结果；它不是零 DRC 的完成品，也不用于判断安装是否成功。

### English

This release improves general PCB routing cleanup, checks, and the desktop viewer. Board parameters remain in project and rules files.

- Differential routing plans both chip and connector fanout. Length tuning can be restricted to a layer and rectangular region, with remaining length reported when space is insufficient.
- Whole-net width editing, continuous power-track rerouting, and improved cleanup address short bulges, covered segments, and narrow sections without silently shrinking a whole net.
- Routing-quality checks cover off-center vias, via detours, vias near pads, sharp corners, width bulges and necks, and self-overlap on constrained nets. Some checks require configuration; quality findings are reported separately from electrical DRC violations.
- Via relocation, shove routing, and manual copper edits preserve more connection points and validate candidates before writing. Center connections can be added within existing via copper.
- The viewer adds track net labels and Ctrl-click multi-net highlighting using actual copper widths and drill openings. Whole-net width edits support undo.
- Opening a schematic with `--page` no longer indexes a page list before its asynchronous load completes. Two widget regression tests cover the loading state for requested pages 1 and 99 before the list arrives.
- Design files can override SMD pad-to-pad clearance and patch a footprint hole in the project without changing its shared library.

Full Windows/macOS ZIPs, the Linux DEB, and the additional `easyedatool-0.2.1-linux-x64.tar.gz` include the viewer; the macOS Homebrew/tar.gz package is CLI-only. Official winget availability is unconfirmed; use the [Release assets](https://github.com/cc38324/PcbCliTool/releases/tag/v0.2.1). Post-publication APT checks passed: the public `0.2.1-1` package SHA256 matches the release artifact, both `InRelease` and `Release.gpg` signatures verify, and index hashes match. In a clean Ubuntu 22.04 environment, `apt-get update` succeeds, the candidate is `0.2.1-1`, and a simulated installation resolves its dependencies.

The CLI is built from `c573fe9`; the viewer is built from `518c439`; bundled public documentation is from `4219a05`. Their Rust source trees are identical; the later source commit adds only the viewer fix, its tests, and related documentation. All viewer builds use Flutter 3.41.9 / Dart 3.11.5 with the dependency lock unchanged. Each platform has 332 passing Rust tests (2 ignored), clean Flutter analysis, and 27 passing widget tests.

Final packages passed the small Demo check: 13 pins with no netlist differences, all 5 connections routed, and no electrical DRC violations. Six existing silkscreen-height warnings remain separate. Windows installer files match the ZIP file for file; PCB and schematic window captures were inspected and logs contained no Dart exceptions. The final macOS ZIP passed the same Demo and both window checks. The Linux DEB was upgraded from `0.2.0-2` to `0.2.1-1` in an Ubuntu 22.04 / glibc 2.35 container; the same Demo and both windows passed under Xvfb, with only environment ATK notices.

Homebrew 7.0.9 on macOS fetched 0.2.1 using an isolated cache and verified its SHA256; the formula passed Ruby syntax validation. This check did not alter the installed version. All 8 public GitHub Release attachments were downloaded again and their hashes verified individually.

The MP157 example demonstrates import and layout reuse. Only generation and `check` were verified: its 1111-pin net comparison passes with 14 layout-distance notices, while generation reports 10 schematic overlaps and automatic DRC reports open connections on the un-routed board. Complete routing was not validated. Use the small Demo for installation checks; the MP157 reference is not a finished board with zero DRC findings.
