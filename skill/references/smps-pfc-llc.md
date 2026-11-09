# PFC Boost 与半桥 LLC 专项检查（0.3.0）

本说明对应0.3.0 提供的 `profile` / `required_profiles`，旧的0.2.7发行包不认识这些字段；先检查当前二进制 `smps --help` 是否说明专项规则。软件按实际PCB焊盘和铜连接检查，不能替代PF、THD、ZVS、磁件及壳内温升的仿真/实测。

## 必须覆盖指定功率级

```toml
[smps]
required_profiles = ["pfc_boost", "llc_half_bridge"]
```

每一级使用 `[[smps.converter]]`，在其 `profile.kind` 明确选择专项类型。只写 `topology = "LLC"` / `"PFC"` 不算专项配置，会失败。缺少必查级、器件、实际焊盘、铜路径或超限，命令退出1；没有识别/配置电源也不能判为通过。仅明确要求去耦检查的项目可没有转换级。

省略 `--rules` 时先读工程旁 `easyedatool.toml` 的 `[checks].rules`；不能因为没传参数而跳过项目要求。

## profile字段

`profile` 是一个表，可写成 `[smps.converter.profile]`。必填：`kind`、`source`、`pins`、`drives`、`sensing`；LLC还须 `resonance`。`source` 记录实际参考电路版本，全部引脚写实际 `位号.脚号`。不凭丝印号猜IC引脚。

| kind | pins必填角色 |
|---|---|
| `pfc_boost` | `inductor_in`、`inductor_sw`、`switch_drain`、`switch_source`、`switch_gate`、`diode_anode`、`diode_cathode`、`bus_positive`、`bus_negative`、`feedback`、`sense` |
| `llc_half_bridge` | `bus_positive`、`bus_negative`、`high_drain`、`high_source`、`high_gate`、`low_drain`、`low_source`、`low_gate`、`lr_in`、`lr_out`、`primary_in`、`primary_out`、`cr_in`、`cr_out`、`secondary_a`、`secondary_ct`、`secondary_b`、`sr_a_drain`、`sr_a_source`、`sr_b_drain`、`sr_b_source`、`output_positive`、`output_negative`、`feedback`、`sense` |

PFC检查Boost连接并自动生成换流回路，低侧检流器件串在回流中时纳入回路。LLC检查半桥→Lr→变压器→Cr→母线负端的串联连接，自动生成半桥换流、谐振、中心抽头次级A/B四个回路。当前LLC配置面向中心抽头双同步整流、独立Lr、Cr返回母线负端的结构；不能套到其它整流/谐振结构后宣称已覆盖。母线电容和输出电容须绑定真实服务器件，不由同网其它电容替代。

必须按厂家依据在converter的 `loop_warn` / `loop_max` 设置面积上限，单位mm²；自动生成的回路仍沿实际铜量三维面积、绕行和连通。默认25/50不是300W电源的通用验收限值。

## drives：每颗初级功率开关的驱动及返回

`profile.drives` 为表数组，PFC必须覆盖开关门极及源极，LLC必须分别覆盖高、低侧。字段：

```toml
[[smps.converter.profile.drives]]
driver = "U_DRV.1"
gate = "Q1.3"
source = "Q1.2"
kelvin_source = "Q1.4"     # 可选；仅限厂家定义的同器件独立Kelvin源极，脚号按实际器件改
return_pin = "U_DRV.2"
resistor = "RG1"           # 可省略，省略要求驱动脚与gate直接同网
max_length = 8.0           # 示意值，须按本板依据重设；驱动含串联R长度+返回，mm
max_area = 12.0            # 示意值，闭合驱动回路mm²
drive_min = 0.0            # 声明的驱动电压下/上界，V
drive_max = 5.0
allowed_min = -1.0         # 示意值，须取确切GaN/集成驱动器的允许工作范围
allowed_max = 6.0
source_document = "确切器件数据手册版本和设计依据"
```

长度、面积、电压为项目输入，不是通用GaN建议。串联路径支持一颗明确电阻；返回须沿实际铜到绑定源极。不能用普通硅MOS驱动的电压直接当作GaN允许电压。驱动范围比较只检查声明参数，真实过冲、负压、死区和ZVS仍待波形验证。

四端功率器件用 `source` 绑定承载功率电流的源极，`kelvin_source` 另外绑定厂家定义的Kelvin返回焊盘（如 ISG6123TA：功率源极1至6号，可绑定1号；Kelvin为7号）。工具要求两个实际焊盘属于同一器件、同一源极网络，随后从Kelvin脚量到 `return_pin` 的实际铜路，门极回路面积也使用Kelvin点。断开Kelvin返回时必须失败，不能借另一条已接通的功率源极铜路通过。省略此字段保留原先返回到 `source` 的行为。此项不推断芯片内部引线或共阻抗，需要依据完整手册确认功能，并另审功率电流是否侵入Kelvin支路。

## sensing：采样支路与参考返回

```toml
[[smps.converter.profile.sensing]]
pin = "U_CTRL.2"
pickup = "RS1.1"
return_pin = "U_CTRL.3"
return_pickup = "RS1.2"
resistor = "RF1"           # 可省略；支持一颗串联采样滤波电阻
max_length = 6.0           # 示意值，实际采样铜路/滤波R长度上限mm
max_return = 6.0           # 示意值，参考返回铜长上限mm
```

控制器的 `pins.sense` 必须确有对应绑定，pickup/return_pickup须为同一实际检流/采样器件的不同焊盘。检查精确引脚、连通与长度，尚不计算共阻抗耦合和噪声；不可单凭它宣称Kelvin路径无噪声。反馈和检流脚的网络自动加入安静网络检查。

## resonance：LLC参数与BOM一致性

```toml
[smps.converter.profile.resonance]
lr = 0.000020             # H，示意值
cr = 0.000000033          # F，示意值
lm = 0.000120             # H，示意值，依据磁件规格
f_min = 100000.0          # Hz，本项目分析/目标工作范围；是否由硬件保证须另记依据
f_max = 350000.0
f_nominal = 200000.0
fr_min = 180000.0         # Hz，本项目计算允许的fr范围
fr_max = 220000.0
lm_lr_min = 3.0           # 本项目磁件设计允许的Lm/Lr范围
lm_lr_max = 10.0
source = "磁件计算书/绕制规格及控制器配置版本"
```

程序核对PCB器件的Lr/Cr标称值，计算 `fr=1/(2π√(Lr·Cr))`、`fm=1/(2π√((Lr+Lm)·Cr))`，并比较项目给定的fr、Lm/Lr及标称工作频率范围。它不把固定的Lm/Lr或必须跨fr当作所有LLC的通用要求，也不计算变比、增益曲线或ZVS边界。

自适应LLC控制器未提供外部频率限位设置时，不把这里填的 `f_min/f_max` 当作已经实现的硬件限频；软启动、轻载、瞬态和保护频率仍须另行核对。

## 验收

运行 `smps <工程> --rules 规则.toml --json 报告.json --png 回路.png`。检查JSON的 `coverage`、每一级 `profile.checks` 和自动生成的 `loops`，不能只看退出码。正例通过后，在副本或独立规则副本中删去LLC级、填不存在的实际焊盘、拆掉门极铜、把驱动电压改到允许范围外、改错Cr值，各项必须退出1并给出对应问题，再用原始输入复查。普通DRC、thermal、全层Gerber复查继续单独执行。
