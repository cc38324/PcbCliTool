# easyedatool 命令参考

由 `tools/package.py` 从各命令的 `--help` 生成，别手改。

```
嘉立创EDA专业版工程离线工具：从设计文件生成工程、自动布线、算铺铜、查铜皮间距（DRC）、核对原理图和 PCB，出效果图、原理图 PDF / 网表 / BOM、生产文件（Gerber、钻孔、贴片坐标）；view 开实时预览窗口

Usage: easyedatool [OPTIONS] <COMMAND>

Commands:
  info         板子概况：尺寸、器件、焊盘、走线、过孔、铺铜、网络
  pads         列出焊盘：位号、脚号、网络、中心（毫米）、尺寸、转角、层
  route        自动布线：删掉全部旧走线、过孔和铺铜填充，按规则文件重新布线（多层板按板子的铜层布，内层铺铜平面只让过孔穿过），写回 .epcb2，再重算铺铜
  drc          查铜皮：不同网络间距、离板边距离、禁布区、没连通的网络、悬空线头、隔离带宽度（有问题时退出码 1）
  check        核对工程：器件重叠 / 出板、原理图没接上的导线、原理图和 PCB 逐脚网络对比（有问题时退出码 1）
  erc          原理图电气规则检查（ERC）：照嘉立创原理图 DRC 逐条查——引脚悬空、导线没接引脚 / 只接一个引脚、一组导线多个网络名、网络标识和导线名不一致、引脚端点重叠、位号、缺器件 / 封装、引脚和焊盘对不上、多部件、超出图纸、不在格点；规则名、级别、中文说明都照它，--pins 再查引脚类型冲突（有致命错误、错误或警告时退出码 1）
  hookup       接法检查：照元件库里芯片的接法规则（按数据手册的参考电路和外部元件表写的）查原理图——两脚之间该有的电感 / 电阻 / 电容和取值、额定电压，该同网的脚，该接地或悬空的脚，几种接法里用的是哪一种；查得出接错脚这类 ERC 查不出来的错（有错误或警告时退出码 1）
  repair       修工程文件：换行改回 LF（CRLF 嘉立创读不了，PCB / 原理图打开是空的）、去掉 BOM、补回索引里丢掉的版本号、删掉没写完的空临时文件；先在嘉立创里关掉这个工程
  gen          从设计文件（TOML / JSON）生成嘉立创EDA专业版工程：原理图、PCB（器件摆放、铺铜、禁布区、丝印、位号）
  render       出 PNG 效果图
  pdf          原理图出 PDF：每页一页（矢量），文字嵌入字体子集、能搜索和复制
  netlist      原理图网表：Protel 格式（.net，Altium 等大多数 EDA 能导入）或 CSV（每个引脚一行）
  place        整理摆放：器件原点吸附到网格，间距不够的推开（只动没连走线、没锁定、不带孔的器件，--all 全动）；默认只列出怎么挪，--write 写回、重算铺铜、自动 DRC
  layout       布局文件（设计文件旁边的 <设计>.layout.toml，和 gen --layout 的原理图排版无关）：器件位置、面、角度、锁定、位号，走线和过孔；窗口里手改过原理图以后还有原理图的画法（[sch]）。有它 gen 就照它摆器件、把走线和过孔写回工程、照人画的画原理图（设计文件改了的对上去），窗口里手改的、命令布的线不会被下次 gen 冲掉；工程被改过（布线、窗口里挪了器件），下次 gen 先把它收回来。不带参数看状态；--save 把工程现在的几何记进去（没有就建）；--forget 删掉（gen 回到照设计文件和自动摆法摆）；--forget-sch 只删原理图的画法（gen 重新自动排原理图）
  review       审核：人在预览窗口里标的「已审」（按器件内容记哈希：值、封装、每个脚的网络变了勾就不算了）和审核意见。AI 每轮开始先看这里和工程里的 .easyedatool/edits.log；改完一条意见用 --answer 回复，人在窗口里确认
  kicad        导出 KiCad 工程：.kicad_pcb（铜皮照工程里存的：焊盘、走线、过孔、铺铜填充和辐条原样带上）、.kicad_pro（规则最小值、网络类、哪些检查算数）、.kicad_dru（嘉立创的安全间距表、板边和孔的间距、线宽、过孔尺寸翻成 KiCad 的条件规则）
  assembly     贴片图 PDF（PADS 那种）：顶面、底面各一页，画板框、焊盘、元件外形，位号写在元件中间（顺着长边、按元件大小缩放），底面从背面看；不改板子，和丝印位号无关
  fab          PCB 生产文件：Gerber（铜、阻焊、钢网、丝印、板框）、钻孔（金属化 / 过孔 / 非金属化）、贴片坐标、贴片图 PDF，另打一个给嘉立创的 zip
  pour         铺铜：照 EDA 的规则算填充（间距、热焊盘、去孤岛），和工程里 EDA 算的逐块比；--write 写回 .epcb2（gen、route 会自动算）
  footprint    画封装：按封装类型和数据手册推荐焊盘图的尺寸（脚数、间距、两排中心距、焊盘、本体）生成焊盘，坐标由工具算；打印量出来的尺寸、焊盘表和设计文件写法，-o 出预览图。也能核对设计文件里的封装
  view         实时预览窗口（viewer/ 里的 Flutter 程序）：PCB 分层图和原理图，工程文件一改就重画；route、pour --write、gen、drc、check、erc 跑的时候，进度、输出、正在布的线、问题点实时显示在窗口里；PCB 一改自动查 DRC、原理图一改自动查 ERC，问题点标在板上和页上。窗口只读文件，不写
  serve        预览窗口的后台（窗口自己会起它，一般不用手动跑）：在 127.0.0.1 上提供工程的绘图数据，盯着文件变化，转发命令的进度
  import       导入 PADS 板子（PADS Layout 导出的 ASCII .asc）或 Altium 板子（.PcbDoc）：转成嘉立创EDA工程（PCB：层叠、封装、器件、网络、走线、过孔、铺铜或铜皮、禁布区、板框、丝印；给 --sch 时连同原理图合成一个工程：PADS 配 OrCAD .DSN，Altium 配 .SchDoc），读回来逐项自检
  pair         差分对布线：按差分对规则的线宽和线距在一层上自动找路，两根线等距并排走、两头从焊盘扇出，走完逐段查间距；默认只报告，--write 写回（这对布过线的加 --replace 先删掉原来的）
  thermal      损耗结温和载流温升：按规则文件 [thermal] 里的工况算功率器件的损耗和结温（MOS 管、二极管、整流桥、电阻、电感、变压器、LDO、开关稳压芯片、电容；热阻用 θJA、散热器、或按板上散热焊盘连着的铜面积插值），走线、铺铜 / 铜皮、过孔按 IPC-2152 算温升（旁边给 IPC-2221）；给了电流从哪进、从哪出（from / to）就把网络当电阻网络（铺铜细分成网格）解出每段的电流和压降（超了退出码 1）
  si           信号完整性（反射、串扰）：按叠层用场求解器算每段走线的阻抗和延时，连同过孔、串联电阻 / 电容、到电源和地的端接搭成电路，从驱动脚加阶跃做时域仿真（通用模型：驱动的上升时间和输出阻抗、每个脚的电容），报每个接收端的飞行时间、过冲、回沟、稳定时间、单调性和阻抗跳变的段；差分对（按网络名认）两根反相一起驱动、并排段按耦合线，报差分波形、P/N 偏斜、共模、差分阻抗；--xtalk 再算同层平行网络的串扰（近端 / 远端）（超了退出码 1）；--spice 把每个电路和自己的波形写出来，tools/verify_si/compare.py 拿 ngspice 复算对比
  ibis         读 IBIS 模型文件（.ibs）：列出器件、引脚、模型选择器和模型（类型、电源、C_comp、有哪些表），每个能驱动的模型把自己的 V–T 波形放回测它时的夹具里重算、和表比（模型自洽、本工具读得对的检查；差超过幅度 10 % 退出码 1）
  smps         开关电源版图检查：热回路（照实际铜走的路径算三维回路面积、估电感）、开关节点的铜皮和过孔、FB 这类安静网络离开关节点多远 / 有没有在相邻层压着它 / 从电感底下走、芯片去耦电容的铜路径和地回路；规则文件 [smps] 写电源，不写就自动认（有原理图按引脚名 SW / VIN / FB / BOOT，没有按连接：电感接芯片是降压 / 升压，一颗芯片几路的每路用自己的输入脚；变压器接 MOS 管或内置开关管的芯片是反激，顺着栅极找控制芯片）（超了退出码 1）
  label        成品板加丝印：照标注文件（TOML）往布好线的板子上加丝印字——自由文字、器件旁边的名字（接口是干什么的）、每个脚旁边的信号名（排针、端子）；只加丝印字，铜皮和别的都不动，不用重新生成、重新布线；字自己找不压焊盘、不压别的丝印、不出板边的地方，放不下就缩小（不小于 min_size）或换一边，还放不下的报出来；再跑一遍替换上次加的（记在工程的 .easyedatool/labels.json）；有 [designators] 时连器件位号一起整理：原地不挡着的留下，压焊盘（板厂会削掉）或压别的丝印的挪到器件旁最近的空处、放不下缩小、再不行不印（hide = false 则照旧并报出来），挪过去的位号必须离自己的器件最近，免得认错；默认只报告，--write 写回
  widen        电源线加粗：布线后把电源网络逐段加到放得下的最粗（先试目标线宽，再 0.4、0.3 mm），细间距焊盘旁边放不下的保持原样（颈缩）；按工程间距规则查别的网络，默认只报告，--write 写回（之后 pour --write 重算铺铜）
  tune         绕等长：在网络的直线段上加蛇形线补长度——差分对里短的那根补到另一根、等长组里超出容差的补到最长那根、一根网络补到指定长度；只在按工程间距规则放得下的地方绕，默认只报告，--write 写回
  impedance    阻抗：按工程的叠层（层管理器里的厚度、介电常数）照嘉立创阻抗计算器的公式和取法算（和它算的逐位一致）：列叠层，每层单端 / 差分要多宽的线、给定线宽的阻抗，每对差分线按实际走线的差分阻抗
  constraints  差分对、等长组、网络类和它们的规则：列出工程里的（每对的走线长度和对内长度差、每组的长度差），--auto 按网络名认差分对（规则按已布走线量出的线宽和间距），--from 从约束文件加，--write 写进工程
  orcad        导入 OrCAD Capture 原理图（.DSN）：摘要（每页的导线和网络名、器件、电源符号、跨页连接……看读得全不全）、网表 CSV；--out 转成嘉立创EDA工程（只有原理图），读回来和 OrCAD 网表逐脚自检
  altium       导入 Altium 原理图（.SchDoc，二进制或 ASCII 存的都行）：自己读（不用装 Altium），`--out` 转成嘉立创EDA工程（只有原理图），写完读回来和 Altium 的连接逐脚自检；没名字的网络照 Altium 起名（Net + 位号_脚号，和它的 PCB 一样）
  lib          公司元件库（PartsLib）：找库、列元件、查元件，按数据手册做新件（引脚表排符号、IPC-7351B 算封装、3D），给草稿分料号
  bom          原理图 BOM：CSV，列和嘉立创EDA导出的一样（Comment / Designator / Footprint / Supplier Part …），能直接传立创贴片
  help         Print this message or the help of the given subcommand(s)

Options:
      --no-drc   改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
  -h, --help     Print help
  -V, --version  Print version
```

