# 第二十一轮：移动 CPU 核内机制证据审计（2026-10-23）

**状态：** MECHANISM_MATRIX_INITIAL / STRUCTURAL_SIGNAL / TERMINOLOGY_AUDIT_OPEN  
**分析主文：** [移动 CPU 核内机制证据矩阵 v0.1](../../03-analysis/移动CPU核内机制证据矩阵-v0.1-2026-10-23.md)  
**来源卡：** [第二十一轮核内微架构机制原始来源](../sources/round-21-核内微架构机制原始来源卡.md)

## 1. 审计目标

以公开来源为依据，建立移动 CPU 的前端/分支、乱序执行/重命名、执行端口、Load/Store、缓存与预取的第一版机制矩阵；不以性能分数推断隐藏硬件参数，也不把不同来源的同名指标假定为同一流水线阶段。

## 2. 关键主张审计

| ID | 主张 | 结论 | 证据等级/边界 |
|---|---|---|---|
| AU21-01 | Cortex-A9 已有乱序执行与寄存器重命名 | **确认（限定为部分乱序）** | Arm 官方 TRM/产品支持页描述双发射、部分乱序、重命名与动态分支预测。不能等同于后续深窗口全 OoO。 |
| AU21-02 | Cortex-A72 的 dispatch 是 5 µops/cycle | **保留术语/计量歧义，不作为统一定量结论** | Arm 工程博客称最多 5 条 µops/cycle 送至执行流水线；Arm 软件优化指南的 dispatch constraints 段又称从顺序段进入乱序段的 dispatch stage 最多 3 µops/cycle。A77 的官方优化指南明确区分 MOP/cycle 与 µOP/cycle，提示 A72 两份来源可能使用了不同术语或阶段定义；当前仍不能确认两者是否指同一计量项，故不拿该数字跨代排名。 |
| AU21-03 | Cortex-A76 每周期可“执行 8 条指令” | **不支持该简化表述** | 4-wide decode、4–8 条/cycle fetch、最多 8 operations/cycle dispatch、8 条执行流水线是不同指标；一个 macro-op 可能在 dispatch 时拆成两个 µops。实际 IPC 受依赖、分支、端口冲突与访存限制。 |
| AU21-04 | Cortex-A77 的 OOO window 是 160 项 ROB | **不支持此同义替换** | Arm 说 OOO window 160 instructions；来源未将其定义为 ROB entries。文档保留原始术语。 |
| AU21-05 | Apple Firestorm 的约 623 项就是 ROB，因此比 Cyclone 的 192 ROB 大约 3.2 倍 | **不支持** | Dougall Johnson 报告约 623 项 rename-retire queue 和约 330 项 coalesced retire queue；Firestorm 结构不同于传统 ROB。AnandTech 的早期分析使用“ROB”措辞，术语与模型需单独保留，不做简单比值。 |
| AU21-06 | Samsung M1→M6 平均 load latency 14.9→8.3 cycles 是硅片实测 | **不支持** | ISCA 2020 论文明确为 trace-driven cycle-accurate model，所有核心模拟在 2.6GHz；M5/M6 当时无可用硅片。数字是模型结果，并且汇总多个机制变化。 |
| AU21-07 | Samsung M5 UOC 可以减少取指/译码功耗 | **机制存在且动因有直接披露；净收益仍有边界** | ISCA 论文描述 384-µop UOC、最多 6 µops/cycle，并在 FetchMode 关闭 I-cache 与译码逻辑；作者将其主要动因之一写为节省重复热点 kernel 的 fetch/decode power。论文整体模型结果不能分离 UOC 的单独终端能耗贡献。 |
| AU21-08 | 预取器越激进，性能越好 | **不成立** | Samsung 论文明确讨论误预取的功耗、带宽和 cache capacity 成本，并采用动态 degree、确认机制、one-pass/two-pass 与置信度调节。 |
| AU21-09 | A78 的全部提升都来自更大执行结构 | **不成立** | Arm 描述其同时使用指令融合、预测结构优化和对部分低性能/面积收益结构的面积/功耗优化；官方收益数字仍是指定比较口径。 |
| AU21-10 | Qualcomm/Taishan 的未公开结构可由跑分推断 | **不支持** | 当前公开资料不足以建立同口径的 ROB/LSQ/端口/预测器数据；缺失保持 UNKNOWN。 |
| AU21-11 | Cortex-A77 的“6 instructions/cycle dispatch”与 µOP 吞吐相同 | **不支持这种简化** | Arm A77 工程博客称最多 6 instructions/cycle；A77 软件优化指南细分为最多处理 6 MOPs/cycle、派发最多 10 µOPs/cycle。必须保留 MOP 与 µOP 的单位/阶段差异。 |

## 3. 方法与来源独立性

- **Arm Cortex 资料：** 官方工程博客、TRM 与软件优化指南来自同一厂商体系。它们对结构披露具有直接性，但并非独立的性能因果复现；跨文档出现不一致时需保留来源差异。
- **Samsung Exynos 论文：** ISCA 2020 Industry Track，由描述的 SARC 团队成员参与撰写，提供独特工程披露。其 4,026 traces、统一 2.6GHz 的周期精确模拟增强了跨代结构分析的可比性，但 M5/M6 无硅片对比、M6 属模型对象，且多个机制变化累积，限制了量产能耗/因果归因。
- **Apple 逆向：** AnandTech 和 Dougall Johnson 使用不同年份、方法与内部队列术语。它们补足官方未公开内容，但不应被写成 Apple 确认规格；Firestorm 的非传统队列模型尤其不适合简单 ROB 数值排名。
- **Qualcomm/HiSilicon：** 公开资料透明度较低。当前证据只支持保留结构未知，不支持从产品表现补写未披露的内部细节。

## 4. 本轮结论的适用范围

- **可以使用：** 结构变化事实、设计者明确公开的动因、预取/前端/乱序机制的定性历史解释。
- **必须限定：** Arm 的跨代百分比、Apple 的逆向参数、Samsung 的模拟 IPC/load-latency 结果。
- **不能使用：** 以本轮材料对所有现代手机 CPU 做统一 IPC、能耗、ROB、分支预测器或“微架构先进性”排名；不能由缺乏公开文档推断厂商没有某种机制。

## 5. 下一步审计动作

1. 继续核对 A72 dispatch 术语差异及相关文档版本/上下文。
2. 深化 load-use latency、寄存器重命名、branch misprediction recovery 和端口占用的公开证据。
3. 建立“微架构结构—编译器可见特性—代码生成利用条件”的桥接表，避免将硬件峰值能力直接当作实际软件收益。
4. 保持 PUBLIC_ONLY；没有真机实测时只做文献推断，不声称已完成端侧实测验证。
