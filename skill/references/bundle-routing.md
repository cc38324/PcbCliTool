# 整束布线

`bundle` 将多根网络作为一束共同规划，而非一根布完再让另一根找剩余通道。网络数不限于两根；可在一个计划中给出四对八线、五对十线或普通信号组。主干只有一条共同路径，各根按顺序向两侧偏移，转弯采用水平、垂直和45度线段，连续转角至少135度。

## 先预览再写入

```powershell
easyedatool gen examples/bundle-demo.toml --out out/bundle-demo/BundleDemo
easyedatool constraints out/bundle-demo/BundleDemo --from examples/bundle-demo.constraints.toml --write
easyedatool bundle out/bundle-demo/BundleDemo --plan examples/bundle-demo.json --json out/bundle-demo/preview.json
```

示例具有八个真实网络和四组差分约束，演示对内与对间不同间距，并不是可生产的HDMI电路。检查预览线路、过孔、实际长度和 `problems`。只有 `valid=true` 且输出“全部检查通过”，再给同一命令加 `--write`。一根失败则整束不写；一次编辑撤销整个线束。写后按项目要求补齐等长、重新铺铜，并运行带项目规则的 DRC。

## 计划

```json
{
  "lanes": [
    {"net":"SCL","from":"U1.1","to":"J1.1","width":0.2,"gap_after":0.2},
    {"net":"SDA","from":"U1.2","to":"J1.2","width":0.2}
  ],
  "layer": 1,
  "width": 0.2,
  "gap": 0.2,
  "grid": 0.05,
  "spine": [[10,10],[20,10],[25,15],[35,15]],
  "via": {"enabled":true,"diameter":0.5,"drill":0.3,"run_layer":2}
}
```

尺寸均为毫米，Y向上。`from`、`to`可为 `位号.脚号` 或精确坐标 `[x,y]`；使用焊盘时必须属于该网络，不会交换两端身份来绕过脚序冲突。沿主干起点看向终点，`lanes` 从左到右；向右前进时，列表第一根在最上方。主干角点吸附到 `grid`，每根偏移线路按真实几何保持间距，不再各自吸附破坏线距。

`gap_after` 是该根与列表下一根的主干铜边间距。它适合表示较小的差分对内间距和较大的对间间距；末根没有下一根。省略每根 `width`、`gap_after` 时用全局 `width`、`gap`。端部扇出须满足板上的安全间距及差分最小间距；连接器较小脚距不能保持较大的对间主干目标间距。

省略 `spine` 时由共同包络搜索主干；提供它时用作整束通道。`via.run_layer` 指定主干层，`layer`为端部层，允许在两端规划过孔扇出和脚序整理；这不是任意跨层线束的无条件可布承诺。过孔保持真实铜环、孔径、层跨度及所有层障碍，找不到安全路径会报告失败。

## 开放尾端与两端接近

有至少两个主干点时可省略 `to`，由主干末方向生成各网络的开放尾端。这样可以先从连接器成组引出，再从芯片一端接近，在预留区完成同网连接与必要换层。开放尾端仍保留网络身份；不得只按几何位置将近邻的另一网络接上。

`POST /api/edit/bundle` 接收同一计划并返回 `valid`、每根线路、过孔、主干、偏移、实际长度和问题；该接口不写工程。编辑器提交 `bundle_route` 操作，将所有网络、线路与过孔作为一个候选重新检查并一次写入；过期或有冲突的预览不能绕过最终校验。

规划器和编辑写入都会检查；预览成功不等于整板已连通、等长或阻抗已满足。两层板的实际阻抗、回流及换层区域仍应结合叠层和连接器布局审查。
