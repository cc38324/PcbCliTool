# STM32MP157 AMOLED 与触摸示例

100×80 mm 四层板，保留 ST AN5122 的 MPU、DDR3L、eMMC、STPMIC1 核心布局。外围包括以太网、Wi-Fi / 蓝牙、USB、CAN、RS485、GPIO，以及用户选定的 **AM319M262928ZS 3.19 英寸 262×928 AMOLED + CST3530 触摸**。

显示使用 MP157 的 **1-lane MIPI DSI**，J6 为用户指定的 **DF40C-30DS-0.4V(51)，C424642**，显示与触摸共用一个 30 针连接器。AMOLED 自发光，不使用原草稿的 MP3202 LED 背光电路。

[原始屏幕 PDF、逐脚接法、1 脚方向、电源及驱动说明](docs/display/README.md)。主板顶视 J6 的 **1 脚在右下角、接地**，板上有方向圆点；屏图的背视图不能直接当成主板顶视图。

提供独立控制的 3.7V VBAT、1.8V IO、2.8V 触摸电源，以及用于 VCI_EN 的受控 3.3V 输出。I²C、触摸中断、TE、显示与触摸复位均按屏端 1.8V 信号处理，通过电平转换接 MP157 的 3.3V GPIO。TCA9538 在主机 I2C2 上控制电源时序，上电默认关闭并保持复位。

显示和触摸供电芯片 U18、U16、U17、U28 集中在 J6 附近的底面，L102 位于连接器下方。U18 到电感的开关主干为 0.6 mm；全板电源按完整路径加粗，细间距焊盘保留必要的末端出线。规则覆盖 34 个电源网络，跨焊盘和过孔检查粗线之间的细颈；不得靠缩细原有粗线消除“小蛮腰”。

按用户确认保留 eMMC **U5.N2** 的必要 BGA 短出线：约 **0.09 mm 宽、0.50 mm 长**。ST 参考封装球距 0.5 mm，邻近 P2 / P3 的焊盘为 0.23 mm，扣除两侧各 0.09 mm 间距后，只剩约 0.09 mm。维持原四层工艺，无需 HDI。原先另一处细线所在的 R40 上拉电源已改为 0.3 mm 绕行。此例外必须按引脚、位置、长度和宽度逐项人工核对，其余中段细颈必须为 0；检查从 **0.1 mm 起查**，不能抬高起查值漏掉 0.2 / 0.3 mm 分支。

工程由 `mp157demo.toml` 直接生成；旁边的 panel / placement / silk 文件保存逐脚接法与布局来源。原生布局文件 `mp157demo.layout.toml` 保存已完成的走线、过孔与铺铜，必须一同保留。本地 `lib/` 提供所有元件，不修改共享元件库。

公开包从0.2.7起只附设计数据，使用下列原生命令恢复完成版，不附Python构建或专项检查源码。命令中的路径相对包根目录，`easyedatool` 指包内程序；输出应放新的工程目录。

```text
easyedatool --no-drc gen examples/mp157demo.toml --out MP157Demo
easyedatool --no-drc constraints MP157Demo --from examples/mp157demo.constraints.toml --write
easyedatool --no-drc label MP157Demo --from examples/mp157demo.labels.toml --write
easyedatool layout MP157Demo --save
easyedatool check MP157Demo --rules examples/mp157demo.rules.toml
easyedatool erc MP157Demo --json MP157Demo/output/erc.json
easyedatool constraints MP157Demo
easyedatool drc MP157Demo --rules examples/mp157demo.rules.toml --json MP157Demo/output/drc.json
```

`gen` 恢复已保存的布局、走线和铺铜。修改设计后须重做电气核对，不能重新下载参考设计覆盖当前布局。命令全通过以后，分别运行 `pdf`、`bom`、`netlist`、`render --view top`、`fab --files` 导出对应资料。

以上通用命令不替代显示与供电专项验收：逐项核对原始屏幕PDF的SHA256、30针接法、1脚坐标、计入LFBGA354封装内部长度差的MIPI配对长度、显示电源器件位置，以及唯一获准的U5.N2短出线。记录实际执行的项目，不能把未附带的专项自动检查宣称为通过。工艺警告和质量提示仍按DRC JSON逐项处理。

按用户要求保留 ST 密集核心的常规丝印，外围采用完整外框。工艺警告和布线质量提示保留在 `project/MP157Demo/output/MP157Demo_drc.json`，不能等同于实物验证结果。

本例是硬件设计，尚未进行实物点屏。软件仍须适配 CO6300 初始化、CST3530 驱动、触摸坐标和模组上下电时序；MP157 接口支持这块一线屏，不代表通用屏驱动可以直接点亮它。
