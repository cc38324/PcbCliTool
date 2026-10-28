# 发布说明 / Release notes

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

Each platform passed 375 Rust tests (2 ignored), clean Flutter analysis and 30 widget tests. Final Windows/macOS/Linux packages passed the bundled Demo and actual PCB/schematic/3D window checks. Windows installation matches the ZIP file for file; Linux upgrades from0.2.1-1 to0.2.2-1 in an isolated Ubuntu22.04 container. The dedicated silkscreen case preserves six complete frames, two pin-1 marks and one cathode bar with no errors or warnings; a deliberately crowded layout is detected even without a copper-clearance violation. The legacy Demo retains six existing text-height warnings.

Source and packaged-document commits are recorded above and in build-info.json. Homebrew uses the release's actual CLI SHA256. APT remains at0.2.1-1; use the release DEB for0.2.2. Winget's previous0.2.0 submission still awaits maintainer approval; the new manifest passes schema validation, which does not establish installation or official availability. Models may be approximate, collision checking is not implemented, and the Windows/macOS packages remain unsigned/unnotarized.


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
