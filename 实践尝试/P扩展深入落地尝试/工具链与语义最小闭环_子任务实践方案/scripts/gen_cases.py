import argparse
import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


INSTRUCTIONS = [
    "PSADD.B",
    "PSSUB.B",
    "PSSHAR.HS",
    "PSSHLR.HS",
    "PMULQ.H",
    "PMULQR.H",
    "PM2ADD.H",
    "PM2ADDA.H",
    "PM4ADD.B",
    "PM4ADDA.B",
]

BYTE_BOUNDARY = [-128, -127, -1, 0, 1, 126, 127]
HALF_BOUNDARY = [-32768, -32767, -1, 0, 1, 32766, 32767]
SSHAMT_BOUNDARY = [-17, -16, -15, -1, 0, 1, 15, 16, 17]
RD_BOUNDARY = [-2147483648, -1, 0, 1, 2147483647]


def to_u32(value: int) -> int:
    return value & 0xFFFFFFFF


def pack_lanes(values: List[int], width: int) -> int:
    mask = (1 << width) - 1
    out = 0
    for idx, value in enumerate(values):
        out |= (value & mask) << (idx * width)
    return to_u32(out)


def make_case(case_id: int, instr: str, rs1: int, rs2: int, rd_in: int, kind: str) -> Dict:
    return {
        "case_id": f"C{case_id:07d}",
        "instr": instr,
        "rs1": to_u32(rs1),
        "rs2": to_u32(rs2),
        "rd_in": to_u32(rd_in),
        "kind": kind,
    }


def boundary_cases() -> List[Dict]:
    cases: List[Dict] = []
    cid = 1

    byte_pairs = [
        (-128, 1),
        (127, 1),
        (-1, 1),
        (126, 2),
        (0, 0),
        (127, 127),
        (-128, -128),
    ]

    for instr in ("PSADD.B", "PSSUB.B"):
        for a, b in byte_pairs:
            rs1 = pack_lanes([a, a, a, a], 8)
            rs2 = pack_lanes([b, b, b, b], 8)
            cases.append(make_case(cid, instr, rs1, rs2, 0, "boundary"))
            cid += 1

    for instr in ("PSSHAR.HS", "PSSHLR.HS"):
        for lane in (-32768, -1, 0, 1, 32767):
            rs1 = pack_lanes([lane, lane], 16)
            for s in SSHAMT_BOUNDARY:
                rs2 = to_u32(s & 0xFF)
                cases.append(make_case(cid, instr, rs1, rs2, 0, "boundary"))
                cid += 1

    q_pairs = [
        (-32768, -32768),
        (-32768, 32767),
        (32767, 32767),
        (16384, 16384),
        (-1, -1),
        (12345, -23456),
    ]

    for instr in ("PMULQ.H", "PMULQR.H"):
        for a, b in q_pairs:
            rs1 = pack_lanes([a, -a], 16)
            rs2 = pack_lanes([b, -b], 16)
            cases.append(make_case(cid, instr, rs1, rs2, 0, "boundary"))
            cid += 1

    pm2_vectors = [
        ([1, 2], [3, 4]),
        ([32767, 32767], [1, 1]),
        ([-32768, -32768], [1, 1]),
        ([1000, -2000], [-3000, 4000]),
    ]

    for instr in ("PM2ADD.H", "PM2ADDA.H"):
        for v1, v2 in pm2_vectors:
            for rd in (RD_BOUNDARY if instr.endswith("ADDA.H") else [0]):
                rs1 = pack_lanes(v1, 16)
                rs2 = pack_lanes(v2, 16)
                cases.append(make_case(cid, instr, rs1, rs2, rd, "boundary"))
                cid += 1

    pm4_vectors = [
        ([1, 1, 1, 1], [1, 1, 1, 1]),
        ([127, 127, 127, 127], [2, 2, 2, 2]),
        ([-128, -128, -128, -128], [2, 2, 2, 2]),
        ([10, -20, 30, -40], [-5, 6, -7, 8]),
    ]

    for instr in ("PM4ADD.B", "PM4ADDA.B"):
        for v1, v2 in pm4_vectors:
            for rd in (RD_BOUNDARY if instr.endswith("ADDA.B") else [0]):
                rs1 = pack_lanes(v1, 8)
                rs2 = pack_lanes(v2, 8)
                cases.append(make_case(cid, instr, rs1, rs2, rd, "boundary"))
                cid += 1

    return cases


def random_cases(start_id: int, seeds: List[int], random_per_seed: int) -> List[Dict]:
    cases: List[Dict] = []
    cid = start_id

    for seed in seeds:
        rng = random.Random(seed)
        for instr in INSTRUCTIONS:
            for _ in range(random_per_seed):
                rs1 = rng.getrandbits(32)
                rs2 = rng.getrandbits(32)
                if instr in ("PSSHAR.HS", "PSSHLR.HS"):
                    rs2 = (rs2 & 0xFFFFFF00) | rng.getrandbits(8)
                rd_in = rng.getrandbits(32) if instr.endswith("ADDA.H") or instr.endswith("ADDA.B") else 0
                cases.append(make_case(cid, instr, rs1, rs2, rd_in, f"random_seed_{seed}"))
                cid += 1

    return cases


def parse_seeds(seed_text: str) -> List[int]:
    if not seed_text.strip():
        return []
    return [int(part.strip()) for part in seed_text.split(",") if part.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="生成最小闭环样例")
    parser.add_argument("--out", type=Path, required=True, help="输出 cases json")
    parser.add_argument("--seeds", type=str, default="1,7,42,20260405", help="逗号分隔随机 seed")
    parser.add_argument("--random-per-seed", type=int, default=200, help="每条指令每个 seed 的随机样例数量")
    args = parser.parse_args()

    seeds = parse_seeds(args.seeds)
    boundary = boundary_cases()
    random_part = random_cases(len(boundary) + 1, seeds, args.random_per_seed)
    all_cases = boundary + random_part

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "instruction_count": len(INSTRUCTIONS),
        "instructions": INSTRUCTIONS,
        "seeds": seeds,
        "random_per_seed": args.random_per_seed,
        "boundary_case_count": len(boundary),
        "random_case_count": len(random_part),
        "case_count": len(all_cases),
        "cases": all_cases,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"cases generated: {args.out}")
    print(f"total cases: {len(all_cases)}")


if __name__ == "__main__":
    main()
