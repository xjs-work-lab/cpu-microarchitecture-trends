# 移动 CPU 跨厂商微架构路线与产品化时间 v0.2

**更新时间：2026-10-23｜资料模式：PUBLIC_ONLY**  
**研究问题：** 不只是按 SoC 名称排列时间线，而是分辨 CPU 核微架构由谁设计、采用什么授权/集成方式、何时真正进入 SoC 与手机，以及路线为何发生变化。  
**关联主线：** [移动 CPU 历史变化时间线 v0.1](移动CPU微架构历史变化时间线-v0.1-2026-10-23.md)；[第十九轮核内来源卡](../02-evidence/sources/round-19-移动CPU核内微架构原始来源.md)。

## 1. 核心结论

1. **“自研 CPU”不是一个足够精确的类别。** 至少要区分完整自研核内微架构、基于 Arm Cortex 的半定制核、直接采用 Cortex IP、以及采用 Arm CSS/C1/C2 并在 SoC 层配置/集成。
2. **Qualcomm 的品牌名 Kryo 并不意味着每一代使用同一类设计。** 2015 年 Snapdragon 820 的 Kryo 是 Qualcomm 所称的自研 64 位核；2017 年 Kryo 280 改用 Arm “Built on Cortex” 半定制许可；2024 年 Snapdragon 8 Elite 的 Oryon 是新一代自研 CPU 路线。
3. **定制 CPU 不是单向、必然持续的路线。** Apple 从 Swift/Cyclone 后持续演进自研核；Samsung 的 Mongoose/M1–M5 路线则于 2019 年终止。公开资料支持“路线不同且可能中止”，但不能把 Samsung 的全部内部原因归结为单一的 IPC 或能效差距。
4. **HiSilicon 的历史不能用一条“始终 Cortex”或“始终自研”概括。** Kirin 980 明确采用 Cortex-A76/A55；Kirin 9000S/9010 的 Taishan 核由第三方公开分析识别，但官方完整核内细节未披露。
5. **采用 Arm CPU IP 不等于没有 SoC 设计空间。** Dimensity 9300 用 Cortex-X4/A720 组成全大核配置；Dimensity 9500 使用 Arm C1 系列和 SME2。配置、缓存/内存、调度和异构引擎协同依然是 SoC 厂商的重要控制点。
6. **发布到终端落地的日期链本身是证据。** 它能确认路线何时从公告进入产品，不足以独立证明设计动因或性能优势。

## 2. 路线分类

| 路线类别 | 定义 | 本轮公开案例 | 应避免的错误 |
|---|---|---|---|
| **R1：完整自研 CPU 核内微架构** | 厂商在 Arm ISA/兼容体系下自行设计前端、分支预测、乱序执行、执行端口、缓存等核心结构 | Apple Swift/Cyclone 及后续 A 系列核；Qualcomm Krait、Snapdragon 820 首代 Kryo、Oryon；Samsung Mongoose；HiSilicon Taishan（第三方逆向识别） | 不可将不同厂商、不同代的所有核视为同等成熟；也不能因有自研核就推定能效/性能必然更优 |
| **R2：基于 Cortex 的半定制 CPU 核** | 以 Arm Cortex 核为基础，允许合作方修改部分设计或配置 | Qualcomm Kryo 280 的 “Built on ARM Cortex Technology” 路线 | 不应把 Kryo 280 写成与 2015 年首代 Kryo 相同的完整自研微架构；其具体基础核来自第三方推断而非 Qualcomm 官方确认 |
| **R3：采用标准 Cortex CPU IP，差异化放在 SoC/集群层** | 采用 Arm 设计的 CPU 核，通过核心数量/频率档位、缓存、互连、内存、调度和整机软硬件协同做产品设计 | HiSilicon Kirin 980；MediaTek Dimensity 9300 | 不能因为 CPU 核是 Arm IP 就说 SoC 没有自研价值；也不能把 SoC 调度创新称为 CPU 核内微架构自研 |
| **R4：Arm CSS/新一代 C1/C2 平台集成** | 采用 Arm 新 CPU IP、SME2 等扩展及可选平台/物理实现，再由 SoC 厂商配置和集成 | MediaTek Dimensity 9500/C1；Dimensity 9600 Pro/C2 | 不能把 Arm C1/C2 的核内设计归为 MediaTek 自研；也不能把平台发布的 AI 性能数字当成独立设备测量 |

## 3. 发布—SoC—终端时间链

