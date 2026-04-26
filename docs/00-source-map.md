# 00A. 资料来源地图

这份教程尽量少用“我感觉”。下面列的是主要参考来源，以及它们分别解决什么问题。

## Hugging Face 训练与微调

| 来源 | 看什么 |
| --- | --- |
| [Hugging Face LLM Course](https://huggingface.co/learn/llm-course) | 端到端理解 tokenizer、Transformers、SFT、评测和部署 |
| [Transformers Docs](https://huggingface.co/docs/transformers) | `AutoTokenizer`、`AutoModelForCausalLM`、chat template、`generate` |
| [PEFT Docs](https://huggingface.co/docs/peft) | LoRA、QLoRA、adapter 保存和加载 |
| [TRL Docs](https://huggingface.co/docs/trl) | `SFTTrainer`、`DPOTrainer`、偏好对齐 |
| [Datasets Docs](https://huggingface.co/docs/datasets) | 数据加载、map、split、处理大规模训练数据 |

## 推理服务与优化

| 来源 | 看什么 |
| --- | --- |
| [vLLM Docs](https://docs.vllm.ai/) | OpenAI-compatible server、continuous batching、PagedAttention、prefix caching |
| [PagedAttention paper](https://arxiv.org/abs/2309.06180) | vLLM 为什么能更好管理 KV cache |
| [Hugging Face TGI](https://huggingface.co/docs/text-generation-inference) | 生产推理服务、streaming、tensor parallel |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | 本地轻量推理、GGUF、CPU/消费级硬件部署 |

## 模型格式

| 来源 | 看什么 |
| --- | --- |
| [ONNX Concepts](https://onnx.ai/onnx/intro/concepts.html) | graph、node、initializer、opset 这些 ONNX 基本概念 |
| [PyTorch ONNX Export](https://docs.pytorch.org/docs/stable/onnx.html) | PyTorch 模型如何导出到 ONNX |
| [safetensors Docs](https://huggingface.co/docs/safetensors) | 为什么 Hugging Face 常用 `.safetensors` 保存权重 |

## GPU/NPU 和底层生态

| 来源 | 看什么 |
| --- | --- |
| [NVIDIA CUDA C Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/) | host/device、kernel launch、memory hierarchy、streams |
| [ZLUDA repo](https://github.com/vosen/ZLUDA) | ZLUDA 的项目定位、目标和限制 |
| [Huawei Ascend CANN](https://www.hiascend.com/en/cann) | 昇腾软件栈总入口 |
| [AscendCL API docs](https://www.hiascend.com/document) | 设备、内存、模型加载、模型执行 |
| [Ascend C operator development](https://www.hiascend.com/document) | 自定义算子开发路径 |
| [MindSpeed-LLM](https://github.com/Ascend/MindSpeed-LLM) | 昇腾生态里大模型训练/微调/推理的开源工程入口 |

## 论文

| 论文 | 用途 |
| --- | --- |
| [LoRA](https://arxiv.org/abs/2106.09685) | 理解低秩 adapter 为什么能减少训练参数 |
| [QLoRA](https://arxiv.org/abs/2305.14314) | 理解 4-bit base model + LoRA adapter 的显存优势 |
| [Direct Preference Optimization](https://arxiv.org/abs/2305.18290) | 理解 DPO 如何用 chosen/rejected 偏好数据做对齐 |
| [FlashAttention](https://arxiv.org/abs/2205.14135) | 理解 attention 为什么容易被显存访问限制 |

## 阅读原则

优先级大概是：

```text
官方文档 / 论文 / 主项目 README
  > 官方 examples
  > 高质量工程博客
  > 二手总结
```

教程里的简化类比只是为了建立直觉，不能代替官方 API 文档。要写代码时，以具体版本的文档为准。