## info

```
板子概况：尺寸、器件、焊盘、走线、过孔、铺铜、网络

Usage: easyedatool info [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .epcb2 文件、.eprj3 工程索引或工程文件夹；PADS .asc、Altium .PcbDoc 直接读

Options:
      --no-drc  改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
  -h, --help    Print help
```

## pads

```
列出焊盘：位号、脚号、网络、中心（毫米）、尺寸、转角、层

Usage: easyedatool pads [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .epcb2 文件、.eprj3 工程索引或工程文件夹

Options:
      --no-drc       改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --part <PART>  只列这个位号的焊盘
  -h, --help         Print help
```

## route

```
自动布线：删掉全部旧走线、过孔和铺铜填充，按规则文件重新布线（多层板按板子的铜层布，内层铺铜平面只让过孔穿过），写回 .epcb2，再重算铺铜

Usage: easyedatool route [OPTIONS] --rules <RULES> <INPUT>

Arguments:
  <INPUT>  .epcb2 文件、.eprj3 工程索引或工程文件夹（会被改写）

Options:
      --no-drc         改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --rules <RULES>  布线规则（TOML），见 examples/
      --only <ONLY>    这次只布这些网络（逗号隔开，可用 * ?；盖过规则文件的 [nets] only）：别的网络的铜原样留着、没连的留给下次布。先布几根要让路的线，再用 pair 布差分对、最后整板布
  -h, --help           Print help
```

