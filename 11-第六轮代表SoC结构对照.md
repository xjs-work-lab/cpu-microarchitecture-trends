# 第六轮：八个代表平台的全 SoC 结构对照

资料截点：2026-10-20；研究模式 PUBLIC_ONLY。选择 8 个节点是为展示不同阶段的**问题与结构取舍**，并非销量或性能排名。表中“未披露”表示所列原始资料不足，不表示该功能不存在。厂商宣传的速度/省电数字不用于横向排序。物理边界区分芯片、配套芯片、手机终端；不把手机功能一概写成 SoC 裸片功能。

## 1. 代表节点及其阶段性问题

| 节点 | 当时聚焦的问题 | 计算、感知、影像/视频/显示 | 通信、安全、数据与功耗 | 结构意义及限制 |
| --- | --- | --- | --- | --- |
| **Snapdragon S4 MSM8960（2011 年白皮书、2012 年产品）** | LTE 连接、应用性能和续航同时提升 | Krait CPU、Adreno GPU、Hexagon DSP、音视频加速器；异步 SMP，每核心独立时钟/电压 | LTE 多模基带与 AP 集成；System Fabric、L2、双通道内存和自适应供电；安全细节在所查白皮书中未充分披露 | 展示**通信与应用处理集成**、系统互连和细粒度功耗控制的早期组合；28nm 同时变化，不能单独量化集成收益。[P01][P02] |
| **Apple A7 / iPhone 5s（2013）** | 交互/图形升级、持续运动感知、指纹支付安全、摄影响应 | A7 64 位 CPU、GPU、片内 ISP；手机另有 M7 运动协处理器，负责休眠时的持续运动测量 | A7 内 Secure Enclave 存储指纹资料；手机支持 LTE；基带物理位置、内存互连在发布稿中未披露 | 展示**常驻感知卸载＋独立安全域**和 ISP/软件共同升级。M7 属手机系统，不据发布稿称其在 A7 裸片上。[P03] |
| **Snapdragon 820（2015–2016）** | 低照度视频、计算视觉、常驻传感与多媒体吞吐 | Kryo CPU、Adreno GPU、Hexagon 680 HVX、Sensor Core 低功耗岛、双 Spectra ISP；4K HEVC 编解码、显示帧缓冲压缩 | 集成 X12 LTE；LPDDR4/UFS 2.0、带宽压缩；SecureMSM 等安全能力；Symphony 管理 CPU/GPU/DSP/ISP/显示/GPS/内存活动 | **固定功能 ISP/编解码＋可编程 DSP＋低功耗感知岛**成为系统级分工。官方产品简报和系统管理说明未给内部互连拓扑或因果收益拆分。[P04][P05] |
| **Snapdragon 865 / X55（2019–2020）** | 5G 多频段、图像/视频和 AI 能力并进 | Kryo/Adreno/Hexagon 张量单元、Sensing Hub、Spectra 480 ISP；所查发布材料披露 ISP 吞吐 | 865 移动平台搭配 X55 Modem-RF；官方演示把 865 AP 与 X55 Modem Module 分列；RF 前端属更大的系统 | **平台集成不等于单裸片集成**。与 S4 构成通信物理边界的反例；不能从两代产品推断分拆原因或普遍能耗优劣。[P06][P07] |
| **Google Tensor / Pixel 6（2021）** | 长时语音、翻译、影像与视频 ML，要求跨处理器协同 | 官方结构图列 TPU、ISP、CPU、GPU、Content Hub 和 System Cache；把 HDRNet 部分直接放进芯片以支持 4K60 视频；TPU 参与音视频语音隔离 | Tensor security core 在 SoC 内；Titan M2 是配套安全芯片；发布材料未给互连和逐任务带宽数据 | **面向明确工作负载的跨引擎协同**，同时保留手机级独立安全芯片。功能存在和厂商功耗比较不等于各引擎时间/能量占比。[P08][P09] |
| **Samsung Exynos 2200（2022）** | 手机游戏光追、多摄/高像素、8K 视频、5G 和密钥保护 | Xclipse RDNA2 GPU、NPU/DSP、支持多摄的 ISP；独立 MFC 视频编解码支持 8K 和 AV1 解码；显示支持 HDR10+ 和高刷新 | 集成 5G 基带；嵌入式 Secure Element 作信任根，UFS/DRAM 在线加密；AMIGO 跨 IP 功耗控制 | **图形、影像、编解码、通信、安全一起升级**，与 865 的通信边界不同。光追、8K、AV1 支持不保证具体手机长期使用体验。[P10] |
| **MediaTek Dimensity 9500（2025）** | 本地模型加载、计算/图形/AI 争用带宽，长时间游戏及多模态拍摄 | 全大核 CPU、Mali G1-Ultra、NPU 990＋Super Efficient NPU；Imagiq ISP 与 NPU 协同对焦；显示自适应处理 | 动态共享 CPU/GPU/NPU 数据缓存与 SLC 管理；四通道 UFS 4.1 方案、5G 节能与网络智能；公开页面未给可核查的安全域拓扑 | 设计重心移到**共享数据和任务调度**；“CIM”等术语为厂商结构披露，未有公开同口径芯片能耗分解。[P11][P12] |
| **Apple A20 Pro / iPhone 18 Pro（2026）** | 本地 AI、游戏与视频竞争带宽及持续热预算 | CPU 内 Neural Accelerators、GPU、双 16 核 Neural Engine；产品说明强调多引擎服务本地模型 | A20 Pro 公开提高内存带宽；封装把内存移出芯片热路径，芯片直接连接新均热板。手机另有 N1 无线芯片与 C2 蜂窝系统；不据此断言 C2 在 A20 Pro 裸片内 | **裸片计算＋封装/内存＋终端散热共同设计**。厂商持续性能百分比不能单独归因于微架构。[P13] |

