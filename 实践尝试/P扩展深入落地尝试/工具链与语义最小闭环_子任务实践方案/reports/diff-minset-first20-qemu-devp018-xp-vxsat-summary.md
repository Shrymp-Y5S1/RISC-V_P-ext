# Diff 归因摘要

生成时间: 2026-04-20T11:32:42.142214+00:00
输入文件: reports/diff-minset-first20-qemu-devp018-xp-vxsat.csv

## 1. 汇总

- total: 20
- pass: 19
- fail: 1
- pass_rate: 95.00%
- fail_rate: 5.00%

## 2. 失败归因分布

| attribution | count |
| --- | ---: |
| IMPLEMENTATION_BUG | 1 |

## 3. 指令失败分布

| instr | fail_count |
| --- | ---: |
| PSSHAR.HS | 1 |

## 4. 失败样例（前 20 条）

| case_id | instr | expected_rd | actual_rd | expected_vxsat | actual_vxsat | attribution |
| --- | --- | --- | --- | ---: | ---: | --- |
| C0000015 | PSSHAR.HS | 0x00000000 | 0xffffffff | 0 | 0 | IMPLEMENTATION_BUG |
