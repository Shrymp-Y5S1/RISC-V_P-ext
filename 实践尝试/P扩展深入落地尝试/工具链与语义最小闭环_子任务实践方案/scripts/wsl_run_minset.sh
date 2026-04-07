#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

# 默认按最小子集建议口径运行 4 个固定 seed。
SEEDS="${SEEDS:-1,7,42,20260405}"
RANDOM_PER_SEED="${RANDOM_PER_SEED:-200}"
CASES_OUT="${CASES_OUT:-cases/minset_seed_1_7_42_20260405.json}"
EXPECTED_OUT="${EXPECTED_OUT:-expected/minset_seed_1_7_42_20260405.expected.json}"
ACTUAL_IN="${ACTUAL_IN:-actual/minset_seed_1_7_42_20260405.actual.json}"
DIFF_OUT="${DIFF_OUT:-reports/diff-minset.csv}"

echo "[1/4] model selftest"
python3 model/p_semantics_min.py --selftest

echo "[2/4] generate cases"
python3 scripts/gen_cases.py --out "$CASES_OUT" --seeds "$SEEDS" --random-per-seed "$RANDOM_PER_SEED"

echo "[3/4] generate expected"
python3 scripts/model_eval.py --cases "$CASES_OUT" --out "$EXPECTED_OUT"

if [[ -f "$ACTUAL_IN" ]]; then
  echo "[4/4] diff expected vs actual"
  python3 scripts/diff.py --expected "$EXPECTED_OUT" --actual "$ACTUAL_IN" --out "$DIFF_OUT"
else
  echo "[4/4] skip diff: actual file not found -> $ACTUAL_IN"
  echo "Please export ISS/DUT results first, then rerun with ACTUAL_IN=<path>."
fi