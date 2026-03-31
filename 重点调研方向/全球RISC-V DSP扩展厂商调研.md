# 全球 RISC-V DSP 扩展厂商调研（公开证据版）

> 调研时间：2026-03-31  
> 调研口径：只采用“可公开验证”的证据（公司官网、官方仓库、官方文档、工具链官方文档）。

## 1. 调研目标

回答三个问题：

1. 目前全世界有哪些公司在“明确做 RISC-V DSP 扩展”。
2. 哪些公司在做 RISC-V，但证据更接近“向量/AI扩展”而非 DSP 扩展。
3. 若要把这件事做成长期跟踪，应该固定监控哪些信息源。

## 2. 判定口径（避免把 AI/向量误判为 DSP 扩展）

本报告将“做 RISC-V DSP 扩展”分为三类：

1. A类（明确）：官方资料直接出现 `DSP/SIMD`、`P-extension`、或等价的 DSP 指令扩展表述。
2. B类（间接）：官方资料显示有面向 DSP 的 vendor extension/指令库（如 MAC/VDOT/xxldsp），但未明确对外宣称“标准 P 扩展量产支持”。
3. C类（待核验/不充分）：仅看到 RISC-V + Vector/AI/可定制指令，暂无足够证据判定为 DSP 扩展。

## 3. 核心结论（先给结论）

1. 基于当前公开证据，A类厂商可明确落到：Andes、Nuclei。
2. B类厂商可落到：Alibaba T-Head（XTheadMac/XTheadVdot）、GreenWaves（自定义 RISC-V 扩展用于 DSP/AI 工作负载）。
3. 多家头部 RISC-V 公司当前公开表述仍偏 Vector/AI（如 SiFive、StarFive），不宜直接归类为“DSP 扩展公司”。
4. 该主题无法仅依赖 `P-ext-proposal.html` 完成，需要结合厂商产品页、SDK/编译选项、开源扩展规范与工具链版本说明。

## 4. 厂商证据分级表（公开可复核）

| 公司 | 总部/主要区域 | 公开证据摘要 | 判定 | 证据强度 |
| --- | --- | --- | --- | --- |
| Andes Technology | 中国台湾 | 官方 D25F 页面写明 `RISC-V P-extension (draft) DSP/SIMD ISA`，且标题即 `CPU Core with DSP` | A类 | 高 |
| Nuclei System | 中国/法国团队 | 官方产品页写 `RISC-V B/K/P/V -extensions`；官方 IAR 说明写 `enable P extension` 与 `Nuclei N300 DSP feature (P-ext 0.5.4)`；NMSIS 文档存在 `xxldsp`/N1/N2/N3 DSP 扩展编译口径 | A类 | 高 |
| Alibaba T-Head（XuanTie） | 中国 | 官方开源扩展规范包含 `XTheadMac`（Multiply-accumulate）与 `XTheadVdot`（四路8-bit乘加）等典型 DSP 指令族；同时维护 XThead vendor extensions | B类 | 中-高 |
| GreenWaves Technologies | 法国 | GAP SDK 官方 README 写明其 GNU 工具链支持“our extensions to the RISC-V ISA”，并面向 FFT/MFCC 等典型 DSP 工作负载 | B类 | 中 |
| SiFive | 美国 | 官方 X100/X200/X280 页面重点是 `RVV 1.0` + AI/ML Intelligence Extensions，未见明确 DSP/P 扩展宣称 | C类 | 高 |
| StarFive | 中国香港 | 官方页面强调 `RVA23` 与 `RVV1.0`，未见明确 DSP/P 扩展宣称 | C类 | 中 |
| Codasip | 欧洲（捷克） | 官方强调可定制指令与特定场景加速（如 motor control），但未见明确 DSP/P 扩展公开声明 | C类 | 中 |
| Bouffalo Lab | 中国 | 官方信息聚焦 AIoT SoC 与无线连接能力，未见明确 DSP/P 扩展公开说明 | C类 | 中-低 |

## 5. 可直接引用的关键证据（摘录）

## 5.1 Andes（A类）

1. `AndesCore™ D25F ... supports the RISC-V P-extension (draft) DSP/SIMD ISA`。
2. `Compact High-Speed 32-bit CPU Core with DSP`。

## 5.2 Nuclei（A类）

1. 产品页：`Excellent Scalability: RISC-V B/K/P/V -extensions`。
2. IAR 工程说明：`If you want to enable P extension, choose Xandesdsp ... link with P-ext 0.5.4 optimized library`。
3. NMSIS-DSP 文档：`_xxldsp`/`_xxldspn1x`/`_xxldspn2x`/`_xxldspn3x` 对应 Nuclei DSP 扩展组合。

## 5.3 T-Head（B类）

1. XuanTie 扩展规范公开：`XTheadMac` 为 `Multiply-accumulate instructions`。
2. `XTheadVdot` 提供 `vector integer four 8-bit multiply and add` 指令。

说明：当前公开证据更接近“已实现 DSP 类 vendor extension”，但不等同于“公开宣称完整标准 P 扩展产品化”。

## 5.4 GreenWaves（B类）

