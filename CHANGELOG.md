# 发布说明 / Release notes

## 0.2.1

本版改进通用 PCB 布线整理、检查和预览。板子的线宽、孔径、间距、调长范围等参数继续来自工程或规则文件，不内置特定板卡的坐标和例外。

- 差分出线同时规划芯片端和连接器端，多对布线预留出口；可按网络选择主干所在层。等长补线支持 `tune --layer` 和 `--window` 限定铜层及区域，放不下时报告剩余长度。
- 增加 `widen --uniform` 整网统一线宽、`--bridge-necks` 连续主干改道，并改进短鼓包、重复覆盖线及细颈的处理。受阻时保留原板并报告，不悄悄缩细整网。
- DRC 布线质量检查覆盖偏心过孔、过孔绕行、焊盘避孔、急弯、短鼓包、细颈及受约束网络的自身搭接。部分检查需在 `[drc.quality]` 启用；质量提示与电气 DRC 错误分开报告。
- `escape-vias` 联合重接各层引线；`clean --center-vias` 可在原铜环内补中心引线。移动、推挤和手工布线加强写盘前检查，保护原有焊盘、分支和跨层接点。
- 窗口放大显示网络名，Ctrl + 单击支持多网络高亮；高亮保留实际线宽和钻孔孔口。整网线宽编辑支持一步撤销，修改仍需按项目规则复查并核对最新画面。
- 设计文件支持贴片焊盘间专用间距和本工程的库封装修孔；共享库保持原样。

完整 Windows 和 macOS ZIP、Linux DEB 带桌面预览；macOS Homebrew / tar.gz 只提供 CLI。winget 官方源尚未确认收录本版，直接下载 [v0.2.1 附件](https://github.com/cc38324/PcbCliTool/releases/tag/v0.2.1)。APT 的候选版本须单独检查。

### 验证记录

本次发布构建的测试、打包自测和平台启动核对完成后，在这里记录实际结果。较早构建的通过数量不作为 0.2.1 成品验证结果。

### English

This release improves general PCB routing cleanup, checks, and the desktop viewer. Board parameters remain in project and rules files.

- Differential routing plans both chip and connector fanout. Length tuning can be restricted to a layer and rectangular region, with remaining length reported when space is insufficient.
- Whole-net width editing, continuous power-track rerouting, and improved cleanup address short bulges, covered segments, and narrow sections without silently shrinking a whole net.
- Routing-quality checks cover off-center vias, via detours, vias near pads, sharp corners, width bulges and necks, and self-overlap on constrained nets. Some checks require configuration; quality findings are reported separately from electrical DRC violations.
- Via relocation, shove routing, and manual copper edits preserve more connection points and validate candidates before writing. Center connections can be added within existing via copper.
- The viewer adds track net labels and Ctrl-click multi-net highlighting using actual copper widths and drill openings. Whole-net width edits support undo.
- Design files can override SMD pad-to-pad clearance and patch a footprint hole in the project without changing its shared library.

Full Windows/macOS ZIPs and the Linux DEB include the viewer; the macOS Homebrew/tar.gz package is CLI-only. Official winget availability is unconfirmed; use the [Release assets](https://github.com/cc38324/PcbCliTool/releases/tag/v0.2.1). Platform validation results will be recorded above after the release builds have been checked.