| 路线/节点 | CPU/架构公告 | SoC 集成/公告 | 手机产品/上市节点 | 可得到的历史解释 |
|---|---|---|---|---|
| Qualcomm Krait | 2011-02-13 公布 Krait 微架构 | Snapdragon S4 家族于 2011 年公布 | HTC One S/One XL 于 2012 年公布；One S 在美国由 T-Mobile 于 2012-04-25 上市 | Krait 从架构公告到手机落地跨越约一年以上；不要把架构宣布日期当作量产日期 |
| Apple Swift/Cyclone | A6/iPhone 5 于 2012-09-12 公布；A7/iPhone 5s 于 2013-09-10 公布 | A6/A7 随 Apple 自有 SoC 产品化 | iPhone 5 于 2012-09-21 上市；iPhone 5s 于 2013 年 9 月上市 | Apple 的核心/SoC/OS 由同一厂商协同设计，能够快速把自研 CPU 与系统软件整合；这属于垂直整合优势的合理解释，不是单一来源测量出的因果 |
| Qualcomm Kryo | Kryo/820 路线于 2015 年公布 | Snapdragon 820 于 2015 年 11 月公开；首款搭载手机 Le Max Pro 于 2016-01-04 公布 | Qualcomm 当时预计 2016 上半年上市；该来源没有证明所有市场的首个零售日期 | 公告与终端落地之间需单独追踪；首代 Kryo 的完全自研路线不应外推到所有 Kryo 品牌产品 |
| Qualcomm Kryo 280 半定制 | “Built on ARM Cortex Technology” 在 2017 年产品中采用 | Snapdragon 835 于 2017-01-02 公布 | Galaxy S8 部分市场版本搭载 835，Samsung 于 2017-04-21 宣布首批市场上市 | 半定制路线可在设计控制、成本/周期和产品差异化间折中；这是技术路线选择，不是“自研必然越来越多”的证据 |
| Samsung Mongoose | 自研 CPU 团队于 2011 年建立；M1–M5 代际在 ISCA 2020 工业论文回顾 | Exynos 990 于 2019-10 公布，含两颗第五代自研核 | Galaxy S20 系列于 2020 年上市，Exynos 990/M5 为最后一代量产自研路线；项目于 2019 年宣布终止 | 自研路线可能因产品竞争力、成本和组织决策而中止；公开证据不足以对内部权衡做精确归因 |
| Arm Cortex-A76 / HiSilicon | Cortex-A76 于 2018-05-31 公布 | Kirin 980 于 2018 年公布；官方称其为首款商用 Cortex-A76-based SoC | Mate 20 系列于 2018-10-16 公布 | 从 Arm IP 到 SoC 和手机产品有清晰时间链；HiSilicon 的差异化体现为 2+2+4 频率/调度组织与系统集成，而不是自研 A76 核 |
| HiSilicon Taishan | Kirin 9000S 于 2023 年进入 Mate 60 产品 | 第三方裸片/CPU ID/基准分析将高性能核识别为 Taishan 系列 | Mate 60 系列于 2023 年上市 | 表明华为路线在公开证据上出现了与早期 Cortex 核不同的高性能核线索；但具体核内结构、指令吞吐、缓存和功耗尚未有完整官方公开说明 |
| MediaTek Dimensity 9300 | Cortex-X4/A720 是 Arm IP 路线 | SoC 于 2023-11-06 公布，4×X4 + 4×A720 | vivo X100 系列于 2023-11-13 发布 | 全大核是 MediaTek 的核心组合选择，不等于其重做 X4/A720 核内微架构；这条路线反映产品配置探索而非行业统一转向 |
| Arm C1 / MediaTek Dimensity 9500 | Arm Lumex/C1 于 2025-09-10 公布 | Dimensity 9500 于 2025-09-22 公布，使用 C1-Ultra/Premium/Pro 与 SME2 | vivo X300 系列于 2025-10-13 发布、10-17 开售 | 这是从 Arm 新 CPU/SME2 公告到商业手机发布约一个月的案例；说明平台集成周期可以很短，但不能泛化为所有设计项目 |
| Arm C2 / MediaTek Dimensity 9600 Pro | Arm CSS for Mobile 2/C2 于 2026-09-08 公布 | Dimensity 9600 Pro 于 2026-09-15 公布，公开配置 2×C2-Ultra + 6×C2-Pro | Arm 2026 年 9 月产品回顾称 vivo X500 Pro 与 OPPO Find X10 系列搭载该平台 | 当前最新公开案例把 C2、SME2 和 agentic AI 设计叙事带入 SoC/手机；性能与持续能耗仍需独立终端验证 |

## 4. 跨厂商微架构演进的关键差异

### 4.1 Apple：持续的自研核与系统垂直整合

AnandTech 的回顾把 Apple 的自研 CPU 微架构起点追溯到 A6/Swift（2012），并将 A7/Cyclone（2013）视为重要的宽执行、64 位转折。Cyclone 的第三方分析估计其 issue width 为 6、ROB 约 192 micro-ops；这些是逆向分析值，不是 Apple 官方披露。

