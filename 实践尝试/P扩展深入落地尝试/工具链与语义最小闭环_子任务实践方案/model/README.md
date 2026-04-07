# 最小黄金语义模型说明

文件: p_semantics_min.py

## 已覆盖指令

- PSADD.B
- PSSUB.B
- PSSHAR.HS
- PSSHLR.HS
- PMULQ.H
- PMULQR.H
- PM2ADD.H
- PM2ADDA.H
- PM4ADD.B
- PM4ADDA.B

## 运行方式

- 自测:
  - python model/p_semantics_min.py --selftest
- 直接从 case 文件生成 expected:
  - python model/p_semantics_min.py --case-file cases/week1_seed20260405.json --out expected/week1_seed20260405.expected.json

## 口径说明

1. 本模型用于最小闭环验证，不替代官方 Sail 或任务组最终裁决语义。
2. 对舍入和 vxsat 的规则采用当前调研可执行口径，若后续草案更新需同步修订。
3. PM2/PM4 累加版按 32 位回绕处理，便于先完成对拍链路。
