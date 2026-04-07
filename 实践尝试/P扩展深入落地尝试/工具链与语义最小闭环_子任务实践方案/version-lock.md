# 版本锁定页

更新时间: 2026-04-07
维护人: 待填写

## 1. 规范版本

- P 扩展文档来源: riscv-p-spec/P-ext-proposal.adoc
- 文档快照日期: 待填写
- 文档关键锚点版本说明: working draft

## 2. 仓库与提交信息

- 主仓库 commit: 待填写
- 本目录相关分支: 待填写
- 子模块或外部快照: 无独立 git 元数据

## 3. 工具链版本

- riscv64-linux-gnu-gcc --version: 待填写
- riscv64-linux-gnu-as --version: 待填写
- riscv64-linux-gnu-objdump --version: 待填写
- clang --version: 待填写
- llvm-objdump --version: 待填写

## 4. 执行环境

- 操作系统: Windows 主机 + WSL2 Ubuntu
- 终端: PowerShell + WSL2
- Python 版本: 待填写

## 5. 关键命令快照

- L0 编译命令:
  - riscv64-linux-gnu-gcc -c asm_l0/psadd_b_insn.S -march=rv64gc -mabi=lp64d -o build/psadd_b_insn.o
  - riscv64-linux-gnu-objdump -d build/psadd_b_insn.o > build/psadd_b_insn.objdump
  - bash scripts/wsl_l0_smoke.sh
- L1 编译命令:
  - clang --target=riscv32-unknown-elf -menable-experimental-extensions -march=<待填写> -mabi=ilp32 -c asm_l1/psadd_b_mnemonic.S -o build/psadd_b_mnemonic.o
- 样例生成:
  - python scripts/gen_cases.py --out cases/week1_seed20260405.json --seeds 20260405 --random-per-seed 200
- 黄金评估:
  - python scripts/model_eval.py --cases cases/week1_seed20260405.json --out expected/week1_seed20260405.expected.json
- 差分命令:
  - python scripts/diff.py --expected expected/week1_seed20260405.expected.json --actual actual/week1_seed20260405.actual.json --out reports/diff-week1.csv

## 6. 版本变更记录

- 2026-04-07: 初始化版本锁定模板。
- 2026-04-07: 切换 L0 命令模板为 WSL2 的 riscv64-linux-gnu 工具链口径。
