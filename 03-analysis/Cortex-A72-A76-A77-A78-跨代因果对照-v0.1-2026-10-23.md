# Cortex-A72 → A76 → A77 → A78 跨代因果对照 v0.1

**日期：** 2026-10-23  
**用途：** 历史因果链的第一条连续主线；只解释公开资料支持的机制与设计目标，不把相邻代变化自动视为因果。  
**证据类型：** Arm 官方微架构文章/软件优化指南/产品支持页；无真机测量。

## 一、结论先行

这四代不能简单讲成“前端越来越宽，因此 CPU 越来越快”。公开资料支持的更精确叙事是：

1. **A72：在热功耗约束下改善每个阶段的效率。** 它保留某些阶段宽度，同时调整微操作处理、dispatch、寄存器文件活动、提交队列、分支预测与内存系统。
2. **A76：更明确地扩展前端供给与乱序后端吞吐。** 4-wide decode、解耦分支预测/取指、最高 8 uops/cycle dispatch，以及更强的内存级并行，共同支持更高单线程性能。
3. **A77：在 A76 的基础上继续提升可供给与可执行操作的带宽。** dispatch 提升到最多 6 instructions/cycle、乱序窗口增至 160 instructions，整数执行和 load/store 资源也扩展；Macro-op cache 帮助重复热点代码减少前端重复工作。
4. **A78：不是把所有结构继续做大，而是更强调固定移动热功耗范围内的持续性能与效率。** 官方资料给出相对前代的持续性能/能效声明，但必须保留其厂商比较口径。

**核心历史规律（中等置信度）：** 性能演进从多处效率修补，转向更系统地提高前端供给、乱序并行与访存并行，再转向在持续热功耗约束下优化性能/能效组合。它不是单一结构逐代放大的直线，也不能只凭这些资料证明每一代瓶颈转移的具体顺序。

## 二、逐代对照

| 代际 | 可直接确认的设计变化 | 公开资料明确的目标/动机 | 机制解释 | 收益证据与边界 | 因果等级 |
|---|---|---|---|---|---|
| A72 | 微操作保留更复杂形式直到 dispatch；有效 dispatch 提升至 5-wide；调整寄存器文件端口/组织、commit queue、register-status FIFO；改进分支预测、预取、TLB/MMU 等 | Arm 直接讨论 decode 功耗、吞吐、面积与功耗优化；手机 SoC 的热预算是重要约束背景 | 同一条路径上减少重复解码/不必要活动，同时改善分支与数据供给；不是简单扩大所有流水线宽度 | Arm 报告特定内存带宽、性能/功耗比较；属于 Arm 的条件化结果，不能拆出每项贡献 | **A**（动机较直接；独立归因仍有限） |
| A76 | 4-wide decode；前端取指 4–8 instructions/cycle；dispatch 最多 8 uops/cycle；更深的 MLP/预取与后端资源 | Arm 将目标描述为高单线程性能并保持移动能效；软件优化指南明确指出要满足 dispatch 各类 uop 约束才能有效利用带宽 | 增加前端与后端之间可供给的操作数量，并通过更大的在途内存并行度隐藏部分延迟；实际吞吐仍受各类执行管线约束 | Arm 文档提供结构规格；不同设备的持续表现还受 SoC、工艺、频率与散热影响 | **A/B** |
| A77 | dispatch 带宽相对 A76 增加 50%，最多 6 instructions/cycle；乱序窗口增至 160 instructions（官方给出相对增幅）；整数执行带宽增加 50%；在途 load/store 窗口增长与 load-store issue bandwidth 提升；改进 prefetch；MOP cache | Arm 明确把目标定位于高性能和能效，并披露各结构带宽变化 | 更大窗口帮助容纳更多独立操作；更强 load/store 资源暴露更多 MLP；MOP cache 在重复代码场景减少重新取指/解码需求。效果依赖依赖链、分支、缓存与内存行为 | 数值来自 Arm 设计者资料；没有独立设备对照证明每项增幅如何映射到应用性能 | **A/B** |
| A78 | 官方强调持续性能；分支预测、指令融合及低收益结构的面积/功耗优化；相对前代的持续性能/能效声明 | Arm 明确把持续表现放在固定移动热功耗预算背景下 | 目标不是无限扩大所有结构，而是通过更高效的前端/执行活动与面积功耗取舍，在热约束下维持更高有效吞吐 | Arm 产品页宣称最高 20% 持续性能提升；“与早期设备比较”的能效口径不等于严格 A77→A78 同配置实测 | **A**（目标明确；比较口径需严格限定） |

