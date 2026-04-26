# LLM Systems and AI Chips Tutorial

## 教程说明

这个仓库用来整理 LLM 系统工程和 AI 芯片相关的学习笔记。

内容按一条工程链路写：

```text
模型从哪里来
  -> 数据怎么清洗和评测
  -> 模型怎么微调
  -> 推理服务怎么部署
  -> 性能瓶颈怎么分析
  -> CUDA / ZLUDA / CANN 这些硬件生态放在哪里
  -> 最后怎么形成实验记录、源码阅读笔记和开源贡献计划
```

仓库里的文档不是一次性写完的教材。更准确地说，它是一份学习手册：读一章，跑一个小实验，补一条笔记，再回头改目录。

![LLM systems learning map](assets/image2-llm-systems-cover.png)

## 适合谁读

适合这些情况：

- 想从 Hugging Face 模型一路学到推理服务和系统优化。
- 想分清 CUDA、ZLUDA、CANN、ONNX、vLLM、TensorRT-LLM 这些词各自在哪一层。
- 想做一点能放到 GitHub 上的 LLM systems / AI infra / chip learning 项目。
- 想把收藏的开源项目变成学习路线，而不是只停在 star 列表。

不适合这些情况：

- 想找速成面经。
- 想直接复制简历 bullet。
- 想找现成大模型训练平台。
- 想学高频交易、投机策略或灰色工具用法。

## 建议读法

第一次读不要按目录从头到尾读。先按自己的目标选一条线。

### 1. 只想分清硬件和模型格式

先读：

- [01. CUDA、ZLUDA 与昇腾 CANN](docs/01-hardware-stacks.md)
- [02. PyTorch、ONNX、safetensors 和 OM](docs/02-model-formats.md)
- [11. CUDA / CANN API Map](docs/11-cuda-cann-api-map.md)
- [12. ONNX -> ATC -> OM -> AscendCL](docs/12-onnx-atc-om-flow.md)

读完以后，至少要能解释：

- CUDA 为什么不是“所有 GPU 通用接口”。
- ZLUDA 为什么不是华为昇腾生态。
- ONNX 和 `.om` 文件分别在哪一步出现。

### 2. 想做一个 Hugging Face 小项目

先读：

- [03. Hugging Face 项目从哪里开始](docs/03-huggingface-workflow.md)
- [04. SFT、LoRA、QLoRA、DPO 到底在训什么](docs/04-training-finetuning-alignment.md)
- [13. 模型评测与 Benchmark](docs/13-evaluation-benchmark.md)
- [14. 数据工程与数据清洗](docs/14-data-engineering.md)

配套练习：

- 跑 `examples/minimal_inference.py`。
- 用 `examples/clean_sft_jsonl.py` 清洗一份小数据。
- 用 `examples/evaluate_predictions.py` 做一个固定评测集。

### 3. 想学推理优化和部署

先读：

- [05. 推理优化和部署](docs/05-inference-optimization.md)
- [10. vLLM Benchmark Guide](docs/10-vllm-benchmark-guide.md)
- [16. 量化专题](docs/16-quantization.md)
- [17. 高级推理优化](docs/17-advanced-inference.md)
- [18. 分布式训练与并行策略](docs/18-distributed-training.md)

配套练习：

- 用 `examples/vllm_client.py` 调一个 OpenAI-compatible 服务。
- 用 `examples/benchmark_openai_server.py` 记录 TTFT、TPOT 和 tokens/s。
- 用 `examples/kv_cache_sweep.py` 估算不同上下文长度的 KV cache 显存。

### 4. 想做 RAG、Agent 或文档智能

先读：

- [15. RAG 与 Agent 工程](docs/15-rag-agent-engineering.md)
- [19. 大模型安全与上线运维](docs/19-safety-ops.md)
- [20. 论文阅读路线](docs/20-paper-reading-roadmap.md)

配套练习：

- 用 `examples/chunk_text_preview.py` 看 chunking 结果。
- 选一篇论文，用 [论文笔记模板](papers/README.md) 写一页笔记。
- 记录一次检索失败或引用错误，而不是只记录成功样例。

### 5. 想整理自己的 GitHub star

读：

- [21. 从 100 个 Starred Repos 清洗知识地图](docs/21-starred-repo-knowledge-map.md)
- [22. Star 驱动的学习路线](docs/22-star-driven-learning-route.md)
- [23. 100 个 Starred Repos 全量索引](docs/23-starred-repo-index.md)
- [24. Source Reading Queue](docs/24-source-reading-queue.md)

这部分的目的不是展示收藏夹。它把 100 个公开 starred repos 分成几类：核心学习、可读可练、参考资料、隔离观察。能转成实验、源码阅读笔记、技术图或贡献计划的项目，才放进主线。

## 目录

