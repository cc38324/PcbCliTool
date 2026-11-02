# 自动拒绝需要重画的布线

间距、短路和连通检查通过后，还要查孔位、连续线宽及供电返回路径。阈值按项目设置。

## DRC与编辑前检查

在 `[drc.quality]` 显式选择阻断类型。默认列表为空，旧工程保留提示行为。
以下仅展示语法，数值和网络范围须按实际板子设定：

```toml
[drc.quality]
blocking_kinds = ["via_offset", "via_detour", "via_placement", "via_pad",
                  "sharp_corner", "width_bulge", "width_neck",
                  "width_neck_contact", "self_crossing"]
via_placement_nets = ["*"]
via_placement_exclude = ["GND", "USB_D*"]
via_placement_min_saving = 1.0
via_offset = 0.05
detour_min = 0.5
detour_ratio = 1.3
lookahead = 5.0
corner_angle = 134.5
corner_cut = 0.2
width_bulge = 3.0
width_neck = 0.127
width_neck_min_length = 0.05
width_neck_through_contacts = true
width_neck_nets = ["+3V3", "+5V", "LED_K"]
```

`blocking_kinds` 接受示例中的九种名称；拼写错误和 `constrained_via_detour` 会拒绝加载。
它只提升已启用检查发现的问题，不自动打开阈值为0的检查。
`enabled=false` 与非空阻断列表冲突；孔位最小收益必须是有限非负毫米数。

运行 `drc <工程> --rules <项目规则> --json <报告>`，省略 `--rules` 时会读取工程
`[checks].rules`，未配置才用通用默认。原始 `routing_quality` 保留所有提示；
严格项另列为 `routing_quality_errors`，计入问题总数，退出码1，终端显示“需重画”。
窗口自动DRC同样计入错误，按网络、层、坐标标记“布线质量需重画”。
`--clearance` 是旧Python对照模式，不执行质量检查，不额外继承工程检查规则，不能用于本门禁验收。

让手动画板同时检查，在工程旁 `easyedatool.toml` 配置：

```toml
[checks]
rules = "项目.route.toml"
```

普通布线、组合布线试算和写回、改线宽、换层、拖线、拖孔及过孔尺寸修改，在写盘前
加载此规则。新增或改变的阻断项拒绝整次编辑，PCB与索引不写入，报告给出具体问题。
旧问题只在所在网络的实际铜几何未变时允许继承，并按完整问题的多重集比较；其他网络
的无关编辑仍可继续。保持问题数量、中心和长度相同但改变几何，也会拒绝。
这不代表旧问题已审核，最后仍须跑全板DRC和项目验收。
普通编辑不直接继承独立 `serve --rules` 参数，须同时配置 `[checks].rules`。

## 绕远过孔

`via_detour` 查局部引线及较短通道，不证明候选满足全板约束。
`via_placement` 枚举有限跨层候选，在内存中检查项目间距、板边、孔/焊盘、工艺、
原焊盘分组及剩余分支，再比较全网有效铜长。`via_placement_min_saving` 是最小节省量；
设0保留旧候选行为，正数过滤收益过小的调整，使用0.001mm原生几何容差。检查不自动应用候选。
差分和等长网络始终跳过跨层移孔；GND平面和外部保护网用排除列表声明。
需删孔对、重排器件或完整重布的绕路可能不在候选内，0条不能证明全局最优。

## 中段突然变细

`width_neck` 查粗线之间的细段，`width_neck_through_contacts=true` 还查可明确追踪的
焊盘、过孔连接。真正分支或歧义接点不能强行合成无分支链。
整条同宽细主干不一定触发细颈检查，应另外按实际源脚和负载核对连续粗铜。
必要密脚短出线须逐项审核，不能用整网豁免、抬高起查值、关闭检查或缩细粗线消警告。
项目若保留人工例外，须绑定精确问题及铜几何，改动后失效；工具不自动批准例外。

## 电源及去耦回流

在 `[[smps.decoupling]]` 指定实际电源脚、服务电容及本板的 `max_distance`、`max_power`、
`max_ground`、`max_area`。最后铺地后运行 `smps --rules ... --json ...`，检查真实供电
铜路、返回芯片地脚的路径及三维回路面积。超限、缺件、断路为失败。
电容与芯片同在3V3网上不能证明它服务了指定引脚。
项目自动验收还须核对JSON完整、绑定正确、数值有限，不能放行缺失数据或标为“ok”的超限值。
这些是指定电源回流的几何检查，不是高速信号参考平面连续性或电磁仿真。

工具开发回归可运行 `python tools/verify_routing_quality_gates.py --tool <新CLI>`。
它只在源码仓库 `out/strict-quality-fixture` 生成测试板，验证原始/严格DRC、项目自动规则、
旧对照模式及宽松参数无法绕过项目编辑约束；不读取或修改生产PCB。
