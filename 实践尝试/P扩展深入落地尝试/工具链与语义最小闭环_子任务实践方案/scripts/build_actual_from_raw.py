import argparse
import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Optional


ID_KEYS = ("case_id", "id", "case")
RD_KEYS = ("actual_rd", "rd", "result_rd", "xrd")
VXSAT_KEYS = ("actual_vxsat", "vxsat", "result_vxsat")
STATUS_KEYS = ("status", "result", "state")
NOTE_KEYS = ("note", "reason", "message", "stderr")
CASE_ID_RE = re.compile(r"C\d{7}", re.IGNORECASE)
PAIR_RE = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*([^,\s]+)")


def parse_int(value) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        text = value.strip().lower()
        if text == "":
            return None
        if text.startswith("0x"):
            return int(text, 16)
        return int(text)
    raise ValueError(f"Unsupported int value: {value}")


def get_first(mapping: Dict, keys) -> Optional[str]:
    for key in keys:
        if key in mapping and mapping[key] not in (None, ""):
            return str(mapping[key])
    return None


def normalize_case(raw: Dict, line_hint: str, strict: bool) -> Optional[Dict]:
    lowered = {str(k).strip().lower(): v for k, v in raw.items()}

    case_id = get_first(lowered, ID_KEYS)
    rd_text = get_first(lowered, RD_KEYS)
    vxsat_text = get_first(lowered, VXSAT_KEYS)
    status_text = get_first(lowered, STATUS_KEYS)
    note_text = get_first(lowered, NOTE_KEYS)

    if case_id is None and "line" in lowered:
        found = CASE_ID_RE.search(str(lowered["line"]))
        if found:
            case_id = found.group(0)

    if case_id is None:
        if strict:
            raise ValueError(f"missing case_id at {line_hint}")
        return None

    found = CASE_ID_RE.search(case_id)
    if found:
        case_id = found.group(0).upper()

    out = {
        "case_id": case_id,
    }
    if status_text is not None:
        out["status"] = status_text
    if note_text is not None:
        out["note"] = note_text

    if rd_text is None:
        if strict:
            raise ValueError(f"missing rd value at {line_hint}")
        if vxsat_text is not None:
            vxsat = parse_int(vxsat_text)
            if vxsat is not None:
                out["actual_vxsat"] = int(vxsat)
        return out

    actual_rd = parse_int(rd_text)
    if actual_rd is None:
        if strict:
            raise ValueError(f"rd value is empty at {line_hint}")
        if vxsat_text is not None:
            vxsat = parse_int(vxsat_text)
            if vxsat is not None:
                out["actual_vxsat"] = int(vxsat)
        return out

    out["actual_rd"] = actual_rd

    if vxsat_text is not None:
        vxsat = parse_int(vxsat_text)
        if vxsat is not None:
            out["actual_vxsat"] = int(vxsat)

    return out


def parse_kv_line(line: str) -> Optional[Dict]:
    pairs = PAIR_RE.findall(line)
    if not pairs:
        return None
    out: Dict[str, str] = {}
    for k, v in pairs:
        out[k.strip().lower()] = v.strip()
    return out


def parse_plain_line(line: str) -> Optional[Dict]:
    tokens = [t for t in re.split(r"[\s,]+", line.strip()) if t]
    if len(tokens) < 2:
        return None

    case_id = tokens[0]
    if not CASE_ID_RE.search(case_id):
        found = CASE_ID_RE.search(line)
        if found:
            case_id = found.group(0)

    out: Dict[str, str] = {
        "case_id": case_id,
        "actual_rd": tokens[1],
    }
    if len(tokens) >= 3:
        out["actual_vxsat"] = tokens[2]
    return out


def load_json_cases(path: Path, strict: bool) -> List[Dict]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and isinstance(data.get("cases"), list):
        raw_cases = data["cases"]
    elif isinstance(data, list):
        raw_cases = data
    else:
        raise ValueError("Unsupported json raw format")

    out: List[Dict] = []
    for idx, item in enumerate(raw_cases, start=1):
        if not isinstance(item, dict):
            if strict:
                raise ValueError(f"json case #{idx} is not an object")
            continue
        parsed = normalize_case(item, f"json-case-{idx}", strict)
        if parsed is not None:
            out.append(parsed)
    return out


def looks_like_header(line: str) -> bool:
    low = line.lower()
    has_key = "case_id" in low or "actual_rd" in low or "result_rd" in low
    has_delim = "," in line or "\t" in line
    return has_key and has_delim


def load_text_cases(path: Path, strict: bool) -> List[Dict]:
    content = path.read_text(encoding="utf-8")
    lines = [
        line
        for line in content.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not lines:
        return []

    out: List[Dict] = []

    if looks_like_header(lines[0]):
        reader = csv.DictReader(lines)
        for idx, row in enumerate(reader, start=2):
            parsed = normalize_case(row, f"line-{idx}", strict)
            if parsed is not None:
                out.append(parsed)
        return out

    for idx, line in enumerate(lines, start=1):
        candidate = parse_kv_line(line)
        if candidate is None:
            candidate = parse_plain_line(line)

        if candidate is None:
            if strict:
                raise ValueError(f"unable to parse line-{idx}: {line}")
            continue

        candidate["line"] = line
        parsed = normalize_case(candidate, f"line-{idx}", strict)
        if parsed is not None:
            out.append(parsed)

    return out


def dedup_cases(cases: List[Dict], strict: bool) -> List[Dict]:
    seen = set()
    out: List[Dict] = []
    for item in cases:
        case_id = item["case_id"]
        if case_id in seen:
            if strict:
                raise ValueError(f"duplicate case_id: {case_id}")
            continue
        seen.add(case_id)
        out.append(item)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="将 ISS/DUT 原始输出转换为 actual json")
    parser.add_argument("--raw", type=Path, required=True, help="原始输出文件（json/csv/txt）")
    parser.add_argument("--out", type=Path, required=True, help="输出 actual json")
    parser.add_argument("--strict", action="store_true", help="严格模式：遇到异常行直接报错")
    args = parser.parse_args()

    if not args.raw.exists():
        raise FileNotFoundError(args.raw)

    text = args.raw.read_text(encoding="utf-8").lstrip()
    if text.startswith("{") or text.startswith("["):
        parsed = load_json_cases(args.raw, args.strict)
    else:
        parsed = load_text_cases(args.raw, args.strict)

    parsed = dedup_cases(parsed, args.strict)

    payload = {
        "source": str(args.raw).replace("\\", "/"),
        "case_count": len(parsed),
        "cases": parsed,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    with_vxsat = sum(1 for item in parsed if "actual_vxsat" in item)
    print(f"actual json generated: {args.out}")
    print(f"case_count={len(parsed)}")
    print(f"with_vxsat={with_vxsat}")


if __name__ == "__main__":
    main()
