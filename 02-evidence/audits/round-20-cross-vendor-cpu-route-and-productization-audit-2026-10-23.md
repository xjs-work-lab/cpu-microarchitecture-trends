# 第二十轮：跨厂商 CPU 路线与产品化时间审计（2026-10-23）

**状态：** CROSS_VENDOR_ROUTE_AUDIT / PUBLIC_ONLY / PARTIALLY_VERIFIED  
**对应分析：** [移动 CPU 跨厂商微架构路线与产品化时间 v0.2](../../03-analysis/移动CPU跨厂商微架构路线与产品化时间-v0.2-2026-10-23.md)  
**来源卡：** [第二十轮跨厂商路线与产品化来源卡](../sources/round-20-移动CPU跨厂商路线与产品化来源卡.md)

## 1. 本轮问题

- 不同厂商所称的 custom CPU / custom core 是否指同一种技术控制权？
- 从 CPU IP/微架构公布到 SoC、手机产品发布和零售上市分别发生在何时？
- 哪些路线变更有直接证据，哪些只能视为第三方识别或分析推论？

## 2. 关键核验结果

| 主张 | 审计结论 | 证据层级与边界 |
|---|---|---|
| Qualcomm 的 Krait、Kryo、Kryo 280 与 Oryon 是一条连续、固定的自研微架构 | **不成立，需改写** | 官方资料将 Krait 和首代 Kryo 描述为自研 CPU；AnandTech 指出 Kryo 280 使用 Arm “Built on Cortex” 半定制许可。Oryon 是 2024 年进入 Snapdragon 手机平台的新一代自研 CPU。品牌名称不能代表固定的设计路线。 |
| 所有手机 CPU 差异化都来自核内自研 | **不成立** | Kirin 980 采用 Arm Cortex-A76/A55，但有 2+2+4 flex-scheduling 配置；Dimensity 9300 采用 Cortex-X4/A720 的全大核组合；Dimensity 9500 使用 Arm C1 核与 SME2。集群、频率、缓存/内存、调度与 SoC 协同也是重要设计层。 |
| Samsung 自研核项目一直延续至今 | **不成立** | Exynos 990 包含第五代自研 CPU 核；Samsung 于 2019 年宣布终止自研 CPU 核开发项目。ISCA 工业论文为 M1–M5 的微架构演进提供细节，但部分 M5/M6 分析来自周期精确模型，不能误作硅片测量。 |
| Huawei/Kirin 全部使用标准 Cortex CPU | **证据不足且可能错误** | Kirin 980 官方资料明确使用 Cortex-A76/A55；Kirin 9000S/9010 的 Taishan 核由第三方芯片/CPU ID 分析识别，但缺乏完整官方微架构文档。应保留代际差异与来源边界。 |
| Dimensity 9300 的全大核证明行业不再需要能效核 | **不成立** | 9300 是采用 Arm Cortex-X4/A720 的特定产品配置；Apple 及其他厂商仍保留异构核路线。单一产品无法证明行业收敛。 |
| Arm C1/C2 只停留在 IP 发布阶段 | **已被产品化证据修正** | Arm 报告 C1/SME2 已进入 vivo/OPPO 的 Lumex 设备；Dimensity 9500 与 vivo X300 时间链可确认 C1/SME2 进入量产产品。2026 年 Arm/MediaTek 资料报告 C2/Dimensity 9600 Pro 及相应终端系列，但本轮未独立测试这些设备的持续性能。 |
| IP 发布日可以直接当作手机上市日 | **不成立** | A76→Kirin 980→Mate 20、C1→Dimensity 9500→vivo X300 的日期链显示三者应分列。对其他节点如 Krait、Oryon、C2，按公开来源分别记录架构公告、SoC 公告和手机发布/开售。 |

## 3. 因果证据强度

- **强（产品/架构事实）：** Qualcomm 2011 年 Krait 公告；Apple A6/A7 产品公告；Kryo 280 的半定制许可资料；Samsung Exynos 990 官方规格与自研 CPU 项目终止公告；HiSilicon Kirin 980 规格；MediaTek Dimensity 9300/9500 官方 CPU 配置。
- **中（独立/工业技术分析）：** AnandTech 对 Cyclone、Kryo 280 和 Exynos 990 的微架构/许可分析；ISCA 2020 Exynos 工业论文。注意 ISCA 作者当时与 Samsung CPU 开发团队有关，属于直接工程披露但非完全独立团队的重复验证。
- **有限（第三方反向识别）：** Kirin 9000S/9010 的 Taishan 核线索。可确认有公开分析支持该解释，但不能据此声称已经知道完整流水线、ROB、预测器、执行端口或每个结构功耗。
- **有限（厂商自述）：** 所有“提升 X% 性能/能效”在缺少同口径设备、功耗、工作负载和软件版本时，仍然是厂商特定比较。
- **未验证：** 本轮没有统一设备实测，也没有把不同厂商的跑分合并为排名；没有验证 C1/C2 设备的长期热降频、真实 agentic 任务能耗或 SME2 的应用覆盖率。

## 4. 下一步审计动作

1. 将本轮发现写回主时间线与续研入口，避免旧状态继续说“尚未建立时间线”。
2. 继续逐核核验前端/分支、乱序执行、寄存器重命名、Load/Store、缓存/预取的代际变化。
3. 对 Taishan、Apple 和 Qualcomm 的隐藏微架构，优先使用高质量逆向/论文/架构资料；未披露部分保留 UNKNOWN。
4. 保持历史因果研究主线，不将本轮改写成新技术立项或产品性能排名。
