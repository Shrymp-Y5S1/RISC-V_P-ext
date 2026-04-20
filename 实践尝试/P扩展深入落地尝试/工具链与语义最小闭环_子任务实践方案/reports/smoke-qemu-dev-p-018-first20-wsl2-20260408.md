# QEMU dev-p-018 first20 回归报告（WSL2）

日期: 2026-04-08  
范围: minset first20（PSADD.B/PSSUB.B/PSSHAR.HS）  
执行口径: WSL2 + rootless build（mollybuild/qemu dev-p-018）

## 1. 目标

在 WSL2 落地 `dev-p-018` qemu 构建，并用该二进制复跑 first20，验证是否能产出可用 `actual_rd`。

## 2. 构建信息

- 源仓: `https://github.com/mollybuild/qemu/tree/dev-p-018`
- 本地构建脚本: `scripts/wsl_build_qemu_devp018_rootless.sh`
- 构建产物: `/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64`
- 版本: `qemu-riscv64 version 10.2.91`
- 提交: `9fc6899`

## 3. first20 复跑（默认 CPU）

执行命令：

```bash
QEMU_BIN=/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64 \
RAW_OUT=actual/minset_first20_qemu_devp018_raw.csv \
ACTUAL_OUT=actual/minset_first20_qemu_devp018.actual.json \
DIFF_OUT=reports/diff-minset-first20-qemu-devp018.csv \
SUMMARY_OUT=reports/diff-minset-first20-qemu-devp018-summary.md \
bash scripts/wsl_qemu_first20.sh
```

结果：

- case_count: 20
- status: `ILLEGAL_INSN` 20/20
- diff: `pass=0`, `fail=20`
- attribution: `CONFIG_MISMATCH` 20/20
- 产物时间: 2026-04-08 09:22:02（本地）

## 4. CPU 参数补充探针

1. `QEMU_CPU=max`
   - 结果: `ILLEGAL_INSN` 19，`TIMEOUT` 1
   - diff: `pass=0`, `fail=20`

2. `QEMU_CPU=max,p=true`
   - 结果: `RUNTIME_FAIL` 20/20
   - 关键信息: `Property 'max-riscv-cpu.p' not found`

说明：`dev-p-018` 构建产物在当前运行口径下未暴露可直接启用的 `p` CPU 属性，且 first20 仍无法得到有效 `actual_rd`。

## 5. 关键证据文件

- `actual/minset_first20_qemu_devp018_raw.csv`
- `actual/minset_first20_qemu_devp018.actual.json`
- `reports/diff-minset-first20-qemu-devp018.csv`
- `reports/diff-minset-first20-qemu-devp018-summary.md`
- `actual/minset_first20_qemu_devp018_max_raw.csv`
- `actual/minset_first20_qemu_devp018_maxp_raw.csv`

## 6. 结论

1. 已完成 `dev-p-018` 在 WSL2 的可复现构建（rootless 方案）。
2. 使用该二进制复跑 first20 后，默认口径仍为 `ILLEGAL_INSN` 20/20。
3. 即使补充 CPU 参数探针，仍未得到可用 `actual_rd`；当前阶段该路径仍只能作为阻塞证据链。