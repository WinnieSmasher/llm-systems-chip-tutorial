# 04. 训练、微调、继续预训练与对齐

这一章解释几个经常被混用的词：

- training
- fine-tuning
- SFT
- LoRA/QLoRA
- continued pretraining
- alignment
- DPO/RLHF

## 1. Training 是总称

Training 是训练的总称，只要模型参数被更新，都可以叫 training。

但在大模型工程里，我们通常会进一步区分：

```text
pretraining
continued pretraining
supervised fine-tuning
parameter-efficient fine-tuning
alignment
```

## 2. Pretraining 预训练

预训练是从大量原始文本里学习语言规律。

典型目标：

```text
给定前面的 token，预测下一个 token
```

这一步非常贵，需要大量数据和算力。普通团队通常不会从零预训练一个 DeepSeek/GLM/Llama 级别模型。

## 3. Continued Pretraining 继续预训练

继续预训练是在已有 base model 上继续读领域语料。

适合：

- 医学论文。
- 法律文书。
- 金融报告。
- 代码仓库。
- 芯片设计文档。
- 企业内部知识库。

通俗理解：

```text
继续预训练 = 让模型先多读某个领域的书
```

它通常不直接教模型“怎么回答”，而是增强领域知识和语言分布适应。

## 4. SFT 监督微调

SFT，全称 Supervised Fine-Tuning，是用 instruction-response 或 conversation 数据教模型完成任务。

通俗理解：

```text
SFT = 给模型看标准问答，教它怎么回答
```

典型样本：

```json
{
  "messages": [
    {"role": "user", "content": "把 CUDA 和 CANN 的区别讲给初学者。"},
    {"role": "assistant", "content": "CUDA 是 NVIDIA GPU 的原生生态，CANN 是华为昇腾 NPU 的原生生态..."}
  ]
}
```

常用工具：

- Transformers Trainer
- TRL SFTTrainer
- LLaMA-Factory
- Axolotl

## 5. LoRA 是什么

全量微调会更新模型所有参数，显存和算力开销很大。

LoRA 的思路是：

```text
冻结原模型
只训练少量低秩 adapter 参数
```

通俗理解：

```text
全量微调 = 把整个大脑都改一遍
LoRA = 给大脑外挂一个小插件
```

LoRA 常见配置项：

- `r`：低秩矩阵的 rank，越大表达能力越强但越占显存。
- `lora_alpha`：缩放系数。
- `target_modules`：把 LoRA 插到哪些层，比如 `q_proj`, `v_proj`, `o_proj`。
- `lora_dropout`：防止过拟合。

## 6. QLoRA 是什么

QLoRA 通常是在 4-bit 量化 base model 的基础上训练 LoRA adapter。

通俗理解：

```text
QLoRA = 把大模型压小后，再训练外挂插件
```

优点：

- 更省显存。
- 单卡也能微调较大模型。

代价：

- 训练和推理配置更复杂。
- 量化可能带来精度损失。

## 7. DPO/RLHF 是什么

SFT 教模型“怎么答”，但不一定教它“哪个回答更好”。

偏好对齐使用这样的数据：

```text
同一个问题
chosen answer: 更好的回答
rejected answer: 更差的回答
```

DPO 用这种偏好对训练模型，让它更倾向于 chosen answer。

RLHF 更复杂，通常包括 reward model 和 reinforcement learning。

通俗理解：

```text
SFT  = 看标准答案学习
DPO  = 看好答案和坏答案的对比学习
RLHF = 根据奖励信号继续调整行为
```

## 8. 一个微调项目应该怎么组织

推荐目录：

```text
project
├── configs/
├── data/
├── scripts/
├── src/
├── eval/
├── outputs/
└── README.md
```

最小闭环：

1. 准备 50 到 200 条高质量 eval examples。
2. 直接用 base/instruct model 跑 baseline。
3. 准备训练集并清洗。
4. 做 LoRA/QLoRA SFT。
5. 用同一套 eval examples 对比。
6. 观察失败样例，决定是否继续清洗数据或调整训练。

## 9. 什么时候不该微调

以下情况先别急着微调：

- 任务知识经常变化，RAG 更合适。
- 只是格式控制，prompt 和 constrained decoding 可能够用。
- 数据量很少且质量不稳定。
- 没有评测集，不知道训练后是否真的变好。
- 线上部署成本比模型效果更重要。

