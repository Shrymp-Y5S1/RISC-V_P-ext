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
