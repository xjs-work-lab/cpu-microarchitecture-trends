# CPU 微架构历史演进与 LLVM 机制深化：范围锁定与领域地图（2026-10-23）

**状态：SCOPE_LOCKED_FOR_PUBLIC_EVIDENCE_DISCOVERY / NOT_YET_A_RESEARCH_CONCLUSION**

## 1. 为什么需要这条支线

本仓主问题始终是**复盘移动终端 SoC 的历史演进、解释变化原因与后果，并从中理解未来可能的延续趋势**，而不是寻找新的硬件立项方向。全 SoC v1.3 已覆盖多个系统阶段和跨引擎机制；CPU 是用户特别关注、需要更细致历史纵深的一部分。

第十五轮跨仓核对确认，独立的 [Agentic CPU-uArch SSOT](https://github.com/xjs-work-lab/agentic-CPU-uArch) 已研究 Agentic 手机负载、LLVM/MLIR、AArch64/SME2、微内核与 CPU↔NPU/GPU 协作。其成果作为相关背景复用，但不应把本支线改造成新的技术路线评选。

本支线补充**移动 CPU 微架构多年来的变化点、变化动因、直接后果、代价与相互影响**，尤其覆盖前端/分支、乱序执行、寄存器、缓存/内存、SIMD/向量能力、功耗管理及 CPU 与异构引擎的分工。LLVM 用于解释软件如何利用或受限于这些硬件变化，是因果链的一部分，不是独立立项目标。

## 2. 研究目标与时间范围

基于公开证据，系统回答：
1. 2007–2026 年移动 CPU 微架构有哪些可确认的阶段、转折和变化点？每项变化在产品/核心/ISA/软件的哪个层级发生？
2. 每项变化是由什么推动的：交互与应用负载、性能/能效要求、制程与面积约束、频率扩展困难、内存瓶颈、持续热限制、软件并行性、竞争产品，还是多个因素共同作用？
3. 变化带来了什么直接收益、代价或新瓶颈？哪些是来源明确说明的设计动因，哪些只是跨来源分析推论？
4. CPU 与 GPU、DSP/NPU、缓存/DRAM、OS/调度器和 LLVM 的关系如何随时间变化？系统中不同层次的职责如何重新分配？
5. 从这些历史因果链可以谨慎推断 2027–2028 年哪些趋势可能延续，哪些仍不可判断？

**主要历史窗口：** 2007–2026；必要时回溯更早的技术起源。  
**前瞻窗口：** 2027–2028，只做有条件的趋势延伸，不将其变成立项清单。  
**目标平台：** 智能手机优先、AArch64；桌面/服务器研究仅在解释机制来源时作为对照，明确标注迁移边界。  
**优化维度：** 性能、能效、面积、持续热表现、响应延迟、软件复杂度和系统协同之间的权衡。  
**编译器范围：** LLVM/MLIR，用于解释硬件能力如何被软件利用，不单独开展 GCC 研究。

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

### Q1 — 历史变化点
移动 CPU 的微架构、ISA、核心组织、缓存/内存和功耗管理在 2007–2026 年间发生了哪些有证据的变化？需要形成时间线，而不是只罗列当前机制。

### Q2 — 变化动因
每个变化是针对什么历史约束或负载压力出现的？优先区分厂商明确披露的设计动因、同期行业共性解释和研究者推论；不能把时间上的先后关系直接当成因果关系。

### Q3 — 收益、代价与新瓶颈
每次变化改善了什么，又增加了什么成本或把瓶颈转移到了哪里？例如性能与能效、峰值与持续表现、并行度与调度复杂度、专用加速与数据搬运之间的权衡。

### Q4 — CPU 与整个 SoC 的关系
CPU 的变化如何受到 GPU、DSP/NPU、内存系统、制程、封装、OS 调度、编译器和终端热设计影响？区分 CPU 核本身的变化与平台层变化。

### Q5 — 对未来的历史性参考
从已发生的变化中，哪些趋势具有连续性，哪些是特定负载或时期的阶段性方案？对 2027–2028 年只做有证据的条件性外推，并列出不确定性；不强制提出新硬件立项建议。

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

先构建 2007–2026 移动 CPU 微架构变化时间线，按“变化点—同期负载/约束—直接证据—设计动因—收益—代价/新瓶颈—后续影响—证据强度”逐项整理。优先补齐代表性手机 CPU 核、Arm 架构/核心 IP、厂商技术日/白皮书、论文与官方编译器资料；随后对关键转折做来源独立性与因果强度审计。**本文件仅锁定研究范围和方法，不表示时间线与因果关系已完成验证。**

