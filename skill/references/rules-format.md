# 规则文件（`route`、`drc`、`check` 的 `--rules`）

一个 TOML 文件三个命令共用。毫米。**写错字段名会报错**。例子：`examples/mp157demo.rules.toml`（STM32MP157 这块板）；隔离区、禁布、预布线这些字段下面逐个说明。差分对的例子是 `examples/mp157demo.constraints.toml`。

通用参数都有默认值，一般只写 `[nets]`、禁布区、隔离区。

## 布线层（多层板）

```toml
layers = ["top", "inner2", "bottom"]   # 可选：在这几层上布线（top / bottom / inner1 …）
```

不写时：两层板布顶 / 底两层；多层板布顶层、底层和没被铺铜盖住一半以上的内层——盖住一半以上的内层当铺铜平面，只让过孔穿过（地、电源的焊盘打过孔下去就接上了，所以平面的网络要写进 `[nets] pour`）。过孔都是通孔。

## `[nets]` 网络分类（最重要）

```toml
[nets]
pour = ["GND"]                 # 铺铜网络：焊盘只出一小段线接过孔到铺铜，不走长线
power = ["VIN", "+3V3"]        # 电源：用粗线（power_track，默认 0.5）
priority = ["SPI_MOSI"]        # 长信号：尽量一层走完、离别的焊盘远一点
first = ["ETH_INT"]            # 最先布，按这个顺序（布不通时把关键网络放这里）
keep = ["USB_DP", "USB_DN"]    # 板上已有的这些网络的走线和过孔原样保留（先用 pair --ends 布好的差分段），只补没连上的
```

`keep` 的名字可以用 `*` `?`；`keep = ["*"]` 板上已有的铜全留（gen 的 `[[reuse]]` 照参考板抄来的走线、BGA 扇出过孔就这样留下，过孔保持自己的尺寸），只布还没连上的连接，保留的铜已经连到铺铜的焊盘不再另打地过孔。

铺铜网络要和设计文件里 `[[pours]]` 的网络一致。

## 禁布、区域

```toml
[[keepout]]                    # 任何铜都不能进（和设计文件里的禁布区同一块，布线器只看这里）
name = "ANT"
rect = [0.0, 35.0, 6.5, 55.0]  # [x0, y0, x1, y1]
track_margin = 0.3             # 可选：走线中心再让开这么多（默认 0）
via_margin = 0.35              # 可选：过孔再让开这么多
no_pour = true                 # 可选：布线器模拟铺铜时这里不铺（默认 true）

[[no_tracks]]                  # 这些层在这里不走线（过孔照样穿、铺铜照样铺）：整层地只在一条通道里让给信号
layers = ["inner1"]            # 层名同 layers；layers 里要列上它
rect = [0.0, 0.0, 45.7, 80.0]  # 几块矩形盖住通道以外的地方

[[area]]                       # 只许列出的网络从这里走（比如网口变压器线路侧）
name = "ETH_LINE_SIDE"
rect = [72.2, 9.0, 84.9, 19.0]
nets = ["TX_P", "TX_N"]

[[zone]]                       # 隔离域：域内网络留在多边形里 zone_margin 以内，别的网络留在外面；drc 查同层距离
name = "RS485"
polygon = [[72.2, 64.5], [93.0, 64.5], [93.0, 86.0], [72.2, 86.0]]
nets = ["GND_ISO", "RS485_A", "RS485_B"]

[[solid_under]]                # 这个器件焊盘圈里的底层整块留给某个网络（QFN 下面的地）
part = "U10"
net = "GND"

[[preroute]]                   # 固定走线，坐标在器件封装的坐标系里（比如 USB-C 两排 D+ / D- 焊盘并联）
part = "J2"
net = "USB_DP"
width = 0.25
points = [[-0.25, 2.37], [-0.25, 1.6], [0.0, 1.35], [0.51, 1.35]]
```

## `[drc]`（`drc` 命令用）

