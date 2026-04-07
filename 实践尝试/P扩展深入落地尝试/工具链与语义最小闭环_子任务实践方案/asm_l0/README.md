# L0 路径说明 (.insn)

目标: 在助记符不可用时，先打通编码、编译、反汇编路径。

注意事项:
1. 最小子集 10 条样例已按 P-ext-proposal 固定常量（含 week1 的 4 条 + 后续补齐的 6 条）。
2. 扩展其它指令时，请继续对照编码表填写 opcode/funct3/funct7。
3. 推荐每次只改一条指令并保存 objdump 结果。

建议命令:
- riscv64-linux-gnu-gcc -c asm_l0/psadd_b_insn.S -march=rv64gc -mabi=lp64d -o build/psadd_b_insn.o
- riscv64-linux-gnu-objdump -d build/psadd_b_insn.o > build/psadd_b_insn.objdump
- bash scripts/wsl_l0_smoke.sh
