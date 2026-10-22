# CPU 微架构与 LLVM 深化支线：范围锁定与领域地图（2026-10-22）

**状态：SCOPE_LOCKED_FOR_PUBLIC_EVIDENCE_DISCOVERY / NOT_YET_A_RESEARCH_CONCLUSION**

## 1. 为什么需要这条支线

第十四轮确认本仓 v1.3 是全 SoC 系统级趋势报告。第十五轮又核对出，独立的 [Agentic CPU-uArch SSOT](https://github.com/xjs-work-lab/agentic-CPU-uArch) 已完成 Agentic 手机负载、LLVM/MLIR、现有 AArch64/SME2、微内核、CPU↔NPU/GPU 和软硬件差异化决策，但其现行结题目标不是对所有通用 CPU 核微架构细节做穷尽式趋势预测。

因此，本支线不是重做 Agentic CPU-uArch，也不是再做一轮全 SoC 历史，而是补足**通用移动 CPU 微架构机制与 LLVM 可达性之间的技术映射**，重点覆盖已有专项未以独立证据链系统回答的前端/分支、乱序执行、寄存器与存储层次等问题。

## 2. 决策目标

基于截至检索时可获得的公开证据，判断 2027–2029 年手机 AArch64 CPU 在 Agentic/多模态负载下：
1. 哪些 CPU 微架构演进信号值得跟踪，哪些仅是公开资料不足以验证的猜测；
2. 寄存器/状态设计、向量/矩阵 ISA、LLVM 代码生成与 ABI 之间有哪些可验证的关键关系；
3. 多 Agent 与 NPU/GPU 交替执行时，哪些问题主要属于 CPU 核、编译器、Runtime/OS、缓存/DRAM或数据布局；
4. 哪些方向可以通过公开原始资料、开源代码、编译器文档和已发表测量作出有边界的建议；
5. 哪些性能、能耗和隐藏芯片实现结论必须保持未知。

**面向对象：** 内部 CPU/编译优化技术路线讨论。  
**时间范围：** 2027–2029。  
**目标平台：** 手机优先，AArch64；其他平台只用于明确可迁移的机制对照。  
**优化目标：** 性能与能耗并重，考虑响应延迟、持续吞吐、代码尺寸、正确性、资源争用和前台 QoE。  
**编译器范围：** LLVM/MLIR，不开展 GCC 专线。

## 3. 研究约束

- **PUBLIC_ONLY**：只用公开论文、专利、官方 ISA/编译器/OS 文档、开源实现和公开独立测量。
- 不做真机测试、benchmark、仿真、PoC、性能测量或外部合作；不联系高校；不使用未授权内部数据。
- 不推断未公开的具体核宽度、ROB/LSQ容量、物理寄存器数量、预测器结构、NoC拓扑或功耗域数据。
- 不把指令/ABI/编译器“支持”写成目标手机已采用或端到端性能已获益。
- 不把某个论文在特定手机/模型上的结果外推为全行业规律。
- 复用 [Agentic CPU-uArch 现行技术组合](https://github.com/xjs-work-lab/agentic-CPU-uArch/blob/main/09-roadmap/current.md)与 [Round15F CPU/LLVM机制审计](https://github.com/xjs-work-lab/agentic-CPU-uArch/blob/main/analysis/engineering/round15f-cpu-llvm-compiler-pressure-2026-10-08.md)，不复制已有 Source/Claim/Decision，也不重开其宽泛研究。

## 4. 既有成果与真正缺口

| 主题 | 既有研究覆盖 | 本支线的剩余问题 |
|---|---|---|
| CPU↔NPU阶段/算子放置、强 NPU 基线 | Agentic CPU-uArch 的 CLM-CPU-001/004/005、CG-06 | 仅在需要解释通用 CPU 核机制时引用，不重复建卡 |
| AArch64/SME2、LLVM/MLIR、微内核与数据布局 | Agentic CPU-uArch 的 Round15F、CLM-CPU-002、现行 CG-06 | 深化寄存器压力、spill、调度、状态/ABI与实际指令选择之间的机制关系 |
| CPU 核前端、分支预测、乱序执行、ROB/LSQ、执行端口 | 不是 Agentic CPU-uArch 的核心结题输出；本仓 v1.3 亦未系统覆盖 | 建立公开资料的可见趋势与不可知边界；不反推具体厂商隐藏配置 |
| 架构寄存器、物理寄存器重命名、向量/矩阵状态 | 已有专项覆盖 SME/ZA ABI 和 LLVM 路径，但未形成通用移动 CPU 寄存器设计趋势图 | 区分 ISA 可见状态、实现内部物理资源、编译器分配压力和 OS/ABI 保存恢复 |
| Cache/TLB/预取/DRAM 与内存布局 | 既有专项覆盖 Agent/KV/model state、共享缓冲、packing、R2 CPU continuation locality | 区分模型/KV状态、跨引擎数据移动与 CPU-local 微状态；不先验认定缓存是首要瓶颈 |
| 多 Agent 与 NPU 协作 | 既有专项已有 Agent-aware DAG/Runtime/OS 强基线 | 仅补与 CPU 核、寄存器/状态、内存层次和 LLVM 代码生成有直接关系的机制接口 |

## 5. 五个研究问题

### Q1 — 移动 CPU 核的公开演进信号
前端取指/译码、分支预测、乱序窗口与调度、load/store 资源、向量/矩阵执行和能耗控制有哪些可靠的移动端证据？哪些属于厂商明确披露，哪些只是通用学术机制，哪些对手机产品不可见？

### Q2 — 寄存器与状态设计
如何区分 AArch64 架构可见寄存器、通用/向量寄存器、SME/ZA 状态、编译器虚拟寄存器分配与物理寄存器重命名？LLVM 的 live range、寄存器压力、spill、调用约定与状态转换如何影响性能/代码尺寸/能耗？不能由公开 ABI 推断哪些物理实现参数？

### Q3 — LLVM/MLIR 的可达优化杠杆
对真实移动负载，哪些已有 lowering、vectorization、tiling、fusion、packing、instruction scheduling、register allocation、SME2/ABI 路径值得优先核验？强基线和可能的开销转移是什么？

### Q4 — 多 Agent 与 NPU/GPU 的 CPU 侧机制
阶段切换、动态形状、精度变化、CPU fallback、队列/同步、数据复制、共享 DRAM 争用和前台 QoE 如何改变 CPU 的工作角色？哪些是 Runtime/OS 问题，哪些可能涉及 CPU 核或内存子系统？

### Q5 — 内存布局与局部性
如何对比 CPU-local cache/TLB/预取、张量 packing、共享缓冲、KV/model state 生命周期、DRAM 带宽和跨引擎数据移动？什么证据才足以将“候选瓶颈”升级为“值得优先投入的瓶颈”？

## 6. 领域地图：首轮检索锚点

本地图是**检索入口而非证据排名**。任何论文/厂商声明仍需按目标相关性、实验设计、基线、独立性与可复现性逐项判断。

| 子领域 | 优先检索入口 | 为什么相关 | 重点记录 |
|---|---|---|---|
| CPU 微架构与存储层次 | ISCA、MICRO、HPCA、ASPLOS、IEEE Micro、ACM TACO | 前端、分支、乱序执行、load/store、缓存/预取与能耗机制；需进一步筛出移动相关证据 | 目标 ISA/设备、工作负载、对照、是否真实手机、公开实现细节 |
| 编译器与代码生成 | CGO、PLDI、ASPLOS、LLVM Developers’ Meeting、LLVM/MLIR 官方文档与源码 | AArch64 指令选择、向量化、寄存器分配、调度、ABI、SME lowering | LLVM 版本、目标 CPU/feature、编译参数、IR/汇编、正确性和代码尺寸 |
| 移动系统与异构执行 | MobiSys、MLSys、EuroSys、ASPLOS，以及 Android/Qualcomm/Arm 官方文档 | CPU↔NPU/GPU 阶段切换、运行时、共享内存、调度和 QoE | 芯片/设备、模型/任务、图切分、fallback、拷贝/同步、端到端指标 |
| ISA 与寄存器状态 | Arm Architecture Reference Manual、Arm SME/SME2 官方资料、AAPCS64/SME ABI、LLVM AArch64 文档 | 区分架构可见状态、调用约定与内部物理实现 | 文档版本、状态保存规则、函数属性、调用/上下文切换约束 |
| 厂商/产品证据 | Arm、Apple、Qualcomm、MediaTek、Samsung、HiSilicon 官方技术材料 | 建立公开的产品/平台信号；不能把营销声明当作独立验证 | 明确披露与未披露字段，发布时间与量产状态 |
| 专利与先前技术 | Google Patents/WIPO/USPTO/EPO 的相关专利族与直接权利要求 | 辅助理解设计控制点与 prior art，不替代论文或产品事实 | 申请人、发明人、优先权、独立权利要求、实施例、目标应用边界 |
| 公开测量与工件 | 论文附录/代码、MLPerf相关移动结果、可公开复核的独立手机评测、LLVM测试与benchmark工具 | 识别已发表的真实设备数据和可复现代码生成证据 | 版本、设备、基线、计量层级、重复次数、误差和可迁移性 |

### 关键词与术语簇

- **Core:** mobile CPU microarchitecture, frontend bandwidth, fetch/decode, branch predictor, out-of-order execution, issue/dispatch width, ROB, load-store queue/LSQ, memory-level parallelism, execution ports, DVFS/energy.
- **Registers:** architectural state, physical register file, register renaming, rename map, vector register file, SME ZA/tile state, AAPCS64, live range, register pressure, spill/reload, context save/restore.
- **LLVM:** AArch64 backend, instruction selection, GlobalISel/SelectionDAG, vectorization, loop transformations, register allocation, instruction scheduling, SME/SME2 lowering, ABI attributes, code size.
- **Memory:** cache hierarchy, SLC, TLB, prefetching, DRAM bandwidth, cache contention, tensor packing/layout, KV-cache, shared buffers, CPU-NPU data movement.
- **Agentic/xPU:** multi-agent scheduling, partial DAG, stage/operator/shape/precision, CPU fallback, graph partition, dispatch/synchronization, QoS/QoE, foreground interference.

## 7. 首轮证据筛选与决策语法

重要陈述采用 [FACT] / [CLAIM] / [OBSERVATION] / [INFERENCE] / [HYPOTHESIS] / [UNKNOWN] 标签。对每项候选机制分别记录：
- **机制证据：** 来源是否直接说明该机制存在？
- **移动相关性：** 是手机实测、移动 SoC、可迁移的通用机制，还是服务器结果？
- **软件可达性：** LLVM/OS/Runtime 是否已有强基线？
- **性能/能耗证据：** 是端到端测量、微基准、模拟、分析模型还是厂商声明？
- **替代解释：** 制程、频率、软件版本、数据移动、NPU后端成熟度、散热和工作负载差异。
- **决策状态：** KEEP / FOLLOW / RESERVE / NOT EVALUABLE；不得仅凭论文数量或新颖性升级为硬件立项。

## 8. 下一最小步骤

先从每个子领域选取少量高质量 seed：优先官方 ISA/LLVM 原始文档、最近且目标相关的顶会论文、公开手机实测与关键专利权利要求；随后做来源独立性和移动适用性审计。**本文件仅锁定范围与领域地图，不表示已完成这些新来源的检索或验证。**

