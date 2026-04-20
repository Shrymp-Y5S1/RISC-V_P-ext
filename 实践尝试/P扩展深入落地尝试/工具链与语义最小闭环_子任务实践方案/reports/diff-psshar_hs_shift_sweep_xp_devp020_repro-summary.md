# Diff 归因摘要

生成时间: 2026-04-20T12:43:40.690576+00:00
输入文件: reports/diff-psshar_hs_shift_sweep_xp_devp020_repro.csv

## 1. 汇总

- total: 32
- pass: 16
- fail: 16
- pass_rate: 50.00%
- fail_rate: 50.00%

## 2. 失败归因分布

| attribution | count |
| --- | ---: |
| IMPLEMENTATION_BUG | 16 |

## 3. 指令失败分布

| instr | fail_count |
| --- | ---: |
| PSSHAR.HS | 16 |

## 4. 失败样例（前 20 条）

| case_id | instr | expected_rd | actual_rd | expected_vxsat | actual_vxsat | attribution |
| --- | --- | --- | --- | ---: | ---: | --- |
| S0001 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
| S0002 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
| S0003 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
| S0004 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
| S0005 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
| S0006 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
| S0007 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
| S0008 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
| S0009 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
| S0010 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
| S0011 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
| S0012 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
| S0013 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
| S0014 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
| S0015 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
| S0016 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