## 2. 五条跨代机制链与反例

| 阶段问题 → 机制 | 已有证据支持的变化 | 最强反例/替代解释 | 当前判断 |
| --- | --- | --- | --- |
| **蜂窝连接增加 → 重新划分通信物理边界** | S4/MSM8960 集成 LTE；865/AP 搭配 X55 Modem-RF；Exynos 2200 又集成 5G 基带。[P01][P02][P06][P07][P10] | 具体选择可能由制程、RF 全球频段、研发时间、面积、OEM 策略共同决定；原始资料没有同条件 A/B 对照 | **[OBSERVATION]** 集成度非单调趋势；“物理位置”必须逐产品核对。原因仍属**[HYPOTHESIS]**。 |
| **常驻感知耗电 → 卸载到低功耗执行域** | iPhone 5s 的 M7 在休眠时测运动；820 的 Sensor Core 低功耗岛；后续 Sensing Hub/微型 NPU 扩到语音与摄像。[P03][P04][E09] | M7 是手机中的协处理器，820 是 SoC 内低功耗岛；不能视作同一物理实现；常驻传感的用户需求和隐私约束也会变 | **[OBSERVATION]** 低功耗常驻路径跨代延续，**物理实现分化**。 |
| **实时影像/视频 → 固定流水线与可编程引擎融合** | 820 ISP＋HVX；Tensor ISP 内实现实时 HDRNet；Exynos 2200 ISP＋NPU、多格式编解码。[P04][P08–P10] | 传感器、镜头、算法、软件和视频编码格式同时变化；不能把图像质量全归于 ISP 结构 | **[OBSERVATION]** 像素流水线与 ML/可编程处理的协同不断加深；任务收益需端到端验证。 |
| **显示/游戏复杂度提高 → 压缩、缓存与专用图形能力** | 820 帧缓冲/带宽压缩；Exynos 2200 光追和高刷/HDR；9500 动态缓存，Qualcomm 2025 HPM/Tile Memory Heap。[P04][P10][P11][E09] | 高刷、光追是负载和能力，不代表所有游戏都用；终端分辨率/散热/驱动会改变持续帧率 | **[OBSERVATION]** 视频/显示和 GPU 的带宽预算是全 SoC 问题；性能胜负尚未证明。 |
| **敏感数据与本地 AI 增加 → 多安全域与数据保护** | A7 Secure Enclave、Tensor security core＋Titan M2、Exynos embedded SE＋内存/存储在线加密、Qualcomm 2025 模型加密/TEE/SPU。[P03][P08][P10][E09] | 名称相似的安全模块不代表同级威胁模型；公开资料没有跨厂商攻击面、性能和安全证明 | **[OBSERVATION]** 安全从附属功能进入 SoC 结构与数据路径；不能给安全强弱排名。 |

