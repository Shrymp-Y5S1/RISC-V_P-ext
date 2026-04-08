# actual 目录说明

本目录存放 ISS 或 DUT 的实际执行结果。

## 建议格式

{
  "case_count": 2,
  "cases": [
    {
      "case_id": "C0000001",
      "actual_rd": 2139095040,
      "actual_vxsat": 1
    }
  ]
}

## 注意事项

1. case_id 必须与 expected 中完全一致。
2. actual_rd 支持十进制或十六进制字符串。
3. actual_vxsat 缺失时默认按 0 处理。

## 原始日志推荐格式

可直接提供为 csv/txt（每行 1 条）：

case_id,actual_rd,actual_vxsat
C0000001,0x81818181,0
C0000002,0x7f7f7f7f,1

也支持键值对文本：

case_id=C0000001 rd=0x81818181 vxsat=0

## 转换命令

也可先生成模板再填写：

python3 scripts/export_iss_cases.py --cases cases/minset_seed_1_7_42_20260405.json --out-json cases/minset_first20_for_iss.json --out-csv cases/minset_first20_for_iss.csv --out-raw-template actual/minset_first20_raw_template.csv --start 0 --limit 20

python3 scripts/build_actual_from_raw.py --raw actual/minset_first20_raw.csv --out actual/minset_first20.actual.json

转换后可直接用于：

python3 scripts/model_eval.py --cases cases/minset_first20_for_iss.json --out expected/minset_first20_for_iss.expected.json
python3 scripts/diff.py --expected expected/minset_first20_for_iss.expected.json --actual actual/minset_first20.actual.json --out reports/diff-minset-first20.csv
