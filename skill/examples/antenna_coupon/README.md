# 四层天线流程示例

只验证安装后的原生求解与远场流程时，用同目录的 `smoke.toml`：`bin/easyedatool em examples/antenna_coupon --config examples/antenna_coupon/smoke.toml -o output/em-smoke --run`。它使用粗网格和 -30 dB 时间门槛，不是天线定版参数；本次执行完成但匹配目标未通过时，须如实保留这个结论。

30×20 mm 原生 EasyEDA Pro 工程，顶部7 mm为净空区，包含底部地参考和一个集总端口。它用于验证工具流程，尚未验证通道匹配、网格收敛或实物射频性能。

复制本目录后，在工具包根目录执行：

```powershell
bin/easyedatool em examples/antenna_coupon --config examples/antenna_coupon/antenna.toml -o output/antenna-em
```

出现「电磁模型已导出」「尚未求解」表示导出通过，不是仿真结果。追加 `--run` 使用工具包中的原生 openEMS；网格生成、求解、端口及远场处理均不需要 Python。完整工具包须包含 `runtime/openems`，不要只复制 `bin`。默认迭代预算只是起点，若短于激励或未达到时间收敛门槛，必须增加步数或核对网格，不能把预算耗尽认定为通过。

核对导出模型中的叠层、材料假设、端口、实际铜形及PCB哈希。端口两个横向边界须在馈线铜内部；不能把0.2 mm端口长度直接放在从y=11 mm起的铜线上并将中心设为11.1 mm，否则下边界恰好贴着金属边缘。当前长度为0.1 mm。

完整配置和验收步骤见 `references/antenna-em.md`。
