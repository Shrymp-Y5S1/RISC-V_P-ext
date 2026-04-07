.option norvc
.text
.align 2
.globl test_psshar_hs_mnemonic

test_psshar_hs_mnemonic:
    li a1, 0x7fff8000
    li a2, -1
    psshar.hs a0, a1, a2
    ret
