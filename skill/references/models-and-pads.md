# 参数模型和下载封装的焊盘修改

这些是通用命令，尺寸和位置都用毫米，旋转用度；模型尺寸、颜色、器件位号不写进工具源码。规格书尺寸用来建几何，照片只用于近似配色。不要从透视照片推断精密尺寸，也不要把组合外形叫作原厂CAD。

## 建一个电容模型

方块和圆柱按名称存入TOML配方。相同名称替换该实体，不同名称添加实体；可以逐个制作陶瓷、金属端头、圆柱外套、顶盖、底座及引脚。每个实体的`at`是XY中心和底部Z；先绕自身底部中心旋转，再平移。

```powershell
easyedatool model3d box cap.toml --name ceramic --size 0.50,0.50,0.50 --color '#B69B70' --source '规格书文件及页码，采用的尺寸和公差' --color-source '照片文件名，近似配色'
easyedatool model3d box cap.toml --name left --size 0.25,0.50,0.50 --at=-0.375,0,0 --color '#C8C8CA'
easyedatool model3d box cap.toml --name right --size 0.25,0.50,0.50 --at=0.375,0,0 --color '#C8C8CA'
easyedatool model3d color cap.toml --name ceramic --color '#AF9164' --source '实物照片近似取色，未测反射率'
easyedatool model3d export cap.toml -o cap.png
easyedatool model3d export cap.toml -o cap.glb
easyedatool model3d export cap.toml -o cap.stl
```

这组数字只是0402名义示例，不代表所有0402电容具有相同高度。圆柱的简单例子：`model3d cylinder can.toml --name sleeve --diameter 5 --height 5.4 --color '#202226'`。用不同名称继续加方块或圆柱；圆柱分段须为4到512的4的倍数。

成功应输出「参数模型已保存」「参数模型颜色已更新」或「参数模型已导出」，导出时同时打印外包尺寸和来源。支持PNG、OBJ+MTL、GLB、STL、STEP；GLB单位为米，其余几何文件为毫米，STL没有颜色。当前为加实体的组合，不做布尔挖孔、倒圆或复杂曲面。两个可以直接导出的配方在`examples/models/`。

## 用到板子上

```powershell
easyedatool model3d bind 工程 --recipe models/cap.toml --part C1 --part C2
easyedatool model3d bind 工程 --recipe models/cap.toml --part C1 --part C2 --write
easyedatool render3d 工程 -o board.glb --json scene.json
```

配方路径相对当前命令目录。配方在工程配置目录内时，绑定保存为相对路径；只修改`easyedatool.toml`的`[view3d.parts.位号] recipe`，不改焊盘、网络或共享库。默认试算，看到「参数模型绑定」后再加`--write`。配置中的`offset`、`rotation`、`alignment`仍可使用；默认在已验证的对称两端焊盘上居中，特殊件可明确指定`alignment="pads"`或`"library"`。

在Flutter 3D页点重新载入模型，实际查看正反面和方向。场景来源以`parametric:`开头，清单记录尺寸和配色依据，`exact=false`，不能拿导出成功当成尺寸验收。先确认模型朝向、脚距、外包尺寸、板面高度及正反面位置；没有规格来源的维度保持未核实。绑错位号先修配置，不挪电气焊盘来配合模型。

## 外部CAD、接线端子和不贴装器件

外部毫米OBJ可在工程`easyedatool.toml`绑定；尺寸未完全核实或采用兼容型号时显式标近似，不把存在网格当成已经与实物匹配：

```toml
[view3d.parts."J1"]
model = "models/connector.obj"
approximate = true
offset = [0, 0, 0]
rotation = [0, 0, 0]
alignment = "library"

[view3d.parts."R_DNP"]
hidden = true
```

