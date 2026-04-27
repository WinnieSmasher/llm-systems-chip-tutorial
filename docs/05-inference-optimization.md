# 05. 推理优化和部署

训练完模型不代表能上线。上线时最烦的是这些问题：

- 首 token 慢。
- 并发一高就爆显存。
- 长上下文把 KV cache 撑满。
- 同一个模型在 Transformers 里能跑，在服务框架里输出变了。
- 换硬件后算子不支持。

推理优化的目标不是“玄学加速”，而是把延迟、吞吐、显存和质量放在一起权衡。

## 本章怎么学

读前问题：

- TTFT、TPOT、tokens/s 分别对应推理服务的哪个侧面？
- prefill 和 decode 为什么要分开看？
- KV cache 为什么会限制长上下文和高并发？

课后产出：

- 用 `examples/estimate_kv_cache.py` 或 `examples/kv_cache_sweep.py` 做一张显存估算表。
- 写一个 benchmark scenario，固定模型、输入长度、输出长度、并发和硬件。

自检标准：

- 能解释为什么“单条 prompt 很快”不能代表服务性能好。
- 能说明量化后为什么必须重新跑评测。

## 1. Prefill 和 Decode

LLM 推理分两段：

```text
prefill: 处理输入 prompt
decode: 逐 token 生成输出
```

输入越长，prefill 越重。  
输出越长，decode 越久。  
并发越高，KV cache 越吃显存。

## 2. KV Cache 为什么重要

Transformer decode 时，每生成一个新 token，都要参考前文。如果每次都重新算全部历史 token，太浪费。

KV Cache 保存历史 token 的 key/value。

粗略估算：

```text
KV cache memory
≈ 2 * num_layers * batch_size * seq_len * hidden_size * bytes_per_element
```

真实模型还要考虑 GQA/MQA、tensor parallel、block size、padding 和框架实现。这个公式只是帮你建立直觉：`seq_len` 和 `batch_size` 一涨，显存压力会很快上来。

## 3. vLLM 为什么常被拿来部署

vLLM 的核心卖点不是“换个 API 名字”，而是更高效地管理请求和 KV cache。

官方文档里几个关键词：

- PagedAttention：把 KV cache 分块管理，减少碎片和浪费。
- continuous batching：服务端动态合批，不是等一整批请求齐了再跑。
- prefix caching：相同前缀可以复用。
- OpenAI-compatible API：客户端可以像调用 OpenAI API 一样调用本地模型。

最小启动：

```bash
vllm serve Qwen/Qwen2.5-0.5B-Instruct
```

调用：

```python
from openai import OpenAI

client = OpenAI(
    api_key="EMPTY",
    base_url="http://localhost:8000/v1",
)

resp = client.chat.completions.create(
    model="Qwen/Qwen2.5-0.5B-Instruct",
    messages=[{"role": "user", "content": "解释 KV Cache"}],
)

print(resp.choices[0].message.content)
```

## 4. 量化不是白嫖

量化把权重或激活从高精度变低精度：

```text
FP32 -> BF16/FP16 -> INT8 -> INT4
```

好处：

- 显存占用下降。
- 某些硬件上吞吐提升。
- 更大的模型可以放进单卡。

代价：

- 质量可能下降。
- 长推理或数学任务可能更敏感。
- 不同框架支持的量化格式不一样。
- 某些硬件对 INT4 的加速不一定理想。

所以量化后必须重新跑评测集。

## 5. FlashAttention 优化的是什么

FlashAttention 主要减少 attention 里的显存读写和中间张量开销。它不改变 Transformer 的数学目标，但改变计算组织方式。

如果你做长上下文训练或推理，需要知道它解决的是 memory IO 问题，而不是“让模型更聪明”。

## 6. NVIDIA、CPU、本地轻量、昇腾各走哪条路

| 场景 | 常用工具 |
| --- | --- |
| NVIDIA GPU 在线服务 | vLLM / TGI / TensorRT-LLM |
| 本地轻量 CPU/消费级设备 | llama.cpp / GGUF |
| 跨平台部署 | ONNX Runtime |
| 华为昇腾 PyTorch 适配 | torch_npu / MindSpeed-LLM |
| 华为昇腾静态推理 | ONNX -> ATC -> OM -> AscendCL |

## 7. 昇腾部署时多出来的事

在 CUDA 生态里，你可能习惯了 PyTorch + CUDA 直接跑。

到了昇腾，如果做静态推理，常见问题会变成：

- ONNX 导出是否成功？
- ATC 是否支持图里的算子？
- shape 是动态还是静态？
- 模型转换后精度是否一致？
- AscendCL 输入输出内存布局是否正确？
- 不支持的算子是否需要 Ascend C 自定义实现？

这就是为什么 CANN 不是“华为版 ZLUDA”。它是另一条部署生态。

## 8. 该记录哪些指标

建议至少记录：

| 指标 | 含义 |
| --- | --- |
| TTFT | Time To First Token，首 token 延迟 |
| TPOT | Time Per Output Token，生成阶段单 token 时间 |
| tokens/s | 吞吐 |
| request latency | 单请求总延迟 |
| GPU/NPU memory | 设备内存占用 |
| concurrency | 并发能力 |
| quality | 输出质量有没有因为量化/转换下降 |

只说“速度提升明显”没有意义。把数字写出来。

## 9. 一个压测实验怎么做

固定模型和机器，变化这些变量：

```text
input length: 128 / 512 / 2048 / 8192
output length: 128 / 512
concurrency: 1 / 4 / 16 / 64
precision: BF16 / INT8 / INT4
```

记录：

- TTFT
- tokens/s
- 显存峰值
- 是否 OOM
- 输出是否异常

这比只跑一个聊天 demo 更有价值。

## 参考

- vLLM docs: https://docs.vllm.ai/
- PagedAttention paper: https://arxiv.org/abs/2309.06180
- FlashAttention paper: https://arxiv.org/abs/2205.14135
- Hugging Face TGI: https://huggingface.co/docs/text-generation-inference
- llama.cpp: https://github.com/ggml-org/llama.cpp
- Huawei Ascend CANN: https://www.hiascend.com/en/cann