```toml
[drc]
# clearance = 0.152   # 可选：所有铜皮统一一个间距；不给就按工程文件里 EDA 的间距规则表（推荐）
# edge = 0.3          # 可选：走线 / 过孔到板框
isolation = 1.0       # 不同隔离域同层铜皮的最小距离（默认 1.0）
isolation_scan = 3.0  # 报各域之间最近距离时看多远（默认 3.0）
# creepage_style = "kicad"  # 爬电照谁报：easyeda（默认：上下层翻板边也算、只报最小生成树上的几对）/ kicad（每层单独量、路径不穿走线、每对都报，和 KiCad 的 DRC 对数用）

# 板厂工艺（默认嘉立创标准工艺，jlcpcb.com/capabilities/pcb-capabilities）；只写要改的
[drc.fab]
# enabled = false       # 整个关掉
# track_min = 0.1       # 线宽下限（默认两层 0.1、多层 3.5 mil）
# via_diameter_min = 0.25
# via_drill_min = 0.15
# annular_via = 0.05    # 过孔焊环
# annular_pth = 0.2     # 通孔焊盘焊环
# drill_min = 0.15
# drill_max = 6.3
# npth_min = 0.5        # 非金属化孔
# via_hole_to_hole = 0.2
# hole_to_hole = 0.45   # 其它孔之间（孔边到孔边）
# hole_to_copper = 0    # 孔边到别的网络的铜；0 = 用工程间距表的「孔」那一行（嘉立创报价页：过孔孔到线 0.2、通孔到线 0.28）
# mask_web = 0.1        # 阻焊桥
# silk_width = 0.15
# silk_height = 1.0

[drc.placement]
# component_spacing = 0.2   # 两个器件（焊盘 + 器件外形，同一面）至少隔开这么多；工程文件 OTHER 规则的器件间距不为 0 时用它
# component_edge = 0.3      # 器件离板框（[check] allow_outside 里的不查）
# silk_gap = 0.2            # place 摆器件时丝印框之间留这么多
# grid = 0.5                # place 吸附的网格
# tht_smd = 5.0             # 金属化插件焊盘到它焊接面（器件另一面）的贴片件至少这么远（过炉载具），0 不查

# PADS / Mentor 式的网络类、网络规则：网络自己的 > 所在类的 > 工程文件里网络自己的 > 工程默认规则
[[drc.class]]
name = "HV"
nets = ["AC_L", "AC_N"]     # 不写 nets：用工程里同名的网络类
clearance = 1.5             # 这些网络的铜到别的网络的铜（和间距表取大的；铺铜填充、铜皮也按它查）
track = [0.5, 0.8, 3.0]     # 线宽 最小 / 默认 / 最大
via = [0.8, 0.4]            # 过孔外径、孔径下限
length = [0, 120]           # 网络走线总长 下限 / 上限（0 = 不限）
vias_max = 4                # 一个网络最多几个过孔
creepage = 3.0              # 爬电距离：沿板面到别的网络的铜（绕槽 / 挖空，上下层翻板边加板厚；只查外层）

[[drc.class_to_class]]      # 两类之间（"*" = 任何网络），优先于上面的 clearance / creepage
a = "HV"
b = "*"
clearance = 2.0
# creepage = 4.0            # 只给 creepage 的一对不影响间距

[[drc.net]]                 # 单个网络，字段同 [[drc.class]]（没有 nets）
name = "VBUS"
track = [0.4, 0.6, 2.0]
```

`drc` 的「规则 / 工艺」一段报这些（`--clearance` 统一间距时不查）：线宽、过孔尺寸、钻孔、焊环、孔到孔、孔到铜、阻焊桥（不同网络的开窗离得太近；同一器件的算警告，板厂会整排开窗）、开窗露铜（别的网络的走线落在开窗里）、丝印（字高、笔画、线宽、压出板边，警告）、元件间距（重叠算错误）、元件离板边（焊盘出板算错误、只有本体伸出算警告）、网络长度、过孔数。距离和规则都先取整到 0.1 mil 再比（和嘉立创一样）。`kicad` 导出时这些规则也写进 KiCad 的规则文件（`--rules` 同一份）。

爬电距离单列一段「爬电距离」：规则文件的 `creepage`（类对类的优先，不然取两个网络里大的）和工程文件里网络 / 网络对选的爬电规则（嘉立创的 `CREEPAGE`，取两边大的），只报最小生成树上的几对（和嘉立创一样，KiCad 每对都报）；`[drc] creepage_style = "kicad"` 改成照 KiCad 报（每层单独量、路径的直线段不横穿走线中心线、每对都报），拿来和 KiCad 的结果逐对比（MP86B 上每对一样）。导出给 KiCad 时 `kicad --drc` 带 `--all-track-errors` 跑（KiCad 默认一根走线只报第一处，会漏）。

