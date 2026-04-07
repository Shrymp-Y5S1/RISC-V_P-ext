import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


def to_u32(value: int) -> int:
    return value & 0xFFFFFFFF


def sign_extend(value: int, width: int) -> int:
    mask = (1 << width) - 1
    value &= mask
    sign_bit = 1 << (width - 1)
    return (value ^ sign_bit) - sign_bit


def sat_signed(value: int, width: int) -> Tuple[int, bool]:
    low = -(1 << (width - 1))
    high = (1 << (width - 1)) - 1
    if value < low:
        return low, True
    if value > high:
        return high, True
    return value, False


def sat_unsigned(value: int, width: int) -> Tuple[int, bool]:
    low = 0
    high = (1 << width) - 1
    if value < low:
        return low, True
    if value > high:
        return high, True
    return value, False


def unpack_lanes(value: int, lane_width: int, signed: bool) -> List[int]:
    lane_count = 32 // lane_width
    mask = (1 << lane_width) - 1
    lanes: List[int] = []
    for idx in range(lane_count):
        lane = (value >> (idx * lane_width)) & mask
        lanes.append(sign_extend(lane, lane_width) if signed else lane)
    return lanes


def pack_lanes(lanes: List[int], lane_width: int) -> int:
    mask = (1 << lane_width) - 1
    result = 0
    for idx, lane in enumerate(lanes):
        result |= (lane & mask) << (idx * lane_width)
    return to_u32(result)


def round_shift_right_signed(value: int, shift: int) -> int:
    if shift <= 0:
        return value
    add = 1 << (shift - 1)
    if value < 0:
        return -(((-value) + add) >> shift)
    return (value + add) >> shift


def round_shift_right_unsigned(value: int, shift: int) -> int:
    if shift <= 0:
        return value
    add = 1 << (shift - 1)
    return (value + add) >> shift


def sshamt_from_rs2(rs2: int) -> int:
    return sign_extend(rs2 & 0xFF, 8)


def psadd_b(rs1: int, rs2: int) -> Tuple[int, int]:
    a = unpack_lanes(rs1, 8, signed=True)
    b = unpack_lanes(rs2, 8, signed=True)
    out: List[int] = []
    vxsat = False
    for x, y in zip(a, b):
        lane, saturated = sat_signed(x + y, 8)
        out.append(lane)
        vxsat |= saturated
    return pack_lanes(out, 8), int(vxsat)


def pssub_b(rs1: int, rs2: int) -> Tuple[int, int]:
    a = unpack_lanes(rs1, 8, signed=True)
    b = unpack_lanes(rs2, 8, signed=True)
    out: List[int] = []
    vxsat = False
    for x, y in zip(a, b):
        lane, saturated = sat_signed(x - y, 8)
        out.append(lane)
        vxsat |= saturated
    return pack_lanes(out, 8), int(vxsat)


def psshar_hs(rs1: int, rs2: int) -> Tuple[int, int]:
    lanes = unpack_lanes(rs1, 16, signed=True)
    shift = sshamt_from_rs2(rs2)
    out: List[int] = []
    vxsat = False

    if shift >= 0:
        for lane in lanes:
            shifted = lane << shift
            clamped, saturated = sat_signed(shifted, 16)
            out.append(clamped)
            vxsat |= saturated
    else:
        right = -shift
        for lane in lanes:
            out.append(round_shift_right_signed(lane, right))

    return pack_lanes(out, 16), int(vxsat)


def psshlr_hs(rs1: int, rs2: int) -> Tuple[int, int]:
    lanes = unpack_lanes(rs1, 16, signed=False)
    shift = sshamt_from_rs2(rs2)
    out: List[int] = []
    vxsat = False

    if shift >= 0:
        for lane in lanes:
            shifted = lane << shift
            clamped, saturated = sat_unsigned(shifted, 16)
            out.append(clamped)
            vxsat |= saturated
    else:
        right = -shift
        for lane in lanes:
            out.append(round_shift_right_unsigned(lane, right))

    return pack_lanes(out, 16), int(vxsat)


def pmulq_h(rs1: int, rs2: int) -> Tuple[int, int]:
    a = unpack_lanes(rs1, 16, signed=True)
    b = unpack_lanes(rs2, 16, signed=True)
    out: List[int] = []
    vxsat = False

    for x, y in zip(a, b):
        if x == -32768 and y == -32768:
            lane = 32767
            saturated = True
        else:
            lane = (x * y) >> 15
            lane, saturated = sat_signed(lane, 16)
        out.append(lane)
        vxsat |= saturated

    return pack_lanes(out, 16), int(vxsat)


def pmulqr_h(rs1: int, rs2: int) -> Tuple[int, int]:
    a = unpack_lanes(rs1, 16, signed=True)
    b = unpack_lanes(rs2, 16, signed=True)
    out: List[int] = []
    vxsat = False

    for x, y in zip(a, b):
        if x == -32768 and y == -32768:
            lane = 32767
            saturated = True
        else:
            lane = ((x * y) + (1 << 14)) >> 15
            lane, saturated = sat_signed(lane, 16)
        out.append(lane)
        vxsat |= saturated

    return pack_lanes(out, 16), int(vxsat)


def pm2add_h(
    rs1: int, rs2: int, rd_in: int = 0, with_acc: bool = False
) -> Tuple[int, int]:
    a0 = sign_extend(rs1 & 0xFFFF, 16)
    a1 = sign_extend((rs1 >> 16) & 0xFFFF, 16)
    b0 = sign_extend(rs2 & 0xFFFF, 16)
    b1 = sign_extend((rs2 >> 16) & 0xFFFF, 16)

    acc = a0 * b0 + a1 * b1
    if with_acc:
        acc += sign_extend(rd_in, 32)

    return to_u32(acc), 0


