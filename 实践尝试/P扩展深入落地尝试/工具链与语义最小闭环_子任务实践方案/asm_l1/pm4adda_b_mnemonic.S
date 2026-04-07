.option norvc
.text
.align 2
.globl test_pm4adda_b_mnemonic

test_pm4adda_b_mnemonic:
    li a0, 0x00000010
    li a1, 0x01020304
    li a2, 0x04030201
    pm4adda.b a0, a1, a2
    ret