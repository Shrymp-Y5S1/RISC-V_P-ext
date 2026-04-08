# L1 助记符可达性 Smoke 报告（WSL2 + LLVM22）

日期: 2026-04-08  
范围: 最小子集 10 条 L1 助记符样例  
执行脚本: scripts/wsl_l1_smoke.sh（clang 自动探测模式）

## 1. 目标

验证升级到 LLVM22 后，L1 助记符路径可达性是否提升，并记录阻塞点。

## 2. 执行环境

- OS: Windows + WSL2 Ubuntu
- Kernel: 6.6.87.2-microsoft-standard-WSL2
- clang: Ubuntu clang version 22.1.3 (++20260402073256+4250a0fc5de9-1~exp1~20260402073413.57)
- llvm-objdump: Ubuntu LLVM version 22.1.3

## 3. 执行命令

bash scripts/wsl_l1_smoke.sh

显式绑定 clang22:

CLANG_BIN=clang-22 bash scripts/wsl_l1_smoke.sh

## 4. 结果汇总

- 探针结果: 已识别 p 0.18
- 批量结果: 10 条中 9 条通过，1 条失败
- 失败项: asm_l1/psshlr_hs_mnemonic.S
- 失败类型: error: unrecognized instruction mnemonic, did you mean: psshar.hs?

## 5. 关键输出

L1 smoke toolchain: clang
L1 smoke clang bin: clang-22
L1 smoke detected P version: 0.18
...
FAIL psshlr_hs_mnemonic.S
asm_l1/psshlr_hs_mnemonic.S:9:5: error: unrecognized instruction mnemonic, did you mean: psshar.hs?
    psshlr.hs a0, a1, a2
SUMMARY total=10 pass=9 fail=1

## 6. 交叉验证

1. 使用 .insn 常量路径编译 psshlr 对应编码后，llvm-objdump 结果为 <unknown>。
2. 对照指令 psshar.hs 在同口径下可被 llvm-objdump 正常识别。
3. llvm-mc -mattr=+experimental-p 对 psshlr 相关助记符同样报 unrecognized。

## 7. 结论与处置

1. LLVM22（p0.18）已将 L1 可达性从 0/10 或 9/10 的历史阻塞中显著推进到 9/10。
2. 当前剩余问题是单指令版本差异（psshlr.hs）。
3. 建议后续按两条线并行：
   - 线A：保持 L0 .insn 主通道，继续语义闭环与 actual/diff 推进。
   - 线B：为 p0.18 建立“助记符兼容映射表”，将 psshlr.hs 标记为版本不兼容项并跟踪上游演进。
