# 和嘉立创EDA客户端配合

easyedatool 只读写磁盘上的工程文件（文件夹工程：`<名>.eprj3` 索引 + `sch/<原理图>/*.esch2` + `pcb/*.epcb2`）。用户的嘉立创EDA专业版客户端要是开着同一个工程，要注意下面这些。以下都是 2026-09-25 用桥实测的。

## EDA 什么时候重读文件

- EDA 开着工程时，页面内容有缓存。**重开页面（关掉再打开）时，只有索引里这一页的版本号（`.eprj3` 里 `profile.pcbs.<uuid>.version`，毫秒时间戳）比它手里那份新，才从磁盘重读**，不然还是缓存。
- `pour --write`、`route` 写完会把索引里这块 PCB 的版本号改成当前时间，所以重开 PCB 页就能看到新内容。`gen` 不改（它自己写索引，保证同一份设计生成的文件一模一样）。
- **关页面时 EDA 会把它自己记着的版本号写回索引**（还会重写 `sch/<原理图>/<原理图>.ecfg` 的文件头，内容不变）。所以顺序必须是：

```
1. EDA 里关掉 PCB 页（或者用 easyeda-api 桥：eda.dmt_EditorControl.closeDocument(tabId)）
2. 跑 easyedatool pour --write / route
3. EDA 里重新打开 PCB 页（桥：eda.dmt_EditorControl.openDocument(PCB 文档 uuid)）
```

  反过来（开着页面写、再关、再开）：关页时旧版本号被写回，重开还是旧内容。
  `constraints --write` 也会改索引版本号，顺序一样。
- **这招不总灵**：2026-09-30 在 M500C 上，嘉立创自己存过这一页（桥上 `pcb_Document.save()`）之后，关页 → 改文件、改版本号 → 开页，它一直用内存里那份。要确定嘉立创读的是磁盘上的新文件：请用户**关掉整个工程再打开**。核对时可以在文件里改一个看得见的值当标记（比如一条规则的数值），用桥读出来确认它真的重读了。
- EDA 里做了任何改动，几秒内会按它自己的格式把 PCB、索引等存回磁盘，会盖掉外面写的内容。所以写文件期间让用户别在 EDA 里改这块板。
- `gen` 整个换掉 sch/、pcb/：最好让用户先在 EDA 里关掉这个工程，生成完再打开。
- 不要用桥 `dmt_Project.openProject` 打开别的工程：会丢掉当前工程没保存的改动。
- 不要用 `sys_FileManager.setDocumentSource` 往开着的工程里灌源码：会丢线、合并记录。

## 用桥核对（用户说桥开着时）

easyeda-api skill 的桥在 `http://127.0.0.1:49620`–`49629`（`/health`、`/execute`）。本机要是设了 HTTP 代理，curl 加 `--noproxy '*'`，Python urllib 用空的 `ProxyHandler({})`。

- 看 EDA 开着哪个工程、哪一页：`eda.dmt_Project.getCurrentProjectInfo()`、`eda.dmt_SelectControl.getCurrentDocumentInfo()`。
- 看 EDA 现在用的铺铜填充：`(await eda.pcb_PrimitivePoured.getAll())` 每个的 `getState_PourPrimitiveId()`、`getState_PourFills()`（`fill: true` 是填充块，`false` 是辐条）。块数和条目 id 能看出是不是写进去的那份。
- EDA 自己的 DRC：`await eda.pcb_Drc.check(true, false, true)` 返回树 `[{name, list: [{name, list: [条目]}]}]`，条目的 `explanation.errData` 有 `minDistance`、`clearance`（单位 10 mil）、`position`、两个图元 id。铺铜的错误名是 `Copper Region(Filled) to …`。
- 截图：`eda.dmt_EditorControl.zoomTo(x_mil, y_mil, 比例)` 后 `getCurrentRenderedAreaImage()`（Blob，转 base64 带回来）。
- 核对完把工程恢复原样：`git checkout` 改过的文件；索引要让 EDA 重读就把版本号改成当前时间再开页；EDA 自己改过、没提交的文件先备份再恢复。

## 文件格式要点（别手改，知道就行）

- 每行一条记录：`{"type":..,"ticket":..,"id":..}||{内容}|`；按 `DOCHEAD` 分文档，最后一个 `PCB` 文档是板子本身，前面是内嵌的封装 / 符号 / 器件库。
- 删除记录 = 同 id、ticket 更大的空内容记录；同一记录可能有旧版本，取 ticket 最大的。
- PCB 单位 mil、y 向上；铺铜填充 `POURED` 单位 10 mil；原理图单位 10 mil、**y 向下**。
- 焊盘 `centerX/Y` 是铜皮的中心，`padOffsetX/Y` 是孔相对它的偏移（没有孔的焊盘嘉立创不理）；ELLIPSE 焊盘 EDA 画成小边长的圆。
- 铺铜轮廓（`POUR`）外圈必须顺时针并闭合，逆时针的整块被 EDA 丢掉；线宽文件里写毫米，EDA 按整 mil 用（0.2 → 0.2032）。
- 安全间距规则是 `RULE` 记录（`["RULE","SAFE",名字]`，`ruleState` DEFAULT），数值 mil；文件里有好几条 DEFAULT 时 EDA 用 ticket 最小（模板）那条。
- 封装里的过孔没有网络，EDA 按它压着的焊盘算网络。
- 差分对、等长组、网络类记在每个网络的 `NET` 记录上（`differentialName` / `isPositiveNet`、`equalLengthGroupName`、`netType`）；规则是 `["RULE","DIFFER_ENTAIL",名字]`、`["RULE","NET_LENGTH_TOLERANCE",名字]`（mil）。谁用哪条规则由 `RULE_SELECTOR` 定：`["DIFF_PAIR",对名]`、`["EQ_LEN_GRP",组名]`，**还有这对 / 这组每根网络的 `["NET",网络]`**——嘉立创给每个网络都建一条网络指定，加载时按文件顺序套、套之前先清回默认，网络的规则传给差分对 / 等长组、反过来不传，DRC 查网络上的规则。只写在对、组上，嘉立创按默认规则查（M500C 上实际发生过）。`constraints --write` 两处都写。值的写法：差分对规则是纯名字，等长规则是 `[名字, 目标网络]`。
