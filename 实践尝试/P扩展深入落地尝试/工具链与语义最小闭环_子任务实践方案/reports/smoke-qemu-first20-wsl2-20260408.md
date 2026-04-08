# QEMU first20 回归报告（WSL2）

日期: 2026-04-08  
范围: minset first20（PSADD.B/PSSUB.B/PSSHAR.HS）  
执行口径: WSL2 + qemu-riscv64-static

## 1. 目标

验证 qemu-user 路径是否可为 T5 提供可用 `actual_rd`，并输出可复现实证据。

## 2. 环境

- OS: Windows + WSL2 Ubuntu
- Kernel: 6.6.87.2-microsoft-standard-WSL2
- qemu: `qemu-riscv64 version 8.2.2 (Debian 1:8.2.2+ds-0ubuntu1.14)`
- gcc: `riscv64-linux-gnu-gcc 13.3.0`

## 3. 执行命令

```bash
bash scripts/wsl_qemu_first20.sh
```

脚本内部步骤:

1. `run_qemu_cases.py` 逐 case 生成 ELF 并调用 qemu 执行
2. `diff.py` 与 `expected/minset_first20_for_iss.expected.json` 对拍
3. `summarize_diff.py` 生成归因摘要

## 4. 结果

- 运行时间戳（本轮产物）: 2026-04-08 08:48:16（本地）
- case 总数: 20
- qemu 执行状态: `ILLEGAL_INSN` 20 / 20
- diff: `pass=0`, `fail=20`
- 归因: `CONFIG_MISMATCH` 20 / 20

## 5. 关键产物

- `actual/minset_first20_qemu_raw.csv`
- `actual/minset_first20_qemu.actual.json`
- `reports/diff-minset-first20-qemu.csv`
- `reports/diff-minset-first20-qemu-summary.md`

## 6. 结论

1. 当前 WSL2 qemu-user 路径可稳定复现“P 指令执行非法指令”现象。
2. 该路径可作为阻塞证据和回归探针，不可作为真实 `actual_rd` 采集来源。
3. T5 真正闭环仍需切换到支持 P 执行的 ISS/DUT。
