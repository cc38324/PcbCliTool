# FPC生产资料

FPC的物理叠层、补强区域和下单参数分别保存不同的信息。物理叠层供厚度、显示及阻抗计算读取；原生FPC类型由58/59补强层的启用状态表示；补强材质、厚度和区域通过 `FPC_FILL`、补强Gerber及 `jlcpcb.json` 传给工厂。

## 操作步骤

1. 按工厂及连接器资料确认铜/PI/覆盖膜叠层、金手指局部总厚及实际补强材质。设计中设置 `board.fpc = true`，需要记录物理叠层时填写 `board.stackup_layers`，局部补强填写 `board.stiffeners`；格式见 [设计格式](design-format.md#fpc类型与局部补强)。
2. `easyedatool gen 设计.toml --out 工程`。重复生成应得到相同文件；原生补强记录的厚度是毫米，外形坐标是mil，不能将两者按相同倍率缩放。
3. 按正常流程布线、补长、铺铜，跑工程实际规则的 `drc`。板边触点确需0.20mm时才设置设计字段 `rules.smd_pad_to_edge`，其余铜到板边不放宽。逐芯独立排线每芯用唯一网络名；即使两芯都叫地或电源，也不能按功能合并或跨芯铺铜。
4. `easyedatool render 工程 --view layers --layer 58,59 -o 补强.png` 查看补强区域和面别，再看顶/底面触点开窗。58是PCB顶面，59是底面；导出坐标保持同一坐标系，不把底面几何预先镜像。
5. `easyedatool fab 工程 --files -o 生产文件`。有补强时成功输出「FPC补强：N 个区域，jlcpcb.json 和分材质/面别的补强 Gerber 已加入压缩包」。确认区域数正确，且每个 `jlcpcb.json` 条目的 `gerber` 文件实际存在于zip。再次核对材料、厚度、形状及正反面，不把3D薄膜本体当作补强/连接器完整装配模型。
6. 上传 `Gerber_工程名.zip` 到嘉立创，下单选择FPC并核对平台解析出的补强及工艺要求。优惠金额由平台的实际识别、活动和订单条件确定，不能仅根据文件扩展名承诺减免金额。

## 文件对应

| 材料 | 顶面文件示例 | 底面对应 | jlcpcb.json材料 |
|---|---|---|---|
| PI，0.20mm | `Gerber_TopStiffenerLayer_pit_0.2.GTSL` | `BottomStiffenerLayer_pib_0.2.GBSL` | `pi` |
| FR4，0.40mm | `Gerber_TopStiffenerLayer_fr4t_0.4.GTSL` | `BottomStiffenerLayer_fr4b_0.4.GBSL` | `fr4` |
| 钢片，0.10mm | `Gerber_TopStiffenerLayer_gpt_0.1.GTSL` | `BottomStiffenerLayer_gpb_0.1.GBSL` | `steel` |
| 3M9077胶 | `Gerber_TopStiffenerLayer_pst_3m9077.GTSL` | `BottomStiffenerLayer_psb_3m9077.GBSL` | `tape`，另有 `model` |
| 电磁膜，0.018mm | `Gerber_TopStiffenerLayer_csa_0.018.GTSL` | `BottomStiffenerLayer_ssa_0.018.GBSL` | `EMI Shielding Film` |

底面对应列省略了相同的 `Gerber_` 前缀。一个生产Gerber可含多个同材质、面别及规格的区域，manifest逐区记录，并用 `gerber` 字段关联。`path` 按嘉立创格式保留形状命令及mil坐标；`thickness` 是毫米字符串。胶文件按型号分，型号不能用厚度替代。没有补强区域时不生成空的 `jlcpcb.json`。

## 依据和验证

- [嘉立创EDA图层管理器](https://prodocs.lceda.cn/cn/pcb/tools-layer-manager/)：FPC类型开放补强层；物理叠层不影响Gerber，下单仍要选择实际叠层参数。
- [嘉立创FPC设计帮助](https://m.jlc.com/portal/server_guide_40115.html)：补强材料、厚度和区域会随Gerber输出供下单处理。
- [嘉立创FPC参数介绍](https://wiki.lceda.cn/zh-hans/design-production/pcb-design/fpc-parameter-introduction.html)：金手指局部厚度应按铜、覆盖膜和补强的实际覆盖情况计算。

2026-11-02已用嘉立创4.1.69实际启用FPC、保存并导出测试板，核对14个区域、10个补强生产层，覆盖两面、同材质多个区域、内洞、圆及多边形。原生区域、manifest材料/厚度/形状与补强Gerber均完成对照；普通板不增加补强文件。

PyGerber 2.4.3会漏画嘉立创补强文件中未结束的 `SRX1Y1I0.0J0.0` 区域。复查脚本只在光栅比较副本里去掉该1×1、零位移声明，保留客户端原始Gerber和zip，不改多实例拼板。[Gerber规范](https://www.ucamco.com/files/downloads/file_en/451/gerber-layer-format-specification-revision-2021-11_en.pdf)中每轴重复次数为1时只有原位一个实例，因此这一步不改变生产图形。
