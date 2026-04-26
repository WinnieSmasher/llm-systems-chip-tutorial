# 15. RAG 与 Agent 工程

RAG 的本质不是“给模型接个知识库”。它是一条检索和生成链路：先把资料切块建索引，用户提问时取回相关片段，再让模型基于片段回答。

Agent 则多了一层工具调用和决策。RAG 可以是 Agent 的一个工具，但 RAG 本身不一定是 Agent。

## 1. RAG 的两条链路

```text
离线 indexing:
documents -> chunking -> embedding -> vector database

在线 retrieval + generation:
query -> retrieve -> rerank -> prompt with context -> answer with citations
```

LangChain 的 RAG 教程也把流程分成 indexing 和 retrieval/generation。这个拆法很重要：离线链路坏了，在线生成再强也救不回来。

## 2. 每一层都可能出错

| 层 | 常见问题 | 怎么查 |
| --- | --- | --- |
| loader | PDF 页眉页脚、乱码、表格丢失 | 抽样看原文 |
| chunking | chunk 太短没上下文，太长召回不准 | 打印 chunk preview |
| embedding | 中英文、代码、公式不匹配 | 用固定 query 看 top-k |
| vector db | 元数据丢失、过滤条件错 | 检查 `source`, `page`, `section` |
| rerank | 排序慢、召回被过度改写 | 比较 rerank 前后 top-k |
| prompt | context 太长、引用不稳 | 记录完整 prompt |
| generation | 编造引用、忽略 context | 做 answer-groundedness 检查 |

`examples/chunk_text_preview.py` 可以先看切块效果：

```bash
python examples/chunk_text_preview.py \
  --input docs/01-hardware-stacks.md \
  --output temp/hardware_chunks.jsonl \
  --chunk-size 900 \
  --overlap 120
```

## 3. chunking 先用简单规则

刚开始不要迷信复杂算法。先用稳定、可解释的规则：

- Markdown 按标题和段落切。
- PDF 先抽文本，再处理页眉页脚。
- 代码按函数、类、文件路径切。
- chunk 保留 `source`, `section`, `page`, `line_start` 等 metadata。

如果没有 metadata，模型答错时你找不到源头。

## 4. Retriever 不是越多越好

常见组合：

```text
embedding retriever
  -> top_k=20
  -> reranker
  -> top_k=4
  -> answer prompt
```

可调参数：

| 参数 | 影响 |
| --- | --- |
| chunk size | 召回粒度和上下文完整性 |
| overlap | 边界信息保留 |
| top-k | 召回率和 prompt 长度 |
| embedding model | 语义匹配质量 |
| reranker | 精排质量和延迟 |

评测时不要只看最终答案。先看 top-k 里有没有正确证据。如果证据没被检索出来，生成模型不该背锅。

## 5. Agent 工程要限制权限

Agent 常见结构：

```text
LLM
  -> decide tool call
  -> execute tool
  -> observe result
  -> continue or answer
```

工具一多，风险就上来了：

- 搜索工具可能取回恶意网页。
- 文件工具可能读到敏感信息。
- 数据库工具可能执行危险查询。
- 浏览器工具可能被网页里的 prompt injection 诱导。

所以工具要做 capability boundary：

| 控制点 | 做法 |
| --- | --- |
| 工具白名单 | 只给当前任务需要的工具 |
| 参数校验 | 路径、URL、SQL、命令都要限制 |
| 人工确认 | 删除、发送、上传、付款、改权限前确认 |
| 日志 | 记录 tool call、输入、输出摘要 |
| 超时和预算 | 防止无限循环和过度消费 |

RAG context 也要当成第三方数据。检索结果里出现“忽略之前所有指令”这种话，不能照做。

## 6. RAG 评测怎么做

至少分四个指标：

| 指标 | 看什么 |
| --- | --- |
| retrieval recall | top-k 是否含有正确证据 |
| citation accuracy | 引用是否真的支撑答案 |
| answer correctness | 答案是否正确 |
| abstention | 找不到资料时是否承认不知道 |

一个简单样本可以这样写：

```json
{
  "question": "ZLUDA 和 CANN 是什么关系？",
  "gold_sources": ["docs/01-hardware-stacks.md"],
  "must_have": ["ZLUDA", "CUDA compatibility layer", "CANN", "Ascend NPU"],
  "bad_patterns": ["华为的 ZLUDA"]
}
```

## 7. 简历里怎么写

弱写法：

```text
搭建 RAG 知识库，支持文档问答。
```

强写法：

```text
搭建 Markdown/PDF 文档 RAG 原型，完成 chunking、metadata 保留、向量检索、top-k 召回检查和引用式回答；通过固定问题集评估 retrieval recall 与 citation accuracy，并加入 prompt injection 防护提示和工具调用边界。
```

## 参考

- LangChain RAG tutorial: https://docs.langchain.com/oss/python/langchain/rag
- LlamaIndex RAG overview: https://developers.llamaindex.ai/python/framework/understanding/rag/
- Milvus overview: https://milvus.io/docs/overview.md
- OWASP LLM Top 10: https://genai.owasp.org/llm-top-10/

