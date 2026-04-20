# first20 x-p 失败归因与推进记录（2026-04-20）

## 1. 背景

在 `dev-p-018` + `x-p` 口径下，初次 first20 对拍结果为：

- `total=20, pass=13, fail=7`

其中失败分布：

- `CONFIG_MISMATCH=6`
- `IMPLEMENTATION_BUG=1`

## 2. 失败原因拆分

### 2.1 `CONFIG_MISMATCH=6` 的根因

这 6 条都满足：

- `actual_rd == expected_rd`
- `actual_vxsat == 0`，但 `expected_vxsat == 1`

根因不是执行语义，而是采样链路：旧版 `run_qemu_cases.py` 在汇报缓冲区第二个 64-bit 槽位固定写 0，没有从 CSR 读取 `vxsat`。

已通过单例探针验证可读取 `vxsat`：

- 脚本：`scripts/wsl_probe_vxsat_once.sh`
- 结果：`probe_rd=0x7f7f7f7f`, `probe_vxsat=1`

### 2.2 `IMPLEMENTATION_BUG=1` 的根因

剩余失败为：

- `C0000015 / PSSHAR.HS`
- `rs1=0x80008000, rs2=0xEF`
- `expected_rd=0x00000000`, `actual_rd=0xffffffff`

为确认是否单点偶发，新增边界扫点：

- 样例：`rs2=0xE0..0xFF`（共 32 条）
- 结果：`pass=16, fail=16`
- 失败窗口：`0xE0..0xEF` 全部失败，均表现为 `expected=0x00000000, actual=0xffffffff`

推断：`PSSHAR.HS` 在负大位移区域（至少 `shift <= -17`）存在实现偏差，行为更接近“在 `-16` 处钳住”而非模型当前定义。

## 3. 推进动作与结果

1. 已在执行器中新增可选 `vxsat` 采集能力：
   - `scripts/run_qemu_cases.py` 新增 `--capture-vxsat`
   - `scripts/wsl_qemu_first20.sh` 新增 `CAPTURE_VXSAT=1` 透传
2. 使用 `x-p + CAPTURE_VXSAT=1` 复跑 first20：
   - `total=20, pass=19, fail=1`
   - 仅保留 `C0000015` 一条真实语义差异

## 4. 关键产物

- first20（x-p，未采集 vxsat）
  - `reports/diff-minset-first20-qemu-devp018-xp-summary.md`
- first20（x-p，采集 vxsat）
  - `reports/diff-minset-first20-qemu-devp018-xp-vxsat-summary.md`
  - `reports/diff-minset-first20-qemu-devp018-xp-vxsat.csv`
- PSSHAR.HS 负位移扫点
  - `reports/diff-psshar_hs_shift_sweep_xp_20260420-summary.md`
  - `reports/diff-psshar_hs_shift_sweep_xp_20260420.csv`

## 5. 建议的后续推进

1. 以 `CAPTURE_VXSAT=1` 作为默认对拍口径，避免伪失败。
2. 将 `PSSHAR.HS(rs2 in 0xE0..0xEF)` 标记为已确认实现差异窗口，并单独跟踪。
3. 使用扫点产物直接准备上游 issue（最小复现可复用本报告中的 32 条 sweep）。