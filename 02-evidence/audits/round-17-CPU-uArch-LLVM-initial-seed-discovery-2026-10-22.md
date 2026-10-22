# 第十七轮：移动 CPU 微架构 / LLVM 初始 Seed Discovery（2026-10-22）

**状态：INITIAL_SEEDS_IDENTIFIED / FULL_COVERAGE_NOT_CLAIMED**

## 0. 本轮范围

根据第十六轮范围锁定，只做小规模、高质量原始来源种子筛选。目标是找到能支撑后续逐篇核验的锚点，不是形成最终技术结论或声称已覆盖整个 CPU 微架构领域。

本轮通过公开网页检索识别初始来源。Exa 深度检索服务返回 credit-quota 错误，因此本轮未完成 Exa 多工作流检索；以下结果只代表初始种子，不代表穷尽式覆盖。

## 1. 初始来源种子

| ID | 来源与层级 | 直接支持的内容 | 适用边界 | 后续动作 |
|---|---|---|---|---|
| UARCH-SEED-001 | [LLVM：Support for AArch64 SME in LLVM](https://www.llvm.org/docs/AArch64SME.html)，官方编译器文档 | 说明 LLVM 如何把 SME ACLE/ABI 状态属性映射到 IR 并降低调用边界；PSTATE.SM 切换会影响向量状态，编译器需在适当位置插入 SMSTART/SMSTOP，处理 live value 的 spill/reload；当前文档还说明特定 streaming 属性下暂时禁用 LoopVectorize/SLP，并对跨状态边界的 inline/tail-call 作限制 | 这是编译器/ABI正确性与代码生成机制，不是手机性能或能耗测量；文档内容随 LLVM 版本变化 | 核验当前 LLVM 版本与 AArch64 后端实现；从公开示例追踪状态切换、寄存器保存和优化限制 |
| UARCH-SEED-002 | [Arm ABI：AAPCS64](https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst)，官方 ABI 规范 | 定义 AArch64 参数传递、寄存器保存约定、SME 的 PSTATE.SM/PSTATE.ZA/ZA 状态和 lazy-save 协议；ZA 存储容量按 SVL.B × SVL.B 定义，支持 off/active/dormant 状态与按需保存 | ABI 描述的是架构可见状态与软件契约，不公开具体 CPU 的物理寄存器文件、重命名资源或实际保存成本；网页顶部显示的发行标签需在后续审计时再次核对 | 按当前正式发行版核对版本、调用约定、异常/线程边界和 ZA save/restore 条款 |
| UARCH-SEED-003 | Chen, Qu, Zhang, [Dissecting Conditional Branch Predictors of Apple Firestorm and Qualcomm Oryon](https://arxiv.org/abs/2411.13900)，2024 原始论文 | 通过公开论文中的微基准和 PMU 方法恢复 Apple M1 Firestorm 与 Qualcomm Snapdragon X Elite Oryon 的条件分支预测器模型；论文在 SPEC INT 2017/Geekbench 5 上报告特定软件/硬件调整最高 14% MPKI 降低与 7% 性能提升 | 设备是 M1 与 X1E-80-100 等客户端高性能平台，不是手机 SoC；数据不是移动端能耗证据，也不能把个别预测器结构外推到其他厂商/核心 | 深读方法、基线、应用集合和可迁移性；作为分支预测机制案例，而非手机产品结论 |
| UARCH-SEED-004 | Cai, Deshmukh, Patt, [Enabling Ahead Prediction with Practical Energy Constraints](https://doi.org/10.1145/3695053.3730998)，ISCA 2025 原始论文；[作者实验室论文 PDF](https://hps.ece.utexas.edu/pub/cai_ahead.pdf) | 研究通过前瞻预测隐藏分支预测器延迟的机制，并显式分析预测能耗/功率代价；公开摘要报告相较先前方案大幅降低每次预测能耗代价 | 通用 CPU 微架构研究，不是移动 CPU 实测；本轮只核对到公开摘要/会议元数据，具体测量口径和所有实验条件尚未深读 | 需要全文方法/评估核验后，才能录入定量结论；只作前端设计与能耗权衡的候选种子 |
| UARCH-SEED-005 | [Qualcomm Oryon CPU in Snapdragon X Elite: Micro-Architecture and Design](https://ieeexplore.ieee.org/abstract/document/11002606)，IEEE Micro，2025 | 论文摘要表明其讨论 Qualcomm 自研 Oryon 核微架构、缓存与内存子系统，是现代 Arm 兼容高性能 CPU 的公开架构描述入口 | 目标是 Snapdragon X Elite 客户端 PC SoC，不是手机 SoC；来源带有厂商技术叙事，且本轮只取得摘要，不把其能效表述当成独立对比结果 | 若要引用具体微架构事实，需取得并逐项审查正文；只可作为机制/公开披露对照 |
| UARCH-SEED-006 | [MLIR ArmSME EnableArmStreaming pass](https://mlir.llvm.org/doxygen/EnableArmStreaming_8cpp_source.html)，官方 LLVM 源码文档 | 公开实现显示该 pass 可为函数添加 arm_streaming / arm_locally_streaming 属性，并处理 ZA 相关属性；接口状态管理与 LLVM 后端生成的状态切换指令相连接 | 源码存在不等于目标手机工具链启用该 pass，也不证明端到端收益 | 与 UARCH-SEED-001 对照，建立从 MLIR pass 到 LLVM IR/ABI/汇编的证据链 |

## 2. 首轮可成立的观察

### O1 — 寄存器/状态与编译器边界是可公开核验的具体技术问题

LLVM SME 文档和 AAPCS64 提供了架构状态、调用约定、ZA lazy-save、SM 状态切换、spill/reload 和优化约束的直接证据。这使“状态生命周期和 ABI 边界是否造成额外代码/保存恢复”成为比猜测某厂商物理寄存器文件大小更可核验的研究问题。

但目前只确认机制存在；没有测量目标手机上状态切换的周期、能耗或端到端代价。

### O2 — 分支预测的细节可以通过公开研究被部分恢复，但移动适用性有限

Firestorm/Oryon 论文说明：在少数公开可测的 AArch64 高性能核心上，学术研究能够利用微基准与性能计数器构建分支预测器模型，并据此解释软件性能变化。它也反向说明，厂商未公开的物理实现参数不能从 ISA 或产品营销页直接推断。

然而，Apple M1 与 Snapdragon X Elite Oryon 不等于手机 CPU 的完整样本；本轮不据此推导移动 CPU 的分支预测器大小或未来规格。

### O3 — 当前最强证据集中在“软件可达性”，而非手机内部微架构参数

当前最直接的原始证据来自 LLVM/Arm ABI；关于前端/分支的公开研究可提供机制级参考，但缺少足够多、同口径的手机核心公开资料。ROB/LSQ 容量、重命名资源、物理寄存器文件端口/能耗等仍是明确的公开证据缺口。

## 3. 来源质量与证据成熟度

| 主题 | 当前成熟度 | 目前可以说什么 | 目前不能说什么 |
|---|---|---|---|
| SME/SME2 ABI、状态与 LLVM lowering | **STRUCTURAL_SIGNAL（强）** | 官方文档明确规定状态与调用约束，编译器存在相应 lowering 机制 | 不能据此宣称手机上存在某个具体性能/能耗收益 |
| 分支预测结构与软件影响 | **STRUCTURAL_SIGNAL（中；跨设备迁移有限）** | 特定高性能核心的公开论文可以恢复部分预测器结构并分析软件影响 | 不能外推到所有手机 CPU 或未来芯片配置 |
| 前端预测延迟与能耗权衡 | **STRUCTURAL_SIGNAL（待全文核验）** | ISCA 论文是候选机制来源 | 本轮尚未核实全部方法/评估细节，不引用为手机收益 |
| 通用移动 CPU 物理寄存器/ROB/LSQ/执行端口 | **NOT_EVALUABLE（当前）** | 已明确需要进一步找直接披露或可迁移研究 | 不根据 ARM ISA/ABI反推具体实现参数 |
| 移动端内存层次与局部性 | **PARTIAL** | Agentic CPU-uArch 已有 KV/model state、packing、CPU–NPU 数据移动及 R2 条件储备；全 SoC 报告把共享缓存降为候选机制 | 不宣称共享缓存/CPU-locality 是首要瓶颈 |

## 4. 当前应保留的竞争解释

- 观察到分支相关性能变化，可能来自分支预测器结构，也可能来自前端带宽、编译器布局、工作集、缓存、分支密度与测试平台差异。
- SME 路径的 spill/reload 或状态切换开销，可能由调用边界与寄存器活跃区间触发，不等于 SME 运算本身低效。
- 某项编译器优化收益可能来自更好的 packing、融合、指令选择或调度，而非物理 CPU 核发生变化。
- 在缺乏手机内部公开信息时，不能把桌面/服务器结果直接转成手机能耗或下一代手机核设计建议。

## 5. 下一步

1. 深读 UARCH-SEED-001/002：形成可复核的 SME/ZA 状态、寄存器保存恢复、LLVM spill/reload 和向量化限制机制卡。
2. 深读 UARCH-SEED-003/004/005：统一设备、负载、基线和测量层级，决定哪些内容仅能作为通用机制参考。
3. 专门补充 ROB/LSQ、寄存器重命名/物理寄存器文件、移动缓存/预取的高质量原始来源；如果只有通用核心或模拟研究，明确标为间接证据。
4. 暂不更新全 SoC v1.3 的结论或 114 条台账计数；等来源逐项审计后再决定是否纳入正式证据登记。

**本轮状态：** `INITIAL_SEEDS_IDENTIFIED / OFFICIAL_ABI_LLVM_SOURCES_HIGH_DIRECTNESS / MOBILE_CORE_MICROARCH_COVERAGE_STILL_SPARSE / FULL_COVERAGE_NOT_CLAIMED`
