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