## `[check]`（`check` 命令用）

```toml
[check]
allow_outside = ["J2", "J5"]   # 故意伸出板边的连接器
overlap = 0.15                 # 器件外框允许重叠这么多（默认 0.15）
layout_skip = ["R??", "C??"]   # 布局检查（芯片方向、阻容放远）不查这些件（参考设计原样摆的；? 一个字符，* 任意）
```

## `[erc]`（`erc` 命令用）

```toml
[erc]
levels = { CHECKFLOATPIN = "error", NETOBJECTONGRID = "ignore" }   # 改规则的级别：fatal / error / warning / note / ignore（关掉）
pins = true                                                        # 查引脚类型冲突（同 --pins；嘉立创默认不查）
pin_levels = { "Undefined-Undefined" = "ignore", "OUT-OUT" = "fatal" }  # 改冲突表的格子，两个引脚类型用 - 连
grid = 10                                                          # 格点，原理图单位（10 mil）；默认 5（0.05 英寸，嘉立创实际查的）
```

规则名照嘉立创（`erc` 的输出里每条后面括号里的就是）；引脚类型：IN、OUT、BI、Passive、Open Collector、Open Emitter、Power、Ground、HIZ、Terminator、Undefined。不写 `[erc]` 就是嘉立创的默认设置。

## `[thermal]`（`thermal` 命令用）

```toml
[thermal]
ta = 50                 # 环境温度 °C（机壳里的空气），默认 25
rise = 20               # 走线 / 铜皮 / 过孔允许温升 °C，默认 10
margin = 25             # 器件温度离它的最高温度至少留多少 °C，默认 25
warn = 0.8              # 额定值用到多少标注意，默认 0.8
copper_outer = "35um"   # 外层 / 内层铜厚、板厚：默认从工程层叠读（没层叠 1 oz / 0.5 oz / 1.6 mm）
copper_inner = "0.5oz"
board_thickness = 1.6
via_plating = "18um"    # 过孔孔壁铜厚，默认 18 µm
planes = true           # 层叠里的平面层算 IPC-2152 的平面修正（false 不算）
plane_distance = 0.2    # 不按层叠，统一按走线下 0.2 mm 有平面算
board_k = 0.25          # 板材导热系数 W/(m·K)，不写按 IPC-2152 图表的板
grid = 0.1              # 铺铜 / 铜皮网格的格子 mm，默认 0.1
map_cell = 0.5          # 热分布图（thermal --map）的格子 mm，默认 0.5
h_top = 10              # 板面换热系数（对流 + 辐射）W/(m²·K)：顶面 / 底面，默认 10（静止空气；有风扇 30–100）
h_bottom = 10
fr4_k_xy = 0.8          # FR4 导热系数 W/(m·K)：面内 / 厚度方向
fr4_k_z = 0.3

[thermal.nets]          # 网络 = 电流（有效值），或 { current, rise, from, to }
VCC_15 = { current = "1.2A", from = "D1.2", to = "P1.2" }   # from / to：位号.脚号，或位号（它在这个网络上的全部焊盘），或列表
GND = { current = 1.2, from = "P1.1", to = ["T1.7", "T1.8"] }
VOUT = { current = 3, from = "U1", to = { "U2.4" = 1.2, "U3.1" = 1.8 } }   # 几路负载各拿多少（加起来要等于 current）
"VIN+" = "0.35A"        # 只给电流：每段按整网电流算（保守，超的只标「可能超」）

[thermal.parts.Q1]      # 位号：kind + 数据手册参数（也可以放元件库 part.toml 的 [thermal]）+ 工况
kind = "mosfet"         # mosfet diode bridge resistor inductor transformer ldo converter capacitor power；不写按位号猜
part = "SVF10N65F"      # 元件库里的料号 / 型号（不写就按器件属性的料号、厂家型号、立创编号找）
```

各类器件的键（数可以带单位：`30ns` `65kHz` `4.7mΩ` `18pF` `62.5K/W` `85%`）：

