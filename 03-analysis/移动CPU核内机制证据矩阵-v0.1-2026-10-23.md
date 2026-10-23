# 移动 CPU 核内微架构机制证据矩阵 v0.1

**更新：2026-10-23｜研究模式：PUBLIC_ONLY｜证据状态：STRUCTURAL_SIGNAL**  
**主线：** 从历史事实解释核内结构为何变化、收益与代价如何出现、瓶颈怎样迁移。此文不是 CPU 性能排行榜，也不是新技术立项清单。  
**来源总卡：** [第二十一轮核内机制原始来源卡](../02-evidence/sources/round-21-核内微架构机制原始来源卡.md)。

## 1. 结论摘要

本轮把分散的公开资料归一到“前端/分支—乱序执行—执行资源—访存/缓存—功耗与证据边界”的机制矩阵。当前证据支持五个历史观察：

1. **从部分乱序到更深的并行窗口，不是单纯追求更宽。** Cortex-A9 已有部分乱序执行和寄存器重命名；Cortex-A76/A77 将前端带宽、乱序窗口与执行/访存资源一起扩展；Apple Cyclone/Firestorm 逆向资料显示另一条强调宽执行和大在途窗口的路线。
2. **前端供给成为可独立优化的瓶颈。** A76 将分支预测与取指解耦；A77 加倍分支预测带宽、扩大 BTB 并加入 Macro-op Cache；Samsung M5 用 384-µop UOC 为可重复热点代码提供旁路供给，主要动机之一是减少 fetch/decode 功耗。
3. **乱序窗口只有和后端、访存并行度配合才有意义。** A77 同时扩展 dispatch、乱序窗口、整数执行带宽、load/store issue 与在途访存窗口；Exynos M3+ 通过预取、L1.5 DTLB、更多在途 miss 与多级缓存处理内存延迟。
4. **能效优化也可能来自“少做无效工作”，而非无限增加资源。** A78 的设计叙述强调分支预测/结构的面积功耗效率与指令融合；Exynos M5 的 UOC 让可预测代码在命中时跳过常规 I-cache/译码活动；预取器则需要控制误预取、带宽和缓存污染。
5. **公开披露深度差异很大。** Arm 的工程博客/TRM、Samsung SARC 团队参与的 ISCA 论文能支撑机制级描述；Apple 关键参数主要依赖第三方黑盒逆向；Qualcomm Krait/Oryon 和 HiSilicon Taishan 的公开资料不足以填满同等深度的字段。未知必须保留。

## 2. 跨核心机制矩阵

