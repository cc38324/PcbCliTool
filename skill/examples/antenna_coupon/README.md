# 四层天线流程示例

30×20 mm 原生 EasyEDA Pro 工程，顶部7 mm为净空区，包含底部地参考和一个集总端口。它用于验证工具流程，尚未验证通道匹配、网格收敛或实物射频性能。

复制本目录后，在工具包根目录执行：

```powershell
bin/easyedatool em examples/antenna_coupon --config examples/antenna_coupon/antenna.toml -o output/antenna-em
```

出现「电磁模型已导出」「尚未求解」表示导出通过，不是仿真结果。安装版本匹配的openEMS/CSXCAD及Python依赖后，通过配置的`python`、`solver_root`或CLI选项指定环境，再追加`--run`。求解器不随工具包安装。

核对导出模型中的叠层、材料假设、端口、实际铜形及PCB哈希。端口两个横向边界须在馈线铜内部；不能把0.2 mm端口长度直接放在从y=11 mm起的铜线上并将中心设为11.1 mm，否则下边界恰好贴着金属边缘。当前长度为0.1 mm。

完整配置、结果含义及验收步骤见工具包的`references/antenna-em.md`。源码使用者也可通过`cargo run --release --example antenna_coupon -- <新目录>`生成参数变体；生成器共用`examples/antenna.toml`并核对生成板与端口配置。
