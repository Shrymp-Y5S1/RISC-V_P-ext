# 工具链与语义最小闭环 - 开工入口

本目录用于落地 P 扩展最小闭环，目标是在 2~3 周内形成可复现的编译、语义、对拍链路。

## 目录说明

- version-lock.md: 版本锁定页
- asm_l0/: L0 路径，.insn 手工编码样例
- asm_l1/: L1 路径，助记符可达性样例
- model/: 黄金语义模型
- cases/: 测试输入
- expected/: 黄金模型输出
- actual/: 执行环境实际输出
- scripts/: 生成、评估、差分脚本
- reports/: 对拍结果与归因报告

## 首周最小执行步骤

1. 填写 version-lock.md。
2. 在 WSL2 中执行 asm_l0/ 的最小子集 10 条指令编译与 objdump 冒烟。
3. 运行 scripts/gen_cases.py 生成 cases。
4. 运行 scripts/model_eval.py 生成 expected。
5. 从 ISS 或 DUT 导出 actual。
6. 运行 scripts/diff.py 生成 reports/diff-week1.csv。

## WSL2 建议口径

已知你当前安装过:
- gcc-riscv64-linux-gnu
- qemu-user-static

建议在 WSL2 内优先使用:
- riscv64-linux-gnu-gcc
- riscv64-linux-gnu-objdump

L0 冒烟可直接运行:

bash scripts/wsl_l0_smoke.sh

L1 助记符冒烟（默认 clang 口径，自动优先 clang-22）:

bash scripts/wsl_l1_smoke.sh

如需对照 GNU 口径（预期会出现助记符不识别）:

L1_TOOLCHAIN=gnu bash scripts/wsl_l1_smoke.sh

如需在已知差异下继续推进回归（将 `psshlr.hs` 记为 GAP，不阻塞退出）:

L1_ALLOW_KNOWN_GAPS=1 CLANG_BIN=clang-22 bash scripts/wsl_l1_smoke.sh

说明:
- `scripts/wsl_l1_smoke.sh` 在 clang 模式会先探测 `experimental-p` 能力，并自动识别本地 `p` 版本号。
- 若本地 clang 构建未包含该能力，脚本会快速失败并给出提示，避免误判为样例语法问题。
- 当前 LLVM22 (`p 0.18`) 实测结果: 最小子集 10 条中 9 条可编译，`psshlr.hs` 仍未被识别。
- 补充同族探针结果（clang-22, `rv64i_p0p18`）: `pssha.hs` / `psshar.hs` 可识别，`psshl.hs` / `psshlr.hs` 不可识别。

语义闭环（WSL2）建议运行:

bash scripts/wsl_run_minset.sh

## 推荐命令

WSL2 (python3):

python3 scripts/gen_cases.py --out cases/minset_seed_1_7_42_20260405.json --seeds 1,7,42,20260405 --random-per-seed 200
python3 scripts/model_eval.py --cases cases/minset_seed_1_7_42_20260405.json --out expected/minset_seed_1_7_42_20260405.expected.json
python3 scripts/diff.py --expected expected/minset_seed_1_7_42_20260405.expected.json --actual actual/minset_seed_1_7_42_20260405.actual.json --out reports/diff-minset.csv

Windows PowerShell:

python scripts/gen_cases.py --out cases/week1_seed20260405.json --seeds 20260405 --random-per-seed 200
python scripts/model_eval.py --cases cases/week1_seed20260405.json --out expected/week1_seed20260405.expected.json
python scripts/diff.py --expected expected/week1_seed20260405.expected.json --actual actual/week1_seed20260405.actual.json --out reports/diff-week1.csv

## T5/T6 快速推进（推荐）

1. 导出给 ISS/DUT 的执行子集（先跑 20 条）：

python3 scripts/export_iss_cases.py --cases cases/minset_seed_1_7_42_20260405.json --out-json cases/minset_first20_for_iss.json --out-csv cases/minset_first20_for_iss.csv --out-raw-template actual/minset_first20_raw_template.csv --start 0 --limit 20

2. 将 ISS/DUT 原始日志转换为 actual（支持 json/csv/txt）：

python3 scripts/build_actual_from_raw.py --raw actual/minset_first20_raw.csv --out actual/minset_first20.actual.json

3. 为 first20 输入生成对应 expected：

python3 scripts/model_eval.py --cases cases/minset_first20_for_iss.json --out expected/minset_first20_for_iss.expected.json

4. 执行差分并生成归因摘要：

python3 scripts/diff.py --expected expected/minset_first20_for_iss.expected.json --actual actual/minset_first20.actual.json --out reports/diff-minset-first20.csv
python3 scripts/summarize_diff.py --diff reports/diff-minset-first20.csv --out reports/diff-minset-first20-summary.md

5. WSL 一键闭环可直接接 raw 输入：

ACTUAL_RAW_IN=actual/minset_first20_raw.csv ACTUAL_IN=actual/minset_first20.actual.json DIFF_OUT=reports/diff-minset-first20.csv DIFF_SUMMARY_OUT=reports/diff-minset-first20-summary.md bash scripts/wsl_run_minset.sh

## WSL2 QEMU 路径实测

已新增 qemu 执行脚本：

- python3 scripts/run_qemu_cases.py --cases cases/minset_first20_for_iss.json --out-raw actual/minset_first20_qemu_raw.csv --out-actual actual/minset_first20_qemu.actual.json
- bash scripts/wsl_qemu_first20.sh

