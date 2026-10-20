# 第九轮：八条关键历史/前瞻原始来源审计
截至2026-10-20。本轮只审核与五问关系最强的八条既有ID，**并非此前所有93条原文完成重新核查**；所称“核实”指公开官方页披露，**不包括重现实测**。

| ID | 已核实官方原始来源 | 可使用的事实层级 | 必须保留的边界 |
| --- | --- | --- | --- |
| E02 | [Qualcomm MSM8960/S4，2012](https://www.qualcomm.com/news/onq/2012/06/what-integrating-4g-lte-modem-means-snapdragon-s4-processor-and-battery-life) | LTE基带与AP结合在同一芯片 | 同期还有28nm/CDRX，不能单因素推出续航收益 |
| P03 | [Apple iPhone5s，2013](https://www.apple.com/newsroom/2013/09/10Apple-Announces-iPhone-5s-The-Most-Forward-Thinking-Smartphone-in-the-World/) | Secure Enclave在A7内；手机还有M7运动协处理器 | **不能把M7误画为A7裸片内的计算单元** |
| E05 | [Qualcomm Snapdragon865+X55，2019](https://www.qualcomm.com/news/releases/2019/12/qualcomm-introduces-worlds-most-advanced-5g-mobile-platform) | 865**平台**与X55 Modem-RF协同 | 不能把modem-RF及天线统称865裸片内 |
| P10 | [Samsung Exynos2200](https://semiconductor.samsung.com/processor/mobile-processor/exynos-2200/) | 官方明确integrated 5G modem，披露AMIGO、GPU、ISP、安全 | 厂商特征和宣称收益不等于独立基准 |
| E08 | [MediaTek Dimensity9500](https://www.mediatek.com/products/smartphones/mediatek-dimensity-9500) | 统一动态CPU/GPU/NPU data cache及新SLC管理 | 未给指定任务cache命中率/功耗因果对照 |
| E10 | [Arm CSS for Mobile 2](https://newsroom.arm.com/news/arm-css-for-mobile-2-agentic-ai-mobile-graphics) | 2026-09发布CPU SME2、GPU神经加速及系统IP | IP公布不代表所有量产手机采用 |
| E11 | [Apple iPhone18 Pro/A20 Pro](https://www.apple.com/newsroom/2026/09/apple-debuts-iphone-18-pro-and-iphone-18-pro-max/) | A20 Pro处理引擎/内存带宽及终端级内存封装和均热变化 | 整机持续性能声明包含工艺/封装/热，不能算纯微架构收益 |
| V13 | [Qualcomm 2026 Hexagon NPU](https://www.qualcomm.com/news/onq/2026/09/hexagon-npu-agentic-ai-architecture) | Element Accelerator、NPU内共享存储扩大50%等**厂商公开披露** | “内存50%更大”不是模型端到端效率或token/s提升50% |

审计决定：这8条可作为**结构事实/厂商披露**用于定性SoC历史及条件性前瞻；若要引用性能百分比，必须另列真实比较基线、硬件和软件条件。下一轮只对关键结论依赖的其余证据定向核查。