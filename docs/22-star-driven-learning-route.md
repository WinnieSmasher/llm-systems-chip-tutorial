# 22. Star 驱动的学习路线

这条路线不是“每周 clone 几个 repo”。它把 starred repos 背后的知识拆成 8 周训练，每周都要交付一个小成果。

![Star-driven learning route](../assets/image2-star-learning-route.svg)

## 第 0 周：建立资料入口

能力目标：

- 分清 PDF parsing、OCR、layout analysis、Markdown conversion。
- 知道复杂文档进入 RAG 前会丢什么信息。
- 能判断一个文档处理结果是否适合进入知识库。

练习：

- 找一篇双栏论文或带公式的 PDF。
- 用两种工具转成 Markdown。
- 标出公式、表格、图注、参考文献的错误。

输出物：

- 一页 document ingestion failure note。
- 一张“PDF -> Markdown -> chunks -> retrieval”的流程图。

参考来源：MinerU、MarkItDown、PDFMathTranslate、BabelDOC。

## 第 1 周：理解 Agent runtime

能力目标：

- 把 agent 看成状态机，而不是“会自动干活的模型”。
- 分清 prompt、skill、tool、MCP、memory、verification 的位置。
- 能解释 tool boundary 和外部内容不可信原则。

练习：

- 画一个 coding agent 执行任务的状态机。
- 写出一次任务里的 plan、edit、test、review、commit 节点。
- 给每个节点标出需要的证据。

输出物：

- 一张 agent loop 图。
- 一个 tool boundary checklist。

参考来源：Codex、Anthropic Skills、MCP、OpenCode、Superpowers。

## 第 2 周：做一个可复盘的 coding workflow

能力目标：

- 理解为什么计划、测试、review、commit 要固定下来。
- 知道任务状态应该记录在哪里。
- 能区分“自动化执行”和“可复盘执行”。

练习：

- 为本仓库写一份小任务流程：需求、计划、修改、验证、提交。
- 找一个已有脚本或文档做小修，严格按流程记录。
- 写下哪里最容易漏验证。

输出物：

- 一页 workflow comparison。
- 一份本仓库任务 checklist。

参考来源：OpenCode、Archon、oh-my-openagent、Superpowers。

## 第 3 周：做一个小型 RAG 评测

能力目标：

- 分清 indexing、chunking、embedding、rerank、generation。
- 知道 RAG 失败不一定是模型差，也可能是切分、召回或证据错误。
- 能用固定问题集比较配置变化。

练习：

- 准备 20 条问题和人工证据片段。
- 改变 chunk size 或 top-k。
- 记录至少 5 个失败样例。

输出物：

- 一个 RAG failure table。
- 一段关于 chunking 取舍的短说明。

参考来源：Paper QA、Langchain-Chatchat、Supermemory、LangBot。

## 第 4 周：读一个 CUDA/kernel 示例

能力目标：

- 看懂 grid、block、thread 怎么映射到数据。
- 能解释 global memory 和 shared memory 的基本区别。
- 能把一个 kernel 的访存模式画出来。

练习：

- 选一个小 CUDA kernel。
- 写出输入、输出、线程索引、访存路径。
- 标出可能的 memory coalescing 问题。

输出物：

- 一页 kernel reading note。
- 一张 thread/data mapping 图。

参考来源：LeetCUDA、ZLUDA、gprMax。

## 第 5 周：把 benchmark 写成工程实验

能力目标：

- 理解 benchmark 的关键是固定场景和可重复。
- 能分清 TTFT、TPOT、throughput、latency、memory。
- 知道只展示最好结果没有意义。

练习：

- 选一个小模型或模拟服务。
- 固定输入长度、输出长度、并发、硬件、模型版本。
- 记录最好结果、中位数和失败结果。

输出物：

- 一份 benchmark scenario。
- 一张结果表。

参考来源：vLLM、OR-Tools 的约束建模思想、量化/回测框架里的现实约束处理方式。

## 第 6 周：整理科研阅读和图表

能力目标：

- 用论文回答工程问题，而不是背论文名。
- 能复述一篇论文的 problem、method、experiment、limitation。
- 能判断一张图表到底在证明什么。

练习：

- 选一篇 LLM systems 论文。
- 写一页笔记。
- 复画一张结构图或实验表。

输出物：

- 一页 paper note。
- 一张改写后的图或表。

参考来源：Papers We Love、PaperBanana、ChatPaper、OpenPrism。

## 第 7 周：补安全边界

能力目标：

- 知道哪些工具不该进入公开教程主线。
- 能识别账号、代理、中转、注册、激活、抢票类项目的风险。
- 能解释 prompt injection 为什么不能靠 system prompt 解决。

练习：

- 写一个工具风险判断清单。
- 给本仓库的 RAG/Agent 章节补一个外部内容不可信的测试点。
- 记录一个“技术上能做但不该做”的例子。

输出物：

- 一份 risk boundary checklist。
- 一组 prompt injection 测试样例。

参考来源：Web security、OSINT、reverse engineering 资料，以及风险隔离类工具作为反面样本。

## 第 8 周：整理成公开成果

能力目标：

- 把前 7 周的材料压缩成别人能读的教程。
- 删除工具清单味道，保留概念、实验、源码问题和失败案例。
- 找出 1 到 3 个可以做 issue/PR 的开源贡献方向。

练习：

- 回看每个输出物，删掉不能验证的句子。
- 每条路线只保留一个代表实验。
- 写 3 个开源贡献候选。

输出物：

- 更新后的 README 入口。
- 3 个 source reading notes。
- 1 个开源贡献计划。
