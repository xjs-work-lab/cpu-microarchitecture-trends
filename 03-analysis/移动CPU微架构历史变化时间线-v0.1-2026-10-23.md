# 移动 CPU 微架构历史变化时间线与因果分析 v0.1

**更新时间：2026-10-23｜研究窗口：2007–2026｜资料模式：PUBLIC_ONLY**  
**本文件性质：第一版证据约束下的历史综合，不是完整产品清单，也不是新技术立项建议。**

核内微架构的重点原始来源另整理为[第十九轮来源卡](../02-evidence/sources/round-19-移动CPU核内微架构原始来源.md)，来源与因果边界审计见[第十九轮初始来源审计](../02-evidence/audits/round-19-cpu-history-timeline-source-audit-2026-10-23.md)。

## 1. 研究问题与读法

本研究要解释：移动 CPU 多年来发生了哪些重要变化、这些变化为何出现、带来哪些收益和代价、它们如何影响后续架构演进。未来趋势只作为历史分析的延伸，不反过来替历史寻找“必然性”。

每个节点必须区分：
- **变化事实**：核心/ISA/集群/产品公开披露了什么；
- **设计动因**：厂商或设计者明确说了什么；
- **分析推论**：我们根据负载、功耗和产品路线作出的解释；
- **证据边界**：厂商性能/能效数字通常是特定配置与测试条件下的声明，不等于独立实测，也不能把制程、微架构、频率、缓存、软件和终端散热的贡献拆开。

因果强度标记：
- **A — 设计动因有直接来源**：设计者明确说明了目标/约束；这不自动证明所宣称收益的独立因果。
- **B — 多来源相互支持**：架构事实和同期负载/行业约束有多处证据，因果解释较可信。
- **C — 合理推论**：与证据相符，但没有直接设计说明或缺少独立测量。
- **U — 未知**：公开资料不能判定，保留未知。

## 2. 2007–2026 关键变化时间线（第一版）

