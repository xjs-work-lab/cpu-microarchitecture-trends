# 第五轮：智能手机 SoC 整体微架构的演进主线

资料截点：2026-10-20。研究模式：PUBLIC_ONLY。此文纠正前四轮过度聚焦 CPU/GPU/NPU 的范围偏差。产品的官方结构披露是架构证据；收益百分比属于厂商主张，除非另有同口径独立测量。公开资料未披露的缓存拓扑、片上网络、功耗策略，记录为未知。

## 核心回答（当前版本）

**[INFERENCE]** 手机 SoC 的长期变化不是把 CPU、GPU、NPU 分别做大，而是不断调整**功能分工、数据路径与电热预算**：从集成连接和多媒体，到异构计算与低功耗常驻岛，再到 ISP/DSP/NPU 协同处理实时感知，近年进一步优化共享缓存、低精度数据、跨引擎执行和持续散热。不同阶段的“最佳”配置并不固定。2012 年的集成 LTE 基带与 2019 年 Snapdragon 865 的外置 5G Modem-RF 系统并存，提醒我们集成度取决于制程、面积、无线复杂度及产品策略，而非必然单向增加。[E02][E05]

## SoC 观察边界

```text
工作负载：网络 / 交互 / 相机视频 / 游戏 / 端侧 AI
        ↓
计算与专用引擎：CPU | GPU | DSP/低功耗岛 | NPU | ISP | 视频/显示
        ↕ 数据路径：片上缓存/SLC | 互连/QoS | DRAM | 存储
        ↕ 控制路径：OS/驱动/编译器/运行时 | 电源域/DVFS | 安全隔离
        ↕ 系统边界：基带/Modem-RF | Wi-Fi/GNSS | 封装/供电/散热
```

**边界说明：**图中列的是需要一起评估的手机计算系统，并不声称全部模块在同一裸片上。RF 前端、DRAM、外置调制解调器、均热板等应按具体产品标注物理位置。[E02][E05][E11]

## 五个阶段：问题推动结构变化

| 阶段 | 阶段性问题 | 观察到的架构响应 | 新代价 / 未解决问题 | 原始证据 |
| --- | --- | --- | --- | --- |
| **2007—2012：集成移动计算平台** | 智能手机同时要求蜂窝连接、网页/媒体、图形与续航；早期 LTE 增加板级芯片和功耗压力 | Snapdragon 早期平台把 CPU/GPU/DSP/ISP/通信纳入同一移动平台；2012 年 MSM8960 将 LTE 基带与应用处理器集成，配合 28nm 和接收机休眠技术 | 芯片面积、无线规格迭代与制程选择相互牵制；不能把续航改善单独归因于基带集成 | [E01][E02] |
| **2013—2016：异构计算与专用流水线** | 交互峰值、待机、低照度摄影、持续感知所需的最优能耗工作点不同 | big.LITTLE/HMP 使不同 CPU 核与调度协同；Snapdragon 820 将 Kryo/Adreno/Hexagon/Spectra ISP 组合，DSP 的 HVX、Sensor Core 低功耗岛与 SoC 级管理分别处理视觉、常驻和电源选择 | 多引擎调度、数据拷贝、驱动与软件适配变复杂；厂商举例的省电倍数非架构单项对照 | [E03][E04] 与第二轮 [R05–R07] |
| **2017—2020：实时 AI、视觉与 5G** | 人脸/摄影/翻译等模型需实时执行；5G 提升链路能力又带来面积和电热成本 | Apple A11 Neural Engine、华为 Kirin 970 NPU 展示专用神经单元；Qualcomm 从 DSP 加张量单元与共享存储；Snapdragon 865 用 X55 Modem-RF **系统**而非单裸片集成例子 | 模型算子覆盖与软件 fallback 限制 NPU 收益；5G 架构不能简化为“集成越多越好” | 第一、二轮 [S05][S06][T01]；[E05] |
| **2021—2024：异构融合与生成式 AI** | 计算摄影、视频、语音跨单元，端侧生成式模型把内存容量/带宽与能效推到前台；GPU 图形复杂度上升 | Google Tensor 公开 TPU、ISP、CPU/GPU 与 System Cache 的协同；Samsung/Arm/Apple 引入移动硬件光追；MediaTek 9300 APU 对 Transformer、INT4 与内存压缩优化；Qualcomm 8 Elite 用共享缓存、分片 GPU、Hexagon Direct Link/ISP 协同 | 需求从单引擎峰值转向任务级延迟、数据搬运、持续负载；不少性能数字同时包含工艺和软件升级 | [E06][E07]、第四轮 [T02–T04]、第一轮 [S07][S09][S10] |
| **2025—2026：系统资源成为主约束** | 本地长上下文/常驻感知、复杂图形与长时游戏同时竞争缓存、内存、功耗和热预算 | MediaTek 9500 披露 CPU/GPU/NPU 动态共享数据缓存、SLC 管理、UFS 读写和 NPU 辅助 ISP；Qualcomm 8 Elite Gen 5 披露 HPM、Tile Memory Heap、Hexagon Direct Link、微型 NPU/常驻 ISP、CPU 矩阵加速与 Modem-RF；Arm 2026 CSS for Mobile 2 将 CPU SME2、GPU 神经加速、系统 IP 和软件一起发布；Apple A20 Pro 同时提高内存带宽并调整封装和散热路径 | 共享资源要处理争用/QoS；低精度需保持质量；常驻功能要受隐私和静态功耗约束；热设计属手机系统，不能全算作裸片微架构 | [E08–E11] |

