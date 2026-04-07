.option norvc
.text
.align 2
.globl test_pm2add_h_insn

# 已按 P-ext-proposal 编码表固定 .insn 常量
test_pm2add_h_insn:
    li a1, 0x00010002
    li a2, 0x00030004
    # P-ext-proposal: opcode=0x3b, funct3=0x5, funct7=0x40
    .insn r 0x3b, 0x5, 0x40, a0, a1, a2
    ret
