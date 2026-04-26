# 00. 学习地图

这份教程围绕一条主线展开：

```text
模型从 Hugging Face 来
数据决定模型学什么
训练/微调改变模型能力
推理优化决定模型跑得快不快
CUDA/CANN 决定模型跑在哪类硬件上
```

## 你需要先建立的直觉

大模型项目不是只有“调 API”这一件事。完整链路通常包括：

1. 选择模型：DeepSeek、GLM、Qwen、Llama 等模型家族中选合适的 base/instruct 模型。
2. 准备数据：instruction data、domain corpus、preference data、evaluation set。
3. 训练或微调：SFT、LoRA、QLoRA、continued pretraining、DPO/RLHF。
4. 评测：准确率、困惑度、人工偏好、任务指标、延迟、吞吐、显存占用。
5. 推理优化：量化、KV Cache、FlashAttention、vLLM、TensorRT-LLM、CANN 部署。
6. 部署迭代：上线服务、收集反馈、清洗新数据、再次训练。

## 两个关键问题

### 问题一：模型是什么？

在 Hugging Face 上，一个模型通常不是一个单独文件，而是一组文件：

- `config.json`：模型结构配置。
- `tokenizer.json` / tokenizer files：分词器。
- `model.safetensors`：模型权重。
- `generation_config.json`：生成参数。
- `README.md` / model card：模型说明、license、训练信息。

### 问题二：硬件生态是什么？

同一个模型可以跑在不同硬件上，但底层路线不同：

- NVIDIA GPU：PyTorch -> CUDA -> cuDNN/cuBLAS/NCCL -> GPU。
- AMD GPU：PyTorch -> ROCm/HIP -> AMD GPU。
- 华为昇腾 NPU：PyTorch/MindSpore -> torch_npu/MindFormers -> CANN -> Ascend NPU。

ZLUDA 不属于华为昇腾生态，它是 CUDA compatibility layer，主要用于让部分 CUDA 程序尝试跑在非 NVIDIA GPU 上。

