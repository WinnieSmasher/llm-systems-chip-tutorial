# 24. Source Reading Queue

这页不是项目清单，而是源码阅读题单。读源码前先定问题，否则很容易从 README 看到 issue，再从 issue 跳到另一个工具，最后什么都没留下。

每个题目只要求一个小输出：一页笔记、一张图、一个 checklist 或一个最小实验。

## A. Agent runtime

### A1. Agent 的状态机在哪里

阅读问题：

- 一个任务从用户输入到工具调用，中间有哪些状态？
- 状态存在内存、文件、数据库还是会话上下文里？
- 任务失败后如何恢复？

输出物：

- 一张 `idle -> planning -> acting -> verifying -> done/blocked` 状态图。
- 一段说明：哪些状态适合持久化，哪些状态只适合留在当前上下文。

参考来源：Codex、OpenCode、Superpowers、Archon。

### A2. Tool boundary 怎么设计

阅读问题：

- 工具调用前如何确认权限和风险？
- 工具返回内容会不会被当成指令？
- 文件、网页、PDF、issue 评论进入上下文时有什么隔离规则？

输出物：

- 一份 tool boundary checklist。
- 3 个测试样例：安全输入、恶意网页文本、含敏感字段的工具输出。

参考来源：Anthropic Skills、MCP、Codex tool policies。

### A3. Skill 和 prompt 模板有什么区别

阅读问题：

- Skill 是否规定了触发条件、步骤、验证方式和停止条件？
- 它能不能跨项目复用？
- 它如何避免“每次重新发明流程”？

输出物：

- 一页 skill anatomy note。
- 给本仓库设计一个 `source-reading` skill 草案。

参考来源：Anthropic Skills、Superpowers。

## B. 文档智能

### B1. PDF parsing 失败在哪里

阅读问题：

- 工具如何处理双栏、公式、表格、页眉页脚、脚注？
- 输出 Markdown 是否保留章节层级？
- 转换错误会不会影响后续检索和引用？

输出物：

- 一张 failure table：原始片段、转换结果、错误类型、对 RAG 的影响。

参考来源：MinerU、PDFMathTranslate、BabelDOC。

### B2. Office / HTML / README 怎么进入统一格式

阅读问题：

- 不同文件格式是否都能变成稳定 Markdown？
- 图片、表格、代码块如何处理？
- metadata 和正文是否分开保存？

输出物：

- 一个 document ingestion pipeline 图。
- 一个最小字段设计：source、title、section、content、page、metadata。

参考来源：MarkItDown、MinerU。

## C. RAG 和 memory

### C1. Chunking 怎么影响召回

阅读问题：

- chunk size、overlap、标题路径对召回有什么影响？
- top-k 增大为什么不一定变好？
- rerank 解决的是哪一段问题？

输出物：

- 20 条固定问题的召回对比表。
- 至少 5 条失败案例。

参考来源：Paper QA、Langchain-Chatchat。

### C2. Memory 和日志有什么区别

阅读问题：

- 什么内容应该进入 memory？
- memory 如何更新、删除和过期？
- 用户隐私和权限如何处理？

输出物：

- 一张 memory lifecycle 图。
- 一份“不该写入 memory”的例子清单。

参考来源：Supermemory、Agent memory 项目。

## D. CUDA / ZLUDA / kernel

### D1. 一个 kernel 如何映射数据

阅读问题：

- thread index 如何对应输入数据？
- block/grid 维度为什么这样设？
- 相邻线程是否访问相邻地址？

输出物：

- 一张 thread/data mapping 图。
- 一页 kernel reading note。

参考来源：LeetCUDA。

### D2. 兼容层解决什么，不解决什么

阅读问题：

- CUDA 兼容层拦截的是 API、kernel、runtime 还是 driver 层？
- 哪些 CUDA 程序容易跑，哪些不容易？
- 兼容层和原生 CANN / AscendCL 是什么关系？

输出物：

- 一张 CUDA / ZLUDA / CANN 边界图。
- 一段说明：为什么 ZLUDA 不是“昇腾版 CUDA”。

参考来源：ZLUDA、CANN docs。

### D3. 科学计算项目里的 GPU 代码怎么读

阅读问题：

- 数值方法的更新公式在哪里？
- CPU 和 GPU 版本如何保持一致？
- 测试怎么证明 GPU 结果没有偏？

输出物：

- 一页 gprMax GPU 代码阅读笔记。
- 一个测试覆盖建议。

参考来源：gprMax。

## E. Benchmark 和工程约束

### E1. benchmark scenario 怎么写

阅读问题：

- 输入长度、输出长度、并发、模型、硬件、量化方式是否固定？
- 记录的是平均值、中位数、P95 还是最好值？
- 失败请求是否进入结果？

输出物：

- 一个 benchmark scenario JSON。
- 一张结果表模板。

参考来源：vLLM benchmark 思路、OR-Tools 的约束建模习惯。

### E2. 现实约束怎么进入系统

阅读问题：

- 系统如何处理手续费、容量、延迟、失败重试、资源限制？
- 哪些约束是硬约束，哪些是可调参数？
- 约束违反时是拒绝执行、降级还是报警？

输出物：

- 一张 constraints table。
- 一个“输入 -> 约束 -> 决策 -> 输出”的流程图。

参考来源：vn.py、QuantLib、OR-Tools。

## F. 科研写作和图表

### F1. 一篇论文怎么读成工程问题

阅读问题：

- 论文解决的系统瓶颈是什么？
- 实验指标是否能复现？
- 哪个模块能迁移到自己的项目？

输出物：

- 一页 paper note。
- 一个 reproduction idea。

参考来源：Papers We Love、LLM systems papers。

### F2. 图表如何降低理解成本

阅读问题：

- 这张图解释结构、流程、对比还是实验结果？
- 有没有把无关视觉元素删掉？
- 图注是否能独立说明变量和结论？

输出物：

- 一张重画后的架构图或实验表。
- 一段图注。

参考来源：PaperBanana、OpenPrism。

## G. 安全边界

### G1. 哪些工具不进入教程主线

阅读问题：

- 是否涉及账号注册、绕过限制、激活、抢票、代理中转或 token 管理？
- 是否会伤害第三方服务或违反平台规则？
- 是否需要处理敏感数据？

输出物：

- 一份 reject checklist。
- 三个“不写进教程”的例子和理由。

参考来源：风险隔离类项目、安全/逆向资料。

### G2. 外部内容如何防 prompt injection

阅读问题：

- README、网页、PDF、issue 评论里出现“忽略系统指令”怎么办？
- 哪些内容只能作为数据，不能作为指令？
- 测试里如何模拟恶意外部内容？

输出物：

- 一组 prompt injection regression cases。
- 一份 agent input sanitization checklist。

参考来源：OWASP LLM Top 10、安全资料、Agent tool policy。
