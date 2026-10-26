# 第25轮来源卡 A｜Samsung Exynos M1–M5/M6 直接工程披露

**日期**：2026-10-26　**用途**：为移动 CPU 历史因果解释提供可核查的设计者原话、结构指标、方法边界；并非手机实测。**模式**：PUBLIC_ONLY。

## S25-01｜ISCA 2020 原始工业论文（重点）

- **题名**：Brian Grayson 等，*Evolution of the Samsung Exynos CPU Microarchitecture*，ISCA 2020 Industry Track，DOI [10.1109/ISCA45697.2020.00015](https://doi.org/10.1109/ISCA45697.2020.00015)；[IEEE记录](https://ieeexplore.ieee.org/document/9138988/)；[作者公开 PDF](https://people.engr.tamu.edu/djimenez/pdfs/exynos_isca2020.pdf)。
- **作者与独立性**：论文注明全体作者都曾参与 Samsung Austin Research & Design Center（SARC）相应开发工作；属第一手工业工程披露，但不是无利益相关的外部复现实验。
- **Methodology，第1页（PDF第1页）**：模拟采用 4,026 条来自 SPEC、网页、移动 benchmark、游戏及应用的 traces；多数负载 SimPoint 10M 指令 warmup、后续 100M 详细模拟；各代统一 2.6GHz；以 trace-driven cycle-accurate performance model 比较。论文写明制作模拟时 M5/M6 silicon 不可用，所以结果**不能叫量产硅片跨代实测**。M1–M5 为产品化代际，M6 为完成设计/未来工作（论文口径）。
- **Table I，PDF第3页**（以下为原表结构指标，不是来自真实手机的测量结果）：

| 项目 | M1 | M2 | M3 | M4 | M5 | M6（未来设计/模拟对象） |
|---|---:|---:|---:|---:|---:|---:|
| Dec/Ren/Ret width（µops/cycle 表中宽度） | 4 | 4 | 6 | 6 | 6 | 8 |
| ROB size | 96 | 100 | 228 | 228 | 228 | 256 |
| Integer PRF entries | 96 | 96 | 192 | 192 | 192 | 224 |
| FP PRF entries | 96 | 96 | 192 | 176 | 176 | 224 |
| L1D容量 | 32KB | 32KB | 64KB | 64KB | 64KB | 128KB |
| L2容量 | 2MB | 2MB | 512KB | 1MB | 2MB | 2MB |
| L3容量 | 无 | 无 | 4MB | 3MB | 3MB | 4MB |

**关键限制**：M3 将4核共享L2调整为私有L2并新增L3，M4集群缩小又重配L3；缓存大小变化不能只解读为“资源越大越好”。Dec/Ren/Ret 是论文明确表项，不能与 Apple reverse 的 issue width 或 retire queue 按数字直接排名。

## 机制层证据

| ID | 原文位置 | [FACT] / [CLAIM] | 可用历史动因及边界 |
|---|---|---|---|
| S25-02 | ISCA Sec. IV.A/B（PDF第2–4页） | Samsung 以 scaled-hashed perceptron + 多级BTB/µBTB设计分支预测；早期 small loop 对 taken-branch 气泡敏感；用zero-bubble µBTB缓解 | **设计者直接说明**短循环/基本块多的前端瓶颈。没有量产设备级独立收益测量 |
| S25-03 | ISCA Sec. IV.C（PDF第4页） | M3从4-wide扩至6-wide且OOO窗口加大，需要提高预测吞吐；改进µBTB与SHP/L2BTB | **有直接因果叙述**：“宽前/后端→预测路径要跟上”。单代结构收益不等于应用FPS收益 |
| S25-04 | ISCA Sec. IV.D/E（PDF第4页） | M4关注更大代码工作集，扩L2BTB；M5对空BTB行优化以及often-taken/always-taken分支快速转向 | **直接动因**：更大的web工作集与无效前端访问。论文称M4相关更改对BBench模拟有2.8% isolated improvement，不是手机硅片全应用增益 |
| S25-05 | ISCA Sec. V（PDF第6–7页） | 针对Spectre v2安全场景，讨论BTB/RAS目标的context-dependent hashing及scrambling | **安全约束成为微架构一阶条件**，但论文特定威胁模型/模拟方案不能自动视作每款M5手机均启用或已被独立证明安全 |
| S25-06 | ISCA Sec. VI（PDF第7–8页） | M5添加384-µop UOC、最多6 µops/cycle，Filter→Build→Fetch模式。Fetch可关闭I-cache/译码，预测充分可靠时还可停用mBTB | **设计者明确说明**主要目的是可重复热点kernel的fetch/decode节能；有容量、命中预测、建立成本；不得推断UOC单独节省全机X%瓦数 |
| S25-07 | ISCA Sec. VII（PDF第8–9页） | 多步长与SMS空间流预取、按确认信息动态调整prefetch degree、one-pass/two-pass及缓冲队列控制 | 论文直接指出过量预取造成带宽、cache容量、功耗浪费；**精度/时效/资源**是必须同时权衡的目标 |
| S25-08 | ISCA Sec. IX–X（PDF第10–11页） | M4 memory return fast-path bypass部分互连路径/时钟域 crossing；M5 latency-critical speculative cache lookup bypass、early DRAM page activate | **瓶颈不只在L1/L2**：CPU到DRAM的电压频率域与互连返回路径也影响访问延迟。更早激活/读预测有额外访问功耗，论文设置取消/校正保护 |
| S25-09 | ISCA Table IV（PDF第11页） | 平均load latency：M1→M6 为14.9→8.3 cycles；模拟同频，含cache、prefetch、旁路、其他变化的合计结果 | [MODEL_RESULT] 不可作为实机内存延迟，不可归因于任一单结构，不可与Apple负载或计量单元直接比较 |
| S25-10 | ISCA Sec. XI（PDF第11页） | 作者在统一trace模型中概述：low-IPC多受cache/prefetch影响；medium-IPC受预测/缓存/资源影响；high-IPC原被4-wide限制，M3+扩为6-wide | [AUTHOR_INTERPRETATION] 在论文该模型与负载集内成立；不同手机软件/温度/平台未受控 |

## S25-11｜IEEE Micro 2019：M3原始论文（第二设计者来源）

- Jeff Rupley、Brad Burgess、Brian Grayson、Gerald D. Zuraski Jr.，*Samsung M3 Processor*，IEEE Micro 39(2):37–44，2019，DOI [10.1109/MM.2019.2897556](https://doi.org/10.1109/MM.2019.2897556)；[作者论文主页](https://geraldzuraskijr.com/publications)。
- **已核的原始论文首页/公开摘要**：M3目标是提升一组广泛负载的IPC、在约束下不牺牲此前频率；优先 power efficiency 而非绝对power最小，允许在有足够性能收益时增加面积；6-wide/更深乱序资源。
- **限制**：该论文的可下载版本本轮检索到作者链接，但网页文档无法完整打开核对后续页；上述只归为已见摘要/首页信息，不能冒称已完成IEEE Micro 8页逐页全文复核。与ISCA 2020存在重合作者，不算独立外部重复验证。

## S25-12｜产品化与项目终止（不能替代技术机制证据）

- [Samsung Exynos 990官方产品页](https://semiconductor.samsung.com/processor/mobile-processor/exynos-990/)：2019–2020代手机平台仍有第5代自研CPU核并配Cortex-A76/A55（产品事实，不是ISM/仿真研究的“硅片实验结果”）。
- [Yonhap 2019-11-05](https://m-en.yna.co.kr/view/AEN20191105001800320)：Samsung停止美国自研CPU核开发，涉及团队调整；引用企业“focus on core competitiveness and improve efficiency”。
- [Reuters报道及Samsung表态，2019-11-05](https://www.investing.com/news/stock-market-news/samsung-says-to-shut-down-us-cpu-research-division-2011925)：Samsung退出的是custom CPU项目，Exynos业务继续。公开报道未提供可分解到预测器/缓存/流水线的因果结论；**禁止**断言“因为M3/M5某项IPC或能效失败才终止”。

## 资料等级与写法规则

- **A**（高直接度）：原论文已明确的设计目标和结构/方法；不自动推成设备收益。
- **B**（厂商模型）：在4,026 traces、2.6GHz下的模拟IPC/延迟/MPKI；不得称为硅片表现。
- **C**（分析推论）：将Samsung与Apple路径解释为“资源供给与实际使用的协调”；这是研究者整合，不是某厂商承认其路线不同。
- **D**（未知）：相同手机工作负载、同工艺热功率边界的两家能效差、项目结束内部决策权衡；保留UNKNOWN。
