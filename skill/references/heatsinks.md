# 散热器和机械件封装

封装与3D分别核对同一型号的机械尺寸。焊脚、安装孔和外形来自推荐安装图；底板、鳍片、安装高度来自三维图或尺寸图。照片可以辅助配色，不用于猜测孔距和精密尺寸。无需为无焊脚的机械件添加电气引脚。

## TO-220管用散热器：先找模型，再按截面图重建

这里包括MOS管、肖特基管背靠安装的型材散热器、冲压散热片和带固定针脚的散热器。TO-220是管子的封装类型，不能据此确定散热器外形、孔位或针脚；按实际厂家型号及规格找模型。用户只问获取渠道时，回答渠道和可用格式即可，不自行选择长度、制作某一款或扩展工具。

### 模型去哪里找

按厂家料号搜索，关键词可用`TO-220 heatsink STEP`、`extruded heatsink CAD`或「TO220 散热器 型材 截面图」，再补厂家、型号。淘宝等商品页主要用于确定采购规格，详情中没有3D时可向卖家索取原始STEP、DXF或带尺寸PDF。

| 渠道 | 找什么、怎么用 |
|------|----------------|
| 厂家官网、原厂CAD目录 | 优先取同一料号、长度、固定方式的机械图及3D；保留图纸版本和来源。 |
| [TraceParts的Fischer目录](https://www.traceparts.com/en/search/fischer-elektronik-gmbh-co-kg?CatalogPath=FISCHERELEKTRONIK) | 有型材散热器及TO-220用件。例如[SK 600系列](https://www.traceparts.com/en/product/fischer-elektronik-gmbh-co-kg-sk-600-35-x-254-mm-for-semiconductor-clipmounting-to-218-to-220-to-247-to-3-p?Product=90-27062019-043357)列出STEP、OBJ、STL、DXF等格式及不同长度、焊针/螺柱选项。按所选配置取文件；型号相近不代表与商品一致。 |
| [3D ContentCentral的TO-220散热器示例](https://www.3dcontentcentral.com/download-model.aspx?catalogid=171&id=686164) | 可查用户库中的型号和2D/3D下载；该示例下载需登录。用户上传模型应与采购图核对，不能当作原厂已确认数据。 |
| 立创/EasyEDA、KiCad元件库 | 找现成机械封装及配套模型；有立创编号可先试`lib pull`。KiCad入口见本文末尾。封装和3D可能只存在一项，不能把有封装说成有三维模型。 |

记录实际取得的文件、来源、型号和单位。网页有模型入口但未下载成功时，只能说找到入口；淘宝详情读不到时直接说明，实际制作需要的尺寸可从用户的图片或本地文件读取。下载模型与转换格式是两步，不把下载STEP说成本工具已经能直接载入。

### 厂家只给截面图时

1. 先区分恒截面型材和冲压/折弯件。恒截面型材可以沿长度拉伸；冲压件还需折弯和侧视尺寸。选定规格后记录截面宽高、底板/鳍片厚度、槽宽、圆角和切断长度，缺少的尺寸标为未核实。
2. 有DXF等矢量图时先核单位和比例；只有正投影位图时，以标注尺寸定标后描成封闭轮廓，并用其它已标尺寸复核。未标鳍片、圆角只能近似，不能声称是精确原厂CAD。截面不包含型材长度和后加工孔位，缺哪项就只补问实际制作需要的哪项。
3. 在支持草图拉伸与开孔的CAD软件中，沿选定长度拉伸，再按图加工管子固定孔、槽和安装结构。`M3`表示螺纹规格，不能直接当成直径3mm的光孔；针脚伸出长度不能当针脚直径。需要只画孔外形的近似模型时注明省略了螺纹。
4. 确定管子接触面、PCB平面、针脚伸出方向和离板高度，再导出三维模型；有需要时把管子、绝缘片等作为独立装配件。记录哪些尺寸来自标注，哪些是描图近似。

例如商品图同时列出截面宽32mm、20/25/30mm三档长度和有/无针脚款时，要分别理解这些配置；未选定款式前不把不同视图的孔位、针脚和长度混合成一件。该例只说明读图方法，尺寸不作为通用默认值。

### 放进本工具前核对什么

- 当前`model3d`仅能组合方块和圆柱，尚无任意截面拉伸、实体布尔开孔或DXF描图命令。复杂型材用外部CAD完成后，转为毫米OBJ并按工程`easyedatool.toml`的`[view3d.parts."位号"] model`绑定，变换字段见[参数模型说明](models-and-pads.md)。原厂STEP可以保留，整板渲染前仍须转换；简单组合可用参数配方。
- PCB封装单独定义投影占位、完整本体丝印、固定孔或可焊针脚；管子上的螺孔不一定穿PCB，不把3D里的所有孔都导出为PCB钻孔。无板上针脚或固定孔时可用下文的无焊盘机械封装。针脚是否导电、是否接网按实际结构决定。
- 成功下载或导出只说明文件得到；实际打开模型，核对总宽/长/高、安装孔距、针脚中心距与直径、板面高度及朝向，再与PCB封装叠加查看。实际精度未确认的部分继续标明，不能用外形相似代替同型号核对。

## 无焊盘机械件

```toml
[[footprints]]
name = "HEATSINK_DEMO_20"
designator = "HS"
mechanical = true
unit = "mm"
pads = []
outline = [-10, -10, 20, 20]
silk = [[[-10,-10],[10,-10],[10,10],[-10,10],[-10,-10]]]
```

`mechanical = true`显式允许没有焊盘的外形封装，`outline`必须是有限坐标和正数宽高，完整本体丝印仍保留。不写该标记的普通封装缺少焊盘仍报错。有安装孔或焊脚的散热器要按实物额外定义；安装孔是否镀铜、是否接地、是否开槽分别核实，不能从3D外观推断。机械标记不会自动生成螺孔、禁铜区或碰撞检查。

生成完整工程时，对应`[[symbols]]`也设置`mechanical = true`，允许无引脚的机械符号；器件`nets = {}`。普通电气符号仍拒绝空引脚。此处的符号与封装机械标记需分别声明。

可以实际运行的例子：

```powershell
easyedatool footprint examples/heatsink.toml --name HEATSINK_DEMO_20 -o heatsink-footprint.png
easyedatool gen examples/heatsink.toml --out build/HeatsinkDemo
easyedatool model3d bind build/HeatsinkDemo --recipe examples/models/heatsink20.toml --part HS1 --write
easyedatool render3d build/HeatsinkDemo -o heatsink-board.glb
easyedatool model3d export examples/models/heatsink20.toml -o heatsink.stl
```

应看到「机械封装：外形 20 × 20 mm，无电气焊盘」「参数模型绑定」「3D板厚…」。这个样例为胶粘式安装，无焊脚和孔；20×20×10mm、底板2mm、8条鳍片都是演示参数，不对应实际采购型号或散热性能。三维配方是底板和鳍片的方块组合，可以修改尺寸、数量及颜色。导出PNG、OBJ+MTL、GLB、STL、STEP后，查看实际图并核对外包尺寸和板面高度。

## 从尺寸图或网上库取得

1. 厂家机械图优先核对单位、孔心、孔径、焊脚位置和安装基准。现阶段可按带尺寸PDF/图片及已解析的CAD几何写设计文件。
2. 有立创编号时可用`lib pull`取库中已有的封装及模型，再对原厂图；没有对应库内容时按尺寸建封装。下载成功不代表型号、孔位和模型方向已核对。
3. 外部库如KiCad、厂家CAD目录可以提供封装或三维来源，先确认每项实际有文件，不能把网页上的“3D”入口当成已取得模型。KiCad原生封装、DWG和DXF目前没有直接导入命令，需解析/转换成工具支持的封装数据。
4. 整板渲染可以直接绑定毫米OBJ或本工具的参数配方。原厂STEP/IGES需先转换为OBJ；现有STEP是参数模型导出能力，不代表能够读取任意STEP。
5. 记录型号、图纸版本和来源；完整丝印、孔和焊脚保留，布局还须复查元件间距、铜/孔间距、禁布区及实际正反面模型。3D外观不代替热设计或装配验证。

现成库入口：[KiCad散热器封装](https://kicad.github.io/footprints/Heatsink.html)、[配套三维模型](https://kicad.github.io/packages3d/Heatsink.html)。例如AAVID 573300D00010G与Stonecold HS-132提供封装及STEP/WRL。并非每个封装都有模型，下载时逐个核对；这些外部格式仍按上述转换流程处理。
