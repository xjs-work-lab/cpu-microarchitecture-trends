# 第二十二轮来源卡：LLVM 代码生成与微架构调度模型（2026-10-23）

**研究模式：** PUBLIC_ONLY  
**用途：** 解释已确认的 CPU 微架构能力如何映射到 LLVM 的目标描述、指令选择、调度、寄存器分配、向量化和静态分析；不声称已验证目标手机的性能/能耗收益。  
**证据标签：** [FACT] 来源直接披露；[CLAIM] 来源自身主张；[OBSERVATION] 跨来源观察；[INFERENCE] 分析推论；[UNKNOWN] 公开证据不足。

## SRC22-01 — LLVM Target-Independent Code Generator

- **原始来源：** [The LLVM Target-Independent Code Generator](https://llvm.org/docs/CodeGenerator.html)
- **来源类型：** LLVM 官方编译器架构文档。
- **[FACT] 直接支持：** LLVM 代码生成包括目标指令选择、机器指令调度、虚拟寄存器到目标物理寄存器的分配、spill code 插入、函数序言/尾声与后期机器码优化。TargetSubtarget 向代码生成提供特定目标支持的指令、指令延迟和执行 itinerary（执行单元/使用顺序/持续时间）。
- **设计意义：** 微架构信息只有在目标描述、指令选择/调度启发式或 profile/feedback 能访问并使用时，才会影响 LLVM 的代码生成决策。
- **边界：** 文档说明的是编译器算法与接口，不证明某款手机上的目标调度模型准确，也不证明生成代码的实机收益。LLVM 分配的是 ISA 可见寄存器，不是 CPU 内部未公开的物理重命名寄存器池。

## SRC22-02 — LLVM MachineScheduler / Register Pressure

- **原始来源：** [LLVM MachineScheduler header / implementation docs](https://llvm.org/doxygen/MachineScheduler_8h_source.html)；[MachineScheduler.cpp](https://llvm.org/doxygen/MachineScheduler_8cpp.html)
- **来源类型：** LLVM 官方 API/实现文档。
- **[FACT] 直接支持：** MachineScheduler 构建指令依赖 DAG，并跟踪寄存器压力/活跃区间；目标可通过调度策略或 DAG mutation 提供特定调度启发式。寄存器压力变化是机器调度中的实际考虑项。
- **设计意义：** 调度器既要尽可能覆盖指令延迟、暴露 ILP，也要避免过度延长 live range，导致寄存器压力和后续 spill 增加。
- **边界：** 调度器的寄存器压力估计是编译期模型；它不直接观测目标核心内部的物理寄存器重命名容量、ROB 占用或动态发射队列状态。

## SRC22-03 — LLVM Loop Vectorizer / SLP Vectorizer

- **原始来源：** [Auto-Vectorization in LLVM](https://llvm.org/docs/Vectorizers.html)；[Vectorization Plan](https://llvm.org/docs/VectorizationPlan.html)
- **来源类型：** LLVM 官方优化文档。
- **[FACT] 直接支持：** Loop Vectorizer 扩宽连续循环迭代；SLP 合并可并行的标量操作；Loop Vectorizer 用 cost model 选择 vectorization factor（VF）与 unroll/interleave factor。文档明确指出，部分展开可暴露多个执行端口上的 ILP，但是否展开取决于寄存器压力和生成代码大小；复杂控制流、类型、调用、内存别名与 trip count 都可能限制收益。
- **设计意义：** 执行端口更宽/吞吐更高只是优化条件之一。LLVM 还必须判断循环是否可合法变换、是否值得扩宽、是否增加尾循环、运行时检查或 spill。
- **边界：** cost model 的估计不等于真实芯片测量；文档中的历史性能示例使用特定旧平台，不能直接外推到现代手机 CPU。

## SRC22-04 — Clang Profile-Guided Optimization（PGO）

- **原始来源：** [Clang Users Manual — Profile Guided Optimization](https://clang.llvm.org/docs/UsersManual.html#profile-guided-optimization)
- **来源类型：** Clang 官方用户手册。
- **[FACT] 直接支持：** profile 可提供指令执行计数、分支走向和函数调用频率；热分支可影响基本块排序，调用频率可影响 inlining。官方明确要求采集代表性 workload，否则未覆盖或比例失真的路径可能被错误地视为不重要。
- **设计意义：** PGO 让编译器利用真实 workload 的频率分布改善布局和内联，而不是让编译器直接读取硬件分支预测器内部表项。
- **边界：** PGO 不等于预测器结构建模；profile 的收益依赖代表性、部署工作负载变化、训练/使用版本一致性和额外流程成本。PGO 本身不证明某一分支预测器结构造成的因果收益。

## SRC22-05 — llvm-mca：静态性能与资源压力模型

- **原始来源：** [llvm-mca documentation](https://llvm.org/docs/CommandGuide/llvm-mca.html)
- **来源类型：** LLVM 官方工具文档。
- **[FACT] 直接支持：** llvm-mca 使用 LLVM 中的 scheduling model 静态估计给定机器码序列的 IPC 与资源压力，结果质量取决于模型质量。文档还明确说明其 LSUnit 不知道缓存层级/内存类型，不判断 load 命中还是未命中，不知道何时发生 store-to-load forwarding；load-to-use 延迟来自模型中的 optimistic latency，通常近似 L1D 命中场景。默认 load/store queue 大小可以是不受限的模型假设。
- **设计意义：** 这类工具可用于定位“在既定模型下”的端口压力和依赖链瓶颈，但不能单独证明真实手机的 cache-miss、DRAM、分支误预测、持续热或能耗表现。
- **边界：** 本研究的 PUBLIC_ONLY 范围不运行 benchmark、仿真或设备测量；这里只核验工具与模型的公开边界，不报告任何新跑分或模拟数值。

## SRC22-06 — AArch64 LLVM Processor Models：调度模型与 tune features 的区别

- **原始来源：** [AArch64Processors.td](https://github.com/llvm/llvm-project/blob/main/llvm/lib/Target/AArch64/AArch64Processors.td)；[AArch64.td](https://github.com/llvm/llvm-project/blob/main/llvm/lib/Target/AArch64/AArch64.td)
- **来源类型：** LLVM AArch64 后端 TableGen 源码。
- **[FACT] 直接支持（以 2026-10-23 可见的 LLVM main 源码为快照）：**
  - ProcessorModel 将 cortex-a76 关联到 NeoverseN1Model，并附加 A76 processor features 与 TuneA76。
  - cortex-a77 和 cortex-a78 关联到 NeoverseN2Model，同时分别附加 A77/A78 features 与 tune features。
  - TuneA76/TuneA77/TuneA78 还包含融合/指令选择等 tuning features；调度模型和 tune features 是不同层面的信息。
- **[OBSERVATION]** 该源码快照中 A76 使用 Neoverse N1 的 scheduler model，A77/A78 使用 Neoverse N2 的 scheduler model，同时配有各自的 tuning features。此事实表明 LLVM 的目标建模可组合/复用模型，而不必为每个商品核心都提供一套完全独立的资源模型。
- **边界：** 不能据此断言模型一定不准确，也不能断言 Cortex-A76 与 Neoverse N1、Cortex-A77/A78 与 Neoverse N2 的真实微架构完全相同。它只是 LLVM 当前公开建模的选择；评估精度需要独立的目标设备/负载证据。链接指向 main，源码会变动，后续比较应固定 LLVM 版本或 commit。

## SRC22-07 — AArch64 Cyclone scheduling model：模型参数是编译器假设的例子

- **原始来源：** [AArch64SchedCyclone.td](https://github.com/llvm/llvm-project/blob/main/llvm/lib/Target/AArch64/AArch64SchedCyclone.td)
- **来源类型：** LLVM AArch64 后端 TableGen 源码。
- **[FACT] 直接支持：** 当前文件定义 Cyclone scheduler model，包含 IssueWidth=6、MicroOpBufferSize=192、LoadLatency=4、MispredictPenalty=16，并定义整数、分支、load/store 与 FP/vector 资源。注释说明部分内容参考 Apple Cortex-A57/Cyclone tuning guide 的特定版本。
- **设计意义：** 公开的微架构参数可被编码成 LLVM 的指令延迟、资源冲突、发射宽度等模型，从而影响调度和 llvm-mca 的静态分析。
- **边界：** 这些值是 LLVM 模型参数，不自动等同于所有负载、所有硅片状态下的实测延迟/吞吐；尤其 LoadLatency 在模型中是乐观的 L1 命中口径。该例不应被拿来代表现代手机所有 Apple CPU。

## SRC22-08 — LLVM SME/SME2：架构状态、ABI 与 spill/reload

- **原始来源：** [Support for AArch64 SME in LLVM](https://www.llvm.org/docs/AArch64SME.html)；[AAPCS64](https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst)
- **来源类型：** LLVM 官方编译器文档与 Arm ABI 规范。
- **[FACT] 直接支持：** LLVM 将 SME streaming/ZA 相关属性映射为 IR 属性；根据函数/调用接口在调用边界插入 SMSTART/SMSTOP，并可能在状态切换前后 spill/reload 活跃的 FP/vector 值。状态切换会改变可用指令集合，且可能清零 FP/AdvSIMD/SVE 寄存器，因此 LLVM 必须尊重 ABI 与状态边界限制。
- **设计意义：** 这是“架构可见状态 → 编译器 lowering → 寄存器活跃区间/保存恢复”的直接可追溯案例。架构新增状态不只是增加一条指令，也可能改变调用边界和优化合法性。
- **边界：** 机制文档不提供目标手机上状态切换的周期、能耗或端到端收益；也不公开具体核心的内部物理寄存器容量。

## SRC22-09 — LLVM prefetch intrinsic

- **原始来源：** [LLVM Language Reference — llvm.prefetch](https://llvm.org/docs/LangRef.html#llvm-prefetch-intrinsic)
- **来源类型：** LLVM 官方 IR 语言参考。
- **[FACT] 直接支持：** llvm.prefetch 是给代码生成器的提示；若目标支持，可能生成预取指令，否则可成为 no-op。它不改变程序语义，但可能改变性能特征。
- **设计意义：** 编译器可在有可预测访问模式的场景插入/保留软件预取提示。
- **边界：** intrinsic 存在不证明目标硬件会按预期取入数据，更不证明它减少了真实负载的 stall/能耗。预取的及时性、精度、带宽和污染需要目标负载证据。

## 使用规则

1. 区分 ISA 特征可用性（如 -march/feature）、微架构调优（如 -mcpu/-mtune）、目标 scheduling model 与真实芯片的动态状态。
2. 目标调度模型是编译器可用的近似输入；不得把 llvm-mca 的 IPC/端口压力直接当成实测 IPC/端口利用率。
3. LLVM 物理寄存器分配指 ISA 可见寄存器类别；CPU 内部物理重命名寄存器数量、ROB/LSQ 的动态占用一般不作为直接编译器寄存器分配对象。
4. profile 是 workload 频率证据，不是分支预测器内部结构证据。
5. 向量化/展开必须同时检查 legality、cost model、live range/register pressure、spill、代码尺寸和循环尾部成本。
6. 源码/文档的链接、版本和日期应随 LLVM 版本更新；不能把一个 main 分支快照当成永恒规范。