历史解释：Apple 的核心设计、SoC、操作系统、编译器与设备发布链由同一公司统筹，减少跨组织接口协调的摩擦是合理推论；但“垂直整合导致多少性能/能效提升”仍需独立实验，不能仅凭产品表现断言。

### 4.2 Qualcomm：自研、半定制与再自研的切换

Krait 与首代 Kryo 体现完整自研核路线；Kryo 280 则是半定制 Cortex 核，不能沿用同一微架构假设。Qualcomm 的官方文章明确把移动性能/能效与多引擎异构协同联系起来；AnandTech 对 Kryo 280 的分析指出，Arm 半定制许可允许修改部分结构，但解码宽度和执行流水线等核心部分不在常规可修改范围内。

历史解释：选择全定制、半定制或现成 Cortex IP，可能随性能/能效目标、工程投入、授权模式、上市周期与商业策略变化。品牌名本身不足以推断具体微架构。

### 4.3 Samsung：自研 CPU 核是可选择、也可退出的路线

Samsung 官方 Exynos 990 规格确认两颗第五代自研 CPU 核，与两颗 Cortex-A76 和四颗 Cortex-A55 共存。ISCA 2020 工业论文对 M1–M5 的分支预测、微操作缓存、预取器和内存延迟优化提供了较少见的核内细节。Samsung 于 2019 年终止自研 CPU 项目。

历史解释：自研微架构有可能带来差异化，但要持续满足 IPC、能效、面积、验证和产品节奏等多重要求。公开证据不能将项目终止归因于某一个单独技术参数；论文也提醒 M5/M6 部分分析依赖周期精确模型而非芯片硅片测量。

### 4.4 HiSilicon：必须按代际区分 Cortex IP 与 Taishan 线索

Kirin 980 官方规格明确使用 Cortex-A76/A55，并以 2+2+4 的频率/调度组织进行产品差异化。Kirin 9000S/9010 的 Taishan 高性能核则主要来自第三方芯片照片、CPU ID 和基准分析；Huawei 没有公开足以重建完整微架构的官方手册。

历史解释：正确结论不是“华为一直使用 Cortex”或“华为一直自研 CPU”，而是不同代际的证据状态不同。Taishan 可以作为“第三方证据支持存在自研高性能核”的事实线索，但其 ROB、分支预测、执行端口和缓存结构仍是未知。

### 4.5 MediaTek：标准 Arm 核也能承载显著的 SoC 级架构选择

Dimensity 9300 用 Cortex-X4/A720 形成 4+4 全大核配置。Dimensity 9500 则采用 Arm C1-Ultra/Premium/Pro 和 SME2，并通过更大的缓存、4 通道 UFS 4.1 和第二代调度引擎构建产品差异。C1 核内微架构属于 Arm 的 CPU IP；MediaTek 的可见控制点更多在组合、频率、缓存/内存、调度、NPU/GPU 协同和系统实现。

历史解释：采用标准 CPU IP 并不等于“没有微架构价值”，但必须准确说清创新位于核内、集群、内存/互连还是 SoC/软件层。

## 5. 本轮可以确认的历史规律与边界

- **[OBSERVATION] 自研核不是单向演进：** Apple 持续自研；Qualcomm 在全自研与半定制之间切换后再引入 Oryon；Samsung 终止了 Mongoose；HiSilicon 的 Taishan 线索来自第三方逆向。
- **[OBSERVATION] “大核/小核”也不是固定组合：** 2+2+4、2+4、4×X4+4×A720、1+3+4 等组合随代际和厂商目标变化；核数不能独立说明能效或持续性能。
- **[OBSERVATION] IP 公布与手机落地应分开：** A76→Kirin 980→Mate 20、C1→Dimensity 9500→vivo X300，以及 C2→Dimensity 9600 Pro 的日期链提供了真实采用顺序。
- **[INFERENCE] 差异化控制点会随厂商能力改变：** 有些厂商将资源投入核内微架构，有些更集中于集群/调度、缓存/内存、ISP/NPU 与系统软件的联合设计。
- **[UNKNOWN] 不能仅靠公开跑分比较每个 CPU 核的真实微架构质量。** 缺少统一设备、同制程/频率、同编译器/软件、同功耗/热状态与独立测试时，不能用厂商跨代百分比得出普适排名。

## 6. 下一步

1. 将上述跨厂商路线写回主时间线，修正 Krait/Kryo/Oryon 的连续性、Samsung Mongoose 退出、HiSilicon Taishan 的证据等级，以及 C1/C2 的实际产品化节点。
2. 继续逐核补齐能公开确认的前端/分支、乱序窗口、执行端口、Load/Store、缓存/预取等具体机制；优先使用原始工程资料、架构论文与高质量逆向分析。
3. 建立一张“事实—厂商主张—第三方分析—推论—未知”的核内机制矩阵，避免把不同证据层级合并成结论。
