# L1 助记符可达性 Smoke 报告（WSL2 + LLVM21）

日期: 2026-04-08  
范围: 最小子集 10 条 L1 助记符样例  
执行脚本: `scripts/wsl_l1_smoke.sh`（clang 自动探测模式）

## 1. 目标

验证安装 LLVM21 后，L1 助记符路径是否可达，并输出可复现证据。

## 2. 执行环境

- OS: Windows + WSL2 Ubuntu
- Kernel: 6.6.87.2-microsoft-standard-WSL2
- clang: Ubuntu clang version 21.1.8 (++20251221032922+2078da43e25a-1~exp1~20251221153059.70)
- llvm-objdump: Ubuntu LLVM version 21.1.8

## 3. 执行命令

```bash
bash scripts/wsl_l1_smoke.sh
```

探针命令:

```bash
clang-21 --target=riscv64-unknown-elf --print-supported-extensions
```

## 4. 结果汇总

- 探针结果: 已识别 `p 0.14`
- 脚本模式: clang 自动探测（选中 clang-21）
- 批量结果: 10/10 FAIL
- 失败类型: `error: unrecognized instruction mnemonic`

## 5. 关键输出

```text
L1 smoke toolchain: clang
L1 smoke clang bin: clang-21
L1 smoke detected P version: 0.14
FAIL psadd_b_mnemonic.S
asm_l1/psadd_b_mnemonic.S:9:5: error: unrecognized instruction mnemonic
    psadd.b a0, a1, a2
...
SUMMARY total=10 pass=0 fail=10
```

补充交叉验证（llvm-mc 直连后端）:

```text
/usr/lib/llvm-21/bin/llvm-mc -triple riscv64 -mattr=+experimental-p /tmp/p_test.s
/tmp/p_test.s:2:1: error: unrecognized instruction mnemonic
padd.b t5, s0, t1
/tmp/p_test.s:3:1: error: unrecognized instruction mnemonic
pm2add.h t3, t1, s0
```

补充交叉验证（march 组合）:

```text
rv64i_p0p14   -> unrecognized instruction mnemonic
rv64im_p0p14  -> unrecognized instruction mnemonic
rv64g_p0p14   -> unrecognized instruction mnemonic
rv64gc_p0p14  -> unrecognized instruction mnemonic
```

## 6. 结论与处置

1. LLVM21 已具备 experimental P 扩展入口（`p 0.14`），但当前实现与本实验的 10 条助记符集合不匹配。
2. L1 仍不可达；L0 `.insn` 路径继续可达且应保持主通道。
3. 下一步建议:
   - 维持 `scripts/wsl_l1_smoke.sh` 作为回归探针，持续验证后续工具链更新。
   - 在独立分支准备“LLVM p0.14 对应助记符子集”映射清单，避免把语法/版本差异误判为实现错误。
