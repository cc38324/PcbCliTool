# STM32MP157 AMOLED 与触摸示例

100×80 mm 四层板，保留 ST AN5122 的 MPU、DDR3L、eMMC、STPMIC1 核心布局。外围包括以太网、Wi-Fi / 蓝牙、USB、CAN、RS485、GPIO，以及用户选定的 **AM319M262928ZS 3.19 英寸 262×928 AMOLED + CST3530 触摸**。

显示使用 MP157 的 **1-lane MIPI DSI**，J6 为用户指定的 **DF40C-30DS-0.4V(51)，C424642**，显示与触摸共用一个 30 针连接器。AMOLED 自发光，不使用原草稿的 MP3202 LED 背光电路。

[原始屏幕 PDF、逐脚接法、1 脚方向、电源及驱动说明](docs/display/README.md)。主板顶视 J6 的 **1 脚在右下角、接地**，板上有方向圆点；屏图的背视图不能直接当成主板顶视图。

提供独立控制的 3.7V VBAT、1.8V IO、2.8V 触摸电源，以及用于 VCI_EN 的受控 3.3V 输出。I²C、触摸中断、TE、显示与触摸复位均按屏端 1.8V 信号处理，通过电平转换接 MP157 的 3.3V GPIO。TCA9538 在主机 I2C2 上控制电源时序，上电默认关闭并保持复位。

工程由 `mp157demo.toml` 直接生成；旁边的 panel / placement / silk 文件保存逐脚接法与布局来源。原生布局文件 `mp157demo.layout.toml` 保存已完成的走线、过孔与铺铜，必须一同保留。本地 `lib/` 提供所有元件，不修改共享元件库。

```powershell
python build_mp157.py --tool <easyedatool.exe路径> --out project/MP157Demo --export
easyedatool view project/MP157Demo
```

`build_mp157.py` 恢复原理图和 PCB、差分约束及标注，执行网表核对、ERC、显示接口专项检查与 DRC；`--export` 在检查通过后导出 PDF、BOM、网表、效果图与 Gerber / 钻孔 / 坐标。显示专项检查还会核对原始 PDF 的 SHA-256、30 个引脚、1 脚坐标，以及计入 LFBGA354 封装内部长度差后的 MIPI 配对长度。工具须支持 `body_silk.pin1.at`。

修改设计文件后使用原生 `gen`，重新接线并复查；仅恢复完成版时运行上述构建脚本即可。已保存的布局让生成过程无需重新下载 ST 参考设计。

按用户要求保留 ST 密集核心的常规丝印，外围采用完整外框。工艺警告和布线质量提示保留在 `project/MP157Demo/output/MP157Demo_drc.json`，不能等同于实物验证结果。

本例是硬件设计，尚未进行实物点屏。软件仍须适配 CO6300 初始化、CST3530 驱动、触摸坐标和模组上下电时序；MP157 接口支持这块一线屏，不代表通用屏驱动可以直接点亮它。
