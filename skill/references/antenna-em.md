# 天线三维全波仿真

窄馈线须先用已知阻抗和负载的传输线模型校核。`mesh.feed_cell_mm` 默认 `0.024` mm，对辐射网络在端口层的长直物理边采用三分网格：局部尺寸的 2/3 在金属内、1/3 在金属外，避免网格恰好落在 PEC 边上造成阻抗偏差。导出的 `feed_edges` 来自实际铜形的外轮廓和孔边，不含分解铜皮的内部边。端口横向范围须放在馈线铜内部，不能与窄线两边重合；例如 0.136 mm 馈线可从 0.04 mm 端口宽度起步，仍须校核。`min_cell_mm` 仅控制均匀网格到已有锚点的避让；边缘网格可以更细。对比网格时同时减小 `feed_cell_mm`，只减小大区域的 `cell_mm` 不足以确认馈线收敛。所有匹配结论以端口校核、时间及网格收敛为前提。

`em` 从原生 PCB 读取实际铜、铺铜填充、钻孔、孔壁及物理叠层，调用外部 openEMS。它与 `impedance` 二维传输线阻抗计算不同。窗口入口「检查 → 天线电磁仿真…」，选择 TOML/JSON 配置，结果在工程 `output/em`。省略 `--run` 仅导出，不能称为仿真成功。

## 环境和运行

