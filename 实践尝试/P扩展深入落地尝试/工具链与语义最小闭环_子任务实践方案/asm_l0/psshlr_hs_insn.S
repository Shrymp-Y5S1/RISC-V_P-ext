.option norvc
.text
.align 2
.globl test_psshlr_hs_insn

# 已按 P-ext-proposal 编码表固定 .insn 常量
test_psshlr_hs_insn:
    li a1, 0x7fff8000
    li a2, 1
    # P-ext-proposal: opcode=0x1b, funct3=0x2, funct7=0x5c
    .insn r 0x1b, 0x2, 0x5c, a0, a1, a2
    ret