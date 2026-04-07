import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List, Optional


def to_u32(value: int) -> int:
    return value & 0xFFFFFFFF


def parse_int(value) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        text = value.strip().lower()
        if text.startswith("0x"):
            return int(text, 16)
        if text == "":
            return None
        return int(text)
    raise ValueError(f"Unsupported int value: {value}")


def format_u32(value: Optional[int]) -> str:
    if value is None:
        return ""
    return f"0x{to_u32(value):08x}"


def load_cases(path: Path) -> List[Dict]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("cases"), list):
        return data["cases"]
    raise ValueError("Unsupported json format")


def get_actual_field(case: Dict, keys: List[str]) -> Optional[int]:
    for key in keys:
        if key in case:
            return parse_int(case[key])
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="expected 与 actual 差分")
    parser.add_argument("--expected", type=Path, required=True, help="expected json")
    parser.add_argument("--actual", type=Path, required=True, help="actual json")
    parser.add_argument("--out", type=Path, required=True, help="输出 csv")
    args = parser.parse_args()

    expected_cases = load_cases(args.expected)
    actual_cases = load_cases(args.actual)
    actual_map = {str(c.get("case_id")): c for c in actual_cases}

    fieldnames = [
        "case_id",
        "instr",
        "rs1",
        "rs2",
        "rd_in",
        "expected_rd",
        "expected_vxsat",
        "actual_rd",
        "actual_vxsat",
        "pass",
        "attribution",
    ]

    args.out.parent.mkdir(parents=True, exist_ok=True)

    total = 0
    passed = 0
    failed = 0

    with args.out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for item in expected_cases:
            total += 1
            case_id = str(item["case_id"])
            instr = str(item["instr"])

            exp_rd = to_u32(parse_int(item.get("expected_rd", item.get("rd", 0))) or 0)
            exp_vxsat = int(parse_int(item.get("expected_vxsat", item.get("vxsat", 0))) or 0)

            actual = actual_map.get(case_id)
            attribution = ""

            if actual is None:
                act_rd = None
                act_vxsat = None
                is_pass = False
                attribution = "CONFIG_MISMATCH"
            else:
                act_rd = get_actual_field(actual, ["actual_rd", "rd", "result_rd", "xrd"])
                act_vxsat = get_actual_field(actual, ["actual_vxsat", "vxsat", "result_vxsat"])
                if act_rd is not None:
                    act_rd = to_u32(act_rd)
                if act_vxsat is None:
                    act_vxsat = 0

                is_pass = act_rd is not None and (act_rd == exp_rd) and (int(act_vxsat) == exp_vxsat)
                if not is_pass:
                    if act_rd is None:
                        attribution = "CONFIG_MISMATCH"
                    elif act_rd == exp_rd and int(act_vxsat) != exp_vxsat:
                        attribution = "CONFIG_MISMATCH"
                    else:
                        attribution = "IMPLEMENTATION_BUG"

            if is_pass:
                passed += 1
            else:
                failed += 1

            writer.writerow(
                {
                    "case_id": case_id,
                    "instr": instr,
                    "rs1": format_u32(parse_int(item.get("rs1", 0))),
                    "rs2": format_u32(parse_int(item.get("rs2", 0))),
                    "rd_in": format_u32(parse_int(item.get("rd_in", 0))),
                    "expected_rd": format_u32(exp_rd),
                    "expected_vxsat": exp_vxsat,
                    "actual_rd": format_u32(act_rd),
                    "actual_vxsat": "" if act_vxsat is None else int(act_vxsat),
                    "pass": "1" if is_pass else "0",
                    "attribution": attribution,
                }
            )

    print(f"diff generated: {args.out}")
    print(f"total={total}, pass={passed}, fail={failed}")


if __name__ == "__main__":
    main()