| kind | 参数（数据手册） | 工况 |
|---|---|---|
| 共用 | `theta_ja`；或 `theta_jc` + `theta_cs`（默认 0.5）+ `theta_sa`（散热器）；或 `theta_ja_area = [[铜面积 mm², θJA], …]` + `tab`（散热焊盘号，默认最大的焊盘）；或 `theta`；`t_max` / `tj_max`；`margin`；`psi_jb`（热分布图上结温 = 板温 + P·ψJB） | `ta`（这颗器件旁边的温度）、`p`（直接给损耗）、`to_board`（热分布图：损耗有多少从焊盘进板，贴片默认 1、只有插件脚的默认 0.3） |
| mosfet | `rds_on`（25 °C）、`rds_on_hot` + `t_hot`（默认 125）或 `rds_ratio`；`tr`、`tf` 或 `qgd`、`qgs`、`rg`、`vplateau`、`vdrive`；`coss`（Co(er)）或 `eoss`；`qg`、`vgs`；`vsd`、`qrr`；`vds_max` | `i_rms`、`fsw`、`v_off`、`i_off`、`v_on`、`i_on`、`v_coss`、`t_dead`、`i_dead`、`v_rr`、`v_peak` |
| diode | `vf` 或 `vf0` + `rd`；`qrr`；`vrrm` | `i_avg`、`i_rms`、`fsw`、`vr`、`v_peak` |
| bridge | `vf` 或 `vf0` + `rd`（一个二极管的）；`vrrm` | `i_avg`（输出）、`i_rms`（交流侧） |
| resistor | `r`（默认读器件的值）、`power`（默认按封装 0402…2512）、`t_knee`（70）、`t_zero`（155） | `i` 或 `v`、`t_board` |
| inductor | `dcr`、`irms_rated` + `rated_rise`（40）、`isat` | `i_rms`、`i_peak`、`p_core` |
| transformer | `dcr = [每个绕组]` | `i_rms = [每个绕组]`、`p_core` |
| ldo | — | `vin`、`vout`、`iout`、`iq` |
| converter | — | `vout`、`iout`、`efficiency`、`p_ext`（片外损耗） |
| capacitor | `esr`、`ripple_rated` + `ripple_rise`（5）、`t_rated`、`life`（小时） | `i_rms` |
| power | — | `p`，或 `v` + `i` |

## `[smps]`（`smps` 命令用）

不写就用默认限值、自动认电源。`easyedatool smps <工程> --suggest` 打出认到的电源，核对后贴进来改：

```toml
[smps]
loop_warn = 25          # 热回路面积 mm²：注意 / 超（每路电源也能单写），默认 25 / 50
loop_max = 50
decouple_warn = 3       # 去耦：引脚到电容的铜路径 mm，默认 3 / 6
decouple_max = 6
decouple_area_warn = 10 # 去耦：引脚—电容—地—芯片地脚围成的回路 mm²，默认 10 / 25
decouple_area_max = 25
quiet_gap = 1.0         # 安静网络离开关节点至少 mm，默认 1
gnd = ["GND", "PGND"]   # 地网络；不写按名字认（带 GND，或 VSS、0V、…_VSS）
decouple = ["U3", "U7"] # 另外要查去耦的芯片（电源芯片自己的在 converter 里）

[[smps.converter]]      # 每路电源一个
name = "U1 降压 → +5V"
topology = "buck（同步）"   # 只是显示
ic = "U1"               # 芯片（去耦、安静网络在它封装里的不算）
inductor = "L1"         # 电感 / 变压器（安静网络从它底下走要标）
output = "+5V"          # 输出网络（芯片在这上面的脚不查去耦）
sw = ["SW5"]            # 开关节点（反激：初级的开关端和每个次级）
loops = [["C3", "VIN", "U1", "GND"]]   # 热回路：器件、网络轮流写，最后一个网络接回第一个器件；
                                       # 器件写成 U1.3 只走这个脚（多路芯片每路用自己的输入脚）
loop_names = ["输入回路"]  # 每个回路叫什么；名字以「驱动回路」开头的限值减半
quiet = ["FB5"]         # 安静网络
boot = ["C4"]           # 自举电容（和芯片、开关节点围成的回路按一半的限值查）
decouple = ["U1"]       # 查去耦的芯片，不写就是 ic
loop_warn = 300         # 这路电源自己的回路限值（反激默认 300 / 600）
loop_max = 600
```

## `[stackup]`（`si`、`impedance --stackup 规则.toml` 用）

板厂叠层单（压合结构 / 叠层阻抗表）照抄进来，从上到下；铜层按顺序对上板子的铜层（层数要一样）。