def pm4add_b(
    rs1: int, rs2: int, rd_in: int = 0, with_acc: bool = False
) -> Tuple[int, int]:
    a = unpack_lanes(rs1, 8, signed=True)
    b = unpack_lanes(rs2, 8, signed=True)
    acc = sum(x * y for x, y in zip(a, b))
    if with_acc:
        acc += sign_extend(rd_in, 32)
    return to_u32(acc), 0


def evaluate_case(case: Dict) -> Dict:
    instr = str(case["instr"]).strip().upper()
    rs1 = to_u32(int(case["rs1"]))
    rs2 = to_u32(int(case["rs2"]))
    rd_in = to_u32(int(case.get("rd_in", 0)))

    if instr == "PSADD.B":
        rd, vxsat = psadd_b(rs1, rs2)
    elif instr == "PSSUB.B":
        rd, vxsat = pssub_b(rs1, rs2)
    elif instr == "PSSHAR.HS":
        rd, vxsat = psshar_hs(rs1, rs2)
    elif instr == "PSSHLR.HS":
        rd, vxsat = psshlr_hs(rs1, rs2)
    elif instr == "PMULQ.H":
        rd, vxsat = pmulq_h(rs1, rs2)
    elif instr == "PMULQR.H":
        rd, vxsat = pmulqr_h(rs1, rs2)
    elif instr == "PM2ADD.H":
        rd, vxsat = pm2add_h(rs1, rs2, with_acc=False)
    elif instr == "PM2ADDA.H":
        rd, vxsat = pm2add_h(rs1, rs2, rd_in=rd_in, with_acc=True)
    elif instr == "PM4ADD.B":
        rd, vxsat = pm4add_b(rs1, rs2, with_acc=False)
    elif instr == "PM4ADDA.B":
        rd, vxsat = pm4add_b(rs1, rs2, rd_in=rd_in, with_acc=True)
    else:
        raise ValueError(f"Unsupported instruction: {instr}")

    enriched = dict(case)
    enriched["expected_rd"] = to_u32(rd)
    enriched["expected_vxsat"] = int(vxsat)
    enriched["expected_rd_hex"] = f"0x{to_u32(rd):08x}"
    return enriched


def run_selftest() -> None:
    tests = [
        {
            "instr": "PSADD.B",
            "rs1": 0x7F7F7F7F,
            "rs2": 0x01010101,
            "rd_in": 0,
            "expected": 0x7F7F7F7F,
            "vxsat": 1,
        },
        {
            "instr": "PSSUB.B",
            "rs1": 0x80808080,
            "rs2": 0x01010101,
            "rd_in": 0,
            "expected": 0x80808080,
            "vxsat": 1,
        },
        {
            "instr": "PSSHAR.HS",
            "rs1": 0x7FFF8000,
            "rs2": 0xFFFFFFFF,
            "rd_in": 0,
            "expected": 0x4000C000,
            "vxsat": 0,
        },
        {
            "instr": "PSSHLR.HS",
            "rs1": 0x00010001,
            "rs2": 0x00000010,
            "rd_in": 0,
            "expected": 0xFFFFFFFF,
            "vxsat": 1,
        },
        {
            "instr": "PMULQ.H",
            "rs1": 0x7FFF7FFF,
            "rs2": 0x00010001,
            "rd_in": 0,
            "expected": 0x00000000,
            "vxsat": 0,
        },
        {
            "instr": "PMULQR.H",
            "rs1": 0x7FFF7FFF,
            "rs2": 0x00010001,
            "rd_in": 0,
            "expected": 0x00010001,
            "vxsat": 0,
        },
        {
            "instr": "PM2ADD.H",
            "rs1": 0x00020001,
            "rs2": 0x00040003,
            "rd_in": 0,
            "expected": 0x0000000B,
            "vxsat": 0,
        },
        {
            "instr": "PM2ADDA.H",
            "rs1": 0x00020001,
            "rs2": 0x00040003,
            "rd_in": 5,
            "expected": 0x00000010,
            "vxsat": 0,
        },
        {
            "instr": "PM4ADD.B",
            "rs1": 0x01010101,
            "rs2": 0x02020202,
            "rd_in": 0,
            "expected": 0x00000008,
            "vxsat": 0,
        },
        {
            "instr": "PM4ADDA.B",
            "rs1": 0x01010101,
            "rs2": 0x02020202,
            "rd_in": 7,
            "expected": 0x0000000F,
            "vxsat": 0,
        },
    ]

    for item in tests:
        out = evaluate_case(item)
        if (
            out["expected_rd"] != item["expected"]
            or out["expected_vxsat"] != item["vxsat"]
        ):
            raise AssertionError(f"Selftest failed: {item['instr']} => {out}")


def load_cases(path: Path) -> List[Dict]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("cases"), list):
        return data["cases"]
    raise ValueError("Unsupported case file format")


def write_expected(out_path: Path, source: Path, cases: List[Dict]) -> None:
    result = {
        "source": str(source).replace("\\", "/"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "case_count": len(cases),
        "cases": [evaluate_case(c) for c in cases],
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="P 扩展最小语义模型")
    parser.add_argument("--case-file", type=Path, help="输入样例文件")
    parser.add_argument("--out", type=Path, help="输出 expected 文件")
    parser.add_argument("--selftest", action="store_true", help="运行内置自测")
    args = parser.parse_args()

    if args.selftest:
        run_selftest()
        print("selftest passed")

    if args.case_file and args.out:
        cases = load_cases(args.case_file)
        write_expected(args.out, args.case_file, cases)
        print(f"expected generated: {args.out}")


if __name__ == "__main__":
    main()