使用 [openEMS 官方发行包](https://github.com/thliebig/openEMS-Project/releases)，安装与 Python 主次版本匹配的 openEMS/CSXCAD wheel，以及 numpy、h5py、matplotlib。[官方安装说明](https://docs.openems.de/en/latest/install/python.html)。可用项目内便携 Python，无须改变系统 Python。Windows `solver_root` 指向包含 `CSXCAD.dll` 的目录。

配置填写 `python`、`solver_root`，或 CLI `--python`、`--solver-root` 覆盖。Python 还可设置环境变量 `EASYEDATOOL_EM_PYTHON`。含目录的相对路径以配置文件为基准，单独 `python` 命令从 PATH 查找。

```powershell
easyedatool em <工程> --config <工程>/antenna.toml -o <工程>/output/em
easyedatool em <工程> --config <工程>/antenna.toml -o <工程>/output/em --run
```

`cargo run --release --example antenna_coupon -- <尚不存在的目录>` 生成 30×20 mm 四层原生测试板及配置，顶部 7 mm 为天线净空。可追加横半轴、纵半轴、地平面边缘 y 三个毫米参数。它是起始几何，不是已验证的 QM35825 参考天线。

发行包已附`examples/antenna_coupon`原生工程，无需源码或Rust即可验证导出流程。先把示例复制到自己的工作目录，运行`em examples/antenna_coupon --config examples/antenna_coupon/antenna.toml -o output/antenna-em`；追加`--run`才会使用外部求解器。默认端口的X/Y横向边界均位于馈线铜内部；修改端口宽度、长度或位置后须重新导出检查，不能让边界贴着金属边缘。

## 配置

完整示例见 `examples/antenna.toml`；几何毫米、频率 GHz、端口欧姆。

| 字段 | 含义 |
|---|---|
| `material_note` | 必填，写明叠层/材料来源和假定值，不能将普通 FR-4 名称视为已知高频参数 |
| `loss_tangent` | 必填，叠层未给损耗时采用；0 是无损假设 |
| `conductor_model` | 默认 `sheet`，铜中心薄片近似。`top_volume_pec` 用实际厚度的顶铜 PEC 体，内层/底铜在上表面放 PEC 薄片，内部介质等效延伸；端口和第一介质按铜的介质侧表面定位，适合薄介质顶层射频验证。该模式未计铜损，不能把效率当成实测值 |
| `omit_solder_mask` | 默认 false；叠层含阻焊/丝印厚度时，须显式 true 才允许忽略，并在材料说明中记录此近似 |
| `frequency_ghz`、`samples` | 默认 4–10 GHz、601 点 |
| `far_field_ghz` | 默认空数组，仅算端口；示例指定通道 5/9 中心 6.4896/7.9872 GHz |
| `[[bands]]` | 可配置多个 `name`、`frequency_ghz=[低,高]`、`max_s11_db`；示例给通道 5/9 全带 −10 dB 目标。未配置时报告匹配目标为 null，不能称匹配通过 |
| `antenna_keepout` | `[x0,y0,x1,y1]`；只允许端口网络在信号层的辐射铜，其余铜和钻孔禁止进入 |
| `[port]` | `net`、`ground_net`、`xy`、`signal_layer`、`ground_layer`、`width_mm`、`length_mm`、`resistance_ohm`；当前支持由下方地层到上方信号层的垂直单集总端口，两端中心须在实际铜内 |
| `[mesh]` | `cell_mm`、`min_cell_mm`、`air_mm`、`steps`、`end_db`、`threads`、`max_cells`；控制网格和迭代，需另做网格加密对照 |
| `[[environment]]` | 可选外部近似结构：`name`、`kind="pec"/"dielectric"/"air"`、`start_mm`/`stop_mm` 三维坐标、`epsilon`、`loss_tangent`、`priority`。PEC 可为零厚度平面，介质/空气须为体积；不允许底板/金属进入天线净空。须在材料说明中注明载板、插针、焊接高度等近似来源，不能冒充客户实际底板模型 |

叠层须给出铜厚、介质厚和介电常数。当前支持一个连续板框，铜层间一个介质层。多板框/板框内孔槽、铜层文字、未转为实心铜的铜层图线、未知实体材料层均报错。盲埋孔按跨度建模，未使用内层焊盘不补铜。

## 成功判据

- 只导出：出现「电磁模型已导出」「尚未求解」，检查 `em-model.json`；不需要 openEMS。
- 真求解：进程退出码 0，出现「电磁求解完成」，`em-report.json` 的 `status=completed`，PCB 与模型 SHA256 对应本次输入。失败看 `em-solver.log`。计算期间 PCB 改变会拒绝将旧结果当作当前结果。
- 「配置频带的 S11 匹配目标：未通过」表示流程完成但匹配未达目标，不能称设计合格。报告 `matching_target_met` 单独记录此判据，未配置为 null；各频带的 `passes_target` 给出逐项结果。
- 每次创建新 `fdtd-*` 目录，保存模型快照、几何 XML、全层铜 PNG、S11/复数阻抗 CSV、S1P、S11 图和远场 CSV/图。根目录报告指向最后一次完整结果；失败保留日志和旧报告，须核对哈希，不能凭旧图报告成功。并发计算用不同输出目录。
- 默认 `mesh_convergence_verified=false`；须加密网格比较频带内复数 S11、谐振频率和效率，记录差异后才能称网格收敛。达到最大迭代数也不能直接称能量衰减已达标。
- `conductor_geometry_resolved=true` 表示所有导体均被网格解析；`time_convergence.verified=true` 表示从本次求解日志确认达到了指定能量衰减。两者与网格收敛各自独立。
- 集总端口在横向两个方向保持单个 Yee 网格单元，避免网格细化时端口离散方式改变。报告 `port_transverse_cells=[1,1]`；仍需验证馈线截面与参考面的物理取法。
- 带孔铜形分解为三角形时，按原连通铜岛检查是否被解析；`unused_mesh_fragments` 记录未解析的小片，不能把网格精度不足隐去。最终仍须加密并核对 S11；所有连通铜岛和外部导体都未解析的模型会失败。

铜为有限电导薄片，镀通孔以钻孔半径外加 20 µm 的实心 PEC 导柱近似，不求解孔内场；非镀通孔切除铜和介质。介质延伸到铜层中心。未被网格解析的铜/导柱会拒绝成功报告。阻焊、表面处理、封装、焊点、实际底板和外壳尚未加入；假设写入报告。核心板天线受邮票口底板地/外壳影响，最终需补装机条件及实物 VNA/辐射测试，不能将测试板结果当成成品指标。
