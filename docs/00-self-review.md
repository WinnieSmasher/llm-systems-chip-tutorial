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

- 一个真实 vLLM 压测记录。
- 一份小型 benchmark 结果表。
- CUDA / CANN API 对照表已经有第一版，还需要继续补真实 API 链接和代码样例。
- ONNX -> ATC -> OM 的流程文档已经有第一版，还缺实机日志。
- 对 DeepSeek、GLM、Qwen 这类模型的 model card 阅读记录。

## 第二版的问题

这轮 review 发现一个更大的问题：仓库已经有章节、脚本和资料，但入口仍然不像教程。

具体表现：

- README 更像路线推荐，不像课程首页。
- 21/22/24 的标题还在强调 starred repos，容易让读者以为重点是收藏夹。
- 目录编号缺了 23，说明内容组织还没有被当成课程产品维护。
- 开源项目没有被放到“概念、实验、问题、checklist”的教学框架里。

这轮修改：

- README 改成课程首页，补课程大纲、推荐阅读顺序、每周输出物。
- [00. 学习地图](00-learning-map.md) 改成阶段表，明确每一层的核心问题和最小产出。
- 将 21/22/24 重命名为 [21. 开源项目知识提炼地图](21-knowledge-extraction-map.md)、[22. 八周能力路线](22-eight-week-learning-route.md)、[23. 源码阅读题单](23-source-reading-questions.md)。
- 配图从 star 叙事改成知识提炼和能力路线叙事。

后续写任何新章节，都要先回答三个问题：

1. 读者读完这一章要能解释什么？
2. 读者要跑什么、画什么、写什么？
3. 这一章和前后章节是什么关系？
