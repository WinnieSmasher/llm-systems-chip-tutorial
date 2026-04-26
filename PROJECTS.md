# Project Backlog

这个文件记录后续可以继续扩展的方向。

## Documentation

- [ ] 增加 CUDA kernel 入门示例。
- [ ] 增加 AscendCL 推理伪代码。
- [x] 增加 ONNX -> ATC -> `.om` 流程示意。
- [x] 增加 vLLM 压测脚本。
- [ ] 增加 LoRA 数据清洗示例。
- [x] 增加 KV Cache 显存估算脚本。
- [x] 增加 vLLM OpenAI-compatible client。

## Experiments

- [ ] 比较不同 context length 下的推理延迟，并填入 `benchmarks/results-template.csv`。
- [ ] 比较 FP16、INT8、INT4 的输出质量。
- [x] 增加 KV Cache 显存 sweep 脚本。
- [ ] 对比 Transformers 原生推理和 vLLM 推理吞吐。

## Resume Materials

- [ ] 整理大模型系统方向简历 bullet。
- [ ] 整理芯片/异构计算方向简历 bullet。
- [ ] 整理开源贡献型经历模板。
- [ ] 补充真实 vLLM benchmark 结果。
- [x] 补充 CUDA / CANN API 对照表。
- [x] 补充 ONNX -> ATC -> OM 流程文档。
- [ ] 补充 ONNX -> ATC -> OM 实机日志。
