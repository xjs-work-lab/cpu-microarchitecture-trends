# 第十九轮：移动 CPU 历史时间线初始来源审计（2026-10-23）

**目的：** 为[移动 CPU 微架构历史变化时间线 v0.1](../../03-analysis/移动CPU微架构历史变化时间线-v0.1-2026-10-23.md)建立来源到主张的初始映射，并明确来源能证明什么、不能证明什么。  
**状态：** INITIAL_SOURCE_AUDIT / NOT_EXHAUSTIVE / CAUSAL_ATTRIBUTION_PARTIAL

## 1. 审计规则

详细的核内来源卡片见[第十九轮移动 CPU 核内微架构原始来源](../sources/round-19-移动CPU核内微架构原始来源.md)，包括 A9、Krait、A72、A76、A77/A78 和 Apple Cyclone 的公开资料与限制。

- **产品/架构事实**优先采用 Arm、Apple、Qualcomm、MediaTek 官方公告、产品页或架构文档。
- **设计动因**若来自厂商公告，标为“厂商明确陈述”，不等于独立证明该因果。
- **性能/能效数字**保留厂商、对照对象、配置和测试口径；未找到完整方法时不升级为独立实测。
- **第三方逆向**可补足公开资料未披露的微架构细节，但必须标注为估计/逆向结论，不作为厂商确认规格。
- **历史解释**若由多个同期事实综合得出，标为推论；不得仅凭前后代际变化声称某项改动造成全部性能提升。

## 2. 来源—主张—边界映射

