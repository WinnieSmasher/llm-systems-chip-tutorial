# 01. CUDA、ZLUDA 与昇腾 CANN

先把结论讲死一点：

```text
CUDA 是 NVIDIA GPU 的原生开发和运行生态。
ZLUDA 是 CUDA compatibility layer，目标是让部分 CUDA 程序跑在非 NVIDIA GPU 上。
CANN 是华为 Ascend NPU 的原生软件栈。
```

所以“华为昇腾是不是 ZLUDA”这个问题，答案是：不是。它们甚至不是同一层东西。

## 本章怎么学

读前问题：

- CUDA、ZLUDA、CANN 分别解决哪一层问题？
- 为什么 ONNX 和 `.om` 不能和 CUDA 放在同一类里比较？
- 一个 PyTorch 矩阵乘法到底会落到哪个硬件后端？

课后产出：

- 画一张 `PyTorch -> runtime -> kernel/operator -> hardware` 的边界图。
- 写清 CUDA、ZLUDA、CANN、ONNX、OM 五个词的关系。

自检标准：

- 能解释为什么“昇腾是不是 ZLUDA”这个问法本身就混了层级。
- 能说出 CUDA kernel 和 Ascend C custom operator 的对应关系和差异。

## 1. 先从一段 PyTorch 代码看底层路线

你写：

```python
import torch

x = torch.randn(4096, 4096, device="cuda")
y = x @ x
```

如果机器上是 NVIDIA GPU，底层大致会走：

```text
PyTorch op
  -> CUDA runtime / CUDA driver
  -> cuBLAS 或对应 CUDA kernel
  -> NVIDIA GPU
```

这里的 CUDA 不是“一个库名”那么简单，它包括：

- host/device 编程模型。
- kernel launch 语义，例如 `kernel<<<grid, block>>>()`。
- memory hierarchy，例如 global memory、shared memory、register。
- stream/event，用来组织异步执行。
- cuBLAS、cuDNN、NCCL 等高性能库。

NVIDIA 官方 CUDA C Programming Guide 讲的就是这套东西：程序怎样在 host 端调度 device 端的并行计算，数据怎样在不同内存层级之间移动。

## 2. ZLUDA 在哪一层

ZLUDA 的思路不是“发明一种新芯片”，而是插在 CUDA 程序和非 NVIDIA 后端之间。

```text
CUDA application
  -> ZLUDA
  -> non-NVIDIA backend
  -> non-NVIDIA GPU
```

它的目标是让一部分原本依赖 CUDA 的程序，尽量少改代码就能运行在非 NVIDIA GPU 上。

这件事很难，因为真实 CUDA 程序可能依赖：

- CUDA runtime API。
- driver API。
- cuBLAS/cuDNN/NVRTC 等库行为。
- 特定 GPU 架构和 PTX/SASS 假设。
- 非公开或边界行为。

所以看 ZLUDA 时不要把它理解成“所有 CUDA 程序无痛迁移”。更保守的说法是：

> ZLUDA 是一个 CUDA 兼容层项目，用来探索和支持部分 CUDA workloads 在非 NVIDIA GPU 上运行。

## 3. 华为昇腾 CANN 在哪一层

华为 Ascend 是 NPU。它不是 NVIDIA GPU，也不是“靠 ZLUDA 伪装 CUDA”。

昇腾常见路线是：

```text
PyTorch / MindSpore
  -> torch_npu / MindFormers / MindSpeed-LLM
  -> CANN
  -> Ascend NPU
```

如果是静态模型部署，路线可能是：

```text
PyTorch / ONNX model
  -> ATC
  -> .om model
  -> AscendCL application
  -> Ascend NPU
```

CANN 是总的软件栈，里面常见组件包括：

