# 06. 集成电路与 AI 芯片学习路线

如果你是软件背景，想往“大模型系统 + 芯片/异构计算”方向靠，不用一开始就钻 Verilog。可以先从一个更贴近工程的问题开始：

> 为什么同一个模型，换一张卡、换一个 runtime、换一个 batch size，速度和显存会差这么多？

这个问题会自然把你带到 GPU/NPU、memory bandwidth、算子库、编译器和推理调度。

## 1. 大模型主要吃什么硬件资源

LLM 推理和训练的压力主要来自：

- 矩阵乘。
- Attention。
- 显存容量。
- 显存带宽。
- KV cache。
- 多卡通信。
- kernel launch 和算子调度。

参数量只是其中一项。很多时候瓶颈不是“算不动”，而是“数据搬得太慢”。

## 2. 软件同学先补哪些概念

### Memory hierarchy

先理解：

```text
register
shared memory / local cache
L2 cache
HBM / global memory
CPU memory
```

很多优化本质是在减少慢内存访问。

### Compute-bound vs memory-bound

如果算术单元很忙，是 compute-bound。  
如果算术单元等数据，是 memory-bound。

大模型里的很多算子，尤其是某些 elementwise、normalization、attention 相关操作，会受 memory IO 影响。

### Tensor Core / AI Core

NVIDIA 有 Tensor Core。昇腾有 AI Core。它们都围绕矩阵计算做硬件加速，但指令、数据布局、编程模型和工具链不同。

### Operator fusion

把多个算子融合，减少中间结果落显存。

例如：

```text
MatMul -> Bias -> GeLU
```

如果每一步都写回显存，会浪费带宽。fusion 能减少搬运。

### Communication

多卡训练/推理离不开通信：

- data parallel
- tensor parallel
- pipeline parallel
- all-reduce
- all-gather
- NCCL/HCCL

模型越大，通信越可能成为瓶颈。

## 3. 该怎么学 CUDA

不要上来就写复杂 kernel。先理解 CUDA 的几个基本词：

- host/device。
- thread/block/grid。
- global memory/shared memory/register。
- stream/event。
- kernel launch。
- memory coalescing。

小练习：

1. vector add。
2. matrix transpose。
3. tiled matrix multiplication。
4. reduction。
5. 用 profiler 看 memory throughput。

这些练习比“看完一堆术语”有用。

## 4. 该怎么学 CANN/昇腾

从软件角度，先把链路跑通：

```text
PyTorch 模型
  -> ONNX
  -> ATC
  -> OM
  -> AscendCL 推理
```

再看：

- torch_npu 如何让 PyTorch 接昇腾。
- MindSpeed-LLM 怎样组织大模型训练/微调。
- Ascend C 自定义算子怎么写。
- HCCL 怎样做多卡通信。

不要一上来就把 CANN 想成 CUDA 的替身。它有自己的模型转换、runtime、算子和编译链路。

## 5. 大模型系统和芯片的交叉题

适合做成学习项目：

- KV cache 显存建模。
- vLLM continuous batching 压测。
- FlashAttention 阅读和复现。
- FP16/INT8/INT4 量化质量对比。
- CUDA 与 CANN runtime API 对照。
- ONNX 导出和后端转换失败案例整理。
- 自定义算子性能分析。
- 多卡通信中 batch、sequence length、tensor parallel 的影响。

## 6. 推荐学习顺序

```text
阶段 1：Transformers 跑通模型推理
阶段 2：vLLM 跑通服务和压测
阶段 3：理解 KV Cache 和 attention 性能瓶颈
阶段 4：学 CUDA 基础 kernel
阶段 5：看 ONNX 和模型转换
阶段 6：对比 CANN/AscendCL/Ascend C
阶段 7：做一个小型性能实验并写报告
```

这条路比“同时学 CUDA、芯片设计、微调、部署”稳得多。

## 参考

- NVIDIA CUDA C Programming Guide: https://docs.nvidia.com/cuda/cuda-c-programming-guide/
- vLLM docs: https://docs.vllm.ai/
- Huawei Ascend CANN: https://www.hiascend.com/en/cann
- MindSpeed-LLM: https://github.com/Ascend/MindSpeed-LLM
- FlashAttention paper: https://arxiv.org/abs/2205.14135

