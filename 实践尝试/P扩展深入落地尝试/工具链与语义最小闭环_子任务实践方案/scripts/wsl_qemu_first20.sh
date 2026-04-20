#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

CASES_IN="${CASES_IN:-cases/minset_first20_for_iss.json}"
RAW_OUT="${RAW_OUT:-actual/minset_first20_qemu_raw.csv}"
ACTUAL_OUT="${ACTUAL_OUT:-actual/minset_first20_qemu.actual.json}"
EXPECTED_IN="${EXPECTED_IN:-expected/minset_first20_for_iss.expected.json}"
DIFF_OUT="${DIFF_OUT:-reports/diff-minset-first20-qemu.csv}"
SUMMARY_OUT="${SUMMARY_OUT:-reports/diff-minset-first20-qemu-summary.md}"

QEMU_BIN="${QEMU_BIN:-/usr/bin/qemu-riscv64-static}"
QEMU_CPU="${QEMU_CPU:-}"
CAPTURE_VXSAT="${CAPTURE_VXSAT:-0}"
GCC_BIN="${GCC_BIN:-riscv64-linux-gnu-gcc}"

EXTRA_ARGS=()
if [[ "$CAPTURE_VXSAT" == "1" ]]; then
  EXTRA_ARGS+=(--capture-vxsat)
fi

echo "[1/3] run qemu cases"
python3 scripts/run_qemu_cases.py \
  --cases "$CASES_IN" \
  --out-raw "$RAW_OUT" \
  --out-actual "$ACTUAL_OUT" \
  --qemu-bin "$QEMU_BIN" \
  --qemu-cpu "$QEMU_CPU" \
  "${EXTRA_ARGS[@]}" \
  --gcc-bin "$GCC_BIN"

echo "[2/3] diff expected vs qemu actual"
python3 scripts/diff.py --expected "$EXPECTED_IN" --actual "$ACTUAL_OUT" --out "$DIFF_OUT"

echo "[3/3] summarize diff"
python3 scripts/summarize_diff.py --diff "$DIFF_OUT" --out "$SUMMARY_OUT"

echo "done"
