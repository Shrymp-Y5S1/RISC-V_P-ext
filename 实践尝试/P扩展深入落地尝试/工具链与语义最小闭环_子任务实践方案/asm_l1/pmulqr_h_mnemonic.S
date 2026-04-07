.option norvc
.text
.align 2
.globl test_pmulqr_h_mnemonic

test_pmulqr_h_mnemonic:
    li a1, 0x7fff8000
    li a2, 0x40004000
    pmulqr.h a0, a1, a2
    ret
