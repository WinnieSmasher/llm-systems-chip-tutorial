# Archived Draft: 模型评测与 Benchmark

这是早期草稿，保留是为了避免本地复数命名文件丢失。正式章节请读 [13. 模型评测与 Benchmark](../13-evaluation-benchmark.md)。

下面内容不再维护，命令和字段可能落后于当前脚本。

# 13. 模型评测与 Benchmark

训练、量化、RAG、推理优化都绕不开评测。没有评测集，所有“效果变好了”都很可疑。

这一章只讲一个原则：

> 先把评测固定下来，再谈训练和优化。

## 1. 评测分两类

### 能力评测

关心模型回答对不对。

常见形式：

- multiple choice：MMLU、C-Eval 这类。
- exact match / F1：问答、抽取。
- code pass@k：代码生成。
- pairwise preference：两个回答哪个更好。
- 人工 rubric：按事实性、完整性、格式、引用打分。

工具入口：

- EleutherAI `lm-evaluation-harness`
- OpenCompass
- HELM
- 自己写的小型 eval set

### 系统评测

关心模型服务跑得怎样。

常见指标：

- TTFT
- TPOT
- tokens/s
- p50/p90/p99 latency
- concurrency
- GPU/NPU memory
- error rate
- cost per 1K tokens

工具入口：

- vLLM benchmark scripts
- 本仓库的 `examples/benchmark_openai_server.py`
- Prometheus / OpenTelemetry / service logs

## 2. 为什么要有小评测集

大型 benchmark 能提供横向比较，但很难代表你的任务。

建议先做一个 50 到 200 条的小评测集：

```json
{
  "id": "hardware_stack_001",
  "question": "华为昇腾 CANN 和 ZLUDA 是什么关系？",
  "must_have": [
    "CANN 是 Ascend NPU 原生软件栈",
    "ZLUDA 是 CUDA 兼容层",
    "二者不是同一层"
  ],
  "bad_patterns": [
    "昇腾就是 ZLUDA",
    "CANN 是 ONNX 的一种"
  ]
}
```

这个评测集应该在训练前就存在。

## 3. 最小评测脚本

本仓库提供：

```bash
python examples/evaluate_predictions.py \
  --gold data/eval_examples.jsonl \
  --pred outputs/predictions.jsonl
```

输入格式：

```json
{"id": "q1", "must_have": ["CUDA", "NVIDIA"], "bad_patterns": ["华为版 CUDA"]}
{"id": "q1", "answer": "CUDA 是 NVIDIA 的 GPU 计算生态..."}
```

它不是替代 lm-eval-harness，只是帮助你先把任务相关的“必须包含/不能出现”固定下来。

## 4. 常见误区

### 只看训练 loss

loss 降低不等于任务变好。模型可能学会了训练集格式，但事实性变差。

### 只跑公开 benchmark

公开 benchmark 有用，但不等于你的业务任务。微调项目至少要有一套自定义 eval set。

### 用 LLM 当裁判但不抽查

LLM-as-a-judge 很方便，但会受 prompt、模型偏好、答案长度影响。重要样本仍然要人工抽查。

### 量化后只看速度

量化后必须重新跑质量评测。INT4 更省显存，不代表对你的任务无损。

## 5. 推荐记录表

```text
model:
revision:
dataset version:
eval set version:
training method:
precision:
backend:
quality metrics:
latency metrics:
memory:
observed failures:
decision:
```

## 参考

- EleutherAI lm-evaluation-harness: https://github.com/EleutherAI/lm-evaluation-harness
- OpenCompass: https://github.com/open-compass/opencompass
- HELM: https://crfm.stanford.edu/helm/
- vLLM benchmark docs and scripts: https://docs.vllm.ai/
