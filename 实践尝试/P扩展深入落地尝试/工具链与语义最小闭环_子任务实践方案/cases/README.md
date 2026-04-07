# cases 目录说明

本目录存放输入样例。

## 文件格式

推荐使用对象格式:

{
  "case_count": 2,
  "cases": [
    {
      "case_id": "C0000001",
      "instr": "PSADD.B",
      "rs1": 2139095040,
      "rs2": 16843009,
      "rd_in": 0,
      "kind": "boundary"
    }
  ]
}

## 生成方式

- python scripts/gen_cases.py --out cases/week1_seed20260405.json --seeds 20260405 --random-per-seed 200
