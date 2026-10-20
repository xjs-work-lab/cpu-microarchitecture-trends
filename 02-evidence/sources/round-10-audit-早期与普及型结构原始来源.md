# 技术审计补充：早期、普及型及华为路线的原始资料（A01—A07）

资料核对日期：2026-10-21。新增来源用于弥补原技术报告对2007—2010及中端/大众型SoC覆盖不足，亦为2017年华为路线建立同期原始证据。**发布、样品出货、商业手机装机分开表示**。此表证明技术节点存在，不是性能/能效独立实测。

| ID | 原始资料（直接链接） | 发布时间和定位 | 原文能证明什么 | 不能据此证明 / 限制 |
|---|---|---|---|---|
| A01 | [Qualcomm, Snapdragon QSD8250/QSD8650 发布](https://www.qualcomm.com/news/releases/2007/11/qualcomm-premieres-snapdragon-first-chipset-solutions-break-gigahertz) | 2007-11-13，官方新闻稿正文 | 官方宣称首批 QSD8250/8650 已向设备厂商供货；定制约1 GHz CPU、约600 MHz DSP、3G、多媒体与通信平台能力 | 不证明2007已有现代NPU；“供货给厂商”不等于2007年大量智能手机量产装机；续航主张未独立复验 |
| A02 | [Qualcomm, QSD8650A 45nm 版本](https://www.qualcomm.com/news/releases/2009/06/qualcomm-expands-snapdragon-platform-45nm-chipset-smarter-smartphones-and) | 2009-05-31，发布、计划2009年底前送样 | 官方公布从更早的Snapdragon版本向45nm/更高CPU频率/图形和多媒体功能升级 | “峰值性能+30%”“动态功率降低最多30%”为厂商宣称且与制程变化强耦合，不是独立微架构IPC提升；计划送样不等于已量产 |
| A03 | [MediaTek, MT6589 Cortex-A7 四核SoC](https://corp.mediatek.com/news-events/press-releases/mediatek-strengthens-global-position-with-worlds-first-quad-core-cortex-a7-system-on-a-chip-mt6589) | 2012-12-12，原始厂商发布 | 28nm、4×Cortex-A7、PowerVR 5XT、UMTS/HSPA+/TD-SCDMA多模modem、双SIM、集成ISP、1080p30，面向中高端及更广泛Android产品 | “世界首个”是厂商措辞；不证明任何终端能效倍数，也不能把3G/HSPA+写成集成LTE；发布≠实际渗透率 |
| A04 | [Qualcomm, Snapdragon 410：大众型LTE/64位方案](https://www.qualcomm.com/news/releases/2013/12/qualcomm-technologies-introduces-snapdragon-410-chipset-integrated-4g-lte) | 2013-12-08，原始新闻稿 | 28nm、64位能力、Adreno 306、集成LTE、多SIM、视频/相机支持；面向高出货量市场；当时预计2014上半年送样、下半年商用设备 | 2013发布不等于2013已有大量商用设备；RF360前端与SoC不是同一裸片；厂商价格/性能描述未独立验证 |
| A05 | [Qualcomm, Snapdragon 410商用进展](https://investor.qualcomm.com/news-events/press-releases/news-details/2015/Qualcomm-Announces-New-Milestone-in-Snapdragon-410-and-210-Shipments-09-14-2015/default.aspx) | 2015-09-14，投资者新闻稿 | 厂商称Snapdragon 410在逾550款终端设计中出现、累计出货逾2亿颗；这是**有来源署名的厂商商业化主张**，补充2013发布与后续装机的时间差 | 数值未由独立供应链核实，不得当作中低端全部SoC份额/真正技术优越性；产品设计数不等于已销售设备数 |
| A06 | [Huawei, IFA 2017 Kirin 970](https://www.huawei.com/en/news/2017/9/Mobile-AI-IFA-2017) | 2017-09-02，华为同期原始发布 | 10nm、8核CPU、12核GPU、独立NPU的手机端AI路线与本地+云协同设计主张 | “25x性能/50x效率”等为华为自设基准的厂商主张，不是行业可比结论；NPU存在不证明指定模型运行率 |
| A07 | [Huawei, Mate 10 / Mate 10 Pro 发布](https://www.huawei.com/en/news/2017/10/HUAWEI-Mate10-Mate10Pro) | 2017-10-16，华为同期手机产品发布 | Kirin 970进入Mate 10系列手机，披露双ISP、NPU/HiAI、双4G卡及相机AI功能。区分芯片发布与实际手机产品发布 | 发布仍不是销售渗透率/独立性能测量，“业界首个”是厂商归属的优先权主张 |

## 用于纠正旧叙事

- **历史起点**：2007的QSD8250/8650不是仅回顾文献提到的模糊“早期平台”，而有当年官方新闻稿；2009变化中工艺/频率混杂尤其明显。[A01][A02]
- **非旗舰路线**：2012 MT6589的四核A7/多模3G、2013 Snapdragon410的64位/LTE/QRD说明“向高端增加功能”之外，还有“把已有能力迁入主流成本/区域运营商约束”的重要系统路线。[A03–A05]
- **华为现场节点**：Kirin 970的独立NPU于2017年9月披露，10月手机发布；与Apple A11等是不同厂商同期选择，不能用华为“第一”的营销措辞进行全球技术首创裁决。[A06][A07]
- 若最终报告涉及**实际销量/渗透率、微架构IPC、功耗收益**，本组来源仍不足，必须另有独立量化或明确标成公开上限。
