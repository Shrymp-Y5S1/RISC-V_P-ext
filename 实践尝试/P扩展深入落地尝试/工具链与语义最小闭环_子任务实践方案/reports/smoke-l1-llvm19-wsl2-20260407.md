# L1 助记符可达性 Smoke 报告（WSL2 + LLVM19）

日期: 2026-04-07  
范围: 最小子集 10 条 L1 助记符样例  
执行脚本: `scripts/wsl_l1_smoke.sh`（默认 clang19 模式）

## 1. 目标

验证安装 LLVM19 后，L1 助记符路径是否可达，并记录可复现证据。

## 2. 执行环境

- OS: Windows + WSL2 Ubuntu
- Kernel: 6.6.87.2-microsoft-standard-WSL2
- clang: Ubuntu clang version 19.1.1 (1ubuntu1~24.04.2)
- llvm-objdump: Ubuntu LLVM version 19.1.1

## 3. 执行命令

```bash
bash scripts/wsl_l1_smoke.sh
```

能力探针命令:

```bash
clang-19 --target=riscv64-unknown-elf --print-supported-extensions
```

## 4. 结果汇总

- 脚本执行结果: 失败（在能力探针阶段提前退出）
- 失败原因: clang19 未暴露 `experimental-p`（`p 0.21`）
- 10 条样例批量编译: 未进入（被探针保护逻辑阻断）

## 5. 关键输出

```text
ERROR clang toolchain does not expose experimental P extension (p 0.21).
HINT  Use a clang build that contains RISCV experimental-p support.
```

## 6. 结论与处置

1. 结论: Ubuntu 24.04 官方 `clang-19` 已安装，但该包构建不包含本实验所需的 `experimental-p` 能力。
2. 当前状态: L1 路径在该 LLVM19 口径下仍不可达；L0 `.insn` 路径继续可用。
3. 处置建议:
   - 使用包含 `experimental-p` 的 clang 构建（例如上游特定分支或自建 LLVM）。
   - 保留当前 `scripts/wsl_l1_smoke.sh` 探针逻辑，后续换编译器后二次复测即可。
