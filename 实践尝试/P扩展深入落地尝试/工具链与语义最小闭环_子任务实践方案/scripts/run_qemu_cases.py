import argparse
import csv
import json
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from typing import Dict, List

INSTR_WORDS = {
    "PSADD.B": 0x94C5853B,
    "PSSUB.B": 0xD4C5853B,
    "PSSHAR.HS": 0xF8C5A51B,
    "PSSHLR.HS": 0xB8C5A51B,
    "PMULQ.H": 0xD0C5F53B,
    "PMULQR.H": 0xD4C5F53B,
    "PM2ADD.H": 0x80C5D53B,
    "PM2ADDA.H": 0x88C5D53B,
    "PM4ADD.B": 0x84C5D53B,
    "PM4ADDA.B": 0x8CC5D53B,
}


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


def render_asm(
    rs1: int, rs2: int, rd_in: int, insn_word: int, capture_vxsat: bool
) -> str:
    lines = [
        ".section .bss",
        ".align 3",
        "outbuf:",
        "  .space 16",
        "",
        ".section .text",
        ".global _start",
        "_start:",
        f"  li a1, {to_u32(rs1)}",
        f"  li a2, {to_u32(rs2)}",
        f"  li a0, {to_u32(rd_in)}",
        f"  .word 0x{insn_word:08x}",
        "  la t0, outbuf",
        "  sd a0, 0(t0)",
    ]

    if capture_vxsat:
        lines.extend(
            [
                "  csrr t1, 0x009",
                "  andi t1, t1, 1",
            ]
        )
    else:
        lines.append("  li t1, 0")

    lines.extend(
        [
            "  sd t1, 8(t0)",
            "",
            "  li a0, 1",
            "  la a1, outbuf",
            "  li a2, 16",
            "  li a7, 64",
            "  ecall",
            "",
            "  li a0, 0",
            "  li a7, 93",
            "  ecall",
            "",
        ]
    )

    return "\n".join(lines)


