# 分析推论

## 当前研究主线（2026-10-26）

当前优先任务不是提出新技术立项建议，而是复盘移动 CPU 历史变化、解释动因和后果。

- **[第27轮五问题×时间×模块×厂商覆盖矩阵](全SoC-移动CPU历史演进五问题覆盖矩阵-v0.1-2026-10-26.md)**：将第19—26轮CPU深化与v1.3全SoC五问对齐；判断哪些能进入研究侧定性结论收敛，哪些要保持未知/阻断跨厂商定量归因。[六条历史结论阅读稿](移动SoC-CPU历史结论收敛草案-v0.1-2026-10-26.md) · [反例/证据卫生审计](../02-evidence/audits/round-27-五问题覆盖-证据卫生-因果反例审计-2026-10-26.md)。

- **[第26轮Apple A8—A13代际机制与因果链](Apple-A8-A13-代际机制与因果链-v0.1-2026-10-26.md)**：从Cyclone到Firestorm中间六代，揭示6-wide大核改良、A10→A11异构六核并发、A12 E核OoO、A13缓存与调度/DVFS的共同演进。[来源卡](../02-evidence/sources/round-26-apple-a8-a13-primary-and-reverse-sources-2026-10-26.md)、[审计](../02-evidence/audits/round-26-apple-a8-a13-lineage-claim-audit-2026-10-26.md)；A10/A11核内隐藏参数和单因素能耗未证。


- **[第25轮 Apple Cyclone/Firestorm vs Samsung Exynos M1–M5机制因果对照](Apple-Cyclone-Firestorm-vs-Samsung-M1-M5-微架构因果比较-v0.1-2026-10-26.md)**：工业设计者第一手动因与Apple独立黑盒逆向并列，区分核内宽度、退休队列、负载、预取及SoC访存。配套[逐项审计](../02-evidence/audits/round-25-apple-samsung-mechanism-causal-audit-2026-10-26.md)；仍不支持跨厂商同条件IPC/能耗比较。

- **[第24轮核心组合分化与能效因果对照 v0.1](移动CPU核心组合分化与能效驱动因果对照-v0.1-2026-10-26.md)**：区分Apple P/E、MediaTek全大核、Qualcomm Oryon及2026 C2的微架构类别/频率档；每项注明动机、机制推论、混杂因素与未知。配套[来源卡](../02-evidence/sources/round-24-多层核心组合路线原始来源卡-2026-10-26.md)和[审计](../02-evidence/audits/round-24-core-topology-causal-audit-2026-10-26.md)。

- **[第二十一轮核内机制证据矩阵 v0.1](移动CPU核内机制证据矩阵-v0.1-2026-10-23.md)**：逐核归一前端、分支预测、乱序执行、执行资源、Load/Store、缓存和预取；边界见[机制审计](../02-evidence/audits/round-21-mobile-cpu-core-mechanism-evidence-audit-2026-10-23.md)，原始来源见[第二十一轮来源卡](../02-evidence/sources/round-21-核内微架构机制原始来源卡.md)。
- **[第二十二轮微架构—LLVM 代码生成桥接矩阵 v0.1](移动CPU微架构与LLVM代码生成桥接矩阵-v0.1-2026-10-23.md)**：把硬件机制连接到 LLVM 的目标模型、调度、寄存器分配、向量化、PGO、prefetch 与 SME/ZA lowering；边界见[桥接审计](../02-evidence/audits/round-22-llvm-hardware-codegen-bridge-audit-2026-10-23.md)，原始资料见[第二十二轮来源卡](../02-evidence/sources/round-22-LLVM代码生成与调度模型原始来源卡.md)。已建立[移动 CPU 微架构历史变化时间线 v0.1](移动CPU微架构历史变化时间线-v0.1-2026-10-23.md)，对应的[初始来源审计](../02-evidence/audits/round-19-cpu-history-timeline-source-audit-2026-10-23.md)列出来源与外推边界。 核内细节见[第十九轮来源卡](../02-evidence/sources/round-19-移动CPU核内微架构原始来源.md)。 跨厂商路线和 IP→SoC→终端时间链见[第二十轮分析](移动CPU跨厂商微架构路线与产品化时间-v0.2-2026-10-23.md)，逐项审计见[第二十轮审计](../02-evidence/audits/round-20-cross-vendor-cpu-route-and-productization-audit-2026-10-23.md)。范围和方法见[历史演进与因果分析框架](../00-project/cpu-uarch-llvm-extension-scope-lock-2026-10-22.md)，目标校正见[第十八轮事务](../00-project/research-transactions/round-18-2026-10-23.md)，第十九轮事务记录见[事务19](../00-project/research-transactions/round-19-2026-10-23.md)，第二十轮记录见[事务20](../00-project/research-transactions/round-20-2026-10-23.md)，当前轮记录见[事务21](../00-project/research-transactions/round-21-2026-10-23.md)。


**第十七轮初始来源筛选（辅助机制来源）：** [CPU 微架构/LLVM Seed Discovery](../02-evidence/audits/round-17-CPU-uArch-LLVM-initial-seed-discovery-2026-10-22.md)。这些资料应放回历史节点解释软硬件关系，不作为当前研究主线。

**历史因果框架：** [移动 CPU 微架构历史演进与 LLVM 机制深化](../00-project/cpu-uarch-llvm-extension-scope-lock-2026-10-22.md)。当前重点是历史变化点、动因、收益/代价与瓶颈转移，不是新的技术立项筛选。


**跨项目 CPU/LLVM 专项入口：** [Agentic CPU-uArch 现行技术组合](https://github.com/xjs-work-lab/agentic-CPU-uArch/blob/main/09-roadmap/current.md) · [Round15F CPU/LLVM机制审计](https://github.com/xjs-work-lab/agentic-CPU-uArch/blob/main/analysis/engineering/round15f-cpu-llvm-compiler-pressure-2026-10-08.md)。该项目已在公开证据范围内结题；本仓只引用，不复制其证据对象或重启宽泛研究。


**当前结论审计入口：** [第十四轮结论审计与技术决策闭环](../02-evidence/audits/round-14-结论审计与技术决策闭环-2026-10-22.md)。该文基于现有SSOT将K01–K10分为结构信号、系统观察、假设与未知，并列出竞争解释、可用表述和下一步判别方式。

[跨负载判断及待证伪问题](跨负载判断与待证伪问题.md)：当前唯一综合推论入口；区别于[原始来源证据](../02-evidence/README.md)和[正式交付](../05-deliverables/README.md)。


[当前技术洞察审计修订版 v1.1](../05-deliverables/06-智能手机SoC整体架构演进-技术洞察审计修订版-v1.1.md)和[深入正确性审计](../02-evidence/audits/round-10-深入内容与正确性审计-2026-10-21.md)优先于此处第九轮的阶段性判断；旧推论仍可追溯。

当前需优先阅读[第十一轮证据闸门](../02-evidence/audits/round-11-关键证据收敛与发布闸门-2026-10-21.md)及[主报告v1.3](../05-deliverables/08-智能手机SoC整体架构演进-技术洞察证据收敛版-v1.3.md)；此处第九轮判断是过程存档。

**第十二轮（2026-10-22）：** [v1.3反向审查与技术评审准备清单](../02-evidence/audits/round-12-v1.3-反向审查与技术评审准备-2026-10-22.md)；[正式技术评审Issue #1](https://github.com/xjs-work-lab/cpu-microarchitecture-trends/issues/1)。