# QEMU dev-p-018 组A（双目标后 system 探测）

- Time (UTC): 2026-04-20 11:08:49 UTC
- WORK_ROOT: /home/shrymp/qemu-devp018-work
- QEMU user binary: /home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64
- QEMU system binary: /home/shrymp/qemu-devp018-work/qemu-src/build/qemu-system-riscv64

### system version

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-system-riscv64 --version | head -n 1
```

```text
(exit=0)
QEMU emulator version 10.2.91
```

### user version

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64 --version | head -n 1
```

```text
(exit=0)
qemu-riscv64 version 10.2.91
```

### system cpu models (-cpu help)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-system-riscv64 -cpu help
```

```text
(exit=0)
Available CPUs:
  lowrisc-ibex
  max
  max32
  mips-p8700
  rv32
  rv32e
  rv32i
  rv64
  rv64e
  rv64i
  rva22s64
  rva22u64
  rva23s64
  rva23u64
  shakti-c
  sifive-e31
  sifive-e34
  sifive-e51
  sifive-u34
  sifive-u54
  thead-c906
  tt-ascalon
  veyron-v1
  x-rv128
  xiangshan-kunminghu
  xiangshan-nanhu
```

### system cpu properties (max,help syntax check)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-system-riscv64 -cpu max,help
```

```text
(exit=1)
qemu-system-riscv64: Expected key=value format, found help.
```

### system probe (-cpu max,p=true,help)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-system-riscv64 -cpu max,p=true,help
```

```text
(exit=1)
qemu-system-riscv64: Expected key=value format, found help.
```

### system probe (-cpu max,p=on,help)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-system-riscv64 -cpu max,p=on,help
```

```text
(exit=1)
qemu-system-riscv64: Expected key=value format, found help.
```

### system probe (-cpu max,rvp=true,help)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-system-riscv64 -cpu max,rvp=true,help
```

```text
(exit=1)
qemu-system-riscv64: Expected key=value format, found help.
```

### system probe (-cpu max,ext_p=true,help)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-system-riscv64 -cpu max,ext_p=true,help
```

```text
(exit=1)
qemu-system-riscv64: Expected key=value format, found help.
```

### system probe (-cpu max,x-p=true,help)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-system-riscv64 -cpu max,x-p=true,help
```

```text
(exit=1)
qemu-system-riscv64: Expected key=value format, found help.
```

### system probe (-cpu max,p=0.18,help)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-system-riscv64 -cpu max,p=0.18,help
```

```text
(exit=1)
qemu-system-riscv64: Expected key=value format, found help.
```

### system runtime probe (-machine none -cpu max,p=true, timeout 2s)

```bash
timeout 2s /home/shrymp/qemu-devp018-work/qemu-src/build/qemu-system-riscv64 -machine none -nographic -display none -S -monitor none -serial none -cpu max,p=true
```

```text
(exit=1)
qemu-system-riscv64: can't apply global max-riscv-cpu.p=true: Property 'max-riscv-cpu.p' not found
```

### system runtime probe (-machine none -cpu max,p=on, timeout 2s)

```bash
timeout 2s /home/shrymp/qemu-devp018-work/qemu-src/build/qemu-system-riscv64 -machine none -nographic -display none -S -monitor none -serial none -cpu max,p=on
```

```text
(exit=1)
qemu-system-riscv64: can't apply global max-riscv-cpu.p=on: Property 'max-riscv-cpu.p' not found
```

### system runtime probe (-machine none -cpu max,rvp=true, timeout 2s)

```bash
timeout 2s /home/shrymp/qemu-devp018-work/qemu-src/build/qemu-system-riscv64 -machine none -nographic -display none -S -monitor none -serial none -cpu max,rvp=true
```

```text
(exit=1)
qemu-system-riscv64: can't apply global max-riscv-cpu.rvp=true: Property 'max-riscv-cpu.rvp' not found
```

### system runtime probe (-machine none -cpu max,ext_p=true, timeout 2s)

```bash
timeout 2s /home/shrymp/qemu-devp018-work/qemu-src/build/qemu-system-riscv64 -machine none -nographic -display none -S -monitor none -serial none -cpu max,ext_p=true
```

```text
(exit=1)
qemu-system-riscv64: can't apply global max-riscv-cpu.ext_p=true: Property 'max-riscv-cpu.ext_p' not found
```

### system runtime probe (-machine none -cpu max,x-p=true, timeout 2s)

```bash
timeout 2s /home/shrymp/qemu-devp018-work/qemu-src/build/qemu-system-riscv64 -machine none -nographic -display none -S -monitor none -serial none -cpu max,x-p=true
```

```text
(exit=124)
qemu-system-riscv64: terminating on signal 15 from pid 452 (timeout)
```

### user cpu models (-cpu help)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64 -cpu help
```

```text
(exit=1)
Available CPUs:
  max
  mips-p8700
  rv64
  rv64e
  rv64i
  rva22s64
  rva22u64
  rva23s64
  rva23u64
  shakti-c
  sifive-e51
  sifive-u54
  thead-c906
  tt-ascalon
  veyron-v1
  xiangshan-kunminghu
  xiangshan-nanhu
```

### user probe (-cpu max,p=true, no program)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64 -cpu max,p=true
```

```text
(exit=1)
qemu: no user program specified
```

### user probe (-cpu max,p=true /dev/null)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64 -cpu max,p=true /dev/null
```

```text
(exit=1)
qemu-riscv64: can't apply global max-riscv-cpu.p=true: Property 'max-riscv-cpu.p' not found
```

### user probe (-cpu max,p=on, no program)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64 -cpu max,p=on
```

```text
(exit=1)
qemu: no user program specified
```

### user probe (-cpu max,p=on /dev/null)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64 -cpu max,p=on /dev/null
```

```text
(exit=1)
qemu-riscv64: can't apply global max-riscv-cpu.p=on: Property 'max-riscv-cpu.p' not found
```

### user probe (-cpu max,rvp=true, no program)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64 -cpu max,rvp=true
```

```text
(exit=1)
qemu: no user program specified
```

### user probe (-cpu max,rvp=true /dev/null)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64 -cpu max,rvp=true /dev/null
```

```text
(exit=1)
qemu-riscv64: can't apply global max-riscv-cpu.rvp=true: Property 'max-riscv-cpu.rvp' not found
```

### user probe (-cpu max,ext_p=true, no program)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64 -cpu max,ext_p=true
```

```text
(exit=1)
qemu: no user program specified
```

### user probe (-cpu max,ext_p=true /dev/null)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64 -cpu max,ext_p=true /dev/null
```

```text
(exit=1)
qemu-riscv64: can't apply global max-riscv-cpu.ext_p=true: Property 'max-riscv-cpu.ext_p' not found
```

### user probe (-cpu max,x-p=true, no program)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64 -cpu max,x-p=true
```

```text
(exit=1)
qemu: no user program specified
```

### user probe (-cpu max,x-p=true /dev/null)

```bash
/home/shrymp/qemu-devp018-work/qemu-src/build/qemu-riscv64 -cpu max,x-p=true /dev/null
```

```text
(exit=1)
(no output)
```

## Quick Findings

- p property missing occurrences: 4
- rvp property missing occurrences: 2
- ext_p property missing occurrences: 2
- x-p property missing occurrences: 0

## Notes

- This report captures parser/CLI evidence only (Group A scope).
- If needed, Group B can run minimal system bare-metal execution probes.
