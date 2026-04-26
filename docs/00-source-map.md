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
| [Transformers chat templates](https://huggingface.co/docs/transformers/chat_templating) | conversation 数据如何变成模型输入 token |

## 评测与 Benchmark

| 来源 | 看什么 |
| --- | --- |
| [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | 公开 benchmark runner 的组织方式 |
| [OpenCompass](https://github.com/open-compass/opencompass) | 中文和多模型评测生态 |
| [OpenAI Evals](https://github.com/openai/evals) | 自定义 eval 和回归测试 |
| [LightEval](https://huggingface.co/docs/lighteval) | Hugging Face 生态里的轻量评测 |

## 推理服务与优化

| 来源 | 看什么 |
| --- | --- |
| [vLLM Docs](https://docs.vllm.ai/) | OpenAI-compatible server、continuous batching、PagedAttention、prefix caching |
| [vLLM speculative decoding](https://docs.vllm.ai/en/latest/features/spec_decode/) | draft/verify 类推理加速思路 |
| [PagedAttention paper](https://arxiv.org/abs/2309.06180) | vLLM 为什么能更好管理 KV cache |
| [Hugging Face TGI](https://huggingface.co/docs/text-generation-inference) | 生产推理服务、streaming、tensor parallel |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | 本地轻量推理、GGUF、CPU/消费级硬件部署 |

## 量化

| 来源 | 看什么 |
| --- | --- |
| [Transformers quantization overview](https://huggingface.co/docs/transformers/quantization/overview) | bitsandbytes、GPTQ、AWQ、Quanto 等量化入口 |
| [bitsandbytes docs](https://huggingface.co/docs/bitsandbytes) | 8-bit/4-bit 加载和 QLoRA 常用依赖 |
| [PEFT LoRA guide](https://huggingface.co/docs/peft/developer_guides/lora) | LoRA/QLoRA adapter 训练和加载 |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | GGUF 本地推理和量化生态 |

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

## 分布式训练

| 来源 | 看什么 |
| --- | --- |
| [PyTorch FSDP](https://docs.pytorch.org/docs/stable/fsdp.html) | 参数、梯度、优化器状态 shard |
| [PyTorch Tensor Parallelism](https://docs.pytorch.org/docs/stable/distributed.tensor.parallel.html) | PyTorch 原生 tensor parallel |
| [DeepSpeed ZeRO](https://www.deepspeed.ai/tutorials/zero/) | ZeRO stage 1/2/3 的切分逻辑 |
| [Megatron-LM](https://github.com/NVIDIA/Megatron-LM) | tensor parallel、pipeline parallel、sequence parallel |
| [NCCL docs](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/overview.html) | 多 GPU collective communication |
| [Ascend HCCL API docs](https://www.hiascend.com/document/detail/zh/canncommercial/80RC1/apiref/hcclapiref/hcclapi_07_0001.html) | 昇腾多机多卡集合通信 |

## RAG、Agent 与安全

| 来源 | 看什么 |
| --- | --- |
| [LangChain RAG tutorial](https://docs.langchain.com/oss/python/langchain/rag) | indexing、retrieval、generation 的基本拆法 |
| [LlamaIndex RAG overview](https://developers.llamaindex.ai/python/framework/understanding/rag/) | RAG 应用框架里的数据和检索概念 |
| [Milvus overview](https://milvus.io/docs/overview.md) | 向量数据库基本概念 |
| [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/) | prompt injection、supply chain、excessive agency 等风险 |

## 论文

| 论文 | 用途 |
| --- | --- |
| [LoRA](https://arxiv.org/abs/2106.09685) | 理解低秩 adapter 为什么能减少训练参数 |
| [QLoRA](https://arxiv.org/abs/2305.14314) | 理解 4-bit base model + LoRA adapter 的显存优势 |
| [Direct Preference Optimization](https://arxiv.org/abs/2305.18290) | 理解 DPO 如何用 chosen/rejected 偏好数据做对齐 |
| [FlashAttention](https://arxiv.org/abs/2205.14135) | 理解 attention 为什么容易被显存访问限制 |
| [Attention Is All You Need](https://arxiv.org/abs/1706.03762) | Transformer 基本结构 |

## 阅读原则

优先级大概是：

```text
官方文档 / 论文 / 主项目 README
  > 官方 examples
  > 高质量工程博客
  > 二手总结
```

教程里的简化类比只是为了建立直觉，不能代替官方 API 文档。要写代码时，以具体版本的文档为准。