## 3. 对 2027—2028 判断的更新

1. **[HYPOTHESIS，方向可信度较高]** 更多任务将在大小不同的计算域和常驻岛之间分配。理由是 M7/Sensor Core/Sensing Hub 到微型 NPU 的连续需求链，以及 CPU/GPU/NPU 的并行 AI 能力。**边界：**具体分区和常驻时间受软件、安全和静态功耗约束。[P03][P04][E09][E10]
2. **[HYPOTHESIS，方向可信度较高]** 内存和片上数据治理会继续决定本地 AI 与图形的可用性能。820 的压缩、2025 年的共享 SLC 与专用 GPU 缓存、2026 年的内存带宽/封装均指向不同层次的访存瓶颈。**反证：**若未来真实任务的主瓶颈仍由算力、软件或网络主导，应下调“内存为首要约束”的普遍性。[P04][P11][P13][E09]
3. **[HYPOTHESIS，中等可信度]** ISP/编解码、图形与神经计算的数据接口将继续融合，以降低实时多摄、视频和神经图形的中间数据搬运。**替代路线：**更高带宽、算法简化或云端处理也可满足一部分场景；现有公开文档尚不足以预测具体片上拓扑。[P09–P11][E10]
4. **维持边界：**不预测基带一定重新集成或一定外置；S4、865、Exynos 2200 已直接构成相反产品选择。[P01][P07][P10]

## 4. 本轮目标审计与下一步

| 用户核心问题 | 本轮能回答的部分 | 尚缺证据 |
| --- | --- | --- |
| **整个 SoC 历史怎样演进？** | 八个节点把 CPU/GPU/NPU 之外的 ISP、编解码/显示、基带、安全、缓存、低功耗域和封装连入一条时间线 | 2007—2010 年原始结构文档稀少；尚未覆盖中低端设计及所有厂商 |
| **哪些阶段问题推动变化？** | 连接续航、常驻感知、影像视频、游戏显示、本地 AI/安全分别对应可追溯的结构响应 | 多数收益无法在工艺/频率/软件/终端条件间因果拆分 |
| **未来一两年如何演进？** | 四条方向与反例均建立在已发布结构上，明确避免把 2027/2028 产品当已知事实 | 缺真实任务在共享缓存、低功耗岛和跨引擎数据路径上的能耗/延迟测量 |
| **是否走偏？** | **否。** CPU/GPU/NPU 被放回 SoC 多模块对照的一部分，通信、影像视频、显示、安全、电热均有独立栏目 | 下一轮应深挖数据路径和功耗管理，而非回到单引擎规格排名 |

本轮状态：**UPGRADE**。下一步在公开资料范围内选取相机视频与端侧 AI 两个完整工作负载，画出传感器/输入→ISP/DSP/NPU/GPU/CPU→内存→视频/显示/存储/网络的数据流和功耗域；逐段标注有原始证据、厂商主张和未知。用此检验“共享缓存/跨引擎路径是否真正是下阶段瓶颈”。

## 原始来源