## drc

```
查铜皮：不同网络间距、离板边距离、禁布区、没连通的网络、悬空线头、隔离带宽度（有问题时退出码 1）

Usage: easyedatool drc [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .epcb2 文件、.eprj3 工程索引或工程文件夹；PADS .asc、Altium .PcbDoc 直接读

Options:
      --no-drc                 改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --rules <RULES>          板子规则（TOML，和布线共用）：铺铜网络、隔离区、[drc] 限值；不给就用默认限值、不查隔离
      --clearance <CLEARANCE>  所有铜皮统一用这个间距（毫米，drc.py 用 0.152）；不给就按工程文件里 EDA 的间距规则
      --json <JSON>            把完整结果写成 JSON
  -h, --help                   Print help
```

## check

```
核对工程：器件重叠 / 出板、原理图没接上的导线、原理图和 PCB 逐脚网络对比（有问题时退出码 1）

Usage: easyedatool check [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .epcb2 文件、.eprj3 工程索引或工程文件夹（原理图在同一工程的 sch 文件夹里）

Options:
      --no-drc         改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --rules <RULES>  板子规则（TOML，和布线共用）：[check] allow_outside 放行伸出板外的连接器
      --json <JSON>    把完整结果写成 JSON
  -h, --help           Print help
```

## erc

```
原理图电气规则检查（ERC）：照嘉立创原理图 DRC 逐条查——引脚悬空、导线没接引脚 / 只接一个引脚、一组导线多个网络名、网络标识和导线名不一致、引脚端点重叠、位号、缺器件 / 封装、引脚和焊盘对不上、多部件、超出图纸、不在格点；规则名、级别、中文说明都照它，--pins 再查引脚类型冲突（有致命错误、错误或警告时退出码 1）

Usage: easyedatool erc [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .eprj3 工程索引、工程文件夹或工程里的 .epcb2

Options:
      --no-drc         改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --rules <RULES>  规则文件（TOML，和布线共用）的 [erc] 表：levels 改级别（"ignore" 关掉）、pins 打开引脚类型冲突、pin_levels 改冲突表
      --pins           再查引脚类型冲突（同一网络上两个输出、电源接地……，照嘉立创的冲突表；它默认关）
      --top <TOP>      每条规则最多列几条（默认 10，0 全列） [default: 10]
      --json <JSON>    把完整结果写成 JSON
  -h, --help           Print help
```

## hookup

```
接法检查：照元件库里芯片的接法规则（按数据手册的参考电路和外部元件表写的）查原理图——两脚之间该有的电感 / 电阻 / 电容和取值、额定电压，该同网的脚，该接地或悬空的脚，几种接法里用的是哪一种；查得出接错脚这类 ERC 查不出来的错（有错误或警告时退出码 1）

Usage: easyedatool hookup [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .eprj3 工程索引、工程文件夹或工程里的 .epcb2

Options:
      --lib <LIB>    元件库文件夹（不给就按 lib 的找法：环境变量、工程旁边的 easyedatool.toml、本机配置）
      --no-drc       改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --json <JSON>  把完整结果写成 JSON
  -h, --help         Print help
```

## repair

```
修工程文件：换行改回 LF（CRLF 嘉立创读不了，PCB / 原理图打开是空的）、去掉 BOM、补回索引里丢掉的版本号、删掉没写完的空临时文件；先在嘉立创里关掉这个工程

Usage: easyedatool repair [OPTIONS] <INPUT>

Arguments:
  <INPUT>  工程文件夹、.eprj3 工程索引或工程里的任一文件

Options:
      --no-drc  改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
  -h, --help    Print help
```

## gen

```
从设计文件（TOML / JSON）生成嘉立创EDA专业版工程：原理图、PCB（器件摆放、铺铜、禁布区、丝印、位号）

Usage: easyedatool gen [OPTIONS] --out <OUT> <DESIGN>

Arguments:
  <DESIGN>  设计文件（.toml 或 .json），见 examples/

Options:
      --no-drc           改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --out <OUT>        工程文件夹：sch、pcb 整个换掉，索引文件就地覆盖
      --keep-fills       保留 EDA 算好的铺铜填充（不自己算）：EDA 里重建铺铜并保存后再跑一次，除填充外 EDA 的 PCB 必须和生成的一模一样
      --no-pour          不算铺铜填充（默认照 EDA 的规则算好写进工程）
      --schematic-only   只重画原理图，PCB 一点不动（布线、铺铜都留着）：原理图器件沿用板子上的 Unique ID 和封装 id，EDA 照样配对。板子上缺器件或封装就不干
      --layout <LAYOUT>  原理图排版，盖过设计文件里的 [schematic] layout：pages（分页，芯片附件连实线）或 build.py（一张图、短线加标签）
  -h, --help             Print help
```

## render

```
出 PNG 效果图

Usage: easyedatool render [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .epcb2 文件、.eprj3 工程索引或工程文件夹；PADS .asc、Altium .PcbDoc 直接读

Options:
      --no-drc           改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
  -o, --out <OUT>        输出文件（默认 <板名>_<视图>.png）
      --view <VIEW>      top 正面实物；bottom 背面实物（左右镜像）；layers 分层线路图；sch 原理图（每页一张） [default: top] [possible values: top, bottom, layers, sch]
      --ppmm <PPMM>      每毫米像素数 [default: 20]
      --window <WINDOW>  只画这一块，毫米，y 向上：x0,y0,x1,y1
      --font <FONT>      TrueType 字体文件（默认用系统里的 Arial 等）
      --net <NET>        高亮这些网络（分层图里画成青色），逗号分隔
      --page <PAGE>      原理图只出这一页（从 1 数）
      --layer <LAYER>    分层图只画这些铜层，逗号分隔：1 顶层、2 底层、15 内层1、16 内层2……
  -h, --help             Print help
```

## pdf

```
原理图出 PDF：每页一页（矢量），文字嵌入字体子集、能搜索和复制

Usage: easyedatool pdf [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .eprj3 工程索引、工程文件夹或 .epcb2 文件（原理图在同一工程的 sch 文件夹里）

Options:
      --no-drc       改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
  -o, --out <OUT>    输出文件（默认 <工程名>_sch.pdf）
      --font <FONT>  TrueType 字体文件（默认用系统里带中文的：微软雅黑、黑体……）
  -h, --help         Print help
```

