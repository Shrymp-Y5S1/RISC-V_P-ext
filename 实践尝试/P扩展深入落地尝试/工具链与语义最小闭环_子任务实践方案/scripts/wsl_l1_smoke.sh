#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p build

TOOLCHAIN="${L1_TOOLCHAIN:-clang}"
PASS=0
FAIL=0
P_VERSION=""

detect_clang_bin() {
  if [[ -n "${CLANG_BIN:-}" ]]; then
    echo "$CLANG_BIN"
    return 0
  fi

  for c in clang-22 clang-21 clang-20 clang-19 clang; do
    if command -v "$c" >/dev/null 2>&1; then
      echo "$c"
      return 0
    fi
  done

  return 1
}

probe_clang_p_support() {
  local clang_bin="$1"
  P_VERSION="$($clang_bin --target=riscv64-unknown-elf --print-supported-extensions \
    | awk '/^[[:space:]]*p[[:space:]]+[0-9]+\.[0-9]+/{print $2; exit}')"

  if [[ -z "$P_VERSION" ]]; then
    echo "ERROR clang toolchain does not expose experimental P extension."
    echo "HINT  Use a clang build that contains RISCV experimental-p support."
    return 1
  fi

  return 0
}

compile_one() {
  local src="$1"
  local out="$2"
  local log="$3"
  local rc=0

  if [[ "$TOOLCHAIN" == "clang" ]]; then
    local clang_bin="${CLANG_BIN}"
    local clang_target="${CLANG_TARGET:-riscv64-unknown-elf}"
    local p_suffix="${P_VERSION/./p}"
    local clang_march="${CLANG_MARCH:-rv64i_p${p_suffix}}"
    local clang_mabi="${CLANG_MABI:-lp64}"
    "$clang_bin" --target="$clang_target" -menable-experimental-extensions \
      -march="$clang_march" -mabi="$clang_mabi" \
      -c "$src" -o "$out" >"$log" 2>&1 || rc=$?
  else
    riscv64-linux-gnu-gcc -c "$src" -march=rv64gc -mabi=lp64d -o "$out" >"$log" 2>&1 || rc=$?
  fi

  if [[ "$rc" -eq 0 ]]; then
    echo "OK   $(basename "$src")"
    PASS=$((PASS + 1))
  else
    echo "FAIL $(basename "$src")"
    sed -n '1,2p' "$log"
    FAIL=$((FAIL + 1))
  fi
}

if [[ "$TOOLCHAIN" == "clang" ]]; then
  CLANG_BIN="$(detect_clang_bin || true)"
  if [[ -z "$CLANG_BIN" ]]; then
    echo "ERROR clang binary not found. Set CLANG_BIN explicitly."
    exit 2
  fi
  probe_clang_p_support "$CLANG_BIN" || exit 2
elif [[ "$TOOLCHAIN" != "gnu" ]]; then
  echo "ERROR unsupported L1_TOOLCHAIN='$TOOLCHAIN' (expected: clang or gnu)"
  exit 2
fi

echo "L1 smoke toolchain: $TOOLCHAIN"
if [[ "$TOOLCHAIN" == "clang" ]]; then
  echo "L1 smoke clang bin: $CLANG_BIN"
  echo "L1 smoke detected P version: $P_VERSION"
fi

compile_one asm_l1/psadd_b_mnemonic.S   build/psadd_b_mnemonic.o   build/psadd_b_mnemonic.log
compile_one asm_l1/pssub_b_mnemonic.S   build/pssub_b_mnemonic.o   build/pssub_b_mnemonic.log
compile_one asm_l1/psshar_hs_mnemonic.S build/psshar_hs_mnemonic.o build/psshar_hs_mnemonic.log
compile_one asm_l1/psshlr_hs_mnemonic.S build/psshlr_hs_mnemonic.o build/psshlr_hs_mnemonic.log
compile_one asm_l1/pmulq_h_mnemonic.S   build/pmulq_h_mnemonic.o   build/pmulq_h_mnemonic.log
compile_one asm_l1/pmulqr_h_mnemonic.S  build/pmulqr_h_mnemonic.o  build/pmulqr_h_mnemonic.log
compile_one asm_l1/pm2add_h_mnemonic.S  build/pm2add_h_mnemonic.o  build/pm2add_h_mnemonic.log
compile_one asm_l1/pm2adda_h_mnemonic.S build/pm2adda_h_mnemonic.o build/pm2adda_h_mnemonic.log
compile_one asm_l1/pm4add_b_mnemonic.S  build/pm4add_b_mnemonic.o  build/pm4add_b_mnemonic.log
compile_one asm_l1/pm4adda_b_mnemonic.S build/pm4adda_b_mnemonic.o build/pm4adda_b_mnemonic.log

echo "SUMMARY total=10 pass=$PASS fail=$FAIL"
if [[ "$FAIL" -gt 0 ]]; then
  exit 1
fi