# LLVM 23.1.4 代码生成优化入口审计 v0.1

**固定版本：** `llvmorg-23.1.4`  
**研究模式：** PUBLIC_ONLY；未运行编译、benchmark、llvm-mca、仿真或设备测试。  
**目标：** 为历史 CPU 微架构变化补上“LLVM 看得见什么、能做什么、仍看不见什么”的实现证据。

## 核心结论

LLVM 中确实存在寄存器压力感知调度、寄存器分配与 spill 处理、向量化成本模型、基于 profile 的基本块布局，以及 SME 架构状态/ABI 属性等具体机制。但这些机制只利用编译器可见的信息和模型，不能自动得知实际手机的隐藏物理寄存器池、实时乱序队列占用、真实 cache miss 或热降频状态。

## 实现入口矩阵

| 主题 | 固定版本源码证据 | 已核实内容 | 对历史解释的意义 | 未证明的内容 |
|---|---|---|---|---|
| 机器指令调度与寄存器压力 | [MachineScheduler.cpp](https://github.com/llvm/llvm-project/blob/llvmorg-23.1.4/llvm/lib/CodeGen/MachineScheduler.cpp), SHA `786fe1d0b8fe3066fa1bc7e80ae1e7a00b2d645c` | 源码中有 `misched-regpressure` 选项，默认启用寄存器压力调度 | 指令排序不仅考虑依赖/延迟，也会顾及活跃值造成的寄存器压力 | 不知道目标核心的内部物理 rename register pool；不保证在每个负载下减少真实 stall |
| 寄存器分配 | [RegAllocGreedy.cpp](https://github.com/llvm/llvm-project/blob/llvmorg-23.1.4/llvm/lib/CodeGen/RegAllocGreedy.cpp), SHA `6b8a9b8190f9a0b5e48d93b8701559b73ad4e707` | Greedy register allocator 处理 live intervals、live register matrix 等分配对象 | 活跃区间、可用架构寄存器和 spill 代价是代码生成层的重要约束 | 本轮未对每个目标执行编译，因此未量化某款手机核的 spill 数量、栈流量或性能代价 |
| Loop Vectorizer | [LoopVectorize.cpp](https://github.com/llvm/llvm-project/blob/llvmorg-23.1.4/llvm/lib/Transforms/Vectorize/LoopVectorize.cpp), SHA `a4aae2651ee4c5b0e09a2bddc68d3954b5679c51` | 代码包含 VF/IC、成本模型、代码尺寸与尾循环处理；源码也明确承认部分 epilogue vectorization 的成本模型仍是粗略启发式 | 更宽 SIMD/更多向量资源要转化成收益，依赖循环合法性、成本估计、代码尺寸与寄存器压力等因素 | 不保证向量化一定变快，也没有证明端到端手机应用或能耗改善 |
| Profile 引导的块布局 | [BasicBlockSections.cpp](https://github.com/llvm/llvm-project/blob/llvmorg-23.1.4/llvm/lib/CodeGen/BasicBlockSections.cpp), SHA `9972d431aae8b0a1082365bc9dc611de953aa9a3` | 基本块聚类逻辑读取 profile-derived block/edge weights 并识别热块 | 运行时频率可以影响代码布局；这条路径利用的是行为 profile | 不直接读取 BTB、预测器表项或实际误预测状态；profile 不代表所有真实部署工作负载 |
| SME 状态/调用边界 | [CGCall.cpp](https://github.com/llvm/llvm-project/blob/llvmorg-23.1.4/clang/lib/CodeGen/CGCall.cpp), SHA `08cb9860f2f920ab00d7f9b48adcabe86816c669` | Clang CodeGen 将 SME function type 属性映射为 LLVM IR function attributes，包括 streaming 与 ZA 状态相关属性 | 新架构状态会影响函数契约、调用兼容性和后端 lowering，而不只是增加几条指令 | 未运行端到端 SME 编译，也未测量手机设备状态切换周期、保存恢复流量或能耗 |

## 对历史微架构变化的桥接

### 1. 乱序窗口与执行资源增长
硬件可能通过更大的窗口、更高的发射/执行能力容纳更多独立操作；编译器能通过指令调度、依赖分析、循环展开和向量化暴露并行性。但编译器不能保证运行时窗口始终填满：指针依赖、cache miss、分支误预测、内存带宽和功耗状态都可能成为限制。

### 2. 架构寄存器压力
硬件内部物理寄存器重命名和 LLVM 的架构寄存器分配不是同一层。LLVM allocator 管理的是目标 ISA 暴露的寄存器类及 spill slots；编译器通过控制活跃区间、复制合并和 spill 代价减少软件层压力，但无法直接分配/读取微架构内部 PRF。

### 3. SIMD 与向量执行能力
新 ISA/更强向量执行资源提供可利用的硬件路径；Loop Vectorizer 需要先证明转换合法，再用目标成本模型选择 VF/IC。若出现额外检查、尾循环、数据转换、寄存器压力或代码膨胀，理论吞吐并不等于实际加速。

### 4. 分支预测与前端
PGO 的块/边权重可影响代码布局，使高频路径更集中；这是把 workload 信息传递给编译器的路径，不是直接操控硬件预测器。真实预测效果还取决于分支历史、地址别名、动态输入与 predictor 实现。

### 5. SME/ZA 等架构状态
编译器需要把架构状态表达在函数属性、调用契约和指令生成中；因此新状态功能的落地通常同时依赖 ISA、ABI、前端语言属性和后端 lowering。仅看到目标 feature 可用，不能推断应用已经使用，更不能推断净能耗收益。

## 证据分级

- **SOURCE_FACT：** 固定 tag 中存在相应代码结构/属性/选项。
- **MECHANISM_INFERENCE：** 根据代码结构说明它如何连接到历史微架构变化。
- **NOT_ESTABLISHED：** 某目标手机的实际代码是否触发该路径、产生多少性能/能耗收益。
- **UNKNOWN：** 实际芯片隐藏状态、厂商编译器配置、工作负载代表性和设备测量。

上述来源均来自同一 LLVM 官方仓库，不应被误算为独立的性能实验证据。

## 下一步

1. 补充固定版本下 AArch64 target 对这些通用机制的具体参数和 feature 差异。
2. 把本表与第21轮核内机制矩阵逐项关联，并标注可直接映射/模型映射/profile 映射/不可直接观测四类路径。
3. 回写第19轮历史时间线：硬件变化 → 软件可利用入口 → 中间限制 → 公开证据成熟度。
4. 最终单独列出哪些结论已可用于历史解释、哪些仍缺手机端公开证据；不补造性能数字。
