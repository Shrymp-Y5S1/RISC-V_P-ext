#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

QEMU_BIN="${QEMU_BIN:-/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64}"
QEMU_CPU="${QEMU_CPU:-max,x-p=true}"
GCC_BIN="${GCC_BIN:-riscv64-linux-gnu-gcc}"

TMP_DIR="$(mktemp -d /tmp/vxsat-probe.XXXXXX)"
trap 'rm -rf "$TMP_DIR"' EXIT

cat > "$TMP_DIR/probe.S" <<'EOF'
.section .bss
.align 3
outbuf:
  .space 16

.section .text
.global _start
_start:
  # Saturating PSADD.B case: expected rd=0x7f7f7f7f and vxsat=1
  li a1, 0x7f7f7f7f
  li a2, 0x01010101
  li a0, 0
  .word 0x94C5853B

  la t0, outbuf
  sd a0, 0(t0)
  csrr t1, 0x009
  andi t1, t1, 1
  sd t1, 8(t0)

  li a0, 1
  la a1, outbuf
  li a2, 16
  li a7, 64
  ecall

  li a0, 0
  li a7, 93
  ecall
EOF

"$GCC_BIN" -nostdlib -static -march=rv64gc "$TMP_DIR/probe.S" -o "$TMP_DIR/probe.elf"
"$QEMU_BIN" -cpu "$QEMU_CPU" "$TMP_DIR/probe.elf" > "$TMP_DIR/out.bin"

python3 - <<PY
from pathlib import Path
b = Path("$TMP_DIR/out.bin").read_bytes()
rd = int.from_bytes(b[:8], "little") & 0xFFFFFFFF
v = int.from_bytes(b[8:16], "little") & 1
print(f"probe_rd=0x{rd:08x}")
print(f"probe_vxsat={v}")
PY
