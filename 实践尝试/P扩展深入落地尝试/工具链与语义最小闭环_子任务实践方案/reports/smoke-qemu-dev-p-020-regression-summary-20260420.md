# QEMU dev-p-020 回归结论（对比 dev-p-018）

日期: 2026-04-20

## 1. 构建信息

- 分支: `dev-p-020`
- 本地提交: `e9693f1`
- user 版本: `qemu-riscv64 version 10.2.91`
- system 版本: `QEMU emulator version 10.2.91`
- 构建根目录: `/home/shrymp/qemu-devp020-work`

## 2. GroupA 属性探测

探测报告:

- `reports/smoke-qemu-dev-p-018-groupA-system-probe-20260420-DEVP020.md`

关键结论（与 dev-p-018 一致）:

- `x-p` 属性可见且可被接受。
- `p` / `rvp` / `ext_p` 均不存在。

Quick Findings:

- `p property missing occurrences: 4`
- `rvp property missing occurrences: 2`
- `ext_p property missing occurrences: 2`
- `x-p property missing occurrences: 0`

## 3. first20 回归（x-p + vxsat）

执行口径:

- `QEMU_BIN=/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-riscv64`
- `QEMU_CPU=max,x-p=true`
- `CAPTURE_VXSAT=1`

产物:

- `actual/minset_first20_qemu_devp020_xp_vxsat_raw.csv`
- `actual/minset_first20_qemu_devp020_xp_vxsat.actual.json`
- `reports/diff-minset-first20-qemu-devp020-xp-vxsat.csv`
- `reports/diff-minset-first20-qemu-devp020-xp-vxsat-summary.md`

结果:

- `total=20`
- `pass=19`
- `fail=1`
- 唯一失败: `C0000015 / PSSHAR.HS`
  - `expected_rd=0x00000000`
  - `actual_rd=0xffffffff`

## 4. PSSHAR.HS 边界扫点复现

执行口径:

- sweep: `rs2=0xE0..0xFF`（共 32 条）
- `QEMU_BIN=/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-riscv64`
- `QEMU_CPU=max,x-p=true`

产物:

- `actual/psshar_hs_shift_sweep_xp_devp020_repro_raw.csv`
- `actual/psshar_hs_shift_sweep_xp_devp020_repro.actual.json`
- `reports/diff-psshar_hs_shift_sweep_xp_devp020_repro.csv`
- `reports/diff-psshar_hs_shift_sweep_xp_devp020_repro-summary.md`

结果:

- `total=32`
- `pass=16`
- `fail=16`
- 失败窗口固定在 `rs2=0xE0..0xEF`
  - `expected_rd=0x00000000`
  - `actual_rd=0xffffffff`
- `rs2=0xF0..0xFF` 与模型一致。

## 5. 与 dev-p-018 结果对比

直接 diff 对比:

- `reports/diff-minset-first20-qemu-devp018-xp-vxsat.csv`
  vs
  `reports/diff-minset-first20-qemu-devp020-xp-vxsat.csv`
- `reports/diff-psshar_hs_shift_sweep_xp_20260420.csv`
  vs
  `reports/diff-psshar_hs_shift_sweep_xp_devp020_repro.csv`

对比结果: 无差异（输出一致）。

## 6. 决策建议

建议可以发 issue，理由如下:

1. 差异在 `dev-p-018` 与 `dev-p-020` 上都可稳定复现。
2. 失败窗口已经最小化到确定区间（`rs2=0xE0..0xEF`）。
3. 已有一键复现入口和可直接粘贴的 issue 草稿。

建议在 issue 中同时给出两组提交信息:

- `dev-p-018` 本地提交: `9fc6899`
- `dev-p-020` 本地提交: `e9693f1`
