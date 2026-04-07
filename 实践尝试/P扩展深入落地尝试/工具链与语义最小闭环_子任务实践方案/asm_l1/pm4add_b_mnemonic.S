.option norvc
.text
.align 2
.globl test_pm4add_b_mnemonic

test_pm4add_b_mnemonic:
    li a1, 0x01020304
    li a2, 0x04030201
    pm4add.b a0, a1, a2
    ret