# 第二十一轮来源卡：核内微架构机制证据（2026-10-23）

**研究模式：** PUBLIC_ONLY  
**用途：** 为逐核机制矩阵提供可追溯的官方手册、厂商工程说明、工业学术论文与第三方逆向来源。  
**证据标签：** [FACT] 来源直接披露；[CLAIM] 厂商的目标/收益声明；[REVERSE] 第三方黑盒逆向或估计；[INFERENCE] 跨来源分析；[UNKNOWN] 公开证据不足。

## SRC21-01 — Arm Cortex-A9：早期部分乱序流水线

- **来源：** [Cortex-A9 Product Support](https://support.arm.com/compute-ip/cortex-a9)；[Cortex-A9 Technical Reference Manual](https://documentation-service.arm.com/static/5e7e23ffb471823cb9de5920)
- **来源类型：** Arm 官方 IP 页面与技术参考手册。
- **[FACT] 可直接支持：** 双发射、部分乱序流水线；取指/分支预测；寄存器重命名；指令队列与推测执行；可选预加载引擎；1–4 核配置。
- **设计意义：** 通过有限的乱序执行与分支预测在移动功耗预算内挖掘指令级并行，而不是单纯依赖频率。
- **边界：** Arm 的 A8→A9 性能百分比是厂商口径；不能当作统一独立测试。A9 的“部分乱序”不可简单与后续大窗口全乱序核等同。

## SRC21-02 — Arm Cortex-A72：解码、调度与访存改进

- **来源：** [Arm：A walk through of the microarchitectural improvements in Cortex-A72](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/a-walk-through-of-the-microarchitectural-improvements-in-cortex-a72)；[Cortex-A72 Software Optimization Guide](https://documentation-service.arm.com/static/5ed75eeeca06a95ce53f93c7)
- **来源类型：** Arm 工程博客与软件优化指南。
- **[FACT] 工程博客直接披露：** 3-wide decode、8-wide issue 描述；更宽的 dispatch 描述（博客称最多 5 个指令/µops 每周期送往执行流水线）；分支预测器改进；I-cache tag lookup、TLB/micro-BTB、寄存器文件功耗优化、commit queue、FP 延迟、load/store buffer、L1/L2 预取与 L2 TLB 改进。
- **重要来源术语/计量歧义：** 软件优化指南“Dispatch Constraints”章节又称从顺序段送入乱序段的 dispatch stage 在其定义和约束下最多处理 3 µops/cycle。工程博客则写作“5 instructions (micro-ops) per cycle”。由于 A77 的官方软件优化指南明确区分每周期处理的 MOP 数和派发的 µOP 数，A72 两份来源可能存在术语使用不精确或阶段定义不同的情况；当前仍无法证明两者指同一计量项。因此不将“5”与“3”视为可比指标，也不裁定哪项错误。
- **[CLAIM] 收益边界：** 同功耗/性能百分比属于 Arm 指定配置和测试口径；不能拆分为某一单独结构的因果贡献。

## SRC21-03 — Arm Cortex-A76：前端解耦与执行资源扩展

- **来源：** [Arm：Cortex-A76—Laptop-Class Performance With Mobile Efficiency](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/cortex-a76-laptop-class-performance-with-mobile-efficiency)；[Cortex-A76 Software Optimization Guide](https://documentation-service.arm.com/static/61c1f57d2183326f217720de)；[Cortex-A76 Core TRM](https://documentation-service.arm.com/static/5e81c5e8c07f701203ad0a9d)
- **来源类型：** Arm 工程博客、软件优化指南、技术参考手册。
- **[FACT] 可直接支持：** 4-wide decode；分支预测与取指解耦；前端每周期可取指 4–8 条；最多 8 个操作每周期 dispatch 到乱序核心；dispatch 时一个 macro-op 可拆分为两个 µops；8 条执行流水线各自可每周期接收/完成一个 µop；整数与 128-bit SIMD/FP 吞吐扩展；第四代预取器与更深的 memory-level parallelism。
- **设计意义：** 更宽的译码/后端供给和前端解耦用于减少指令供给停顿，并在手机面积/功耗约束下增加可利用的并行度。
- **边界：** 4-wide decode、8-op dispatch 和 8 条执行流水线是不同阶段/资源，不能写成“每周期必定执行 8 条架构指令”。Arm 宣称的跨代性能/能效收益还受制程、频率和平台配置影响。

## SRC21-04 — Arm Cortex-A77：前端带宽、乱序窗口与访存并行度

- **来源：** [Arm：New Cortex-A77 CPU continues path towards compute performance leadership](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/new-arm-cortex-a77-provides-compute-performance-leadership)；[Cortex-A77 Software Optimization Guide, Issue 4.0](https://documentation-service.arm.com/static/64adbc3e38511951cb79e6d4?token=)
- **来源类型：** Arm 官方工程博客。
- **[FACT] 直接披露：** 分支预测带宽翻倍；L1 BTB 容量为前代的 4 倍、L2 BTB 增大 33%；新增 Macro-op Cache；dispatch 带宽增加 50%，最多 6 instructions/cycle；乱序窗口扩大 25% 至 160 instructions；整数执行带宽增加 50%；in-flight loads/stores 窗口增加 25%；专用 load-store issue 带宽翻倍；预取器可按内存子系统配置和集群利用率动态调整行为。
- **设计意义：** 同时扩大前端供给、后端窗口和访存并行度，避免只加宽某一段后被其他阶段卡住。
- **边界：** 160 是 Arm 对 out-of-order window 的表述，不在此处重命名为 ROB entries；相对 A76 的百分比属于厂商口径。

## SRC21-05 — Arm Cortex-A78：在相近性能目标下削减低收益结构成本

- **来源：** [Arm：Cortex-A78 CPU—Sustained Performance for Greater Digital Immersion](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/arm-cortex-a78-cpu)；[Cortex-A78 Core TRM](https://documentation-service.arm.com/static/64bea12b38511951cb7a0ee8)
- **来源类型：** Arm 工程博客与非保密 TRM。
- **[FACT] 直接披露：** 改进分支预测带宽/准确率与指令融合；对部分低性能/面积收益结构（包括 L1-I/L1-D 相关结构）及分支预测结构进行面积/功耗优化；TRM 描述动态分支预测、寄存器重命名、issue queues、乱序执行与 L0 Macro-op cache。
- **[CLAIM] 指标：** Arm 报告相对 A77 的单线程性能 +7%、同移动热功耗预算下集群持续性能 +20%，以及特定比较下的面积/功耗效率改善。
- **设计意义：** 设计目标不只是加大所有结构，而是让结构的面积和功耗投入与性能贡献更匹配。
- **边界：** 不应把“优化 L1-I/L1-D 相关结构”误读为所有产品的 L1 容量一定减小；具体配置以相应 TRM/SoC 为准。收益数字不是独立跨手机实测。

## SRC21-06 — Apple Cyclone：宽执行与大乱序窗口的第三方逆向

- **来源：** [AnandTech：Apple’s Cyclone Microarchitecture Detailed](https://www.anandtech.com/show/7910/apples-cyclone-microarchitecture-detailed)
- **来源类型：** 第三方技术逆向分析，2014。
- **[REVERSE] 分析估计：** 峰值 issue width 约 6 µops/cycle；ROB 约 192 µops；4 个整数 ALU、2 个 load/store units、2 个 branch units；64KB L1 I-cache + 64KB L1 D-cache、1MB L2、4MB L3。
- **设计意义：** Cyclone 表明手机 CPU 在较早阶段已探索明显加宽的执行资源和较大的乱序窗口，以提高单线程指令级并行。
- **边界：** Apple 未公开上述内部规格；这些是第三方测量/推导，需保留“估计”属性，不能视为 Apple 官方规格。

## SRC21-07 — Apple Firestorm：现代 Apple 核的黑盒逆向及队列术语问题

- **来源：** [Dougall Johnson：Firestorm Overview](https://dougallj.github.io/applecpu/firestorm.html)；[AnandTech/Tom’s Hardware：A14/M1 深入分析](https://www.anandtech.com/show/16226/apple-silicon-m1-a14-deep-dive/2)
- **来源类型：** 黑盒逆向、指令吞吐/延迟测量与第三方分析。
- **[REVERSE] 直接报告：** Firestorm（A14/M1 高性能核）每周期管线宽度约 8 µops；Dougall Johnson 估计其 coalesced retire queue 约 330 项、rename-retire queue 约 623 项，并报告约 130 个在途 load、约 60 个在途 store。AnandTech 的早期表述曾将约 630 的观测称为 ROB 深度。
- **关键解释边界：** Firestorm 使用不同寻常的 retire-group/coalesced queue 结构；约 623 的 rename-retire queue 不能直接等同传统 ROB entries。不同分析者的命名和测量模型不完全一致，故不能把 Cyclone 的“192 ROB”与 Firestorm 的“623”当成严格同口径的 ROB 代际对比。
- **限制：** 逆向资料作者明确承认其结果可能存在错误；应使用方法、测试代码与术语边界，不把估计当作官方事实。

## SRC21-08 — Samsung Exynos M1–M6：跨代微架构工程论文

- **来源：** [Evolution of the Samsung Exynos CPU Microarchitecture, ISCA 2020 / IEEE DOI 10.1109/ISCA45697.2020.00015](https://ieeexplore.ieee.org/document/9138988/)；[作者公开 PDF](https://people.engr.tamu.edu/djimenez/pdfs/exynos_isca2020.pdf)
- **来源类型：** ISCA 2020 Industry Track 论文；作者在描述的项目期间供职于 Samsung SARC。
- **[FACT] 论文明确披露：**
  - M1 每周期供给约 4 条指令/µops，M3 增至 6；M5 增加 384-µop micro-operation cache（UOC），最多每周期供给 6 µops，以在可预测、可复用的代码段中减少取指/译码功耗。
  - 分支预测路线使用 scaled hashed perceptron；小型 µBTB 与本地历史预测用于常见零气泡路径，主 BTB/预测器处理更复杂情况。
  - M3 及之后引入 L1.5 Data TLB；M3 及更新核心以物理寄存器文件方式重命名，支持零周期整数寄存器间 move 的重命名映射；M4 及以后有 load-load cascading，可使特定 load 链的有效延迟达到 3 cycles。
  - L1 D-cache 从 M1 的 32KB 增至 M3 的 64KB、M6 的 128KB；在途 miss 从 M1 的 8 个增至 M3 的 12、M4 的 32、M6 的 40。
  - L2/L3 配置：M1/M2 为 2MB L2、无 L3；M3 为 512KB L2 + 4MB L3；M4 为 1MB L2 + 3MB L3；M5 为 2MB L2 + 3MB L3；M6 为 2MB L2 + 4MB L3。
  - M3 加入 spatial memory stream prefetcher；预取器有动态 degree、确认机制和 one-pass/two-pass 等策略，以平衡及时性、带宽、miss-buffer 压力和缓存污染。
  - 论文的平均 load latency 从 M1 的 14.9 cycles 降到 M6 的 8.3 cycles；所有核心模拟统一运行在 2.6GHz，使用 4,026 条 workload traces。
- **重要方法边界：** 论文明确说明结果基于 trace-driven cycle-accurate model，而非全代际硅片对比；M5/M6 硅片在论文编写时不可用。M6 属于未来工作/建模对象，不能称为手机中实测的量产核数据。作者与所述 SARC 项目有直接工作关系，属于工程披露，不是完全独立团队的复现。

## SRC21-09 — Qualcomm Krait/Oryon 与 HiSilicon Taishan：公开结构披露边界

- **来源：** [Qualcomm Krait 公告](https://www.qualcomm.com/news/releases/2011/02/qualcomm-announces-next-generation-snapdragon-mobile-chipset-family)；[Qualcomm Oryon 官方产品页](https://www.qualcomm.com/processors/oryon)；[Kirin 9000S 第三方裸片分析](https://www.tomshardware.com/news/die-shot-of-hisilicons-sanction-busting-kirin-9000s-chip-revealed)
- **来源类型：** 厂商产品资料与第三方反向识别。
- **[FACT] 可支持：** Krait 和 Oryon 是 Qualcomm 不同阶段的 CPU 路线；Kirin 9000S 的 Taishan 核有第三方分析线索。
- **[UNKNOWN] 不足以公开确认：** 对 Krait/Oryon/Taishan 的所有代际，公开资料没有形成统一、可比的前端宽度、ROB/LSQ、物理寄存器数量、预测器表结构、执行端口与各结构功耗数据表。
- **使用规则：** 不从峰值性能、IPC 或跑分倒推未披露的核内结构。缺少公开资料表示“未公开证据”，不是“内部没有该机制”。

## 总体来源使用规则

1. 核内结构、设计目标、性能收益分别记录；同一篇厂商博客不能自动独立证明三者之间的因果。
2. 区分 fetch/decode/rename/dispatch/issue/execute/retire；一个来源中的“width”不自动等于另一来源中的同名字段。
3. 对第三方逆向保留估计、工具、测试方法和作者自述限制。
4. 对 Samsung M1–M6 论文区分实际产品代际与模拟对象；所有性能数字需保留统一 2.6GHz 与 workload traces 的方法上下文。
5. 不以核心数量、频率、跑分或单一 ROB 估计给厂商作排名。
