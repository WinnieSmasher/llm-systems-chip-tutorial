# 02. PyTorch、ONNX、safetensors 和 OM

很多人第一次看 Hugging Face，会以为“模型就是一个文件”。其实不是。

一个模型项目里通常同时有结构、权重、分词器、推理模板、license 和示例代码。不同文件负责不同事情。

## 1. Hugging Face 模型 repo 里有什么

一个常见 LLM repo 大概长这样：

```text
Qwen2.5-0.5B-Instruct/
├── config.json
├── generation_config.json
├── tokenizer.json
├── tokenizer_config.json
├── special_tokens_map.json
├── model.safetensors
└── README.md
```

大致分工：

| 文件 | 作用 |
| --- | --- |
| `config.json` | 模型结构配置，比如层数、hidden size、attention heads |
| tokenizer files | 把文本变成 token id，再把 token id 解码成文本 |
| `model.safetensors` | 权重矩阵 |
| `generation_config.json` | 默认生成参数 |
| `README.md` | model card，包含 license、训练说明、用法和限制 |

Transformers 加载模型时，会把这些东西组合起来。

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)
```

这时的 `model` 是一个 PyTorch module，可以 forward、generate、训练、保存。

## 2. PyTorch checkpoint 为什么适合训练

PyTorch 模型是动态图框架里的模型对象。它适合：

- 算梯度。
- 更新参数。
- 接 LoRA adapter。
- 做 SFT / DPO。
- 保存 checkpoint。

你可以把它理解成“还可以继续学习的模型状态”。

训练时通常保留这些东西：

```text
base model weights
tokenizer
training config
optimizer state
lr scheduler state
adapter weights
checkpoint metadata
```

注意：如果你只保存了 LoRA adapter，不等于保存了完整模型。推理时还需要 base model。

## 3. safetensors 是权重存储格式

`.safetensors` 保存的是 tensor，不保存任意 Python 对象。它比传统 pickle 格式更安全，也适合快速加载。

但它不是“完整模型”。完整加载仍然需要：

```text
config.json + tokenizer + safetensors weights + 对应代码
```

所以看到 `model.safetensors`，不要以为单独这个文件就能聊天。

## 4. ONNX 是部署交换格式

ONNX 的核心是一张计算图：

```text
Graph
  -> Node
  -> Tensor
  -> Operator
  -> Initializer
```

PyTorch 导出 ONNX 时，会把模型 forward 过程转换成一个静态图。ONNX Runtime、TensorRT、OpenVINO、CANN 等后端可以基于这个图做推理优化或硬件适配。

常见路线：

```text
PyTorch model
  -> export to ONNX
  -> backend optimization
  -> inference runtime
```

ONNX 更偏部署，不是大模型继续训练的主路线。

## 5. 昇腾 OM 是什么

在 Ascend 静态图推理中，ATC 可以把 ONNX 等模型转换成 `.om`：

```text
model.onnx
  -> ATC
  -> model.om
  -> AscendCL application
  -> Ascend NPU
```

`.om` 是面向昇腾推理执行的模型文件。它不是通用训练 checkpoint。

所以别把这几个东西混成一团：

```text
PyTorch checkpoint: 适合训练、微调、继续迭代
ONNX: 适合跨框架推理部署
OM: 适合 Ascend NPU 静态推理部署
safetensors: 常见权重存储格式
```

## 6. 一个实际选择表

| 你要做什么 | 更常用的入口 |
| --- | --- |
| 下载开源 LLM 试聊 | Hugging Face + Transformers |
| LoRA/QLoRA 微调 | PyTorch checkpoint + PEFT/TRL |
| 做 DPO 偏好对齐 | PyTorch checkpoint + TRL |
| 部署 OpenAI-compatible 服务 | vLLM / TGI |
| 跨框架推理 | ONNX / ONNX Runtime |
| NVIDIA 极致推理优化 | TensorRT-LLM |
| 昇腾静态推理 | ONNX -> ATC -> OM -> AscendCL |
| 昇腾训练或微调 | torch_npu / MindSpeed-LLM / CANN |

## 7. 一个常见坑

有人会问：“我把模型转 ONNX 以后，还能不能继续 LoRA 微调？”

通常不这么做。LoRA 微调发生在 PyTorch 训练图里；ONNX 是为了推理图执行。你应该保留原始 PyTorch/Hugging Face checkpoint，训练完成后再考虑导出部署格式。

## 参考

- Hugging Face Transformers: https://huggingface.co/docs/transformers
- safetensors: https://huggingface.co/docs/safetensors
- ONNX Concepts: https://onnx.ai/onnx/intro/concepts.html
- PyTorch ONNX Export: https://docs.pytorch.org/docs/stable/onnx.html
- Huawei Ascend documentation: https://www.hiascend.com/document

