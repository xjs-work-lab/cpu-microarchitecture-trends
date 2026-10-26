# 第25轮分析｜Apple Cyclone/Firestorm 与 Samsung Exynos M1–M5 微架构因果对照 v0.1

**日期**：2026-10-26。**范围**：移动CPU的历史设计取舍、负载/约束与可解释机制；不做性能排名、未来立项，不将M6视作量产代际，不以M1测试代替iPhone A14测量。具体原始证据仅在[Samsung来源卡](../02-evidence/sources/round-25-samsung-m1-m5-engineering-paper-2026-10-26.md)、[Apple来源卡](../02-evidence/sources/round-25-apple-cyclone-firestorm-reverse-evidence-2026-10-26.md)维护。

## 1. 结论概览

1. **[B/OBSERVATION] 两条路线都包含宽执行/深乱序窗口和访存/预测优化；不应误读为Apple只加宽、Samsung只做节能。** Apple Cyclone及Firestorm的公开剖析以黑盒测试和代码线索为主，Samsung ISCA文给出持续七/八年设计团队的第一手解释。
2. **[A/作者动机] Samsung M3的设计者明确把广泛负载IPC、频率保持、能效及可接受的面积增长作为权衡目标；M5 UOC明确针对热点代码重复解码的功耗。** 这是“为何做”的直接证据。
3. **[B/C] Apple 2013 Cyclone大幅提高单线程并行资源，2020 Firestorm仍呈现非常大的并行、队列与访存资源；但无法仅凭两份逆向报告精确证明每代因果连续性，也不能直接认定真实手机净功率/IPC增益。**
4. **[A/结构与作者动机] Samsung近年的关键变化从核内发射宽度扩展到低功耗指令供给、可预测分支快速路径、自适应预取和多时钟域/DRAM返回延迟控制，说明“瓶颈缓解”跨越CPU核与SoC内存系统。**
5. **[高可信事实/内部原因未知] Samsung于2019年停止美国自研CPU项目，但Exynos平台持续；不能把项目停止解释为M5某一项微架构机制失败的定量证据。**

## 2. 横向矩阵：相同问题、不同证据

| 问题/资源 | Apple Cyclone A7（2013） | Apple Firestorm A14/M1代（2020） | Samsung Exynos M1→M5（2016–2020） | 因果解释与可比性 |
|---|---|---|---|---|
| 前端供给 | 第三方称约6 µops/cycle的decode/issue/retire | M1黑盒观察8 µops/cycle的pipeline约束；执行issue有不同计数口径 | M1 4→M3 6（论文表Dec/Ren/Ret）；M5 384 µop UOC作为可选路径 | 扩宽只是提高能力上限，必须匹配预测、cache和后端；宽度口径不相同，**不可直接跨厂商排行** |
| 分支/短循环 | 第三方估分支单元、mis-predict代价，原始动机未披露 | 黑盒报告融合/elimination细节；预测器容量与算法公开不足 | SHP+µBTB/mBTB/L2BTB；M3随扩宽提升预测吞吐，M4关注大工作集、M5零气泡重定向与空行节能 | **Samsung可直接证明设计者想缓解什么；Apple只能做机制解释**。不存在证据说Apple不做类似预测技术 |
| 乱序/寄存器 | AnandTech估约192项ROB，另有LLVM公开提交线索 | ~330 coalesced retire groups + ~623 rename-retire entries，由Dougall反推 | Samsung表ROB M1 96→M3/M5 228、Integer PRF 96→192，M3起rename remapping可零周期整数move | Apple的“623”不是普通ROB，Apple两核都不能与Samsung ROB表直接相比；前后年代也不同 |
| 执行单元 | 估计4整数ALU、2 load/store单元等 | M1逆向列多条整数/访存/SIMD执行管线及fusion/elimination | M3同时增加decode/retire width、ROB、PRF、访存/FP资源；M4之后做不同延迟细节优化 | 都不是“只加宽”；是否真实能被workload用满要有受控应用分析 |
| 数据预取/缓存 | 第三方给L1 I/D 64KB等缓存估计 | M1逆向见~130在途load、~60 store；部分load→load 3cycle特例 | M3 L1D 64KB、新L1.5 DTLB和3级缓存；预取动态degree/SMS与确认队列；M4/M5 DRAM返回/预测旁路 | Samsung论文提供明确“避免滥预取浪费功耗/带宽”“节省跨域返回延迟”的动机；Apple在途队列规模不是性能归因 |
| 功耗/热权衡 | AnandTech评论race-to-sleep，但非Apple内部目标文件 | A14/iPhone12第三方整机评测显示功耗/性能变化同时伴随5nm制程 | M3文直接陈述 power efficiency > absolute power；M5 UOC可关闭常规decode、部分预测路径 | 不能据此说Samsung架构更省电或Apple只追求速度；必须解耦制程/频率/OS/应用 |
| 证据形式 | 2014年技术作者的黑盒＋源码线索 | 2020/21技术作者的黑盒性能计数器与实验表，主要M1载体 | 工业论文Table I及4,026 traces/2.6GHz模型，属作者直接工程披露 | 一个是**观测微结构**，一个是**设计者机制+模拟**，不是同负载、同环境对照 |

