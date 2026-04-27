# 00. 学习地图

这份教程按工程学习顺序组织，不按名词表组织。主线是：

```text
模型来源
  -> 模型格式
  -> 数据清洗
  -> 微调和评测
  -> 推理服务
  -> 硬件后端
  -> RAG / Agent 应用
  -> 安全和复盘
```

读的时候不要急着追最新工具。先把每一层的问题说清楚，再看对应项目和源码。

## 课程结构

| 阶段 | 核心问题 | 对应章节 | 最小输出 |
| --- | --- | --- | --- |
| 1. 模型在哪里 | 模型 repo 里有哪些文件，tokenizer 和 chat template 为什么重要 | [02](02-model-formats.md), [03](03-huggingface-workflow.md) | 模型文件结构笔记 |
| 2. 怎么改模型 | SFT、LoRA、QLoRA、DPO 分别在改什么 | [04](04-training-finetuning-alignment.md), [14](14-data-engineering.md) | 一份 toy 数据和 smoke test |
| 3. 怎么判断变好 | baseline、评测集、bad case 怎么固定 | [13](13-evaluation-benchmark.md) | 20 条固定评测样例 |
| 4. 怎么跑得快 | prefill、decode、KV cache、batching、量化是什么关系 | [05](05-inference-optimization.md), [10](10-vllm-benchmark-guide.md), [16](16-quantization.md), [17](17-advanced-inference.md) | 一份 benchmark 记录 |
| 5. 跑在哪种硬件上 | CUDA、ZLUDA、CANN、AscendCL、ONNX、OM 的边界在哪里 | [01](01-hardware-stacks.md), [06](06-chip-domain-roadmap.md), [11](11-cuda-cann-api-map.md), [12](12-onnx-atc-om-flow.md) | 一张硬件/格式边界图 |
| 6. 怎么变成应用 | RAG、Agent、tool call、memory 怎么接到系统里 | [15](15-rag-agent-engineering.md), [19](19-safety-ops.md) | 一组 RAG 失败样例 |
| 7. 怎么持续学习 | 论文、源码、开源项目如何转成练习 | [20](20-paper-reading-roadmap.md), [21](21-knowledge-extraction-map.md), [22](22-eight-week-learning-route.md), [23](23-source-reading-questions.md) | 一页源码阅读笔记 |

开始之前，先读 [00C. 学习协议](00-study-contract.md)。它规定了这份教程的完成标准：每章都要有读前问题、最小产出和自检记录。

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
- [10. vLLM Benchmark Guide](10-vllm-benchmark-guide.md)
- [16. 量化专题](16-quantization.md)
- [17. 高级推理优化](17-advanced-inference.md)
- [18. 分布式训练与并行策略](18-distributed-training.md)

## 第五层：模型跑在哪种硬件生态上

这里最容易混：

- CUDA 是 NVIDIA GPU 原生生态。
- ZLUDA 是 CUDA 兼容层。
- CANN 是华为 Ascend NPU 原生生态。
- ONNX 是模型交换格式，不是硬件后端。

对应章节：

- [01. CUDA、ZLUDA 与昇腾 CANN](01-hardware-stacks.md)
- [06. 集成电路与 AI 芯片学习路线](06-chip-domain-roadmap.md)
- [11. CUDA / CANN API Map](11-cuda-cann-api-map.md)
- [12. ONNX -> ATC -> OM -> AscendCL](12-onnx-atc-om-flow.md)

## 第六层：模型怎么变成应用

真实应用里经常会接 RAG、工具调用和上线监控。这里要格外小心：检索内容、网页内容和工具返回都不是可信指令。

对应章节：

- [15. RAG 与 Agent 工程](15-rag-agent-engineering.md)
- [19. 大模型安全与上线运维](19-safety-ops.md)
- [20. 论文阅读路线](20-paper-reading-roadmap.md)

## 第七层：怎么读开源和论文

开源项目不是目录装饰。每个项目都要回答一个问题：

- 它解释了哪个系统概念？
- 它有没有可复现的实验？
- 它的源码能不能拆成一个阅读题？
- 它能不能变成一次小贡献？

对应章节：

- [21. 开源项目知识提炼地图](21-knowledge-extraction-map.md)
- [22. 八周能力路线](22-eight-week-learning-route.md)
- [23. 源码阅读题单](23-source-reading-questions.md)
- [09. Source Reading Notes](09-source-reading-notes.md)

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
