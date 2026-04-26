# 参考资料

这页只放主参考。每章末尾还有更贴近该主题的链接。

## Hugging Face

- Hugging Face LLM Course: https://huggingface.co/learn/llm-course
- Transformers: https://huggingface.co/docs/transformers
- Transformers chat templates: https://huggingface.co/docs/transformers/chat_templating
- Transformers quantization: https://huggingface.co/docs/transformers/quantization/overview
- PEFT: https://huggingface.co/docs/peft
- TRL: https://huggingface.co/docs/trl
- Datasets: https://huggingface.co/docs/datasets
- LightEval: https://huggingface.co/docs/lighteval
- safetensors: https://huggingface.co/docs/safetensors
- bitsandbytes: https://huggingface.co/docs/bitsandbytes

## 评测

- lm-evaluation-harness: https://github.com/EleutherAI/lm-evaluation-harness
- OpenCompass: https://github.com/open-compass/opencompass
- OpenAI Evals: https://github.com/openai/evals

## 推理服务

- vLLM docs: https://docs.vllm.ai/
- vLLM GitHub: https://github.com/vllm-project/vllm
- vLLM speculative decoding: https://docs.vllm.ai/en/latest/features/spec_decode/
- Text Generation Inference: https://huggingface.co/docs/text-generation-inference
- llama.cpp: https://github.com/ggml-org/llama.cpp
- TensorRT-LLM: https://github.com/NVIDIA/TensorRT-LLM

## 模型格式

- ONNX Concepts: https://onnx.ai/onnx/intro/concepts.html
- PyTorch ONNX Export: https://docs.pytorch.org/docs/stable/onnx.html
- ONNX Runtime: https://onnxruntime.ai/

## GPU/NPU 与硬件生态

- NVIDIA CUDA C Programming Guide: https://docs.nvidia.com/cuda/cuda-c-programming-guide/
- NVIDIA CUDA Toolkit: https://developer.nvidia.com/cuda-toolkit
- ZLUDA: https://github.com/vosen/ZLUDA
- Huawei Ascend CANN: https://www.hiascend.com/en/cann
- Huawei Ascend documentation: https://www.hiascend.com/document
- MindSpeed-LLM: https://github.com/Ascend/MindSpeed-LLM

## 分布式训练

- PyTorch FSDP: https://docs.pytorch.org/docs/stable/fsdp.html
- PyTorch Tensor Parallelism: https://docs.pytorch.org/docs/stable/distributed.tensor.parallel.html
- DeepSpeed ZeRO: https://www.deepspeed.ai/tutorials/zero/
- Megatron-LM: https://github.com/NVIDIA/Megatron-LM
- NVIDIA NCCL: https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/overview.html
- Huawei Ascend CANN docs: https://www.hiascend.com/document
- Huawei Ascend HCCL API docs: https://www.hiascend.com/document/detail/zh/canncommercial/80RC1/apiref/hcclapiref/hcclapi_07_0001.html
- MindSpeed-LLM: https://github.com/Ascend/MindSpeed-LLM

## RAG、Agent 与安全

- LangChain RAG tutorial: https://docs.langchain.com/oss/python/langchain/rag
- LlamaIndex RAG overview: https://developers.llamaindex.ai/python/framework/understanding/rag/
- Milvus overview: https://milvus.io/docs/overview.md
- OWASP Top 10 for LLM Applications: https://genai.owasp.org/llm-top-10/

## 开源项目参考来源

开源项目只作为素材来源，不作为教程目录。这里按知识主题保留少量代表项目，真正要沉淀的是概念、源码阅读问题、实验和练习项目。

### Agent Runtime

- OpenAI Codex: https://github.com/openai/codex
- Model Context Protocol Rust SDK: https://github.com/modelcontextprotocol/rust-sdk
- OpenCode: https://github.com/anomalyco/opencode

### 文档智能和科研资料处理

- MarkItDown: https://github.com/microsoft/markitdown
- MinerU: https://github.com/opendatalab/MinerU
- Paper QA: https://github.com/Future-House/paper-qa

### RAG、Memory 和本地知识库

- Langchain-Chatchat: https://github.com/chatchat-space/Langchain-Chatchat
- LlamaIndex: https://github.com/run-llama/llama_index
- Milvus: https://github.com/milvus-io/milvus

### CUDA、Kernel 和异构硬件

- LeetCUDA: https://github.com/xlite-dev/LeetCUDA
- ZLUDA: https://github.com/vosen/ZLUDA
- gprMax: https://github.com/gprMax/gprMax

### 科研写作和图表生产力

- PaperBanana: https://github.com/dwzhu-pku/PaperBanana
- Manim: https://github.com/ManimCommunity/manim

## 论文

- Attention Is All You Need: https://arxiv.org/abs/1706.03762
- GPT-3: https://arxiv.org/abs/2005.14165
- Chinchilla: https://arxiv.org/abs/2203.15556
- InstructGPT: https://arxiv.org/abs/2203.02155
- LoRA: https://arxiv.org/abs/2106.09685
- QLoRA: https://arxiv.org/abs/2305.14314
- DPO: https://arxiv.org/abs/2305.18290
- FlashAttention: https://arxiv.org/abs/2205.14135
- PagedAttention / vLLM paper: https://arxiv.org/abs/2309.06180
- RAG: https://arxiv.org/abs/2005.11401
- DPR: https://arxiv.org/abs/2004.04906
- HELM: https://arxiv.org/abs/2211.09110
