# expected 目录说明

本目录存放黄金语义模型输出。

## 生成方式

- python scripts/model_eval.py --cases cases/week1_seed20260405.json --out expected/week1_seed20260405.expected.json

## 关键字段

- expected_rd: 黄金期望寄存器值
- expected_vxsat: 黄金期望饱和标志
- expected_rd_hex: 可读十六进制格式
