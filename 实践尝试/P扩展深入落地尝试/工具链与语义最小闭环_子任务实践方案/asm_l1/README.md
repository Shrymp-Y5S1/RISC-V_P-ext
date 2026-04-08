# L1 路径说明 (助记符)

目标: 验证工具链对 P 指令助记符的可达性。

注意事项:
1. 最小子集 10 条助记符样例已补齐，用于可达性检查，不保证本地工具链一定支持。
2. `scripts/wsl_l1_smoke.sh` 默认使用 `clang`，自动优先 `clang-22` 并探测 `experimental-p` 与本地 `p` 版本号。
3. 若汇编失败，请记录报错并回退到 L0 .insn 路径。
4. 建议保留失败日志到 reports/smoke-week1-template.md。
5. LLVM22 (`p 0.18`) 下当前实测为 9/10 通过，`psshlr.hs` 报 `unrecognized instruction mnemonic`。

建议命令:
- bash scripts/wsl_l1_smoke.sh
- L1_TOOLCHAIN=gnu bash scripts/wsl_l1_smoke.sh
- CLANG_BIN=clang-22 CLANG_MABI=lp64 bash scripts/wsl_l1_smoke.sh
- CLANG_BIN=clang-22 CLANG_MARCH=rv64i_p0p18 CLANG_MABI=lp64 bash scripts/wsl_l1_smoke.sh
