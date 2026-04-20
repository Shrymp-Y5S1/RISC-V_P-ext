# QEMU dev-p-018 组A（双目标后 system 探测）

- Time (UTC): 2026-04-20 12:42:59 UTC
- WORK_ROOT: /home/shrymp/qemu-devp020-work
- QEMU user binary: /home/shrymp/qemu-devp020-work/qemu-src/build/qemu-riscv64
- QEMU system binary: /home/shrymp/qemu-devp020-work/qemu-src/build/qemu-system-riscv64

### system version

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-system-riscv64 --version | head -n 1
```

```text
(exit=0)
QEMU emulator version 10.2.91
```

### user version

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-riscv64 --version | head -n 1
```

```text
(exit=0)
qemu-riscv64 version 10.2.91
```

### system cpu models (-cpu help)

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-system-riscv64 -cpu help
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
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-system-riscv64 -cpu max,help
```

```text
(exit=1)
qemu-system-riscv64: Expected key=value format, found help.
```

### system qmp device-list-properties (typename=max-riscv-cpu)

```bash
cat /tmp/tmp.hHTAqgjTMd | /home/shrymp/qemu-devp020-work/qemu-src/build/qemu-system-riscv64 -machine none -nographic -display none -S -monitor none -serial none -qmp stdio
```

```text
(exit=0)
{"QMP": {"version": {"qemu": {"micro": 91, "minor": 2, "major": 10}, "package": ""}, "capabilities": ["oob"]}}
{"return": {}}
{"return": [{"name": "memory", "type": "link<memory-region>"}, {"name": "start-powered-off", "type": "bool"}, {"name": "num-pmp-regions", "description": "num-pmp-regions", "type": "uint8"}, {"default-value": true, "name": "debug", "description": "on/off", "type": "bool"}, {"name": "pmu-num", "description": "pmu-num", "type": "int8"}, {"default-value": false, "name": "rvv_vl_half_avl", "description": "on/off", "type": "bool"}, {"default-value": 0, "name": "rnmi-interrupt-vector", "type": "uint64"}, {"name": "elen", "description": "elen", "type": "uint16"}, {"name": "priv_spec", "description": "priv_spec", "type": "str"}, {"name": "cbom_blocksize", "description": "cbom_blocksize", "type": "uint16"}, {"name": "mmu", "description": "mmu", "type": "bool"}, {"default-value": 4096, "name": "resetvec", "type": "uint64"}, {"default-value": false, "name": "rvv_vsetvl_x0_vill", "description": "on/off", "type": "bool"}, {"default-value": false, "name": "rvv_ta_all_1s", "description": "on/off", "type": "bool"}, {"default-value": 0, "name": "rnmi-exception-vector", "type": "uint64"}, {"name": "pmp-granularity", "description": "pmp-granularity", "type": ""}, {"default-value": false, "name": "rvv_ma_all_1s", "description": "on/off", "type": "bool"}, {"name": "cboz_blocksize", "description": "cboz_blocksize", "type": "uint16"}, {"name": "vext_spec", "description": "vext_spec", "type": "str"}, {"name": "cbop_blocksize", "description": "cbop_blocksize", "type": "uint16"}, {"default-value": false, "name": "x-misa-w", "description": "on/off", "type": "bool"}, {"name": "vlen", "description": "vlen", "type": "uint16"}, {"name": "pmp", "description": "pmp", "type": "bool"}, {"name": "pmu-mask", "description": "pmu-mask", "type": "int8"}, {"name": "mvendorid", "description": "mvendorid", "type": "uint32"}, {"default-value": false, "name": "short-isa-string", "description": "on/off", "type": "bool"}, {"name": "mimpid", "description": "mimpid", "type": "uint64"}, {"name": "marchid", "description": "marchid", "type": "uint64"}, {"name": "zvkt", "type": "bool"}, {"name": "ssccfg", "type": "bool"}, {"name": "unnamed-gpio-in[4]", "type": "child<irq>"}, {"name": "sstc", "type": "bool"}, {"name": "zknh", "type": "bool"}, {"name": "zicbom", "type": "bool"}, {"name": "unnamed-gpio-in[16]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[53]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[90]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[97]", "type": "child<irq>"}, {"name": "zvks", "type": "bool"}, {"name": "zihintpause", "type": "bool"}, {"name": "unnamed-gpio-in[106]", "type": "child<irq>"}, {"name": "smmpm", "type": "bool"}, {"name": "zfhmin", "type": "bool"}, {"name": "zfbfmin", "type": "bool"}, {"name": "unnamed-gpio-in[21]", "type": "child<irq>"}, {"name": "xventanacondops", "type": "bool"}, {"name": "unnamed-gpio-in[28]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[65]", "type": "child<irq>"}, {"name": "rva22s64", "type": "bool"}, {"name": "unnamed-gpio-in[111]", "type": "child<irq>"}, {"name": "zbkc", "type": "bool"}, {"name": "unnamed-gpio-in[118]", "type": "child<irq>"}, {"name": "zkne", "type": "bool"}, {"name": "riscv.cpu.rnmi[3]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[33]", "type": "child<irq>"}, {"name": "zicsr", "type": "bool"}, {"name": "unnamed-gpio-in[70]", "type": "child<irq>"}, {"name": "zbkb", "type": "bool"}, {"name": "unnamed-gpio-in[77]", "type": "child<irq>"}, {"name": "zknd", "type": "bool"}, {"name": "zbc", "type": "bool"}, {"name": "unnamed-gpio-in[123]", "type": "child<irq>"}, {"name": "m", "description": "Integer multiplication and division", "type": "bool"}, {"name": "zbb", "type": "bool"}, {"name": "xtheadcmo", "type": "bool"}, {"name": "riscv.cpu.rnmi[10]", "type": "child<irq>"}, {"name": "svadu", "type": "bool"}, {"name": "smpmpmt", "type": "bool"}, {"name": "unnamed-gpio-in[45]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[82]", "type": "child<irq>"}, {"name": "sscofpmf", "type": "bool"}, {"name": "unnamed-gpio-in[89]", "type": "child<irq>"}, {"name": "zama16b", "type": "bool"}, {"name": "zvkn", "type": "bool"}, {"name": "unnamed-gpio-in[1]", "type": "child<irq>"}, {"name": "zfh", "type": "bool"}, {"name": "zba", "type": "bool"}, {"name": "unnamed-gpio-in[8]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[13]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[50]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[57]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[94]", "type": "child<irq>"}, {"name": "zawrs", "type": "bool"}, {"name": "zk", "type": "bool"}, {"name": "xlrbr", "type": "bool"}, {"name": "unnamed-gpio-in[103]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[25]", "type": "child<irq>"}, {"name": "svpbmt", "type": "bool"}, {"name": "i", "description": "Base integer instruction set", "type": "bool"}, {"name": "unnamed-gpio-in[62]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[69]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[115]", "type": "child<irq>"}, {"name": "h", "description": "Hypervisor", "type": "bool"}, {"name": "smrnmi", "type": "bool"}, {"name": "zfinx", "type": "bool"}, {"name": "riscv.cpu.rnmi[0]", "type": "child<irq>"}, {"name": "xtheadfmemidx", "type": "bool"}, {"name": "unnamed-gpio-in[30]", "type": "child<irq>"}, {"name": "riscv.cpu.rnmi[7]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[37]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[74]", "type": "child<irq>"}, {"name": "g", "description": "General purpose (IMAFD_Zicsr_Zifencei)", "type": "bool"}, {"name": "unnamed-gpio-in[120]", "type": "child<irq>"}, {"name": "smepmp", "type": "bool"}, {"name": "zve64f", "type": "bool"}, {"name": "f", "description": "Single-precision float point", "type": "bool"}, {"name": "unnamed-gpio-in[42]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[49]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[86]", "type": "child<irq>"}, {"name": "riscv.cpu.rnmi[14]", "type": "child<irq>"}, {"name": "svvptc", "type": "bool"}, {"name": "e", "description": "Base integer instruction set (embedded)", "type": "bool"}, {"name": "zve32f", "type": "bool"}, {"name": "sv57", "type": "bool"}, {"name": "zvkg", "type": "bool"}, {"name": "unnamed-gpio-in[5]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[10]", "type": "child<irq>"}, {"name": "zve64d", "type": "bool"}, {"name": "zfa", "type": "bool"}, {"name": "unnamed-gpio-in[17]", "type": "child<irq>"}, {"name": "d", "description": "Double-precision float point", "type": "bool"}, {"name": "unnamed-gpio-in[54]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[91]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[100]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[98]", "type": "child<irq>"}, {"name": "zkt", "type": "bool"}, {"name": "unnamed-gpio-in[107]", "type": "child<irq>"}, {"name": "c", "description": "Compressed instructions", "type": "bool"}, {"name": "zcf", "type": "bool"}, {"name": "unnamed-gpio-in[22]", "type": "child<irq>"}, {"name": "xtheadbb", "type": "bool"}, {"name": "unnamed-gpio-in[29]", "type": "child<irq>"}, {"name": "zks", "type": "bool"}, {"name": "unnamed-gpio-in[66]", "type": "child<irq>"}, {"name": "b", "description": "Bit manipulation (Zba_Zbb_Zbs)", "type": "bool"}, {"name": "rva23u64", "type": "bool"}, {"name": "zce", "type": "bool"}, {"name": "unnamed-gpio-in[112]", "type": "child<irq>"}, {"name": "zvkng", "type": "bool"}, {"name": "xtheadba", "type": "bool"}, {"name": "xtheadmemidx", "type": "bool"}, {"name": "unnamed-gpio-in[119]", "type": "child<irq>"}, {"name": "xtheadfmv", "type": "bool"}, {"name": "zkr", "type": "bool"}, {"name": "a", "description": "Atomic instructions", "type": "bool"}, {"name": "riscv.cpu.rnmi[4]", "type": "child<irq>"}, {"name": "zcd", "type": "bool"}, {"name": "unnamed-gpio-in[34]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[71]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[78]", "type": "child<irq>"}, {"name": "zclsd", "type": "bool"}, {"name": "unnamed-gpio-in[124]", "type": "child<irq>"}, {"name": "svnapot", "type": "bool"}, {"name": "zvkb", "type": "bool"}, {"name": "xtheadmempair", "type": "bool"}, {"name": "zalasr", "type": "bool"}, {"name": "zcb", "type": "bool"}, {"name": "unnamed-gpio-in[46]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[83]", "type": "child<irq>"}, {"name": "riscv.cpu.rnmi[11]", "type": "child<irq>"}, {"name": "rva23s64", "type": "bool"}, {"name": "smctr", "type": "bool"}, {"name": "unnamed-gpio-in[2]", "type": "child<irq>"}, {"name": "zvknc", "type": "bool"}, {"name": "zca", "type": "bool"}, {"name": "unnamed-gpio-in[9]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[14]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[51]", "type": "child<irq>"}, {"name": "zksh", "type": "bool"}, {"name": "zcmop", "type": "bool"}, {"name": "unnamed-gpio-in[58]", "type": "child<irq>"}, {"name": "zkn", "type": "bool"}, {"name": "unnamed-gpio-in[95]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[104]", "type": "child<irq>"}, {"name": "xmipslsp", "type": "bool"}, {"name": "svade", "type": "bool"}, {"name": "unnamed-gpio-in[26]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[63]", "type": "child<irq>"}, {"name": "ztso", "type": "bool"}, {"name": "zdinx", "type": "bool"}, {"name": "unnamed-gpio-in[116]", "type": "child<irq>"}, {"name": "smnpm", "type": "bool"}, {"name": "riscv.cpu.rnmi[1]", "type": "child<irq>"}, {"name": "zvknhb", "type": "bool"}, {"name": "unnamed-gpio-in[31]", "type": "child<irq>"}, {"name": "riscv.cpu.rnmi[8]", "type": "child<irq>"}, {"name": "zvfbfmin", "type": "bool"}, {"name": "unnamed-gpio-in[38]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[75]", "type": "child<irq>"}, {"name": "smdbltrp", "type": "bool"}, {"name": "unnamed-gpio-in[121]", "type": "child<irq>"}, {"name": "zifencei", "type": "bool"}, {"name": "zvknha", "type": "bool"}, {"name": "unnamed-gpio-in[43]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[80]", "type": "child<irq>"}, {"name": "zksed", "type": "bool"}, {"name": "smstateen", "type": "bool"}, {"name": "unnamed-gpio-in[87]", "type": "child<irq>"}, {"name": "riscv.cpu.rnmi[15]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[11]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[6]", "type": "child<irq>"}, {"name": "supm", "type": "bool"}, {"name": "zaamo", "type": "bool"}, {"name": "ssdbltrp", "type": "bool"}, {"name": "zilsd", "type": "bool"}, {"name": "xtheadmac", "type": "bool"}, {"name": "unnamed-gpio-in[18]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[55]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[92]", "type": "child<irq>"}, {"name": "xtheadcondmov", "type": "bool"}, {"name": "unnamed-gpio-in[99]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[101]", "type": "child<irq>"}, {"name": "zvfbfwma", "type": "bool"}, {"name": "unnamed-gpio-in[108]", "type": "child<irq>"}, {"name": "zbkx", "type": "bool"}, {"name": "ssctr", "type": "bool"}, {"name": "zvkned", "type": "bool"}, {"name": "unnamed-gpio-in[23]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[60]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[67]", "type": "child<irq>"}, {"name": "sv64", "type": "bool"}, {"name": "zimop", "type": "bool"}, {"name": "unnamed-gpio-in[113]", "type": "child<irq>"}, {"name": "sspm", "type": "bool"}, {"name": "zalrsc", "type": "bool"}, {"name": "riscv.cpu.rnmi[5]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[35]", "type": "child<irq>"}, {"name": "zihintntl", "type": "bool"}, {"name": "unnamed-gpio-in[72]", "type": "child<irq>"}, {"name": "zihpm", "type": "bool"}, {"name": "sv39", "type": "bool"}, {"name": "unnamed-gpio-in[79]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[125]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[40]", "type": "child<irq>"}, {"name": "x-p", "description": "Packed-SIMD instructions", "type": "bool"}, {"name": "ssnpm", "type": "bool"}, {"name": "unnamed-gpio-in[47]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[84]", "type": "child<irq>"}, {"name": "riscv.cpu.rnmi[12]", "type": "child<irq>"}, {"name": "smaia", "type": "bool"}, {"name": "unnamed-gpio-in[3]", "type": "child<irq>"}, {"name": "zcmt", "type": "bool"}, {"name": "unnamed-gpio-in[15]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[52]", "type": "child<irq>"}, {"name": "zicboz", "type": "bool"}, {"name": "unnamed-gpio-in[59]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[96]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[105]", "type": "child<irq>"}, {"name": "xmipscmov", "type": "bool"}, {"name": "xmipscbop", "type": "bool"}, {"name": "unnamed-gpio-in[20]", "type": "child<irq>"}, {"name": "zbs", "type": "bool"}, {"name": "smcsrind", "type": "bool"}, {"name": "unnamed-gpio-in[27]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[64]", "type": "child<irq>"}, {"name": "zvksh", "type": "bool"}, {"name": "unnamed-gpio-in[110]", "type": "child<irq>"}, {"name": "x-svukte", "type": "bool"}, {"name": "xtheadsync", "type": "bool"}, {"name": "unnamed-gpio-in[117]", "type": "child<irq>"}, {"name": "zvksg", "type": "bool"}, {"name": "riscv.cpu.rnmi[2]", "type": "child<irq>"}, {"name": "zvbc", "type": "bool"}, {"name": "unnamed-gpio-in[32]", "type": "child<irq>"}, {"name": "svinval", "type": "bool"}, {"name": "riscv.cpu.rnmi[9]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[39]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[76]", "type": "child<irq>"}, {"name": "zvbb", "type": "bool"}, {"name": "unnamed-gpio-in[122]", "type": "child<irq>"}, {"name": "sscsrind", "type": "bool"}, {"name": "zcmp", "type": "bool"}, {"name": "zvfhmin", "type": "bool"}, {"name": "zvfh", "type": "bool"}, {"name": "zicfiss", "type": "bool"}, {"name": "unnamed-gpio-in[44]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[81]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[88]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[0]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[93]", "type": "child<irq>"}, {"name": "zve64x", "type": "bool"}, {"name": "unnamed-gpio-in[7]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[12]", "type": "child<irq>"}, {"name": "svrsw60t59b", "type": "bool"}, {"name": "unnamed-gpio-in[19]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[56]", "type": "child<irq>"}, {"name": "smcdeleg", "type": "bool"}, {"name": "zvksc", "type": "bool"}, {"name": "unnamed-gpio-in[102]", "type": "child<irq>"}, {"name": "zve32x", "type": "bool"}, {"name": "zicfilp", "type": "bool"}, {"name": "unnamed-gpio-in[109]", "type": "child<irq>"}, {"name": "ssaia", "type": "bool"}, {"name": "zmmul", "type": "bool"}, {"name": "unnamed-gpio-in[24]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[61]", "type": "child<irq>"}, {"name": "zabha", "type": "bool"}, {"name": "v", "description": "Vector operations", "type": "bool"}, {"name": "unnamed-gpio-in[68]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[114]", "type": "child<irq>"}, {"name": "zicntr", "type": "bool"}, {"name": "u", "description": "User-level instructions", "type": "bool"}, {"name": "zvksed", "type": "bool"}, {"name": "riscv.cpu.rnmi[6]", "type": "child<irq>"}, {"name": "zicbop", "type": "bool"}, {"name": "unnamed-gpio-in[36]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[73]", "type": "child<irq>"}, {"name": "zhinx", "type": "bool"}, {"name": "smcntrpmf", "type": "bool"}, {"name": "zicond", "type": "bool"}, {"name": "unnamed-gpio-in[126]", "type": "child<irq>"}, {"name": "xtheadbs", "type": "bool"}, {"name": "zhinxmin", "type": "bool"}, {"name": "sv48", "type": "bool"}, {"name": "unnamed-gpio-in[41]", "type": "child<irq>"}, {"name": "s", "description": "Supervisor-level instructions", "type": "bool"}, {"name": "zacas", "type": "bool"}, {"name": "rva22u64", "type": "bool"}, {"name": "unnamed-gpio-in[48]", "type": "child<irq>"}, {"name": "unnamed-gpio-in[85]", "type": "child<irq>"}, {"name": "riscv.cpu.rnmi[13]", "type": "child<irq>"}]}
{"timestamp": {"seconds": 1776688979, "microseconds": 854253}, "event": "SHUTDOWN", "data": {"guest": false, "reason": "host-qmp-quit"}}
{"return": {}}
```

### system probe (-cpu max,p=true,help)

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-system-riscv64 -cpu max,p=true,help
```