| 核心/代际 | 前端与分支预测 | 乱序执行、重命名与执行资源 | Load/Store、缓存与预取 | 公开设计动因/历史意义 | 证据强度与边界 |
|---|---|---|---|---|---|
| **Arm Cortex-A9（早期移动 OoO）** | 官方 TRM 描述指令预取、动态分支预测与返回地址栈；双发射 | 双发射、部分乱序、多发射推测执行与寄存器重命名 | 具有 L1 cache/MMU/TLB；可选 preload engine；具体缓存与 SoC 实现可配置 | 在移动功耗约束下，用有限的乱序/预测机制挖掘 ILP，早于后来更宽、更深的旗舰核 | **高（官方 TRM）**；不应把“部分乱序”与后续大窗口全 OoO 视为同一能力级别 |
| **Arm Cortex-A72** | 3-wide decode；分支预测器、I-cache tag lookup、TLB/micro-BTB 有改进 | Arm 工程博客称 8-wide issue、dispatch 最多 5 条 µops/cycle；寄存器文件功耗优化、commit queue、FP 延迟优化；但 Arm 软件优化指南的 dispatch 约束章节称顺序段到乱序段最多处理 3 µops/cycle，术语/阶段口径未解决 | load/store buffer、L1/L2 prefetch、L2 TLB 均有改进 | 在移动热/功耗约束下，不只提高峰值发射，还通过预测、缓存、寄存器文件与访存结构共同提升效率 | **中高（官方资料）**；dispatch 的“5 vs 3”需保留为来源口径冲突，不将其作为可比定量结论 |
| **Arm Cortex-A76** | 分支预测与取指解耦；前端每周期取指 4–8 条；首次 4-wide decode 的 Arm Cortex 核 | 最多 8 个操作/周期 dispatch 到 OoO 核；macro-op 在 dispatch 时可拆成两个 µops；8 条执行流水线；整数与双 128-bit SIMD/FP 吞吐增强 | 第四代预取器、完整缓存层级协同与更深 memory-level parallelism | 减少前端供给停顿，并扩大执行与访存并行能力；目标是在手机预算内提高持续计算能力 | **高（官方工程博客/TRM/优化指南）**；decode、dispatch、execution pipelines 是不同指标，不能等同于每周期完成 8 条架构指令 |
| **Arm Cortex-A77** | 分支预测带宽翻倍；L1 BTB ×4、L2 BTB +33%；新增 Macro-op Cache | dispatch 带宽 +50%；工程博客称最多 6 instructions/cycle，软件优化指南进一步区分最多处理 6 MOPs/cycle、派发最多 10 µOPs/cycle；乱序窗口扩大 25% 至 160 instructions；整数执行带宽 +50% | 在途 loads/stores 窗口 +25%；load-store issue 带宽 ×2；预取器按系统配置与集群利用率调整 | 前端、乱序窗口、整数执行和访存并行度同步扩展，降低单一阶段扩宽后出现的瓶颈转移 | **高（官方工程博客/软件优化指南）**；160 是 Arm 对 OOO window 的描述，不改称 ROB entries；收益数字是厂商比较 |
| **Arm Cortex-A78** | 提高分支预测带宽/准确率；加入更多指令融合场景；TRM 描述 L0 Macro-op cache | 同 ISA 下优化宽度/深度；官方强调对低收益结构进行面积/功耗优化 | 通过结构效率而非简单扩大所有资源提高性能/面积和性能/功耗 | 设计重点由单纯扩展资源转向在相近面积、功耗与热预算下提高可持续性能 | **高（官方博客/TRM）**；+7% 单线程、同热预算集群 +20% 等是 Arm 指定口径，不是跨设备独立测量 |
| **Apple Cyclone（A7，2013）** | 第三方逆向估计其执行宽度明显高于 Swift；分支误预测代价估计约 14–19 cycles | AnandTech 估计约 6 µops/cycle issue、192-µop ROB、4 个整数 ALU、2 个 load/store 与 2 个 branch units | 估计 64KB L1 I/D、1MB L2、4MB L3 | 早期移动自研核中就出现明显加宽执行与扩大乱序窗口的设计，目标是提升单线程 ILP | **中（第三方逆向）**；这些不是 Apple 官方规格，ROB/issue 数字保留估计属性 |
| **Apple Firestorm（A14/M1 代高性能核）** | 第三方逆向测得约 8 µops/cycle 管线宽度，并公开了大量指令延迟/吞吐测试 | 逆向研究报告约 330 项 coalesced retire queue、约 623 项 rename-retire queue；另报告较大的物理寄存器/在途资源 | 逆向研究报告约 130 个在途 loads、约 60 个在途 stores，并指出特定 load-load 链可有 3-cycle 转发延迟 | 展示了现代 Apple 核对高并行度和访存并行度的投入；也说明内部队列可能不是传统 ROB 的简单形态 | **中（黑盒逆向）**；不将 623 rename-retire queue 直接等同于传统 ROB，不能和 Cyclone 192 ROB 做同口径排名 |
| **Samsung Exynos M1→M6（ISCA 工业论文）** | M1 每周期约 4 条指令/µops；M3 为 6；M5 加 384-µop UOC、最多 6 µops/cycle。多级 BTB 与 perceptron 预测逐代演进 | 使用物理寄存器文件重命名；M3+ 支持零周期整数寄存器间 move 的 rename remapping；M4+ 特定 load-load cascading 可达到 3-cycle 有效延迟 | M3 增加 L1.5 DTLB、L3 与 spatial prefetch；L1 D-cache 从 32KB（M1）到 64KB（M3）再到 128KB（M6）；在途 miss 从 8 增至 40；L2/L3 按代际重配；论文模型中的平均 load latency 14.9 cycles（M1）降至 8.3（M6） | 从“更宽前端”扩展到热点代码省电、动态预取、降低访存延迟与协调多级缓存；不是所有瓶颈都靠加宽解决 | **高（工程披露）/中（结果适用范围）**；论文使用 4,026 条 trace 的 cycle-accurate 模型，统一 2.6GHz；M5/M6 当时无可用硅片，M6 不应称量产实测 |
| **Qualcomm Krait / Oryon；HiSilicon Taishan** | 公开产品资料能确认路线/产品节点，但本轮尚无同等深度、可审计的公开前端/预测器数据 | 未形成可靠、可同口径比较的 decode/dispatch/issue/ROB/寄存器文件矩阵 | 未形成公开可比的 LSQ、在途 miss、预取器与各级缓存机制数据 | 这体现的是公开资料透明度差异，不代表这些厂商没有相关结构或研发能力 | **不足/UNKNOWN**；禁止用跑分反推隐藏结构，后续仅在找到直接证据时补齐 |

