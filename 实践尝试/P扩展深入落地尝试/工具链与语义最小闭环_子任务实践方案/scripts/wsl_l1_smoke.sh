#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p build

compile_one() {
  local src="$1"
  local out="$2"
  local log="$3"

  if riscv64-linux-gnu-gcc -c "$src" -march=rv64gc -mabi=lp64d -o "$out" >"$log" 2>&1; then
    echo "OK   $(basename "$src")"
  else
    echo "FAIL $(basename "$src")"
    sed -n '1,2p' "$log"
  fi
}

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