- [00. 学习地图](docs/00-learning-map.md)
- [00A. 资料来源地图](docs/00-source-map.md)
- [00B. 自我 Review 记录](docs/00-self-review.md)
- [01. CUDA、ZLUDA 与昇腾 CANN](docs/01-hardware-stacks.md)
- [02. PyTorch、ONNX、safetensors 和 OM](docs/02-model-formats.md)
- [03. Hugging Face 项目从哪里开始](docs/03-huggingface-workflow.md)
- [04. SFT、LoRA、QLoRA、DPO 到底在训什么](docs/04-training-finetuning-alignment.md)
- [05. 推理优化和部署](docs/05-inference-optimization.md)
- [06. 集成电路与 AI 芯片学习路线](docs/06-chip-domain-roadmap.md)
- [07. 练手项目与简历表达](docs/07-practice-projects.md)
- [08. Hands-on Labs](docs/08-hands-on-labs.md)
- [09. Source Reading Notes](docs/09-source-reading-notes.md)
- [10. vLLM Benchmark Guide](docs/10-vllm-benchmark-guide.md)
- [11. CUDA / CANN API Map](docs/11-cuda-cann-api-map.md)
- [12. ONNX -> ATC -> OM -> AscendCL](docs/12-onnx-atc-om-flow.md)
- [13. 模型评测与 Benchmark](docs/13-evaluation-benchmark.md)
- [14. 数据工程与数据清洗](docs/14-data-engineering.md)
- [15. RAG 与 Agent 工程](docs/15-rag-agent-engineering.md)
- [16. 量化专题](docs/16-quantization.md)
- [17. 高级推理优化](docs/17-advanced-inference.md)
- [18. 分布式训练与并行策略](docs/18-distributed-training.md)
- [19. 大模型安全与上线运维](docs/19-safety-ops.md)
- [20. 论文阅读路线](docs/20-paper-reading-roadmap.md)
- [21. 从 100 个 Starred Repos 清洗知识地图](docs/21-starred-repo-knowledge-map.md)
- [22. Star 驱动的学习路线](docs/22-star-driven-learning-route.md)
- [23. 100 个 Starred Repos 全量索引](docs/23-starred-repo-index.md)
- [24. Source Reading Queue](docs/24-source-reading-queue.md)
- [术语表](docs/99-glossary.md)
- [参考资料](docs/references.md)
- [论文笔记模板](papers/README.md)
- [后续项目清单](PROJECTS.md)

## 怎么练

每章最好配一个小输出。不要只读。

| 学习内容 | 输出物 |
| --- | --- |
| 模型格式 | 一张 PyTorch / ONNX / safetensors / OM 对照表 |
| LoRA / QLoRA | 一个 toy 数据清洗脚本和一次 smoke test |
| 推理服务 | 一份 vLLM 压测记录 |
| KV cache | 一个显存估算表 |
| RAG | 一组失败样例和修正记录 |
| CUDA / CANN | 一个 API 对照表或 kernel 阅读笔记 |
| 论文阅读 | 一页论文笔记 |
| 开源项目阅读 | 一页 source reading note |

仓库里已经放了一些最小脚本：

- `examples/minimal_inference.py`
- `examples/minimal_sft_lora.py`
- `examples/benchmark_openai_server.py`
- `examples/estimate_kv_cache.py`
- `examples/kv_cache_sweep.py`
- `examples/chunk_text_preview.py`
- `examples/evaluate_predictions.py`

## 资料怎么来的

主要来源有三类：

- 官方文档：Hugging Face、PyTorch、NVIDIA CUDA、Huawei Ascend CANN、vLLM 等。
- 开源项目：Codex、MCP、MinerU、MarkItDown、LeetCUDA、ZLUDA、gprMax 等。
- 论文和技术报告：Transformer、LoRA、QLoRA、DPO、FlashAttention、vLLM、RAG 等。

链接集中放在 [参考资料](docs/references.md)。如果一个概念没有官方文档、论文或可运行项目支撑，就先不写成结论。

## 自检问题

读完一轮后，可以用这些问题检查自己是不是真的懂了：

- LoRA 更新的是哪些参数？
- QLoRA 的低比特量化发生在哪里？
- vLLM 的 PagedAttention 解决了什么问题？
- TTFT 和 TPOT 分别反映什么？
- KV cache 显存为什么会随上下文长度增长？
- ONNX、ONNX Runtime、`.om` 文件是什么关系？
- CUDA kernel、Ascend C 自定义算子、PyTorch op 是什么关系？
- CANN 和 ZLUDA 为什么不是一类东西？
- RAG 的 indexing、retrieval、generation 为什么要分开评估？
- prompt injection 为什么不能只靠 system prompt 解决？

答不清楚时，回到对应章节和脚本。不要急着把名词写进简历。
