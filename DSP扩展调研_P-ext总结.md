# RISC-V P 扩展（DSP）公开内容与架构总结

> 资料来源：`调研材料/P-ext-proposal.html`（标题：Preliminary in-progress RISC-V "P" Extension）

## 1. 文档状态与结论先行

- 当前版本：`0.20-draft`（修订日期显示到 2026-03-17）。
- 文档明确声明：**Development state，内容可能变化**。
- 结论：这份资料可用于架构与指令族调研，但**不应直接视为冻结标准**，实现与产品规划应预留变更空间。

## 2. P 扩展定位

### 2.1 目标定位

P 扩展面向 DSP/多媒体/控制类负载，核心目标是：

- 用更少指令完成常见 DSP 内核（向量化风格但在通用整数寄存器上执行）
- 提升能效与吞吐
- 覆盖加减、移位、比较、饱和、乘法、乘加、归约等高频模式

### 2.2 依赖与适用架构

文档中明确：

- P 依赖：`Zmmul`、`Zba`、`Zbb`
- 适用：`RV32 (RV32E?)` 与 `RV64`

## 3. 整体架构思路（不是单条指令堆砌）

## 3.1 Packed-SIMD 计算模型

P 扩展核心是“打包 SIMD”（Packed SIMD）：

- 一个整数寄存器按元素宽度切分为多个 lane 并行计算
- 元素宽度主要用后缀表示：`.B`（8-bit）、`.H`（16-bit）、`.W`（32-bit）
- 同一条指令通常在所有 lane 上执行同构操作

## 3.2 RV32 的双宽寄存器对机制

P 在 RV32 中大量使用寄存器对（even-odd pair）表示双宽数据流：

- 指令字段：`rs1_p`、`rs2_p`、`rd_p`（4-bit，映射到偶/奇寄存器对）
- 语义上常等价于“对偶寄存器执行一次 + 对奇寄存器执行一次”
- 文档给出 `rd+ / rs1+ / rs2+` 记法；若基寄存器为 `x0`，其 `+` 仍视作 `x0`

这让 RV32 能实现很多 RV64 才能单寄存器完成的宽数据运算。

## 3.3 宽化、窄化与混合宽度

P 扩展在命名层面直接编码数据宽度流：

- 宽化：`WADD/WSUB/WMUL/...`，通常意味着目标是寄存器对
- 窄化：`NSRL/NCLIP/NSRAR/...`，通常意味着首源是寄存器对
- RV32 双宽后缀：`.DB/.DH/.DW`
- 混合宽度：如 `.H.B0`、`.W.H1`、`.H.B01`，表示在大元素中抽取子元素参与计算

## 3.4 饱和、舍入与 Q-format 语义

P 把 DSP 常用数值行为放进指令语义本身：

- 大量 `S`/`R`/`Q` 相关操作（饱和、舍入、Q-format）
- 例如 `MULQ`：按 Q-format 规则移位；极值相乘溢出场景通常做饱和处理
- 文档中更强调“**每条指令定义自己的数值语义**”

调研结论：在该提案文本中，未看到类似“统一舍入模式 CSR”的明确总控接口（至少在本次通读范围内无集中定义）。

## 3.5 与其他扩展关系

- 与 `V` 扩展在命名和语义上有呼应（如 mask set/reduction 的理念）
- 但 P 的执行载体是通用整数寄存器的 packed lanes，不是向量寄存器体系
- 与 `M/Zmmul` 在乘法语义有基础关联，但 P 提供更丰富的 DSP 组合形态

## 4. 指令内容版图（按功能族）

文档的 Detailed Instruction Descriptions 非常庞大，按功能可归纳为以下主族：