两个字段默认false，也支持`[view3d.footprints."封装名"]`。`hidden`只从3D装配排除实体，输出「3D装配隐藏 N 个器件/标记：…；PCB焊盘和网络未修改」；恢复为false或去掉该覆盖可重新显示。依据当前BOM判断不贴装，导入板的器件Value可能全部为空，不能凭此隐藏；PCB本体丝印和孔仍保留。`approximate`仅把已载入外部CAD降为近似并说明匹配未核实，不改变模型几何，不能用false代替尺寸验收；参数配方始终标为简化模型。

接线端子先确认脚距、针数、板端/线端和插接方向，再找完整料号。例：[菲尼克斯MC 1,5/4-ST-3,5（1840382）](https://www.phoenixcontact.com/zh-cn/products/pcb-connector-mc-15-4-st-35-1840382)是4针线端插头，配套板端MC/MCV插座需要分别匹配；不能因为都是3.5mm脚距，就把4针插头或3.81mm型号装到8针PCB针座位置。

下载入口可查[菲尼克斯官方CAD门户](https://phoenix-contact.partcommunity.com/3d-cad-models/?info=phoenix_contact/27/27-46/27-46-02/27-46-02-02/1840382.prj)，或[KiCad的Connector_Phoenix_MC三维库](https://kicad.github.io/packages3d/Connector_Phoenix_MC.html)（MC水平、MCV垂直、不同针数/脚距的STEP及WRL）。未成功下载时只说找到入口；已取得文件还须转换为本工具可读的毫米OBJ，保留原始文件、来源和许可信息。模型对齐要核真实焊脚位置与离板高度，不能只让外包矩形居中。厂牌不同的兼容模型在尚未逐尺寸确认前设`approximate=true`。

## 加长、缩小下载的焊盘

输入是带`footprintDoc`的库封装JSON。`width`/`height`指焊盘自身旋转前的X/Y尺寸；`grow-x`/`grow-y`是总尺寸增量，负值缩小；`scale`同时缩放两轴，不能与其它尺寸参数混用。

```powershell
easyedatool pad-edit C0603.json --pad 1,2 --grow-x 0.10
easyedatool pad-edit C0603.json --pad 1,2 --grow-x 0.10 --name C0603_LONG --out C0603_LONG.json --preview pad-review
easyedatool pad-edit C0603.json --scale 0.9 --name C0603_SMALL --out C0603_SMALL.json
easyedatool pad-edit C0603.json --pad 1 --width 1.2 --height 0.7 --anchor left --out C0603_FIXED_LEFT.json
```

默认只试算，`--out`才写副本，禁止覆盖输入。副本使用按内容生成的新封装UUID，图元ID和脚号保留；指定新名称后可与原封装同时用于工程，避免两者被当作同一封装覆盖。脚号`*`表示全部，同号多个实体会一起修改。锚点固定焊盘的局部左/右/上/下边，旋转后仍沿正确方向变尺寸；有孔焊盘只支持中心锚点，钻孔位置及尺寸不变。支持RECT、OVAL、圆形；多边形和逐层独立焊盘拒绝处理，不能只改宽高伪装成功。

应看到「焊盘尺寸试算…通过」「封装副本已写入」，并逐脚打印实际尺寸。新短路、低于`--clearance`的间距恶化、焊环不足或新增丝印干涉时不输出副本。原有丝印问题会继续列明，不能称作已经交付。工具保留全部本体框、极性条、脚号、记录ID及孔、阻焊、钢网属性；不删丝印来消除冲突。打开`before.png`和`after.png`比较，再把副本用于工程；需要移动丝印时按完整外框和方向标记要求另行修改。

生成器工程也可永久记录项目内修正：

```toml
[[library_pad_patches]]
footprint = "库封装名称"
pad = "1"
width = 1.2
height = 0.7
```

这一项只改生成工程内嵌的封装，不改共享库。原有`hole_width`/`hole_height`仍是钻孔尺寸，不能与铜面尺寸混淆。已有板子的焊盘变小可能让原走线脱离，不能直接交生产；在副本中重新生成、核对逐脚网表、接线、间距、焊环和完整丝印，再导出生产文件。不要把测试副本的封装尺寸改回正式板，除非该尺寸修改本身已获授权。
