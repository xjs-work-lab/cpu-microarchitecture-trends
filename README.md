# 智能手机 SoC 整体架构演进｜技术洞察知识库

> **当前状态（2026-10-23）：已按用户澄清校正研究目标。** 本项目要复盘移动终端 SoC、尤其 CPU 的历史变化点，解释变化动因、收益、代价与瓶颈转移，并据此理解未来趋势；不是以提出新技术立项为目标。第十七轮的 LLVM/SME/分支预测材料仅是初始种子；第十九轮建立了 CPU 历史变化时间线；第二十轮完成跨厂商路线与产品化时间审计；第二十一轮已归档逐核微架构机制矩阵，第二十二轮已归档硬件机制—LLVM 代码生成桥接矩阵。下一步核验 LLVM 目标模型与手机 CPU 型号/版本的对应关系，并把软件利用路径回写历史因果时间线。全 SoC v1.3 仍待 Issue #1 真实专家评审与用户视觉验收；PPT批量制作暂停。

仓名 `cpu-microarchitecture-trends` 沿用早期命名；项目研究对象是**智能手机完整 SoC/平台的 2007—2026 年演进及 2027—2028 年有条件前瞻**，并非只研究CPU。覆盖 CPU/GPU/DSP/NPU、ISP/编解码/显示、Modem-RF/天线、缓存/DRAM/互连、软件运行时、常驻感知/安全、电源域/封装/散热。严格区分**裸片、同封装/配套芯片、平台、手机整机和网络环境**。

## 一、最重要的入口

- **[移动 CPU 微架构历史变化时间线 v0.1](03-analysis/移动CPU微架构历史变化时间线-v0.1-2026-10-23.md)** — 按时间梳理主要转折、动因、收益、代价和未来参考。
- **[第十九轮初始来源审计](02-evidence/audits/round-19-cpu-history-timeline-source-audit-2026-10-23.md)** — 将官方/技术来源映射到历史主张，并明确厂商声明、第三方逆向和未知边界。
- **[第十九轮移动 CPU 核内微架构来源卡](02-evidence/sources/round-19-移动CPU核内微架构原始来源.md)** — A9、Krait、A72、A76、A77/A78、Apple Cyclone 的具体核内变化证据。
- **[第十九轮事务记录](00-project/research-transactions/round-19-2026-10-23.md)** — 本轮完成项、限制与下一步。
- **[第二十轮跨厂商微架构路线与产品化时间 v0.2](03-analysis/移动CPU跨厂商微架构路线与产品化时间-v0.2-2026-10-23.md)** — 比较 Apple、Qualcomm、Samsung、HiSilicon 与 MediaTek 的核设计路线，区分 IP、SoC、终端上市时间。
- **[第二十轮路线/时间审计](02-evidence/audits/round-20-cross-vendor-cpu-route-and-productization-audit-2026-10-23.md)** · [来源卡](02-evidence/sources/round-20-移动CPU跨厂商路线与产品化来源卡.md) · [事务记录](00-project/research-transactions/round-20-2026-10-23.md)。
- **[第二十一轮核内机制证据矩阵 v0.1](03-analysis/移动CPU核内机制证据矩阵-v0.1-2026-10-23.md)** — 逐核比较前端/分支、乱序执行、执行资源、Load/Store、缓存与预取；[机制审计](02-evidence/audits/round-21-mobile-cpu-core-mechanism-evidence-audit-2026-10-23.md)记录指标口径冲突与测量边界；[来源卡](02-evidence/sources/round-21-核内微架构机制原始来源卡.md) · [事务记录](00-project/research-transactions/round-21-2026-10-23.md)。
- **[第二十二轮微架构—LLVM 代码生成桥接矩阵 v0.1](03-analysis/移动CPU微架构与LLVM代码生成桥接矩阵-v0.1-2026-10-23.md)** — 说明目标模型、调度、寄存器分配、向量化、PGO、预取和 SME/ZA 的软件利用路径；[桥接审计](02-evidence/audits/round-22-llvm-hardware-codegen-bridge-audit-2026-10-23.md)与[来源卡](02-evidence/sources/round-22-LLVM代码生成与调度模型原始来源卡.md) · [事务记录](00-project/research-transactions/round-22-2026-10-23.md)。

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

1. 深化[移动 CPU 历史变化时间线 v0.1](03-analysis/移动CPU微架构历史变化时间线-v0.1-2026-10-23.md)，核对每个节点的 IP 公布、SoC 集成和终端上市时间，避免混淆公告与量产。
2. 按[第十九轮来源审计](02-evidence/audits/round-19-cpu-history-timeline-source-audit-2026-10-23.md)补齐 Qualcomm、Apple、Arm IP 与 MediaTek/HiSilicon 的并列历史证据。
3. 定向核验公开可见的取指/译码、乱序执行、分支预测、load/store、寄存器重命名与缓存层次变化；不从跑分猜测未披露实现参数。
4. 每个历史节点明确区分设计者直接说明、跨源支持的解释、合理推论和未知；再基于历史规律延伸 2027–2028 趋势。
5. 全 SoC v1.3 的专家评审 Issue #1 与页面级视觉验收仍是独立交付事项；正式 PPT 继续等待验收后再批量制作。

公开仓不存公司非公开材料或未经授权的第三方全文。
