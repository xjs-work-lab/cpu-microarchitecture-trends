# 移动 CPU 微架构历史变化时间线与因果分析 v0.1

**更新时间：2026-10-23｜研究窗口：2007–2026｜资料模式：PUBLIC_ONLY**  
**本文件性质：第一版证据约束下的历史综合，不是完整产品清单，也不是新技术立项建议。**

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
| **2011–2014：big.LITTLE 把“峰值性能”和“日常能耗”分开优化** | Cortex-A15/A7 等高性能核与高能效核组合，通过异构集群和软件调度，让不同任务在不同能效区间执行。2012 年后 A57/A53 延续这一思路。Apple 的 A10 Fusion（2016）后来也公开采用 2 个性能核加 2 个高能效核，说明异构 CPU 并非单一厂商路线。 | 手机负载是间歇的：网页/游戏可能短时高强度，消息、音频和后台任务则更轻；电池容量和可散热功率有限。Arm 对 big.LITTLE 的说明直接把这种负载差异与电池寿命目标联系起来。 | 同一 SoC 可以兼顾突发性能与低负载能效；代价是异构调度、任务迁移、缓存/一致性和功耗管理更复杂。Arm 宣称特定常见负载下平均应用处理器功耗可降低“最高 70%”，应保留为厂商条件性声明，不能泛化到所有应用/手机。 | **A/B**：设计动因明确；实际收益高度依赖负载、调度器和实现。 |
| **2012–2015：64 位从架构路线进入手机产品** | Armv8-A 和 Cortex-A53/A57 引入 AArch64，并兼顾当时的 32 位软件生态；Apple A7 于 2013 年进入 iPhone 5s，Apple 同时强调 iOS 7 与系统应用针对 64 位设计。 | 更大的地址空间、系统软件能力、长期应用性能与架构演进是推动因素。Arm 明确提及更大物理地址空间及虚拟化等能力；Apple 则把 64 位作为整机软件和应用生态升级的一部分。不能将转向 64 位简化为“因为手机内存超过 4GB”。 | 64 位不仅是地址宽度变化，也改变寄存器/调用约定、编译器、ABI、系统库和应用发布链路。潜在收益依具体代码而异；更宽指针也可能增加部分数据结构的内存占用。Apple A7 的微架构拆解显示其强调较宽的乱序执行资源，但具体宽度/ROB 数字属于第三方逆向估计，不是 Apple 官方披露。 | **A/B**：产品与 ISA 变化明确；不同收益需按软件和负载分别验证。 |
| **2015–2017：持续性能、能效和面积效率成为核心设计目标** | Cortex-A72 面向高端手机并针对 16nm FinFET+ 等工艺；Cortex-A73 强调更小面积、能效和持续性能。Arm 公开把复杂相机/视频、游戏、较大显示和常驻传感等体验与严格的手机功耗/热预算联系起来。 | 用户需求不再只是短时跑分：高分辨率影像、游戏、多应用和常驻功能带来更复杂的混合负载；无风扇机身需要控制表面温度和长期功耗。 | 设计目标从单纯提高峰值，转向在给定功耗/面积下保持更高的持续性能。Arm 对 A72/A73 的能效与性能百分比是其目标配置下的厂商声明；由于同时涉及微架构、制程和 SoC/手机实现，不能把代际差异全部归因于 CPU 微架构。 | **A/B**：热/能效目标有直接资料；单项技术的独立贡献仍不明。 |
| **2016–2018：异构核设计从“两个集群”走向更灵活的集群组织** | Arm 于 2017 年公布 DynamIQ，将 big 与 LITTLE 核组合在同一集群设计框架中，并通过 DynamIQ Shared Unit 提供集群级共享资源；它扩展了核心组合和集群配置选择。 | 核心类型、并发任务和计算密度持续增加，SoC 需要更灵活地组合不同性能/能效的核。Arm 将 DynamIQ 与持续增长的计算需求、AI 等新负载联系起来。 | 更灵活的异构配置为调度、共享缓存和集群扩展提供了新的实现空间；实际收益仍依赖 SoC 采用的核组合、缓存/互连配置与 OS 调度。DynamIQ 是可配置的 IP/集群技术，不代表所有手机都采用相同物理拓扑。 | **A/B**：设计意图直接公开；各产品实际收益与拓扑须逐款核对。 |
| **2018–2020：高性能核继续提高 IPC，同时向更广泛的客户端负载扩展** | Cortex-A76 采用新微架构；Arm 宣称其相较前代有 35% 性能提升和 40% 能效提升，并强调 7nm 工艺和“笔记本级”性能。2020 年 Arm 同时推出面向持续性能/效率的 Cortex-A78 和偏重峰值性能的 Cortex-X1/Cortex-X 定制项目。 | 手机承担更重的生产力、多任务、游戏与计算负载；与此同时，制程缩放不再足以单独支撑性能增长，移动平台也不能无限提高频率和功耗。 | 核心路线开始更明确地分层：一类优化持续性能和能效，另一类把更多设计预算投向峰值单线程性能。A76 的跨代数字同时受微架构、工艺和目标配置影响；X 系列则体现了性能目标分层，不代表所有 SoC 都会选择最大核或相同核数。 | **A/B**：产品策略和设计目标明确；跨代百分比的独立因果不可拆分。 |
| **2020–2022：Armv9、向量/安全扩展与 64 位软件迁移相互交织** | Armv9 将 SVE2 等扩展带入客户端路线，并强化安全方向；Arm 在 2020 年宣布，从 2022 年的 IP 开始，未来 Cortex-A “big” 核只支持 64 位执行。 | 软件工作负载对向量化、媒体/信号处理、机器学习和安全能力的需求增长；同时，长期维护 AArch32/AArch64 两套执行环境会增加架构与生态复杂度。 | 新 ISA 扩展提供软件可用的新能力，但只有 OS、编译器、库和应用实际使用后才可能转化为收益。big 核不再支持 AArch32 是 IP 路线的变化，不等于同一时间所有 Android 手机、所有小核或所有应用都完成 32 位淘汰。 | **A/B**：路线公告明确；生态迁移与应用收益有不同时间表。 |
| **2022–2024：细分核心等级与“全大核”成为并存路线** | Arm 持续区分 Cortex-X 性能核、A7x 平衡/效率核与 A5x 高能效核；另一方面，MediaTek Dimensity 9300 于 2023 年采用 4× Cortex-X4 + 4× Cortex-A720 的 All-Big-Core 配置，Dimensity 9400 延续全大核设计。 | 高端游戏、影像、端侧生成式 AI 和多线程负载提高了对持续并行吞吐的要求；新核心的性能/能效改善也使厂商可以重新评估“小核”的数量与角色。 | 这不是“全行业都不再需要小核”的证据。All-Big-Core 是厂商选择的一条路线，A720 仍与 X4 有不同定位；Apple A19（2025）仍采用 2 性能核 + 4 能效核。不同路线的后台能耗、峰值/持续性能和面积代价需通过同口径设备测量比较。 | **B/C**：产品配置是事实；其背后的因果解释及普适性仍有限。 |
| **2023–2024：定制 CPU 微架构重新成为高端手机平台的显著差异点** | Qualcomm 于 2024 年把定制 Oryon CPU 引入 Snapdragon 8 Elite 手机平台；Apple 则长期维持自研 CPU 核路线。 | 高端平台竞争从单纯采用通用 CPU IP，进一步涉及单线程性能、能效、平台差异化以及 CPU 与 GPU/NPU 的协同。Qualcomm 将 Oryon 与端侧多模态生成式 AI 时代联系起来。 | 定制微架构可以让厂商针对目标产品做不同的性能、缓存和功耗取舍；但公开资料没有披露全部微架构细节，也不能仅凭厂商峰值数字判定其相对其他厂商的普遍优势。Oryon 不是 Qualcomm 历史上第一次设计定制 CPU，而是其新一代定制架构进入旗舰手机的重要节点。 | **B/C**：产品事实明确；动因有厂商表述，跨厂商优势须独立验证。 |
| **2025：CPU 侧向量/矩阵计算能力与系统级 AI 计算更紧密结合** | Arm Lumex/C1 平台把 SME2 纳入 CPU 集群级设计；Arm 将其与低延迟端侧 AI、实时翻译、语音和个性化应用联系起来。 | 端侧 AI 不只有 NPU 上的大规模推理，也包含控制逻辑、短任务、前后处理和需要低延迟响应的部分工作；CPU 可能需要执行一部分小型模型或矩阵工作，并与 GPU/NPU 协作。 | CPU 的职责开始在部分实现中从传统通用执行进一步延伸到向量/矩阵计算与异构工作流协同。SME2 是可选扩展/平台能力，具体是否进入量产 SoC、由软件栈开放，以及是否优于 NPU，必须逐产品核验；不能据此得出 NPU 会被 CPU 取代。 | **A/B**：平台能力和设计目标有直接资料；具体终端收益取决于实现与软件。 |
| **2026：面向持续 AI 工作流的 CPU 集群与 SoC 协同被明确提出** | Arm 于 2026 年 9 月公布 CSS for Mobile 2/C2 CPU cluster：C2-Ultra 面向高单线程与低延迟，C2-Pro 面向持续能效，并配有两个 SME2 单元。MediaTek 于 2026 年 9 月公布 Dimensity 9600 Pro，采用 2× C2-Ultra + 6× C2-Pro 的 2+3+3 分组。 | 厂商明确提出，持续运行的 agentic AI 不只是调用一次模型，还要保持上下文、运行应用、协调服务、规划并把工作分配给 CPU/GPU/AI 加速器，同时受手机功耗与散热限制。 | 这是截至资料截点的最新公开设计信号：CPU 被描述为系统级工作流协调者，并在某些任务中直接执行低延迟 AI；高性能核与效率核仍然分层存在。需注意 C2/CSS 与 Dimensity 9600 Pro 的性能、功耗数字属于厂商公布结果；量产设备的长期体验、软件实际使用率和跨厂商普适性仍需独立验证。 | **A（设计动因）/C（普适趋势）**：官方动因明确，但不能把厂商路线等同于全行业必然方向。 |

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

