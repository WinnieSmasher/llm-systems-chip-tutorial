# 13. 模型评测与 Benchmark

评测不是最后补一张分数表。它应该在项目一开始就有：先固定题目、输入格式、输出判定规则，再去改数据、微调、量化和部署。

一个大模型项目至少要有三类评测：

```text
离线能力评测：模型会不会答
服务性能评测：模型答得快不快、稳不稳
安全与边界评测：模型在恶意输入下是否会越权、泄露信息或误调用工具
```

## 1. 先区分 leaderboard 和项目评测

leaderboard 用来判断一个模型大概强不强。项目评测用来判断你的系统是否能上线。

| 评测 | 关心什么 | 例子 |
| --- | --- | --- |
| 通用能力 benchmark | 知识、推理、数学、代码、语言理解 | MMLU、GSM8K、HumanEval |
| 领域评测 | 你的业务题目、术语、格式要求 | 金融研报问答、医学病例摘要、游戏运营分析 |
| 回归评测 | 新版本有没有把旧能力弄坏 | 固定 100 条线上问题 |
| 服务评测 | TTFT、TPOT、吞吐、错误率、显存 | vLLM/TGI/OpenAI-compatible server benchmark |
| 安全评测 | prompt injection、敏感信息、越权工具调用 | OWASP LLM Top 10 相关用例 |

不要只看一个总分。一个模型在通用榜单上很高，不代表它能按你的格式稳定输出 JSON，也不代表它适合低延迟服务。

## 2. 常用评测框架

| 工具 | 适合什么 | 入口 |
| --- | --- | --- |
| `lm-evaluation-harness` | 标准 NLP/LLM benchmark，适合复现实验分数 | EleutherAI 官方仓库 |
| OpenCompass | 中文和多模型评测生态，适合批量跑公开数据集 | OpenCompass 官方仓库 |
| OpenAI Evals | 写自定义 eval、做 LLM system 回归测试 | OpenAI Evals 仓库 |
| LightEval | Hugging Face 生态里的 lightweight eval | Hugging Face docs |
| 自己写 JSONL eval | 小项目、课程项目、简历项目 | `examples/evaluate_predictions.py` |

先用公开框架建立评测概念，再写自己的小评测集。不要反过来一开始就造一个很复杂的评测平台。

## 3. 一条最小可用评测链路

```text
prompts.jsonl
  -> run model
  -> predictions.jsonl
  -> evaluate_predictions.py
  -> metrics.json
  -> changelog / experiment note
```

`predictions.jsonl` 可以长这样：

```jsonl
{"id":"cuda-001","prediction":"CUDA 是 NVIDIA GPU 的并行计算平台。","answer":"CUDA 是 NVIDIA GPU 的并行计算平台。","must_have":["NVIDIA","GPU"],"bad_patterns":["华为"]}
{"id":"cann-001","prediction":"CANN 是昇腾 NPU 的计算软件栈。","answer":"CANN 是昇腾 NPU 的计算软件栈。","must_have":["昇腾","NPU"],"bad_patterns":["ZLUDA"]}
```

然后跑：

```bash
python examples/evaluate_predictions.py \
  --input predictions.jsonl \
  --output metrics.json
```

这个脚本不会替代严肃 benchmark，但足够做版本回归。你要知道一次改动有没有把基础概念答错。

## 4. 指标的适用边界

| 指标 | 适合 | 不适合 |
| --- | --- | --- |
| exact match | 标准答案短、格式严格 | 开放问答 |
| contains / must-have | 概念解释、摘要覆盖 | 需要严密推理的题 |
| bad-pattern rate | 检查幻觉、禁用词、错概念 | 判断整体质量 |
| win rate | 两个模型或两个 prompt 对比 | 没有裁判标准时直接当真 |
| human review | 高风险输出、论文写作、代码建议 | 大规模自动回归 |

开放式答案不要强行用 exact match。更实用的办法是：先用 must-have 和 bad-pattern 做低成本筛查，再抽样人工看。

## 5. 评测集怎么做

一个小评测集也要有结构：

```text
30 条概念题：CUDA/CANN/ZLUDA/ONNX/LoRA/vLLM
30 条工程题：日志诊断、参数选择、OOM 原因
20 条格式题：固定 JSON 输出、表格输出
20 条安全题：拒答、注入、防越权
```

每条样本至少记录：

- `id`
- `prompt`
- `expected_behavior`
- `must_have`
- `bad_patterns`
- `source`
- `notes`

如果数据来自公开文档或论文，记录 URL。以后结果变差时，能追到题目来源。

## 6. 防止评测污染

评测污染有两种：

1. 训练数据里混进了测试题。
2. 调 prompt 时反复看测试集，等于把测试集当开发集。

实际项目里可以分三份：

```text
dev: 日常调 prompt 和脚本
regression: 每次改动都跑
holdout: 少看，只在阶段性版本跑
```

小项目不必做得很重，但至少要把“我用来调的题”和“我用来报结果的题”分开。

## 7. 性能评测要跟能力评测分开

性能报告里不要只写“更快”。写清楚场景：

| 项 | 记录 |
| --- | --- |
| model | 模型名、revision、量化方式 |
| backend | Transformers / vLLM / TGI / TensorRT-LLM / CANN |
| hardware | GPU/NPU 型号、显存、驱动、CANN/CUDA 版本 |
| input length | prompt tokens |
| output length | generated tokens |
| concurrency | 并发数 |
| metrics | TTFT、TPOT、p50/p90 latency、throughput、error rate |

性能数据没有环境信息，就很难复现。

## 8. 简历里怎么写

弱写法：

```text
熟悉大模型评测，了解 MMLU、GSM8K 等 benchmark。
```

强写法：

```text
搭建 120 条领域回归评测集，覆盖概念解释、格式遵循、RAG 引用和安全拒答；基于 JSONL 结果统计 exact match、must-have 命中率和 bad-pattern rate，用于 LoRA 微调与量化部署前后的版本对比。
```

强写法不是堆工具名，而是写清楚你控制了什么变量、产出了什么证据。

## 参考

- EleutherAI lm-evaluation-harness: https://github.com/EleutherAI/lm-evaluation-harness
- OpenCompass: https://github.com/open-compass/opencompass
- OpenAI Evals: https://github.com/openai/evals
- Hugging Face LightEval: https://huggingface.co/docs/lighteval
- OWASP Top 10 for LLM Applications: https://genai.owasp.org/llm-top-10/
