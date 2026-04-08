import argparse
import csv
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


def load_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def is_pass(row: Dict[str, str]) -> bool:
    return str(row.get("pass", "")).strip() == "1"


def main() -> None:
    parser = argparse.ArgumentParser(description="汇总 diff csv，生成 T6 归因摘要")
    parser.add_argument("--diff", type=Path, required=True, help="diff csv")
    parser.add_argument("--out", type=Path, required=True, help="输出 markdown")
    parser.add_argument("--top", type=int, default=20, help="失败样例展示条数")
    args = parser.parse_args()

    rows = load_rows(args.diff)
    total = len(rows)
    passed_rows = [r for r in rows if is_pass(r)]
    failed_rows = [r for r in rows if not is_pass(r)]
    passed = len(passed_rows)
    failed = len(failed_rows)

    fail_by_attr = Counter((r.get("attribution") or "UNSPECIFIED") for r in failed_rows)
    fail_by_instr = Counter((r.get("instr") or "UNKNOWN") for r in failed_rows)

    lines: List[str] = []
    lines.append("# Diff 归因摘要")
    lines.append("")
    lines.append(f"生成时间: {datetime.now(timezone.utc).isoformat()}")
    lines.append(f"输入文件: {str(args.diff).replace('\\\\', '/')}")
    lines.append("")
    lines.append("## 1. 汇总")
    lines.append("")
    lines.append(f"- total: {total}")
    lines.append(f"- pass: {passed}")
    lines.append(f"- fail: {failed}")
    if total > 0:
        lines.append(f"- pass_rate: {passed * 100.0 / total:.2f}%")
        lines.append(f"- fail_rate: {failed * 100.0 / total:.2f}%")
    lines.append("")

    lines.append("## 2. 失败归因分布")
    lines.append("")
    lines.append("| attribution | count |")
    lines.append("| --- | ---: |")
    if fail_by_attr:
        for attr, cnt in fail_by_attr.most_common():
            lines.append(f"| {attr} | {cnt} |")
    else:
        lines.append("| (none) | 0 |")
    lines.append("")

    lines.append("## 3. 指令失败分布")
    lines.append("")
    lines.append("| instr | fail_count |")
    lines.append("| --- | ---: |")
    if fail_by_instr:
        for instr, cnt in fail_by_instr.most_common():
            lines.append(f"| {instr} | {cnt} |")
    else:
        lines.append("| (none) | 0 |")
    lines.append("")

    lines.append(f"## 4. 失败样例（前 {max(args.top, 0)} 条）")
    lines.append("")
    header_row = (
        "| case_id | instr | expected_rd | actual_rd | "
        "expected_vxsat | actual_vxsat | attribution |"
    )
    lines.append(header_row)
    lines.append("| --- | --- | --- | --- | ---: | ---: | --- |")
    if failed_rows and args.top > 0:
        for row in failed_rows[: args.top]:
            row_fmt = (
                "| {case_id} | {instr} | {expected_rd} | {actual_rd} | "
                "{expected_vxsat} | {actual_vxsat} | {attribution} |"
            )
            lines.append(
                row_fmt.format(
                    case_id=row.get("case_id", ""),
                    instr=row.get("instr", ""),
                    expected_rd=row.get("expected_rd", ""),
                    actual_rd=row.get("actual_rd", ""),
                    expected_vxsat=row.get("expected_vxsat", ""),
                    actual_vxsat=row.get("actual_vxsat", ""),
                    attribution=row.get("attribution", ""),
                )
            )
    else:
        lines.append("| (none) | - | - | - | - | - | - |")
    lines.append("")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")

    print(f"summary generated: {args.out}")
    print(f"total={total}, pass={passed}, fail={failed}")


if __name__ == "__main__":
    main()
