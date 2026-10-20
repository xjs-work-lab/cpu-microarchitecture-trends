# 第八轮公开来源卡

资料截点：2026-10-20；本轮核读，**不代表来源的产品收益被独立测量验证**。来源事实→论证推断见[第八轮](../../01-research/rounds/13-第八轮通信与持续游戏任务链.md)。

| ID | 原始出处 | 明确支持与不能推导的范围 | 链接 |
| --- | --- | --- | --- |
| N01 | ETSI 3GPP TS 38.321 15.4.0 §5.7 | RRC配置DRX使PDCCH监听可不连续；不是某手机实际功耗 | [原文](https://www.etsi.org/deliver/etsi_ts/138300_138399/138321/15.04.00_60/ts_138321v150400p.pdf) |
| N02 | MediaTek M80 5G modem 发布资料 | UltraSave网络环境/频率动态适配由厂商披露 | [原文](https://www.mediatek.com/press-room/mediatek-unveils-new-m80-5g-modem-with-support-for-mmwave-and-sub-6-ghz-5g-networks) |
| N03 | MediaTek 5G UltraSave | DRX、BWP、WUS、SCell dormancy等方案；省电数字为主张 | [原文](https://www.mediatek.com/technology/5g/5g-modem) |
| N04 | Qualcomm Snapdragon 865平台发布 | 865配套X55 Modem-RF；平台≠单裸片 | [原文](https://www.qualcomm.com/news/releases/2019/12/qualcomm-introduces-worlds-most-advanced-5g-mobile-platform) |
| N05 | Qualcomm X55 Modem-RF产品页 | Modem到RF/天线的系统及SA/NSA能力，不是实测 | [原文](https://www.qualcomm.com/modems/products/snapdragon-x55-5g-modem) |
| N06 | Samsung Exynos 2200产品资料 | 集成5G modem的不同产品架构选择 | [原文](https://semiconductor.samsung.com/processor/mobile-processor/exynos-2200/) |
| N07 | AOSP 5G network slicing文档 | App/Telephony/Radio HAL/modem协作层级，不代表所有手机开启切片 | [原文](https://source.android.com/docs/core/connect/5g-slicing) |
| N08 | AOSP Implement IMS | IMS部分功能可在AP或modem实现 | [原文](https://source.android.com/docs/core/connect/ims) |
| G01 | Arm Mali tile-based rendering | tile、Transaction Elimination、AFBC降低部分外存写回的技术机制 | [原文](https://developer.arm.com/community/arm-community-blogs/b/mobile-graphics-and-gaming-blog/posts/the-mali-gpu-an-abstract-machine-part-2---tile-based-rendering) |
| G02 | AOSP Graphics components | Surface/BufferQueue/SurfaceFlinger/显示硬件结构 | [原文](https://source.android.com/docs/core/graphics) |
| G03 | AOSP Hardware Composer HAL | 可将合成部分交HWC，具体取决于终端 | [原文](https://source.android.com/docs/core/graphics/hwc) |
| G04 | Android Frame Pacing Swappy | 渲染与显示帧同步，不能当作硬件加速收益 | [原文](https://developer.android.com/games/sdk/frame-pacing) |
| G05 | Android Dynamic Performance Framework | 热状态/CPU Hint/Game Mode等OS—应用功耗协作 | [原文](https://developer.android.com/games/optimize/adpf) |
| G06 | Android Game Mode FPS throttling | 帧率上限与功耗权衡，官网效果非设备通用值 | [原文](https://developer.android.com/games/optimize/adpf/gamemode/fps-throttling) |
| G07 | Android Game Mode interventions | 下调背缓冲尺寸等软件减负方案 | [原文](https://developer.android.com/games/optimize/adpf/gamemode/gamemode-interventions) |
| G08 | UL 3DMark Wild Life Extreme Stress Test | 20分钟重放场景测性能变化；基准方法不等于实际设备样本 | [原文](https://support.benchmarks.ul.com/support/solutions/articles/44002201772-overview-of-3dmark-wild-life-extreme-benchmark) |
| G09 | Android CPU/GPU optimization tips | ASTC、几何、render attachments对负载/带宽影响 | [原文](https://developer.android.com/games/optimize/optimization-tips) |

证据性质：N01为2019年Release15规范（非最新全部扩展）；N02–N06为厂商产品资料（收益属于CLAIM）；N07/N08/G02–G07/G09是系统规范或开发接口（不保证每机落地）；G01为IP技术机制（不代表所有GPU）；G08是独立测试方法（**尚无本轮抄录的设备测量点**）。