## 3. 机制演进：观察、解释与边界

### 3.1 前端从“预测下一条指令”演进到“持续供给后端”

- **[FACT]** A9 TRM 已有动态分支预测与指令预取；A76 把分支预测和取指解耦并扩大取指带宽；A77 增加 BTB 容量和预测带宽并引入 Macro-op Cache；Samsung M5 用 UOC 为重复热点代码提供独立 µop 供给路径。
- **[INFERENCE]** 这说明前端瓶颈至少有三类：目标/方向预测不准、取指路径带宽/延迟不足、重复译码耗能。BTB、预测器、MOP/UOC 分别处理不同问题，不是可互换的单一“加大前端”机制。
- **代价/边界：** 更大预测结构和 µop cache 占面积；预测错误会造成无效取指/训练；UOC/MOP cache 只有对可复用代码段有效，需处理容量、分配与失效。不能从其存在直接推出所有应用都获得同样收益。

### 3.2 “宽度”必须按流水线阶段拆开

- **[FACT]** A76 官方资料分别给出 4-wide decode、4–8 条/cycle fetch、最多 8 operations/cycle dispatch 和 8 条 execution pipelines。A77 的公开指标则是最多 6 instructions/cycle dispatch 与 160-instruction OOO window。Firestorm 的“8 µops/cycle”来自第三方黑盒逆向。
- **[INFERENCE]** decode width、macro-op/µop 数量、dispatch bandwidth、issue bandwidth、执行端口数、retire bandwidth、ROB/OOO window 容量不是同一指标。宽度也不等于实际 IPC：依赖链、分支、端口冲突、缓存 miss、后端压力都会限制实际吞吐。
- **证据修正：** Cortex-A72 两份 Arm 来源对 dispatch 口径存在未解决冲突；因此当前矩阵不把 A72 的“5”用于跨核排名。

### 3.3 乱序窗口要和访存并行度一起看

- **[FACT]** A77 同时扩大 OOO window、dispatch、整数执行带宽与 load/store 并行能力；Samsung M3+ 增加在途 miss、预取器与缓存层次协同。
- **[INFERENCE]** 更大的窗口让核心能在较早指令等待数据时寻找更多独立工作，但只有当代码中存在可利用的独立指令、执行端口有容量、内存系统能承载更多并发请求时，窗口扩大才可能变成性能收益。
- **代价/边界：** 更大的队列/寄存器文件/miss tracking 需要面积和动态/漏电功耗；若工作负载缺乏 ILP 或访存模式难预测，扩展结构未必有效。

### 3.4 预取从静态规则走向置信度/反馈控制

- **[FACT]** Samsung 论文披露 multi-stride 与 spatial memory stream 预取、动态 degree、确认机制、one-pass/two-pass、L2/L3 协同和预取元数据；A77 也公开称预取行为可按内存配置和集群利用率动态调整。
- **[INFERENCE]** 预取的目标不是最大化请求数量，而是在目标数据到达及时性、准确率、带宽、miss-buffer 压力和 cache pollution 之间动态取舍。
- **证据边界：** Samsung M1–M6 的 14.9→8.3 cycles 平均 load latency 是统一频率的周期精确模型结果，且包含多项机制的累积效果；不能归因于单一预取器，也不能称为硅片实测。

### 3.5 寄存器与访存延迟优化可以改变“依赖链”的成本

