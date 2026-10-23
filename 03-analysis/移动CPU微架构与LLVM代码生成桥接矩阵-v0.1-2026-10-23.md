# 移动 CPU 微架构—LLVM 代码生成桥接矩阵 v0.1

**更新：2026-10-23｜研究模式：PUBLIC_ONLY｜证据成熟度：STRUCTURAL_SIGNAL**  
**研究目标：** 把第二十一轮已确认的 CPU 核内机制与 LLVM 的可见信息、优化入口和收益边界连接起来；继续解释历史因果，不把本轮变成新的技术立项清单。  
**来源卡：** [第二十二轮 LLVM/调度模型原始来源](../02-evidence/sources/round-22-LLVM代码生成与调度模型原始来源卡.md)。  
**范围：** AArch64 / LLVM / Clang / MLIR；不研究 GCC，不运行真机测试、benchmark、仿真或 PoC。

## 1. 核心结论

**[OBSERVATION] LLVM 可以利用的是 ISA/ABI、目标后端模型、代码依赖图、静态成本估计和 workload profile；它通常不能直接读取目标 CPU 内部物理寄存器重命名池、实时 ROB/LSQ 占用、动态分支预测器状态或真实 cache/DRAM miss 状态。**

**[INFERENCE] 因此，微架构演进转化为编译器收益有三条不同路径：**
1. **直接映射：** ISA 指令/状态或 ABI 规则发生变化，LLVM 可以直接选择指令或实施状态/调用约束。
2. **模型驱动：** 目标 scheduler model 提供延迟、资源、融合和成本启发式，LLVM 据此安排指令、选择向量宽度/展开因子，但收益受模型精度限制。
3. **反馈驱动：** PGO 或外部 profiling 提供真实 workload 的热度/分支频率，LLVM 优化布局、内联等；它得到的是行为频率，不是隐藏硬件内部状态。
4. **不可直接映射：** 未公开的物理寄存器池、ROB/LSQ 动态状态、cache 命中与 DRAM 争用通常需要硬件性能计数器、动态运行证据或更强的系统模型；不能靠静态 LLVM IR 或单一 llvm-mca 结果反推出。

## 2. 桥接矩阵