## netlist

```
原理图网表：Protel 格式（.net，Altium 等大多数 EDA 能导入）或 CSV（每个引脚一行）

Usage: easyedatool netlist [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .eprj3 工程索引、工程文件夹或 .epcb2 文件

Options:
      --no-drc           改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
  -o, --out <OUT>        输出文件（默认 <工程名>.net；扩展名 .csv 时写 CSV）
      --format <FORMAT>  格式（不给就看扩展名） [possible values: protel, csv]
  -h, --help             Print help
```

## place

```
整理摆放：器件原点吸附到网格，间距不够的推开（只动没连走线、没锁定、不带孔的器件，--all 全动）；默认只列出怎么挪，--write 写回、重算铺铜、自动 DRC

Usage: easyedatool place [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .epcb2 文件、.eprj3 工程索引或工程文件夹

Options:
      --no-drc             改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --rules <RULES>      规则文件（TOML，和 drc 的同一份）：元件间距、网格取 [drc.placement]（工程文件 OTHER 规则的器件间距不为 0 时用它）
      --grid <GRID>        网格（mm；默认 [drc.placement] 的 0.5；0 = 不吸附）
      --spacing <SPACING>  元件间距（mm；默认规则里的）
      --all                连了走线、锁定、带孔（连接器、安装孔）的器件也动（会扯断走线、对不上外壳）
      --arrange            不是推开，而是把能动的器件在它们现在占的范围里（或 --area 给的矩形里）按 gen 的整齐摆法重新排成行
      --area <AREA>        重新排时用的矩形（mm，y 向上）：x0,y0,x1,y1
      --write              写回工程（先 git 提交）
  -h, --help               Print help
```

## layout

```
布局文件（设计文件旁边的 <设计>.layout.toml，和 gen --layout 的原理图排版无关）：器件位置、面、角度、锁定、位号，走线和过孔；窗口里手改过原理图以后还有原理图的画法（[sch]）。有它 gen 就照它摆器件、把走线和过孔写回工程、照人画的画原理图（设计文件改了的对上去），窗口里手改的、命令布的线不会被下次 gen 冲掉；工程被改过（布线、窗口里挪了器件），下次 gen 先把它收回来。不带参数看状态；--save 把工程现在的几何记进去（没有就建）；--forget 删掉（gen 回到照设计文件和自动摆法摆）；--forget-sch 只删原理图的画法（gen 重新自动排原理图）

Usage: easyedatool layout [OPTIONS] <INPUT>

Arguments:
  <INPUT>  gen 生成的工程文件夹（工程里的 .easyedatool/source.toml 记着设计文件）

Options:
      --no-drc      改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --save        把工程现在的几何记进布局文件（没有就建）
      --forget      删掉布局文件
      --forget-sch  只删布局文件里记的原理图画法（[sch]）：下次 gen 重新自动排原理图，人在窗口里拖的、画的都不留
  -h, --help        Print help
```

## review

```
审核：人在预览窗口里标的「已审」（按器件内容记哈希：值、封装、每个脚的网络变了勾就不算了）和审核意见。AI 每轮开始先看这里和工程里的 .easyedatool/edits.log；改完一条意见用 --answer 回复，人在窗口里确认

Usage: easyedatool review [OPTIONS] <INPUT>

Arguments:
  <INPUT>  工程文件夹、.eprj3 工程索引或 .epcb2 文件

Options:
      --answer <编号> <怎么改的>  回复一条审核意见：编号和怎么改的，如 --answer 3 "新加 R2，U1.3 改接 EN"
      --no-drc              改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --json <JSON>         另存 JSON（已审的器件、改了要重看的、全部意见、人还没确认的改动）
  -h, --help                Print help
```

## kicad

```
导出 KiCad 工程：.kicad_pcb（铜皮照工程里存的：焊盘、走线、过孔、铺铜填充和辐条原样带上）、.kicad_pro（规则最小值、网络类、哪些检查算数）、.kicad_dru（嘉立创的安全间距表、板边和孔的间距、线宽、过孔尺寸翻成 KiCad 的条件规则）

Usage: easyedatool kicad [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .epcb2 文件、.eprj3 工程索引或工程文件夹；PADS .asc、Altium .PcbDoc 直接读

Options:
      --no-drc         改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
  -o, --out <OUT>      输出文件夹（默认 <工程名>_kicad）
      --drc            写完用 KiCad 自己的命令行查一遍 DRC（kicad-cli：环境变量 KICAD_CLI、PATH，或各盘 Program Files\KiCad 下最新的）
      --rules <RULES>  规则文件（TOML，和 drc 的同一份）：[drc.fab] 工艺、[drc.placement] 元件间距、[[drc.class]] 网络类规则也写进 KiCad 的规则
  -h, --help           Print help
```

## assembly

```
贴片图 PDF（PADS 那种）：顶面、底面各一页，画板框、焊盘、元件外形，位号写在元件中间（顺着长边、按元件大小缩放），底面从背面看；不改板子，和丝印位号无关

Usage: easyedatool assembly [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .epcb2 文件、.eprj3 工程索引或工程文件夹；PADS .asc、Altium .PcbDoc 直接读

Options:
      --no-drc       改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
  -o, --out <OUT>    输出文件（默认 <工程名>_assembly.pdf）
      --value        位号下面再写元件值
      --font <FONT>  TrueType 字体（默认用系统里带中文的）
  -h, --help         Print help
```

## fab

```
PCB 生产文件：Gerber（铜、阻焊、钢网、丝印、板框）、钻孔（金属化 / 过孔 / 非金属化）、贴片坐标、贴片图 PDF，另打一个给嘉立创的 zip

Usage: easyedatool fab [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .epcb2 文件、.eprj3 工程索引或工程文件夹；PADS .asc、Altium .PcbDoc 直接读

Options:
      --no-drc       改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
  -o, --out <OUT>    输出文件夹（默认 <工程名>_fab）
      --font <FONT>  丝印文字用的 TrueType 字体（默认用系统里带中文的）
      --files        压缩包之外也把每个 Gerber / 钻孔文件单独写出来（默认只出压缩包和贴片坐标）
  -h, --help         Print help
```

## pour

