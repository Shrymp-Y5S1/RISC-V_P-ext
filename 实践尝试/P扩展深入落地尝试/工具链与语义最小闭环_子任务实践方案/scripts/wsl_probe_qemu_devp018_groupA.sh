#!/usr/bin/env bash
set -euo pipefail

WORK_ROOT="${WORK_ROOT:-$HOME/qemu-devp018-work}"
QSYS="$WORK_ROOT/qemu-src/build/qemu-system-riscv64"
QUSR="$WORK_ROOT/qemu-src/build/qemu-riscv64"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPORTS_DIR="$PROJECT_DIR/reports"
mkdir -p "$REPORTS_DIR"

TS="${TS:-$(date +%Y%m%d-%H%M%S)}"
REPORT_MD="$REPORTS_DIR/smoke-qemu-dev-p-018-groupA-system-probe-$TS.md"

if [[ ! -x "$QSYS" || ! -x "$QUSR" ]]; then
  echo "ERROR: expected binaries not found or not executable"
  echo "  QSYS=$QSYS"
  echo "  QUSR=$QUSR"
  echo "Hint: run scripts/wsl_build_qemu_devp018_dual_rootless.sh first"
  exit 1
fi

cat >"$REPORT_MD" <<EOF
# QEMU dev-p-018 组A（双目标后 system 探测）

- Time (UTC): $(date -u +"%Y-%m-%d %H:%M:%S UTC")
- WORK_ROOT: $WORK_ROOT
- QEMU user binary: $QUSR
- QEMU system binary: $QSYS

EOF

run_probe() {
  local title="$1"
  local cmd="$2"
  local out
  local rc

  set +e
  out="$(eval "$cmd" 2>&1)"
  rc=$?
  set -e

  if [[ -z "$out" ]]; then
    out="(no output)"
  fi

  {
    echo "### $title"
    echo
    echo '```bash'
    echo "$cmd"
    echo '```'
    echo
    echo '```text'
    echo "(exit=$rc)"
    echo "$out"
    echo '```'
    echo
  } >>"$REPORT_MD"
}

run_probe "system version" "$QSYS --version | head -n 1"
run_probe "user version" "$QUSR --version | head -n 1"

run_probe "system cpu models (-cpu help)" "$QSYS -cpu help"
run_probe "system cpu properties (max,help syntax check)" "$QSYS -cpu max,help"

QMP_CMDS="$(mktemp)"
cat >"$QMP_CMDS" <<'EOF'
{"execute":"qmp_capabilities"}
{"execute":"device-list-properties","arguments":{"typename":"max-riscv-cpu"}}
{"execute":"quit"}
EOF

run_probe \
  "system qmp device-list-properties (typename=max-riscv-cpu)" \
  "cat $QMP_CMDS | $QSYS -machine none -nographic -display none -S -monitor none -serial none -qmp stdio"

rm -f "$QMP_CMDS"

for opt in \
  "max,p=true,help" \
  "max,p=on,help" \
  "max,rvp=true,help" \
  "max,ext_p=true,help" \
  "max,x-p=true,help" \
  "max,p=0.18,help"; do
  run_probe "system probe (-cpu $opt)" "$QSYS -cpu $opt"
done

for opt in \
  "max,p=true" \
  "max,p=on" \
  "max,rvp=true" \
  "max,ext_p=true" \
  "max,x-p=true"; do
  run_probe \
    "system runtime probe (-machine none -cpu $opt, timeout 2s)" \
    "timeout 2s $QSYS -machine none -nographic -display none -S -monitor none -serial none -cpu $opt"
done

run_probe "user cpu models (-cpu help)" "$QUSR -cpu help"

for opt in \
  "max,p=true" \
  "max,p=on" \
  "max,rvp=true" \
  "max,ext_p=true" \
  "max,x-p=true"; do
  run_probe "user probe (-cpu $opt, no program)" "$QUSR -cpu $opt"
  run_probe "user probe (-cpu $opt /dev/null)" "$QUSR -cpu $opt /dev/null"
done

p_missing_count="$(grep -c "Property 'max-riscv-cpu.p' not found" "$REPORT_MD" || true)"
rvp_missing_count="$(grep -c "Property 'max-riscv-cpu.rvp' not found" "$REPORT_MD" || true)"
extp_missing_count="$(grep -c "Property 'max-riscv-cpu.ext_p' not found" "$REPORT_MD" || true)"
xp_missing_count="$(grep -c "Property 'max-riscv-cpu.x-p' not found" "$REPORT_MD" || true)"

{
  echo "## Quick Findings"
  echo
  echo "- p property missing occurrences: $p_missing_count"
  echo "- rvp property missing occurrences: $rvp_missing_count"
  echo "- ext_p property missing occurrences: $extp_missing_count"
  echo "- x-p property missing occurrences: $xp_missing_count"
  echo
  echo "## Notes"
  echo
  echo "- This report captures parser/CLI evidence only (Group A scope)."
  echo "- If needed, Group B can run minimal system bare-metal execution probes."
} >>"$REPORT_MD"

echo "report saved: $REPORT_MD"