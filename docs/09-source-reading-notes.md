# 09. Source Reading Notes

这一页记录“从来源里读到了什么”。不是完整翻译，只保留会影响工程判断的点。

## Hugging Face Transformers

入口：`AutoTokenizer`、`AutoModelForCausalLM`、chat template、`generate`。

工程判断：

- chat/instruct 模型不要手写对话模板，优先用 tokenizer 的 `apply_chat_template`。
- `device_map="auto"` 方便入门，但正式部署要明确设备、精度和内存预算。
- `generate` 参数会显著影响输出，baseline 阶段建议先固定采样策略。

## PEFT

入口：LoRA adapter、`LoraConfig`、`get_peft_model`、adapter 保存/加载。

工程判断：

- LoRA 不是压缩模型本体，而是在冻结 base model 的基础上训练额外 adapter。
- adapter 单独发布时，要写清楚 base model 名称和版本。
- `target_modules` 必须按模型结构确认，不能照抄别的模型。

## TRL

入口：`SFTTrainer`、`DPOTrainer`。

工程判断：

- SFT 和 DPO 是不同训练目标，不要把 LoRA、SFT、DPO 混成同一类词。
- DPO 需要 chosen/rejected 偏好数据。没有偏好数据时硬做 DPO，通常只是制造噪声。
- `SFTTrainer` 能降低入门成本，但数据格式、chat template、EOS token 仍然要自己检查。

## vLLM

入口：`vllm serve <model>`、OpenAI-compatible API、PagedAttention、continuous batching。

工程判断：

- vLLM 的价值主要在 serving：请求调度、KV cache 管理、吞吐。
- 单条 prompt 测试不能说明服务性能，至少要测并发、输入长度、输出长度。
- PagedAttention 解决的是 KV cache 管理和碎片问题，不是让模型质量变好。

## CUDA Programming Guide

入口：host/device、kernel、thread/block/grid、memory hierarchy、stream。

工程判断：

- CUDA 不是单个函数库，是编程模型、runtime、driver、库和硬件约定的组合。
- 写 CUDA kernel 时必须考虑并行粒度、内存访问模式和同步。
- cuBLAS/cuDNN/NCCL 是深度学习框架性能的重要来源。

## Huawei CANN / Ascend

入口：CANN、AscendCL、ATC、Ascend C、HCCL、MindSpeed-LLM。

工程判断：

- CANN 是昇腾 NPU 原生生态，不是 ZLUDA。
- 静态推理常见链路是 ONNX -> ATC -> OM -> AscendCL。
- PyTorch 适配昇腾通常看 torch_npu / MindSpeed-LLM / MindFormers 这类项目。
- 自定义算子看 Ascend C，不要把 CUDA kernel 直接搬过去。

## ONNX

入口：graph、node、operator、initializer、opset。

工程判断：

- ONNX 更偏模型交换和推理部署，不是大模型训练主格式。
- 导出成功不等于后端一定支持，算子和动态 shape 是常见问题。
- 部署前要做 PyTorch 输出和 ONNX/后端输出的一致性检查。

## ZLUDA

入口：项目 README 和 issue。

工程判断：

- ZLUDA 的定位是 CUDA compatibility layer。
- 它和华为昇腾 CANN 不是一个问题空间。
- 写教程时不要把“兼容 CUDA”说成“所有 CUDA 程序都能无痛运行”。

