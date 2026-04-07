#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p build

riscv64-linux-gnu-gcc -c asm_l0/psadd_b_insn.S   -march=rv64gc -mabi=lp64d -o build/psadd_b_insn.o
riscv64-linux-gnu-gcc -c asm_l0/psshar_hs_insn.S -march=rv64gc -mabi=lp64d -o build/psshar_hs_insn.o
riscv64-linux-gnu-gcc -c asm_l0/pmulqr_h_insn.S  -march=rv64gc -mabi=lp64d -o build/pmulqr_h_insn.o
riscv64-linux-gnu-gcc -c asm_l0/pm2add_h_insn.S  -march=rv64gc -mabi=lp64d -o build/pm2add_h_insn.o

for name in psadd_b_insn psshar_hs_insn pmulqr_h_insn pm2add_h_insn; do
  echo "=== ${name} ==="
  riscv64-linux-gnu-objdump -d "build/${name}.o" | sed -n '1,20p'
done
