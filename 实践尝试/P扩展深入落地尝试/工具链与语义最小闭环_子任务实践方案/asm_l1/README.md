# L1 路径说明 (助记符)

目标: 验证工具链对 P 指令助记符的可达性。

注意事项:
1. 助记符样例用于可达性检查，不保证本地工具链一定支持。
2. 若汇编失败，请记录报错并回退到 L0 .insn 路径。
3. 建议保留失败日志到 reports/smoke-week1-template.md。

建议命令:
- clang --target=riscv32-unknown-elf -menable-experimental-extensions -march=<本地可用版本串> -mabi=ilp32 -c asm_l1/psadd_b_mnemonic.S -o build/psadd_b_mnemonic.o
