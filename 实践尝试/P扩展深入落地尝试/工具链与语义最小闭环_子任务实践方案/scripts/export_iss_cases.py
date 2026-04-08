import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List


def to_u32(value: int) -> int:
    return value & 0xFFFFFFFF


def to_hex32(value: int) -> str:
    return f"0x{to_u32(value):08x}"


def load_cases(path: Path) -> List[Dict]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("cases"), list):
        return data["cases"]
    raise ValueError("Unsupported cases format")


def main() -> None:
    parser = argparse.ArgumentParser(description="导出 ISS/DUT 执行输入子集")
    parser.add_argument("--cases", type=Path, required=True, help="输入 cases json")
    parser.add_argument("--out-json", type=Path, required=True, help="输出子集 json")
    parser.add_argument("--out-csv", type=Path, required=True, help="输出子集 csv")
    parser.add_argument(
        "--out-raw-template", type=Path, default=None, help="输出 raw 模板 csv"
    )
    parser.add_argument("--start", type=int, default=0, help="起始索引，默认 0")
    parser.add_argument("--limit", type=int, default=20, help="导出数量，默认 20")
    args = parser.parse_args()

    if args.start < 0:
        raise ValueError("--start must be >= 0")
    if args.limit <= 0:
        raise ValueError("--limit must be > 0")

    all_cases = load_cases(args.cases)
    subset = all_cases[args.start : args.start + args.limit]

    out_cases: List[Dict] = []
    for item in subset:
        out_cases.append(
            {
                "case_id": str(item["case_id"]),
                "instr": str(item["instr"]),
                "rs1": int(item["rs1"]),
                "rs2": int(item["rs2"]),
                "rd_in": int(item.get("rd_in", 0)),
            }
        )

    json_payload = {
        "source": str(args.cases).replace("\\", "/"),
        "start": args.start,
        "limit": args.limit,
        "case_count": len(out_cases),
        "cases": out_cases,
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    with args.out_json.open("w", encoding="utf-8") as f:
        json.dump(json_payload, f, indent=2, ensure_ascii=False)

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "case_id",
                "instr",
                "rs1",
                "rs2",
                "rd_in",
                "rs1_hex",
                "rs2_hex",
                "rd_in_hex",
            ],
        )
        writer.writeheader()
        for item in out_cases:
            writer.writerow(
                {
                    "case_id": item["case_id"],
                    "instr": item["instr"],
                    "rs1": item["rs1"],
                    "rs2": item["rs2"],
                    "rd_in": item["rd_in"],
                    "rs1_hex": to_hex32(item["rs1"]),
                    "rs2_hex": to_hex32(item["rs2"]),
                    "rd_in_hex": to_hex32(item["rd_in"]),
                }
            )

    if args.out_raw_template is not None:
        args.out_raw_template.parent.mkdir(parents=True, exist_ok=True)
        with args.out_raw_template.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["case_id", "actual_rd", "actual_vxsat"]
            )
            writer.writeheader()
            for item in out_cases:
                writer.writerow(
                    {"case_id": item["case_id"], "actual_rd": "", "actual_vxsat": ""}
                )

    print(f"iss bundle json generated: {args.out_json}")
    print(f"iss bundle csv generated: {args.out_csv}")
    if args.out_raw_template is not None:
        print(f"raw template generated: {args.out_raw_template}")
    print(f"case_count={len(out_cases)}")


if __name__ == "__main__":
    main()