def first_stderr_line(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line
    return ""


def run_one_case(
    case: Dict,
    gcc_bin: str,
    qemu_bin: str,
    qemu_cpu: str,
    capture_vxsat: bool,
    timeout_sec: float,
) -> Dict:
    case_id = str(case["case_id"])
    instr = str(case["instr"])

    out: Dict = {
        "case_id": case_id,
        "instr": instr,
        "status": "UNKNOWN",
        "note": "",
    }

    insn_word = INSTR_WORDS.get(instr)
    if insn_word is None:
        out["status"] = "UNSUPPORTED_INSTR"
        out["note"] = "no instruction word mapping"
        return out

    rs1 = int(case.get("rs1", 0))
    rs2 = int(case.get("rs2", 0))
    rd_in = int(case.get("rd_in", 0))

    with tempfile.TemporaryDirectory(prefix="p_qemu_case_") as td:
        tdp = Path(td)
        asm_path = tdp / "case.S"
        elf_path = tdp / "case.elf"

        asm_path.write_text(
            render_asm(rs1, rs2, rd_in, insn_word, capture_vxsat), encoding="utf-8"
        )

        compile_cmd = [
            gcc_bin,
            "-nostdlib",
            "-static",
            "-march=rv64gc",
            "-mabi=lp64d",
            str(asm_path),
            "-o",
            str(elf_path),
        ]
        cp = subprocess.run(compile_cmd, capture_output=True, text=True)
        if cp.returncode != 0:
            out["status"] = "COMPILE_FAIL"
            out["note"] = first_stderr_line(cp.stderr)
            return out

        qemu_cmd = [qemu_bin]
        if qemu_cpu:
            qemu_cmd.extend(["-cpu", qemu_cpu])
        qemu_cmd.append(str(elf_path))

        try:
            rp = subprocess.run(
                qemu_cmd,
                capture_output=True,
                timeout=timeout_sec,
            )
        except subprocess.TimeoutExpired:
            out["status"] = "TIMEOUT"
            out["note"] = f"timeout>{timeout_sec}s"
            return out

        if rp.returncode != 0:
            out["status"] = "RUNTIME_FAIL"
            if rp.returncode == -4 or rp.returncode == 132:
                out["status"] = "ILLEGAL_INSN"
            stderr_text = rp.stderr.decode("utf-8", errors="replace")
            out["note"] = first_stderr_line(stderr_text)
            return out

        raw = rp.stdout
        if len(raw) < 8:
            out["status"] = "BAD_OUTPUT"
            out["note"] = f"stdout bytes={len(raw)}"
            return out

        rd64 = int.from_bytes(raw[0:8], byteorder="little", signed=False)
        out["actual_rd"] = rd64 & 0xFFFFFFFF

        vxsat = 0
        if len(raw) >= 16:
            vxsat64 = int.from_bytes(raw[8:16], byteorder="little", signed=False)
            vxsat = int(vxsat64 & 0x1)
        out["actual_vxsat"] = vxsat
        out["status"] = "OK"
        return out


def write_raw_csv(path: Path, rows: List[Dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "case_id",
                "instr",
                "actual_rd",
                "actual_vxsat",
                "status",
                "note",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "case_id": row.get("case_id", ""),
                    "instr": row.get("instr", ""),
                    "actual_rd": (
                        ""
                        if "actual_rd" not in row
                        else to_hex32(int(row["actual_rd"]))
                    ),
                    "actual_vxsat": (
                        "" if "actual_vxsat" not in row else int(row["actual_vxsat"])
                    ),
                    "status": row.get("status", ""),
                    "note": row.get("note", ""),
                }
            )


def write_actual_json(path: Path, rows: List[Dict], source_path: Path) -> None:
    cases: List[Dict] = []
    for row in rows:
        item: Dict = {
            "case_id": row["case_id"],
            "status": row.get("status", ""),
        }
        if row.get("note"):
            item["note"] = row.get("note")
        if "actual_rd" in row:
            item["actual_rd"] = int(row["actual_rd"])
        if "actual_vxsat" in row:
            item["actual_vxsat"] = int(row["actual_vxsat"])
        cases.append(item)

    payload = {
        "source": str(source_path).replace("\\", "/"),
        "case_count": len(cases),
        "cases": cases,
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="通过 qemu 执行 case 集并导出 raw/actual"
    )
    parser.add_argument("--cases", type=Path, required=True, help="输入 cases json")
    parser.add_argument("--out-raw", type=Path, required=True, help="输出 raw csv")
    parser.add_argument(
        "--out-actual", type=Path, required=True, help="输出 actual json"
    )
    parser.add_argument(
        "--gcc-bin",
        type=str,
        default="riscv64-linux-gnu-gcc",
        help="交叉编译器路径",
    )
    parser.add_argument(
        "--qemu-bin",
        type=str,
        default="/usr/bin/qemu-riscv64-static",
        help="qemu 可执行路径",
    )
    parser.add_argument(
        "--qemu-cpu",
        type=str,
        default="",
        help="可选 CPU 参数（示例: max,x-p=true）",
    )
    parser.add_argument(
        "--capture-vxsat",
        action="store_true",
        help="通过 CSR 0x009 读取 vxsat（默认关闭）",
    )
    parser.add_argument("--limit", type=int, default=0, help="只跑前 N 条，0 表示全量")
    parser.add_argument("--timeout", type=float, default=3.0, help="单 case 超时秒数")
    args = parser.parse_args()

    all_cases = load_cases(args.cases)
    cases = all_cases[: args.limit] if args.limit > 0 else all_cases

    rows = [
        run_one_case(
            c,
            args.gcc_bin,
            args.qemu_bin,
            args.qemu_cpu,
            args.capture_vxsat,
            args.timeout,
        )
        for c in cases
    ]

    write_raw_csv(args.out_raw, rows)
    write_actual_json(args.out_actual, rows, args.cases)

    status_counter = Counter(row.get("status", "") for row in rows)
    print(f"qemu raw generated: {args.out_raw}")
    print(f"qemu actual generated: {args.out_actual}")
    print(f"case_count={len(rows)}")
    for status, cnt in status_counter.most_common():
        print(f"status[{status}]={cnt}")


if __name__ == "__main__":
    main()
