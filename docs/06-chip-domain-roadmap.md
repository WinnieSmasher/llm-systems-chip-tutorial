# 06. 集成电路与 AI 芯片方向怎么学

这一章不是让你立刻去做芯片设计，而是帮你把“大模型工程”和“芯片/集成电路/AI 加速器”之间的关系建立起来。

## 1. 大模型为什么离不开芯片

大模型计算主要压力来自：

- 大规模矩阵乘法。
- Attention 计算。
- 高带宽显存访问。
- 多卡通信。
- KV Cache 存储和调度。
- 长上下文带来的显存与带宽压力。

所以大模型性能不只取决于模型结构，也取决于硬件：

```text
算力 FLOPS
显存容量
显存带宽
片上缓存
互联带宽
编译器和算子库
推理调度系统
```

## 2. 从软件角度看 AI 芯片

如果你是软件背景，建议先从这几个层次理解芯片生态：

```text
应用层: Chatbot, RAG, Agent, code generation
框架层: PyTorch, TensorFlow, MindSpore
编译/运行时: CUDA, CANN, ROCm, XLA, TVM
算子库: cuDNN, cuBLAS, CANN operators
硬件层: GPU, NPU, TPU, ASIC
```

你不需要一开始就懂 RTL/Verilog，也可以先从“模型如何跑到硬件上”切入。

## 3. 集成电路方向的基础模块

如果后续想系统学习芯片方向，可以按下面路线：

1. 数字逻辑：组合逻辑、时序逻辑、FSM。
2. 计算机组成：流水线、cache、memory hierarchy、ISA。
3. 并行计算：SIMD、SIMT、thread/block、数据并行。
4. 硬件描述语言：Verilog/SystemVerilog。
5. EDA 基础：综合、布局布线、时序分析。
6. AI 加速器：矩阵乘阵列、systolic array、片上缓存、数据复用。
7. 编译器和 runtime：算子 lowering、kernel scheduling、memory planning。

## 4. 软件同学最应该补的芯片概念

### Memory bandwidth

大模型很多时候不是算力不够，而是数据搬运太慢。

```text
compute-bound: 算得慢
memory-bound: 搬数据慢
```

### Tensor Core / AI Core

这些是专门加速矩阵乘的硬件单元。NVIDIA 叫 Tensor Core，昇腾有 AI Core。

### Operator fusion

把多个小算子融合成一个大算子，减少中间结果写回显存。

例如：

```text
MatMul -> Add -> ReLU
```

可以融合成一个更高效的执行单元。

### Quantization

低精度计算可以减少显存和带宽压力。比如从 BF16 到 INT8/INT4。

### Communication

多卡训练和推理绕不开通信：

- data parallel
- tensor parallel
- pipeline parallel
- all-reduce
- all-gather
- NCCL/HCCL

## 5. 大模型系统与芯片之间的连接点

如果你想做交叉方向，可以关注：

- Attention 优化。
- KV Cache 管理。
- 低比特量化。
- MoE 推理调度。
- 多卡通信优化。
- 编译器图优化。
- 自定义算子开发。
- AI 芯片上的 LLM serving。
- GPU/NPU 性能建模。

## 6. 一个务实学习顺序

1. 先会用 PyTorch/Transformers 跑模型。
2. 再学 vLLM，理解 KV Cache 和 continuous batching。
3. 学 CUDA 基本概念：thread、block、shared memory、stream。
4. 对比 CANN：AscendCL、Ascend C、ATC、算子库。
5. 学 ONNX 和模型转换。
6. 看一个自定义算子例子。
7. 做一个小实验：同一模型在不同 batch size、context length 下测延迟和显存。

## 7. 可以做的项目题目

- 基于 vLLM 的本地 LLM 推理服务压测。
- LoRA 微调一个芯片文档问答模型。
- 比较 FP16、INT8、INT4 量化对模型质量和延迟的影响。
- 整理 CUDA 与 CANN 的 API 对照表。
- 实现一个简单 ONNX -> 推理后端部署 demo。
- 阅读并复现 FlashAttention 的核心思想。
- 分析 KV Cache 在不同并发下的显存占用。