```text
(exit=1)
qemu-system-riscv64: Expected key=value format, found help.
```

### system probe (-cpu max,p=on,help)

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-system-riscv64 -cpu max,p=on,help
```

```text
(exit=1)
qemu-system-riscv64: Expected key=value format, found help.
```

### system probe (-cpu max,rvp=true,help)

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-system-riscv64 -cpu max,rvp=true,help
```

```text
(exit=1)
qemu-system-riscv64: Expected key=value format, found help.
```

### system probe (-cpu max,ext_p=true,help)

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-system-riscv64 -cpu max,ext_p=true,help
```

```text
(exit=1)
qemu-system-riscv64: Expected key=value format, found help.
```

### system probe (-cpu max,x-p=true,help)

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-system-riscv64 -cpu max,x-p=true,help
```

```text
(exit=1)
qemu-system-riscv64: Expected key=value format, found help.
```

### system probe (-cpu max,p=0.18,help)

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-system-riscv64 -cpu max,p=0.18,help
```

```text
(exit=1)
qemu-system-riscv64: Expected key=value format, found help.
```

### system runtime probe (-machine none -cpu max,p=true, timeout 2s)

```bash
timeout 2s /home/shrymp/qemu-devp020-work/qemu-src/build/qemu-system-riscv64 -machine none -nographic -display none -S -monitor none -serial none -cpu max,p=true
```

```text
(exit=1)
qemu-system-riscv64: can't apply global max-riscv-cpu.p=true: Property 'max-riscv-cpu.p' not found
```

### system runtime probe (-machine none -cpu max,p=on, timeout 2s)

```bash
timeout 2s /home/shrymp/qemu-devp020-work/qemu-src/build/qemu-system-riscv64 -machine none -nographic -display none -S -monitor none -serial none -cpu max,p=on
```

```text
(exit=1)
qemu-system-riscv64: can't apply global max-riscv-cpu.p=on: Property 'max-riscv-cpu.p' not found
```

### system runtime probe (-machine none -cpu max,rvp=true, timeout 2s)

```bash
timeout 2s /home/shrymp/qemu-devp020-work/qemu-src/build/qemu-system-riscv64 -machine none -nographic -display none -S -monitor none -serial none -cpu max,rvp=true
```

```text
(exit=1)
qemu-system-riscv64: can't apply global max-riscv-cpu.rvp=true: Property 'max-riscv-cpu.rvp' not found
```

### system runtime probe (-machine none -cpu max,ext_p=true, timeout 2s)

```bash
timeout 2s /home/shrymp/qemu-devp020-work/qemu-src/build/qemu-system-riscv64 -machine none -nographic -display none -S -monitor none -serial none -cpu max,ext_p=true
```

```text
(exit=1)
qemu-system-riscv64: can't apply global max-riscv-cpu.ext_p=true: Property 'max-riscv-cpu.ext_p' not found
```

### system runtime probe (-machine none -cpu max,x-p=true, timeout 2s)

```bash
timeout 2s /home/shrymp/qemu-devp020-work/qemu-src/build/qemu-system-riscv64 -machine none -nographic -display none -S -monitor none -serial none -cpu max,x-p=true
```

```text
(exit=124)
qemu-system-riscv64: terminating on signal 15 from pid 9009 (timeout)
```

### user cpu models (-cpu help)

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-riscv64 -cpu help
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
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-riscv64 -cpu max,p=true
```

