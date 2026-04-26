# 14. 数据工程与数据清洗

训练大模型时，很多问题看起来像“模型不行”，实际是数据不行：角色格式错、回答为空、重复样本太多、prompt 泄漏答案、评测集混进训练集。

数据工程的目标不是把数据做得漂亮，而是让训练、评测和复现实验都能说清楚。

## 1. 三种常见数据

| 数据类型 | 用在哪里 | 常见字段 |
| --- | --- | --- |
| pretraining text | 继续预训练 | `text`, `source`, `license` |
| SFT conversation | 指令微调 | `messages`, `instruction`, `input`, `output` |
| preference pair | DPO/RLHF | `prompt`, `chosen`, `rejected` |

SFT 数据建议统一成 chat messages：

```json
{
  "messages": [
    {"role": "user", "content": "解释 CUDA 和 CANN 的区别"},
    {"role": "assistant", "content": "CUDA 是 NVIDIA GPU 生态，CANN 是昇腾 NPU 生态。"}
  ]
}
```

这个格式和 Hugging Face Transformers 的 chat template 更容易接起来。

## 2. chat template 是训练入口的一部分

聊天模型不是天然理解 `role=user` 和 `role=assistant`。这些消息最终会被 tokenizer 转成一串 token，中间带控制符。

Hugging Face 的 `apply_chat_template` 做的就是这件事：

```python
input_ids = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_tensors="pt",
)
```

训练和推理的模板不一致，模型会变得很怪。常见错误：

- 训练时没有 assistant 起始 token，推理时加了。
- 手动拼 `<bos>`、`<eos>`，又让 tokenizer 自动加了一遍。
- 把 system prompt 混进每轮 user 内容里。
- 多轮对话里连续出现两个 assistant message。

## 3. 清洗不是只删脏字

一份 SFT 数据至少做这些检查：

| 检查 | 为什么 |
| --- | --- |
| 空内容 | 空回答会教模型输出空 |
| role 顺序 | user/assistant 错位会破坏对话结构 |
| 重复样本 | 重复过多会让模型记模板 |
| 长度分布 | 超长样本会拖慢训练，短垃圾样本会稀释信号 |
| 语言分布 | 中英混杂要符合目标场景 |
| license/source | 数据能不能用于训练 |
| train/eval 泄漏 | 评测结果会虚高 |

这个仓库给了一个标准库脚本：

```bash
python examples/clean_sft_jsonl.py \
  --input raw_sft.jsonl \
  --output clean_sft.jsonl \
  --report clean_sft.report.json \
  --min-chars 8 \
  --max-chars 8000
```

它支持两种输入：

```jsonl
{"messages":[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
{"instruction":"...","input":"...","output":"..."}
```

## 4. 数据版本要能回退

不要只保存 `train.jsonl`。建议这样命名：

```text
data/
  raw/
    sft_2026-04-27.jsonl
  interim/
    sft_2026-04-27_dedup.jsonl
  processed/
    sft_2026-04-27_clean_v1.jsonl
  reports/
    sft_2026-04-27_clean_v1.report.json
```

每次训练记录：

- 数据文件路径。
- 数据条数。
- 清洗脚本 commit。
- tokenizer 和 chat template。
- train/dev/test split。
- 随机种子。

数据不能复现，训练结论就没有根。

## 5. 数据质量比数据量更早重要

早期不要急着收几十万条。先拿 200 到 1000 条高质量样本，把链路跑通：

1. 清洗。
2. 切分 train/dev。
3. 跑一个短 SFT。
4. 用固定评测集比较 base model 和 adapter。
5. 人工看 20 条失败样本。

失败样本比平均分更有价值。它会告诉你该补哪类数据。

## 6. 数据卡要写什么

公开或半公开项目建议写 data card：

| 项 | 内容 |
| --- | --- |
| source | 数据来源、采集方式 |
| license | 能否商用、能否再分发 |
| schema | 每列字段含义 |
| preprocessing | 清洗、去重、过滤 |
| splits | train/dev/test 比例 |
| risks | 隐私、偏见、版权、敏感内容 |
| intended use | 适合什么，不适合什么 |

这不是形式主义。以后你换模型、换脚本、换硬件时，数据卡能救命。

## 7. 简历里怎么写

弱写法：

```text
负责大模型训练数据清洗。
```

强写法：

```text
设计 SFT 数据清洗流程，将 instruction/input/output 与 messages 两类 schema 统一为 chat template 兼容格式；完成空样本、角色顺序、重复样本和长度异常过滤，并生成数据质量报告用于后续 LoRA 微调与回归评测。
```

## 参考

- Hugging Face Datasets loading: https://huggingface.co/docs/datasets/loading
- Hugging Face Datasets processing: https://huggingface.co/docs/datasets/process
- Transformers chat templates: https://huggingface.co/docs/transformers/chat_templating
- TRL SFT Trainer: https://huggingface.co/docs/trl/sft_trainer

