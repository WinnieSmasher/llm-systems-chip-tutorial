# 03. Hugging Face 项目从哪里开始

如果你想拿 Hugging Face 上的开源模型做训练、推理、微调，不要第一步就写训练脚本。先把下面这个闭环跑通：

```text
选模型
  -> 看 model card 和 license
  -> 跑最小推理
  -> 建小评测集
  -> 记录 baseline
  -> 再决定要不要微调
```

很多项目失败不是因为 LoRA 参数没调好，而是连 baseline、数据质量和评测集都没有。

## 1. 选模型时先看四件事

### License

能不能商用、能不能再分发、能不能做衍生模型，先看 model card。不要下载完才发现不能用。

### Context length

长上下文会显著影响显存，尤其是 KV cache。不要只看“7B/14B/32B”参数量。

### Chat template

Instruct/chat 模型通常有自己的对话格式。Transformers 提供 `apply_chat_template`，尽量用 tokenizer 自带模板，不要自己拼字符串。

### 是否需要 remote code

有些模型需要 `trust_remote_code=True`。这意味着你会执行模型仓库里的自定义 Python 代码。只对你信任的模型使用。

## 2. 最小推理脚本

先用小模型跑通：

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

messages = [
    {"role": "user", "content": "用三句话解释 PyTorch 模型和 ONNX 模型的区别。"}
]

inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt",
    tokenize=True,
).to(model.device)

outputs = model.generate(
    inputs,
    max_new_tokens=256,
    do_sample=False,
)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

这里先用 `do_sample=False`，因为做 baseline 时要稳定，不要每次输出都漂。

## 3. 建一个小评测集

不要等训练完再想怎么评测。先准备 20 到 100 条你关心的样例。

比如你要做“大模型系统教程助手”，评测集可以包括：

```json
{
  "id": "cuda_cann_001",
  "question": "华为昇腾 CANN 和 ZLUDA 是什么关系？",
  "must_have": ["CANN 是 Ascend NPU 原生生态", "ZLUDA 是 CUDA 兼容层", "二者不是同一层"],
  "bad_patterns": ["昇腾就是 ZLUDA", "CANN 是 ONNX 的一种"]
}
```

评测不一定一开始就自动化。人工表格也可以，但要固定样例。

## 4. 数据格式

SFT 常见格式是 messages：

```json
{
  "messages": [
    {"role": "user", "content": "解释一下 vLLM 的 PagedAttention。"},
    {"role": "assistant", "content": "PagedAttention 把 KV cache 分页管理..."}
  ]
}
```

或者 instruction 格式：

```json
{
  "instruction": "解释下面术语",
  "input": "KV Cache",
  "output": "KV Cache 是 Transformer 解码时保存历史 key/value 的缓存..."
}
```

无论哪种，最后都要变成模型 chat template 对应的 token 序列。

## 5. 用 TRL 做一个最小 SFT

TRL 的 `SFTTrainer` 是常见入口。真实训练前先小步跑通：

```python
from datasets import load_dataset
from trl import SFTConfig, SFTTrainer

dataset = load_dataset("trl-lib/Capybara", split="train")

args = SFTConfig(
    output_dir="outputs/qwen-sft-smoke",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-5,
    num_train_epochs=1,
    max_length=2048,
    packing=True,
)

trainer = SFTTrainer(
    model="Qwen/Qwen2.5-0.5B-Instruct",
    args=args,
    train_dataset=dataset,
)

trainer.train()
```

这只是 smoke test，不代表最终训练配置。正式训练要加：

- eval dataset。
- checkpoint 策略。
- logging。
- seed。
- 数据版本记录。
- 训练环境记录。

## 6. 一条靠谱的迭代路线

```text
第 0 步：读 model card，确认 license 和硬件需求
第 1 步：跑最小推理，保存 baseline 输出
第 2 步：做小评测集，人工检查模型弱点
第 3 步：整理训练数据，先不要太大，先要干净
第 4 步：LoRA/QLoRA SFT
第 5 步：用同一套评测集对比
第 6 步：决定是继续清洗数据、调训练，还是直接做 RAG/Prompt
第 7 步：推理优化和部署
```

## 7. 不要一上来就微调

先问自己：

- 任务是不是知识更新频繁？如果是，RAG 可能更合适。
- 只是输出格式不好？先试 prompt 和 constrained decoding。
- 数据是不是只有几十条？先做 eval 和数据清洗。
- 有没有明确指标？没有指标就不知道微调是否变好。

微调不是魔法。它只是把你给的数据分布压进模型行为里。

## 参考

- Hugging Face LLM Course: https://huggingface.co/learn/llm-course
- Transformers docs: https://huggingface.co/docs/transformers
- TRL SFTTrainer docs: https://huggingface.co/docs/trl
- Datasets docs: https://huggingface.co/docs/datasets