## 三、真正的跨代因果链

### A72 → A76：从效率优化走向更高供给能力

- **事实：** A72 的公开说明强调 dispatch、寄存器文件活动、commit/状态队列、分支预测和访存路径优化；A76 则公开了 4-wide decode、最高 8 uops/cycle dispatch 与更深的 MLP。
- **明确动机：** 两代资料均把性能与能效并置；A72 对解码功耗/活动优化描述较具体，A76 强调更高单线程性能和移动能效。
- **机制推论：** 当目标从“减少低效活动”进一步转向更高单线程吞吐时，必须同时改善前端供给、后端接收与内存并行，单纯增加一个宽度指标不够。
- **尚未证明：** 不能声称 A72 的某个具体瓶颈直接导致 A76 的每一项结构变化；没有公开证据量化 decode、dispatch、MLP 各自的应用贡献。

### A76 → A77：提高带宽与在途并行度

- **事实：** A77 官方说明列出 dispatch、乱序窗口、整数执行带宽、load/store issue 与在途内存窗口的增加，并提及 MOP cache 和预取器改进。
- **明确动机：** Arm 把改进放在性能与能效框架下，而不是只提高频率。
- **机制推论：** 多个阶段同步扩展，表明提高有效吞吐需要协调前端供给、执行资源和数据供给；更大的窗口只有在指令/内存独立性足够时才能兑现收益。
- **尚未证明：** 不把“窗口扩大”直接写成“解决了内存瓶颈”。更多在途请求也可能受到 cache miss、DRAM 带宽、依赖链和错误预取的限制；公开资料没有证明下一代变化必然由这些残余瓶颈引起。

### A77 → A78：从峰值带宽进一步强调持续热功耗效率

- **事实：** A78 官方材料强调固定移动热功耗范围内的持续性能，及分支预测/融合/结构效率方面的调整。
- **明确动机：** 持续性能和功耗是官方明确目标。
- **机制推论：** 当高峰值性能不能长期维持时，减少无效工作、优化预测和选择性投入面积可能比无条件扩大每个结构更划算。
- **尚未证明：** 不能将 A78 的持续性能改善完全归因于某一核内机制；芯片配置、制程、频率策略、散热设计与系统软件也影响终端表现。

## 四、瓶颈转移：哪些可以说，哪些不能说

| 判断 | 状态 | 推荐表达 |
|---|---|---|
| A72 对多个阶段做功耗/效率优化 | 官方资料支持 | “Arm 公开说明了这些优化及其功耗/效率目标。” |
| A76 将前端供给与后端 dispatch 能力提升到更高水平 | 官方结构资料支持 | “A76 提供更高的前端/dispatch 带宽，设计上有利于提高有效指令吞吐。” |
| A77 同时扩大乱序窗口和内存并行相关资源 | 官方结构资料支持 | “设计增加了暴露/容纳并行工作的能力；实际收益取决于负载。” |
| A77 后瓶颈必然转移到 DRAM 带宽 | **未证实** | “在内存受限负载下，DRAM 带宽可能成为限制因素之一；当前资料不足以将其定为代际设计动因。” |
| A78 的改善主要由减少低收益结构活动导致 | **部分推论** | “这些优化与持续性能/能效目标一致，但缺少可拆分的独立贡献数据。” |
| 每代结构增加意味着手机端实际性能同比增加 | **错误推断** | 不作此结论；需要同条件的应用/功耗/热测试。 |

## 五、与 LLVM 软件利用路径的连接

