# 01. CUDA、ZLUDA 与昇腾 CANN 的区别

这一章回答一个最容易混的问题：

> 华为昇腾是不是 ZLUDA？CUDA、ZLUDA、CANN 到底是什么关系？

结论先放前面：

```text
CUDA  是 NVIDIA GPU 的原生计算生态
ZLUDA 是 CUDA 兼容层，试图让 CUDA 程序跑到非 NVIDIA GPU 上
CANN  是华为昇腾 Ascend NPU 的原生 AI 计算生态
```

## 1. CUDA 是什么

CUDA 是 NVIDIA 给 GPU 准备的一整套计算平台。它不只是一个语法，而是一套从编程到运行的生态：

- CUDA Runtime / Driver API：管理 GPU、显存、stream、kernel launch。
- CUDA C++ kernel：开发者直接写 GPU 并行计算代码。
- cuBLAS：高性能矩阵计算库。
- cuDNN：深度学习算子库。
- NCCL：多 GPU 通信库。

在深度学习中，你平时写：

```python
x = x.cuda()
```

背后大致是：

```text
PyTorch
  -> CUDA
  -> cuDNN / cuBLAS / NCCL
  -> NVIDIA GPU
```

所以 CUDA 可以理解为 **NVIDIA GPU 的原生语言和工具链**。

## 2. ZLUDA 是什么

ZLUDA 不是硬件，也不是华为生态的一部分。

它更像一个兼容翻译层：

```text
原本调用 CUDA 的程序
  -> ZLUDA 假装自己是 CUDA
  -> 转到底层非 NVIDIA GPU 后端
```

ZLUDA 解决的问题是：

> 我有一个 CUDA 程序，但我没有 NVIDIA GPU，能不能少改代码，在别的 GPU 上跑？

关键词：

- CUDA compatibility layer
- drop-in replacement
- non-NVIDIA GPU

但是 CUDA 生态非常庞大，真实项目里可能遇到库缺失、kernel 不兼容、性能不稳定等问题。因此 ZLUDA 更适合理解为“兼容尝试”，不是通用万能迁移方案。

## 3. 华为昇腾 CANN 是什么

华为昇腾 Ascend 是 NPU，不是 NVIDIA GPU，也不是 AMD GPU。

它的原生软件栈叫 CANN。可以粗略类比为：

```text
NVIDIA GPU : CUDA
Huawei Ascend NPU : CANN
```

CANN 生态里常见组件：

- AscendCL / ACL：控制设备、内存、stream、模型加载与执行。
- ACL Runtime：AscendCL 里面更底层的运行时能力。
- Ascend C：写自定义算子，地位有点像 CUDA kernel，但不是 CUDA。
- ATC：模型转换工具，例如把 ONNX 转成昇腾可执行的 `.om` 模型。
- CANN 算子库：高性能 Conv、MatMul、LayerNorm、Softmax 等算子实现。

一条典型昇腾推理链路是：

```text
PyTorch / ONNX 模型
  -> ATC 转换
  -> .om 模型
  -> AscendCL 加载执行
  -> CANN 算子库
  -> Ascend NPU
```

如果是 PyTorch 训练或微调，常见路线更像：

```text
PyTorch
  -> torch_npu
  -> CANN
  -> Ascend NPU
```

## 4. CUDA kernel 与 Ascend C 的关系

如果现成算子不够用，你可能需要写自定义算子。

在 NVIDIA 上：

```cpp
__global__ void my_kernel(...) {
    ...
}
```

这是 CUDA kernel。

在昇腾上，对应方向是 Ascend C 自定义算子。它们定位相似，都是为了实现底层高性能计算，但编程模型、内存层级、硬件执行单元和工具链都不同。

所以不能说：

```text
Ascend C = CUDA
```

更准确是：

```text
Ascend C 在昇腾生态中的位置，类似 CUDA kernel 在 NVIDIA 生态中的位置。
```

## 5. 最通俗的类比

把硬件看成不同国家：

- NVIDIA GPU 说 CUDA 语系。
- AMD GPU 说 ROCm/HIP 语系。
- 华为 Ascend NPU 说 CANN 语系。

ZLUDA 是一个翻译器，试图让“说 CUDA 的程序”在非 NVIDIA GPU 上跑。

昇腾不是靠 ZLUDA，而是走自己的 CANN 路线。

## 6. 简历中怎么写才准确

不准确：

```text
熟悉昇腾 ZLUDA
```

准确一点：

```text
了解 NVIDIA CUDA 与华为昇腾 CANN 生态差异，熟悉 GPU/NPU 异构计算基本概念。
```

更工程化：

```text
了解 PyTorch 模型在 Ascend NPU 上通过 torch_npu、CANN、AscendCL 进行适配与推理部署的基本流程。
```