这版时间线建立了主要节点，但**尚不是完整历史审计**。下一轮应优先做三件事：

1. **逐节点核验原始证据**：把 Arm IP 公告、架构文档、Apple/Qualcomm/MediaTek 官方资料与独立分析逐条绑定到时间线节点，补发布日期、实际量产/上市时间与来源类型。
2. **补强 2010–2024 的 CPU 核微架构细节**：特别是取指/译码、分支预测、乱序窗口、load/store、寄存器重命名和缓存层次；只写公开证据可支持的变化，不猜隐藏实现。
3. **把“原因”与“同时发生”分开**：每个节点明确标注厂商明说、跨源支持、合理推论或未知；性能/能耗百分比保留原始测试口径与厂商归属。

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
- [Arm Cortex-A73：持续性能与能效（2016）](https://www.arm.com/company/news/2016/05/latest-arm-premium-mobile-technology-to-drive-immersive-experiences)
- [Arm DynamIQ 公告（2017）](https://newsroom.arm.com/news/arm-dynamiq-expanding-the-possibilities-for-artificial-intelligence)
- [Arm Cortex-A76 与移动/客户端性能（2018）](https://www.arm.com/ja/company/news/2018/05/arm-announces-new-suite-of-ip-for-premium-mobile-experiences)
- [Arm Cortex-A78 与 Cortex-X1（2020）](https://newsroom.arm.com/news/new-arm-ip-delivers-true-digital-immersion-for-the-5g-era)
- [Arm：未来 Cortex-A big 核转向 64 位（2020 公告）](https://newsroom.arm.com/news/pushing-the-boundaries-of-performance-and-security-to-unleash-the-power-of-64-bit-computing)
- [Arm Cortex-A715（2022）](https://www.arm.com/products/silicon-ip-cpu/cortex-a/cortex-a715)
- [Arm Cortex-A720（2023）](https://www.arm.com/products/silicon-ip-cpu/cortex-a/cortex-a720)
- [Arm Cortex-X925 的 IPC 说明（2024，厂商基准声明）](https://newsroom.arm.com/blog/armv9-cortex-x925-cpu-performance)

### 2023–2026：全大核、定制核与 CPU 侧 AI
- [MediaTek Dimensity 9300：All-Big-Core 配置（2023）](https://www.mediatek.com/press-room/mediateks-new-all-big-core-design-for-flagship-dimensity-9300-chipset-maximizes-smartphone-performance-and-efficiency)
- [MediaTek Dimensity 9400：第二代 All-Big-Core 配置（2024）](https://www.mediatek.com/press-room/mediateks-dimensity-9400-flagship-soc-offers-extreme-performance-and-efficiency-for-the-latest-ai-experiences)
- [Qualcomm：Snapdragon 8 Elite 与 Oryon（2024）](https://www.qualcomm.com/news/releases/2024/10/qualcomm-unveils-snapdragon-8-elite-with-the-world-s-fastest-mobile-cpu)
- [Arm Lumex/C1 与 SME2（2025）](https://newsroom.arm.com/news/announcing-lumex-css-platform-ai-era)
- [Arm CSS for Mobile 2/C2 CPU cluster（2026）](https://newsroom.arm.com/news/arm-css-for-mobile-2-agentic-ai-mobile-graphics)
- [MediaTek Dimensity 9600 Pro：C2 CPU 配置（2026）](https://www.mediatek.com/press-room/mediatek-dimensity-9600-pro-sets-new-standard-for-flagship-smartphone-chips)

---

**阶段性结论：** 目前能确认的长期主线是，移动 CPU 从早期提高单核吞吐与扩展多核，逐步演进为在性能层级、能效、持续热表现、软件兼容性和异构系统协同之间做更精细的联合设计。近期 CPU 侧矩阵扩展和工作流协调是新出现的公开信号，但它们应被放在这条历史连续性中理解，而不是当成预先确定的未来答案。
