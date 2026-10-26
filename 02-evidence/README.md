# 事实证据、来源与审计

## 当前审计入口

- **[第28轮P0关键因果/2026产品化/数值来源审计](audits/round-28-P0因果与产品化关键证据审计-2026-10-26.md)** · [原文来源卡](sources/round-28-关键因果-产品化与测量口径来源卡-2026-10-26.md)：十项主张判定；Samsung M4/M5跨时钟域路径、A13 E核DVFS与2026 9600Pro具体手机发布；中央114条唯一来源中只更新M01/M03/M04、X07/X08/X09、E11七个高重要性记录。**不是**全114条外链重新核实或整体因果定量认证。

- **[第27轮五问题覆盖、114条台账字段卫生与12条因果反例审计](audits/round-27-五问题覆盖-证据卫生-因果反例审计-2026-10-26.md)**：直接解析CSV：114唯一ID、86条对应判断、30条精确位置、基线/单位/反例各4，区分字段齐备与全量原文核验；与[全SoC/CPU覆盖矩阵](../03-analysis/全SoC-移动CPU历史演进五问题覆盖矩阵-v0.1-2026-10-26.md)和[历史结论草案](../03-analysis/移动SoC-CPU历史结论收敛草案-v0.1-2026-10-26.md)互链。

- **[第26轮Apple A8—A13 16项Claim审计](audits/round-26-apple-a8-a13-lineage-claim-audit-2026-10-26.md)** · [18组官方及逆向来源卡](sources/round-26-apple-a8-a13-primary-and-reverse-sources-2026-10-26.md)：明确Apple官方SoC/核群声明、AnandTech芯内逆向、TechInsights拆片和SPEC/DVFS测试边界；CPU支线来源不计入下方主报告114条中央台账。

- **[第25轮Apple/Samsung因果可比性审计](audits/round-25-apple-samsung-mechanism-causal-audit-2026-10-26.md)** · [Samsung设计者论文原始来源](sources/round-25-samsung-m1-m5-engineering-paper-2026-10-26.md) · [Apple黑盒实验原始来源](sources/round-25-apple-cyclone-firestorm-reverse-evidence-2026-10-26.md)：核对宽度、ROB/退休队列、UOC省电、预取/访存与模拟/真机边界；支线来源尚不计入下方主报告114条台账。

- **[第24轮核组合与因果审计](audits/round-24-core-topology-causal-audit-2026-10-26.md)** · [第24轮原始来源卡T24-01—11](sources/round-24-多层核心组合路线原始来源卡-2026-10-26.md)：审计全大核/P-E/自研核、频率档位、持续能效的定量归因限制。这些支线来源暂不计入下方主报告114条中央台账。

- [第十九轮：移动 CPU 历史时间线初始来源审计](audits/round-19-cpu-history-timeline-source-audit-2026-10-23.md)：将官方/技术来源映射到 2007–2026 CPU 变化点，区分设计动因、厂商收益声明、第三方逆向与未知边界。
- [第十九轮移动 CPU 核内微架构原始来源卡](sources/round-19-移动CPU核内微架构原始来源.md)：收录 A9、Krait、A72、A76、A77/A78、Apple Cyclone 的核内机制资料和外推限制。
- [第二十轮跨厂商 CPU 路线与产品化来源卡](sources/round-20-移动CPU跨厂商路线与产品化来源卡.md)：区分自研核、半定制核、Cortex IP 与 CSS 集成，并核对关键 SoC/手机日期。
- [第二十轮路线与产品化时间审计](audits/round-20-cross-vendor-cpu-route-and-productization-audit-2026-10-23.md)：汇总主张核验、来源层级、因果强度与公开资料边界。
- [第二十一轮核内机制证据审计](audits/round-21-mobile-cpu-core-mechanism-evidence-audit-2026-10-23.md)：逐项审计 A72 dispatch 口径、Apple Firestorm 队列术语、Samsung 模拟数据与各厂商公开披露边界。
- [第二十一轮核内微架构机制原始来源卡](sources/round-21-核内微架构机制原始来源卡.md)：Arm A9/A72/A76/A77/A78、Apple Cyclone/Firestorm、Samsung Exynos M1–M6 的原始来源与边界。
- [第二十二轮桥接证据审计](audits/round-22-llvm-hardware-codegen-bridge-audit-2026-10-23.md)：审计 LLVM 目标调度模型、寄存器分配、PGO、向量化、prefetch 与 SME/ZA lowering 的直接证据及其手机端效果边界。
- [第二十二轮 LLVM/调度模型原始来源卡](sources/round-22-LLVM代码生成与调度模型原始来源卡.md)：收录 LLVM CodeGenerator、MachineScheduler、Vectorizers、Clang PGO、llvm-mca、AArch64 TableGen 与 SME 文档。