**[OBSERVATION]** 五阶段中的转折来自公开产品和 IP 的代表节点，不表示所有厂商同年转换，也不表示旧结构消失。例如全大核与效率核路线并存，独立 NPU 与 CPU/GPU 内部矩阵/神经能力并存，基带集成与独立方案均有公开先例。[E02][E05][E09][E10]

## 阶段问题如何具体改变微架构

1. **连接与续航：**LTE 初期，减少基带/AP 芯片间边界有系统集成收益的可能；但制程改进和无线接收机休眠同时变化，因果无法用一款手机的续航拆分。[E02] 5G 时期出现外置 Modem-RF 方案，说明射频复杂度和产品取舍会重画边界。[E05]
2. **影像与常驻感知：**图像输入有固定速率和处理期限，ISP 保留专用像素流水线，DSP/HVX 承担可编程视觉，低功耗岛处理常驻传感；2015 年的原始资料已经把这些模块与 SoC 级功耗管理一起描述。[E03][E04]
3. **推理与数据移动：**NPU/TPU 因模型任务增设，但 2025 年的公开方案又加强 CPU 矩阵、GPU 神经处理、共享缓存和内存管理。说明问题从“是否有 AI 单元”移到“模型哪个阶段在哪执行、搬运多少数据、如何保持带宽与质量”。这是跨资料归纳，不是已测得最优调度法。[E08][E09][E10]
4. **持续图形与热：**光追和神经图形增加单帧计算与带宽，缓存和 tile 机制减少访存；Apple 2026 年公开说明内存封装位置与均热路径改变持续性能。芯片与整机热结构共同决定用户可见结果。[E09–E11]
5. **安全与隐私：**长期上下文、常驻感知增加敏感数据在 SoC 各单元间流动，2025 年 Qualcomm 产品资料披露模型加密、SPU/TEE/隔离等能力；目前缺公开证据证明不同实现的安全强弱。[E09]

## 2027—2028：有条件的演进判断

