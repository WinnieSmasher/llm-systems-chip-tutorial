# 08. Hands-on Labs

这一章放可以直接动手的小实验。实验不追求大，先把链路打通。

## Lab 1: Transformers 最小推理

目标：确认模型、tokenizer、chat template 能正常工作。

```bash
python examples/minimal_inference.py
```

记录：

- 模型名和 revision。
- 显卡/CPU/NPU 环境。
- 输入 prompt。
- 输出结果。
- 是否需要 `trust_remote_code`。

不要一上来改训练脚本。先确认模型能稳定推理。

## Lab 2: LoRA SFT smoke test

目标：确认 PEFT/TRL 训练链路能跑通。

```bash
python examples/minimal_sft_lora.py
```

这个脚本只是 smoke test，不是最终训练方案。跑通后再换自己的数据集。

检查点：

- 是否能加载 dataset。
- 是否能插入 LoRA adapter。
- 是否能完成一个短训练。
- 是否能保存 adapter。

## Lab 3: KV Cache 显存估算

目标：理解为什么长上下文和高并发容易爆显存。

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

输出会给出粗略 KV cache 显存。这个估算不等于框架真实占用，但足够说明趋势。

## Lab 4: vLLM OpenAI-compatible client

先启动服务：

```bash
vllm serve Qwen/Qwen2.5-0.5B-Instruct
```

再调用：

```bash
python examples/vllm_client.py
```

记录：

- TTFT。
- 总延迟。
- 输出 token 数。
- 并发数变化后的吞吐。

## Lab 5: vLLM 教学版压测

启动服务后：

```bash
python examples/benchmark_openai_server.py \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --prompt "请比较 CUDA、ZLUDA、CANN 在大模型部署链路中的位置。" \
  --requests 16 \
  --concurrency 4 \
  --max-tokens 128 \
  --stream
```

把结果填到：

```text
benchmarks/results-template.csv
```

更详细说明见 [10. vLLM Benchmark Guide](10-vllm-benchmark-guide.md)。

## Lab 6: KV Cache sweep

```bash
python examples/kv_cache_sweep.py \
  --layers 32 \
  --heads 32 \
  --kv-heads 8 \
  --head-dim 128 \
  --seq-lens 1024,2048,4096,8192 \
  --batch-sizes 1,4,8,16 \
  --output benchmarks/kv-cache-sweep.csv
```

观察 `seq_len` 和 `batch_size` 怎么把 KV cache 显存推高。

## Lab 7: 做一张对照表

自己整理一张表，至少包括：

| 问题 | NVIDIA 生态 | 昇腾生态 |
| --- | --- | --- |
| 设备初始化 | CUDA runtime | AscendCL |
| 自定义 kernel/operator | CUDA kernel | Ascend C |
| 高性能矩阵/深度学习算子 | cuBLAS/cuDNN | CANN operators |
| 多卡通信 | NCCL | HCCL |
| 模型转换部署 | TensorRT/ONNX Runtime | ATC/OM/AscendCL |

这张表如果能解释清楚，CUDA/CANN/ZLUDA 就不会混了。

可以对照 [11. CUDA / CANN API Map](11-cuda-cann-api-map.md) 继续补。

## Lab 8: 写一份 ONNX -> OM 转换记录

没有昇腾机器也可以先写模板。有机器时把真实日志补上。

```text
model:
CANN version:
soc_version:
ATC command:
conversion result:
runtime result:
accuracy comparison:
```

流程见 [12. ONNX -> ATC -> OM -> AscendCL](12-onnx-atc-om-flow.md)。
