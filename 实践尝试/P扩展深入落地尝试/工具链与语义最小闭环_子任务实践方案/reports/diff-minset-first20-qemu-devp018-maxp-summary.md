# Diff 归因摘要

生成时间: 2026-04-08T01:23:45.350877+00:00
输入文件: reports/diff-minset-first20-qemu-devp018-maxp.csv

## 1. 汇总

- total: 20
- pass: 0
- fail: 20
- pass_rate: 0.00%
- fail_rate: 100.00%

## 2. 失败归因分布

| attribution | count |
| --- | ---: |
| CONFIG_MISMATCH | 20 |

## 3. 指令失败分布

| instr | fail_count |
| --- | ---: |
| PSADD.B | 7 |
| PSSUB.B | 7 |
| PSSHAR.HS | 6 |

## 4. 失败样例（前 20 条）

| case_id | instr | expected_rd | actual_rd | expected_vxsat | actual_vxsat | attribution |
| --- | --- | --- | --- | ---: | ---: | --- |
| C0000001 | PSADD.B | 0x81818181 |  | 0 | 0 | CONFIG_MISMATCH |
| C0000002 | PSADD.B | 0x7f7f7f7f |  | 1 | 0 | CONFIG_MISMATCH |
| C0000003 | PSADD.B | 0x00000000 |  | 0 | 0 | CONFIG_MISMATCH |
| C0000004 | PSADD.B | 0x7f7f7f7f |  | 1 | 0 | CONFIG_MISMATCH |
| C0000005 | PSADD.B | 0x00000000 |  | 0 | 0 | CONFIG_MISMATCH |
| C0000006 | PSADD.B | 0x7f7f7f7f |  | 1 | 0 | CONFIG_MISMATCH |
| C0000007 | PSADD.B | 0x80808080 |  | 1 | 0 | CONFIG_MISMATCH |
| C0000008 | PSSUB.B | 0x80808080 |  | 1 | 0 | CONFIG_MISMATCH |
| C0000009 | PSSUB.B | 0x7e7e7e7e |  | 0 | 0 | CONFIG_MISMATCH |
| C0000010 | PSSUB.B | 0xfefefefe |  | 0 | 0 | CONFIG_MISMATCH |
| C0000011 | PSSUB.B | 0x7c7c7c7c |  | 0 | 0 | CONFIG_MISMATCH |
| C0000012 | PSSUB.B | 0x00000000 |  | 0 | 0 | CONFIG_MISMATCH |
| C0000013 | PSSUB.B | 0x00000000 |  | 0 | 0 | CONFIG_MISMATCH |
| C0000014 | PSSUB.B | 0x00000000 |  | 0 | 0 | CONFIG_MISMATCH |
| C0000015 | PSSHAR.HS | 0x00000000 |  | 0 | 0 | CONFIG_MISMATCH |
| C0000016 | PSSHAR.HS | 0xffffffff |  | 0 | 0 | CONFIG_MISMATCH |
| C0000017 | PSSHAR.HS | 0xffffffff |  | 0 | 0 | CONFIG_MISMATCH |
| C0000018 | PSSHAR.HS | 0xc000c000 |  | 0 | 0 | CONFIG_MISMATCH |
| C0000019 | PSSHAR.HS | 0x80008000 |  | 0 | 0 | CONFIG_MISMATCH |
| C0000020 | PSSHAR.HS | 0x80008000 |  | 1 | 0 | CONFIG_MISMATCH |
