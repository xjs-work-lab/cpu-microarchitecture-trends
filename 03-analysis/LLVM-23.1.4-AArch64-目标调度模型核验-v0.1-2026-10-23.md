# LLVM 23.1.4 AArch64 目标调度模型核验 v0.1

**日期：** 2026-10-23  
**状态：** INITIAL_SOURCE_AUDIT / STRUCTURAL_SIGNAL / PUBLIC_ONLY  
**固定版本：** `llvmorg-23.1.4`  
**主事务：** [第23轮记录](../00-project/research-transactions/round-23-2026-10-23.md)

## 核心结论

LLVM 23.1.4 的 AArch64 后端并非为每一个 Cortex 核都配置完全独立的 scheduler model。多个处理器目标共享调度模型，但使用各自的处理器特征和 tuning feature 列表。模型内部部分参数被明确注明为乐观值、经验选择或从其他核心复制。

因此，**LLVM target 是编译器对目标 ISA 和调度行为的编码，不是该商品 CPU 微架构的完整规格表。** 模型共享本身不能证明两个核心相同；模型参数也不能直接用于给手机 SoC 排性能名次。

## 1. 固定 tag 下的目标映射

| Processor target | Scheduler model | Tune feature |
|---|---|---|
| Cortex-A72 | CortexA57Model | TuneA72 |
| Cortex-A76 | NeoverseN1Model | TuneA76 |
| Cortex-A77 / A78 | NeoverseN2Model | TuneA77 / TuneA78 |
| Cortex-A710 / A715 / A720 | NeoverseN2Model | 各自独立 Tune feature |
| Cortex-X1 | NeoverseV1Model | TuneX1 |
| Cortex-X2 / X3 | NeoverseV2Model | TuneX2 / TuneX3 |
| Cortex-X4 / X925 | NeoverseV3Model | TuneX4 / TuneX925 |

来源：[AArch64Processors.td @ llvmorg-23.1.4](https://github.com/llvm/llvm-project/blob/llvmorg-23.1.4/llvm/lib/Target/AArch64/AArch64Processors.td)（blob SHA: `550c72d2b1ad90bbe1a56c52bcf26bdeb674513e`）。

### 如何理解映射

- A72 使用 A57 调度模型，但单独采用 TuneA72；不能据此声称 A72 与 A57 的真实硬件相同。
- A76 使用 N1 模型，A77/A78 使用 N2 模型；同一模型内部参数被共享，而目标 tuning features 仍可不同。
- A710/A715/A720 也共用 N2 模型；X2/X3 共用 V2；X4/X925 共用 V3。
- 本矩阵仅记录 LLVM 23.1.4 的软件模型映射。实际手机还需进一步确认 SoC、CPU 核配置、编译工具链版本、构建参数及厂商定制。

## 2. Scheduler model 参数（源码中编码的数值）

| Model | IssueWidth | MicroOpBufferSize | LoadLatency | MispredictPenalty |
|---|---:|---:|---:|---:|
| CortexA57Model | 3 | 128 | 4 | 14 |
| NeoverseN1Model | 3 | 128 | 4 | 11 |
| NeoverseN2Model | 5 | 160 | 4 | 10 |
| NeoverseV1Model | 8 | 256 | 4 | 11 |
| NeoverseV2Model | 6 | 320 | 4 | 10 |
| NeoverseV3Model | 10 | 320 | 4 | 10 |

数值来源：
- [AArch64SchedA57.td](https://github.com/llvm/llvm-project/blob/llvmorg-23.1.4/llvm/lib/Target/AArch64/AArch64SchedA57.td) — SHA `9260379fb5b270c8bd632731cadc873d5a61740d`
- [AArch64SchedNeoverseN1.td](https://github.com/llvm/llvm-project/blob/llvmorg-23.1.4/llvm/lib/Target/AArch64/AArch64SchedNeoverseN1.td) — SHA `8847f32a9da9ad0d3ffe83d13cc2239232a42315`
- [AArch64SchedNeoverseN2.td](https://github.com/llvm/llvm-project/blob/llvmorg-23.1.4/llvm/lib/Target/AArch64/AArch64SchedNeoverseN2.td) — SHA `80151c644e7066e26bf0d1288bbb4615859b7168`
- [AArch64SchedNeoverseV1.td](https://github.com/llvm/llvm-project/blob/llvmorg-23.1.4/llvm/lib/Target/AArch64/AArch64SchedNeoverseV1.td) — SHA `0b3afa05789190031b8f34fb0f7706995b7e92c9`
- [AArch64SchedNeoverseV2.td](https://github.com/llvm/llvm-project/blob/llvmorg-23.1.4/llvm/lib/Target/AArch64/AArch64SchedNeoverseV2.td) — SHA `199a4ba0b392fd46b83317cf980a76a444afdf35`
- [AArch64SchedNeoverseV3.td](https://github.com/llvm/llvm-project/blob/llvmorg-23.1.4/llvm/lib/Target/AArch64/AArch64SchedNeoverseV3.td) — SHA `c061d4d9858a8e16493a8db9638fb469bf5da1fe`

**关键注释：**
- A57 与 N1 的 MicroOpBufferSize 均为 128；N1 源码注释说明该值复制自 Cortex-A76。
- N2 的 IssueWidth=5、V2 的 IssueWidth=6 均是调度模型选择；V2 注释指出更低值在经验测量中表现更好，不能用 IssueWidth 数值直接推断真实芯片宽度。
- V3 IssueWidth=10 的注释表述为预期略高于 V2；其 MicroOpBufferSize=320 明确复制自 V2。
- 各模型 LoadLatency=4 均标注为 optimistic load latency；这不是手机真实缓存命中/未命中延迟。
- V2/V3 的 MispredictPenalty=10 注释明确沿用 N2；不能把它当作各自实测的分支误预测恢复周期。

## 3. 对历史演进研究的意义

1. **硬件机制变化与编译器模型变化不是同一件事。** 核心的真实前端、乱序窗口或访存能力发生变化，不代表 LLVM 立即为该核建立独立模型。
2. **模型参数必须连同来源注释解读。** 参数可能来自公开规格、经验拟合、相邻模型复用或乐观假设；来源不同，证据等级不同。
3. **Tune features 是另一维度。** 即使 scheduler model 共用，融合启发式、调度器开关或循环交错因子等 tuning 仍可能分化。
4. **没有手机端定量结论。** 本轮未运行编译器、llvm-mca、benchmark、仿真或设备测试；没有测得任何 IPC、性能、能耗或持续负载结果。
5. **下一步必须做交叉映射。** 将 CPU 历史机制、产品上市时间、LLVM target、源码版本与可利用路径放在同一条证据链里，并保留实际设备匹配未知项。

## 4. 下一步

- 检查 Apple A 系列与 Qualcomm/Oryon 的 target/scheduler model 是否存在，及其模型参数公开程度。
- 在固定 tag 下追踪寄存器压力/spill、vectorizer cost model、PGO/block placement、prefetch 与 SME lowering 的关键实现。
- 回写第19轮历史时间线与第21轮核内机制矩阵，形成“历史变化—软件入口—模型限制—因果解释”的交叉索引。