```toml
[stackup]
layers = [
  { copper = "0.036mm", name = "L1" },                  # 外层：基铜加电镀后的厚度
  { dielectric = "0.069mm", dk = 4.2, name = "PP 1080" },
  { plane = "0.03mm", name = "L2 GND" },                # 内层平面写 plane，信号层写 copper
  { dielectric = "0.508mm", dk = 4.2, name = "Core" },
  { plane = "0.03mm", name = "L3 POWER" },
  { dielectric = "0.169mm", dk = 4.2, name = "PP 1080+2116" },
  { copper = "0.03mm", name = "L4 SIGNAL" },
  { dielectric = "0.508mm", dk = 4.2, name = "Core" },
  { plane = "0.03mm", name = "L5 GND" },
  { dielectric = "0.069mm", dk = 4.2, name = "PP 1080" },
  { copper = "0.036mm", name = "L6" },
]
mask = "1mil"           # 阻焊：基材上的厚度（两面外层），线上的厚度，介电常数
mask_trace = "0.5mil"
mask_dk = 3.7
etch = "0.5mil"         # 蚀刻后线顶比线底窄多少（板厂 SI9000 里 W1 − W2）
```

厚度可以写 `mm`、`mil`、`um`、`oz`。介电常数叠层单上常常不写：拿它阻抗表里的一行（线宽、参考层、算出的阻抗）用 `impedance --stackup 规则.toml --layer 1 --field --width …` 试几个 `dk`，对上就是它用的。

## `[si]`（`si` 命令用）

```toml
[si]
rise = "0.5ns"          # 默认驱动：10–90 % 上升时间、输出阻抗、每个脚的电容（默认 0.5 ns / 40 Ω / 2 pF）
r_out = 40
c_in = "2pF"
# odt = 60              # 接收端片内端接（到交流地），默认不加
# r_diff = 100          # 差分对接收端 P、N 之间的端接，默认不加
# ibis = false          # 不用 IBIS（默认用：元件库里绑了 IBIS 的器件按 IBIS 算，没有的按上面的通用值）
# corner = "typ"        # IBIS 用哪一列：typ / min（慢、弱）/ max（快、强）
overshoot_warn = 0.10   # 反射限值（按接收端稳态电平的比例）：过冲、回沟
overshoot_max = 0.20
ringback_warn = 0.15
ringback_max = 0.30
xtalk_warn = 0.05       # 串扰限值（按攻击线驱动幅度的比例，各攻击线峰值相加）
xtalk_max = 0.10

[[si.group]]            # 按网络名分组（* ? 通配；第一个对上的组算数），没写的键沿用 [si]
nets = ["LPDDR4_DQ*", "LPDDR4_DM*"]
driver = "U1000"        # 驱动的器件或脚（U1000 / U1000.G2）；不写按原理图引脚名，再不行取引脚最多的芯片
rise = "100ps"
r_out = 40
c_in = "1pF"
odt = 60

[[si.group]]
nets = ["SPI_*"]
rise = "2ns"

[[si.group]]
nets = ["DDR_DQ*"]      # 有 IBIS 的 I/O 脚：[Model Selector] 里选哪个模型
model = "DQ_40_1600"    # 驱动脚（驱动强度）
rx_model = "DQ_ODT60_1600"  # 接收脚（片内端接）

[[si.group]]
nets = ["MIPI_DSI_*"]   # 差分对
rise = "150ps"
r_out = 50              # 每根
r_diff = 100            # 接收端差分端接
```

差分对（名字里的 DP / DM、P / N、+ / -）选了一根就两根一起算，用 P 那根所在的组。命令行 `--rise` `--rout` `--cin` `--odt` `--rdiff` `--driver` `--corner` `--no-ibis` 压过规则文件（默认值和每个组）；不给 `--net` 就仿所有组里的网络。

器件的 IBIS 默认从公司元件库来（part.toml 的 `[sim] ibis` / `ibis_component`，器件按 料号 / Manufacturer Part / 立创编号 认）。库里没有、认不出来、或者要临时换一个时，按位号写：

```toml
[si.parts.U3]
ibis = "models/rk3566.ibs"   # IBIS 文件（相对这个规则文件），压过元件库
component = "RK3566"         # 文件里的 [Component]（只有一个时可不写）
model = "GPIO_8MA_33"        # 可选：它的信号脚都用这个模型（在选择器里的才算）

[si.parts.U7]
part = "910119748"           # 板子上的属性认不出来：指定元件库里的件（料号 / 型号 / 厂家型号）

[si.parts.U9]
ibis = false                 # 这颗不用 IBIS，按通用模型
```

