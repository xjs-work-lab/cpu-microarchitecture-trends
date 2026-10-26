# 第26轮审计｜Apple A8—A13核内变化的事实、第三方逆向与因果区分

**审计日期**：2026-10-26　**分析对象**：[A8—A13代际机制与因果链](../../03-analysis/Apple-A8-A13-代际机制与因果链-v0.1-2026-10-26.md)　**原始来源ID**：[AP26-01—18](../sources/round-26-apple-a8-a13-primary-and-reverse-sources-2026-10-26.md)。

| ID | 主要论断 | 裁定 | 理由与边界 |
|---|---|---|---|
| AU26-01 | A8比A7全面加宽了CPU流水线 | REJECT | AnandTech2014 A8依旧约6µops；只是优化部分延迟与性能/能效，厂商目的/制程不可反演 |
| AU26-02 | A8 ROB确实192、branch penalty必定16 | REVISE/UNCERTAIN | A8同期比较表项明确加?，仅可写“与Cyclone接近，未见同口径确认改变” |
| AU26-03 | A9约6-wide/192ROB，分支惩罚约16→9 | PASS[THIRD_PARTY_ANALYSIS] | 同一AnandTech表述/测量估计，不能当Apple官方硅片规格；惩罚变化不代表预测正确率的变化 |
| AU26-04 | A9官宣70% CPU提升由分支预测改良单独带来 | BLOCK | 包含制程、频率、存储、软件与其它结构差异；无消融归因 |
| AU26-05 | A10自2016公开2P+2E | PASS[OFFICIAL_PRODUCT] | Apple2016直接描述，动态行为与内部结构未披露 |
| AU26-06 | A11有6核同时利用能力 | PASS[OFFICIAL_PRODUCT] | Apple2017明确第二代performance controller与六核同时工作；声明70%多线程改善不可归到单一核数 |
| AU26-07 | Tempest与Arm A53/A55一样都是顺序小核 | REJECT | AnandTech2018报告3-wide OoO小核；仍属第三方而非官方结构 |
| AU26-08 | A12 Vortex约7-wide，L1I/D 128KB | CONDITIONAL_PASS[REVERSE] | 由同期评测及A13后续同团队核内回顾支持，留出测量和文档版本限定，不写Apple官方 |
| AU26-09 | A12 SPEC绝对结果是官方认证且可跨OS直接排名 | BLOCK | AnandTech声明estimated，iOS Xcode10、修改429.mcf工作集并缩放修正、频率不能固定 |
| AU26-10 | A13大核执行资源每项都较A12明显增加 | REJECT | AnandTech发现7-wide与主要执行管线保持，部分整数乘除路径改良，小核与内存/调度变化更显著 |
| AU26-11 | A13小核相比Tempest FP/SIMD与L1D显著演进 | CONDITIONAL_PASS[THIRD_PARTY_TEST] | 原始延迟/吞吐测试和L1D逆向；受测试集与内存控制策略影响 |
| AU26-12 | A13 SLC=16MB与小核L2≈4MB属Apple官方CPU L3 | REJECT | 第三方拆片/架构推断，SLC共享SoC，与CPU私有L2不同；L2为likely而非官方确认 |
| AU26-13 | A13任务迁核阈值固定30ms、A12固定54ms | REVISE | AnandTech在其测量条件下观察到近似迁移时间，非iOS所有负载的固定阈值/调度政策文档 |
| AU26-14 | 小核禁用高DRAM频点能保证一切负载更快更省电 | BLOCK | 逆向观察部分memory workloads可能退步，仍需能量/延迟/热系统测量 |
| AU26-15 | 苹果CPU核名/低层参数全部由Apple公告直接公布 | REJECT | 核名与参数大量源于第三方、拆片、公开LLVM与低层实验；苹果公告更多是产品与目标层 |
| AU26-16 | Apple 2013→2020连续每代ROB都同比扩容 | BLOCK | A8/A9本轮显示持平或未知；A10/A11缺同定义，Firestorm623 rename-retire≠传统ROB |

## 本轮合格输出

1. **可发布的产品史：** A8/A9双大核；A10 2P2E；A11 2P4E且可同时利用全部六核；A12/A13延续2P4E、架构与软件协同加强。各时间点对应官方公告，内部代号由技术来源支撑。
2. **可限定的机制史：** A8/A9大核宽度近似维持，A9分支恢复改善；A12 Tempest 3-wide OoO；A13大核执行资源增量有限而小核FP/SIMD与SLC/迁核策略有明显改变。
3. **不可归因的结果：** 70%/15%/20%厂商性能声明、手机电池续航变化、某项缓存/预测器/调度贡献的净节能、A13所有任务固定30ms迁移、2013→2020的ROB增长倍率。

## 审计方法与可信度

- 官方发布**高可信产品事实**不等于高可信内部微架构；
- 同一媒体隔年多篇低层分析虽可形成研究连续性，**不是多个独立实验团队的多源重复验证**；
- Apple与Samsung公开透明度差异很大：前者第三方黑盒，后者自研团队工业论文周期精确模拟；没有同条件、同负载可比数据，不准给性能/W绝对胜负排名；
- 保留对A8疑问项、A10/A11隐藏结构、系统调度的机型/OS/负载适用边界。

**状态**：HISTORY_NODE_COVERAGE_PASS / MICROARCH_NOT_FULLY_VERIFIED / CAUSAL_INTENT_NOT_FULLY_VERIFIED / DEVICE_ENERGY_ATTRIBUTION_BLOCKED / PUBLIC_ONLY。

**后续最小任务**：在不扩张代际名单的前提下，做覆盖/证据强度矩阵与跨层因果反证；定向补A10/A11核内来源、A12/13单核测量方法与系统DVFS，同上一轮Samsung模型口径并列。
