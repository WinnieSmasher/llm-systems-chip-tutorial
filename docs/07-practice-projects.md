# 07. 练手项目与简历表达

这一章把前面的知识变成可以动手做、可以写进简历的项目。

## 1. 入门项目：本地模型推理 baseline

目标：

```text
下载一个小模型
跑通 Transformers 推理
记录延迟、显存和输出质量
```

建议模型：

- Qwen/Qwen2.5-0.5B-Instruct
- Qwen/Qwen2.5-1.5B-Instruct
- GLM/DeepSeek 等模型家族中你有权限访问且本机能跑的较小版本

可交付物：

- `minimal_inference.py`
- 一份 benchmark 表格
- 5 到 20 条人工测试样例

简历表达：

```text
基于 Hugging Face Transformers 搭建本地 LLM 推理 baseline，完成 tokenizer/chat template 适配，并记录模型在不同上下文长度下的延迟和显存占用。
```

## 2. 进阶项目：LoRA 微调领域问答模型

目标：

```text
用领域数据做 SFT
比较微调前后回答质量
```

可以选择领域：

- CUDA/CANN 知识问答。
- 芯片设计文档问答。
- 游戏数据分析问答。
- 论文写作与图表优化问答。

可交付物：

- 数据清洗脚本。
- 训练配置。
- LoRA adapter。
- eval set。
- 微调前后对比报告。

简历表达：

```text
基于 PEFT/TRL 完成领域问答模型 LoRA 微调，构建 instruction 数据集和评测集，对比微调前后在术语解释、格式遵循和领域问答准确性上的表现。
```

## 3. 推理优化项目：vLLM 服务压测

目标：

```text
用 vLLM 部署模型
压测不同 batch/concurrency/context length 下的吞吐和延迟
```

重点指标：

- TTFT
- TPOT
- tokens/s
- concurrency
- GPU memory

简历表达：

```text
使用 vLLM 搭建 OpenAI-compatible 本地推理服务，围绕并发数、上下文长度和输出长度进行压测，分析 KV Cache 对显存占用和吞吐的影响。
```

## 4. 硬件生态项目：CUDA 与 CANN 对照学习

目标：

```text
整理 CUDA 与 CANN 的概念对照
跑通一个简单模型在不同硬件生态下的部署流程
```

对照表可以包括：

| NVIDIA 生态 | 昇腾生态 | 含义 |
| --- | --- | --- |
| CUDA Runtime | AscendCL/ACL Runtime | 设备、内存、stream、执行管理 |
| CUDA kernel | Ascend C custom operator | 自定义底层计算 |
| cuDNN/cuBLAS | CANN operators | 高性能算子库 |
| TensorRT | ATC/CANN 推理工具链 | 模型转换与推理优化 |
| NCCL | HCCL | 多卡通信 |

简历表达：

```text
系统梳理 NVIDIA CUDA 与华为昇腾 CANN 异构计算生态差异，理解模型转换、runtime API、算子库和自定义算子在推理部署链路中的作用。
```

## 5. 研究型项目：KV Cache 显存建模

目标：

```text
分析 batch size、sequence length、hidden size、layer number 对 KV Cache 显存的影响
```

可以做：

- 公式推导。
- Python 估算脚本。
- 实际推理测量。
- 不同模型对比。

简历表达：

```text
围绕 LLM 推理中的 KV Cache 显存开销建立估算模型，并通过本地推理实验分析上下文长度、batch size 与显存占用之间的关系。
```

## 6. 建议的 GitHub repo 结构

如果你要把项目继续做大，可以这样组织：

```text
llm-systems-chip-tutorial
├── README.md
├── docs/
├── assets/
├── examples/
├── benchmarks/
├── configs/
└── reports/
```

## 7. 写简历时的原则

好的经历不是堆工具名，而是写清楚：

```text
背景 -> 任务 -> 方法 -> 验证 -> 结果
```

比如：

```text
围绕大模型推理部署场景，使用 vLLM 搭建本地 OpenAI-compatible 服务，设计并发压测脚本，统计 TTFT、TPOT、tokens/s 和显存占用，分析 KV Cache 对长上下文推理性能的影响。
```

这比单独写：

```text
熟悉 vLLM、CUDA、CANN、LoRA
```

更有说服力。

