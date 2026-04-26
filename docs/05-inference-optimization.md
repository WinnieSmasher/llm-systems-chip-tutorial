# 05. 推理优化与部署

训练完模型只是第一步。真正上线时，你还会关心：

- 生成速度快不快。
- 显存够不够。
- 多用户并发能不能扛住。
- 延迟是否稳定。
- 部署到 NVIDIA GPU、AMD GPU、昇腾 NPU 的路线是否不同。

## 1. 推理为什么慢

大模型推理通常分成两个阶段：

```text
prefill: 处理输入 prompt
decode: 一个 token 一个 token 生成输出
```

长 prompt 会让 prefill 压力变大。  
长输出会让 decode 时间变长。  
并发用户多了以后，KV cache 会占大量显存。

## 2. KV Cache

Transformer 每生成一个 token，都需要 attention。

KV Cache 的作用是缓存历史 token 的 key/value，避免每一步重复计算全部历史内容。

通俗理解：

```text
不使用 KV Cache：每说一个字，都把前文重新读一遍
使用 KV Cache：记住前文的中间结果，只算新增部分
```

KV Cache 能显著提高长文本生成效率，但会占显存。

## 3. FlashAttention

FlashAttention 优化的是 attention 的计算和显存访问。

它不改变模型数学含义，主要让 attention 更快、更省显存。

适合：

- 长上下文。
- 大 batch。
- 训练和推理中的 attention 计算优化。

## 4. Quantization 量化

量化是把权重和/或激活从高精度压到低精度。

常见精度：

```text
FP32
BF16 / FP16
INT8
INT4
```

优点：

- 更省显存。
- 更容易放进单卡。
- 推理可能更快。

风险：

- 精度下降。
- 部分任务更容易退化。
- 不同硬件对 INT4/INT8 支持差异很大。

## 5. vLLM 是什么

vLLM 是高吞吐大模型推理服务框架。

它的关键词：

- PagedAttention
- continuous batching
- prefix caching
- OpenAI-compatible API server
- tensor parallel
- quantization support

最简单启动方式：

```bash
vllm serve Qwen/Qwen2.5-0.5B-Instruct
```

然后可以像调用 OpenAI API 一样调用本地服务。

## 6. TensorRT-LLM、TGI、llama.cpp 怎么选

| 工具 | 更适合 |
| --- | --- |
| vLLM | GPU 服务端高吞吐在线推理 |
| TGI | Hugging Face 生态的生产推理服务 |
| TensorRT-LLM | NVIDIA GPU 上追求极致性能 |
| llama.cpp | CPU/消费级设备/本地轻量部署 |
| ONNX Runtime | 跨平台推理部署 |
| CANN/AscendCL | 华为昇腾 NPU 推理部署 |

## 7. 昇腾 NPU 推理路线

如果走昇腾静态图推理，常见路线：

```text
PyTorch / ONNX
  -> ATC
  -> .om
  -> AscendCL
  -> Ascend NPU
```

如果走 PyTorch 生态适配：

```text
PyTorch
  -> torch_npu
  -> CANN
  -> Ascend NPU
```

如果现成算子不支持：

```text
自定义逻辑
  -> Ascend C 自定义算子
  -> CANN 编译/注册
  -> 模型调用
```

## 8. 推理优化的指标

不要只看“速度快不快”。建议同时记录：

- TTFT：time to first token，首 token 延迟。
- TPOT：time per output token，单 token 生成时间。
- throughput：每秒生成 token 数。
- latency：请求总延迟。
- GPU/NPU memory：显存/设备内存占用。
- concurrency：并发能力。
- quality：模型质量是否因量化或部署转换下降。

## 9. 一个部署前 checklist

1. 确认模型 license 允许部署。
2. 固定 model revision，避免线上版本漂移。
3. 固定 tokenizer 和 chat template。
4. 对比部署前后输出质量。
5. 记录显存、吞吐、延迟。
6. 准备 fallback 模型或降级策略。
7. 加监控、日志和异常样本回收。