```
铺铜：照 EDA 的规则算填充（间距、热焊盘、去孤岛），和工程里 EDA 算的逐块比；--write 写回 .epcb2（gen、route 会自动算）

Usage: easyedatool pour [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .epcb2 文件、.eprj3 工程索引或工程文件夹

Options:
      --no-drc           改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --write            把算出的填充写回 .epcb2（会改写输入：先 git 提交）
      --gerber <GERBER>  用算出的填充出铜层 Gerber 到这个文件夹（和 EDA 的比）
      --svg <SVG>        查差别用：每块铺铜画一张 SVG 到这个文件夹（红 EDA 的、蓝这里的、灰 避让、黄 热焊盘间隙），要给 --window
      --window <WINDOW>  SVG 画的范围，毫米，y 向上：x0,y0,x1,y1
  -h, --help             Print help
```

## footprint

```
画封装：按封装类型和数据手册推荐焊盘图的尺寸（脚数、间距、两排中心距、焊盘、本体）生成焊盘，坐标由工具算；打印量出来的尺寸、焊盘表和设计文件写法，-o 出预览图。也能核对设计文件里的封装

Usage: easyedatool footprint [OPTIONS] <WHAT>

Arguments:
  <WHAT>  标准名（SOIC-8、TSSOP-20、SOT-23-6、SOT-223、LQFP-48、R0805、HDR-2x5-2.54……；list 列出全部）或设计文件（.toml / .json）

Options:
      --name <NAME>  设计文件里只看这一个封装
      --no-drc       改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
  -o, --out <OUT>    出预览图（PNG，第一个封装）
      --ppmm <PPMM>  预览图每毫米像素 [default: 60]
  -h, --help         Print help
```

## view

```
实时预览窗口（viewer/ 里的 Flutter 程序）：PCB 分层图和原理图，工程文件一改就重画；route、pour --write、gen、drc、check、erc 跑的时候，进度、输出、正在布的线、问题点实时显示在窗口里；PCB 一改自动查 DRC、原理图一改自动查 ERC，问题点标在板上和页上。窗口只读文件，不写

Usage: easyedatool view [OPTIONS] <INPUT>

Arguments:
  <INPUT>  工程文件夹、.eprj3 工程索引或 .epcb2 文件；PADS .asc、Altium .PcbDoc 直接读

Options:
      --no-drc       改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --page <PAGE>  先显示原理图第几页（从 1 数；不给就先显示 PCB）
      --find <FIND>  打开后找这个位号或网络给人看：在 PCB 上（器件框出焊盘、网络高亮），带 --page 时在原理图上
  -h, --help         Print help
```

## serve

```
预览窗口的后台（窗口自己会起它，一般不用手动跑）：在 127.0.0.1 上提供工程的绘图数据，盯着文件变化，转发命令的进度

Usage: easyedatool serve [OPTIONS] <INPUT>

Arguments:
  <INPUT>  工程文件夹、.eprj3 工程索引或 .epcb2 文件；PADS .asc、Altium .PcbDoc 直接读

Options:
      --no-drc           改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --port <PORT>      端口（0 = 挑一个空闲的） [default: 0]
      --exit-with-stdin  标准输入关掉就退出（窗口起它时用：窗口没了它也跟着走）
      --rules <RULES>    自动 DRC / ERC 用的规则文件（和 drc、erc 的同一份；PCB、原理图一改就查，问题点标在窗口里；全局 --no-drc 关掉）
  -h, --help             Print help
```

## import

```
导入 PADS 板子（PADS Layout 导出的 ASCII .asc）或 Altium 板子（.PcbDoc）：转成嘉立创EDA工程（PCB：层叠、封装、器件、网络、走线、过孔、铺铜或铜皮、禁布区、板框、丝印；给 --sch 时连同原理图合成一个工程：PADS 配 OrCAD .DSN，Altium 配 .SchDoc），读回来逐项自检

Usage: easyedatool import [OPTIONS] --out <OUT> <INPUT>

Arguments:
  <INPUT>  PADS 导出的 .asc，或 Altium 的 .PcbDoc

Options:
      --no-drc       改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --out <OUT>    写到这个文件夹（要空文件夹，或上次导入的同名工程）；文件夹名就是工程名
      --name <NAME>  工程名（默认用 --out 文件夹的名字：嘉立创按文件夹名认工程，两者最好一致）
      --sch <SCH>    同一块板的原理图（PADS 板配 OrCAD .DSN，Altium 板配 .SchDoc）：和 PCB 合成一个工程，两边的器件按位号配对（同一个 Unique ID 和器件，器件用 PCB 的封装），写完逐脚比原理图和 PCB 的网络
  -h, --help         Print help
```

## pair

```
差分对布线：按差分对规则的线宽和线距在一层上自动找路，两根线等距并排走、两头从焊盘扇出，走完逐段查间距；默认只报告，--write 写回（这对布过线的加 --replace 先删掉原来的）

Usage: easyedatool pair [OPTIONS] <INPUT>

Arguments:
  <INPUT>  工程（文件夹、.eprj3 或 .epcb2）

Options:
      --no-drc                       改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --pair <PAIR>                  差分对（名字，可以给几次）
      --layer <LAYER>                走哪层：1 顶层、2 底层、15 内层1…… [default: 1]
      --width <WIDTH>                线宽（mm；默认差分对规则这一层的默认线宽）
      --gap <GAP>                    线距（mm；默认差分对规则这一层的默认线距）
      --escape-width <ESCAPE_WIDTH>  出线（焊盘到并排走起来那一段）的线宽（mm；默认差分对规则这一层的最小线宽）
      --grid <GRID>                  网格（mm；默认线宽和线距里小的那个的一半）
      --replace                      先删掉这对原来的走线和过孔
      --ends <ENDS>                  只布一段：两头的器件位号，逗号隔开（如 U4,U3：USB 从 ESD 到模组；U10,T1：网口从 PHY 到变压器）。每根网络在每个器件上取一个焊盘（有两个的取离另一头近的），这对网络别的焊盘、过孔、走线照样避开，不删（除非 --replace）
      --no-tune                      布完不自动绕等长（默认：对内长度差超出规则时在短的那根上补）
      --write                        写回 .epcb2（先 git 提交；嘉立创开着这个工程时先关掉，写完再打开；铺铜要在嘉立创里重建）
  -h, --help                         Print help
```

## thermal