| 判断与置信度 | 2025—2026 已公开的前置信号 | 可能继续解决的瓶颈 | 替代路线 / 证伪条件 |
| --- | --- | --- | --- |
| **[HYPOTHESIS] 跨引擎缓存、互连和任务放置继续优化；中高置信度方向，低置信度收益幅度** | MediaTek 的动态共享 CPU/GPU/NPU 缓存、Arm 系统 IP、Qualcomm Direct Link/HPM 已公布 [E08–E10] | 多模态流水线、GPU/AI 并行时的数据搬运、DRAM 能耗和争用 | 更大 DRAM 带宽或软件融合也可能足够；若独立任务实测无设备级时延/能耗收益，应下调判断 |
| **[HYPOTHESIS] AI 运算进一步分布到 CPU/GPU/NPU/常驻岛；高置信度方向，具体分工待证** | CPU SME2/矩阵能力、GPU Neural Accelerators、微型 NPU/常驻 ISP 同时出现 [E09–E11] | 低延迟小模型、图形中的神经计算、常驻感知与大模型有不同功耗工作点 | 如果模型主要由单 NPU 更高效执行，或软件接口阻碍其他单元采用，实际分布可能收窄 |
| **[HYPOTHESIS] 模型内存/加载与持续散热成为下一代系统设计重点；中高置信度方向** | MediaTek 披露缓存/UFS/低比特/CIM；Apple 调整内存带宽与封装散热；Qualcomm 增 GPU 专用缓存 [E08][E09][E11] | 长上下文、常驻模型、复杂游戏同时要求容量、带宽和持续功率 | 模型压缩、云侧卸载、应用取舍可能削弱本地资源需求；需看真实应用的质量、时延、能耗 |
| **[HYPOTHESIS] ISP/感知/连接侧继续局部 AI 化；中等置信度** | 2025 年产品已公开 NPU 辅助 ISP、常驻 ISP 和 Modem-RF AI 处理 [E08][E09] | 实时多摄、个性化感知、无线网络状态估计 | 隐私、耗电和软件采用可能压低常驻范围；不能把营销中的“agentic”视作用户需求已验证 |

**不作预测：**某厂商 2027/2028 年具体 SoC 的核心数、制程、TOPS、上市时间、架构赢家。Arm 2026 年发布的是平台/IP 方向，不自动证明其会进入所有 2027 年手机。[E10] TSMC 的公开工艺路线说明工艺可用性，不能代替手机 SoC 微架构路线。[E12]

## 本轮目标审计

| 用户当前问题 | 是否已回答 | 证据边界与下一步 |
| --- | --- | --- |
| 整个 SoC 的历史架构如何演进？ | **已有有边界的阶段性答案** | 五阶段覆盖计算、ISP/媒体、通信、感知、缓存互连、电热/安全；早期不同厂商覆盖还不均衡 |
| 每次变化解决什么阶段问题？ | **已有主要因果机制假设** | 连接、影像、实时 AI、生成式 AI/持续性能的瓶颈和机制可讲；收益量化不能纯归因于架构 |
| 未来一两年可能怎样演进？ | **已有四条有条件方向** | 前置信号来自 2025—2026 产品/IP，实际终端普及及任务收益待核对 |
| 是否仍围绕整个 SoC，而非仅 CPU/GPU/NPU？ | **本轮已纠偏** | 下一轮继续补视频/显示、调制解调器与安全的代表代际，并对每阶段找一例替代路线或反证 |

本轮结论状态：**REFRAME / UPGRADE**。将前四轮 CPU/GPU/NPU 证据保留为全 SoC 的子线，不把其原始六问继续作为唯一目标。下一轮最小公开取证是建立 6—8 个代表 SoC 的“物理边界—数据路径—电源域—软件路径”对照卡，再针对两条最重要的跨代机制查原始技术材料；独立基准作为检验任务结果的一层，而非替代整体架构研究。

## 本轮新增原始来源