| 微架构机制/历史变化 | LLVM 能直接看到什么 | LLVM/Clang 的相关机制 | 何时可能获益 | 主要成本/失效条件 | 证据与边界 |
|---|---|---|---|---|---|
| **ISA 指令与扩展能力** | ISA/CPU feature、目标数据布局、可用寄存器类和指令约束 | AArch64 指令选择、目标特征、-march/-mcpu/-mtune 相关的 feature 与 tuning 决策 | 新指令能表达热点操作，且目标/部署设备支持该扩展；目标选择与实际设备匹配 | 错误的目标参数可能生成不兼容指令；有指令不等于 LLVM 一定选择它或 workload 一定受益 | [FACT] LLVM TargetSubtarget 与后端源码公开了目标指令、延迟和资源描述；不是产品性能证明 |
| **前端供给、宏操作融合与指令带宽** | 指令序列、目标特定融合/成本特征、代码尺寸与控制流 | 指令选择、peephole、目标 fusion tuning、基本块布局与内联 | 代码形态符合目标融合规则，或布局减少冷代码/无用指令；热点指令供给与后端需求匹配 | 编译器一般不掌握运行时 µop-cache/BTB 命中状态；内联/展开可能增大代码 footprint，导致 I-cache/前端压力 | [FACT] AArch64 后端有如 FeatureCmpBccFusion、FeatureFuseAdrpAdd 等 tuning feature；不能把这些 feature 当成完整的硬件前端仿真 |
| **分支预测与误预测恢复** | 静态控制流、profile 提供的分支频率/热度 | PGO、分支权重、基本块排序、函数内联和部分控制流变换 | profile 与真实部署负载相符，热点路径被合理布局，分支/函数频率稳定 | profile 不代表预测器内部表项；训练负载失真、工作负载漂移、代码膨胀和分支依赖会削弱收益 | [FACT] Clang PGO 文档说明分支频率影响块排序；[INFERENCE] 这不是对特定 CPU predictor 的建模或直接控制 |
| **执行端口、发射资源与指令延迟** | 目标调度模型中的指令 latency、resource、issue/throughput 等描述 | SelectionDAG/MachineScheduler、目标调度启发式、指令选择、llvm-mca 静态资源压力分析 | 有独立指令可重排，目标模型能描述主要延迟/端口冲突，生成代码避免长依赖链或单端口热点 | 模型与真实芯片不一致、动态 OoO 能力、频率/功耗状态、缓存 miss 和实际输入都会影响结果；编译器调度不等于硬件发射调度 | [FACT] LLVM TargetSubtarget 提供延迟/执行 itinerary；[FACT] llvm-mca 的结果质量依赖模型质量。它不证明实机 IPC |
| **寄存器重命名、架构寄存器与内部物理寄存器** | ISA 可见的 GPR/SIMD/SVE/SME 寄存器类别、调用约定、虚拟寄存器活跃区间 | Register allocation、live intervals、register-pressure-aware scheduling、spill/reload、copy coalescing | 缩短 live range、减少不必要复制/溢出；合理平衡 unroll/vectorization 和可用架构寄存器 | LLVM 不直接分配内部物理 rename registers；过度展开/向量化会增加 live values，导致架构寄存器压力、spill/reload 和栈流量 | [FACT] LLVM CodeGenerator 文档明确虚拟寄存器映射到目标寄存器/内存并可能插入 spill；隐藏 PRF/ROB 容量仍是 UNKNOWN |
| **Load-use 延迟、LSQ 与内存级并行度（MLP）** | 静态数据依赖、已知 alias/内存效果、目标 load latency 模型 | 指令调度、别名分析、循环变换、展开/向量化、特定场景的软件预取提示 | 存在可重排的独立 loads；编译器能证明无依赖/无别名；展开产生的并行请求能被系统承载 | 指针追踪/真实地址依赖、alias 不确定、队列/带宽限制、缓存 miss、DRAM 延迟和争用；编译器不能仅凭 ISA 得知实际 MLP | [FACT] llvm-mca 不建模 cache hierarchy、命中/未命中或 store-to-load forwarding；其 load latency 是模型的乐观口径 |
| **Cache/TLB 与硬件预取器** | 可推导的访问顺序、循环步长、部分 locality/alias 信息；显式 prefetch intrinsic | Loop transformations、vectorization、llvm.prefetch（目标支持时可生成指令，否则可能 no-op） | 地址流可预测、预取有足够提前量、访问数据确实会被使用，且额外带宽成本可接受 | 误预取、缓存污染、带宽/队列争用、访问延迟波动；静态提示不能确定运行时缓存状态 | [FACT] LLVM LangRef 将 prefetch 定义为 hint；intrinsic 存在不证明端到端性能/能耗改善 |
| **SIMD/向量吞吐与执行资源** | ISA vector features、操作类型、循环依赖/别名、trip count 与成本模型 | Loop Vectorizer、SLP Vectorizer、VF/UF cost model、interleaving、reduction lowering | 数据并行、依赖可证明安全、循环足够长，目标向量指令成本有利且寄存器压力可控 | 复杂控制流、短循环、scalar epilogue、runtime checks、向量转换、寄存器压力/溢出、代码尺寸和带宽限制 | [FACT] LLVM 官方文档明确 cost model 同时考虑 VF/UF、寄存器压力与代码尺寸；向量宽度不等于实测加速倍数 |
| **SME/ZA 等架构状态与 ABI** | 函数/调用的 streaming、ZA 属性、可用指令约束、架构状态生命周期 | Clang 属性 → LLVM IR attributes → SelectionDAG lowering；调用边界 SMSTART/SMSTOP、状态相关 spill/reload 与优化限制 | 调用边界和状态生命周期清晰，热计算段可在兼容状态下执行并摊薄状态管理成本 | 状态转换、活跃向量值保存/恢复、调用约束、非兼容指令与 inline/tail-call 限制 | [FACT] LLVM SME 文档直接给出 lowering 规则和汇编示例；未给出目标手机实际切换周期/能耗 |
| **热点代码与 workload 特征** | profile 中的指令/分支/函数频率，采样或插桩数据 | PGO、内联、基本块排序及其他 profile-guided 决策 | profile 能代表线上负载，并且代码布局/内联改善热点路径 | profile 收集成本、代表性不足、工作负载漂移、热度不等于微架构 stall 来源 | [FACT] PGO 使用频率而非预测器内部状态；需把 workload 代表性单独审计 |

## 3. 本轮重要的直接源码发现

### 3.1 LLVM 的目标模型是“微架构事实的编码”，不是芯片本身

- **[FACT]** LLVM AArch64Processors.td 当前可见源码把 cortex-a76 关联到 NeoverseN1Model，把 cortex-a77 和 cortex-a78 关联到 NeoverseN2Model，另附各自的 tuning features。
- **[INFERENCE]** 因此分析这些目标的 LLVM 静态代码生成时，必须区分“调度资源/延迟模型”和“特定 CPU 的调优特征”。仅看到 -mcpu=cortex-a76 并不意味着每个微架构资源参数都来自一套独立的 Cortex-A76 模型。
- **边界：** 这不是说 LLVM 模型必然错误，也不是说 Cortex-A76 与 Neoverse N1 硅片等同。它是当前 LLVM 源码的建模选择；模型对实际手机的精度仍需独立证据。当前链接指向 main，后续需固定版本再比较。

### 3.2 Cyclone 展示了微架构参数如何进入后端模型

- **[FACT]** LLVM 的 Cyclone schedule model 公开编码了 6 µops/cycle issue width、192 µop buffer、4-cycle optimistic load latency、16-cycle mispredict penalty，并对整数/分支/访存/向量资源做区分。
- **[INFERENCE]** 当硬件资料足够公开时，编译器可把某些机制转化为调度模型输入；模型参数会影响静态性能估计和代码调度。
- **边界：** 模型数字不等于每种真实负载的硅片实测；Cyclone 是历史核心案例，不代表现代手机核通用行为。