```
损耗结温和载流温升：按规则文件 [thermal] 里的工况算功率器件的损耗和结温（MOS 管、二极管、整流桥、电阻、电感、变压器、LDO、开关稳压芯片、电容；热阻用 θJA、散热器、或按板上散热焊盘连着的铜面积插值），走线、铺铜 / 铜皮、过孔按 IPC-2152 算温升（旁边给 IPC-2221）；给了电流从哪进、从哪出（from / to）就把网络当电阻网络（铺铜细分成网格）解出每段的电流和压降（超了退出码 1）

Usage: easyedatool thermal [OPTIONS] --rules <RULES> <INPUT>

Arguments:
  <INPUT>  工程文件夹、.eprj3 工程索引或 .epcb2；PADS .asc、Altium .PcbDoc 直接读

Options:
      --no-drc                   改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --rules <RULES>            规则文件（TOML，和布线共用）的 [thermal] 表：环境温度 ta、允许温升 rise、[thermal.nets] 各网络的电流、[thermal.parts.位号] 器件的工况和参数
      --lib <LIB>                公司元件库（器件的 [thermal] 参数从这里补）；不给就照常找（环境变量、工程旁的 easyedatool.toml、本机配置），找不到也能算
      --top <TOP>                每个网络列几段最热的走线和过孔（超的全列） [default: 5]
      --map <MAP>                再算整块板的温度分布（器件损耗从焊盘进板、载流网络的铜损，铜和 FR4 导热、过孔、板面散热），出热分布图 PNG
      --map-layers <MAP_LAYERS>  热分布图画哪些层：outer 顶层和底层（默认），all 每一层 [default: outer]
      --json <JSON>              把完整结果写成 JSON（每段走线、每个过孔的电流和温升）
  -h, --help                     Print help
```

## si

```
信号完整性（反射、串扰）：按叠层用场求解器算每段走线的阻抗和延时，连同过孔、串联电阻 / 电容、到电源和地的端接搭成电路，从驱动脚加阶跃做时域仿真（通用模型：驱动的上升时间和输出阻抗、每个脚的电容），报每个接收端的飞行时间、过冲、回沟、稳定时间、单调性和阻抗跳变的段；差分对（按网络名认）两根反相一起驱动、并排段按耦合线，报差分波形、P/N 偏斜、共模、差分阻抗；--xtalk 再算同层平行网络的串扰（近端 / 远端）（超了退出码 1）；--spice 把每个电路和自己的波形写出来，tools/verify_si/compare.py 拿 ngspice 复算对比

Usage: easyedatool si [OPTIONS] <INPUT>

Arguments:
  <INPUT>  工程文件夹、.eprj3 工程索引或 .epcb2；PADS .asc、Altium .PcbDoc 直接读

Options:
      --net <NET>        网络，逗号分隔，可用 * 和 ? 通配：LPDDR4_DQ*,SDIO_CLK（不写就仿规则文件 [[si.group]] 里的网络）
      --no-drc           改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --rules <RULES>    规则文件（TOML，和布线共用）的 [si] 表：默认驱动参数和限值，[[si.group]] 按网络分组各写驱动脚、上升时间、输出阻抗、脚电容、端接；有 [stackup] 就按它的板厂叠层算
      --driver <DRIVER>  驱动的器件或脚（U1 / U1.A5）；不写按原理图引脚名（TXD / SDO 是输出，RXD / MOSI / CS 是输入），再不行取引脚最多的芯片
      --rise <RISE>      驱动的上升时间（10–90 %），默认 0.5ns
      --rout <ROUT>      驱动的输出阻抗，默认 40Ω
      --cin <CIN>        每个脚的电容（驱动和接收），默认 2pF
      --odt <ODT>        接收端的片内端接（到交流地），默认不加
      --rdiff <RDIFF>    差分对接收端 P、N 之间的端接电阻（如 100），默认不加
      --json <JSON>      把完整结果（含波形）写成 JSON
      --spice <SPICE>    每根网络写一份 ngspice 网表（.cir）和自己算的波形（.json）到这个文件夹
      --xtalk            再算串扰：同层平行走的别的网络（场求解器算耦合），攻击线跳变、受害线保持低电平，报近端 / 远端
      --png <PNG>        出波形图 PNG：每根网络一格（驱动灰线、各接收端彩线、稳态电平虚线），串扰每根受害线一格
      --lib <LIB>        元件库文件夹（找器件绑的 IBIS：part.toml 的 [sim] ibis；只这一次；默认依次看环境变量 EASYEDATOOL_LIB、工程旁边的 easyedatool.toml、本机配置）
      --corner <CORNER>  IBIS 用哪一列：typ（默认）、min（慢、弱）、max（快、强）
      --no-ibis          不用 IBIS，全部按通用模型
  -h, --help             Print help
```

## ibis

```
读 IBIS 模型文件（.ibs）：列出器件、引脚、模型选择器和模型（类型、电源、C_comp、有哪些表），每个能驱动的模型把自己的 V–T 波形放回测它时的夹具里重算、和表比（模型自洽、本工具读得对的检查；差超过幅度 10 % 退出码 1）

Usage: easyedatool ibis [OPTIONS] <FILE>

Arguments:
  <FILE>  IBIS 文件

Options:
      --component <COMPONENT>  只看这个器件（[Component] 名）
      --no-drc                 改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --model <MODEL>          只看这个模型（[Model] 名）
      --corner <CORNER>        用哪一列：typ（默认）、min（慢、弱）、max（快、强） [default: typ]
      --json <JSON>            把波形复算结果写成 JSON
  -h, --help                   Print help
```

## smps

```
开关电源版图检查：热回路（照实际铜走的路径算三维回路面积、估电感）、开关节点的铜皮和过孔、FB 这类安静网络离开关节点多远 / 有没有在相邻层压着它 / 从电感底下走、芯片去耦电容的铜路径和地回路；规则文件 [smps] 写电源，不写就自动认（有原理图按引脚名 SW / VIN / FB / BOOT，没有按连接：电感接芯片是降压 / 升压，一颗芯片几路的每路用自己的输入脚；变压器接 MOS 管或内置开关管的芯片是反激，顺着栅极找控制芯片）（超了退出码 1）

Usage: easyedatool smps [OPTIONS] <INPUT>

Arguments:
  <INPUT>  工程文件夹、.eprj3 工程索引或 .epcb2；PADS .asc、Altium .PcbDoc 直接读

Options:
      --no-drc         改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --rules <RULES>  规则文件（TOML，和布线共用）的 [smps] 表：[[smps.converter]] 每路电源（loops 热回路：器件和网络轮流写）、限值
      --suggest        把自动认出的电源按规则文件的写法打出来（核对后贴进规则文件）
      --png <PNG>      出 PNG：分层图上画热回路（面积着色）、开关节点和安静网络高亮；每路电源再出一张放大图（<名>_1.png …）
      --json <JSON>    把完整结果写成 JSON
  -h, --help           Print help
```