模型选择器（`[Model Selector]`）里选哪个：分组 `model` / `rx_model` > `[si.parts] model` > 元件库 `[sim.ibis_models]` > 按器件 POWER 脚网络名里的电压（+3V3 → 3.3 V）对模型的 `[Voltage Range]` > 选择器第一个。

## 布线器参数（一般不用改，默认值）

| 参数 | 默认 | 意思 |
|---|---|---|
| `grid` | 0.1 | 网格（毫米） |
| `clearance` | 0.15 | 铜间距（走线另加网格余量） |
| `margin_orth` / `margin_diag` | 自动 | 横竖 / 斜走一格时的网格余量（距离只在格子中心上看）。不写就按间距和线宽算刚好够的：整段线离别的铜至少「间距 + `via_margin`」——横竖 √((间距 + 半线宽 + via_margin)² + (网格/2)²) − 间距 − 半线宽，斜走把 网格/2 换成 √2·网格 − 网格/2（0.1 网格、0.1 间距、0.12 线宽时 0.017 / 0.033 mm）。以前固定 0.05 / 0.0708，0.8 mm 间距的 BGA 底下两个过孔中间过不了一根线 |
| `via_margin` | 0.01 | 过孔额外间距 |
| `via_spacing` | 0.75 | 过孔中心最小距离 |
| `track` / `power_track` | 0.2 / 0.5 | 信号线宽 / 电源线宽 |
| `via_diameter` / `via_drill` | 0.6 / 0.3 | 过孔外径 / 孔径 |
| `edge` | 0.6 | 走线中心到板框 |
| `via_cost` / `via_cost_priority` | 60 / 200 | 打过孔的代价（优先网络更贵，尽量一层走完） |
| `dir_penalty` / `diag_penalty` | 1.5 / 1.15 | 布线层从顶层往下轮流偏横、偏竖（两层板：顶横底竖）；斜走代价 |
| `soft_cost` / `rip_passes` / `rip_max` | 40 / 8 / 8 | 拆线重布；每次重来取剩得最少的那一轮。两个网络来回互拆（A 为布通拆了 B、B 又拆了 A）以后，这次重来里 A 不再拆 B：找路时 B 的铜当固定铜，只能穿过别的网络或绕开（MP157 的 PA10 和 FDCAN1_RX 抢 MPU 角上一条道，原来来回拆满 16 轮） |
| `hist_cost` | 0 | 拆线重布的拥堵历史：没布通的连接找路时穿过别的网络的格子，每次加一，之后这次重来的每次找路在那里每格多付 `hist_cost` × 次数（被占的格子是 `soft_cost` 倍），抢同一个口子的连接自己分散开（0 = 不用） |
| `layer_plan` / `layer_pref_cost` | false / 3 | 布线前分层规划：待连连接的直线两两算交叉，三层（或几层）分给网络让交叉的网络不同层，网络离开自己的层每格付 `layer_pref_cost` 倍；`[nets] layer = { 网络 = "bottom" }` 手工指定。按球心直线算、不算 BGA 出口的过孔，MP157 上开了反而少通 2–6 根，先别用 |
| `restarts` | 3 | 没布通的网络挪到前面整轮重布几次（0 = 不做） |
| `optimize_passes` / `optimize_soft_cost` | 3 / 4 | 绕远的网络连同挡路的一起重布（0 = 不做） |
| `stub_len` / `narrow` / `fan_band` / `stub_end_radius` | 1.0 / 0.35 / 2.6 / 0.7 | 细间距焊盘出线短线 |
| `short_first` | 6.5 | 短于这个的连接先布 |
| `near_pad` / `near_cost` | 0.8 / 3 | 优先网络离焊盘近的代价 |
| `zone_margin` | 1.0 | 隔离域内外各让开 |
| `pour_clearance` / `pour_edge` / `pour_neck` | 0.35 / 0.35 / 2 | 布线时模拟铺铜（判断地是否连通） |
| `stitch_pitch` / `stitch_min` | 4.0 / 1.8 | 地缝合过孔的间距 |
| `island_rounds` | 4 | 孤立铺铜补线轮数 |
| `octi_span` / `bbox_margin` | 300 / 12 | 路径拉直、搜索范围 |

布不通时先改摆放和 `[nets] first` / `priority`，别先动这些参数。
