.option norvc
.text
.align 2
.globl test_psadd_b_mnemonic

test_psadd_b_mnemonic:
    li a1, 0x7f807f80
    li a2, 0x01010101
    psadd.b a0, a1, a2
    ret
