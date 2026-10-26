# 智能手机 SoC 整体架构演进｜技术洞察知识库

> **当前状态（2026-10-26）：已完成第26轮Apple A8—A13代际连续性审计。** 研究复盘2007—2026移动SoC尤其CPU的历史变化、驱动、收益、代价与瓶颈迁移，2027—2028只作条件性参考，不是新技术立项。第19—23轮形成历史因果/LLVM辅助机制，第24轮比较P/E、全大核与自研核组合，第25轮对照Apple/Samsung自研核，第26轮补全Apple Cyclone(A7)与Firestorm(A14)之间A8—A13逐代来源，并发现异构六核、E核OoO、共享缓存与iOS/DVFS共同演进。微架构细节部分依赖第三方逆向，单因素能效归因仍阻断。全SoC v1.3待Issue #1真实专家评审，PPT批量制作暂停。

仓名 `cpu-microarchitecture-trends` 沿用早期命名；项目研究对象是**智能手机完整 SoC/平台的 2007—2026 年演进及 2027—2028 年有条件前瞻**，并非只研究CPU。覆盖 CPU/GPU/DSP/NPU、ISP/编解码/显示、Modem-RF/天线、缓存/DRAM/互连、软件运行时、常驻感知/安全、电源域/封装/散热。严格区分**裸片、同封装/配套芯片、平台、手机整机和网络环境**。

## 一、最重要的入口

- **[第26轮：Apple A8—A13代际机制与因果链](03-analysis/Apple-A8-A13-代际机制与因果链-v0.1-2026-10-26.md)** — 从Typhoon/Twister到Hurricane/Zephyr、Monsoon/Mistral、Vortex/Tempest、Lightning/Thunder，区分核内改善、P/E控制、系统缓存与DVFS；[18组官方/逆向来源卡](02-evidence/sources/round-26-apple-a8-a13-primary-and-reverse-sources-2026-10-26.md) · [16项Claim审计](02-evidence/audits/round-26-apple-a8-a13-lineage-claim-audit-2026-10-26.md) · [事务26](00-project/research-transactions/round-26-2026-10-26.md)。

- **[第25轮：Apple Cyclone/Firestorm vs Samsung Exynos M1–M5核内因果对照](03-analysis/Apple-Cyclone-Firestorm-vs-Samsung-M1-M5-微架构因果比较-v0.1-2026-10-26.md)** — 正面比较前端宽度、ROB/退休队列的术语、预测、UOC、寄存器与跨层内存延迟；[Samsung第一手工程论文卡](02-evidence/sources/round-25-samsung-m1-m5-engineering-paper-2026-10-26.md) · [Apple黑盒测量卡](02-evidence/sources/round-25-apple-cyclone-firestorm-reverse-evidence-2026-10-26.md) · [逐项审计](02-evidence/audits/round-25-apple-samsung-mechanism-causal-audit-2026-10-26.md) · [事务记录](00-project/research-transactions/round-25-2026-10-26.md)。

- **[第24轮：CPU核组合分化与能效因果对照 v0.1](03-analysis/移动CPU核心组合分化与能效驱动因果对照-v0.1-2026-10-26.md)** — 对照Apple P/E、MediaTek 9300→9600 Pro全大核、Qualcomm Oryon，并拆分核内微架构/核型/频率档位/调度；[原始来源卡](02-evidence/sources/round-24-多层核心组合路线原始来源卡-2026-10-26.md) · [因果审计](02-evidence/audits/round-24-core-topology-causal-audit-2026-10-26.md) · [事务记录](00-project/research-transactions/round-24-2026-10-26.md)。