## label

```
成品板加丝印：照标注文件（TOML）往布好线的板子上加丝印字——自由文字、器件旁边的名字（接口是干什么的）、每个脚旁边的信号名（排针、端子）；只加丝印字，铜皮和别的都不动，不用重新生成、重新布线；字自己找不压焊盘、不压别的丝印、不出板边的地方，放不下就缩小（不小于 min_size）或换一边，还放不下的报出来；再跑一遍替换上次加的（记在工程的 .easyedatool/labels.json）；有 [designators] 时连器件位号一起整理：原地不挡着的留下，压焊盘（板厂会削掉）或压别的丝印的挪到器件旁最近的空处、放不下缩小、再不行不印（hide = false 则照旧并报出来），挪过去的位号必须离自己的器件最近，免得认错；默认只报告，--write 写回

Usage: easyedatool label [OPTIONS] --from <FROM> <INPUT>

Arguments:
  <INPUT>  .epcb2 文件、.eprj3 工程索引或工程文件夹

Options:
      --from <FROM>  标注文件（TOML，毫米）：size、min_size、rename，[[text]]、[[part]]、[[pins]]，[designators]（size、min_size、stroke、hide、reach、skip、only 只印哪些如 U*、J*、min_body 元件够大才印）
      --no-drc       改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --write        写回 .epcb2（先 git 提交；嘉立创开着这个工程时先关掉这块 PCB 的页面）
  -h, --help         Print help
```

## widen

```
电源线加粗：布线后把电源网络逐段加到放得下的最粗（先试目标线宽，再 0.4、0.3 mm），细间距焊盘旁边放不下的保持原样（颈缩）；按工程间距规则查别的网络，默认只报告，--write 写回（之后 pour --write 重算铺铜）

Usage: easyedatool widen [OPTIONS] <INPUT>

Arguments:
  <INPUT>  工程（文件夹、.eprj3 或 .epcb2）

Options:
      --no-drc         改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --rules <RULES>  布线规则（TOML）：[nets] power 是要加粗的网络，power_track 是目标线宽
      --net <NET>      要加粗的网络（可以给几次；给了就不用规则里的 power）
      --width <WIDTH>  目标线宽（mm；默认规则的 power_track，没给规则 0.5）
      --write          写回 .epcb2（嘉立创开着这个工程时先关掉这块 PCB 的页面，写完再打开）
  -h, --help           Print help
```

## tune

```
绕等长：在网络的直线段上加蛇形线补长度——差分对里短的那根补到另一根、等长组里超出容差的补到最长那根、一根网络补到指定长度；只在按工程间距规则放得下的地方绕，默认只报告，--write 写回

Usage: easyedatool tune [OPTIONS] <INPUT>

Arguments:
  <INPUT>  工程（文件夹、.eprj3 或 .epcb2）

Options:
      --no-drc                 改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --pair <PAIR>            差分对（名字，可以给几次）：短的那根补到和另一根一样长
      --group <GROUP>          等长组（名字，可以给几次）：比最长那根短过容差的网络补到最长那根减去容差的四分之一
      --net <NET>              一根网络，补到 --length
      --length <LENGTH>        --net 要补到的长度（mm）
      --all                    所有对内长度差超出的差分对、有网络超出容差的等长组都补
      --amplitude <AMPLITUDE>  蛇形线最高多高（mm；默认 1，差分对里的那根默认 2 倍的线宽加线距）
      --spacing <SPACING>      蛇形线相邻两段的间隔（mm，边到边；默认线宽的 3 倍）
      --write                  写回 .epcb2（先 git 提交；嘉立创开着这个工程时先关掉，写完再打开；铺铜要在嘉立创里重建）
  -h, --help                   Print help
```

## impedance

```
阻抗：按工程的叠层（层管理器里的厚度、介电常数）照嘉立创阻抗计算器的公式和取法算（和它算的逐位一致）：列叠层，每层单端 / 差分要多宽的线、给定线宽的阻抗，每对差分线按实际走线的差分阻抗

Usage: easyedatool impedance [OPTIONS] <INPUT>

Arguments:
  <INPUT>  工程（文件夹、.eprj3 或 .epcb2），或 PADS .asc

Options:
      --layer <LAYER>            只算这一层：1 顶层、2 底层、15 内层1……
      --no-drc                   改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --z0 <Z0>                  单端目标阻抗（Ω），算每层的线宽 [default: 50]
      --zdiff <ZDIFF>            差分目标阻抗（Ω），和 --gap 一起算每层的线宽；也用来标出差分对偏了多少
      --gap <GAP>                差分线距（mm）
      --width <WIDTH>            给定线宽（mm）算阻抗，加 --gap 算差分
      --top-ref <TOP_REF>        上参考层（层号，none 为没有；默认上面相邻的铜层，和嘉立创一样）
      --bottom-ref <BOTTOM_REF>  下参考层（层号，none 为没有；默认下面相邻的铜层）
      --stackup <STACKUP>        用嘉立创层管理器里的立创标准叠层代替工程的叠层来算（list 列出有哪些）；或者给规则文件（.toml），用它的 [stackup]（板厂叠层单：各层厚度、介电常数、阻焊、蚀刻梯形）
      --field                    再用二维场求解器算一遍（嘉立创公式算不了的内层、混合介电常数也能算；外层带阻焊；每层几秒）
      --json <JSON>              全部结果写成 JSON
  -h, --help                     Print help
```

## constraints

```
差分对、等长组、网络类和它们的规则：列出工程里的（每对的走线长度和对内长度差、每组的长度差），--auto 按网络名认差分对（规则按已布走线量出的线宽和间距），--from 从约束文件加，--write 写进工程

Usage: easyedatool constraints [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .epcb2 文件、.eprj3 工程索引或工程文件夹

Options:
      --auto         按网络名认差分对（DP/DM、P/N、+/-，后面可以跟 _A、数字这类短后缀），规则按已布走线量出的线宽和间距
      --no-drc       改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --from <FROM>  约束文件（TOML，mm）：[[pair_rule]] [[pair]] [[length_rule]] [[group]] [classes]，同名的替换工程里的
      --write        写进工程的 .epcb2（会改写文件：先 git 提交；嘉立创开着这个工程时先关掉这块 PCB 的页面，写完再打开，工程索引里这一页的版本号会跟着更新，嘉立创才重新读）
      --json <JSON>  按嘉立创 DRC 口径检查的全部结果写成 JSON（线宽、间距、对内长度差、等长，mm）
  -h, --help         Print help
```

