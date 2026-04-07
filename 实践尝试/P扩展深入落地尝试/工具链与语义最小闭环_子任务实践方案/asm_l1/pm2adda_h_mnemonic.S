.option norvc
.text
.align 2
.globl test_pm2adda_h_mnemonic

test_pm2adda_h_mnemonic:
    li a0, 0x00010000
    li a1, 0x00010002
    li a2, 0x00030004
    pm2adda.h a0, a1, a2
    ret