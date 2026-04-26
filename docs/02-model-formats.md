# 02. PyTorch 模型、ONNX 模型和部署格式

这一章解释几个常见词：

- PyTorch 模型
- Hugging Face 模型
- ONNX 模型
- safetensors
- 昇腾 `.om` 模型

## 1. Hugging Face 上的模型是什么

Hugging Face 上一个大模型通常不是一个单独文件，而是一个目录结构：

```text
model repo
├── config.json
├── tokenizer.json
├── tokenizer_config.json
├── generation_config.json
├── model.safetensors
└── README.md
```

这些文件分别负责：

- `config.json`：模型结构，例如层数、hidden size、attention heads。
- tokenizer files：把自然语言切成 token。
- `model.safetensors`：模型权重。
- `generation_config.json`：默认生成参数。
- `README.md`：model card，说明训练数据、license、用法和限制。

用 Transformers 加载时：

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)
```

这时你拿到的是一个可以在 PyTorch 里运行的模型对象。

## 2. PyTorch 模型是什么

PyTorch 模型可以继续训练、微调、算梯度、更新参数。

通俗地说：

```text
PyTorch 模型 = 还活着的大脑
```

它适合：

- 直接推理。
- SFT 监督微调。
- LoRA/QLoRA 参数高效微调。
- continued pretraining 继续预训练。
- DPO/RLHF 偏好对齐。
- 保存新 checkpoint。

训练和微调时，通常优先使用 PyTorch 模型。

## 3. safetensors 是什么

`.safetensors` 是一种保存模型权重的格式。相比传统 pickle-based 的 `.bin`，它更安全、加载也更可控。

你可以把它理解成：

```text
safetensors = 模型参数矩阵的安全存储文件
```

它不是模型结构本身，模型结构仍然需要 `config.json`。

## 4. ONNX 模型是什么

ONNX 是一种跨框架模型交换格式。

通俗地说：

```text
PyTorch 模型 = 活的大脑，可以继续学习
ONNX 模型    = 固化后的电路图，主要用于高效执行
```

ONNX 常用于：

- 推理部署。
- 跨框架迁移。
- ONNX Runtime 加速。
- TensorRT / OpenVINO / CANN 等后端转换。

它通常不适合继续训练大型语言模型。

常见路线：

```text
PyTorch model
  -> export
  -> ONNX
  -> runtime/backend optimization
  -> inference service
```

## 5. 昇腾 `.om` 模型是什么

在华为昇腾部署场景里，ATC 可以把 ONNX、TensorFlow、Caffe 等模型转换成 `.om`。

`.om` 可以理解为：

```text
Ascend NPU 更容易直接执行的模型文件
```

典型流程：

```text
model.onnx
  -> ATC
  -> model.om
  -> AscendCL 加载
  -> Ascend NPU 推理
```

注意：`.om` 更偏部署执行，不是你日常用来 LoRA 微调的训练格式。

## 6. 什么时候用哪个

| 目标 | 推荐格式/工具 |
| --- | --- |
| 继续训练大模型 | PyTorch checkpoint + Transformers |
| LoRA/QLoRA 微调 | PyTorch + PEFT/TRL |
| Hugging Face 推理测试 | Transformers |
| 高吞吐大模型服务 | vLLM / TGI |
| 跨框架部署 | ONNX |
| NVIDIA 推理优化 | TensorRT / TensorRT-LLM |
| 昇腾静态推理部署 | ONNX -> ATC -> `.om` |
| 昇腾 PyTorch 适配 | torch_npu + CANN |

## 7. 一个关键误区

不要把“模型文件格式”和“硬件计算生态”混在一起。

```text
PyTorch/ONNX/safetensors 是模型表达或存储问题
CUDA/CANN/ROCm 是硬件执行生态问题
vLLM/TensorRT/CANN runtime 是推理优化和部署问题
```