- A72/A76/A77/A78 的 target tuning 与 scheduler model 只是一种编译器抽象；LLVM 23.1.4 对部分 Cortex target 使用共享 scheduler model。不能据此断言每项新硬件机制都被精确建模。
- A76 的 dispatch 指南表明，代码生成需满足多类 uop 同周期资源约束；这直接说明“理论带宽”不等于任何指令序列都能达到该带宽。
- PGO 可提供热块/边频率；向量化与寄存器压力模型可影响代码形态；这些路径并不直接观测运行时分支预测器、ROB/LSQ 占用或真实 cache miss。
- 本项目未在手机上生成并分析汇编、运行 llvm-mca 或 benchmark，因此软件利用效果仍标为 **UNKNOWN**。

## 六、主要原始来源

1. Arm, [A walk-through of the microarchitectural improvements in Cortex-A72](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/a-walk-through-of-the-microarchitectural-improvements-in-cortex-a72) — A72 的微操作、dispatch、寄存器/队列、分支与内存路径细节。
2. Arm, [Cortex-A76: Laptop-class performance with mobile efficiency](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/cortex-a76-laptop-class-performance-with-mobile-efficiency) — A76 设计定位与结构变化。
3. Arm, [Cortex-A76 Software Optimization Guide](https://documentation-service.arm.com/static/64a2b013df6cd61d528c3fa0) — dispatch 的 MOP/uop 带宽与管线资源约束。
4. Arm, [New Arm Cortex-A77 provides compute performance leadership](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/new-arm-cortex-a77-provides-compute-performance-leadership) — dispatch、乱序窗口、整数执行、load/store 与预取变化。
5. Arm, [Cortex-A78 Product Support](https://support.arm.com/compute-ip/cortex-a78) — 产品级持续性能与能效声明；需保留其比较口径。
6. LLVM, [AArch64 target processor definitions at llvmorg-23.1.4](https://github.com/llvm/llvm-project/blob/llvmorg-23.1.4/llvm/lib/Target/AArch64/AArch64Processors.td) — 目标与模型映射。
7. LLVM, [AArch64 scheduler model for Neoverse N1](https://github.com/llvm/llvm-project/blob/llvmorg-23.1.4/llvm/lib/Target/AArch64/AArch64SchedNeoverseN1.td), [N2](https://github.com/llvm/llvm-project/blob/llvmorg-23.1.4/llvm/lib/Target/AArch64/AArch64SchedNeoverseN2.td) — 模型参数及注释边界。

## 七、审计结论与后续

- 这条主线可以作为历史解释的核心案例，但结论限定为“公开资料支持的机制演进”，不能写成全部瓶颈已被直接证明。
- 下一步优先复核每项官方性能/能效比较的测试条件与基准；随后将这条跨代主线回写到总时间线，并以同一格式扩展到 Apple 和 Samsung。
- 不制作 PPT，直到跨代因果链和来源口径审计完成。

## 八、性能/能效声明口径复核（2026-10-23）

本节基于重新打开的 Arm 原始文章正文与脚注补充，优先区分**公开声明值**和**可独立横向比较的实测值**。

| 核心 | 官方公开声明 | 来源实际说明的比较口径 | 可以得出的结论 | 不应得出的结论 |
|---|---|---|---|---|
| A72 | 对比 Cortex-A15：相同性能下 28nm 条件约减半功耗，14/16nm FinFET 条件约减 75%；在 2.5GHz 情景下功耗低 30–35%，峰值性能超过 2 倍 | Arm 说明历史图中截至 2015 年的点来自在售设备测量；A72 部分是实验室测量基础上的预测；性能提升同时来自微架构与频率，制程也影响结果 | Arm 明确把移动热预算和效率作为设计动机，并给出带条件的比较 | 不能把全部提升归因于 CPU 微架构；不能把 A72 预测值当成所有量产手机的统一实测 |
| A76 | 35% 性能提升、40% 能效改善；另称对比标准 Cortex-A75 system 在相同功耗预算下性能高 40% | Arm 原始文章把 35%/40% 放在代际宣传语境；同文明确提到 A76 的性能来自微架构、面积/功耗优化与更先进制程。同期 Arm 演讲资料说明 SPECint2006 估算；不同系统/频率/制程比较不能视为严格控制变量的单核硅片对照 | 可确认官方的目标、设计变化与声明的性能/效率幅度 | 不应把 35% 与 40% 相加；不应说 35% 全由 IPC 或微架构单因素造成 |
| A77 | 相对 A76：20% 更高单线程性能；另称整数性能 +20% 以上、FP +35% 以上、内存带宽 +15% 以上；结构层面 dispatch +50%、乱序窗口增至 160、整数执行带宽 +50% 等 | 官方文章给出相对前代的架构/工作负载声明，但本轮可见正文未找到可将所有数字统一到同一公开设备、频率、编译器、基准和功耗条件的完整方法说明 | 可将其作为 Arm 对 A77 设计目标和结构带宽变化的官方描述 | dispatch +50% 不等于应用性能 +50%；整数/FP/内存指标也不可相加，不能直接外推到手机 SoC 总体性能 |
| A78 | 相对 A77：同一移动热功耗包络下持续性能 +20%；同一 A77 性能点下，相对 2019 设备能耗节省 50%；单线程 SPECint2006 估算 +7%；单位性能功耗效率 +4%，单位面积性能效率 +5%；4+4 集群持续性能 +20%、面积 -15% | Arm 脚注明确：主要 CPU 比较基于 SPECint2006 的 SPECspeed Integer component；1W 单核性能比较包括架构与制程改进（与 2019 设备比较）；集群面积对比为 A78/A55 4+4 与 A77/A55 4+4，且同样包括架构与制程改进 | 这是四代中比较口径注释最明确的一组官方声明；能区分单核、功耗点和集群面积 | 不能把 20% 持续性能理解为所有应用普遍 +20%；不能把 50% 能耗节省完全归因于核内微架构；也不能把 7%、20%、50%、15% 合成一个指标 |

### 来源复核记录

1. **A72 官方原文**：[A walk through of the Microarchitectural improvements in Cortex-A72](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/a-walk-through-of-the-microarchitectural-improvements-in-cortex-a72)。正文明确说 2015 年以前的数据点来自在售设备测量，而 A72 结果基于实验室测量作预测；也明确写到提升来自微架构变化与频率增加的组合。该限定必须随数字一起引用。
2. **A76 官方原文**：[Cortex-A76: Laptop-Class Performance With Mobile Efficiency](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/cortex-a76-laptop-class-performance-with-mobile-efficiency)。正文给出 35% 性能、40% 能效等声明，并描述前端、dispatch、执行与 MLP 的结构变化；同期 Arm 发布演讲资料将性能曲线标为基于 SPECint2006 的 Arm 估算。比较中存在制程与系统实现差异。
3. **A77 官方原文**：[New Arm Cortex-A77 CPU continues path towards compute performance leadership](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/new-arm-cortex-a77-provides-compute-performance-leadership)。官方列出 20% 单线程、20%+ 整数、35%+ FP、15%+ 内存带宽声明和相应结构变化；当前审计不把这些不同指标视为同一基准或独立硅片归因。
4. **A78 官方原文与脚注**：[Arm Cortex-A78 CPU: Sustained Performance for Greater Digital Immersion](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/arm-cortex-a78-cpu)。脚注注明 SPECint2006、单核 1W 对照、2019 设备比较，以及 A78/A55 与 A77/A55 4+4 集群面积口径；声明包含架构与制程改进。

### 本轮审计后的证据等级修正

- **A72：** 设计动机 A；总体性能数字为厂商测量/预测混合证据，不应标成独立因果实验。
- **A76：** 结构/目标 A；性能幅度为 Arm 声明/估算，制程和平台条件为混杂变量。
- **A77：** 结构增幅与官方性能声明 A；各项结构对实际应用性能的独立贡献 C/D。
- **A78：** 声明的基准和比较条件有明确脚注，证据可追溯性较好；仍是 Arm 估算并包含架构与制程因素，不是独立的全机型实测。
