# 20. 论文阅读路线

这条线不是为了背论文名。目标是建立“模型、训练、推理系统、评测、安全”之间的因果图。读完以后，你应该能解释一个工程选择背后的论文来源。

## 1. 读论文的顺序

建议按问题读，不按时间线读：

```text
模型为什么这么设计
  -> 怎么训练和对齐
  -> 怎么省显存
  -> 怎么跑得快
  -> 怎么评测
  -> 怎么安全上线
```

每篇论文做一页笔记，别一开始就写长综述。

## 2. 模型与训练

| 主题 | 论文 | 看什么 |
| --- | --- | --- |
| Transformer | Attention Is All You Need | attention、position encoding、encoder/decoder |
| Scaling | GPT-3、Chinchilla | 参数量、数据量、compute 的关系 |
| Instruction tuning | InstructGPT | SFT、reward model、RLHF 的位置 |
| Preference optimization | DPO | chosen/rejected 数据如何进入训练目标 |
| LoRA | LoRA | 低秩 adapter 为什么省参数 |
| QLoRA | QLoRA | 4-bit base model + LoRA 的显存收益 |

读这组论文时，不要只看公式。重点问：

- 训练数据是什么。
- 训练目标是什么。
- 哪些参数被更新。
- 需要多少显存和算力。
- 实验怎么证明有效。

## 3. 推理系统

| 主题 | 论文/项目 | 看什么 |
| --- | --- | --- |
| FlashAttention | FlashAttention | attention 的 IO bottleneck |
| vLLM / PagedAttention | vLLM paper | KV cache block 管理 |
| TensorRT-LLM | NVIDIA project | kernel、parallelism、serving |
| llama.cpp | ggml/llama.cpp | GGUF、本地推理、量化 |

读系统论文时，先画图：

```text
request -> scheduler -> prefill -> KV cache -> decode -> output
```

然后标出优化发生在哪一段。

## 4. 分布式训练

| 主题 | 论文/项目 | 看什么 |
| --- | --- | --- |
| Megatron-LM | Megatron-LM | tensor parallel、pipeline parallel |
| ZeRO | DeepSpeed ZeRO | optimizer/gradient/parameter state partition |
| FSDP | PyTorch FSDP docs | 参数 shard 和 checkpoint |
| NCCL | NVIDIA docs | collective communication |

读这组内容时，把显存拆成：

```text
parameters + gradients + optimizer states + activations
```

再看每种方法切掉哪一块。

## 5. RAG 与评测

| 主题 | 论文/项目 | 看什么 |
| --- | --- | --- |
| RAG | Retrieval-Augmented Generation | retriever + generator |
| DPR | Dense Passage Retrieval | dense retrieval 的训练方式 |
| HELM | Holistic Evaluation of Language Models | 多维度评测 |
| lm-evaluation-harness | EleutherAI project | benchmark runner 结构 |
| OpenCompass | OpenCompass project | 中文/多模型评测组织方式 |

RAG 论文读完要能落到工程问题：

- chunk 怎么切。
- embedding 模型怎么选。
- top-k 和 rerank 怎么调。
- 引用怎么验证。
- 找不到证据时怎么拒答。

## 6. 安全与 Agent

| 主题 | 来源 | 看什么 |
| --- | --- | --- |
| OWASP LLM Top 10 | OWASP | prompt injection、supply chain、excessive agency |
| Tool use / agents | LangChain / LlamaIndex docs | tool boundary、trace、retrieval |
| Red teaming | model provider docs / papers | 攻击样本、拒答、越权 |

安全材料读的时候，直接映射到代码：

```text
risk -> attack example -> control -> test case
```

不这样做，就容易停在“了解安全风险”。

## 7. 一页论文笔记模板

```text
paper:
problem:
core idea:
method:
experiment:
what changed in engineering:
limitations:
terms to remember:
code/project:
my reproduction idea:
```

论文图表也要单独记：

| 图/表 | 作用 |
| --- | --- |
| architecture figure | 解释模块关系 |
| ablation table | 证明哪个组件有效 |
| scaling curve | 解释变量变化趋势 |
| latency/memory table | 支撑工程选择 |

如果以后要写 paper，画图和表格优化能力就是从这里练出来的。

## 8. 8 周阅读安排

| 周 | 主题 | 输出 |
| --- | --- | --- |
| 1 | Transformer 和 scaling | 一张模型结构图 |
| 2 | SFT/RLHF/DPO | 一张训练阶段对照表 |
| 3 | LoRA/QLoRA/量化 | 一张显存组成图 |
| 4 | FlashAttention/vLLM | 一张推理链路图 |
| 5 | FSDP/ZeRO/Megatron | 一张并行策略表 |
| 6 | RAG/DPR | 一个 chunk + retrieval 小实验 |
| 7 | benchmark/HELM/lm-eval | 一个 JSONL eval |
| 8 | OWASP/Agent safety | 一份上线 checklist |

## 参考

- Attention Is All You Need: https://arxiv.org/abs/1706.03762
- LoRA: https://arxiv.org/abs/2106.09685
- QLoRA: https://arxiv.org/abs/2305.14314
- DPO: https://arxiv.org/abs/2305.18290
- FlashAttention: https://arxiv.org/abs/2205.14135
- PagedAttention / vLLM: https://arxiv.org/abs/2309.06180
- DeepSpeed ZeRO: https://www.deepspeed.ai/tutorials/zero/
- PyTorch FSDP: https://docs.pytorch.org/docs/stable/fsdp.html