## orcad

```
导入 OrCAD Capture 原理图（.DSN）：摘要（每页的导线和网络名、器件、电源符号、跨页连接……看读得全不全）、网表 CSV；--out 转成嘉立创EDA工程（只有原理图），读回来和 OrCAD 网表逐脚自检

Usage: easyedatool orcad [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .DSN（或 .OLB 库）

Options:
      --json <JSON>        读到的全部内容写成 JSON（包括还没弄懂的字节，十六进制）
      --no-drc             改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --netlist <NETLIST>  网表写成 CSV（网络、位号、脚号）
      --out <OUT>          转成嘉立创EDA工程（文件夹工程 .eprj3，只有原理图），写到这个文件夹（要空文件夹，或上次导入的同名工程）
      --name <NAME>        工程名（默认用 --out 文件夹的名字：嘉立创按文件夹名认工程，两者最好一致）
  -h, --help               Print help
```

## altium

```
导入 Altium 原理图（.SchDoc，二进制或 ASCII 存的都行）：自己读（不用装 Altium），`--out` 转成嘉立创EDA工程（只有原理图），写完读回来和 Altium 的连接逐脚自检；没名字的网络照 Altium 起名（Net + 位号_脚号，和它的 PCB 一样）

Usage: easyedatool altium [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .SchDoc

Options:
      --netlist <NETLIST>  网表写成 CSV（网络、位号、脚号）
      --no-drc             改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
      --out <OUT>          转成嘉立创EDA工程（文件夹工程 .eprj3，只有原理图），写到这个文件夹（要空文件夹，或上次导入的同名工程）
      --name <NAME>        工程名（默认用 --out 文件夹的名字：嘉立创按文件夹名认工程，两者最好一致）
  -h, --help               Print help
```

## lib

```
公司元件库（PartsLib）：找库、列元件、查元件，按数据手册做新件（引脚表排符号、IPC-7351B 算封装、3D），给草稿分料号

Usage: easyedatool lib [OPTIONS] <COMMAND>

Commands:
  status   连的是哪个库（从哪找到的）、在哪个提交、有没有没提交的改动、比内部仓库领先 / 落后多少、元件数
  new      新建元件（草稿）：parts/_draft/<型号>/part.toml、符号定义 symbols/<型号>.toml 和空引脚表 .pins.csv、封装尺寸模板 footprints/<型号>.toml（注释写着数据手册上的字母）；照数据手册填完再 lib build
  import   导入 PADS 元件库（PADS Library Manager 导出的 ASCII：.p 器件类型、.c 原理图符号、.d PCB 封装；给文件或文件夹）：每个 PCB 封装成库里的封装，每个器件类型成一个草稿元件带符号（每个门一个单元，脚号、脚名、类型照器件类型），属性原样带过来
  link     本机默认用这个库：写进本机配置（Windows：%APPDATA%\easyedatool\config.toml）
  list     列出全部元件：料号（草稿没有）、型号、状态、符号、封装、立创编号
  search   找元件（走索引）：料号、型号、描述、分类、厂家、厂家型号、立创编号里都要有这几个词（不分大小写），再加上给了的条件
  index    数据库索引（库根目录的 index.sqlite，不进 git）：和文件对一遍（改过的重读、删了的去掉），报元件、符号、封装个数，元件用到库里却没有的、没有元件用的；平时每个命令都会先自己更新，不用手动跑
  build    按定义生成：符号（symbols/<名>.toml + 引脚表 .pins.csv，一个 unit 一个单元），写 symbols/<名>.json，出预览图到 preview/<元件>/
  check    入库前检查：字段齐不齐、符号脚和封装焊盘一一对应、焊盘间距和阻焊桥够不够嘉立创的工艺、丝印压没压焊盘、3D 和仿真文件在不在（有错误时退出码 1）
  compare  和立创的库元件对比：按 C 编号拉立创官方的符号、封装（嘉立创公开接口），逐脚比脚号和脚名、逐个比焊盘位置和大小，--model 再比 3D 外形
  pull     从立创拉元件：按 C 编号取立创库的符号、封装（转成嘉立创专业版，和嘉立创自己库里的一样）、3D 模型（STEP），建草稿 part.toml（厂家、型号、立创编号填好）；库里已有这个编号的不重复拉
  assign   给草稿分料号：写进 part.toml 的 pn（别的内容、注释不动），parts/_draft/<型号> 移到 parts/<料号>
  serve    企业版元件库服务器：内网网页和 HTTP 接口（GET 查、POST 改）。元件库的 git 仓库是唯一真相，服务器是唯一写的人：每次修改都校验后 git 提交，作者是登录的人。流程 草稿 → 待审（自动检查要过、要有 ERP 料号、规格书、分类（有分类表时要是表里的））→ 可用（按清单逐项审核；一个人的公司也要单独审一次，记成「自审」）；改可用的件要开新版本、重新审；停用不删；分类表 categories.csv 在网页「分类」页改
  user     元件库服务器的用户：加人（打印登录令牌，只显示这一次）、列出、重发令牌、删人；角色 viewer 只看、editor 编辑、reviewer 审核、admin 管理员
  help     Print this message or the help of the given subcommand(s)

Options:
      --lib <LIB>  元件库文件夹（只这一次；默认依次看环境变量 EASYEDATOOL_LIB、工程旁边的 easyedatool.toml、本机配置）
      --no-drc     改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
  -h, --help       Print help
```

## bom

```
原理图 BOM：CSV，列和嘉立创EDA导出的一样（Comment / Designator / Footprint / Supplier Part …），能直接传立创贴片

Usage: easyedatool bom [OPTIONS] <INPUT>

Arguments:
  <INPUT>  .eprj3 工程索引、工程文件夹或 .epcb2 文件

Options:
      --no-drc     改板子的命令（gen、route、pour --write、widen、tune、pair 的 --write）跑完不自动查 DRC（gen 也不查原理图 ERC 和接法）
  -o, --out <OUT>  输出文件（默认 <工程名>_bom.csv）
  -h, --help       Print help
```
