# 失败归因记录

## 标签定义

- MODEL_BUG: 黄金模型实现错误
- IMPLEMENTATION_BUG: ISS 或 DUT 实现错误
- CONFIG_MISMATCH: 版本、参数、输入映射或观测口径不一致

## 记录模板

| 日期 | case_id | instr | 现象 | 初判标签 | 证据 | 处置动作 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-04-08 | C0000001~C0000020 | PSADD.B/PSSUB.B/PSSHAR.HS | qemu first20 全部 `ILLEGAL_INSN`，无可用 actual_rd | CONFIG_MISMATCH | actual/minset_first20_qemu_raw.csv；reports/diff-minset-first20-qemu.csv；reports/diff-minset-first20-qemu-summary.md；reports/smoke-qemu-first20-wsl2-20260408.md | 复现实验: `bash scripts/wsl_qemu_first20.sh`；保留 qemu 证据链；切换支持 P 的 ISS/DUT 产出真实 actual | CONFIRMED |
| 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | OPEN |

## 归因流程

1. 先比对输入映射和工具链参数，排除 CONFIG_MISMATCH。
2. 再用最小样例复跑黄金模型，确认是否复现。
3. 若黄金与规范不符，归为 MODEL_BUG；若黄金稳定且实现偏离，归为 IMPLEMENTATION_BUG。
4. 每个失败样例必须给出一次可复现实验命令。

## 自动化摘要

可先运行 `scripts/summarize_diff.py` 生成归因总览，再逐条回填本文件：

python3 scripts/summarize_diff.py --diff reports/diff-minset.csv --out reports/diff-minset-summary.md