| ID | 原始来源 | URL | 取证范围 |
| --- | --- | --- | --- |
| P01 | Qualcomm，Snapdragon S4 白皮书，2011-10，图 1 和第 2–3 页 | https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/QU_SnapdragonS4_White_Paper_FNL_Rev6.pdf | MSM8960 功能块、System Fabric、双通道内存、aSMP；厂商资料，原图不复制 |
| P02 | Qualcomm，S4/LTE 集成解释，2012-06 | https://www.qualcomm.com/news/onq/2012/06/what-integrating-4g-lte-modem-means-snapdragon-s4-processor-and-battery-life | AP/基带集成，以及 28nm/CDRX 等并行变化 |
| P03 | Apple，iPhone 5s/A7/M7/Secure Enclave，2013-09 | https://www.apple.com/newsroom/2013/09/10Apple-Announces-iPhone-5s-The-Most-Forward-Thinking-Smartphone-in-the-World/ | SoC 与手机系统的边界、ISP、运动/安全卸载 |
| P04 | Qualcomm，Snapdragon 820 产品简报，2015–2016，第 2 页 | https://www.qualcomm.com/content/dam/qcomm-martech/dm-assets/documents/snapdragon_product_brief_820_update062416.pdf | 计算、ISP、视频显示、LTE、LPDDR4/UFS、压缩、安全 |
| P05 | Qualcomm，Snapdragon 820 异构计算与 Symphony，2015-09 | https://www.qualcomm.com/news/onq/2015/09/snapdragon-820-and-kryo-cpu-heterogeneous-computing-and-role-custom-compute | 跨引擎系统管理厂商描述 |
| P06 | Qualcomm，Snapdragon 865 平台发布，2019-12 | https://www.qualcomm.com/news/releases/2019/12/qualcomm-introduces-worlds-most-advanced-5g-mobile-platform | X55 Modem-RF、ISP、AI/感知平台功能 |
| P07 | Qualcomm，Snapdragon Summit 官方演示，2019，865 AP / X55 Modem Module 页 | https://www.qualcomm.com/media/documents/files/2019-snapdragon-tech-summit-2019-keynote-alex-katouzian.pdf | 物理边界；不推断拆分原因 |
| P08 | Google，Google Tensor 技术说明，2021-10 | https://blog.google/products-and-platforms/devices/pixel/introducing-google-tensor/ | SoC 模块、跨引擎任务、Tensor security core/Titan M2 边界 |
| P09 | Google，Pixel 6 Camera 技术说明，2021-10 | https://blog.google/products-and-platforms/devices/pixel/pixel-6s-camera-combines-hardware-software-and-ml/ | ISP 内 Live HDR+、4K60、TPU 参与音视频处理 |
| P10 | Samsung Semiconductor，Exynos 2200 产品技术页 | https://semiconductor.samsung.com/processor/mobile-processor/exynos-2200/ | CPU/GPU/NPU、集成基带、ISP/MFC/显示、AMIGO、eSE、在线加密 |
| P11 | MediaTek，Dimensity 9500 产品页 | https://www.mediatek.com/products/smartphones/mediatek-dimensity-9500 | 动态共享缓存/SLC、NPU/ISP/GPU、连接和显示 |
| P12 | MediaTek，Dimensity 9500 发布，2025-09 | https://www.mediatek.com/press-room/mediatek-dimensity-9500-unleashes-best-in-class-performance-ai-experiences-and-power-efficiency-for-the-next-generation-of-mobile-devices?hs_amp=true | 存储、调度、Super Efficient NPU、MiraVision 和连接；收益为厂商主张 |
| P13 | Apple，iPhone 18 Pro/A20 Pro，2026-09 | https://www.apple.com/newsroom/2026/09/apple-debuts-iphone-18-pro-and-iphone-18-pro-max/ | CPU/GPU/Neural Engine、内存带宽、封装/热、N1/C2 手机系统 |

`E09/E10` 来源见[第五轮主线](10-第五轮整体SoC演进主线.md)。