1. GAP SDK 明确写有“toolchain supports our extensions to the RISC-V ISA”。
2. 官方工具链与示例长期面向 FFT/MFCC/CNN 等 DSP/AI 任务。

说明：证据能证明其在做“RISC-V + DSP类扩展生态”，但是否对齐标准 P 扩展需进一步核验。

## 6. 这份清单如何用于立项决策

建议按“短期可接入”与“中长期跟踪”分层：

1. 短期优先跟踪：Andes、Nuclei（证据最完整，含 ISA 与工具链接口）。
2. 中期重点观察：T-Head、GreenWaves（有强烈 DSP 指令迹象，但标准口径与版本映射需补证）。
3. 对照组：SiFive、StarFive、Codasip（验证行业“向量/AI与DSP扩展”边界）。

## 7. 与“标准演进跟踪与边界管理”主题的关系

仅靠 `P-ext-proposal.html` 不能回答“哪个公司真正做了DSP扩展”，原因是：

1. 规范定义的是 ISA 草案，不定义各公司产品化路线与发布时间。
2. 厂商可能采用 vendor extension 或旧版 P 草案，不会在单一规范中反映。
3. 工具链支持往往滞后或分叉（编译器/SDK/ISS 不同版本并存）。

因此该主题必须并行跟踪：规范仓库 + 厂商资料 + 工具链版本。

## 8. 建议固定监控的信息源（可做月度巡检）

1. RISC-V P 扩展仓库：<https://github.com/riscv/riscv-p-spec>
2. RISC-V 官方文档页（P 扩展历史与定位）：<https://docs.riscv.org/reference/isa/v20240411/unpriv/p-st-ext.html>
3. LLVM RISC-V 扩展支持页：<https://llvm.org/docs/RISCVUsage.html>
4. Andes 官方处理器页（重点 D25F/相关DSP内核）：<https://www.andestech.com/en/products-solutions/andescore-processors/riscv-d25f/>
5. Nuclei 产品页与文档：<https://www.nucleisys.com/product.php>、<https://doc.nucleisys.com/nmsis/dsp/get_started.html>
6. XuanTie 扩展规范仓库：<https://github.com/XUANTIE-RV/thead-extension-spec>
7. GreenWaves GAP SDK：<https://github.com/GreenWaves-Technologies/gap_sdk>
8. StarFive/SiFive/Codasip 官网产品更新页（用于排除误判）：
   - <https://www.starfivetech.com/en/>
   - <https://www.sifive.com/cores/intelligence-x200-series>
   - <https://codasip.com/>

## 9. 你方若要补齐“全球完整名单”，建议主动补采这些资料

当前公开网页足够做“初版分级”，但要做到“完整全球名单 + 量产判断”，建议补采：

1. 厂商受限文档：部分资料需登录/FAE权限（例如 T-Head 技术资料页）。
2. 产品 brief 与编译器手册：尤其是 `-march` 扩展名与 intrinsic 列表。
3. RISC-V Summit 演讲资料：常出现尚未写入官网的路线图信息。
4. 商用 IP 授权信息：许多“做了 DSP 扩展”的项目只在客户 NDA 资料出现。
5. 关键联系人反馈：FAE/销售确认“是否量产、对应哪个草案版本、是否向后兼容”。

## 10. 组会可直接引用结论

1. “全球有哪些公司在做 RISC-V DSP 扩展”这件事，公开证据下可以先分三层，而不是给单一名单。
2. A类（明确）目前可稳定落到 Andes 与 Nuclei；B类（间接）重点是 T-Head 与 GreenWaves。
3. 许多头部公司公开口径仍是 Vector/AI，不应直接等同 DSP 扩展。
4. 该议题必须与“标准演进跟踪”并行推进，否则会出现规范版本与产业实现错位。

---

## 参考来源

1. <https://www.andestech.com/en/products-solutions/andescore-processors/riscv-d25f/>
2. <https://www.nucleisys.com/product.php>
3. <https://github.com/Nuclei-Software/nuclei-sdk/blob/master/ideprojects/iar/README.md>
4. <https://doc.nucleisys.com/nmsis/dsp/get_started.html>
5. <https://github.com/Nuclei-Software/NMSIS/releases>
6. <https://github.com/XUANTIE-RV/thead-extension-spec>
7. <https://raw.githubusercontent.com/XUANTIE-RV/thead-extension-spec/master/xtheadmac.adoc>
8. <https://raw.githubusercontent.com/XUANTIE-RV/thead-extension-spec/master/xtheadvdot.adoc>
9. <https://github.com/GreenWaves-Technologies/gap_sdk>
10. <https://raw.githubusercontent.com/GreenWaves-Technologies/gap_sdk/master/README.md>
11. <https://www.sifive.com/cores/intelligence-x200-series>
12. <https://www.starfivetech.com/en/>
13. <https://codasip.com/>
14. <https://www.bouffalolab.com/>
15. <https://github.com/riscv/riscv-p-spec>
16. <https://docs.riscv.org/reference/isa/v20240411/unpriv/p-st-ext.html>
17. <https://llvm.org/docs/RISCVUsage.html>