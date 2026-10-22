# 智能手机 SoC 整体架构演进｜技术洞察知识库

> **当前状态（2026-10-22）：第十五轮已完成跨仓范围核对。** 本仓 v1.3 是全 SoC 系统级报告；Agentic 手机 CPU/LLVM 的既有专项结论已在独立仓结题，应复用而非重启宽泛研究。全 SoC 报告仍待 Issue #1 真实专家评审与用户视觉验收；PPT批量制作暂停。114条唯一来源中86条映射核心Claim、28条未映射；不以机械清零为目标。

仓名 `cpu-microarchitecture-trends` 沿用早期命名；项目研究对象是**智能手机完整 SoC/平台的 2007—2026 年演进及 2027—2028 年有条件前瞻**，并非只研究CPU。覆盖 CPU/GPU/DSP/NPU、ISP/编解码/显示、Modem-RF/天线、缓存/DRAM/互连、软件运行时、常驻感知/安全、电源域/封装/散热。严格区分**裸片、同封装/配套芯片、平台、手机整机和网络环境**。

## 一、最重要的入口

0. **[第十五轮跨仓范围核对与 CPU/LLVM 成果复用](02-evidence/audits/round-15-跨仓范围核对与CPU-LLVM成果复用-2026-10-22.md)** — 明确本仓全 SoC 报告与已结题 Agentic CPU-uArch 专项的分工，避免重复研究。\n0. **[第十四轮结论审计与技术决策闭环](02-evidence/audits/round-14-结论审计与技术决策闭环-2026-10-22.md)** — 将核心结论分为结构信号、系统观察、假设与未知；列出竞争解释、最小验证方式，并指出全SoC报告与详细CPU微架构路线图之间的范围差距。

1. **[当前主报告 v1.3：智能手机 SoC 整体架构演进](05-deliverables/08-智能手机SoC整体架构演进-技术洞察证据收敛版-v1.3.md)** — 在历史/CPU/四任务与系统架构基础上，补HMP发布时间、NNAPI应用API与HAL分层、Tensor ISP/TPU具体功能、Geekerwan及MLPerf测量口径；待专家评审。
2. **[PPT逐页内容设计v0.1（18页候选）](05-deliverables/09-智能手机SoC架构演进-PPT逐页内容设计-v0.1.md)** — 逐页结论标题、叙事桥接、视觉角色、证据ID、边界与备注合同；第04/07/15页三种角色已有可编辑试制。
3. [三页试制与渲染QA记录](02-evidence/audits/round-13-ppt-pilot-qa-2026-10-22.md) — 结构、备注、越界和渲染检查；用户视觉验收待完成。
4. [第十三轮预裁决矩阵与PPT准入清单](02-evidence/audits/round-13-预裁决矩阵与PPT准入清单-2026-10-22.md)。
5. [第十二轮反向审查与技术评审准备](02-evidence/audits/round-12-v1.3-反向审查与技术评审准备-2026-10-22.md)；[GitHub正式评审Issue #1](https://github.com/xjs-work-lab/cpu-microarchitecture-trends/issues/1)。
6. [第十一轮决策性证据收敛与发布闸门](02-evidence/audits/round-11-关键证据收敛与发布闸门-2026-10-21.md)；[第十轮深入审计](02-evidence/audits/round-10-深入内容与正确性审计-2026-10-21.md).
7. **[续研入口](00-project/00-续研入口.md)** — 唯一主问题、进展、限制、下一步；[五个最终研究问题](00-project/01-任务简报.md)。
8. [统一证据台账 CSV（114条唯一记录）](02-evidence/02-证据台账.csv) — 86条已映射核心Claim，28条未映射；记录数不等于独立研究数，也不等于所有来源全文/页码已核。
9. [早期/普及型/华为路线 A01–A07 来源卡](02-evidence/sources/round-10-audit-早期与普及型结构原始来源.md)；[第1–9轮研究索引](01-research/README.md)；[跨负载判断与待证伪问题](03-analysis/跨负载判断与待证伪问题.md)。
10. [v1.2 审计补充版（历史）](05-deliverables/07-智能手机SoC整体架构演进-技术洞察审计补充修订版-v1.2.md)；[v1.1 审计修订版（历史）](05-deliverables/06-智能手机SoC整体架构演进-技术洞察审计修订版-v1.1.md)；[v1.0 原始综合稿（历史）](05-deliverables/05-智能手机SoC整体架构演进-技术洞察终稿-v1.md)。

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

1. 先审阅[第十四轮结论审计](02-evidence/audits/round-14-结论审计与技术决策闭环-2026-10-22.md)，确认当前结论边界与范围缺口。
2. 明确下一阶段要继续收敛全SoC核心Claim，还是单独深化CPU微架构/LLVM优化决策；不要把两种目标混为一谈。
3. 在[GitHub Issue #1](https://github.com/xjs-work-lab/cpu-microarchitecture-trends/issues/1)收集真实专家对EX-01至EX-12的裁决，优先EX-01至EX-04。
4. 仅对可能改变核心判断的Claim做定向补证；不为清空28条未映射来源而无限扩展。
5. PPT批量制作继续暂停，直到研究结论边界与用户希望支持的内部决策层级明确。
6. 若后续需要量化架构收益，必须在固定负载、软件、功耗边界与热环境下做可复现对照。

公开仓不存公司非公开材料或未经授权的第三方全文。
