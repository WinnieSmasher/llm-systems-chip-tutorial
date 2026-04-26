# 03. Hugging Face 大模型工作流

这一章从工程视角解释：

> Hugging Face 上的 DeepSeek、GLM、Qwen、Llama 等开源模型，拿下来以后到底怎么用？

模型名字可以替换，核心流程基本类似。

## 1. Hugging Face 是什么

Hugging Face 可以理解成大模型领域的 GitHub + package registry：

- Hub：存模型、数据集、Space demo。
- Transformers：加载和运行模型。
- Datasets：加载和处理训练数据。
- Tokenizers：分词。
- PEFT：LoRA/QLoRA 等参数高效微调。
- TRL：SFT、DPO、PPO 等大模型训练/对齐工具。
- Accelerate：多 GPU/混合精度/分布式训练辅助。

## 2. 最小推理流程

假设你选择一个 causal language model，也就是自回归语言模型。

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    dtype=torch.bfloat16,
    device_map="auto",
)

messages = [
    {"role": "user", "content": "用通俗语言解释 CUDA 和 CANN 的区别。"}
]

input_ids = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_tensors="pt",
).to(model.device)

outputs = model.generate(input_ids, max_new_tokens=512, temperature=0.7)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

这里几个关键概念：

- `AutoTokenizer`：自动加载对应 tokenizer。
- `AutoModelForCausalLM`：加载自回归语言模型。
- `device_map="auto"`：自动把模型放到可用设备上。
- `apply_chat_template`：把多轮对话转成模型能理解的 token 序列。
- `generate`：让模型一个 token 一个 token 地生成回答。

## 3. 数据长什么样

如果做指令微调，数据通常长这样：

```json
{
  "messages": [
    {"role": "user", "content": "解释一下什么是 ONNX。"},
    {"role": "assistant", "content": "ONNX 是一种跨框架模型交换格式..."}
  ]
}
```

或者更传统的 instruction 格式：

```json
{
  "instruction": "分析下面的玩家行为序列",
  "input": "login -> level_1_fail -> retry -> quit",
  "output": "该玩家在第 1 关反复失败后退出，可能存在早期关卡难度过高的问题。"
}
```

数据质量通常比训练代码更重要。常见清洗项：

- 去掉重复样本。
- 去掉空回答、乱码、格式错误。
- 统一角色字段。
- 控制输出长度。
- 避免把测试集泄露到训练集。
- 保留高质量人工样本或专家样本。

## 4. 训练大模型通常有哪些层次

从轻到重：

```text
Prompt engineering
  -> RAG
  -> LoRA/QLoRA SFT
  -> full fine-tuning
  -> continued pretraining
  -> alignment with DPO/RLHF
```

不要一上来就训练。很多任务可以先用 prompt、RAG 或 workflow 解决。

## 5. 一个真实项目的迭代闭环

```text
选模型
  -> 构造小评测集
  -> 直接推理 baseline
  -> 收集错误案例
  -> 清洗训练数据
  -> LoRA/QLoRA 微调
  -> 跑评测
  -> 推理优化
  -> 部署服务
  -> 收集线上反馈
  -> 继续迭代
```

每次迭代要记录：

- base model 版本。
- 数据集版本。
- 训练超参数。
- eval 指标。
- 推理延迟和显存占用。
- 人工观察到的失败模式。

## 6. DeepSeek、GLM 这种模型怎么代入

不要被模型名字吓到。只要模型支持 Transformers 或提供对应推理/训练接口，基本逻辑就是：

```text
model_id = "实际 Hugging Face repo id"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)
```

需要注意：

- 有些模型需要申请 license 或登录 Hugging Face token。
- 有些模型需要 `trust_remote_code=True`。
- 不同模型 chat template 不同，EOS token 也可能不同。
- 大模型需要足够显存，不能只看参数量，还要看精度、上下文长度和 KV cache。

## 7. 最容易踩的坑

### 坑一：把 instruct 模型和 base 模型混用

- base model：更像“续写器”，适合继续预训练或作为微调起点。
- instruct/chat model：已经做过指令微调，更适合直接聊天和任务指令。

### 坑二：只看训练 loss

训练 loss 降低不等于模型更好。你还要看：

- 任务评测集。
- 人工样例。
- 幻觉率。
- 格式遵循能力。
- 延迟、吞吐、显存。

### 坑三：数据太脏

低质量数据会把模型带偏。尤其是小规模 LoRA 微调，数据噪声会非常明显。

### 坑四：忘记 tokenizer 和 chat template

同样的文字，不同 tokenizer 和 chat template 会变成不同 token 序列。对于 chat model，这往往直接影响回答质量。

