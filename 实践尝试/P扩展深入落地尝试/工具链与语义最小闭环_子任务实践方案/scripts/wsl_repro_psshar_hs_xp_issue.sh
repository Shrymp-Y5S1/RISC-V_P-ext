#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

CASES_IN="${CASES_IN:-cases/psshar_hs_shift_sweep_xp_20260420.json}"
EXPECTED_IN="${EXPECTED_IN:-expected/psshar_hs_shift_sweep_xp_20260420.expected.json}"
RAW_OUT="${RAW_OUT:-actual/psshar_hs_shift_sweep_xp_repro_raw.csv}"
ACTUAL_OUT="${ACTUAL_OUT:-actual/psshar_hs_shift_sweep_xp_repro.actual.json}"
DIFF_OUT="${DIFF_OUT:-reports/diff-psshar_hs_shift_sweep_xp_repro.csv}"
SUMMARY_OUT="${SUMMARY_OUT:-reports/diff-psshar_hs_shift_sweep_xp_repro-summary.md}"

QEMU_BIN="${QEMU_BIN:-/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64}"
QEMU_CPU="${QEMU_CPU:-max,x-p=true}"
CAPTURE_VXSAT="${CAPTURE_VXSAT:-1}"
GCC_BIN="${GCC_BIN:-riscv64-linux-gnu-gcc}"

EXTRA_ARGS=()
if [[ "$CAPTURE_VXSAT" == "1" ]]; then
  EXTRA_ARGS+=(--capture-vxsat)
fi

for f in "$CASES_IN" "$EXPECTED_IN"; do
  if [[ ! -f "$f" ]]; then
    echo "missing required file: $f"
    exit 1
  fi
done

echo "[1/3] run qemu sweep cases"
python3 scripts/run_qemu_cases.py \
  --cases "$CASES_IN" \
  --out-raw "$RAW_OUT" \
  --out-actual "$ACTUAL_OUT" \
  --qemu-bin "$QEMU_BIN" \
  --qemu-cpu "$QEMU_CPU" \
  "${EXTRA_ARGS[@]}" \
  --gcc-bin "$GCC_BIN"

echo "[2/3] diff expected vs actual"
python3 scripts/diff.py --expected "$EXPECTED_IN" --actual "$ACTUAL_OUT" --out "$DIFF_OUT"

echo "[3/3] summarize diff"
python3 scripts/summarize_diff.py --diff "$DIFF_OUT" --out "$SUMMARY_OUT"

DIFF_OUT="$DIFF_OUT" python3 - <<'PY'
import csv
import os

diff_path = os.environ["DIFF_OUT"]
fails = []
with open(diff_path, "r", encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        if row.get("pass") == "0":
            fails.append(row)

print(f"repro diff file: {diff_path}")
print(f"fail_count={len(fails)}")
if fails:
    first = fails[0]
    print(
        "first_fail:"
        f" case_id={first.get('case_id')}"
        f" rs2={first.get('rs2')}"
        f" expected_rd={first.get('expected_rd')}"
        f" actual_rd={first.get('actual_rd')}"
    )
PY

echo "done"