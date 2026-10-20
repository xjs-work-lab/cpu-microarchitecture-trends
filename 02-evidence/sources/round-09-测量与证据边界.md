# 第九轮新来源卡与可证实范围

日期：2026-10-20。**本轮正文**：[独立测量审计](../../01-research/rounds/14-第九轮独立测量与证据审计.md)。来源ID全局唯一，旧记录不覆盖。同一研究团队的相近论文不得当独立复验。

| ID | 来源（原始链接） | 作者/机构、出版信息 | 可核实范围 | 不能证明/使用限制 |
| --- | --- | --- | --- | --- |
| X01 | [Comparative Analysis of Power Consumption in LTE, 5G-NSA, 5G-SA, and Private 5G Networks](https://doi.org/10.1109/CCNC54725.2025.10976187) | R. Singh、D. Jadaan、D. Ghimire、M. Berger、A. Skavhaug、L. Dittmann；IEEE CCNC 2025，2页 | **仅摘要已核到**：两地点UE能耗；NSA较LTE+92–111%、SA+79%、私网SA较公网SA节能63% | 不可泛化5G所有手机；尚缺可核实全文的UE型号、场景、频段、功耗边界；与X02同研究组 |
| X02 | [Evaluating Energy Efficiency: A Comparative Study of LTE, 5G-NSA, 5G-SA, and Private 5G Networks](https://doi.org/10.1109/CommNet63022.2024.10793350) | 同X01六作者；IEEE CommNet 2024，7页 | 机构元数据摘要列出与X01相同的92–111%、79%、63% | **不能作第二组独立实验**；是否完全相同原始数据仍需全文 |
| X03 | [3 W's of smartphone power consumption](https://wcsng.ucsd.edu/ue-power/) | Agrim Gupta等；UCSD，ACM MobiCom 2024 workshop | Google Pixel 7A使用ODPM观察无线连接与显示组件；Samsung S23+以估算方法辅助 | 网站概述无统一手机modem毫瓦数据；方法/成品机证据而非chip级A/B；[配套分析代码](https://github.com/ucsdwcsng/Perfetto-Trace-Analysis) |
| X04 | [Antenna Performance Over-the-Air Testing of 5G Commercial Smartphones](https://doi.org/10.1109/TIM.2024.3373106) | H. Gao、X. Chen、Y. Liu、G. F. Pedersen；IEEE TIM 2024 | 18部商用5G手机TRP/TIS，头部侧向变化可至约10dB TRP差 | **dB不是手机电池功耗W**；[大学资料页](https://vbn.aau.dk/en/publications/antenna-performance-over-the-air-testing-of-5g-commercial-smartph/) |
| X05 | [Study and analysis of runtime energy consumption in cellular 5G network](https://doi.org/10.1186/s13638-026-02598-6) | M. Uitto等；J Wireless Commun Networking，2026 | HTML全文§4.1无DRX、§4.3/5.1：Intel i7笔记本有线连接Huawei 5G CPE Pro 2，另测RAN | **排除：不是智能手机Modem能耗实测**，不能转述为“5G手机4G/5G功耗相当” |
| X06 | [Bare-Metal Development Setup for Highly Accurate Energy Measurements of Mobile Radio Interface](https://doi.org/10.1109/SACI66288.2025.11030159) | IEEE SACI 2025（作者信息待核） | 电流探头/万用表测无线模块原子操作能耗的方法 | **模块台架不等于成品智能手机** |
| X07 | [Vivo X300 review](https://www.notebookcheck.net/Brilliant-Zeiss-camera-in-a-compact-smartphone-Vivo-X300-review.1192262.0.html) | Notebookcheck（2026发表） | Dimensity9500，3DMark Wild Life Extreme **20分钟稳定性46.7%**，单次Wild Life Extreme得分7089 | 是设备级稳定性%，不是fps或GPU能效；与X08同媒体机构 |
| X08 | [OPPO Find X9 review](https://www.notebookcheck.net/Oppo-Find-X9-smartphone-review-High-end-for-under-900-but-with-SoC-problems.1173149.0.html) | Florian Schmitt，Notebookcheck，2025-11-29 | Dimensity9500，同一UL测试稳定性**74.3%**；跨评测表单次成绩6251 | 设备差异不能归因某散热/固件或裸片；不是独立机构复验 |
| X09 | [UL 3DMark Wild Life Extreme Overview](https://support.benchmarks.ul.com/support/solutions/articles/44002201772) | UL Solutions 基准说明 | Stress Test使用相同场景**20分钟循环**，主要输出性能随时间变化曲线 | 方法不是测量样本；Stability%≠绝对稳定帧率 |
| X10 | [In Situ Assessment of Uplink Duty Cycles for 4G and 5G Wireless Communications](https://doi.org/10.3390/s24103012) | G. Vermeeren、L. Verloock、S. Aerts、L. Martens、W. Joseph；Sensors 2024 | 10处位置、6业务；Twitch/VoLTE/WhatsApp上行占空比4–22% | 发射占空比并非电池能耗W，不可直接推modem省电 |

**来源依赖：**X01/X02同作者且数值重复，只计一个研究团队链；X07/X08为同一评测机构的不同手机测试，不算不同机构复验。**排除证据：**X05不是商品智能手机；X04、X10指标不是电池能耗。**期望补证：**X01完整实验方法；Pixel7A ODPM原始数据；OPPO/vivo逐loop绝对得分及温度/功耗轨迹。