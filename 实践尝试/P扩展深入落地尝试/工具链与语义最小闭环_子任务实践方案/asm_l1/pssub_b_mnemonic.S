.option norvc
.text
.align 2
.globl test_pssub_b_mnemonic

test_pssub_b_mnemonic:
    li a1, 0x7f807f80
    li a2, 0x0101ff01
    pssub.b a0, a1, a2
    ret