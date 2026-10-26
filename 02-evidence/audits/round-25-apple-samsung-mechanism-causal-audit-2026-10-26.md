# 第25轮审计｜Apple黑盒逆向与Samsung工业论文是否可比

**日期**：2026-10-26；审计主体：[跨厂商因果对照v0.1](../../03-analysis/Apple-Cyclone-Firestorm-vs-Samsung-M1-M5-微架构因果比较-v0.1-2026-10-26.md)；原始来源分别在[Apple卡](../sources/round-25-apple-cyclone-firestorm-reverse-evidence-2026-10-26.md)、[Samsung卡](../sources/round-25-samsung-m1-m5-engineering-paper-2026-10-26.md)。

## 审计清单

| Audit ID | 需要审计的陈述 | 裁定 | 关键原始出处与限制 |
|---|---|---|---|
| AU25-01 | Cyclone 6-wide，约192 ROB属于Apple官方披露 | REVISE | AnandTech 2014黑盒/LLVM提交技术分析，非Apple官方规格；“ROB=192”还涉及公开代码线索而非相同测量 |
| AU25-02 | Firestorm的~623就是传统ROB，约为Cyclone的3.25倍 | BLOCK | Dougall将其称rename-retire entries，并单列~330 coalesced-retire groups；不具备同对象同方法可比性 |
| AU25-03 | Firestorm的约130 load、60 store为A14手机硅片官方规格 | BLOCK | Dougall研究主要是M1黑盒，队列测量受分配/回收、scheduler/dispatch和别名行为影响；不能替代A14 SKU与苹果官方规格 |
| AU25-04 | Samsung M1→M3宽4→6，ROB100→228 | PASS [DESIGNER_TABLE] | ISCA2020 Table I，准确是M2 ROB100、M3 ROB228；宽度列为Dec/Ren/Ret，不应改写成issue全阶段同宽 |
| AU25-05 | M5 UOC主要节省可重用代码取指/译码电力 | PASS [DESIGNER_INTENT] | ISCA Sec.VI 384-µop，Filter/Build/Fetch；但净瓦数/每应用收益BLOCK |
| AU25-06 | Samsung M1→M6 load 14.9→8.3是手机芯片实测 | BLOCK | 4,026 traces、全代统一2.6GHz的周期精确模型，M5/M6硅片在论文建模时不可用，M6未量产 |
| AU25-07 | Samsung M3扩大窗口时加强分支供给的因果动机 | PASS [DESIGNER_EXPLICIT] | ISCA Sec.IV.C直接描述；IEEE Micro M3论文摘要/首页也支持wide/deep与IPC/能效设计目标 |
| AU25-08 | Samsung预取越激进越好 | BLOCK | ISCA Sec.VII明确指出过度预取浪费power、bandwidth、cache；自适应degree和two-pass就是为平衡 |
| AU25-09 | Apple宽执行、Samsung低功耗结构互斥 | BLOCK | Samsung M3也扩大宽度/ROB/PRF；Apple Firestorm有fusion/elimination；“二选一流派”是错误二分 |
| AU25-10 | 三星项目关闭证明某具体自研核结构失败 | BLOCK | Yonhap/Reuters确认组织终止与公司竞争力调整，未证实定量核内技术原因 |
| AU25-11 | M4/M5访存优化全部属于CPU核内 | REVISE | ISCA Sec.IX包含interconnect、DRAM控制器、power/frequency domain、异步跨域路径，必须标SoC内存系统层 |
| AU25-12 | Samsung论文提供完全独立的第三方实机复测 | BLOCK | 作者均曾在SARC，论文工业设计者直接披露、周期精确建模；不是独立复现 |
| AU25-13 | Apple 2013/2020间的所有代际历史因果链已经完成 | BLOCK | 本轮深核仅两个Apple节点，A8–A13缺连续性，且方法不统一 |
| AU25-14 | M3 IEEE Micro已经全8页逐页审阅 | NOT_EVALUABLE | DOI、作者页、摘要与公开首页可核，正文链接暂不能稳定阅读全文；只采纳已核部分 |

## 定量比较闸门

| 领域 | 是否允许同列展示 | 为什么 |
|---|---|---|
| 结构是否存在/来源年份 | 可以，在具体核与来源等级下注明 | 产品事实、工业论文与逆向的证据形式需显示 |
| 同厂Samsung M1–M6 Table I | 可以，明确含设计模型M6与统一Table I语义 | 可对比“模型/设计资源改变”，不可当纯硅片实测 |
| Apple Cyclone vs Firestorm 的ROB/retire queue | **不允许直接画同比例柱状图** | 计量定义、核型、载体、测试方法差异 |
| Apple vs Samsung IPC/FPS/energy per instruction | **BLOCK** | 无同工作负载、同制程、同频率/功率/热、同软件和独立测量 |
| 同功能机制的设计目标 | 可以，**逐行注明是设计者明言或分析推断** | 不得混合“设计者说过”和“根据结构猜测的动因” |

## 对历史研究产生的修正

1. 将Samsung定位为在**明确的宽度/窗口扩展基础上**优化前端功耗、预测安全与访存延迟的案例，而非“小窗节能路线”。
2. Apple Cyclone高资源规模和Firestorm复杂队列只能称“公开黑盒可观察的高并行资源方向”，不能把ROB数字作为同定义持续增长曲线。
3. 用Samsung M5的UOC模式转换、dynamic prefetch degree、memory fast path三个例子说明“控制低收益工作/缓解数据等待”的成本效益逻辑，但不保证在所有应用有效。
4. 全SoC未来趋势分析继续保留多路线共存，不输出“谁领先几代”或“最终赢家”的未经控制的强结论。

**验收**：MECHANISM_AUDIT_CONDITIONAL_PASS / APPLE_QUEUE_EQUIVALENCE_BLOCKED / DEVICE_QUANT_ATTRIBUTION_BLOCKED / M3_FULLTEXT_PENDING。

**最小下一步**：补Apple A8–A13中间代际的直接来源；把第25轮已通过的机制发现以短索引写回第19轮时间线及第21轮矩阵，避免手工复制全文。
