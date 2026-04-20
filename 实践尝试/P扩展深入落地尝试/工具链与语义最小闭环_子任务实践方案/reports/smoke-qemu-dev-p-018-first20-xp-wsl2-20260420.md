# QEMU dev-p-018 first20 回归报告（x-p 口径，WSL2）

日期: 2026-04-20  
范围: minset first20（PSADD.B / PSSUB.B / PSSHAR.HS）

## 1. 执行口径

- QEMU bin: /home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64
- QEMU CPU: max,x-p=true
- 入口脚本: scripts/wsl_qemu_first20.sh

## 2. 关键结果

- qemu 执行状态:
  - status[OK] = 20
  - 20/20 均产出 actual_rd（不再是 ILLEGAL_INSN）
- diff 对拍结果:
  - total = 20
  - pass = 13
  - fail = 7
  - pass_rate = 65.00%

## 3. 失败归因

- CONFIG_MISMATCH: 6
- IMPLEMENTATION_BUG: 1

注：失败主要体现在 vxsat 预期为 1 但实际为 0，以及 1 条 PSSHAR.HS 的 rd 结果差异。

## 4. 产物文件

- actual/minset_first20_qemu_devp018_xp_raw.csv
- actual/minset_first20_qemu_devp018_xp.actual.json
- reports/diff-minset-first20-qemu-devp018-xp.csv
- reports/diff-minset-first20-qemu-devp018-xp-summary.md

## 5. 结论

在 dev-p-018 的 x-p 口径下，first20 已可稳定执行并生成实际 actual_rd。下一步应将关注点从“是否可执行”转到“语义差异收敛”（尤其是 vxsat 与个别指令语义）。