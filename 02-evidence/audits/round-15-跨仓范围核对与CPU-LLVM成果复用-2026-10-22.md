# 第十五轮：跨仓范围核对与 CPU/LLVM 既有成果复用（2026-10-22）

## 0. 本轮目标

第十四轮发现：当前 v1.3 全 SoC 报告不能单独回答详细 CPU 微架构与 LLVM 优化决策。本轮不立即新增论文/专利搜索，而是检查是否已有独立、权威的 CPU/LLVM 研究 SSOT，避免重复研究、混淆结题状态或把一个子项目的结论错误地提升到另一个项目。

## 1. 核对的两个权威范围

| 项目/SSOT | 研究范围 | 当前状态 | 不应承担的任务 |
|---|---|---|---|
| 本仓 `xjs-work-lab/cpu-microarchitecture-trends` | 2007–2026 手机整体 SoC/平台历史；2027–2028 条件性系统趋势；CPU/GPU/NPU、媒体、通信、内存、软件与电热协同 | v1.3定性有条件可用；专家评审待完成；PPT批量制作暂停 | 不应把系统级综合稿当作详细CPU核设计或LLVM优化方案 |
| [Agentic CPU-uArch 仓](https://github.com/xjs-work-lab/agentic-CPU-uArch) | 2027–2029 Agentic 手机负载对 AArch64 CPU、LLVM/MLIR、微内核、OS/Runtime、CPU↔NPU/GPU 与内存协同的影响 | 2026-10-09 已在公开证据边界内结题；仅在出现可能改变决策的新公开原始证据或关键错误时重开 | 不应重新启动宽泛文献循环，也不应把“公开证据不足”包装成待本研究自有实验解决的遗留任务 |

### 权威入口

- 全 SoC 当前报告：[v1.3](../../05-deliverables/08-智能手机SoC整体架构演进-技术洞察证据收敛版-v1.3.md)
- 全 SoC 本轮结论审计：[第十四轮](round-14-结论审计与技术决策闭环-2026-10-22.md)
- Agentic CPU-uArch [CONTINUE-HERE](https://github.com/xjs-work-lab/agentic-CPU-uArch/blob/main/CONTINUE-HERE.md)
- Agentic CPU-uArch [现行技术组合](https://github.com/xjs-work-lab/agentic-CPU-uArch/blob/main/09-roadmap/current.md)
- Agentic CPU-uArch [CPU/LLVM、微内核与异构 NPU 证据审计 Round15F](https://github.com/xjs-work-lab/agentic-CPU-uArch/blob/main/analysis/engineering/round15f-cpu-llvm-compiler-pressure-2026-10-08.md)
- Agentic CPU-uArch [2027–2029 管理层技术洞察报告](https://github.com/xjs-work-lab/agentic-CPU-uArch/blob/main/09-roadmap/management-final-public-evidence-2027-2029.md)

## 2. 已有 CPU/LLVM 研究具体覆盖到哪里

Agentic CPU-uArch 的现有材料已经完成面向 Agentic 手机负载的决策级技术分析，尤其是以下五个可控技术杠杆：

| 杠杆 | 已有分析重点 | 当前可支持的决策 | 证据边界 |
|---|---|---|---|
| C1 形状/精度感知 lowering | MLIR Linalg 的分块、融合、向量化到 Arm SME；LLVM AArch64 目标代码生成 | 优先投资现有 ISA 的编译器与内核路径，按形状/精度/布局选择快速路径 | 代码生成能力不等于目标手机端到端收益；工具链版本、算子覆盖和后端均影响结果 |
| C2 SME streaming/ZA ABI | PSTATE.SM/ZA 状态、函数/调用点转换与 live-state 兼容 | 把 ABI 正确性、状态切换和调用边界作为工程问题检查 | 已有 ABI 文档不提供目标手机上的状态切换周期或能耗实测 |
| C3 CPU 微内核与布局生命周期 | KleidiAI GEMM/GEMV、packing、布局复用和数据搬移成本 | 优先评估内核、packing 和张量生命周期的协同优化 | vivo X300 等公开披露不能自动外推到 Agent 任务或 CPU 对 NPU 的普遍优势 |
| C4 CPU–NPU 阶段/精度分区 | NPU 图形状分桶、CPU 精度残差、fallback、子图重叠、受限拷贝/dispatch | 对照强 NPU/runtime 基线后，优化可证明有价值的 CPU 子任务和跨引擎路径 | 已发表研究的芯片、模型和软件栈不同；不能合并成统一跨厂商排名 |
| C5 Agent workflow 与 QoE | 部分 DAG 调度、关键路径、DRAM 亲和、前台 QoE 与 OS 资源准入 | 以 Runtime/OS 调度和端到端体验作为重要控制点 | 不应把软件调度问题直接重新包装成新 CPU 指令或硬件原语 |

### 当前技术组合（按 Agentic CPU-uArch SSOT）

- **工程/平台优先：** CG-06（现有 AArch64/SME2、LLVM/微内核与 CPU/NPU 快速路径）、PT-A（可信 Agent 工具执行）、C（Runtime/OS 异构调度与 QoE）。
- **条件研究储备：** A（额外的 Agent 私有 RequiredProgress 信息）、B-residual（跨引擎派生状态的物理有效性残余问题）、R2（CPU 续执行局部性）；均不是已批准的新硬件项目。
- **新增差异化 Agent CPU-uArch/ISA Primary Bet：0 项。** 这是截至该仓结题时公开证据范围内的决策，不代表这些方向在任何未来证据条件下都永远没有价值。
- **强制基线：** 已有 LLVM/MLIR/AArch64/SME、Arm KleidiAI、优化 NPU 后端、Android NPU Manager、QNN 与已有异构调度机制；任何新主张都必须说明它相对这些基线的增量。

## 3. 对第十四轮 K10“范围缺口”的修订解释

第十四轮 K10 的判断仍然成立：**本仓 v1.3 本身不是详细 CPU 微架构设计路线图。** 跨仓核对后，需要把它的含义限定为“该报告自身的覆盖范围不足”，而不是推断“整个研究体系没有 CPU/LLVM 分析”。

现有 Agentic CPU-uArch SSOT 已覆盖 Agentic 工作负载、编译器/微内核、现有 ISA 能力、CPU/NPU 分工和软硬件差异化判断，足以支撑当前公开证据下的工程方向。但它也**不声称**完成对所有通用 CPU 核设计参数（如前端宽度、分支预测、ROB/LSQ、重命名资源、缓存一致性等）的全面行业路线预测，更不提供未公开芯片的配置反推。

因此要分开三种问题：

1. **全 SoC 行业趋势：** 以本仓 v1.3 为主。
2. **Agentic 手机的 CPU/LLVM/Runtime 技术投入：** 以 Agentic CPU-uArch 的现行技术组合与结题报告为主。
3. **具体 CPU 核设计参数或微架构因果收益：** 两份报告都不能凭公开证据一概裁定；只有出现具体、会改变决策的公开原始证据时，才针对该问题开展有界更新。

## 4. 竞争解释与不可越过的证据边界

- “CPU 在某个模型/阶段更快”可能由模型形状、量化、算子覆盖、后端成熟度、数据搬移、图切分与同步开销共同造成；不能直接归因为 CPU 核微架构。
- “SME/ZA 已有软件支持”证明的是工具链/ABI 能力，不证明手机上一定有该扩展、应用一定启用，或端到端一定更快。
- “某篇论文使用手机 SoC”不等于测量的是手机整机电池能耗；平台、设备、模型、质量、软件版本和计量边界必须分别核对。
- “公开证据未证明 Agent-only 硬件差异化”不等于“专用硬件已被证明永远无用”。
- Agentic CPU-uArch 明确采用 PUBLIC_ONLY、ZERO NEW EXPERIMENTS 的研究合同。本轮不更改该合同，也不要求自行真机测试、仿真、benchmark 或 PoC。

## 5. 本轮裁决

**KEEP：**
- 全 SoC 与 Agentic CPU/LLVM 两条主线分开治理、互相引用。
- CG-06 作为现有 ISA/编译器/内核/Runtime 的工程优先方向。
- 对 NPU 和异构 Runtime 采用强基线，不预设 CPU 优于 NPU。
- 对芯片级收益、未公开微架构配置和物理因果保持未知。

**NARROW：**
- 将第十四轮“CPU 微架构/LLVM 范围缺口”限定为“全 SoC v1.3 文档内部的范围缺口”；全局研究体系已存在一个独立 Agentic CPU-uArch SSOT。

**DO NOT REOPEN：**
- 不重新开展已经结题的 Agentic CPU-uArch 宽泛检索。
- 不因为两份报告主题有交集而复制论文卡片、决策事件或路线图。
- 不为填满“微架构研究”名目而创建新的 Agent-only CPU 硬件 Primary Bet。

## 6. 下一步

1. 在本仓入口文件增加跨仓导航，说明哪份 SSOT 对哪类问题负责。
2. 对本仓 EX-06/EX-11 等涉及 CPU 与验证边界的问题，引用 Agentic CPU-uArch 的现有结论，但仍由全 SoC 专家评审独立裁决本仓报告。
3. 仅当出现新的公开原始证据或具体决策争议时，才按受影响的 Claim 局部更新；否则不启动新一轮宽泛研究。
4. 本仓 PPT 继续等待用户视觉方向与 Issue #1 的真实专家意见，不把跨仓核对当作专家签字。

**状态：** CROSS_REPO_SCOPE_AUDIT_COMPLETE / EXISTING_CPU_LLVM_SSOT_REUSED / NO_BROAD_RESEARCH_REOPEN / EXPERT_REVIEW_PENDING_FOR_SOC_REPORT

## 7. 研究事务记录

本轮事务记录：[round-15-2026-10-22.md](../../00-project/research-transactions/round-15-2026-10-22.md)。