| ID | 资料与定位 | 原始 URL | 证明范围/限制 |
| --- | --- | --- | --- |
| E01 | Qualcomm，Snapdragon 十年回顾，2017 | https://www.qualcomm.com/news/onq/2017/11/celebrating-10-years-innovation-snapdragon | 厂商回顾早期平台组件和工艺；非逐代版图证据 |
| E02 | Qualcomm，Snapdragon S4 集成 LTE，2012-06 | https://www.qualcomm.com/news/onq/2012/06/what-integrating-4g-lte-modem-means-snapdragon-s4-processor-and-battery-life | MSM8960 集成基带/AP；同文提工艺/CDRX，不能单因素归因 |
| E03 | Qualcomm，Snapdragon 820/Hexagon 680，2015-08 | https://www.qualcomm.com/news/onq/2015/08/snapdragon-820-countdown-new-hexagon-680-dsp | HVX、Sensor Core 低功耗岛、ISP 协作，收益为厂商宣称 |
| E04 | Qualcomm，820 Kryo 与异构系统管理，2015-09 | https://www.qualcomm.com/news/onq/2015/09/snapdragon-820-and-kryo-cpu-heterogeneous-computing-and-role-custom-compute | CPU/GPU/DSP/ISP/内存/显示/GPS 的系统级管理描述 |
| E05 | Qualcomm，Snapdragon 865 与 X55 Modem-RF，2019-12；同期官方演示材料 | https://www.qualcomm.com/news/releases/2019/12/qualcomm-introduces-worlds-most-advanced-5g-mobile-platform ; https://www.qualcomm.com/media/documents/files/2019-snapdragon-tech-summit-2019-keynote-alex-katouzian.pdf | 产品搭配 X55 Modem-RF 系统；演示材料分列 865 AP 与 X55 Modem Module，不代表所有厂商采用相同板级布局 |
| E06 | Google，Tensor，2021-10 | https://blog.google/products-and-platforms/devices/pixel/introducing-google-tensor/ | TPU/ISP/CPU/GPU/System Cache 与负载协同；厂商功耗对比非独立测量 |
| E07 | MediaTek，Dimensity 9300，2023-11 | https://www.mediatek.com/press-room/mediateks-new-all-big-core-design-for-flagship-dimensity-9300-chipset-maximizes-smartphone-performance-and-efficiency?hs_amp=true | CPU 全大核、APU 790 低精度/压缩/Transformer；不可推普遍优势 |
| E08 | MediaTek，Dimensity 9500 产品页及发布，2025-09 | https://www.mediatek.com/products/smartphones/mediatek-dimensity-9500 ; https://www.mediatek.com/press-room/mediatek-dimensity-9500-unleashes-best-in-class-performance-ai-experiences-and-power-efficiency-for-the-next-generation-of-mobile-devices?hs_amp=true | 动态共享缓存、SLC、UFS、ISP/NPU、CIM 等厂商披露；细部拓扑和收益待验证 |
| E09 | Qualcomm，Snapdragon 8 Elite Gen 5 产品简报，2025 | https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/Snapdragon-8-Elite-Gen-5-product-brief.pdf | 第 2–3 页：缓存、NPU/常驻、ISP、Modem-RF、安全、内存；官方功能和主张 |
| E10 | Arm，CSS for Mobile 2，2026-09 | https://newsroom.arm.com/news/arm-css-for-mobile-2-agentic-ai-mobile-graphics | IP/平台发布，含 C2/SME2、GPU 神经加速、系统 IP/软件；不等于所有手机已采用 |
| E11 | Apple，A20 Pro / iPhone 18 Pro，2026-09 | https://www.apple.com/newsroom/2026/09/apple-debuts-iphone-18-pro-and-iphone-18-pro-max/ | CPU/GPU/Neural Engine、带宽、封装和整机散热；性能数字为厂商主张 |
| E12 | TSMC，2026 AGM 议程，技术路线段 | https://investor.tsmc.com/sites/ir/shareholders-meeting/2026-06-04/2026AGM_Agenda_wmn_0.pdf | N2P/A16 2026 下半年量产计划、A14 2028 计划；工艺路线不等于手机产品计划 |