## 3. 形成了哪些较强的“变化→动因”链

| ID | 受约束的历史问题/前代限制 | 实际设计动作 | 为什么可能有效 | 证据层级与反例 |
|---|---|---|---|---|
| C25-01 Samsung M1→M3 | M1 4-wide限制高IPC负载；扩大乱序资源后需提升分支供给 | M3 6-wide、ROB 100→228、PRF扩展、µBTB/L2BTB变化 | 同步增强指令供给、并行窗口与预测，使后端不易断粮 | **A直接陈述/工业论文模型**，实机比例未知；大窗口未必适合全负载 |
| C25-02 Samsung M3→M4 | 实际网页/代码工作集扩大，预测表容量不够 | L2BTB再次扩容、低延迟/高带宽填充 | 大工作集减少预测目标错失、降低转向等待 | **A设计者动机**；BBench 2.8% isolation是论文口径，不能当任意手机收益 |
| C25-03 Samsung M4→M5 | 频繁重复热点kernel的decode/取指活动功耗 | 384 µop UOC + Filter/Build/Fetch，有利时关闭I-cache/decode | 对高度可重复路径减少重复译码切换与预测访问 | **A直接动机+结构**；UOC的面积/训练/错误路径开销未知，整体功耗净收益未分解 |
| C25-04 Samsung预取演进 | DRAM延迟难隐藏，盲目高预取度占满miss buffer、浪费带宽/功耗 | 多步长、SMS、基于命中确认调动态degree、one/two-pass | 高置信时激进、低置信克制；减少晚到/无效预取 | **A直接设计描述**；效果依赖工作集、cache命中、互连及DRAM |
| C25-05 Samsung M4/M5系统返回路径 | 多电压/频率域的异步跨越和cache/互连返回路径抬高load延迟 | M4 fast DRAM return; M5 speculative read bypass、early page activate | 为关键读减少跨域/排队等待；错误投机时取消请求控带宽 | **A直接工程说明/B模型整体结果**，M1→M6 load14.9→8.3含众多变化，不可分给此项 |
| C25-06 Apple Cyclone | 需要提高手机单线程吞吐的时代背景 | 大幅增加发行/执行及在途资源（逆向/提交线索） | 利用更大ILP/MLP，增加瞬时完成工作能力 | **B结构、C动机推断**；文中race-to-sleep只是评论，并无Apple内部成本数据 |
| C25-07 Apple Firestorm | 2020代继续追求高IPC/复杂流水线能力 | M1逆向8-wide、融合/消除、非传统退休队列与大在途load/store | 能将部分命令从执行端口卸载、增加依赖隐藏机会 | **B逆向结构/C因果推论**，630“ROB”术语冲突且A14/M1设备不同 |

## 4. 不是“谁更大”，而是“资源为什么值得开销”