| ID | 原始来源 | 可支撑的历史主张 | 来源类型 | 不能单独证明的事项 |
|---|---|---|---|---|
| S19-01 | [Arm Cortex-A8 产品支持](https://support.arm.com/compute-ip/cortex-a8) | Armv7-A、NEON、双发射、单核应用处理器等早期设计特征 | 官方 IP 文档/产品支持 | 不能代表所有 2007 年量产手机，也不能量化其对用户体验的独立贡献 |
| S19-02 | [Arm：Cortex-A9 的诞生与演进](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/the-birth-evolution-of-cortex-a9-and-what-s-coming-next) | A9 的部分乱序设计、最多四核 MPCore、相对 A8 的厂商 IPC/功耗说法，以及从频率扩展转向核心数扩展的历史回顾 | Arm 工程博客（2013 回顾） | 25% IPC 是 Arm 陈述；不能当作统一独立测试，也不能证明多核对所有应用有收益 |
| S19-03 | [Arm：Cortex-A 移动产品路线回顾](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/a-walk-through-the-cortex-a-mobile-roadmap) | A8/A9/A15 等阶段的产品定位、乱序与多核路线、A15 的性能/地址空间/虚拟化背景 | Arm 工程博客（回顾） | 回顾材料不能替代每代核心的完整技术参考手册 |
| S19-04 | [Arm big.LITTLE 技术说明](https://www.arm.com/technologies/big-little)；[2011 年设计背景论文/文章](https://www.eetimes.com/Big-LITTLE-processing-with-ARM-Cortex-A15---Cortex-A7/) | 高强度与低强度任务并存、电池续航与性能并重、异构核心调度的设计动因 | Arm 官方技术说明 + 同期工程文章 | “最高 70%”等节能数字受工作负载、调度和实现条件限制 |
| S19-05 | [Arm Cortex-A50 / A53 / A57 公告](https://www.arm.com/company/news/2012/10/arm-launches-cortex-a50-series-the-worlds-most-energy-efficient-64-bit-processors) | Armv8-A、AArch64 与 A53/A57 的高效/高性能分工、32/64 位兼容路线 | 官方发布公告 | 不能单独证明所有后续手机的迁移时间或应用性能收益 |
| S19-06 | [Apple iPhone 5s/A7 公告](https://www.apple.com.cn/newsroom/2013/09/10Apple-Announces-iPhone-5s-The-Most-Forward-Thinking-Smartphone-in-the-World/) | 64 位进入智能手机产品，以及 iOS 7/系统应用面向 64 位设计 | Apple 官方产品公告 | 不能证明 64 位对所有程序都带来相同加速 |
| S19-07 | [AnandTech：Cyclone 微架构拆解](https://www.anandtech.com/show/7910/apples-cyclone-microarchitecture-detailed) | A7/Cyclone 的宽执行、乱序资源等第三方逆向估计 | 第三方技术分析/逆向 | 不是 Apple 官方披露；应保留测量方法、推导与估计不确定性 |
| S19-08 | [Arm Cortex-A72 公告](https://www.arm.com/company/news/2015/02/arm-sets-new-standard-for-the-premium-mobile-experience)；[Cortex-A73 公告](https://www.arm.com/company/news/2016/05/latest-arm-premium-mobile-technology-to-drive-immersive-experiences) | 高端移动负载、16nm FinFET、面积/能效/持续性能目标 | 官方 IP 公告 | 跨代收益同时受微架构、工艺、频率、SoC 配置和整机散热影响 |
| S19-09 | [Apple A10 Fusion 公告](https://www.apple.com/newsroom/2016/09/apple-introduces-iphone-7-iphone-7-plus/) | 2 性能核 + 2 高能效核，厂商公开的相对性能/功耗定位 | Apple 官方产品公告 | 不说明其调度策略全部细节，也不能与 Arm big.LITTLE 数字直接横比 |
| S19-10 | [Arm DynamIQ 公告](https://newsroom.arm.com/news/arm-dynamiq-expanding-the-possibilities-for-artificial-intelligence)；[DynamIQ 技术说明](https://www.arm.com/en/technologies/dynamiq) | 单一集群中组合不同 CPU 核的设计框架、可配置性与共享单元概念 | 官方公告/技术页 | 不代表每款 SoC 使用相同集群配置或同一缓存/互连实现 |
| S19-11 | [Arm Cortex-A76 公告](https://www.arm.com/ja/company/news/2018/05/arm-announces-new-suite-of-ip-for-premium-mobile-experiences) | 新微架构、7nm 目标配置、性能与能效宣传口径 | 官方 IP 公告 | 35%/40% 数字不是跨厂商独立比较，不能拆分工艺与微架构贡献 |
| S19-12 | [Arm A78/X1 公告](https://newsroom.arm.com/news/new-arm-ip-delivers-true-digital-immersion-for-the-5g-era)；[64 位路线公告](https://newsroom.arm.com/news/pushing-the-boundaries-of-performance-and-security-to-unleash-the-power-of-64-bit-computing) | 持续性能型与峰值性能型 CPU IP 分层，以及 2022 年起大核转向仅支持 64 位的公开路线 | 官方路线/产品公告 | 不能将 IP 路线等同于所有手机的同步采用，也不能证明某种核配置普遍优胜 |
| S19-13 | [Apple A17 Pro 公告](https://www.apple.com/newsroom/2023/09/apple-unveils-iphone-15-pro-and-iphone-15-pro-max/)；[A18 公告](https://www.apple.com/newsroom/2024/09/apple-introduces-iphone-16-and-iphone-16-plus/) | 近年 Apple 仍在宣称 CPU 微架构/设计改进，并把能效与持续游戏表现放在同一系统中说明 | Apple 官方产品公告 | 不能从公告反推出具体 ROB、分支预测器或执行端口参数；性能数字为厂商口径 |
| S19-14 | [MediaTek Dimensity 9300 公告](https://www.mediatek.com/press-room/mediateks-new-all-big-core-design-for-flagship-dimensity-9300-chipset-maximizes-smartphone-performance-and-efficiency)；[Dimensity 9400 公告](https://www.mediatek.com/press-room/mediateks-dimensity-9400-flagship-soc-offers-extreme-performance-and-efficiency-for-the-latest-ai-experiences) | All-Big-Core 作为真实存在的旗舰手机 CPU 配置分支 | MediaTek 官方产品公告 | 不能据此断言小核路线已被淘汰；能效和持续热表现需同条件设备测量 |
| S19-15 | [Qualcomm Oryon 官方页面](https://www.qualcomm.com/processors/oryon)；[Snapdragon 8 Elite 公告](https://www.qualcomm.com/news/releases/2024/10/qualcomm-unveils-snapdragon-8-elite-with-the-world-s-fastest-mobile-cpu) | Oryon 定制 CPU 进入旗舰手机平台的产品事实与厂商设计定位 | Qualcomm 官方产品页/公告 | 未公开的微架构结构不能从峰值性能反推；厂商“最快”等说法需要独立测量验证 |
| S19-16 | [Arm Lumex/C1 公告](https://newsroom.arm.com/news/announcing-lumex-css-platform-ai-era)；[C1-Ultra 产品资料](https://www.arm.com/products/silicon-ip-cpu/c1-ultra) | SME2、CPU 侧矩阵能力与移动计算子系统平台化 | Arm 官方平台公告/产品页 | 不代表所有 C1 SoC 都启用 SME2，也不证明所有 AI 任务放在 CPU 上更好 |
| S19-17 | [Arm CSS for Mobile 2/C2 公告](https://newsroom.arm.com/news/arm-css-for-mobile-2-agentic-ai-mobile-graphics)；[C2 CPU 集群资料](https://www.arm.com/products/silicon-ip-cpu/c2-cpu-cluster) | 2026 年公开提出的 C2-Ultra/C2-Pro 与双 SME2 集群，以及 CPU 协调持续 AI 工作流的设计叙述 | Arm 官方平台/产品资料 | 设计公告不自动证明终端长期收益；厂商内部测试数据尚非独立复验 |
| S19-18 | [MediaTek Dimensity 9600 Pro 公告](https://www.mediatek.com/press-room/mediatek-dimensity-9600-pro-sets-new-standard-for-flagship-smartphone-chips)；[规格页](https://www.mediatek.com/products/smartphones/mediatek-dimensity-9600-pro) | 2026 年 2× C2-Ultra + 6× C2-Pro 配置、缓存与内存平台公开信息 | MediaTek 官方产品公告/规格页 | 代际性能/功耗百分比为厂商声明；不能只凭单款产品确定“全大核”是否成为行业主流 |

| S19-19 | [Qualcomm Krait 新一代 Snapdragon CPU 微架构公告（2011）](https://www.qualcomm.com/news/releases/2011/02/qualcomm-announces-next-generation-snapdragon-mobile-chipset-family) | Krait 作为 Qualcomm 新一代 CPU 微架构路线、单/双/四核配置，以及与更复杂移动负载的产品定位 | Qualcomm 官方公告 | 性能提升 150%、功耗降低 65% 是厂商自报比较；不能当作独立统一测试，也不能由此推出与 Cortex 同条件胜负 |
| S19-20 | [Arm Cortex-A72 核内微架构改进详解（2015）](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/a-walk-through-of-the-microarchitectural-improvements-in-cortex-a72) | A72 的 3-wide decode/8-wide issue、5-wide dispatch、分支预测、寄存器文件功耗优化、预取、load/store buffer 与 TLB 改进等直接披露 | Arm 工程博客/核内设计说明 | 性能和能效收益属于 Arm 指定配置/测试口径；不能把超过 50% 内存带宽等数字外推为所有 SoC/负载结果 |
| S19-21 | [Arm Cortex-A76 核内微架构详解（2018）](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/cortex-a76-laptop-class-performance-with-mobile-efficiency) | A76 4-wide decode、分离分支预测与取指、每周期取指/dispatch能力、双 128-bit SIMD/FP 吞吐和更深 memory-level parallelism | Arm 工程博客/核内设计说明 | 不证明每个量产 SoC 都使用相同缓存、频率和物理实现；跨代性能提升也受到工艺与系统配置影响 |
| S19-22 | [Arm Cortex-A77 微架构说明](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/new-arm-cortex-a77-provides-compute-performance-leadership)；[Arm Cortex-A78 微架构说明](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/arm-cortex-a78-cpu) | A77 的 MOP cache、分支预测带宽/BTB、dispatch/乱序窗口改进；A78 对同热功耗预算下持续性能和结构功耗效率的设计说明 | Arm 工程博客/核内设计说明 | 不能由 MOP cache 存在推断所有代码都命中；20% 持续性能为 Arm 指定比较口径，不等于跨手机独立实测 |

| S19-23 | [Arm Cortex-A78 Core Technical Reference Manual](https://documentation-service.arm.com/static/64bea12b38511951cb7a0ee8)，Issue 09（2023） | 指令取指、动态分支预测、1.5K-entry L0 Macro-OP cache、寄存器重命名、issue queues 与乱序执行的公开技术描述 | Arm 非保密技术参考手册 | 文档说明 A78，不自动证明相较 A77 的全部新增项；实现选项需按具体配置核对 |

## 3. 初步审计结论

1. **架构/产品事实：** 早期乱序/多核、big.LITTLE、Armv8-A 64 位、DynamIQ、A76/A78/X1 分层、All-Big-Core、Oryon、C1/SME2、C2 等节点均有可定位的官方或技术来源。
2. **设计动因：** 对任务强度差异、电池续航、持续性能/热预算、异构计算和端侧 AI 工作流，厂商有直接说明；但厂商说明主要证明设计目标和产品叙事，不等于独立因果实验。
3. **定量收益：** 多数公开百分比属于厂商发布口径；本轮没有把这些数字当成同平台、同工艺、同设备的可比实测。
4. **隐藏微架构：** 取指/译码宽度、ROB/LSQ 容量、物理寄存器数量、分支预测器结构和缓存命中率仍未形成跨代可靠数据表。第三方逆向资料只能单独标记，不能和官方规格混为一谈。
5. **下一步审计重点：** 为时间线中每个转折补齐原始发布日期、实际采用/量产产品、版本、同代竞争路线与来源独立性；随后单独研究可公开核实的微架构内部变化，明确未披露部分。

## 4. 状态

`INITIAL_SOURCE_AUDIT / ARCHITECTURE_FACTS_GROUNDED / DESIGN_MOTIVES_PARTIALLY_GROUNDED / QUANTITATIVE_CAUSAL_ATTRIBUTION_INCOMPLETE / HIDDEN_CORE_DETAILS_UNKNOWN`
