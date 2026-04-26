# 16. 量化专题

量化不是“把模型压小”这么简单。它会改变权重、激活值、KV cache 或计算 kernel 的精度，目标是在显存、速度和质量之间换一个更合适的点。

## 1. 先看量化对象

| 对象 | 说明 | 常见场景 |
| --- | --- | --- |
| weight-only quantization | 只压权重 | 推理部署最常见 |
| weight + activation quantization | 权重和激活都低精度 | 更依赖校准和 kernel 支持 |
| KV cache quantization | 压低 KV cache 占用 | 长上下文和高并发服务 |
| training quantization | 训练中使用低精度 | QLoRA、FP8 training |

如果只说“INT4”，信息不够。要说清楚是权重量化、KV cache 量化，还是训练时的 4-bit base model。

## 2. 常见方法怎么区分

| 方法 | 大概位置 | 关键词 |
| --- | --- | --- |
| bitsandbytes | Hugging Face 加载时量化 | 8-bit、4-bit、QLoRA |
| GPTQ | post-training weight quantization | 校准数据、离线量化 |
| AWQ | activation-aware weight quantization | 激活感知、推理部署 |
| GGUF / GGML | llama.cpp 生态 | 本地 CPU/消费级硬件 |
| Quanto / Optimum | Hugging Face 量化工具链 | 多后端实验 |
| torchao | PyTorch 量化生态 | PyTorch 原生方向 |
| FP8 | 训练和推理都可能用 | 新硬件支持更关键 |

Hugging Face Transformers 量化文档列了很多方法。不要一开始就全学，先把 bitsandbytes、GPTQ/AWQ、GGUF 这三类分清楚。

## 3. QLoRA 不是普通 INT4 推理

QLoRA 的典型思路：

```text
base model: 4-bit loaded, frozen
adapter: LoRA weights, trainable
optimizer/state: 针对低显存训练设计
```

也就是说，训练时更新的是 LoRA adapter，不是把整个 4-bit base model 都拿去全量训练。

这和“下载一个 INT4 模型直接推理”不是一回事。

## 4. 量化前先固定评测

量化会让模型质量下降，也可能让格式遵循变差。至少测：

- 基础问答正确率。
- 领域术语解释。
- JSON/表格格式输出。
- 长上下文下是否漏信息。
- RAG 引用是否稳定。
- 拒答和安全边界。

推荐流程：

```text
FP16/BF16 baseline
  -> run eval
  -> quantize
  -> run same eval
  -> compare quality + latency + memory
```

没有 baseline，量化结果没法解释。

## 5. 速度不一定更快

量化后显存通常更省，但速度要看 kernel：

| 情况 | 可能结果 |
| --- | --- |
| 有高效 INT4/INT8 kernel | 速度提升 |
| kernel 不匹配 | 反而变慢 |
| batch 很小 | 加速不明显 |
| CPU offload | 显存省了，延迟可能差 |
| KV cache 仍然很大 | 长上下文瓶颈没解决 |

所以性能报告要写：

```text
model:
quantization:
backend:
hardware:
batch/concurrency:
input/output length:
memory:
latency:
quality:
```

## 6. 和部署后端的关系

| 后端 | 关注点 |
| --- | --- |
| Transformers | 能否加载量化权重，适合实验 |
| vLLM | 是否支持该量化格式和 serving kernel |
| TGI | 是否支持该模型和量化方式 |
| llama.cpp | GGUF 生态，适合本地轻量部署 |
| TensorRT-LLM | NVIDIA 生态里的强部署路径 |
| CANN / MindSpeed-LLM | 昇腾生态要看模型、算子和转换支持 |

量化格式不是孤立文件。能不能跑，取决于后端支持。

## 7. 简历里怎么写

弱写法：

```text
熟悉 INT4/INT8 量化。
```

强写法：

```text
完成 FP16 与 4-bit 量化模型的推理对比，记录显存、TTFT、p90 latency 和固定评测集质量变化；分析量化格式、推理后端 kernel 支持和 KV cache 对长上下文服务的影响。
```

## 参考

- Transformers quantization overview: https://huggingface.co/docs/transformers/quantization/overview
- bitsandbytes docs: https://huggingface.co/docs/bitsandbytes
- PEFT LoRA guide: https://huggingface.co/docs/peft/developer_guides/lora
- QLoRA paper: https://arxiv.org/abs/2305.14314
- llama.cpp: https://github.com/ggml-org/llama.cpp

