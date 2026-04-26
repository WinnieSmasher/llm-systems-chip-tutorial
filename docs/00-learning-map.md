# 00. 学习地图

这份教程按一条工程链路组织，不按名词表组织。

```text
Hugging Face 模型
  -> PyTorch/Transformers 推理 baseline
  -> 数据清洗和评测集
  -> SFT / LoRA / QLoRA / DPO
  -> 量化和推理优化
  -> RAG / Agent 应用
  -> CUDA / CANN / vLLM 等部署后端
  -> 安全、监控和下一轮迭代
```

## 第一层：模型从哪里来

先学 Hugging Face Hub 和 Transformers：

- 模型 repo 里有哪些文件。
- tokenizer 和 chat template 为什么重要。
- `AutoModelForCausalLM` 和 `AutoTokenizer` 怎么加载模型。
- model card 里的 license 和限制怎么读。

对应章节：

- [02. PyTorch、ONNX、safetensors 和 OM](02-model-formats.md)
- [03. Hugging Face 项目从哪里开始](03-huggingface-workflow.md)

## 第二层：模型怎么被训练和微调

把这些词放到正确位置：

- continued pretraining：继续读领域语料。
- SFT：学 instruction-response。
- LoRA：少量 adapter 参数更新。
- QLoRA：低比特 base model + LoRA。
- DPO：用 chosen/rejected 偏好样本做对齐。

对应章节：

- [04. SFT、LoRA、QLoRA、DPO 到底在训什么](04-training-finetuning-alignment.md)
- [14. 数据工程与数据清洗](14-data-engineering.md)

## 第三层：怎么知道改动有没有变好

模型项目不能只靠“看起来回答不错”。要固定评测集，记录 baseline，再比较微调、量化、prompt 和后端变化。

对应章节：

- [13. 模型评测与 Benchmark](13-evaluation-benchmark.md)

## 第四层：模型怎么跑得快

推理优化不是“换个框架就快”。你要看：

- prefill / decode。
- KV cache。
- continuous batching。
- quantization。
- attention kernel。
- serving framework。

对应章节：

- [05. 推理优化和部署](05-inference-optimization.md)
- [16. 量化专题](16-quantization.md)
- [17. 高级推理优化](17-advanced-inference.md)

## 第五层：模型跑在哪种硬件生态上

这里最容易混：

- CUDA 是 NVIDIA GPU 原生生态。
- ZLUDA 是 CUDA 兼容层。
- CANN 是华为 Ascend NPU 原生生态。
- ONNX 是模型交换格式，不是硬件后端。

对应章节：

- [01. CUDA、ZLUDA 与昇腾 CANN](01-hardware-stacks.md)
- [06. 集成电路与 AI 芯片学习路线](06-chip-domain-roadmap.md)
- [18. 分布式训练与并行策略](18-distributed-training.md)

## 第六层：模型怎么变成应用

真实应用里经常会接 RAG、工具调用和上线监控。这里要格外小心：检索内容、网页内容和工具返回都不是可信指令。

对应章节：

- [15. RAG 与 Agent 工程](15-rag-agent-engineering.md)
- [19. 大模型安全与上线运维](19-safety-ops.md)
- [20. 论文阅读路线](20-paper-reading-roadmap.md)

## 最小实践路线

建议不要光读。按这个顺序做：

1. 用 `examples/minimal_inference.py` 跑一个小模型。
2. 用 `examples/clean_sft_jsonl.py` 清洗一份 toy SFT 数据。
3. 建 20 条固定评测样例，并用 `examples/evaluate_predictions.py` 跑回归。
4. 用 `examples/minimal_sft_lora.py` 跑一个小 LoRA smoke test。
5. 用 `examples/chunk_text_preview.py` 看一次 RAG chunking 效果。
6. 用 vLLM 起一个 OpenAI-compatible 服务。
7. 测 input length、output length、concurrency 对延迟和显存的影响。
8. 用 `examples/kv_cache_sweep.py` 写一张 KV cache 估算表。
9. 写一页实验报告。

最后能写成简历的不是“熟悉很多名词”，而是你真的测过、对比过、解释过。