### 3.3 llvm-mca 能分析一部分后端瓶颈，但不能代替真实内存系统

- **[FACT]** 官方文档指出 llvm-mca 估算 IPC 与资源压力，结果依赖 LLVM scheduling model；它不知道真实 cache hierarchy、load hit/miss 和 store-to-load forwarding。
- **[INFERENCE]** 对纯计算、指令依赖链和执行资源竞争，它可以提供模型内的诊断线索；对指针追踪、冷缓存、DRAM 争用、热/功耗降频等问题，不能把静态估算当作终端结论。
- **本轮约束：** 本轮未运行 llvm-mca、benchmark、仿真或真机测试；仅审计其公开定义与适用边界。

## 4. 历史因果解释：硬件变化如何传到软件

| 历史硬件变化 | 编译器可利用的通道 | 中间限制 | 可以谨慎得出的结论 |
|---|---|---|---|
| 更高的执行带宽/更多端口 | 目标延迟/资源模型、ILP 暴露、循环展开和向量化 | 数据依赖、寄存器压力、代码大小、内存供给 | 只有存在独立操作且模型/代码变换匹配时，增加的硬件宽度才可能被利用 |
| 更大的乱序窗口/更多在途 load/store | 编译器可暴露独立 loads、缩短依赖链、改变循环结构 | 硬件动态窗口对编译器不可见；alias、真实 miss 和 MLP 不可由静态模型完整获知 | LLVM 可以减少不必要的串行化，但不能仅靠静态代码保证填满真实窗口 |
| 更强的分支预测/更大的 BTB | PGO 代码布局、分支权重、减少冷路径进入热路径 | profile 与真实 workload 的代表性、实际预测器内部状态未知 | PGO 是软件行为反馈，不等于直接调优预测器表项 |
| 更高的 SIMD/SVE/SME 能力 | 指令选择、Loop/SLP vectorization、SME attributes/ABI lowering | 可用 ISA、数据并行性、向量化合法性、状态/调用成本、spill | 新硬件特性需要编译器支持与负载可向量化两者同时成立 |
| 更复杂的缓存/预取 | locality-aware loop transformations、显式 prefetch hints | cache hierarchy/DRAM 动态状态、带宽竞争、误预取成本 | 软件预取只是提示，不能替代动态测量，也不能把预取指令数当成性能指标 |

## 5. 可公开审计的证据检查清单

后续若需进一步核验某个编译器收益，最低需要公开记录：
1. LLVM/Clang 精确版本、目标 triple、-march/-mcpu/-mtune 和功能开关；
2. 源代码/IR、优化 remarks、最终汇编，以及调用约定/ABI 假设；
3. workload、输入规模、profile 的采集与使用版本；
4. 目标 CPU/SoC/手机是否真实匹配该调度模型，若无法确认则明确标注；
5. 结果层级：静态成本估计、微基准、内核调用、算子 aggregate、端到端应用、设备 QoE 或能耗；
6. 基线是否使用同一编译器版本、同一 target model、同一正确性约束；
7. 是否检查 spill/reload、代码尺寸、尾循环、运行时 alias checks 和预取副作用；
8. 是否有证据区分微架构因素与制程、频率、OS、运行时、散热和负载变化。

本轮未采集任何新设备数据，因此当前可成立的是机制桥接与证据边界，而不是定量性能因果结论。

## 6. 阶段性结论

**[OBSERVATION]** LLVM 与微架构之间并非“硬件变强，编译器自动变快”的直接映射，而是由目标特征/调度模型、依赖图、寄存器分配、成本模型与 workload profile 共同中介。

**[INFERENCE]** 最容易建立直接证据链的是 ISA/ABI 可见变化和 LLVM 明确实现的 lowering 规则；最容易产生过度外推的是隐藏的 ROB/LSQ/物理寄存器资源、动态分支预测状态和 cache/DRAM 行为。

**[UNKNOWN]** 公开资料仍不足以证明当前 LLVM 调度模型对所有手机 SKU、厂商定制核和实际混合负载都准确；也不足以仅凭静态成本模型量化各机制的手机端净能耗收益。

## 7. 下一步

1. 固定 LLVM release/commit，核对目标手机常见 CPU 的 ProcessorModel、scheduler model、tuning features 和指令延迟来源。
2. 从公开编译器实现与文档继续审计 branch layout/PGO、register pressure/spill、loop vectorization、prefetch 和 SME 状态边界的真实 lowering 规则。
3. 把桥接结果回写历史时间线，解释哪些历史硬件变化有直接软件利用路径，哪些只是硬件能力而缺少公开的 LLVM/手机端效果证据。
4. 维持 PUBLIC_ONLY；不运行真机、benchmark、仿真或 PoC，也不从桌面/服务器结果直接推导手机净能耗收益。