- **[FACT]** Samsung 论文披露 M3+ 的物理寄存器文件重命名与零周期整数 move remapping；M4+ 的 load-load cascading 可让特定 load 链达到 3-cycle 有效延迟；Firestorm 的第三方逆向也报告特定 load-load 链有 3-cycle 转发延迟。
- **[INFERENCE]** 对链式数据结构、指针追踪和依赖地址生成，这类延迟可能比理论峰值带宽更重要；但不能将一个特定 load-load 场景外推到所有 load-to-use 依赖。
- **代价/边界：** 更复杂的重命名、转发和队列逻辑增加验证复杂度；必须精确说明依赖类型、操作数和延迟口径。

### 3.6 能效优化不是无限加宽所有结构

- **[FACT]** A78 的设计说明强调通过指令融合、预测结构功耗优化及减少部分低收益结构的面积/功耗成本来提高效率；Samsung M5 的 UOC 在可复用代码路径上绕开 I-cache/译码活动。
- **[INFERENCE]** 结构设计需要针对负载分布优化：高峰值带宽只在热点路径可持续供给、并且后端有工作可做时才有价值；对重复代码，省掉取指/译码可能比继续加宽更划算。
- **边界：** 这些是可解释的设计机制，不代表已测得每一项在所有手机应用中的净能耗收益。

## 4. 目前可确认与仍未知的字段

| 字段 | 当前状态 | 下一步处理 |
|---|---|---|
| Cortex-A9 双发射、部分乱序、寄存器重命名、动态预测 | **可由官方 TRM 确认** | 可进入历史叙述；收益数字保留厂商口径 |
| Cortex-A72 decode/dispatch/issue 术语 | **部分确认、存在来源口径冲突** | 先核对阶段定义，不做定量排名 |
| A76/A77 前端、执行和访存带宽变化 | **可由 Arm 官方工程博客/TRM 直接确认** | 可作结构变化事实；厂商收益数字仍是声明 |
| A78 的预测/融合/结构功耗优化 | **可由官方资料确认** | 解释设计意图；不外推成所有应用的实际节能比例 |
| Cyclone 内部宽度、ROB、端口与缓存 | **第三方逆向估计** | 保留估计/年份/方法边界 |
| Firestorm 队列和在途 load/store 规模 | **第三方黑盒逆向估计** | 明确 rename-retire queue ≠ 传统 ROB；不可直接跨架构比较 |
| Samsung M1–M6 机制演进 | **工程论文有较详细披露** | 量化结果保留 2.6GHz 仿真、trace 与 M5/M6 无硅片对比边界 |
| Krait/Oryon/Taishan 的完整核内参数 | **公开证据不完整** | 不从跑分倒推；只有找到直接公开来源再补矩阵 |

## 5. 本轮阶段性结论

**[OBSERVATION]** 已公开的微架构演进显示，前端预测/供给、乱序窗口、执行资源、访存并行度与能效控制是相互牵制的系统，而不是彼此独立的“越大越好”参数。

**[INFERENCE]** 历史变化往往表现为瓶颈转移：扩大解码/dispatch 后，执行端口或数据供给可能成为新瓶颈；扩大乱序窗口后，缓存 miss、带宽和错误预取成本更突出；增加预取后，带宽、缓存污染和 miss-buffer 容量变成控制对象。

**[UNKNOWN]** 公开资料不足以为所有现代手机 CPU 建立完整、统一口径的 ROB/LSQ/物理寄存器/预测器/端口数据表；尤其 Qualcomm Oryon 与 HiSilicon Taishan 的一些关键内部参数仍未公开。缺失字段不应用估算值填满。

## 6. 下一步

1. 逐条审计 A72 “dispatch 5 vs 3”来源差异，确认阶段定义与版本口径；在确认前保留冲突。
2. 从 Arm TRM/优化指南和 Apple/Samsung 可复现实验中继续补充可核验的寄存器重命名、load-use 延迟、执行端口和分支误预测相关机制。
3. 把“微架构能力”与编译器/LLVM 实际能否利用分开记录，避免将理论带宽直接转成编译收益。
4. 完成关键代际的机制矩阵后，再更新历史因果叙事与 2027–2028 条件性判断。
