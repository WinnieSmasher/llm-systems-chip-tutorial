# 10. vLLM Benchmark Guide

这一章不是替代 vLLM 官方 benchmark。官方仓库里有更完整的 `benchmark_serving.py`、`benchmark_latency.py` 等脚本。这里放的是教学版，目的是让你先把几个核心指标跑出来。

## 1. 先启动服务

```bash
vllm serve Qwen/Qwen2.5-0.5B-Instruct
```

如果模型需要更多显存，可以先换更小的模型或降低 `--max-model-len`。

## 2. 跑单场景压测

```bash
python examples/benchmark_openai_server.py \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --prompt "用四句话解释 KV Cache 为什么影响 LLM 推理显存。" \
  --requests 16 \
  --concurrency 4 \
  --max-tokens 128 \
  --stream
```

输出是 JSON，重点看：

- `latency_p50_s`
- `latency_p90_s`
- `ttft_p50_s`
- `ttft_p90_s`
- `output_chars_per_s`

脚本用 Python 标准库写，减少环境依赖。它统计的是教学指标，不是严格 tokenizer-level throughput。正式 benchmark 应该使用 vLLM 官方脚本或把返回 token usage 纳入统计。

## 3. 为什么要开 stream

非 streaming 请求只能测总延迟。  
streaming 请求可以估算 TTFT，首 token 延迟。

```text
TTFT 高：用户等第一句话出来很久
TPOT 高：后续生成一个 token 一个 token 慢
```

在线聊天应用里，TTFT 会直接影响体感。

## 4. 建议实验矩阵

至少跑这些组合：

| input length | output length | concurrency |
| --- | --- | --- |
| 128 | 128 | 1 |
| 512 | 128 | 4 |
| 2048 | 128 | 8 |
| 4096 | 256 | 16 |

每组记录到：

```text
benchmarks/results-template.csv
```

## 5. 结果怎么解释

### 并发增加，吞吐提高但延迟变差

这是常见现象。continuous batching 会提高设备利用率，但单个请求可能排队。

### 输入长度增加，TTFT 变差

prefill 阶段要处理全部输入 token，长 prompt 会拉高首 token 延迟。

### 输出长度增加，总延迟变差

decode 是逐 token 生成，输出越长，总时间越长。

### 显存不够

常见原因：

- 模型权重太大。
- KV cache 太大。
- `max_model_len` 太高。
- batch/concurrency 太高。
- 精度太高。

## 6. 和官方 benchmark 的关系

这个仓库的脚本适合学习和快速验证。要做严肃性能报告，继续看：

- vLLM 官方 benchmark scripts。
- vLLM docs 的 serving 配置。
- PagedAttention paper。

## 参考

- vLLM docs: https://docs.vllm.ai/
- vLLM GitHub: https://github.com/vllm-project/vllm
- PagedAttention paper: https://arxiv.org/abs/2309.06180

