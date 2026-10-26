# 第25轮来源卡 B｜Apple Cyclone/Firestorm 第三方逆向与官方产品边界

**日期**：2026-10-26　**用途**：将Apple实际手机SoC的产品事实与独立黑盒微架构估计分离；同时明确M1测量向A14的迁移边界。

## A25-01｜Apple 产品事实，不含核内隐藏参数

- [Apple 2013 iPhone 5s/A7新闻稿](https://www.apple.com/uk/newsroom/2013/09/10Apple-Announces-iPhone-5s-The-Most-Forward-Thinking-Smartphone-in-the-World/)：确认A7为Apple设计的64位手机SoC；新闻稿未公布ROB、物理寄存器、预测器表或执行端口。
- [Apple 2020 iPhone 12/A14新闻稿](https://www.apple.com/uk/newsroom/2020/10/apple-announces-iphone-12-and-iphone-12-mini-a-new-era-for-iphone-with-5g/)；[Apple iPhone 12技术规格](https://support.apple.com/en-am/111876)：确认A14进入iPhone 12；2 performance +4 efficiency配置；厂商性能宣传包含新制程和多引擎，不可作为Firestorm核内结构独立效果。

## A25-02｜Apple Cyclone（A7，2013）的第三方技术实测与源码线索

- [Anand Lal Shimpi，AnandTech，2014-03-31，Apple's Cyclone Microarchitecture Detailed](https://www.anandtech.com/show/7910/apples-cyclone-microarchitecture-detailed)。
- [REVERSE/TECH-ANALYSIS] 文章基于指令并发测试、技术推导和作者所称Apple LLVM提交，估计Cyclone约6 µops/clock peak issue/dec/ret、192 µop ROB、4整数ALU、2 load/store、2 branch、L1 64KB I +64KB D、L2 1MB、L3 4MB；上代Swift表列3 µops/clock与45 ROB。
- **方法可信边界**：作者明确称没有Apple内部协助，部分端口/缓冲划分仍为推断；不能将所有数字标为Apple官宣，也不能把一篇文章说成Apple多年各代完整剖析。
- **特殊修正**：192 ROB的原文描述部分基于Apple LLVM commits线索，并非“全部数字都由同一实机基准直接测量”，今后记录每一项独立测量路径。
- **历史解释**：Apple在A7时期已选择明显加宽和增加在途指令资源，以提高单线程并行度；“Apple为什么批准此设计”的内部动因未披露。作者提到race-to-sleep、内存容量与软件利用障碍属于分析，不是Apple的设计者原话。

## A25-03｜Firestorm（A14/M1代）的研究者可追溯黑盒实验

- [Dougall Johnson，Firestorm Overview](https://dougallj.github.io/applecpu/firestorm.html)；该研究明确以**M1 Firestorm**为实验对象，描述使用公开/未知性能计数器、指令延迟与缓冲压力测试，部分指令表链接数万组实验计数器结果。
- [REVERSE] 观察到8 µops/cycle限制，约330 **coalesced retire queue groups**、约623 **rename-retire entries**，以及约130 in-flight loads、约60 in-flight stores（均为作者解释下的近似值）。
- **不要写成“Firestorm传统ROB=623”**。作者给出按组退休的机制；一组可包含多个µop，不同指令的重命名/退休结构占用量也不同。rename-retire queue类似Physical Register Reclaim Table，与传统ROB不是同一件事。
- **不要写成“issue宽度=8所以每周期可独立完成8条任意指令”**：文档区分RETIRE_UOP、SCHEDULE_UOP和issue to units；被融合/消除的指令占用不同，contrived input甚至可观察到11 issues/cycle。
- **重要能力实例**：部分move指令可在rename阶段消除；部分CMP+B.cond、CBZ相关指令可融合；loads参与地址依赖时可能出现3-cycle有效传递，其他相关链为4-cycle。均为M1黑盒测量下的特定路径，不是普遍所有load/ALU延迟。
- **不等于A14所有细节已直接在iPhone验证**：Firestorm核型也在A14出现，但不同SoC配置/频率/cache/系统电热会改变整机结果；实验载体须标M1。

## A25-04｜测量方法复核：Load/Store队列的推断不是简单指令计数

- [Dougall Johnson，Apple M1: Load and Store Queue Measurements，2021-04-08](https://dougallj.wordpress.com/2021/04/08/apple-m1-load-and-store-queue-measurements/)。
- 使用两个长期依赖链之间插入load/store并观察是否可并行执行；发现队列项分配释放时机和额外scheduler/dispatch容量会影响阈值。
- 作者推导约130 load queue entries、60 store queue entries，并说明约48-entry load/store scheduler+10-entry dispatch queue可能改变表观阈值；还报告一次受寄存器选择影响的reproducibility异常，2022-07-22更新对部分现象提出复现实验警告。
- 因此，**估计参数须带方法/具体测试链/修订历史**；单一微基准的数值不应与Samsung官方Table I中的不同定义项直接比大小。

## A25-05｜AnandTech另一组独立分析及其术语变化

- [AnandTech，Apple Silicon M1/A14深度分析（2020）](https://www.anandtech.com/show/16226/apple-silicon-m1-a14-deep-dive/2)；[AnandTech，iPhone 12/A14复核（2020-11-30）](https://www.anandtech.com/show/16192/the-iphone-12-review/2)。
- 文章观察A13→A14在SIMD/FP执行等方面有变化，早期将Firestorm “ROB”估约630，并自行标注其未必是传统ROB。随后Dougall提出更细的按组退休/重命名结构解释。
- **裁定**：两者确认“大在途资源”的相同方向，但**不是对同一个传统ROB计量项的独立一致复现**；不得把早期630与后续623视为重复的“630项ROB官方规格”。
- iPhone 12评测提供设备层功耗/性能观察，但制程、频率、频点策略和软件与早年芯片不同；不能据此单独归因于Firestorm的队列结构。

## A25-06｜同代对照的能效核不能被忽视

- [Dougall Johnson，Icestorm Overview（M1）](https://dougallj.github.io/applecpu/icestorm.html)；[Apple iPhone 12规格](https://support.apple.com/en-am/111876)。
- 研究者还量化Icestorm的并行度、寄存器及缓冲结构（约4 µops retire/cycle，约30 load/18 store等），且明确部分缓冲测试可能不准确。
- **历史意义（[INFERENCE]）**：Apple不是仅靠无限增大P核来达成移动能效目标，而是同时构建不同功耗/性能等级；不等同于“Firestorm黑盒队列越大整机越省电”。

## 证据归类

产品上市与核数＝Apple官方直接事实；Cyclone管线/ROB＝第三方测试及代码线索；Firestorm队列＝M1黑盒逆向的近似模型；Apple内部目标、每项机制净能耗贡献、苹果/三星同工艺公平比较＝未知。

**跨代严禁外推**：Cyclone 2013→Firestorm 2020不是连续每一代的完整链；两者没有同工作负载/同测试方法的定量IPC或ROB增长率，不能将192→623写成“ROB扩大3.25倍”。
