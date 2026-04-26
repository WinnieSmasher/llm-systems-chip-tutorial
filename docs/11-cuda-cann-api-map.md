# 11. CUDA / CANN API Map

这张表不是“API 一一等价表”。它只是帮你定位：在 NVIDIA GPU 生态里某件事大概由谁负责，在昇腾 NPU 生态里应该去看哪块文档。

## 1. 设备、上下文、内存、stream

| 任务 | CUDA 生态 | CANN / Ascend 生态 | 备注 |
| --- | --- | --- | --- |
| 选择设备 | `cudaSetDevice` | `aclrtSetDevice` | 选择当前 device |
| 分配 device memory | `cudaMalloc` | `aclrtMalloc` | 设备侧内存 |
| 释放 device memory | `cudaFree` | `aclrtFree` | 资源释放 |
| Host <-> Device 拷贝 | `cudaMemcpy` | `aclrtMemcpy` | 注意方向和内存类型 |
| 创建 stream | `cudaStreamCreate` | `aclrtCreateStream` | 异步执行队列 |
| 销毁 stream | `cudaStreamDestroy` | `aclrtDestroyStream` | 资源释放 |
| 同步 stream | `cudaStreamSynchronize` | `aclrtSynchronizeStream` | 等待任务完成 |

## 2. 模型和算子

| 任务 | CUDA / NVIDIA | CANN / Ascend | 备注 |
| --- | --- | --- | --- |
| 自定义底层计算 | CUDA kernel | Ascend C custom operator | 编程模型不同 |
| 深度学习算子库 | cuDNN | CANN operators | Conv、Norm、Activation 等 |
| 矩阵计算库 | cuBLAS | CANN operators / Ascend 算子库 | 不要假设接口等价 |
| 多卡通信 | NCCL | HCCL | all-reduce、all-gather 等 |
| 静态模型优化 | TensorRT / ONNX Runtime | ATC / OM / AscendCL | 部署链路不同 |

## 3. 一个最小推理程序会做什么

NVIDIA CUDA/C++ 侧，大致是：

```text
set device
allocate memory
copy input
launch kernel or call library
copy output
free memory
```

AscendCL 侧，大致是：

```text
aclInit
aclrtSetDevice
create context / stream
load OM model
create input/output dataset
execute model
destroy dataset / unload model
destroy stream / context
aclFinalize
```

## 4. 为什么这不是简单替换

不能把：

```text
cudaMalloc -> aclrtMalloc
cudaMemcpy -> aclrtMemcpy
```

看成就能迁移整个程序。真实迁移还涉及：

- 算子是否支持。
- shape 是否支持动态。
- 数据 layout 是否一致。
- 精度是否一致。
- runtime 错误处理。
- 性能是否符合预期。
- 自定义 kernel 是否要重写成 Ascend C。

## 5. 适合做的练习

1. 整理 CUDA Runtime 和 AscendCL 的设备/内存/stream API。
2. 画出 ONNX -> OM -> AscendCL 的推理调用链。
3. 找一个不支持算子的转换失败案例，分析是算子、shape 还是 dtype 问题。
4. 对比 NCCL 和 HCCL 在多卡训练里的位置。

## 参考

- CUDA C Programming Guide: https://docs.nvidia.com/cuda/cuda-c-programming-guide/
- CUDA Runtime API: https://docs.nvidia.com/cuda/cuda-runtime-api/
- Huawei Ascend documentation: https://www.hiascend.com/document
- Huawei CANN: https://www.hiascend.com/en/cann

