# 04. SFT、LoRA、QLoRA、DPO 到底在训什么

先分清楚：这些词不是同一个维度。

```text
SFT / DPO 说的是训练目标
LoRA / QLoRA 说的是参数更新方式和显存策略
continued pretraining 说的是让模型继续读领域语料
```

## 1. Pretraining 和 continued pretraining

预训练通常是下一个 token 预测：

```text
给定 token_1 ... token_n，预测 token_{n+1}
```

从零预训练一个大模型非常贵。普通团队更常见的是 continued pretraining，也就是拿已有 base model 继续读领域语料。

适合：

- 芯片手册。
- 医学论文。
- 法律文书。
- 企业内部技术文档。
- 代码仓库。

它解决的是“模型不熟这个领域的语言和知识”。但它不一定让模型更会听指令。

## 2. SFT 训练的是什么

SFT，Supervised Fine-Tuning，用的是标准答案。

样例：

```json
{
  "messages": [
    {"role": "user", "content": "解释 CUDA kernel 和 Ascend C 的区别"},
    {"role": "assistant", "content": "CUDA kernel 面向 NVIDIA GPU..."}
  ]
}
```

训练目标仍然是预测 assistant 的 token。区别是数据已经整理成“用户问题 -> 理想回答”。

SFT 适合：

- 教模型固定任务。
- 教回答风格。
- 教输出格式。
- 教领域问答。

## 3. LoRA 训练的是什么

LoRA 的论文核心想法是：大模型适配任务时，不一定要更新所有权重，可以训练低秩矩阵。

原本线性层是：

```text
y = W x
```

LoRA 冻结 `W`，额外加一个低秩更新：

```text
y = W x + B A x
```

其中 `A` 和 `B` 很小。训练时只更新它们。

直观理解：

```text
全量微调：改整本书
LoRA：在书边加一套可学习批注
```

常见配置：

```python
from peft import LoraConfig

peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
)
```

`target_modules` 不要乱填。不同模型结构命名不同，Llama/Qwen/GLM 可能不一样。

## 4. QLoRA 解决什么

QLoRA 的目标是进一步省显存：base model 以低比特方式加载，训练 LoRA adapter。

典型理解：

```text
base model: 4-bit
trainable parameters: LoRA adapter
optimizer state: 只围绕 adapter
```

适合单卡资源有限时微调较大模型。

代价是：

- 训练配置更复杂。
- 对硬件和量化库有要求。
- 量化可能影响质量。

## 5. DPO 训练的是什么

DPO 用偏好数据：

```json
{
  "prompt": "解释 ZLUDA 和 CANN 的区别",
  "chosen": "ZLUDA 是 CUDA 兼容层，CANN 是昇腾 NPU 原生生态...",
  "rejected": "CANN 就是华为版 ZLUDA..."
}
```

它不是教“标准答案长什么样”，而是教模型更偏向 chosen，远离 rejected。

适合：

- SFT 后回答可用，但风格、偏好、拒答边界还不理想。
- 你有成对偏好数据。

没有偏好数据就别硬做 DPO。

## 6. 怎么选

| 目标 | 优先方案 |
| --- | --- |
| 只是想让模型知道新资料 | RAG 或 continued pretraining |
| 想让模型学会固定问答/格式 | SFT |
| 显存有限还想微调 | LoRA / QLoRA |
| 想让模型更偏好某类回答 | DPO |
| 模型知识经常更新 | RAG，不要急着训练 |
| 只是输出格式不稳 | Prompt、schema、constrained decoding |

## 7. 训练前 checklist

正式训练前先检查：

- base model 是 base 还是 instruct？
- tokenizer 和 chat template 是否正确？
- 训练集和评测集有没有泄露？
- 是否记录 model revision？
- 是否固定 random seed？
- 是否保存训练配置？
- 是否有人工可读的错误案例分析？

## 8. 训练后的交付物

一个像样的微调项目至少应该有：

```text
adapter 或 checkpoint
训练配置
数据版本说明
评测结果
失败样例分析
推理脚本
README
```

只上传一个 adapter，别人很难判断你到底做了什么。

## 参考

- LoRA paper: https://arxiv.org/abs/2106.09685
- QLoRA paper: https://arxiv.org/abs/2305.14314
- DPO paper: https://arxiv.org/abs/2305.18290
- PEFT docs: https://huggingface.co/docs/peft
- TRL docs: https://huggingface.co/docs/trl