| 组件 | 作用 | NVIDIA 生态里大概对应什么 |
| --- | --- | --- |
| AscendCL / ACL | 设备、内存、stream、模型加载和执行 | CUDA Runtime / Driver API 的一部分角色 |
| ACL Runtime | 更底层的 context、stream、memory、event 管理 | CUDA runtime 相关能力 |
| ATC | 模型转换和图优化，生成 `.om` | TensorRT / ONNX 后端转换的某些角色 |
| CANN operators | 高性能算子库 | cuDNN / cuBLAS |
| Ascend C | 自定义算子开发 | CUDA kernel 的位置相似，但不是同一种编程模型 |
| HCCL | 多卡通信 | NCCL |

这个表只是帮助定位，不是说 API 能一一替换。

## 4. AscendCL 到底在做什么

推理部署时，AscendCL 程序通常要做这些事：

```text
初始化 ACL
  -> 选择 device
  -> 创建 context / stream
  -> 分配 device memory
  -> 加载 .om 模型
  -> 准备输入 tensor
  -> 执行模型
  -> 拿回输出
  -> 释放资源
```

非常粗的伪代码：

```cpp
aclInit(nullptr);
aclrtSetDevice(0);
aclrtCreateContext(&context, 0);
aclrtCreateStream(&stream);

aclmdlLoadFromFile("model.om", &modelId);
aclmdlExecute(modelId, inputDataset, outputDataset);

aclmdlUnload(modelId);
aclrtDestroyStream(stream);
aclrtDestroyContext(context);
aclrtResetDevice(0);
aclFinalize();
```

这类 API 离业务模型很远，更像“你亲自把数据搬到设备上，让设备执行，再把结果拿回来”。

## 5. Ascend C 和 CUDA kernel 的关系

CUDA kernel 是 NVIDIA GPU 上的自定义并行计算代码。

```cpp
__global__ void add(float* x, float* y, float* out) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    out[i] = x[i] + y[i];
}
```

Ascend C 是昇腾生态里写自定义算子的路线。它也要考虑：

- 数据怎么切分。
- 哪些数据放片上缓存。
- 算子怎么并行。
- 输入输出 tensor shape 怎么处理。
- 编译和注册后怎么接入模型图。

但它不是 CUDA。不要把 CUDA kernel 直接搬过去。

更准确的理解是：

```text
CUDA kernel 解决 NVIDIA GPU 上的自定义计算。
Ascend C custom operator 解决 Ascend NPU 上的自定义算子。
```

## 6. 这几个词怎么放进脑子里

把它们按层级排：

```text
模型框架层: PyTorch, TensorFlow, MindSpore
训练/微调层: Transformers, PEFT, TRL, DeepSpeed, MindSpeed-LLM
硬件运行层: CUDA, ROCm/HIP, CANN
算子和通信: cuBLAS/cuDNN/NCCL, CANN operators/HCCL
硬件层: NVIDIA GPU, AMD GPU, Ascend NPU
兼容层: ZLUDA 这种项目插在 CUDA application 和非 NVIDIA 后端之间
```

ZLUDA 不等于 CUDA，也不等于 CANN。  
CANN 不等于 ONNX，也不等于 PyTorch。  
PyTorch 可以接 CUDA，也可以通过扩展接 NPU 后端。

## 7. 简历里怎么写

别写：

```text
熟悉昇腾 ZLUDA
```

可以写：

```text
了解 NVIDIA CUDA、ZLUDA 兼容层与华为昇腾 CANN 的生态差异，能够区分模型框架、runtime、算子库和硬件后端在大模型部署链路中的作用。
```

如果你真的做过实验，可以写得更具体：

```text
基于 PyTorch/Transformers 跑通本地 LLM 推理 baseline，并整理 CUDA 与 CANN 在设备管理、内存管理、算子库和自定义算子开发上的差异。
```

## 参考

- NVIDIA CUDA C Programming Guide: https://docs.nvidia.com/cuda/cuda-c-programming-guide/
- ZLUDA: https://github.com/vosen/ZLUDA
- Huawei Ascend CANN: https://www.hiascend.com/en/cann
- Ascend documentation: https://www.hiascend.com/document
- MindSpeed-LLM: https://github.com/Ascend/MindSpeed-LLM