1. Load Immediate（打包立即数装载）
2. Basic Packed Add/Subtract
3. Saturating Add/Subtract
4. Averaging Add/Subtract
5. Shift-Add
6. Add-Subtract Cross
7. Absolute Difference / Saturating Absolute
8. Reduction Sum（含 double-wide）
9. Min/Max、Comparison
10. Sign Extension
11. Saturation/Clipping
12. Shift Operations
13. Saturating/Rounding Shift
14. Pair Operations
15. Zip/Unzip/Byte-Reverse
16. Misc Scalar / Double-wide Scalar Add/Sub
17. Widening Add/Sub、Widening Shift、Widening Zip
18. Narrowing Shift / Narrowing Clip
19. Multiply High（same-width）
20. Q-format Multiply
21. Multiply-High Accumulate
22. Q-format Multiply-Accumulate
23. Cross-element Multiply
24. Cross-element Multiply-Accumulate
25. PM2/PM4 Horizontal Multiply-Add/Sub
26. Mixed-width Multiply-High
27. Widening Multiply / Widening Multiply-Accumulate
28. Widening Q-format Multiply-Accumulate
29. Widening PM2 Multiply-Add/Sub
30. RV32 Double-Register Equivalences

可见它不是“少量补丁指令”，而是一套较系统的 DSP 指令簇。

## 5. 命名与编码规律（实现/译码最有用）

## 5.1 命名规律

- 基本形式：`P<operations>.<S>`
- 标量第二操作数：后缀再加 `S`（如 `.HS/.BS/.DHS`）
- 复合链操作按先后拼接（如 `MHRACC`）
- 乘法在链中常缩写：`MUL -> M`，`MULHR -> MHR`，`MULQ -> MQ` 等
- 横向归约常见标记：`2ADD`、`4ADD`、`2SUB`、`REDSUM/SUM`

## 5.2 编码层观察

- 文档每条指令都给了 Encoding + Pseudocode，适合直接做译码与 ISS 对照
- 常见主 opcode 族出现 `OP-32`、`OP-IMM-32` 及其变体
- 同一语义常给出 RV64 单寄存器形式 + RV32 寄存器对形式（便于跨 XLEN 对齐）

## 6. RV32 与 RV64 的关键差异

- `.W` packed 单寄存器语义通常是 RV64 专有（RV32 的单寄存器只有一个 32-bit lane）
- RV32 通过 `.D*` 和寄存器对承载双宽 packed 语义
- 许多 RV32 条目标注为 “register-pair format, RV32 only”

工程含义：

- 若产品线同时覆盖 RV32/RV64，建议将语义层抽象统一，再做后端映射（RV32 pair vs RV64 single-reg）。

## 7. 对“公开标准内容”的判断

从“公开可查”角度，这份文档提供了：

- 完整可浏览的功能分组
- 相当丰富的具体指令（助记符、编码、伪代码、描述）
- 明确的命名体系和跨宽度/跨寄存器形态规则

但从“标准成熟度”角度：

- 仍是 preliminary + draft + development 状态
- 文档自己提示未来章节位置仍会调整（如命名/约定章节预计 ratification 后转附录）

因此建议在报告中标注：

- **属于公开草案级规范，不等同于最终 ratified ISA**。

## 8. 对组内项目的落地建议

1. 建立“指令语义中间层”
- 先抽象 lane 语义（元素宽度、饱和、舍入、宽化/窄化）
- 再映射到 RV32/RV64 各自编码形态

2. 先做高价值子集
- 优先落地：饱和加减、移位+舍入、Q-format 乘法/乘加、横向乘加
- 这些是 DSP 内核最容易产生收益的子族

3. 把“变更管理”纳入计划
- 指令名或编码在草案阶段仍可能调整
- 测试基线建议同时记录“语义测试”和“编码测试”，便于后续改版迁移

4. 与编译器/汇编器同步推进
- 文档存在较多别名与形态规则，需尽早统一汇编语法约定
- 尤其是立即数、寄存器对、混合宽度后缀这些易错点

## 9. 一句话总结

RISC-V P 扩展在公开草案中已经展现出“面向 DSP 的系统化 packed-SIMD ISA 框架”：覆盖从基础算术到饱和/舍入、宽窄变换、Q-format 与横向乘加的完整指令族；其架构核心是 lane 化并行 + RV32 寄存器对机制 + 强语义命名规则，但当前仍处于 draft 开发态，工程落地必须按“可演进规范”处理。
