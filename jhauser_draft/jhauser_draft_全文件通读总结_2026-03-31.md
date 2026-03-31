# jhauser_draft 全文件通读总结

> 日期：2026-03-31  
> 范围：jhauser_draft 目录全部文件（含 PDF）

## 1. 通读范围与方法

本次覆盖文件共 6 个：

- RVP-baseInstrs-020.pdf
- RVP-baseInstrs-A-020.pdf
- RVP-instrEncodings-020.pdf
- RVP-instrNames-020.pdf
- RVP-baseInstrs-Sail-020.txt
- RVP-baseInstrs-Sail-020_通读总结.md

执行方式：

- 对 `.txt` 和 `.md` 做全文读取与结构提取。
- 对 4 个 PDF 使用逐页文本抽取（总计 60 页）并建立 page map（每页首行/文本长度），再做关键词与标题级归纳。
- 对现有 `RVP-baseInstrs-Sail-020_通读总结.md` 做一致性复核。

## 2. 文件级结论

## 2.1 RVP-instrNames-020.pdf（命名规则基准）

定位：定义 P 扩展指令命名系统，强调“可读性优先于简写”。

核心内容：

- 先定义“标量 vs packed-SIMD”的分类标准。
- 给出 operation name、operation chain 的组合规则。
- 说明 packed 指令后缀体系（`.B/.H/.W`）、标量第二源后缀（`...S`）等。
- 涵盖 widening / narrowing / mixed-width 的命名拼接规则。
- 明确 RV32 双宽命名（`.D*`）及相关变体（含标量第二源）规则。

工程价值：

- 可作为汇编器助记符解析、文档自动生成、IR 到 asm 名称映射的上层规范。

## 2.2 RVP-instrEncodings-020.pdf（编码规则基准）

定位：定义 Base P 指令编码与格式分配。

核心内容：

- 给出指令格式总览。
- 区分“无寄存器对操作数”与“含寄存器对操作数（RV32）”编码区域。
- 编码表覆盖 RV32/RV64 分别分配，并与 instruction proposal 文档联动。

工程价值：

- 直接服务解码器位段设计、汇编器 operand checker、反汇编一致性检查。

## 2.3 RVP-baseInstrs-020.pdf（指令集合与选择原则）

定位：提出 Base P 的候选指令集合与分组原则。

核心结构（按页级主题）：

- 第 1 节：通用原则（Commonalities）。
- 第 2 节：非乘法类指令（含有/无 register pair 路径）。
- 第 3 节：乘法类指令（同样区分 pair 与非 pair）。

文档显式给出 v020 的增量方向：

- 增加 SHL/SHLR（作为 SHA/SHAR 的 unsigned 对应语义路径）。
- 增加 RV64 的 PNCLIPP/PNCLIPUP（B/H/W）族。
- 增加 PSSHL/PSSHLR 相关组合（含 RV32 双宽变体）。

工程价值：

- 适合作为“功能清单 + 优先子集切入”总入口。

## 2.4 RVP-baseInstrs-A-020.pdf（新旧草案映射）

定位：Annex A，对照“新提案指令名”与“早期 P 提案指令名”。

核心内容：

- 按类别给出新旧名称对应表（尤其便于从 v0.9.x 体系迁移）。
- v020 说明中强调：去除了已归入 Zba/Zbb 的重叠项映射，保留更聚焦的 P 范围。

工程价值：

- 对迁移、兼容层、历史代码映射非常关键。

## 2.5 RVP-baseInstrs-Sail-020.txt（语义实现底稿）

定位：大量 Base P 指令候选语义（Sail 风格），用于后续正式模型落地。

关键事实（全文统计）：

- 行数：4061
- 标题/语义小节：338
  - RV32 前缀：151
  - RV64 前缀：108
  - 通用：79
- 文本特征：
  - `vxsat = 1`：83 处
  - 舍入“+1 后取高位”模式：26 处
  - `rd_p` 保护写回：57 处
  - “等价展开为两条指令”块：14 处

关键语义脉络：

- 变长移位 + 饱和/舍入（PSSHL/PSSHLR/PSSHA/PSSHAR）是高密度核心。
- RV32 `.D*` 与 `.D*S` 等价展开规则明确，含“共享 rs2 时不得被中间覆盖”的执行约束。
- 窄化裁剪（PNCLIP 系列）、Q-format 与 PM2/PM4 归约乘加族语义完整。

风险提示（文档自带声明）：

- 作者明确说明该 Sail 代码未测试，可能有错误；应作为语义意图参考，不应直接视为最终金标准。

## 2.6 RVP-baseInstrs-Sail-020_通读总结.md（现有总结复核）

结论：

- 该文件对 `RVP-baseInstrs-Sail-020.txt` 的总结方向基本准确，覆盖了高价值语义主线。
- 但它只覆盖 Sail 文本，不覆盖同目录 4 个 PDF 的“命名体系 / 编码体系 / 指令总表 / 历史映射”维度。
- 本文档可视为对该总结的“目录级补全”。

## 3. 跨文档统一视图

从体系结构上看，5 份原始资料构成了完整闭环：

1. `RVP-instrNames-020.pdf`：定义“怎么命名”
2. `RVP-instrEncodings-020.pdf`：定义“怎么编码”
3. `RVP-baseInstrs-020.pdf`：定义“有哪些指令、为什么选它们”
4. `RVP-baseInstrs-Sail-020.txt`：定义“每条指令怎么执行”
5. `RVP-baseInstrs-A-020.pdf`：定义“与旧提案如何映射”

一致性观察：

- v020 新增点在多文档中相互呼应（SHL/SHLR、PSSHL*、RV64 PNCLIPP/UP）。
- RV32 寄存器对机制在命名、编码、语义三层保持一致。
- 语义层大量依赖饱和与舍入模板，便于抽象成公共函数实现。

## 4. 对后续工程的建议

1. 以“命名-编码-语义-历史映射”建立统一索引表。  
建议字段：`new_name | old_name | rv32/rv64 | encoding_template | sail_anchor | risk_level`。

2. 把 RV32 `.D<S>S` 的 rs2 生命周期约束列为强制验证项。  
这是跨文档反复出现的高风险点，不应仅在文档中备注。

3. 以 `RVP-baseInstrs-Sail-020.txt` 为语义蓝本时，必须做二次审校。  
先做小规模指令集（移位饱和、PNCLIP、PM2/PM4）闭环，再扩展全量。

4. 对历史项目迁移优先使用 Annex A。  
避免仅凭助记符直觉做新旧映射。

## 5. 结论

jhauser_draft 目录中的文件并非重复材料，而是分工明确的五层文档栈：

- Names（命名规则）
- Encodings（编码规则）
- BaseInstrs（功能集合）
- Sail（执行语义）
- Annex A（新旧映射）

如果要把 v020 草案真正转成“可实现、可验证、可迁移”的工程资产，这 5 层必须一起使用，不能只看其中任意一份。
