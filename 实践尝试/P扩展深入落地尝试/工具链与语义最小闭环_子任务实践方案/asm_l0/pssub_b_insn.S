.option norvc
.text
.align 2
.globl test_pssub_b_insn

# 已按 P-ext-proposal 编码表固定 .insn 常量
test_pssub_b_insn:
    li a1, 0x7f807f80
    li a2, 0x0101ff01
    # P-ext-proposal: opcode=0x3b, funct3=0x0, funct7=0x6a
    .insn r 0x3b, 0x0, 0x6a, a0, a1, a2
    ret