本机实测结果（2026-04-08）：

- qemu: `/usr/bin/qemu-riscv64-static`（8.2.2）
- first20 结果：`status[ILLEGAL_INSN]=20`
- diff: `pass=0, fail=20`，归因为 `CONFIG_MISMATCH`

结论：当前 WSL2 自带 qemu-user 路径可用于输出阻塞证据，但不能产出有效 `actual_rd`（P 指令执行即非法指令）。

## v0.18 参考实现链（2026-04-08 新增）

根据 `riscv/riscv-p-spec` 的 Links 小节，当前可用参考链路为：

- John Hauser draft: https://www.jhauser.us/RISCV/ext-P/
- v0.18 gcc: https://github.com/ruyisdk/riscv-gcc/tree/p-dev
- v0.18 binutils: https://github.com/ruyisdk/riscv-binutils/tree/p-dev
- v0.18 intrinsics (WIP): https://github.com/topperc/p-ext-intrinsics
- v0.18 qemu: https://github.com/mollybuild/qemu/tree/dev-p-018

这组线索与当前阻塞高度相关：

1. 我们当前 `/usr/bin/qemu-riscv64-static`（8.2.2）不支持本 P 子集执行（first20 为 `ILLEGAL_INSN` 20/20）。
2. 可优先尝试将 `QEMU_BIN` 切到 `dev-p-018` 构建产物后复跑：

```bash
QEMU_BIN=/path/to/dev-p-018/build/qemu-riscv64 bash scripts/wsl_qemu_first20.sh
```

3. 若切换后出现可执行样例（`status[OK] > 0`），即可沿现有链路直接进入真实 T5/T6 对拍，不需改脚本：

```bash
python3 scripts/build_actual_from_raw.py --raw actual/minset_first20_qemu_raw.csv --out actual/minset_first20_qemu.actual.json
python3 scripts/diff.py --expected expected/minset_first20_for_iss.expected.json --actual actual/minset_first20_qemu.actual.json --out reports/diff-minset-first20-qemu.csv
python3 scripts/summarize_diff.py --diff reports/diff-minset-first20-qemu.csv --out reports/diff-minset-first20-qemu-summary.md
```

## x-p 口径推进更新（2026-04-20）

在 `dev-p-018` 上完成组A后，继续将 first20 切到 `x-p` 口径并补齐 `vxsat` 采集：

```bash
QEMU_BIN=/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64 \
QEMU_CPU=max,x-p=true \
CAPTURE_VXSAT=1 \
RAW_OUT=actual/minset_first20_qemu_devp018_xp_vxsat_raw.csv \
ACTUAL_OUT=actual/minset_first20_qemu_devp018_xp_vxsat.actual.json \
DIFF_OUT=reports/diff-minset-first20-qemu-devp018-xp-vxsat.csv \
SUMMARY_OUT=reports/diff-minset-first20-qemu-devp018-xp-vxsat-summary.md \
bash scripts/wsl_qemu_first20.sh
```

结果（first20）：

- `status[OK]=20`
- `pass=19, fail=1`
- 唯一剩余差异：`C0000015 / PSSHAR.HS`（`expected_rd=0x00000000`, `actual_rd=0xffffffff`）

说明：

- 早先 `pass=13, fail=7` 的 6 条差异主要来自 `vxsat` 采集链路缺失（旧路径把 second word 固定写 0）。
- 已新增 `scripts/wsl_probe_vxsat_once.sh` 用于单例验证 CSR `0x009` 读取；在饱和样例上可观测到 `probe_vxsat=1`。

## PSSHAR.HS 上游最小复现入口（2026-04-20）

针对当前唯一剩余差异（`C0000015 / PSSHAR.HS`），已补充“一键复现实验 + issue 草稿”。

1. 一键复现（默认使用 `x-p` + `vxsat` 采集）：

```bash
bash scripts/wsl_repro_psshar_hs_xp_issue.sh
```

默认输入与输出：

- 输入样例：`cases/psshar_hs_shift_sweep_xp_20260420.json`（`rs2=0xE0..0xFF`）
- 期望文件：`expected/psshar_hs_shift_sweep_xp_20260420.expected.json`
- diff 输出：`reports/diff-psshar_hs_shift_sweep_xp_repro.csv`
- 摘要输出：`reports/diff-psshar_hs_shift_sweep_xp_repro-summary.md`

2. 上游 issue 草稿（可直接粘贴）：

- `reports/upstream-issue-psshar-hs-xp-e0-ef-20260420.md`

当前观测窗口：

- `rs2=0xE0..0xEF`：模型期望 `0x00000000`，QEMU 返回 `0xffffffff`
- `rs2=0xF0..0xFF`：与模型一致

## dev-p-020 回归结论（2026-04-20）

已在 `dev-p-020` 分支完成同口径复测（`x-p + CAPTURE_VXSAT=1`），结果如下：

1. first20：`pass=19, fail=1`，唯一失败仍为 `C0000015 / PSSHAR.HS`。
2. PSSHAR 边界 sweep（`rs2=0xE0..0xFF`）：`pass=16, fail=16`，失败窗口仍是 `0xE0..0xEF`。
3. 与 `dev-p-018` 的 CSV 结果直接对比无差异。

结论：`dev-p-020` 未消除该窗口差异，可以据此继续发 issue。

详情见：

- `reports/smoke-qemu-dev-p-020-regression-summary-20260420.md`