| 时期 | 可确认的变化点 | 为什么发生／当时的压力 | 直接后果、代价与后续影响 | 因果证据强度 |
|---|---|---|---|---|
| **2007–2011：从单核高性能转向乱序与多核扩展** | Cortex-A8 代表 Armv7-A、NEON、多媒体 SIMD 与双发射应用处理器阶段；2007 年公布的 Cortex-A9 引入部分乱序流水线，并提供最多四核的 MPCore 配置和硬件一致性管理。Arm 回顾资料称 A9 相对 A8 在相同功耗下有约 25% IPC 提升。 | 手机从基本通信扩展到网页、应用、多媒体与更丰富交互，单靠提高频率受到功耗约束。Arm 的回顾材料明确描述了性能需求上升以及设计者从提高 MHz 转向增加核心数的阶段性选择。 | 乱序执行可在依赖允许时挖掘指令级并行；多核提高可并行负载吞吐，但不会自动加速单线程，且增加面积、缓存一致性、调度和并行软件的复杂度。A9 的百分比是 Arm 回顾性陈述，不能视为统一独立基准。 | **B**：架构事实强；动因有回顾资料支持，定量收益不是独立归因。 |
| **2011–2013（并行路线）：Qualcomm Krait 体现厂商定制 CPU 微架构** | Qualcomm 于 2011-02-13 公布 Krait，面向下一代 Snapdragon，提供单核、双核和四核产品配置，并与 GPU、DSP、连接模块共同构成移动平台；Krait 路线随后进入 2012 年 Snapdragon S4 手机，HTC One S 于 2012-04-25 在美国上市。 | Qualcomm 将其与更复杂的智能手机/平板负载联系起来，包括更大屏幕、更复杂 OS、多任务、HD 游戏和高清视频；这反映了性能、功耗与平台集成的竞争压力。 | Krait 说明移动 CPU 演进并非只有 Arm Cortex IP 一条路线，芯片厂商也会用自有微架构争取性能/能效差异化。Qualcomm 公告中“性能提升 150%、功耗降低 65%”是其自报比较，不应当作独立可比结果。 | **A（厂商目标）/C（收益幅度）**：定制路线和配置明确，量化收益需独立验证。 |
| **2011–2016：big.LITTLE 把“峰值性能”和“日常能耗”分开优化** | Cortex-A15/A7 等高性能核与高能效核组合，通过异构集群和软件调度，让不同任务在不同能效区间执行。2012 年后 A57/A53 延续这一思路。Apple 的 A10 Fusion（2016）后来也公开采用 2 个性能核加 2 个高能效核，说明异构 CPU 并非单一厂商路线。 | 手机负载是间歇的：网页/游戏可能短时高强度，消息、音频和后台任务则更轻；电池容量和可散热功率有限。Arm 对 big.LITTLE 的说明直接把这种负载差异与电池寿命目标联系起来。 | 同一 SoC 可以兼顾突发性能与低负载能效；代价是异构调度、任务迁移、缓存/一致性和功耗管理更复杂。Arm 宣称特定常见负载下平均应用处理器功耗可降低“最高 70%”，应保留为厂商条件性声明，不能泛化到所有应用/手机。 | **A/B**：设计动因明确；实际收益高度依赖负载、调度器和实现。 |
| **2012–2015：64 位从架构路线进入手机产品** | Armv8-A 和 Cortex-A53/A57 引入 AArch64，并兼顾当时的 32 位软件生态；Apple 的自研 CPU 核路线可追溯至 2012 年 A6/Swift，随后 A7/Cyclone 于 2013 年进入 iPhone 5s，Apple 同时强调 iOS 7 与系统应用针对 64 位设计。 | 更大的地址空间、系统软件能力、长期应用性能与架构演进是推动因素。Arm 明确提及更大物理地址空间及虚拟化等能力；Apple 则把 64 位作为整机软件和应用生态升级的一部分。不能将转向 64 位简化为“因为手机内存超过 4GB”。 | 64 位不仅是地址宽度变化，也改变寄存器/调用约定、编译器、ABI、系统库和应用发布链路。潜在收益依具体代码而异；更宽指针也可能增加部分数据结构的内存占用。Apple A7 的微架构拆解显示其强调较宽的乱序执行资源，但具体宽度/ROB 数字属于第三方逆向估计，不是 Apple 官方披露。 | **A/B**：产品与 ISA 变化明确；不同收益需按软件和负载分别验证。 |
| **2015–2017：持续性能、能效和面积效率成为核心设计目标** | Cortex-A72 面向高端手机并针对 16nm FinFET+ 等工艺；Cortex-A73 强调更小面积、能效和持续性能。Qualcomm 于 2015 年公布 Snapdragon 820 的首代 Kryo 自研 64 位核，但 2017 年 Snapdragon 835 的 Kryo 280 转为基于 Arm “Built on Cortex” 许可的半定制路线。Arm 公开把复杂相机/视频、游戏、较大显示和常驻传感等体验与严格的手机功耗/热预算联系起来。 | 用户需求不再只是短时跑分：高分辨率影像、游戏、多应用和常驻功能带来更复杂的混合负载；无风扇机身需要控制表面温度和长期功耗。 | 设计目标从单纯提高峰值，转向在给定功耗/面积下保持更高的持续性能。Arm 对 A72/A73 的能效与性能百分比是其目标配置下的厂商声明；由于同时涉及微架构、制程和 SoC/手机实现，不能把代际差异全部归因于 CPU 微架构。 | **A/B**：热/能效目标有直接资料；单项技术的独立贡献仍不明。 |
| **2016–2018：异构核设计从“两个集群”走向更灵活的集群组织** | Arm 于 2017 年公布 DynamIQ，将 big 与 LITTLE 核组合在同一集群设计框架中，并通过 DynamIQ Shared Unit 提供集群级共享资源；它扩展了核心组合和集群配置选择。 | 核心类型、并发任务和计算密度持续增加，SoC 需要更灵活地组合不同性能/能效的核。Arm 将 DynamIQ 与持续增长的计算需求、AI 等新负载联系起来。 | 更灵活的异构配置为调度、共享缓存和集群扩展提供了新的实现空间；实际收益仍依赖 SoC 采用的核组合、缓存/互连配置与 OS 调度。DynamIQ 是可配置的 IP/集群技术，不代表所有手机都采用相同物理拓扑。 | **A/B**：设计意图直接公开；各产品实际收益与拓扑须逐款核对。 |
| **2015–2019：Samsung 的 Mongoose 自研核持续迭代后退出** | Exynos M1–M5 是 Samsung 自研 CPU 核路线；Exynos 990（2019）采用两颗第五代自研核，并与 Cortex-A76/A55 组成三簇 CPU。Samsung 于 2019 年宣布停止自研 CPU 核开发项目。 | 自研核需要同时达到性能、能效、面积、验证与产品节奏目标；对某些厂商而言，采用标准/半定制 IP 可能成为后续的资源配置选择。 | ISCA 2020 工业论文公开讨论了 M1–M5 的分支预测、微操作缓存、预取和内存延迟优化，证明这条路线存在较深入的核内迭代；但论文注明 M5/M6 的部分分析来自周期精确模型，不是硅片实测。项目停止的完整内部权衡未公开，不能单凭外部跑分认定单一原因。 | **A（项目终止事实）/B（机制历史）/C（退出原因）**：自研核与终止事实明确，组织决策因果不完整。 |
| **2018–2020：高性能核继续提高 IPC，同时向更广泛的客户端负载扩展** | Cortex-A76 采用新微架构；Arm 宣称其相较前代有 35% 性能提升和 40% 能效提升，并强调 7nm 工艺和“笔记本级”性能。2020 年 Arm 同时推出面向持续性能/效率的 Cortex-A78 和偏重峰值性能的 Cortex-X1/Cortex-X 定制项目。 | 手机承担更重的生产力、多任务、游戏与计算负载；与此同时，制程缩放不再足以单独支撑性能增长，移动平台也不能无限提高频率和功耗。 | 核心路线开始更明确地分层：一类优化持续性能和能效，另一类把更多设计预算投向峰值单线程性能。A76 的跨代数字同时受微架构、工艺和目标配置影响；X 系列则体现了性能目标分层，不代表所有 SoC 都会选择最大核或相同核数。 | **A/B**：产品策略和设计目标明确；跨代百分比的独立因果不可拆分。 |
| **2020–2022：Armv9、向量/安全扩展与 64 位软件迁移相互交织** | Armv9 将 SVE2 等扩展带入客户端路线，并强化安全方向；Arm 在 2020 年宣布，从 2022 年的 IP 开始，未来 Cortex-A “big” 核只支持 64 位执行。 | 软件工作负载对向量化、媒体/信号处理、机器学习和安全能力的需求增长；同时，长期维护 AArch32/AArch64 两套执行环境会增加架构与生态复杂度。 | 新 ISA 扩展提供软件可用的新能力，但只有 OS、编译器、库和应用实际使用后才可能转化为收益。big 核不再支持 AArch32 是 IP 路线的变化，不等于同一时间所有 Android 手机、所有小核或所有应用都完成 32 位淘汰。 | **A/B**：路线公告明确；生态迁移与应用收益有不同时间表。 |
| **2023–2024：HiSilicon Kirin 出现 Taishan 自研高性能核的第三方证据** | Kirin 980 官方资料明确采用 Cortex-A76/A55；而 Kirin 9000S/9010 的裸片照片、CPU ID 与第三方系统分析将部分高性能核识别为 Taishan 系列，并报告其与 Cortex-A510 能效核混合。 | 制裁/供应链环境、产品路线与既有 Arm ISA 生态构成背景，但本轮不能证明这些因素中哪一项直接导致 Taishan 微架构决策。 | 应按代际和证据类型表述：Kirin 980 是官方确认的 Cortex 核配置；Taishan 是第三方分析支持的自研核线索，Huawei 未公开足以重建其前端、ROB/LSQ、分支预测、执行端口与缓存结构的完整文档。 | **B（第三方识别）/U（核内细节与因果）**：存在多源线索，但不是官方完整微架构披露。 |
| **2022–2024：细分核心等级与“全大核”成为并存路线** | Arm 持续区分 Cortex-X 性能核、A7x 平衡/效率核与 A5x 高能效核；另一方面，MediaTek Dimensity 9300 于 2023 年采用 4× Cortex-X4 + 4× Cortex-A720 的 All-Big-Core 配置，Dimensity 9400 延续全大核设计。 | 高端游戏、影像、端侧生成式 AI 和多线程负载提高了对持续并行吞吐的要求；新核心的性能/能效改善也使厂商可以重新评估“小核”的数量与角色。 | 这不是“全行业都不再需要小核”的证据。All-Big-Core 是厂商选择的一条路线，A720 仍与 X4 有不同定位；Apple A19（2025）仍采用 2 性能核 + 4 能效核。不同路线的后台能耗、峰值/持续性能和面积代价需通过同口径设备测量比较。 | **B/C**：产品配置是事实；其背后的因果解释及普适性仍有限。 |
| **2023–2024：定制 CPU 微架构重新成为高端手机平台的显著差异点** | Qualcomm 于 2024 年把定制 Oryon CPU 引入 Snapdragon 8 Elite 手机平台；Apple 则长期维持自研 CPU 核路线。 | 高端平台竞争从单纯采用通用 CPU IP，进一步涉及单线程性能、能效、平台差异化以及 CPU 与 GPU/NPU 的协同。Qualcomm 将 Oryon 与端侧多模态生成式 AI 时代联系起来。 | 定制微架构可以让厂商针对目标产品做不同的性能、缓存和功耗取舍；但公开资料没有披露全部微架构细节，也不能仅凭厂商峰值数字判定其相对其他厂商的普遍优势。Oryon 不是 Qualcomm 历史上第一次设计定制 CPU，而是其新一代定制架构进入旗舰手机的重要节点。 | **B/C**：产品事实明确；动因有厂商表述，跨厂商优势须独立验证。 |
| **2025：CPU 侧向量/矩阵计算能力与系统级 AI 计算更紧密结合** | Arm Lumex/C1 平台把 SME2 纳入 CPU 集群级设计；Arm 将其与低延迟端侧 AI、实时翻译、语音和个性化应用联系起来。 | 端侧 AI 不只有 NPU 上的大规模推理，也包含控制逻辑、短任务、前后处理和需要低延迟响应的部分工作；CPU 可能需要执行一部分小型模型或矩阵工作，并与 GPU/NPU 协作。 | CPU 的职责开始在部分实现中从传统通用执行进一步延伸到向量/矩阵计算与异构工作流协同。Arm Lumex/C1 于 2025-09-10 公布；MediaTek Dimensity 9500 于 2025-09-22 公布并明确使用 C1-Ultra/C1-Premium/C1-Pro 与 SME2；vivo X300 系列于 2025-10-13 发布、10-17 开售，提供了从 IP 到 SoC 再到终端的可追踪产品化链。实际终端收益仍依赖软件栈和负载，不能据此得出 NPU 会被 CPU 取代。 | **A/B**：平台能力和设计目标有直接资料；具体终端收益取决于实现与软件。 |
| **2026：面向持续 AI 工作流的 CPU 集群与 SoC 协同被明确提出** | Arm 于 2026 年 9 月公布 CSS for Mobile 2/C2 CPU cluster：C2-Ultra 面向高单线程与低延迟，C2-Pro 面向持续能效，并配有两个 SME2 单元。MediaTek 于 2026 年 9 月公布 Dimensity 9600 Pro，采用 2× C2-Ultra + 6× C2-Pro；Arm 后续公开资料将 vivo X500 Pro 与 OPPO Find X10 系列列为搭载该平台的终端。 | 厂商明确提出，持续运行的 agentic AI 不只是调用一次模型，还要保持上下文、运行应用、协调服务、规划并把工作分配给 CPU/GPU/AI 加速器，同时受手机功耗与散热限制。 | 这是截至资料截点的最新公开设计信号：C2 于 2026-09-08 公布，Dimensity 9600 Pro 于 2026-09-15 公布，Arm 后续报道其进入 vivo X500 Pro 与 OPPO Find X10 系列。CPU 被描述为系统级工作流协调者，并在某些任务中直接执行低延迟 AI；高性能核与效率核仍然分层存在。性能、功耗数字和设备采用信息仍主要来自厂商公开资料，量产设备的长期体验、软件实际使用率和跨厂商普适性仍需独立验证。 | **A（设计动因）/C（普适趋势）**：官方动因明确，但不能把厂商路线等同于全行业必然方向。 |

