# [ISSUE DRAFT] PSSHAR.HS mismatch on x-p path for rs2=0xE0..0xEF (dev-p-018)

## Summary

On `qemu-riscv64` from `mollybuild/qemu` branch `dev-p-018` (version `10.2.91`, commit `9fc6899`),
`PSSHAR.HS` shows a deterministic mismatch against the local reference model in the `x-p` execution path.

For test input `rs1=0x80008000` and `rs2 in [0xE0, 0xEF]`, expected result is `0x00000000`,
while QEMU returns `0xffffffff`.

Boundary check indicates `rs2=0xF0` and above match the model.

## Environment

- Host: WSL2 Ubuntu
- QEMU: `qemu-riscv64 version 10.2.91`
- QEMU source: `https://github.com/mollybuild/qemu/tree/dev-p-018`
- QEMU commit (local): `9fc6899`
- CPU argument: `-cpu max,x-p=true`

## Reproduction (one command)

From project root:

```bash
bash scripts/wsl_repro_psshar_hs_xp_issue.sh
```

The script runs:

1. `scripts/run_qemu_cases.py` on `cases/psshar_hs_shift_sweep_xp_20260420.json` (`rs2=0xE0..0xFF`)
2. `scripts/diff.py`
3. `scripts/summarize_diff.py`

Output files:

- `actual/psshar_hs_shift_sweep_xp_repro_raw.csv`
- `actual/psshar_hs_shift_sweep_xp_repro.actual.json`
- `reports/diff-psshar_hs_shift_sweep_xp_repro.csv`
- `reports/diff-psshar_hs_shift_sweep_xp_repro-summary.md`

## Observed vs Expected

Sweep range: `rs2=0xE0..0xFF` (`32` cases total)

- `rs2=0xE0..0xEF`: mismatch (`16` cases)
  - expected: `0x00000000`
  - actual: `0xffffffff`
- `rs2=0xF0..0xFF`: match (`16` cases)

Example failing row:

- `case_id=S0016`
- `instr=PSSHAR.HS`
- `rs1=0x80008000`
- `rs2=0x000000ef`
- `expected_rd=0x00000000`
- `actual_rd=0xffffffff`

## Extra context

This is currently the only remaining semantic mismatch in local first20 regression after enabling
`x-p` and capturing real `vxsat`.

first20 status (same environment):

- total `20`
- pass `19`
- fail `1`
- only failing case: `C0000015 / PSSHAR.HS`

## Requested clarification

Please confirm expected behavior for `PSSHAR.HS` on this input window:

- `rs1=0x80008000`
- `rs2=0xE0..0xEF`

and whether this should return `0x00000000` (model behavior) or `0xffffffff` (current QEMU behavior).
