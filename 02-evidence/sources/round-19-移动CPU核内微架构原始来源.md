# 第十九轮来源卡：移动 CPU 核内微架构原始资料（2026-10-23）

**用途：** 为移动 CPU 历史时间线补充可直接核验的核内变化资料，重点关注乱序执行、分支预测、前端供给、寄存器/队列、预取和内存级并行。  
**边界：** 厂商工程博客和技术参考手册能证明公开披露的设计特征与设计目标，但厂商给出的百分比不等于独立可比结果；第三方逆向必须另行标注。

| ID | 来源与日期 | 公开资料直接支持的内容 | 设计动因／历史意义 | 限制 |
|---|---|---|---|---|
| C19-01 | [Arm：Cortex-A9 的诞生与演进](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/the-birth-evolution-of-cortex-a9-and-what-s-coming-next)，2013 回顾 2007 年设计 | Cortex-A9 部分乱序流水线；MPCore 可扩展至四核；硬件缓存一致性管理；Arm 声称相对 A8 提升 IPC | 在移动功耗限制下，一边提升单核指令级并行，一边探索多核吞吐扩展 | IPC 百分比来自 Arm 回顾，不是统一独立基准；不能代表所有工作负载 |
| C19-02 | [Qualcomm：Krait 新一代 Snapdragon CPU 微架构](https://www.qualcomm.com/news/releases/2011/02/qualcomm-announces-next-generation-snapdragon-mobile-chipset-family)，2011 | Qualcomm 公布 Krait 微架构，并提供单核、双核、四核产品配置；同期平台结合 GPU、连接和其他引擎 | 表明移动 CPU 不只有 Arm Cortex IP 一条路线，SoC 厂商也以自有 CPU 微架构进行性能/能效差异化 | Qualcomm 的“性能+150%、功耗−65%”是厂商自报比较；未提供统一第三方对照 |
| C19-03 | [Arm：Cortex-A72 核内微架构改进详解](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/a-walk-through-of-the-microarchitectural-improvements-in-cortex-a72)，2015 | 3-wide decode/8-wide issue、最多 5-wide dispatch；更新的分支预测器；I-cache tag lookup、TLB/micro-BTB、寄存器文件、commit queue、FP 延迟、load/store buffer、L1/L2 预取与 L2 TLB 优化 | Arm 明确指出手机受热预算约束，单纯提高频率或发射宽度不够；必须通过多处微架构优化提高给定功耗下的性能 | “超过 50% 内存带宽”等数字是 Arm 的指定测试/配置口径；不能直接外推到所有 SoC |
| C19-04 | [Arm：Cortex-A76 核内微架构详解](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/cortex-a76-laptop-class-performance-with-mobile-efficiency)，2018 | 4-wide decode；前端取指 4–8 条/周期；分支预测与取指解耦；最多 8 个操作/周期 dispatch；更高整数/SIMD吞吐；更先进预取和 memory-level parallelism | 明确从 A72/A57 的 3-wide decode 向更宽前端演进，降低前端供给瓶颈，并在移动功耗/面积约束下提高 IPC | 跨代性能数字同时受工艺、频率和目标配置影响；不能将全部增益归因于某一个结构 |
| C19-05 | [Arm：Cortex-A77 微架构说明](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/new-arm-cortex-a77-provides-compute-performance-leadership)，2019 | 新增 Macro-op Cache；提高分支预测带宽/准确率和 BTB 容量；增加乱序后端吞吐与窗口能力 | 缓存已解码宏操作可以降低重复解码成本，改善前端延迟与后端供给；反映核心持续向更宽前端和更高指令吞吐发展 | 公开数字来自 Arm 对该 IP 的描述；不证明每个应用都能命中 MOP cache 或获得同等收益 |
| C19-06 | [Arm：Cortex-A78 微架构说明](https://developer.arm.com/community/arm-community-blogs/b/architectures-and-processors-blog/posts/arm-cortex-a78-cpu)，2020 | 通过分支预测、指令融合和结构面积/功耗优化提高性能效率；Arm 报告相对 A77 在同一移动热功耗预算下持续性能提升 | 设计重点明确转向持续性能：不只优化峰值吞吐，也要在手机有限散热条件下减少功耗和热降频 | “持续性能 +20%”是 Arm 指定比较口径，非独立跨手机测量 |
| C19-07 | [Arm Cortex-A78 Core Technical Reference Manual](https://documentation-service.arm.com/static/64bea12b38511951cb7a0ee8)，Issue 09（2023） | 官方 TRM 说明指令取指、动态分支预测、1.5K-entry L0 Macro-OP cache、寄存器重命名、issue queues 和 out-of-order execution | 展示某些微架构组件可通过非保密技术参考手册核验；可把概念级时间线深化到软件可见机制 | TRM 仅描述 A78，不自动证明前后代之间的全部变化；具体实现选项仍需按文档/SoC配置核对 |
| C19-08 | [AnandTech：Apple Cyclone 微架构拆解](https://www.anandtech.com/show/7910/apples-cyclone-microarchitecture-detailed)，2014 | 第三方逆向估计 A7/Cyclone 的 issue width、ROB、执行资源和缓存结构明显不同于前代 Swift | 说明手机 CPU 曾出现强调宽执行和大乱序窗口的高单线程设计路线 | 不是 Apple 官方规格；ROB/宽度数值应作为逆向估计而非确定事实 |

## 使用规则

1. 先用官方来源记录结构事实与厂商自述设计目标。
2. 再用独立论文、逆向分析或终端测量补足官方未披露部分，并保留其方法和不确定性。
3. 不把同一厂商的跨代宣传百分比拼成跨厂商排名。
4. 不由 IPC/跑分反推未公开的 ROB/LSQ、物理寄存器数、预测器内部结构或每个结构的功耗。
5. 对每个变化点保留“变化前状态—变化后状态—为什么改—带来什么—代价/新瓶颈—证据强度”的链条。
