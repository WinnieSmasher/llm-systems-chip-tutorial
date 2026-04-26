# 18. 分布式训练与并行策略

大模型训练最难的不是“多插几张卡”。难点在于模型参数、梯度、优化器状态、激活值和通信都变大了。不同并行策略是在切不同的东西。

## 1. 先看训练显存由什么组成

```text
model parameters
gradients
optimizer states
activations
temporary buffers
communication buffers
```

Adam 这类优化器会带来额外状态。训练比推理更吃显存，原因就在这里。

## 2. 常见并行策略

| 策略 | 切什么 | 典型工具 |
| --- | --- | --- |
| Data Parallel / DDP | 数据 batch | PyTorch DistributedDataParallel |
| FSDP | 参数、梯度、优化器状态 shard | PyTorch FSDP |
| ZeRO | optimizer/gradient/parameter redundancy | DeepSpeed ZeRO |
| Tensor Parallel | 单层矩阵乘 | Megatron-LM |
| Pipeline Parallel | 层 | Megatron-LM、DeepSpeed |
| Sequence Parallel | sequence 维度部分计算 | Megatron-LM |
| Expert Parallel | MoE experts | Megatron/DeepSpeed/MoE 系统 |

不要把这些词背成名词。问自己：它到底切了什么，通信发生在哪里？

## 3. DDP 到 FSDP / ZeRO

DDP 的直觉：

```text
每张卡一份完整模型
每张卡吃不同 batch
反向传播后 all-reduce gradients
```

DDP 简单，但每张卡都有完整参数和优化器状态。

FSDP / ZeRO 的直觉：

```text
不要每张卡都存完整训练状态
把参数、梯度、优化器状态切开
需要计算时再 gather
```

代价是通信和配置复杂度增加。

## 4. Tensor Parallel

Transformer 里大矩阵乘很多。tensor parallel 会把矩阵乘拆到多卡上，例如按列切或按行切。

优点：

- 单层大矩阵能跨卡放。
- 适合超大模型。

代价：

- 每层都有通信。
- 对 interconnect 要求高。
- 配错后速度可能很差。

## 5. Pipeline Parallel

pipeline parallel 把模型层分到不同卡：

```text
GPU0: layer 0-7
GPU1: layer 8-15
GPU2: layer 16-23
GPU3: layer 24-31
```

micro-batch 会像流水线一样流过各张卡。问题是 pipeline bubble：有些阶段会等待，设备利用率不是天然满。

## 6. 通信库：NCCL / HCCL

NVIDIA 生态常见 NCCL，昇腾生态常见 HCCL。它们负责多设备之间的 collective communication，例如：

- all-reduce
- all-gather
- reduce-scatter
- broadcast

分布式训练慢，很多时候不是算力不够，而是通信和拓扑限制。单机多卡、跨机多卡、PCIe、NVLink、InfiniBand、RoCE，差别很大。

在昇腾项目里，还要同时看 CANN、HCCL、MindSpore/torch_npu/MindSpeed-LLM 的版本匹配。通信库能用，不代表上层训练框架的并行策略已经适配好。

## 7. Checkpoint 也会变复杂

单卡训练保存一个 `model.safetensors` 还比较直观。分布式训练会出现：

- sharded checkpoint。
- optimizer state shard。
- rank-specific files。
- resume 时 world size 不一致。
- 保存太频繁拖慢训练。

训练脚本要明确：

```text
save strategy:
checkpoint format:
resume command:
how to merge adapter / full weights:
```

## 8. 最小学习路线

建议顺序：

1. 单卡跑通 `Trainer` 或 `SFTTrainer`。
2. DDP 跑通两卡 toy example。
3. 看 PyTorch FSDP 的 wrapping 和 checkpoint。
4. 看 DeepSpeed ZeRO stage 1/2/3 差别。
5. 读 Megatron-LM 里的 tensor/pipeline parallel 概念。
6. 再去看 MoE、expert parallel、sequence parallel。

先别一上来改 Megatron 配置。那样很容易只是在调 YAML。

## 9. 简历里怎么写

弱写法：

```text
熟悉分布式训练，了解 FSDP、ZeRO、Megatron。
```

强写法：

```text
梳理 DDP、FSDP/ZeRO、tensor parallel 与 pipeline parallel 的训练状态切分方式，基于 toy model 对比显存占用、通信模式和 checkpoint 结构，为后续 LoRA/SFT 多卡训练配置提供实验依据。
```

## 参考

- PyTorch FSDP: https://docs.pytorch.org/docs/stable/fsdp.html
- PyTorch Tensor Parallelism: https://docs.pytorch.org/docs/stable/distributed.tensor.parallel.html
- DeepSpeed ZeRO: https://www.deepspeed.ai/tutorials/zero/
- Megatron-LM: https://github.com/NVIDIA/Megatron-LM
- NCCL docs: https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/overview.html
- Huawei Ascend CANN docs: https://www.hiascend.com/document
- Huawei Ascend HCCL API docs: https://www.hiascend.com/document/detail/zh/canncommercial/80RC1/apiref/hcclapiref/hcclapi_07_0001.html
- MindSpeed-LLM: https://github.com/Ascend/MindSpeed-LLM