```text
(exit=1)
qemu: no user program specified
```

### user probe (-cpu max,p=true /dev/null)

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-riscv64 -cpu max,p=true /dev/null
```

```text
(exit=1)
qemu-riscv64: can't apply global max-riscv-cpu.p=true: Property 'max-riscv-cpu.p' not found
```

### user probe (-cpu max,p=on, no program)

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-riscv64 -cpu max,p=on
```

```text
(exit=1)
qemu: no user program specified
```

### user probe (-cpu max,p=on /dev/null)

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-riscv64 -cpu max,p=on /dev/null
```

```text
(exit=1)
qemu-riscv64: can't apply global max-riscv-cpu.p=on: Property 'max-riscv-cpu.p' not found
```

### user probe (-cpu max,rvp=true, no program)

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-riscv64 -cpu max,rvp=true
```

```text
(exit=1)
qemu: no user program specified
```

### user probe (-cpu max,rvp=true /dev/null)

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-riscv64 -cpu max,rvp=true /dev/null
```

```text
(exit=1)
qemu-riscv64: can't apply global max-riscv-cpu.rvp=true: Property 'max-riscv-cpu.rvp' not found
```

### user probe (-cpu max,ext_p=true, no program)

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-riscv64 -cpu max,ext_p=true
```

```text
(exit=1)
qemu: no user program specified
```

### user probe (-cpu max,ext_p=true /dev/null)

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-riscv64 -cpu max,ext_p=true /dev/null
```

```text
(exit=1)
qemu-riscv64: can't apply global max-riscv-cpu.ext_p=true: Property 'max-riscv-cpu.ext_p' not found
```

### user probe (-cpu max,x-p=true, no program)

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-riscv64 -cpu max,x-p=true
```

```text
(exit=1)
qemu: no user program specified
```

### user probe (-cpu max,x-p=true /dev/null)

```bash
/home/shrymp/qemu-devp020-work/qemu-src/build/qemu-riscv64 -cpu max,x-p=true /dev/null
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