- **[移动 CPU 微架构历史变化时间线 v0.1](03-analysis/移动CPU微架构历史变化时间线-v0.1-2026-10-23.md)** — 按时间梳理主要转折、动因、收益、代价和未来参考。
- **[第十九轮初始来源审计](02-evidence/audits/round-19-cpu-history-timeline-source-audit-2026-10-23.md)** — 将官方/技术来源映射到历史主张，并明确厂商声明、第三方逆向和未知边界。
- **[第十九轮移动 CPU 核内微架构来源卡](02-evidence/sources/round-19-移动CPU核内微架构原始来源.md)** — A9、Krait、A72、A76、A77/A78、Apple Cyclone 的具体核内变化证据。
- **[第十九轮事务记录](00-project/research-transactions/round-19-2026-10-23.md)** — 本轮完成项、限制与下一步。
- **[第二十轮跨厂商微架构路线与产品化时间 v0.2](03-analysis/移动CPU跨厂商微架构路线与产品化时间-v0.2-2026-10-23.md)** — 比较 Apple、Qualcomm、Samsung、HiSilicon 与 MediaTek 的核设计路线，区分 IP、SoC、终端上市时间。
- **[第二十轮路线/时间审计](02-evidence/audits/round-20-cross-vendor-cpu-route-and-productization-audit-2026-10-23.md)** · [来源卡](02-evidence/sources/round-20-移动CPU跨厂商路线与产品化来源卡.md) · [事务记录](00-project/research-transactions/round-20-2026-10-23.md)。
- **[第二十一轮核内机制证据矩阵 v0.1](03-analysis/移动CPU核内机制证据矩阵-v0.1-2026-10-23.md)** — 逐核比较前端/分支、乱序执行、执行资源、Load/Store、缓存与预取；[机制审计](02-evidence/audits/round-21-mobile-cpu-core-mechanism-evidence-audit-2026-10-23.md)记录指标口径冲突与测量边界；[来源卡](02-evidence/sources/round-21-核内微架构机制原始来源卡.md) · [事务记录](00-project/research-transactions/round-21-2026-10-23.md)。
- **[第二十二轮微架构—LLVM 代码生成桥接矩阵 v0.1](03-analysis/移动CPU微架构与LLVM代码生成桥接矩阵-v0.1-2026-10-23.md)** — 说明目标模型、调度、寄存器分配、向量化、PGO、预取和 SME/ZA 的软件利用路径；[桥接审计](02-evidence/audits/round-22-llvm-hardware-codegen-bridge-audit-2026-10-23.md)与[来源卡](02-evidence/sources/round-22-LLVM代码生成与调度模型原始来源卡.md) · [事务记录](00-project/research-transactions/round-22-2026-10-23.md)。

