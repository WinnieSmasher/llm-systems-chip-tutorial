# 00B. 自我 Review 记录

这一页记录我对前几版教程的审稿意见。保留它是为了提醒自己：教程不是把名词排整齐就算完成。

## 第一版的问题

### 1. 太像概念卡片

之前的写法经常是：

```text
X 是什么
Y 是什么
一句话总结
```

这种结构适合聊天解释，不适合开源教程。读者看完可能知道几个词，但不知道该读哪份文档、跑什么代码、如何验证自己理解对不对。

这轮修改：

- 每章末尾补来源。
- 增加 [资料来源地图](00-source-map.md)。
- 增加 [Hands-on Labs](08-hands-on-labs.md)。
- 用 `examples/` 放最小脚本。

### 2. 类比太多，工程细节太少

“PyTorch 模型像活的大脑，ONNX 像电路图”这类比可以建立直觉，但不能一直靠类比撑内容。

这轮修改：

- 在模型格式章节补 `config.json`、tokenizer、`.safetensors`、ONNX graph、OM 的工程位置。
- 在 CANN 章节补 AscendCL 推理流程伪代码。
- 在推理章节补 prefill/decode、KV cache 估算、vLLM 部署入口。

### 3. 缺少项目入口

之前写了很多“可以做项目”，但没有明确第一步。

这轮修改：

- `examples/minimal_inference.py`：Transformers 最小推理。
- `examples/minimal_sft_lora.py`：SFT + LoRA smoke test。
- `examples/estimate_kv_cache.py`：KV cache 显存估算。
- `examples/vllm_client.py`：调用本地 vLLM 服务。

### 4. 配图太简陋

之前只有手写 SVG，信息是对的，但不够像教程入口图。

这轮修改：

- 使用 image2 生成技术底图。
- 后期叠加中文标签和箭头，避免生成模型乱写文字。
- 保留底图和成图：`assets/image2-llm-systems-cover-base.png`、`assets/image2-llm-systems-cover.png`。

## 后续还缺什么

这份仓库还不是“完成品”。下一步应该补：

- 一个真实 vLLM 压测脚本。
- 一份小型 benchmark 结果表。
- CUDA / CANN API 对照表已经有第一版，还需要继续补真实 API 链接和代码样例。
- ONNX -> ATC -> OM 的流程文档已经有第一版，还缺实机日志。
- 一个 LoRA 数据清洗脚本。
- 对 DeepSeek、GLM、Qwen 这类模型的 model card 阅读记录。