## 2.1 公开资料能够直接验证的核内微架构变化

逐核机制的第一版归一矩阵见[移动 CPU 核内机制证据矩阵 v0.1](移动CPU核内机制证据矩阵-v0.1-2026-10-23.md)，其[第二十一轮机制审计](../02-evidence/audits/round-21-mobile-cpu-core-mechanism-evidence-audit-2026-10-23.md)专门记录了 A72 dispatch 口径冲突、Apple Firestorm 队列术语差异和 Samsung 跨代数据的仿真边界。以下案例用于说明历史时间线，不替代逐项机制审计。 已完成的软件利用路径梳理见[移动 CPU 微架构—LLVM 代码生成桥接矩阵 v0.1](移动CPU微架构与LLVM代码生成桥接矩阵-v0.1-2026-10-23.md)，对应[第二十二轮桥接审计](../02-evidence/audits/round-22-llvm-hardware-codegen-bridge-audit-2026-10-23.md)明确哪些机制可由 LLVM 直接利用、哪些仅通过模型或 profile 间接利用，以及哪些仍需真实手机证据。

这组案例是时间线里最有价值的深化部分：不仅看产品名、核心数或最高频率，也看前端、分支预测、执行宽度、寄存器/队列和内存子系统怎样变化。以下仅记录有公开原始资料支撑的部分。

### A. Cortex-A9：引入部分乱序执行和多核一致性管理

Arm 对 A9 的回顾称其采用部分 out-of-order 流水线，MPCore 配置可扩展到四核，并集成硬件缓存一致性管理；相较 A8 的 IPC 改善是 Arm 自己报告的结果。历史意义在于同时沿两条轴线扩展：单核更能挖掘指令级并行，多核可以提高可并行任务的总吞吐。代价是更复杂的执行/一致性逻辑和更高的软件并行要求。来源：[Arm Cortex-A9 回顾](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/the-birth-evolution-of-cortex-a9-and-what-s-coming-next)。

