# 发布说明 / Release notes

## 0.2.1

本版改进通用 PCB 布线整理、检查和预览。板子的线宽、孔径、间距、调长范围等参数继续来自工程或规则文件，不内置特定板卡的坐标和例外。

- 差分出线同时规划芯片端和连接器端，多对布线预留出口；可按网络选择主干所在层。等长补线支持 `tune --layer` 和 `--window` 限定铜层及区域，放不下时报告剩余长度。
- 增加 `widen --uniform` 整网统一线宽、`--bridge-necks` 连续主干改道，并改进短鼓包、重复覆盖线及细颈的处理。受阻时保留原板并报告，不悄悄缩细整网。
- DRC 布线质量检查覆盖偏心过孔、过孔绕行、焊盘避孔、急弯、短鼓包、细颈及受约束网络的自身搭接。部分检查需在 `[drc.quality]` 启用；质量提示与电气 DRC 错误分开报告。
- `escape-vias` 联合重接各层引线；`clean --center-vias` 可在原铜环内补中心引线。移动、推挤和手工布线加强写盘前检查，保护原有焊盘、分支和跨层接点。
- 窗口放大显示网络名，Ctrl + 单击支持多网络高亮；高亮保留实际线宽和钻孔孔口。整网线宽编辑支持一步撤销，修改仍需按项目规则复查并核对最新画面。
- 修复使用 `--page` 打开原理图时，页面列表尚未异步加载完成导致的越界；增加两个窗口回归测试，覆盖指定第 1 页和第 99 页、页面列表尚未到达时的加载状态。
- 设计文件支持贴片焊盘间专用间距和本工程的库封装修孔；共享库保持原样。

完整 Windows 和 macOS ZIP、Linux DEB 带桌面预览；另附 [Linux x64 完整 tar.gz](https://github.com/cc38324/PcbCliTool/releases/download/v0.2.1/easyedatool-0.2.1-linux-x64.tar.gz)，同样包含 CLI、窗口及使用文档。macOS Homebrew / tar.gz 只提供 CLI。winget 官方源尚未确认收录本版，直接下载 [v0.2.1 附件](https://github.com/cc38324/PcbCliTool/releases/tag/v0.2.1)。APT 源的本版发布状态仍须在发布后单独验证，不属于下面的安装包验证结果。

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

Full Windows/macOS ZIPs, the Linux DEB, and the additional `easyedatool-0.2.1-linux-x64.tar.gz` include the viewer; the macOS Homebrew/tar.gz package is CLI-only. Official winget availability is unconfirmed; use the [Release assets](https://github.com/cc38324/PcbCliTool/releases/tag/v0.2.1). Availability of this version through APT still requires separate verification after publication.

The CLI is built from `c573fe9`; the viewer is built from `518c439`; bundled public documentation is from `4219a05`. Their Rust source trees are identical; the later source commit adds only the viewer fix, its tests, and related documentation. All viewer builds use Flutter 3.41.9 / Dart 3.11.5 with the dependency lock unchanged. Each platform has 332 passing Rust tests (2 ignored), clean Flutter analysis, and 27 passing widget tests.

Final packages passed the small Demo check: 13 pins with no netlist differences, all 5 connections routed, and no electrical DRC violations. Six existing silkscreen-height warnings remain separate. Windows installer files match the ZIP file for file; PCB and schematic window captures were inspected and logs contained no Dart exceptions. The final macOS ZIP passed the same Demo and both window checks. The Linux DEB was upgraded from `0.2.0-2` to `0.2.1-1` in an Ubuntu 22.04 / glibc 2.35 container; the same Demo and both windows passed under Xvfb, with only environment ATK notices.

The MP157 example demonstrates import and layout reuse. Only generation and `check` were verified: its 1111-pin net comparison passes with 14 layout-distance notices, while generation reports 10 schematic overlaps and automatic DRC reports open connections on the un-routed board. Complete routing was not validated. Use the small Demo for installation checks; the MP157 reference is not a finished board with zero DRC findings.