- [第十七轮 CPU 微架构/LLVM 初始来源筛选](audits/round-17-CPU-uArch-LLVM-initial-seed-discovery-2026-10-22.md)：官方 SME/ABI/LLVM 机制种子、分支预测候选论文及移动适用性边界。

- [第十五轮跨仓范围核对与 CPU/LLVM 成果复用](audits/round-15-跨仓范围核对与CPU-LLVM成果复用-2026-10-22.md)：将本仓全 SoC 研究与已结题的 Agentic CPU-uArch/LLVM 专项分工；后者只在出现决策性新公开证据或关键错误时重开。
- [第十四轮结论审计与技术决策闭环](audits/round-14-结论审计与技术决策闭环-2026-10-22.md)。

## 唯一证据登记

[全 SoC v1.3 主报告中央证据台账 CSV](02-证据台账.csv) **当前共114条唯一来源记录**，以CSV中实际存在的唯一ID为准。CPU 历史/LLVM 深化支线的轮次来源卡单独归档，未映射回主报告 Claim 前不计入该数；后续纳入时必须先做来源去重与 Claim 映射。E13与A01指向同一2007 Qualcomm新闻稿，E13已从当前台账移除；第十一轮新增Y01（AOSP Neural Networks HAL接口说明）。旧版本对基础来源与后续补充的分段统计存在口径不一致，因此不再用旧分段算术推算当前总数。**记录条数不是独立测量组数，也不是全部来源全文/页码核验完成数。**

- [早期/普及型/华为路线七条同期原文](sources/round-10-audit-早期与普及型结构原始来源.md)：2007、2009、2012、2013、2015、2017的原始发布与边界。
- [深入内容与正确性审计（2026-10-21）](audits/round-10-深入内容与正确性审计-2026-10-21.md)：AU-01至AU-17问题、C01–C11 Claim映射、修订结果与仍未通过的验收项。
- [第十轮初始来源/链接审计（历史快照）](audits/round-10-终稿来源与推论审计.md)。
- [第九轮10条测量/方法来源](sources/round-09-测量与证据边界.md)及[八条历史官方材料审计](audits/round-09-关键论据审计.md)。
- [第八轮通信/游戏原始来源](sources/round-08-来源与边界.md)。

- **[第十三轮预裁决矩阵与PPT准入清单](audits/round-13-预裁决矩阵与PPT准入清单-2026-10-22.md)**：EX-01至EX-12研究侧预裁决，划分可直接进入PPT、需限定和必须保留未知的结论。
- [第十二轮反向审查与技术评审准备](audits/round-12-v1.3-反向审查与技术评审准备-2026-10-22.md)：专家正式裁决清单；[正式评审Issue #1](https://github.com/xjs-work-lab/cpu-microarchitecture-trends/issues/1)。
- [第十一轮决策性证据收敛](audits/round-11-关键证据收敛与发布闸门-2026-10-21.md)：R05/R07、V11/V12/Y01、P09、M01/M04/M03的原文定位与不允许外推范围，当前核心报告[v1.3](../05-deliverables/08-智能手机SoC整体架构演进-技术洞察证据收敛版-v1.3.md)。

## 台账健康度

原始103条基础记录中，标题和URL均有值，但作者、准确位置、对应判断、比较基线、指标单位、测量层级等结构化字段大量缺失。当前**86条记录映射到核心Claim，28条尚未映射**。已映射不代表来源全文或页码全部复核；旧条目的逐段核查按决策影响优先级推进，不以猜测填空。

测量边界必须保留：X01/X02为同作者相近结果；X05测的是Laptop+CPE而非手机Modem；X04的TRP/TIS为dB，X10为上行占空比，均不是手机电池功率；X07–X09的稳定性%不等于FPS、瓦数或芯片微架构收益。M01/M04为设备级估算主板功耗曲线，不是CPU/GPU rail；M03是端侧AI基准方法，未在本报告中变成同版本跨手机排名。

来源ID族：S、R、M、T、E、P、V、N、G、X、A、Y（第十一轮）。外部URL索引不是已入仓的原始PDF；未经授权不镜像第三方全文。
