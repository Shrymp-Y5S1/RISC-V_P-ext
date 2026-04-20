# Diff 归因摘要

生成时间: 2026-04-20T11:15:16.857449+00:00
输入文件: reports/diff-minset-first20-qemu-devp018-xp.csv

## 1. 汇总

- total: 20
- pass: 13
- fail: 7
- pass_rate: 65.00%
- fail_rate: 35.00%

## 2. 失败归因分布

| attribution | count |
| --- | ---: |
| CONFIG_MISMATCH | 6 |
| IMPLEMENTATION_BUG | 1 |

## 3. 指令失败分布

| instr | fail_count |
| --- | ---: |
| PSADD.B | 4 |
| PSSHAR.HS | 2 |
| PSSUB.B | 1 |

## 4. 失败样例（前 20 条）

| case_id | instr | expected_rd | actual_rd | expected_vxsat | actual_vxsat | attribution |
| --- | --- | --- | --- | ---: | ---: | --- |
| C0000002 | PSADD.B | 0x7f7f7f7f | 0x7f7f7f7f | 1 | 0 | CONFIG_MISMATCH |
| C0000004 | PSADD.B | 0x7f7f7f7f | 0x7f7f7f7f | 1 | 0 | CONFIG_MISMATCH |
| C0000006 | PSADD.B | 0x7f7f7f7f | 0x7f7f7f7f | 1 | 0 | CONFIG_MISMATCH |
| C0000007 | PSADD.B | 0x80808080 | 0x80808080 | 1 | 0 | CONFIG_MISMATCH |
| C0000008 | PSSUB.B | 0x80808080 | 0x80808080 | 1 | 0 | CONFIG_MISMATCH |
| C0000015 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
| C0000020 | PSSHAR.HS | 0x80008000 | 0x80008000 | 1 | 0 | CONFIG_MISMATCH |