- **[Cortex-A72 → A76 → A77 → A78 性能/能效声明口径审计](03-analysis/Cortex-A72-A76-A77-A78-%E8%B7%A8%E4%BB%A3%E5%9B%A0%E6%9E%9C%E5%AF%B9%E7%85%A7-v0.1-2026-10-23.md)** — 复核 Arm 官方性能/能效声明的基准、对照条件与制程混杂，避免将不同指标拼成无条件的代际增长曲线。
- **[Cortex-A72 → A76 → A77 → A78 跨代因果对照 v0.1](03-analysis/Cortex-A72-A76-A77-A78-跨代因果对照-v0.1-2026-10-23.md)** — 以 Arm 原始资料对照四代设计动作、明确动机、机制、收益口径、代价与尚未证实的瓶颈转移。
- **[移动 CPU 微架构历史因果链完整性审计 v0.1](03-analysis/移动CPU微架构历史因果链完整性审计-v0.1-2026-10-23.md)** — 检查“前代约束→设计动作→作用机制→收益/代价→后续瓶颈”是否有证据支撑，给出 A72/A76/A77/A78 主线及 Apple/Samsung/Qualcomm/Taishan 的证据等级与缺口；确认尚不能宣称全部代际因果链已闭环。
- **[LLVM—核内机制交叉索引与历史因果补充](03-analysis/移动CPU核内机制证据矩阵-v0.1-2026-10-23.md)**、[历史时间线补充](03-analysis/移动CPU微架构历史变化时间线-v0.1-2026-10-23.md) — 将硬件机制与 LLVM 23.1.4 的软件利用路径关联，并明确模型、profile 与真实手机效果的证据边界。
- **[LLVM 23.1.4 代码生成优化入口审计 v0.1](03-analysis/LLVM-23.1.4-代码生成优化入口审计-v0.1-2026-10-23.md)** — 固定版本核查寄存器压力调度、寄存器分配、向量化成本模型、profile 引导的基本块布局与 SME 状态属性；明确软件机制存在不等于手机端效果已验证。
- **[LLVM 23.1.4 AArch64 目标调度模型核验 v0.1](03-analysis/LLVM-23.1.4-AArch64-目标调度模型核验-v0.1-2026-10-23.md)** — 固定 tag 下核验 A72/A76/A77/A78/A710/A715/A720/X1/X2/X3/X4/X925 的 ProcessorModel 与共享 scheduler model，记录模型参数、源码 SHA 和不应外推的边界。
- **[第二十三轮 LLVM 版本冻结与目标模型核验记录（进行中）](00-project/research-transactions/round-23-2026-10-23.md)** — 已选择 LLVM 23.1.4 固定 tag，明确逐核字段与尚待源码验证的边界；不把 main 的模型映射冒充固定版本事实。
- **[研究目的澄清与下一步框架（2026-10-23）](00-project/research-transactions/round-18-2026-10-23.md)** — 将 CPU 深化支线重新锚定在历史变化、动因、后果和未来趋势参考。
- **[第十七轮 CPU 微架构/LLVM 初始来源筛选](02-evidence/audits/round-17-CPU-uArch-LLVM-initial-seed-discovery-2026-10-22.md)** — 官方 SME/ABI/LLVM 种子、分支预测研究与设备迁移边界。
- **[CPU 微架构历史演进与因果分析框架](00-project/cpu-uarch-llvm-extension-scope-lock-2026-10-22.md)** — 明确通用移动 CPU 核、寄存器/状态、存储层次与 LLVM 代码生成的剩余问题。
- **[第十五轮跨仓范围核对与 CPU/LLVM 成果复用](02-evidence/audits/round-15-跨仓范围核对与CPU-LLVM成果复用-2026-10-22.md)** — 明确本仓全 SoC 报告与已结题 Agentic CPU-uArch 专项的分工，避免重复研究。
- **[第十四轮结论审计与技术决策闭环](02-evidence/audits/round-14-结论审计与技术决策闭环-2026-10-22.md)** — 核心结论强度、竞争解释、可验证性与范围缺口。
- **[当前主报告 v1.3：智能手机 SoC 整体架构演进](05-deliverables/08-智能手机SoC整体架构演进-技术洞察证据收敛版-v1.3.md)** — 历史/CPU/四任务与系统架构综合；待专家评审。
- **[Agentic CPU-uArch 现行技术组合](https://github.com/xjs-work-lab/agentic-CPU-uArch/blob/main/09-roadmap/current.md)** — Agentic 手机 CPU/LLVM/Runtime 的独立结题决策。
- **[CPU/LLVM、微内核与异构 NPU 机制审计](https://github.com/xjs-work-lab/agentic-CPU-uArch/blob/main/analysis/engineering/round15f-cpu-llvm-compiler-pressure-2026-10-08.md)** — 已有 AArch64/SME/LLVM/微内核与 CPU–NPU 分工证据。
- **[PPT逐页内容设计 v0.1（18页候选）](05-deliverables/09-智能手机SoC架构演进-PPT逐页内容设计-v0.1.md)** — 逐页结论、叙事、证据ID、外推边界和备注要求。
- [三页试制与渲染 QA 记录](02-evidence/audits/round-13-ppt-pilot-qa-2026-10-22.md) — 用户视觉验收待完成。
- [第十三轮预裁决矩阵与 PPT 准入清单](02-evidence/audits/round-13-预裁决矩阵与PPT准入清单-2026-10-22.md)。
- [第十二轮反向审查与技术评审准备](02-evidence/audits/round-12-v1.3-反向审查与技术评审准备-2026-10-22.md)；[正式评审 Issue #1](https://github.com/xjs-work-lab/cpu-microarchitecture-trends/issues/1)。
- [第十一轮决策性证据收敛与发布闸门](02-evidence/audits/round-11-关键证据收敛与发布闸门-2026-10-21.md)；[第十轮深入审计](02-evidence/audits/round-10-深入内容与正确性审计-2026-10-21.md)。
- **[续研入口](00-project/00-续研入口.md)** — 唯一主问题、状态、限制和下一步；[五个最终研究问题](00-project/01-任务简报.md)。
- [全 SoC 主报告中央证据台账 CSV（114条唯一记录）](02-evidence/02-证据台账.csv) — 86条映射核心 Claim、28条未映射；CPU 历史/LLVM 深化分支的独立来源卡按轮次归档，暂不计入此数，待映射回主报告 Claim 时再去重合并。
- [早期/普及型/华为路线 A01–A07 来源卡](02-evidence/sources/round-10-audit-早期与普及型结构原始来源.md)；[第1–9轮研究索引](01-research/README.md)；[跨负载判断与待证伪问题](03-analysis/跨负载判断与待证伪问题.md)。
- [v1.2审计补充版（历史）](05-deliverables/07-智能手机SoC整体架构演进-技术洞察审计补充修订版-v1.2.md)；[v1.1审计修订版（历史）](05-deliverables/06-智能手机SoC整体架构演进-技术洞察审计修订版-v1.1.md)；[v1.0原始综合稿（历史）](05-deliverables/05-智能手机SoC整体架构演进-技术洞察终稿-v1.md)。

## 二、目前可以与不可以下的结论

**可以有边界地讨论：** 早期通信/媒体集成、异构CPU与常驻低功耗、专用AI与5G、跨引擎媒体/AI协同、数据/软件与终端电热治理；CPU/GPU/NPU、ISP/媒体、Modem-RF、内存、安全与软件的功能分工；四类负载（4K视频、端侧AI、蜂窝通信、持续游戏）的QoS差异。

**不能宣称已证明：** 某个缓存/NPU/CPU核/互连普遍是首要瓶颈；某个微架构单独带来X% IPC/FPS/续航；主报告台账中的114条来源都已全文核验；不同手机或不同测试口径可以排出无条件赢家。TOPS、RF dB、发射占空比、3DMark稳定性%和CPU/GPU rail功率不可混用。

## 三、项目目录

| 目录 | 职责 |
|---|---|
| [00-project](00-project/README.md) | 目标、状态、续研入口与事务记录 |
| [01-research](01-research/README.md) | 前九轮原始研究与历史版本 |
| [02-evidence](02-evidence/README.md) | 原始来源、台账、Claim映射、审计 |
| [03-analysis](03-analysis/README.md) | 跨源推论、竞争解释与可证伪假设 |
| [04-figures](04-figures/README.md) | 可编辑图源与示意图 |
| [05-deliverables](05-deliverables/README.md) | v1.0/v1.1/v1.2历史稿、v1.3当前稿与未来PPTX |
| [06-tools](06-tools/README.md) | 校验脚本和后续工具 |

## 四、下一步

1. **整体因果覆盖审计：** 将Apple A8—A13、Samsung M1—M5、Arm A72—A78、第24轮P/E/全大核纳入统一的“代际×变化原因×证据强度×反例”矩阵，评估是否足以收敛历史趋势结论。
2. **定向补证而不扩张型号：** 重点核验A10/A11内部微架构缺失字段、A12/A13小核低层测试/DVFS口径，以及安全/负载等机制驱动与竞争解释；无法公开确认保持UNKNOWN。
3. **严格归因边界：** 不拼接厂商宣传收益、第三方黑盒、Samsung周期精确模拟为同一数值序列；CPU核内、SoC内存/缓存、OS调度和整机热功耗分层。
4. **交付独立：** 全SoC v1.3专家评审Issue #1仍未完成，PPT继续暂停。

公开仓不存公司非公开材料或未经授权的第三方全文。
