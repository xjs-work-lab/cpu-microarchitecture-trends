# 第二十二轮审计：微架构机制—LLVM 代码生成桥接（2026-10-23）

**状态：** BRIDGE_MATRIX_INITIAL / STRUCTURAL_SIGNAL / MODEL_FIDELITY_GAP_OPEN / PUBLIC_ONLY  
**主文：** [移动 CPU 微架构—LLVM 代码生成桥接矩阵 v0.1](../../03-analysis/移动CPU微架构与LLVM代码生成桥接矩阵-v0.1-2026-10-23.md)  
**来源卡：** [第二十二轮 LLVM/调度模型原始来源卡](../sources/round-22-LLVM代码生成与调度模型原始来源卡.md)

## 1. 审计问题

对第二十一轮中的前端、分支、执行资源、寄存器、访存/预取和 SIMD/SME 机制，审计 LLVM 能看到什么、能改变什么，以及静态模型无法证明什么。范围仅为公开文档和开源实现，不执行设备测量、benchmark、仿真或 PoC。

## 2. 关键主张审计

| ID | 主张 | 结论 | 证据等级与边界 |
|---|---|---|---|
| AU22-01 | LLVM 可以根据目标 CPU 的指令延迟/执行资源调度机器指令 | **确认** | LLVM CodeGenerator 文档说明 TargetSubtarget 提供目标指令、延迟和 execution itinerary；MachineScheduler 处理指令依赖与寄存器压力。它证明机制存在，不证明模型对每个手机 SKU 准确。 |
| AU22-02 | LLVM 的寄存器分配能看到 CPU 内部物理重命名寄存器池 | **不支持** | LLVM 将虚拟寄存器映射到 ISA 可见目标寄存器类或 spill slot；内部 rename PRF、ROB、LSQ 动态占用不属于一般 LLVM register allocator 的直接分配对象。 |
| AU22-03 | 更宽的执行端口必然让 LLVM 代码变快 | **不支持** | 向量化/展开可暴露 ILP，但成本模型也考虑寄存器压力和代码大小；数据依赖、访存供给、目标模型误差与实际负载会限制收益。 |
| AU22-04 | PGO 能直接重构硬件分支预测器 | **不支持** | PGO 获取运行时分支/函数频率，影响基本块排序和内联；它不是预测器内部表项的读取/训练接口。 |
| AU22-05 | llvm-mca 的 IPC/端口压力是实机测量 | **不支持** | 工具文档定义为基于 LLVM scheduling model 的静态估计；结果受模型质量影响。LSUnit 不知道 cache hierarchy、hit/miss 或 store-to-load forwarding。 |
| AU22-06 | LLVM 可以对任何目标保证软件预取有效 | **不支持** | llvm.prefetch 是 hint，目标支持时才可能生成指令，也不保证减少 stall、带宽消耗或能耗。 |
| AU22-07 | SME/ZA 的架构状态与调用边界会影响 LLVM lowering | **确认** | LLVM SME 文档直接给出属性映射、状态切换、调用边界与 spill/reload 示例；具体手机的周期/能耗代价仍未知。 |
| AU22-08 | LLVM 对每一代 Cortex-A76/A77/A78 都使用独立且完全准确的资源模型 | **不支持** | 当前可见 AArch64Processors.td 将 A76 关联至 NeoverseN1Model，A77/A78 关联至 NeoverseN2Model，另附对应 tune features。这是源码模型复用事实，不证明准确或不准确；必须审计 LLVM 版本和目标匹配。 |
| AU22-09 | 当前公开资料已证明 LLVM 优化在真实手机上带来特定净能耗收益 | **未建立证据** | 本轮只完成机制桥接与官方模型边界核验；没有真实手机测量、端到端 workload 数据或净能耗归因。 |

## 3. 关键的目标模型发现

### 3.1 AArch64 ProcessorModel 不是一列“芯片真相”

- 当前公开源码将 cortex-a76 映射至 NeoverseN1Model，cortex-a77 与 cortex-a78 映射至 NeoverseN2Model，并同时附加各自的 processor features 与 tuning features。
- **审计解释：** 要判断 LLVM 对某核心的代码生成是否“贴合”，需分别检查 ISA features、tuning features、scheduler model 的 latency/resource 参数与 LLVM 版本；不能只看 -mcpu 的名称。
- **边界：** 模型复用不自动等于错误，也不自动证明两个核心的微架构相同。

### 3.2 llvm-mca 的结果有明确的物理边界

- LLVM 文档明示，工具不建模真实 cache hierarchy、load hit/miss 与 store-to-load forwarding；load-to-use latency 是 scheduling model 提供的乐观值。
- 因此，对于本项目关心的手机持续热负载、cache/DRAM 争用、真实分支误预测和端到端能耗，静态 llvm-mca 不能单独作为结论证据。

## 4. 来源独立性与适用范围

- LLVM CodeGenerator、Vectorizers、llvm-mca、Clang PGO、SME 文档和 TableGen 源码均来自 LLVM 官方项目体系。它们对“实现了什么”具有直接性，但不构成独立手机性能复现。
- Arm AAPCS64/SME ABI 是架构/软件契约；它不披露具体手机核心的物理寄存器容量、内部队列和功耗。
- AArch64 schedule model 当前链接指向 main 分支；必须记录检查日期，后续需要对比时固定 LLVM tag/commit。
- 本轮没有将工具模型输出当成设备测量，也没有把缺失的手机数据补成推断数值。

## 5. 本轮结论适用范围

- **可以使用：** LLVM 目标描述、调度、寄存器分配、向量化、PGO、SME lowering 的公开实现机制；对 llvm-mca 适用边界的说明；特定源码快照中的 ProcessorModel 映射事实。
- **必须限定：** 目标调度模型对特定商品核心的精度；桌面/服务器与手机之间的迁移；PGO 的 workload 代表性；软件预取净收益。
- **不能使用：** 由静态模型直接宣称手机 IPC、能耗、持续性能、分支误预测率或 DRAM stall 改善；由 LLVM 的架构寄存器分配推断隐藏物理寄存器池。

## 6. 下一步审计动作

1. 固定 LLVM release/commit，核对目标手机常见 CPU 的 ProcessorModel、scheduler model、tuning features 和 latency/resource 来源。
2. 对关键 lowering 建立源码级证据：PGO/block placement、register pressure/spill、vectorizer cost model、prefetch intrinsic、SME streaming/ZA call boundary。
3. 将桥接矩阵与第二十一轮历史机制矩阵关联，逐条补“软件利用路径是否有直接证据”字段。
4. 继续维持 PUBLIC_ONLY；如需定量验证，必须先单独获得用户对执行模式的明确授权，并按项目范围重新评估。
