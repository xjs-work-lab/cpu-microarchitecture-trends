# 智能手机 SoC 整体架构演进｜技术洞察知识库

> **当前状态（2026-10-22）：第十七轮已完成移动 CPU 微架构/LLVM 初始来源筛选。** 官方 LLVM/AAPCS64 来源已提供可核验的 SME/ZA 状态、ABI 与 spill/reload 机制；分支预测论文目前主要是客户端高性能核心证据，手机核心直接覆盖仍不足。全 SoC 报告仍待 Issue #1 真实专家评审与用户视觉验收；PPT批量制作暂停。

仓名 `cpu-microarchitecture-trends` 沿用早期命名；项目研究对象是**智能手机完整 SoC/平台的 2007—2026 年演进及 2027—2028 年有条件前瞻**，并非只研究CPU。覆盖 CPU/GPU/DSP/NPU、ISP/编解码/显示、Modem-RF/天线、缓存/DRAM/互连、软件运行时、常驻感知/安全、电源域/封装/散热。严格区分**裸片、同封装/配套芯片、平台、手机整机和网络环境**。

## 一、最重要的入口

- **[第十七轮 CPU 微架构/LLVM 初始来源筛选](02-evidence/audits/round-17-CPU-uArch-LLVM-initial-seed-discovery-2026-10-22.md)** — 官方 SME/ABI/LLVM 种子、分支预测研究与设备迁移边界。\n- **[CPU 微架构与 LLVM 深化支线：范围锁定与领域地图](00-project/cpu-uarch-llvm-extension-scope-lock-2026-10-22.md)** — 明确通用移动 CPU 核、寄存器/状态、存储层次与 LLVM 代码生成的剩余问题。
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
- [统一证据台账 CSV（114条唯一记录）](02-evidence/02-证据台账.csv) — 86条映射核心 Claim、28条未映射；不等于全文/页码全部核验。
- [早期/普及型/华为路线 A01–A07 来源卡](02-evidence/sources/round-10-audit-早期与普及型结构原始来源.md)；[第1–9轮研究索引](01-research/README.md)；[跨负载判断与待证伪问题](03-analysis/跨负载判断与待证伪问题.md)。
- [v1.2审计补充版（历史）](05-deliverables/07-智能手机SoC整体架构演进-技术洞察审计补充修订版-v1.2.md)；[v1.1审计修订版（历史）](05-deliverables/06-智能手机SoC整体架构演进-技术洞察审计修订版-v1.1.md)；[v1.0原始综合稿（历史）](05-deliverables/05-智能手机SoC整体架构演进-技术洞察终稿-v1.md)。

## 二、目前可以与不可以下的结论

**可以有边界地讨论：** 早期通信/媒体集成、异构CPU与常驻低功耗、专用AI与5G、跨引擎媒体/AI协同、数据/软件与终端电热治理；CPU/GPU/NPU、ISP/媒体、Modem-RF、内存、安全与软件的功能分工；四类负载（4K视频、端侧AI、蜂窝通信、持续游戏）的QoS差异。

**不能宣称已证明：** 某个缓存/NPU/CPU核/互连普遍是首要瓶颈；某个微架构单独带来X% IPC/FPS/续航；所有114条来源都已全文核验；不同手机或不同测试口径可以排出无条件赢家。TOPS、RF dB、发射占空比、3DMark稳定性%和CPU/GPU rail功率不可混用。

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

1. 深读[第十七轮初始来源筛选](02-evidence/audits/round-17-CPU-uArch-LLVM-initial-seed-discovery-2026-10-22.md)中的 LLVM SME/AAPCS64 和分支预测种子，先核实机制、基线与迁移边界。\n2. 按[范围锁定与领域地图](00-project/cpu-uarch-llvm-extension-scope-lock-2026-10-22.md)定向补充 ROB/LSQ、物理寄存器/重命名、移动缓存/预取的原始来源；不重做已结题 Agentic CPU-uArch 的宽泛研究。
2. CPU/LLVM 专项判断复用 [Agentic CPU-uArch 现行技术组合](https://github.com/xjs-work-lab/agentic-CPU-uArch/blob/main/09-roadmap/current.md)与 [Round15F 技术机制审计](https://github.com/xjs-work-lab/agentic-CPU-uArch/blob/main/analysis/engineering/round15f-cpu-llvm-compiler-pressure-2026-10-08.md)。
3. 本仓继续收集 [Issue #1](https://github.com/xjs-work-lab/cpu-microarchitecture-trends/issues/1) 对 EX-01 至 EX-12 的真实专家裁决。
4. 只对可能改变全 SoC 核心判断的 Claim 定向补证；不为清空28条未映射来源而无限扩展。
5. PPT 批量制作继续暂停，直到专家裁决与用户视觉方向确认。
6. 若未来出现会改变 CPU/LLVM 决策的新公开原始证据，再按对应 SSOT 的门槛局部更新。

公开仓不存公司非公开材料或未经授权的第三方全文。
