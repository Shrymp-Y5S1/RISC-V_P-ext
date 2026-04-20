# 版本锁定页

更新时间: 2026-04-08
维护人: HP

## 1. 规范版本

- P 扩展文档来源: riscv-p-spec/P-ext-proposal.adoc
- 文档快照日期: 2026-04-07
- 文档关键锚点版本说明: working draft

补充（2026-04-08）:

- `riscv/riscv-p-spec` 的 Links 小节明确给出 v0.18 参考实现链。
- draft 参考入口: https://www.jhauser.us/RISCV/ext-P/
- v0.18 gcc: https://github.com/ruyisdk/riscv-gcc/tree/p-dev
- v0.18 binutils: https://github.com/ruyisdk/riscv-binutils/tree/p-dev
- v0.18 intrinsics (WIP): https://github.com/topperc/p-ext-intrinsics
- v0.18 qemu: https://github.com/mollybuild/qemu/tree/dev-p-018

## 2. 仓库与提交信息

- 主仓库 commit: e98bd80
- 本目录相关分支: main
- 子模块或外部快照: 无独立 git 元数据

## 3. 工具链版本

- riscv64-linux-gnu-gcc --version: riscv64-linux-gnu-gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0
- riscv64-linux-gnu-as --version: GNU assembler (GNU Binutils for Ubuntu) 2.42
- riscv64-linux-gnu-objdump --version: GNU objdump (GNU Binutils for Ubuntu) 2.42
- clang-19 --version: Ubuntu clang version 19.1.1 (1ubuntu1~24.04.2)
- /usr/lib/llvm-19/bin/llvm-objdump --version: Ubuntu LLVM version 19.1.1
- clang-19 experimental 扩展探针: `--print-supported-extensions` 未出现 `p 0.21`（当前 Ubuntu 包构建不含 experimental-p）
- clang-21 --version: Ubuntu clang version 21.1.8 (++20251221032922+2078da43e25a-1~exp1~20251221153059.70)
- /usr/lib/llvm-21/bin/llvm-objdump --version: Ubuntu LLVM version 21.1.8
- clang-21 experimental 扩展探针: `--print-supported-extensions` 出现 `p 0.14`
- clang-21 L1 助记符冒烟: `-march=rv64i_p0p14` 下最小子集 10 条仍全部 `unrecognized instruction mnemonic`
- clang-22 --version: Ubuntu clang version 22.1.3 (++20260402073256+4250a0fc5de9-1~exp1~20260402073413.57)
- /usr/lib/llvm-22/bin/llvm-objdump --version: Ubuntu LLVM version 22.1.3
- clang-22 experimental 扩展探针: `--print-supported-extensions` 出现 `p 0.18`
- clang-22 L1 助记符冒烟: 最小子集 10 条通过 9 条（仅 `psshlr.hs` 未识别）
- clang-22 同族助记符探针（HS 变体）: `pssha.hs` / `psshar.hs` 可识别，`psshl.hs` / `psshlr.hs` 不可识别
- qemu-riscv64-static --version: qemu-riscv64 version 8.2.2 (Debian 1:8.2.2+ds-0ubuntu1.14)
- qemu first20 执行: 20/20 `ILLEGAL_INSN`（P 子集在当前 qemu-user 路径不可执行）
- qemu first20 最新回归时间: 2026-04-08 08:48（本地）

## 4. 执行环境

- 操作系统: Windows 主机 + WSL2 Ubuntu (Linux kernel 6.6.87.2-microsoft-standard-WSL2)
- 终端: PowerShell + WSL2
- Python 版本: Python 3.12.3 (WSL2)

## 5. 关键命令快照

- L0 编译命令:
  - riscv64-linux-gnu-gcc -c asm_l0/psadd_b_insn.S -march=rv64gc -mabi=lp64d -o build/psadd_b_insn.o
  - riscv64-linux-gnu-objdump -d build/psadd_b_insn.o > build/psadd_b_insn.objdump
  - bash scripts/wsl_l0_smoke.sh
- L1 编译命令:
  - clang-22 --target=riscv64-unknown-elf -menable-experimental-extensions -march=rv64i_p0p18 -mabi=lp64 -c asm_l1/psadd_b_mnemonic.S -o build/psadd_b_mnemonic.o
  - bash scripts/wsl_l1_smoke.sh
  - CLANG_BIN=clang-22 bash scripts/wsl_l1_smoke.sh
  - L1_ALLOW_KNOWN_GAPS=1 CLANG_BIN=clang-22 bash scripts/wsl_l1_smoke.sh
  - L1_TOOLCHAIN=gnu bash scripts/wsl_l1_smoke.sh
- 样例生成:
  - python scripts/gen_cases.py --out cases/week1_seed20260405.json --seeds 20260405 --random-per-seed 200
- 黄金评估:
  - python scripts/model_eval.py --cases cases/week1_seed20260405.json --out expected/week1_seed20260405.expected.json
- 差分命令:
  - python scripts/diff.py --expected expected/week1_seed20260405.expected.json --actual actual/week1_seed20260405.actual.json --out reports/diff-week1.csv
  - bash scripts/wsl_qemu_first20.sh
  - 结果报告: reports/smoke-qemu-first20-wsl2-20260408.md

## 6. 版本变更记录

- 2026-04-07: 初始化版本锁定模板。
- 2026-04-07: 切换 L0 命令模板为 WSL2 的 riscv64-linux-gnu 工具链口径。
- 2026-04-07: 回填 WSL2 实机工具链版本、仓库 commit/branch 与 Python 版本。
- 2026-04-07: 新增 LLVM19 口径信息与能力探针结论（Ubuntu clang-19.1.1 未暴露 experimental-p）。
- 2026-04-08: 回填 LLVM21 安装与探针结果（支持 `p 0.14`，但 L1 最小子集助记符仍不可达）。
- 2026-04-08: 回填 LLVM22 安装与探针结果（支持 `p 0.18`，L1 最小子集提升至 9/10）。
- 2026-04-08: 新增 clang-22 同族助记符探针结论（`pssha/psshar` 可达，`psshl/psshlr` 不可达）与 known-gap 回归命令。
- 2026-04-08: 新增 qemu-user first20 实测（全部 `ILLEGAL_INSN`）与 qemu 路径 T5/T6 脚本证据。
- 2026-04-08: 新增 riscv-p-spec Links 的 v0.18 参考实现链记录（ruyisdk gcc/binutils p-dev，mollybuild qemu dev-p-018，topperc intrinsics）。