- **利用率优先于名义峰值**：宽核增加了decode、rename、PRF、队列、cache和执行端口的面积/动态功耗，却只有在预测准确、代码有独立操作、内存及时供给时带来吞吐。上述是一般机制逻辑，不是厂商亲自披露的跨家厂策略。
- **预测机制同时影响功率**：Samsung µBTB的高置信路径可关闭其他预测活动；UOC不仅缓存µops，还会根据代码段稳定性切换运行模式；因此“减少不必要活动”与“供足宽核”可以同时成立。
- **访存效率需要跨层协作**：更大的ROB不一定解除实际DRAM stall；Samsung将M4/M5的延迟关键路径优化延伸至cache、互连、电源域和控制器，证明微架构演进已超出单CPU核逻辑。
- **资源参数有不同语义**：Samsung公开的ROB确系Table I相同口径；Apple Firestorm实验的coalesced group与rename-retire是独立资源，不能和Apple早期单一ROB值连成线性数值图。
- **安全需求进入预测器演进**：Samsung论文明确回应Spectre v2威胁模型，这是“不只是跑分/能耗”的典型约束变化；不代表本文防护对全部手机有效或具备完备安全证明。

## 5. Apple/Samsung差异的最强反例与不确定性

| 诱人的判断 | 为什么不能成立 | 当前可讲的替代版本 |
|---|---|---|
| “Apple以大ROB换性能，Samsung靠小ROB做功耗” | Firestorm的623非传统ROB；Samsung M3 ROB从100增加到228，同时扩大执行资源 | 两家均扩大并行资源，但**公开结构定义和年代不等价** |
| “Samsung M5加入UOC说明Apple前端不重视省电” | Apple未公开同样的微功耗路径，并不等于不存在；Firestorm已有fusion/elimination逆向 | Samsung明确公开了UOC省电动机，Apple相关具体门控/能耗归因未知 |
| “三星退出是因自研微架构设计失败” | 2019企业声明只确认组织调整/业务竞争，不提供M5具体设计失败的机制证据 | 自研核路线并非必然持续，经济/产品系统竞争也是长期演进约束；具体原因不可确定 |
| “Samsung模拟IPC增益可以和Apple手机跑分比较” | 4,026 traces、2.6GHz模型 vs 真机跨制程/不同OS/编译器/热控制 | 只能分别叙述各自证据，不能给跨厂商IPC/W排名 |
| “2013 Cyclone→2020 Firestorm已证实每代ROB等比例扩展” | 仅两节点、不同测量方法，Firestorm不同队列定义 | 早期宽核与后期高并行需求是连续**方向信号**，非完整代际因果证明 |

## 6. 回到全SoC历史研究的判断

**较强可讲结论**：移动端CPU从早期拓宽单线程与乱序并行，演进到在前端稳定供给、热点重用/门控、预测准确性/安全、预取精度及跨电源域访存延迟之间进行协同权衡；多个厂商采取不完全相同的产品化/自研路线。

**仅能条件化表述**：更宽/更深增加了可利用并行上限，资源的实际收益受工作负载和软硬件配置影响。Apple与Samsung在公开材料中的差别主要体现在“可直接知道的设计动机与黑盒可观察结构”不同，不能无证据推断相反设计哲学或能效胜负。

**缺口**：Apple A8–A13/P核中间阶段；Samsung M4/M5更细分受控消融；同代实机受控比较；Apple编译产物/设备调度与热功率；Samsung关闭自研项目的完整内部经济/技术因果。

## 7. 下一轮收敛方向（无需马上制作PPT）

- **P0**：以Samsung已明确的设计目标与Apple可复现黑盒为例，形成统一的“瓶颈—设计响应—收益口径—代价/反例”标准对照，更新第19轮历史时间线而非复制全部论文内容。
- **P1**：核对Apple A8–A13核心代际中间转折，并与2020 Firestorm对照，避免2013→2020之间形成推测连续链。
- **P1**：补齐近年Arm X1/X2/X3/X4/X925与Samsung/Apple同问题（前端、窗口、内存、能效）不同取舍的**并列证据**，避免只依赖两家叙事。
- **P2**：追踪核内机制与软件变化的真实产品采用路径；延续第23轮LLVM来源边界，避免将任何静态模型当手机实测。

**本轮状态**：QUALITATIVE_MECHANISM_PASS / CROSS_VENDOR_QUANT_ATTRIBUTION_BLOCKED / INTERMEDIATE_GENERATIONS_INCOMPLETE / PUBLIC_ONLY。
