# QEMU dev-p-018 组A结论报告（双目标构建 + system 探测）

日期: 2026-04-20  
范围: 组A（构建打通 + CPU/属性可达性探测）

## 1. 构建状态

- 双目标 rootless 构建已成功完成：
  - qemu-riscv64: 10.2.91
  - qemu-system-riscv64: 10.2.91
- 构建脚本:
  - scripts/wsl_build_qemu_devp018_dual_rootless.sh

## 2. system 侧关键证据

- CPU 模型可枚举（包含 max/rv64 等）。
- 通过 QMP `device-list-properties` 查询 `max-riscv-cpu`，可见属性：
  - `x-p`（description: Packed-SIMD instructions, type: bool）
- 下列属性在 system 侧均报不存在：
  - `p`
  - `rvp`
  - `ext_p`

运行时探测（`-machine none` + `timeout 2s`）结果：

- `-cpu max,p=true` -> `Property 'max-riscv-cpu.p' not found`
- `-cpu max,rvp=true` -> `Property 'max-riscv-cpu.rvp' not found`
- `-cpu max,ext_p=true` -> `Property 'max-riscv-cpu.ext_p' not found`
- `-cpu max,x-p=true` -> 未出现属性错误，进程被 timeout 终止（说明参数被接受并进入运行等待）

## 3. user 侧补充证据

- `-cpu max,p=true /dev/null` 报 `Property 'max-riscv-cpu.p' not found`
- `-cpu max,rvp=true /dev/null` 报 `Property 'max-riscv-cpu.rvp' not found`
- `-cpu max,ext_p=true /dev/null` 报 `Property 'max-riscv-cpu.ext_p' not found`
- `-cpu max,x-p=true` 至少可通过参数解析阶段（无“属性不存在”报错）

## 4. 组A最终结论

1. 组A“构建打通”已完成：system/user 双二进制均可产出。  
2. 组A“属性探测”已完成：该分支启用 Packed-SIMD 的可见入口不是 `p`，而是 `x-p`。  
3. 当前可落地的后续尝试应以 `x-p` 口径推进，而不是 `p=true`。

## 5. 证据文件

- 完整探测报告（最新版）：
  - reports/smoke-qemu-dev-p-018-groupA-system-probe-20260420-190937.md
- 组A探测脚本：
  - scripts/wsl_probe_qemu_devp018_groupA.sh
- 双目标构建脚本：
  - scripts/wsl_build_qemu_devp018_dual_rootless.sh