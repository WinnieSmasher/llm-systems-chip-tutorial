# 术语表

## AI Chip / NPU

面向 AI 计算优化的芯片或处理器。NPU 常用于加速矩阵乘、卷积、Transformer 等工作负载。

## Ascend

华为昇腾 AI 处理器系列。

## Ascend C

华为昇腾生态中用于开发自定义算子的编程方式。它在定位上类似 CUDA kernel，但不是 CUDA。

## AscendCL / ACL

Ascend Computing Language。用于设备管理、内存管理、模型加载、模型执行等推理部署任务。

## ATC

Ascend Tensor Compiler。常用于把 ONNX 等模型转换为昇腾可执行的 `.om` 模型。

## CANN

Compute Architecture for Neural Networks。华为昇腾的 AI 计算软件栈。

## CUDA

NVIDIA GPU 的并行计算平台和编程模型。

## DPO

Direct Preference Optimization。用 chosen/rejected 偏好数据进行模型对齐的方法。

## FlashAttention

一种优化 attention 计算和显存访问的技术，常用于提升训练和推理效率。

## Hugging Face Hub

模型、数据集和 demo 的托管平台。

## KV Cache

Transformer 解码时缓存历史 token 的 key/value，减少重复计算。

## LoRA

Low-Rank Adaptation。冻结原模型，只训练少量低秩 adapter 参数。

## ONNX

Open Neural Network Exchange。跨框架模型交换格式，常用于部署和推理优化。

## PEFT

Parameter-Efficient Fine-Tuning。参数高效微调方法集合，包括 LoRA、Prefix Tuning 等。

## QLoRA

在低比特量化 base model 上训练 LoRA adapter 的方法，常用于节省显存。

## RLHF

Reinforcement Learning from Human Feedback。基于人类反馈进行模型对齐。

## SFT

Supervised Fine-Tuning。用 instruction-response 或 conversation 数据进行监督微调。

## TensorRT-LLM

NVIDIA 生态中的大模型推理优化工具。

## torch_npu

PyTorch 适配华为昇腾 NPU 的扩展。

## vLLM

高吞吐大模型推理服务框架，核心能力包括 PagedAttention、continuous batching 和 OpenAI-compatible API。

## ZLUDA

CUDA compatibility layer，目标是让部分 CUDA 程序在非 NVIDIA GPU 上运行。