### B. Apple A7/Cyclone：高单线程能力不只靠增加核心数

第三方 AnandTech 对 Cyclone 的逆向分析估计其峰值 issue width 为 6，并估计重排序缓冲区（ROB）从前代 Swift 的约 45 个 micro-ops 增至约 192 个；它还报告更大的 L1 指令/数据缓存以及更多执行资源。这些数字不是 Apple 官方规格，必须保留“第三方逆向估计”的身份。它们说明当时至少有一条移动 CPU 路线，把大量设计资源投入宽执行、乱序窗口和单线程吞吐，而不是只增加核心数。来源：[AnandTech Cyclone 拆解](https://www.anandtech.com/show/7910/apples-cyclone-microarchitecture-detailed)。

### C. Cortex-A72：在不单纯增加频率/发射宽度的情况下，重做多处效率瓶颈

Arm 在 2015 年的核内微架构文章提供了少见的具体细节：
- A72 保留与 A57 相近的 3-wide decode、8-wide issue，但把 dispatch 扩展到每周期最多 5 个指令/micro-ops；
- 更新分支预测器，并通过减少无用预测器访问、优化 I-cache tag lookup 等方式兼顾预测准确性与功耗；
- 优化 decode/rename、寄存器文件访问和 commit 队列，以减少不必要的活动与面积/功耗；
- 引入更先进的 L1/L2 数据预取，调整 load/store buffer，并改善 MMU table walker 和 L2 TLB 延迟；
- Arm 报告 CPU 内存带宽提升超过 50%，并强调同等性能下显著降低功耗。

**为什么重要：** Arm 明确指出，手机受限于 SoC 热预算，单纯拉高频率或提高 issue rate 并非充分解法；要在热/功耗边界内提高性能，必须改善效率。这里可直接观察到的设计策略是同时修补分支、前端、寄存器、浮点延迟、预取和 TLB 等多处瓶颈，而不是押注一个孤立参数。性能/能效数字仍属于 Arm 的实验/宣传口径，不等于第三方手机实测。来源：[Arm Cortex-A72 微架构改进详解](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/a-walk-through-of-the-microarchitectural-improvements-in-cortex-a72)。

### D. Cortex-A76：前端加宽、分离分支预测与取指，并提高内存级并行能力

Arm 的 A76 微架构说明称，该核首次采用 4-wide decode；前端可以每周期取 4–8 条指令，分支预测与取指解耦，最多每周期向乱序后端 dispatch 8 个操作；整数执行和 128-bit SIMD/浮点吞吐也有扩展，并采用更先进的预取器和更深的 memory-level parallelism。

**为什么重要：** 这是从 A72/A57 时代的 3-wide decode 向更宽前端迈进的明确例子。设计意图不是只把频率拉高，而是通过减少前端供给瓶颈、增加每周期可利用的指令并行性，以及更好地隐藏内存延迟来提高性能；同时仍要受移动设备的功耗与面积约束。来源：[Arm Cortex-A76 微架构说明](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/cortex-a76-laptop-class-performance-with-mobile-efficiency)。

### E. Cortex-A77/A78：用宏操作缓存、分支预测带宽和后端效率，继续改善前端供给与持续性能

Arm 对 A77 的公开说明指出，前端加入 Macro-op（MOP）Cache，用于缓存已解码的宏操作；分支预测带宽提升，BTB 容量增加，乱序执行窗口与 dispatch 带宽也有扩展。该机制的作用是让重复执行的代码在缓存命中时减少重新取指/解码成本，并更稳定地向后端供给操作。来源：[Arm Cortex-A77 微架构说明](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/new-arm-cortex-a77-provides-compute-performance-leadership)。

Arm 对 A78 的说明进一步把设计重点放在固定移动热功耗预算下的持续性能：其公开报告称，相对 A77，A78 在相同移动热功耗范围内可提高约 20% 持续性能；微架构侧则通过分支预测带宽/准确率、指令融合和对低收益结构的面积/功耗优化来取得改善。这个案例说明前端优化并非只为峰值 IPC，也能减少误预测和无效活动，从而支持更长时间的高性能运行。相关百分比是 Arm 的特定比较口径。来源：[Arm Cortex-A78 微架构说明](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/arm-cortex-a78-cpu)。

### F. 哪些细节仍不能从公开资料补齐？

以上案例表明，部分 CPU IP 的前端、调度、预取与缓存设计确实有公开细节；但这不代表每一代、每个厂商都公开同样深度。对当前手机 SoC，以下字段仍应逐型号核验，不得从跑分反推：ROB/LSQ 的精确容量、物理寄存器数量、完整分支预测器算法/表结构、未公开的执行端口限制、真实缓存命中率、每个结构的动态功耗。若只有第三方估计，必须单独标明方法与不确定性。

## 2.2 跨厂商路线与产品化时间校正

第十九轮时间线已覆盖主要架构转折；第二十轮进一步区分 CPU 核微架构所有权、SoC 级差异化与终端落地日期。详细比较见[跨厂商路线与产品化时间 v0.2](移动CPU跨厂商微架构路线与产品化时间-v0.2-2026-10-23.md)，逐项原始来源见[第二十轮来源卡](../02-evidence/sources/round-20-移动CPU跨厂商路线与产品化来源卡.md)与[路线/时间审计](../02-evidence/audits/round-20-cross-vendor-cpu-route-and-productization-audit-2026-10-23.md)。

| 厂商/路线 | 已核验的关键变化 | 当前可以得出的结论 |
|---|---|---|
| **Apple** | A6/Swift（2012）到 A7/Cyclone（2013），之后持续演进自研 A 系列 CPU 核；Cyclone 的宽执行/ROB 数值来自第三方逆向 | 长期自研核是其明确路线；具体微架构数字需区分官方披露与逆向测量 |
| **Qualcomm** | Krait（2011）→首代 Kryo（2015/2016）→半定制 Kryo 280（2017）→手机平台 Oryon（2024） | 品牌名不等于固定微架构；全自研、半定制与 SoC 级异构协同会随代际变化 |
| **Samsung** | Mongoose/M1–M5 自研核；Exynos 990/M5 是最后一代，项目于 2019 年终止 | 自研核是可以投入也可以退出的路线；不能由单一跑分推断完整的项目决策原因 |
| **HiSilicon** | Kirin 980 官方采用 Cortex-A76/A55；Kirin 9000S/9010 的 Taishan 高性能核由第三方分析识别 | 必须按代际与证据来源区分；Taishan 的完整核内结构仍未知 |
| **MediaTek + Arm IP** | Dimensity 9300 采用 X4/A720；Dimensity 9500 使用 Arm C1 系列/SME2；Dimensity 9600 Pro 使用 C2 系列 | SoC 厂商可在核心组合、频率、缓存/内存、调度和异构协同上差异化；不应把 Arm 核内设计归为 SoC 厂商自研 |

关键时间链包括：**Cortex-A76（2018-05-31）→ Kirin 980（2018 年公布）→ Mate 20（2018-10-16）**；**Arm C1/Lumex（2025-09-10）→ Dimensity 9500（2025-09-22）→ vivo X300（2025-10-13 发布、10-17 开售）**；以及 **Arm C2/CSS（2026-09-08）→ Dimensity 9600 Pro（2026-09-15）→ Arm 后续报道的 vivo/OPPO 终端系列**。日期链能证明产品化顺序，不直接证明性能因果。

## 3. 从时间线可得到的阶段性历史解释

### 3.1 不是简单的“核心越来越多、频率越来越高”

早期的重要变化包括乱序执行和多核化；随后，移动 CPU 更明显地把不同性能/能效区间分给不同核心，并通过调度来适应负载变化。后续代际又把核心微架构、工艺、缓存与集群组织共同纳入性能设计。核心数量或最高频率都不足以单独解释跨代体验。

### 3.2 异构设计没有沿单一路线演进

big.LITTLE、DynamIQ、Apple 性能核/能效核、Arm X/A7x/A5x 多等级，以及 MediaTek 的 All-Big-Core 都体现了对同一约束的不同回答：如何在峰值响应、并行吞吐、后台能耗和持续热表现之间取舍。全大核是重要分支，但不是异构核路线的终结。

### 3.3 能效与持续表现逐步成为和峰值性能同等重要的设计问题

高分辨率影像、游戏、多应用与持续运行任务会让短时峰值和长时间表现分离。架构、制程、频率、电压、散热结构与系统调度共同决定结果；只看厂商给出的 IPC、峰值频率或短跑分，无法还原整机持续体验。

### 3.4 ISA 扩展的历史收益依赖软件生态

NEON、AArch64、SVE2、MTE、SME2 等能力的引入，不意味着每款手机、每个 OS 版本和每个应用都会立即使用。硬件能力要经过编译器、ABI、运行时、库与应用迁移，才能转化为用户可见收益。这也是为什么架构变化的原因与后果需要跨层追踪。

### 3.5 CPU 的角色扩展，但通用计算与专用加速并未简单互相替代

CPU 仍承担 OS、应用控制流、调度与大量通用代码；GPU/NPU 继续处理适合其并行/矩阵模型的任务。近期 SME2/C1/C2 的公开方向说明 CPU 也可能直接执行某些低延迟矩阵任务并协调其他引擎，但不能据此推断所有 AI 都会迁到 CPU 或 NPU 会失去作用。

## 4. 当前可提出的 2027–2028 历史延伸判断（非立项建议）

以下只是由既有变化推得的观察重点，可信度不同：

1. **高可信度：** 峰值性能、能效和持续热表现仍会共同塑造移动 CPU；只提升频率的解释力有限。
2. **高可信度：** 高性能核与能效核的配置会继续因产品定位而分化，不会仅凭一款 All-Big-Core 产品就形成单一路线。
3. **中等可信度：** CPU 与 GPU/NPU 的软件协同和数据移动管理会更重要，尤其是 AI 工作流包含大量控制逻辑、前后处理和阶段切换时。
4. **中等可信度：** CPU ISA 中的向量/矩阵和安全扩展会继续影响编译器与运行时；实际收益取决于量产硬件、软件支持和负载。
5. **尚不能判断：** 具体手机 CPU 的 ROB/LSQ 容量、分支预测器结构、物理寄存器数量、内部缓存命中率及各模块瓦数。除非厂商或可靠测量公开披露，不从性能分数反推隐藏微架构。

## 5. 当前缺口与下一步

第十九轮建立了初版历史时间线；第二十轮已完成首轮跨厂商路线分类、关键 IP/SoC/终端日期核验，并把主要发现回写到本时间线。**本文件仍不是完整历史审计**，特别是核内机制覆盖、Taishan 公开细节和统一条件下的因果测量仍不完整。

1. **建立逐核机制证据矩阵：** 按厂商/核心/代际追踪取指/译码、分支预测、乱序窗口、寄存器重命名、执行端口、Load/Store、缓存和预取。每个条目明确标记 FACT、厂商主张、第三方分析、推论或未知。
2. **补齐竞争路线与隐藏结构边界：** Apple、Qualcomm、Samsung、HiSilicon Taishan、Arm Cortex/C1/C2 采用不同公开资料深度；优先使用原始工程资料、架构论文与高质量逆向分析，不从跑分推断 ROB/LSQ、物理寄存器数或预测器内部结构。
3. **把“原因”与“同时发生”分开：** 对每个机制变化记录设计者明确说出的目标、同期负载/功耗/面积约束、可能收益、代价和替代解释；厂商性能/能耗数字保留原始比较口径。
4. **将机制与软件采用连接：** 追踪 ISA/SME2 等能力经过编译器、ABI、运行时和应用后如何真正被使用；区分硬件可用、软件可用与终端默认启用。
5. **最后再做 2027–2028 条件性延伸：** 不提前把单一厂商路线当成行业必然趋势，也不把公开证据缺口当成技术不存在。

## 6. 主要公开来源

### Arm：早期核心、big.LITTLE 与 64 位
- [Cortex-A8 产品支持与架构概述](https://support.arm.com/compute-ip/cortex-a8)
- [Arm：Cortex-A9 的诞生与演进（2013 回顾）](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/the-birth-evolution-of-cortex-a9-and-what-s-coming-next)
- [Arm：Cortex-A 移动产品路线回顾（2013）](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/a-walk-through-the-cortex-a-mobile-roadmap)
- [Arm big.LITTLE 技术说明](https://www.arm.com/technologies/big-little)
- [Arm Cortex-A50：Cortex-A53/A57 与 Armv8-A（2012）](https://www.arm.com/company/news/2012/10/arm-launches-cortex-a50-series-the-worlds-most-energy-efficient-64-bit-processors)

### Apple：64 位、异构核与近年性能/能效声明
- [Apple：iPhone 5s/A7 64 位公告（2013）](https://www.apple.com.cn/newsroom/2013/09/10Apple-Announces-iPhone-5s-The-Most-Forward-Thinking-Smartphone-in-the-World/)
- [AnandTech：Apple Cyclone 微架构拆解（2014，第三方逆向估计）](https://www.anandtech.com/show/7910/apples-cyclone-microarchitecture-detailed)
- [Apple：A10 Fusion 的性能核/能效核配置（2016）](https://www.apple.com/newsroom/2016/09/apple-introduces-iphone-7-iphone-7-plus/)
- [Apple：A17 Pro CPU 微架构改进声明（2023）](https://www.apple.com/newsroom/2023/09/apple-unveils-iphone-15-pro-and-iphone-15-pro-max/)
- [Apple：A18 CPU 性能/能效与持续游戏表现声明（2024）](https://www.apple.com/newsroom/2024/09/apple-introduces-iphone-16-and-iphone-16-plus/)
- [Apple：A19 与性能核/能效核配置（2025）](https://www.apple.com/uk/iphone-17/specs/)

### Arm：持续性能、DynamIQ、Cortex-X、Armv9
- [Arm Cortex-A72 与高端移动体验（2015）](https://www.arm.com/company/news/2015/02/arm-sets-new-standard-for-the-premium-mobile-experience)
- [Arm Cortex-A72 核内微架构改进详解（2015）](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/a-walk-through-of-the-microarchitectural-improvements-in-cortex-a72)
- [Arm Cortex-A73：持续性能与能效（2016）](https://www.arm.com/company/news/2016/05/latest-arm-premium-mobile-technology-to-drive-immersive-experiences)
- [Arm DynamIQ 公告（2017）](https://newsroom.arm.com/news/arm-dynamiq-expanding-the-possibilities-for-artificial-intelligence)
- [Arm Cortex-A76 与移动/客户端性能（2018）](https://www.arm.com/ja/company/news/2018/05/arm-announces-new-suite-of-ip-for-premium-mobile-experiences)
- [Arm Cortex-A76 核内微架构详解（2018）](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/cortex-a76-laptop-class-performance-with-mobile-efficiency)
- [Arm Cortex-A77 核内微架构详解（2019）](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/new-arm-cortex-a77-provides-compute-performance-leadership)
- [Arm Cortex-A78 核内微架构详解（2020）](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/arm-cortex-a78-cpu)
- [Arm Cortex-A78 与 Cortex-X1（2020）](https://newsroom.arm.com/news/new-arm-ip-delivers-true-digital-immersion-for-the-5g-era)
- [Arm：未来 Cortex-A big 核转向 64 位（2020 公告）](https://newsroom.arm.com/news/pushing-the-boundaries-of-performance-and-security-to-unleash-the-power-of-64-bit-computing)
- [Arm Cortex-A715（2022）](https://www.arm.com/products/silicon-ip-cpu/cortex-a/cortex-a715)
- [Arm Cortex-A720（2023）](https://www.arm.com/products/silicon-ip-cpu/cortex-a/cortex-a720)
- [Arm Cortex-X925 的 IPC 说明（2024，厂商基准声明）](https://newsroom.arm.com/blog/armv9-cortex-x925-cpu-performance)

### Qualcomm：定制 CPU 路线与平台集成
- [Qualcomm Krait 新一代 Snapdragon CPU 微架构公告（2011）](https://www.qualcomm.com/news/releases/2011/02/qualcomm-announces-next-generation-snapdragon-mobile-chipset-family)
- [Qualcomm Kryo 与 Snapdragon 820（2015）](https://www.qualcomm.com/news/onq/2015/09/snapdragon-820-and-kryo-cpu-heterogeneous-computing-and-role-custom-compute)
- [AnandTech：Snapdragon 835/Kryo 280 半定制核分析（2017）](https://www.anandtech.com/show/10948/qualcomm-snapdragon-835-kryo-280-adreno-540)
- [Samsung Exynos 990 官方规格](https://semiconductor.samsung.com/processor/mobile-processor/exynos-990/)
- [ISCA 2020：Samsung Exynos CPU 微架构演进](https://people.engr.tamu.edu/djimenez/pdfs/exynos_isca2020.pdf)
- [Yonhap：Samsung 终止自研 CPU 项目（2019）](https://en.yna.co.kr/view/AEN20191105001800320)
- [HiSilicon Kirin 980 官方规格](https://www.hisilicon.com/cn/products/kirin/kirin-flagship-chips/kirin-980)
- [Tom’s Hardware：Kirin 9000S 裸片与 Taishan 核第三方分析（2023）](https://www.tomshardware.com/news/die-shot-of-hisilicons-sanction-busting-kirin-9000s-chip-revealed)
- [MediaTek Dimensity 9300 与全大核设计（2023）](https://www.mediatek.com/press-room/mediateks-new-all-big-core-design-for-flagship-dimensity-9300-chipset-maximizes-smartphone-performance-and-efficiency)
- [MediaTek Dimensity 9500 / Arm C1 与 SME2（2025）](https://www.mediatek.com/products/smartphones/mediatek-dimensity-9500)
- [MediaTek Dimensity 9600 Pro / Arm C2（2026）](https://www.mediatek.com/press-room/mediatek-dimensity-9600-pro-sets-new-standard-for-flagship-smartphone-chips)

### 2023–2026：全大核、定制核与 CPU 侧 AI
- [MediaTek Dimensity 9300：All-Big-Core 配置（2023）](https://www.mediatek.com/press-room/mediateks-new-all-big-core-design-for-flagship-dimensity-9300-chipset-maximizes-smartphone-performance-and-efficiency)
- [MediaTek Dimensity 9400：第二代 All-Big-Core 配置（2024）](https://www.mediatek.com/press-room/mediateks-dimensity-9400-flagship-soc-offers-extreme-performance-and-efficiency-for-the-latest-ai-experiences)
- [Qualcomm：Snapdragon 8 Elite 与 Oryon（2024）](https://www.qualcomm.com/news/releases/2024/10/qualcomm-unveils-snapdragon-8-elite-with-the-world-s-fastest-mobile-cpu)
- [Arm Lumex/C1 与 SME2（2025）](https://newsroom.arm.com/news/announcing-lumex-css-platform-ai-era)
- [Arm CSS for Mobile 2/C2 CPU cluster（2026）](https://newsroom.arm.com/news/arm-css-for-mobile-2-agentic-ai-mobile-graphics)
- [MediaTek Dimensity 9600 Pro：C2 CPU 配置（2026）](https://www.mediatek.com/press-room/mediatek-dimensity-9600-pro-sets-new-standard-for-flagship-smartphone-chips)

---

**阶段性结论：** 目前能确认的长期主线是，移动 CPU 从早期提高单核吞吐与扩展多核，逐步演进为在性能层级、能效、持续热表现、软件兼容性和异构系统协同之间做更精细的联合设计。近期 CPU 侧矩阵扩展和工作流协调是新出现的公开信号，但它们应被放在这条历史连续性中理解，而不是当成预先确定的未来答案。

## 7. 第23轮补充：历史硬件变化与 LLVM 软件利用路径的关系

本节将历史时间线与固定 LLVM 23.1.4 源码相连。它补充的是“软件是否存在利用入口”的证据，不改变既有硬件历史事实，也不声称已获得手机端定量结果。细节见[LLVM 23.1.4 目标调度模型核验](LLVM-23.1.4-AArch64-目标调度模型核验-v0.1-2026-10-23.md)、[代码生成优化入口审计](LLVM-23.1.4-代码生成优化入口审计-v0.1-2026-10-23.md)。

| 历史变化方向 | 硬件侧变化的意义 | LLVM 中对应的软件路径 | 因果链中尚缺的环节 |
|---|---|---|---|
| 前端融合与取指供给优化 | 减少前端供给浪费，改善热点指令流效率 | 目标 tuning features、指令选择/peephole、PGO 热路径布局 | 目标 feature 与真实硅片行为的精确对应、实际生成汇编与 workload 结果 |
| 执行资源/调度宽度变化 | 提高可并行执行操作的上限 | scheduler model、MachineScheduler、依赖分析 | LLVM 模型是否准确描述目标手机核心，独立操作是否足够，真实端口/频率/功耗状态 |
| 更大的乱序窗口与更多在途内存操作 | 有机会隐藏依赖和内存延迟 | 指令调度、循环变换、展开与向量化间接暴露 ILP/MLP | LLVM 不直接观察运行时 ROB/LSQ 占用、cache miss 和 DRAM 争用；没有证据保证填满窗口 |
| 寄存器重命名/架构寄存器使用优化 | 降低依赖链代价或减少不必要的值搬运 | 寄存器压力感知调度、register allocation、spill/reload | 软件架构寄存器与硬件内部 PRF 必须分开；目标机生成代码和 spill 数据仍缺 |
| SIMD/新 ISA 扩展（SVE/SME 等） | 为数据并行或矩阵/向量运算提供新能力 | ISA feature、Loop Vectorizer、Clang 属性和 ABI lowering | 目标支持、编译器启用、代码实际走到路径、数据布局/调用边界与端到端收益需同时成立 |
| 分支预测改善 | 降低特定控制流负载的误预测成本 | PGO profile、分支权重、基本块布局 | PGO 只传入行为频率，不直接调节/读取预测器内部状态；真实输入代表性未知 |
| Cache/预取演进 | 改变局部性、miss 延迟和带宽竞争 | 循环/访问模式变换、prefetch hint | 编译器不掌握运行时缓存命中、硬件预取器状态、带宽争用与热降频；需动态证据 |

### 对历史演进叙事的修正

1. **硬件变化不等于软件收益自动兑现。** 软件利用至少经过 ISA/ABI、target model、代码变换和 workload 代表性等中介。
2. **同一个硬件改进可能产生不同的软件收益。** 若 workload 受依赖链或 DRAM 延迟限制，增加执行端口可能无法兑现；若循环可向量化且数据供给充分，向量资源更可能被利用。
3. **编译器模型是历史证据链的一部分，而非硬件真相。** 固定 LLVM 23.1.4 中多个 Cortex target 共享 scheduler model，且源码存在乐观/复制/经验参数。模型共享并不证明核心相同，但提醒我们不能只凭 `-mcpu` 名称推断建模精度。
4. **本项目没有手机端定量归因。** 未运行 benchmark、llvm-mca、仿真或设备测量；对真实产品的净性能和能耗影响继续标注 UNKNOWN。

## 8. 第23轮历史因果链审计状态

跨文档完整性审计见[移动 CPU 微架构历史因果链完整性审计 v0.1](移动CPU微架构历史因果链完整性审计-v0.1-2026-10-23.md)。

**审计判断：** 当前时间线可以支持“证据约束下的历史解释框架”，但不能宣称所有代际的因果链已闭环。A72→A76→A77/A78 是当前公开结构证据相对连续的一条主线；Apple、Samsung 的部分代际有第三方逆向/论文支撑，但需保留方法边界；Qualcomm Oryon、HiSilicon Taishan、近年 Cortex-X/C1/C2 的公开内部机制证据不均衡。

后续叙述统一采用“前代约束/负载背景 → 设计动作 → 作用机制 → 收益/代价 → 后续瓶颈”的结构，并将设计者明确动机与分析推论分开。对瓶颈转移，除非来源明确说明或有针对性证据，否则标记为机制推论而非已证实的代际因果。性能分数不用于反推隐藏微架构；LLVM 模型不等于硬件规格；SoC/整机收益不得全部归因于 CPU 核。

## 9. A72→A76→A77→A78 连续因果主线（第23轮审计）

跨代详细对照已独立归档：[Cortex-A72-A76-A77-A78 跨代因果对照 v0.1](Cortex-A72-A76-A77-A78-跨代因果对照-v0.1-2026-10-23.md)。

**阶段性历史解释：**
- A72：官方资料明确显示，其不是单纯加宽，而是同时调整微操作处理、dispatch、寄存器文件/提交队列活动、分支预测和内存系统，以提升吞吐并控制功耗/面积。
- A76：更明确地提升前端与后端之间的供给能力，并提高 dispatch 带宽和内存级并行能力；软件优化指南还指出 dispatch 存在不同 uop 类别的资源约束，因此峰值带宽不是所有代码都能达到的吞吐。
- A77：官方披露 dispatch、乱序窗口、整数执行和 load/store 相关资源同步提升，MOP cache 与预取器也针对重复代码和数据供给优化。
- A78：官方重点转向固定移动热功耗约束下的持续性能和效率，不能简单叙述为所有结构继续放大。

**因果边界：** A72→A76 的每个具体结构变化是否由某一前代瓶颈直接导致，公开资料没有逐项证明；A77 的更大窗口也不等于 DRAM 瓶颈必然成为下一代设计动因；A78 的持续性能声明不能拆分归因于某个单一结构。更准确的总体规律是：在性能、前端/后端供给、在途并行度和移动热功耗约束之间进行跨阶段协同取舍。


## 10. 第25轮补充：Apple/Samsung自研核的动因证据与连续性边界（2026-10-26）

完整对照与原始出处见[Apple Cyclone/Firestorm vs Samsung Exynos M1–M5机制因果对照](Apple-Cyclone-Firestorm-vs-Samsung-M1-M5-微架构因果比较-v0.1-2026-10-26.md)与[第25轮审计](../02-evidence/audits/round-25-apple-samsung-mechanism-causal-audit-2026-10-26.md)。这里只保留历史时间线中影响结论的变化：

- **2013 Apple A7/Cyclone：** 第三方黑盒与源码线索提示约6-wide、高并行执行与较大的ROB、执行/访存资源；Apple未直接说明各项内部设计的动因。标记**[REVERSE/B 结构；C 动因推论]**。
- **2016–2018 Samsung M1→M3：** 第一手工业论文明确4→6 Dec/Ren/Ret、ROB M2 100→M3 228、PRF扩大，并因更宽后端需求提高预测器供给。标记**[A 设计者直接描述；定量性能属统一2.6GHz/4026 traces模型]**。
- **2018–2020 Samsung M4/M5：** M4预测器更强调代码工作集、M5引入384µop UOC、按热点预测切换三模式来节约重复取指/译码功耗；预取控制和跨缓存/互连/DRAM时钟域的访存优化并进。标记**[A 原始机制与动因；D 单项实机能耗]**。
- **2019 Samsung自研核项目结束：** 项目终止与Exynos业务仍持续是新闻与公司表态所证实的事实，**内在技术/经济权衡未知**；不能把退出归咎某个隐藏的核内失败。
- **2020 Apple A14/Firestorm：** M1等平台的逆向证据观察到8µops/cycle与约330 coalesced-retire groups、约623 rename-retire entries，并有大在途访存/融合/消除路径；这些**不等于623传统ROB，也不等于A14 iPhone的直接量化测试**。标记**[REVERSE/B；内部因果C]**。

**修正后的长周期观察：** 高性能移动核不只加宽，还持续调整指令供给、前端功耗、预测/安全、窗口与访存跨层路径；Apple与Samsung公开机制在部分目标上相互重叠。Apple A8–A13中间代际还不够完整，禁止把2013和2020的估计ROB/retire数字拼成同口径增长曲线。


## 11. 第26轮补充：Apple A8—A13 连续历史节点与CPU—SoC—OS联动（2026-10-26）

已单独归档[Apple A8—A13代际机制与因果链](Apple-A8-A13-代际机制与因果链-v0.1-2026-10-26.md)，其[原始资料AP26-01—18](../02-evidence/sources/round-26-apple-a8-a13-primary-and-reverse-sources-2026-10-26.md)及[逐项审计](../02-evidence/audits/round-26-apple-a8-a13-lineage-claim-audit-2026-10-26.md)是本节证据所有者。

- **2014 A8**：官方强调第二代64位移动能效与持续性能；第三方低层测试显示仍约6-wide、对Cyclone有延迟优化，但ROB“192?”有疑问。**[OFFICIAL_PRODUCT + REVERSE; 内部动机C]**
- **2015 A9**：第三方报告仍约6-wide/192ROB，branch mispredict penalty约16→9 cycles、FP延迟与L2优化，不能把Apple官方CPU70%宣传单独归到branch penalty。**[REVERSE/B; 收益归因C/D]**
- **2016 A10**：Apple公开2P+2E异构CPU，能效核1/5功耗为厂商比较声明；CPU控制策略更重要。**[OFFICIAL/A配置; 能耗归因D]**
- **2017 A11**：Apple官方2P+4E，第二代performance controller使六核同时工作，标志从“两种核型”发展为“不同核型可同时并行”。**[OFFICIAL/A配置与能力; 端到端收益C]**
- **2018 A12**：第三方观察Vortex大核约7-wide/128KB L1、Tempest E核为3-wide OoO，及偏访存负载受cache/存储子系统影响；Apple官方核心组仍2P+4E。**[REVERSE/B，受SPEC工具链/制程/系统限制]**
- **2019 A13**：第三方观察Lightning大核7-wide不再全面扩宽，Thunder E核大幅提升FP/SIMD、L1D；SLC增至推断16MB，OS/DVFS小核→大核迁移在具体工作负载下从约54ms缩短到30ms。低DRAM频点可能令特定E核访存负载退步。**[REVERSE+MEASUREMENT/B; 阈值/收益不是所有负载事实]**

**本轮历史含义：** Apple并非沿“逐代扩ROB/issue宽度”单一路线发展；高性能核逐渐与更强的E核、共享内存层次、操作系统工作负载调度和电源状态决策形成一体化设计。在第25轮Apple/Samsung对照中，该案例支持“负载/电热/数据路径驱动优化”的解释，但不证明Apple内部每个芯内设计决策的因果来源。
