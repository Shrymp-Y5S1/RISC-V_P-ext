.option norvc
.text
.align 2
.globl test_pmulq_h_mnemonic

test_pmulq_h_mnemonic:
    li a1, 0x7fff8000
    li a2, 0x40004000
    pmulq.h a0, a1, a2
    ret