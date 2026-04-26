# 17. 高级推理优化

推理优化不是只换 vLLM。真正要看的是请求在后端里怎么走：prefill、decode、KV cache、batching、scheduler、kernel、并行策略。

## 1. Prefill 和 Decode

```text
prefill: 处理完整输入 prompt，生成第一步 KV cache
decode: 每次生成一个新 token，不断复用 KV cache
```

长 prompt 主要拖慢 prefill。长输出主要拖慢 decode。

所以要分开看指标：

| 指标 | 说明 |
| --- | --- |
| TTFT | time to first token，首 token 延迟 |
| TPOT | time per output token，后续 token 平均时间 |
| throughput | 单位时间输出 token 数 |
| p50/p90/p99 latency | 不同尾延迟 |
| error rate | 超时、OOM、服务错误 |

## 2. Continuous batching

传统 batching 要等一批请求一起进来。LLM 服务里请求长度不同，等待会浪费设备。

continuous batching 的思路是：decode 过程中不断把新请求插进来，让 GPU/NPU 尽量保持忙。

代价也明显：

- 单请求延迟可能变高。
- scheduler 更复杂。
- KV cache 管理更重要。

看吞吐时也要看尾延迟。只报 tokens/s 很容易误导。

## 3. PagedAttention 和 KV cache

KV cache 会随 batch size 和 sequence length 增长。PagedAttention 的核心直觉是像操作系统管理虚拟内存一样管理 KV cache block，减少浪费，支持更灵活的调度。

这就是 vLLM 常被拿来讲高吞吐服务的原因之一。

可以先跑：

```bash
python examples/estimate_kv_cache.py \
  --layers 32 \
  --heads 32 \
  --kv-heads 8 \
  --head-dim 128 \
  --seq-len 8192 \
  --batch-size 8 \
  --dtype-bytes 2
```

再用：

```bash
python examples/kv_cache_sweep.py \
  --layers 32 \
  --heads 32 \
  --kv-heads 8 \
  --head-dim 128 \
  --seq-lens 1024,2048,4096,8192,16384 \
  --batch-sizes 1,4,8,16
```

你会直观看到长上下文和并发为什么吃显存。

## 4. Speculative Decoding

speculative decoding 的思路：用一个小模型或 draft 机制先猜几个 token，再让大模型验证。猜对了就一次接受多个 token，猜错了回退。

它适合：

- decode-bound 场景。
- 大模型验证很贵，小模型草稿便宜。
- 输出分布比较容易预测的任务。

它不一定适合：

- draft model 和 target model 差太多。
- prompt 很短但服务瓶颈在调度。
- 系统已经被 memory bandwidth 或通信卡住。

vLLM 文档有 speculative decoding 相关功能，但具体效果要实测，不要只看概念。

## 5. Prefix caching

如果大量请求共享同一段系统 prompt、工具说明、文档前缀，可以缓存 prefix 的 KV。

适合：

- 固定 system prompt。
- RAG 模板里前缀很长。
- 多轮对话共享历史。

不适合：

- 每个请求前缀都不同。
- prefix 经常变。
- 业务不能接受缓存命中不稳定带来的延迟波动。

## 6. Tensor Parallel 和 Pipeline Parallel

单卡放不下或吞吐不够时，推理也会用并行：

| 策略 | 直觉 | 代价 |
| --- | --- | --- |
| tensor parallel | 把矩阵乘切到多卡 | 通信频繁 |
| pipeline parallel | 把层切到多卡 | pipeline bubble |
| expert parallel | MoE 专家分布到多卡 | 路由和 all-to-all |

推理并行不是卡越多越快。小模型、小 batch、短输出时，多卡通信可能把收益吃掉。

## 7. 一份像样的推理实验

至少跑这些变量：

```text
backend: Transformers / vLLM
precision: BF16 / INT8 / INT4
input length: 128 / 1024 / 4096
output length: 128 / 512
concurrency: 1 / 4 / 16
```

记录：

- TTFT p50/p90。
- total latency p50/p90。
- throughput。
- peak memory。
- error/OOM。
- 输出质量变化。

## 8. 简历里怎么写

弱写法：

```text
熟悉 vLLM、PagedAttention 和推理优化。
```

强写法：

```text
基于 OpenAI-compatible API 搭建 vLLM 推理压测流程，按 input length、output length 和 concurrency 记录 TTFT、p90 latency、throughput 与显存变化，并结合 KV cache 估算解释长上下文服务的瓶颈。
```

## 参考

- vLLM docs: https://docs.vllm.ai/
- vLLM speculative decoding: https://docs.vllm.ai/en/latest/features/spec_decode/
- PagedAttention paper: https://arxiv.org/abs/2309.06180
- Text Generation Inference: https://huggingface.co/docs/text-generation-inference
- TensorRT-LLM: https://github.com/NVIDIA/TensorRT-LLM

