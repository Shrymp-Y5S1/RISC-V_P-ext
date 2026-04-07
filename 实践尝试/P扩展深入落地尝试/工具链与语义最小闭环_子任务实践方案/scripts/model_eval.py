import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from model.p_semantics_min import evaluate_case  # noqa: E402


def load_cases(path: Path) -> List[Dict]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("cases"), list):
        return data["cases"]
    raise ValueError("Unsupported cases format")


def main() -> None:
    parser = argparse.ArgumentParser(description="调用黄金语义模型生成 expected")
    parser.add_argument("--cases", type=Path, required=True, help="输入 cases json")
    parser.add_argument("--out", type=Path, required=True, help="输出 expected json")
    args = parser.parse_args()

    cases = load_cases(args.cases)
    expected = [evaluate_case(c) for c in cases]

    payload = {
        "source": str(args.cases).replace("\\", "/"),
        "case_count": len(expected),
        "cases": expected,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"expected generated: {args.out}")
    print(f"total cases: {len(expected)}")


if __name__ == "__main__":
    main()
