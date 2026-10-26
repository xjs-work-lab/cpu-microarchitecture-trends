# 第26轮来源卡｜Apple A8—A13（2014—2019）CPU代际演进与证据边界

**2026-10-26；研究目的：** 填补第25轮Cyclone(A7, 2013)→Firestorm(A14, 2020)之间的6代证据，解释真正发生的变化、设计者明确目的及合理机制。PUBLIC_ONLY；不执行真机/benchmark/仿真，且不把Apple官方产品发布当作隐藏核内参数的披露。

## 来源等级
- **OFFICIAL_PRODUCT**：Apple同期发布，仅证实核数/架构级能力/设计者宣传目标、特定性能声明，不自动证实ROB/端口/延迟。
- **REVERSE_TEST**：AnandTech同期逆向、低层微基准、推测和公开LLVM线索，注意各参数有不同实测/推导来源。
- **DIE_ANALYSIS**：TechInsights拆片分析核数、面积与布局；面积/位置并不能证明执行宽度或缓存访问延迟。
- **METHOD_LIMIT**：第三方设备SPEC、浏览器与功耗测试受工具链、频率、系统调度、制程和测量层影响；不能拼成跨代单结构因果收益。

## 2014 A8｜Typhoon / Enhanced Cyclone

| ID | 资料 | 可支撑的内容与限定 |
|---|---|---|
| AP26-01 | [Apple iPhone 6/A8产品公告，2014-09-09](https://www.apple.com/newsroom/2014/09/09Apple-Announces-iPhone-6-iPhone-6-Plus-The-Biggest-Advancements-in-iPhone-History/) | A8是第二代64位Apple芯片；Apple强调性能、持续表现与能效；**没有公开6-wide/ROB参数**。 |
| AP26-02 | [AnandTech，iPhone 6 Review：A8’s CPU: What Comes After Cyclone?，2014-09-30](https://www.anandtech.com/show/8554/the-iphone-6-review/3) | 当时称“Enhanced Cyclone”，认为对A7主要是温和微架构迭代；低层分析仍显示约6µops/cycle，整数/FP部分延迟改善；“192 ROB?”“16-cycle mispredict?”在原表打问号。**不可将疑问参数当成确认规格，也不应把早期文章的未知内部代号说成Apple官方名称**。 |

## 2015 A9｜Twister

| ID | 资料 | 可支撑的内容与限定 |
|---|---|---|
| AP26-03 | [Apple iPhone 6s/A9公告，2015-09-09](https://www.apple.com/newsroom/2015/09/09Apple-Introduces-iPhone-6s-iPhone-6s-Plus/) | 第三代64位A9；Apple将A9+iOS9软硬件联动与真实使用性能、常驻M9和低功耗应用并提；CPU“比A8快70%”是**厂商整代比较**。 |
| AP26-04 | [AnandTech，A9’s CPU: Twister，iPhone 6s评测，2015](https://www.anandtech.com/show/9686/the-apple-iphone-6s-and-iphone-6s-plus-review/4) | 对照A8/Twister，表中都是约6 µops issue与192 µops ROB（第三方估计），分支误预测惩罚由约16降到约9 cycles，FP32加法/乘法延迟分别4→3、5→4，L2 1→3 MB；这些是**作者同文对照测量/归纳**。原文强调Apple公开核内资料有限，不能将branch penalty降低全归结于某个未知预测器模块，更不能将整代70%宣传全部归因为该改善。 |

## 2016 A10｜Hurricane/Zephyr、异构核转折

| ID | 资料 | 可支撑的内容与限定 |
|---|---|---|
| AP26-05 | [Apple iPhone 7/A10 Fusion，2016-09-07](https://www.apple.com/newsroom/2016/09/apple-introduces-iphone-7-iphone-7-plus/) | 首次产品公开 **2 performance + 2 efficiency** CPU核；能效核“功耗仅为高性能核1/5”属Apple工作点比较而非所有负载的实测恒等式。公告未给内部ROB/LSQ参数。 |
| AP26-06 | [TechInsights iPhone 7 teardown，2016（随调查更新）](https://www.techinsights.com/blog/apple-iphone-7-teardown) | 芯片布局支持不同类型CPU块存在，拆解者与AnandTech团队修正了最初的小核位置推断；**拆片中物理相邻并非逻辑共享/调度/激活机制的直接证据**。 |
| AP26-07 | [Ars Technica iPhone 8评测：A10与A11调度差别，2017](https://arstechnica.com/gadgets/2017/09/iphone-8-and-8-plus-review-the-curious-case-of-the-time-traveling-phone/) | 作为后见第三方对照，报告A10同时只运行一个核群的观察、A11可六核并发；仍非Apple披露硬件限制的正式规格。 |

## 2017 A11｜Monsoon/Mistral，六核可协同

| ID | 资料 | 可支撑的内容与限定 |
|---|---|---|
| AP26-08 | [Apple iPhone 8/A11 Bionic发布，2017-09-12](https://www.apple.com/newsroom/2017/09/iphone-8-and-iphone-8-plus-a-new-generation-of-iphone/) | **2 performance + 4 efficiency**，Apple正式称第二代performance controller可同时利用全部六核；25%、70%、多线程70%等是Apple在自身定义基线下的**声明**，不可当作纯核数/核内收益。 |
| AP26-09 | [TechInsights iPhone 8 Plus拆片，2017](https://www.techinsights.com/blog/apple-iphone-8-plus-teardown) | 实际A11 SoC面积和CPU布局，可证实小核块增多、芯片同时引入Neural Engine；不可从die尺寸直接归因为某个核内机制能效。 |
| AP26-10 | [MacRumors针对泄露设备树的Monsoon/Mistral分析，2017](https://www.macrumors.com/2017/09/12/a11-architecture-heterogeneous-computing/) | 微架构代号来自设备树/第三方报道，不能说Apple2017官方发布已经公开全部小核L2/cluster细节。与AP26-08直接官方调度声明分别使用。 |

## 2018 A12｜Vortex/Tempest，宽大核与非平凡小核

| ID | 资料 | 可支撑的内容与限定 |
|---|---|---|
| AP26-11 | [Apple iPhone XS/A12，2018-09-12](https://www.apple.com/newsroom/2018/09/iphone-xs-and-iphone-xs-max-bring-the-best-and-biggest-displays-to-iphone/) | 7nm，2 performance+4 efficiency；Apple宣传大核快15%、小核节能50%，**两者没有给单结构归因**。 |
| AP26-12 | [AnandTech，A12 Tempest CPU与NN性能，2018-10-05](https://www.anandtech.com/show/13392/the-iphone-xs-xs-max-review-unveiling-the-silicon-secrets/5) | 原始低层测试报告Tempest为**3-wide OoO**，不同于典型当年的Cortex-A53/A55顺序小核；讨论大小核隔离与漏电、动态能效差异。这些属于研究者逆向和机制分析，Apple未公开其全部队列。 |
| AP26-13 | [AnandTech，A12 SPEC2006测评及编译条件，2018-10-05](https://www.anandtech.com/show/13392/the-iphone-xs-xs-max-review-unveiling-the-silicon-secrets/4) | 作者用Xcode10、-Ofast测评，结果是**估计，不是SPEC官方验证成绩**；429.mcf数据集因iOS内存分配条件而做缩放修正，作者估±5%；部分store/cross-cache-line表现和内存系统变化显著，但不可据此识别未披露的ROB/预测器表。 |
| AP26-14 | [AnandTech A13后续反向核内表述，2019](https://www.anandtech.com/show/14892/the-apple-iphone-11-pro-and-max-review/2) | Lightning大核的约7-wide decode沿袭Vortex；即**A12 Vortex 7-wide**来自后续同一研究团队的技术描述。A13报告同时指A12/Vortex有128KB L1 I/D、8MB共享L2；精确SoC级地址行为仍属于逆向/拆片推断。 |

## 2019 A13｜Lightning/Thunder，能效核、SLC与调度的交叉变化

| ID | 资料 | 可支撑的内容与限定 |
|---|---|---|
| AP26-15 | [Apple iPhone 11/A13，2019-09-10](https://www.apple.com/uk/newsroom/2019/09/apple-introduces-dual-camera-iphone-11/) | A13/iOS13、机器学习加速器、性能和能效协同是官方**产品/目标**事实；20% CPU速度为厂商整代对照，不证明单CPU核增益。 |
| AP26-16 | [AnandTech，A13 Lightning & Thunder芯片和执行资源，2019](https://www.anandtech.com/show/14892/the-apple-iphone-11-pro-and-max-review/2) | A13大核沿用约7-wide decode/6整数ALU/3 FP向量执行路径，整数乘除 latency/throughput有改良；Thunder较Tempest FP/SIMD路径大幅加强，L1D 32→48KB。该团队根据芯片观察推断小核L2约4MB、A13 system-level cache约16MB（A12约8MB），须标**REVERSE/DIE_ESTIMATE**；不能混称CPU专属L3。 |
| AP26-17 | [AnandTech，A13 system & ML performance、OS/DVFS观察，2019](https://www.anandtech.com/show/14892/the-apple-iphone-11-pro-and-max-review/5) | 第三方观察特定负载下小核→大核迁移时间约A12 54ms、A13 30ms，且A13小核不能独立提升某些内存控制器performance states，可能造成孤立小核内存负载反而下降；作者将原因关联iOS13调度策略和内存DVFS，是**测量＋作者解释**。**数字不是iOS所有任务的固定迁移阈值**。 |
| AP26-18 | [Apple Developer：Optimize for Apple Silicon with performance and efficiency cores，2020-06-22](https://developer.apple.com/news/?id=vk3m204o) | 官方明确提到A13及P/E，软件提供QoS/工作负载语义可辅助OS做调度决策；文章也涉及Apple Silicon Mac，**不能将Mac系统所有细节倒推为2019 iPhone实现**。 |

## 四条证据治理规则

1. 日期分别标CPU研发未知、Apple公开SoC公告和第三方文章日期；不创造每代核心首次内部流片/首发日期。
2. **名词规范**：A8早期文称“Enhanced Cyclone”，后称Typhoon；Hurricane/Zephyr、Monsoon/Mistral、Vortex/Tempest、Lightning/Thunder为外部技术材料常用代号，Apple同期新闻稿未披露完整芯内结构。
3. **可比性**：A8“ROB 192?”不能和A9“ROB 192”都当做官方测量；Firestorm 623 rename-retire≠传统ROB；Apple对Apple实机SPEC、Samsung 2.6GHz模拟、Arm官方产品宣称不能连为同一数据曲线。
4. **链条强度**：2014–2019已对每代建立至少一个产品来源/逆向来源，覆盖≠完整设计者动机和因果归因；没有可复现本地实验和相同条件能耗拆解。
