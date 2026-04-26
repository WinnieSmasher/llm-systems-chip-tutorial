# 21. 从 100 个 Starred Repos 清洗知识地图

这页不是“我 star 了什么”的展示页，而是把公开 star 列表当成一批原始资料，清洗成能指导学习和开源贡献的知识地图。

本次读取范围：GitHub public starred repositories 共 100 个；README 成功读取 93 个，其余 7 个用仓库 metadata、topics、description 补足。公开文档里不保留精确 star 时间戳，因为它对学习路线没有价值。

![Starred repo knowledge map](../assets/image2-star-knowledge-map.svg)

## 清洗规则

| 规则 | 解释 |
| --- | --- |
| A 核心学习 | 和 LLM systems、AI infra、chip/CUDA/CANN、agent runtime、科研文档智能直接相关，值得写实验或源码笔记。 |
| B 可读可练 | 能提供工程经验或领域方法，但不是当前教程主线。 |
| C 参考资料 | 工具性、资料性或个人效率类，按需要查，不主动深挖。 |
| D 隔离观察 | 账号、代理、中转、注册、激活、抢票等风险或合规边界较多的项目，不进入教程主线。 |

## 分类概览

| 分类 | 数量 | A 核心 | B 可读 | D 隔离 |
| --- | ---: | ---: | ---: | ---: |
| 安全/逆向/移动系统 | 17 | 0 | 8 | 0 |
| 风险隔离/账号与代理工具 | 16 | 1 | 0 | 15 |
| 工具/自托管/个人效率 | 14 | 0 | 0 | 0 |
| 科研写作/文档智能 | 10 | 4 | 6 | 0 |
| 量化/金融工程 | 4 | 0 | 2 | 0 |
| 系统性能/芯片/优化 | 5 | 3 | 2 | 0 |
| 资源索引/待观察 | 6 | 1 | 1 | 0 |
| Agent/Codex 工作流 | 25 | 10 | 15 | 0 |
| LLM 应用/AI Infra | 3 | 2 | 1 | 0 |

## 进入教程主线的项目

这些项目最值得后续写成章节、实验或源码阅读笔记。

| Repo | 语言 | 层级 | 可抽取知识 | 下一步 |
| --- | --- | --- | --- | --- |
| [anomalyco/opencode](https://github.com/anomalyco/opencode) | TypeScript | A 核心学习 | agent loop、skill、MCP、状态、工具边界 | 纳入主线，做源码/实验笔记 |
| [anthropics/skills](https://github.com/anthropics/skills) | Python | A 核心学习 | agent loop、skill、MCP、状态、工具边界 | 纳入主线，做源码/实验笔记 |
| [microsoft/markitdown](https://github.com/microsoft/markitdown) | Python | A 核心学习 | PDF/Markdown/引用/论文工作流/知识抽取 | 纳入主线，做源码/实验笔记 |
| [Comfy-Org/ComfyUI](https://github.com/Comfy-Org/ComfyUI) | Python | A 核心学习 | RAG、memory、metadata、bot、可视化工作流 | 纳入主线，做源码/实验笔记 |
| [openai/codex](https://github.com/openai/codex) | Rust | A 核心学习 | agent loop、skill、MCP、状态、工具边界 | 纳入主线，做源码/实验笔记 |
| [opendatalab/MinerU](https://github.com/opendatalab/MinerU) | Python | A 核心学习 | agent loop、skill、MCP、状态、工具边界 | 纳入主线，做源码/实验笔记 |
| [chatchat-space/Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) | Python | A 核心学习 | agent loop、skill、MCP、状态、工具边界 | 纳入主线，做源码/实验笔记 |
| [PDFMathTranslate/PDFMathTranslate](https://github.com/PDFMathTranslate/PDFMathTranslate) | Python | A 核心学习 | agent loop、skill、MCP、状态、工具边界 | 纳入主线，做源码/实验笔记 |
| [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything) | Python | A 核心学习 | agent loop、skill、MCP、状态、工具边界 | 纳入主线，做源码/实验笔记 |
| [bytedance/UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop) | TypeScript | A 核心学习 | agent loop、skill、MCP、状态、工具边界 | 纳入主线，做源码/实验笔记 |
| [supermemoryai/supermemory](https://github.com/supermemoryai/supermemory) | TypeScript | A 核心学习 | agent loop、skill、MCP、状态、工具边界 | 纳入主线，做源码/实验笔记 |
| [vosen/ZLUDA](https://github.com/vosen/ZLUDA) | Rust | A 核心学习 | 性能瓶颈、kernel/runtime、硬件生态、benchmark | 纳入主线，做源码/实验笔记 |
| [xlite-dev/LeetCUDA](https://github.com/xlite-dev/LeetCUDA) | Cuda | A 核心学习 | 性能瓶颈、kernel/runtime、硬件生态、benchmark | 纳入主线，做源码/实验笔记 |
| [Future-House/paper-qa](https://github.com/Future-House/paper-qa) | Python | A 核心学习 | PDF/Markdown/引用/论文工作流/知识抽取 | 纳入主线，做源码/实验笔记 |
| [funstory-ai/BabelDOC](https://github.com/funstory-ai/BabelDOC) | Python | A 核心学习 | PDF/Markdown/引用/论文工作流/知识抽取 | 纳入主线，做源码/实验笔记 |
| [modelcontextprotocol/rust-sdk](https://github.com/modelcontextprotocol/rust-sdk) | Rust | A 核心学习 | 资料入口、工具配置、工程习惯 | 纳入主线，做源码/实验笔记 |
| [wyf3/llm_related](https://github.com/wyf3/llm_related) | Python | A 核心学习 | RAG、memory、metadata、bot、可视化工作流 | 纳入主线，做源码/实验笔记 |
| [agentclientprotocol/agent-client-protocol](https://github.com/agentclientprotocol/agent-client-protocol) | Rust | A 核心学习 | agent loop、skill、MCP、状态、工具边界 | 纳入主线，做源码/实验笔记 |
| [gprMax/gprMax](https://github.com/gprMax/gprMax) | Python | A 核心学习 | 性能瓶颈、kernel/runtime、硬件生态、benchmark | 纳入主线，做源码/实验笔记 |
| [caomaolufei/AIInfraGuide](https://github.com/caomaolufei/AIInfraGuide) | Astro | A 核心学习 | PDF/Markdown/引用/论文工作流/知识抽取 | 纳入主线，做源码/实验笔记 |
| [basellm/llm-metadata](https://github.com/basellm/llm-metadata) | TypeScript | A 核心学习 | 识别合规风险和供应链风险 | 纳入主线，做源码/实验笔记 |

## 可读可练项目

这些项目不一定全部进入主线，但很适合做专题阅读或工程对照。

| Repo | 语言 | 层级 | 可抽取知识 | 下一步 |
| --- | --- | --- | --- | --- |
| [obra/superpowers](https://github.com/obra/superpowers) | Shell | B 可读可练 | agent loop、skill、MCP、状态、工具边界 | 抽取 agent runtime、skill、MCP、评审流程 |
| [papers-we-love/papers-we-love](https://github.com/papers-we-love/papers-we-love) | Shell | B 可读可练 | PDF/Markdown/引用/论文工作流/知识抽取 | 转化为论文/PDF/知识库处理流程 |
| [code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) | TypeScript | B 可读可练 | agent loop、skill、MCP、状态、工具边界 | 抽取 agent runtime、skill、MCP、评审流程 |
| [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) | Python | B 可读可练 | agent loop、skill、MCP、状态、工具边界 | 抽取 agent runtime、skill、MCP、评审流程 |
| [farion1231/cc-switch](https://github.com/farion1231/cc-switch) | Rust | B 可读可练 | agent loop、skill、MCP、状态、工具边界 | 抽取 agent runtime、skill、MCP、评审流程 |
| [vnpy/vnpy](https://github.com/vnpy/vnpy) | Python | B 可读可练 | 回测、约束建模、优化、事件驱动系统 | 抽取工程约束/回测思想，不当赚钱策略 |
| [jivoi/awesome-osint](https://github.com/jivoi/awesome-osint) | Unknown | B 可读可练 | 系统边界、逆向分析、移动端安全、合规意识 | 只作为系统安全阅读，不写攻击型教程 |
| [iBotPeaches/Apktool](https://github.com/iBotPeaches/Apktool) | Java | B 可读可练 | 系统边界、逆向分析、移动端安全、合规意识 | 只作为系统安全阅读，不写攻击型教程 |
| [coleam00/Archon](https://github.com/coleam00/Archon) | TypeScript | B 可读可练 | agent loop、skill、MCP、状态、工具边界 | 抽取 agent runtime、skill、MCP、评审流程 |
| [Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) | Unknown | B 可读可练 | PDF/Markdown/引用/论文工作流/知识抽取 | 转化为论文/PDF/知识库处理流程 |
| [kaixindelele/ChatPaper](https://github.com/kaixindelele/ChatPaper) | Python | B 可读可练 | PDF/Markdown/引用/论文工作流/知识抽取 | 转化为论文/PDF/知识库处理流程 |
| [langbot-app/LangBot](https://github.com/langbot-app/LangBot) | Python | B 可读可练 | agent loop、skill、MCP、状态、工具边界 | 抽取 agent runtime、skill、MCP、评审流程 |
| [blader/humanizer](https://github.com/blader/humanizer) | Unknown | B 可读可练 | agent loop、skill、MCP、状态、工具边界 | 抽取 agent runtime、skill、MCP、评审流程 |
| [mytechnotalent/Reverse-Engineering](https://github.com/mytechnotalent/Reverse-Engineering) | Assembly | B 可读可练 | 系统边界、逆向分析、移动端安全、合规意识 | 只作为系统安全阅读，不写攻击型教程 |
| [google/or-tools](https://github.com/google/or-tools) | C++ | B 可读可练 | 性能瓶颈、kernel/runtime、硬件生态、benchmark | 保留为参考，后续按任务再读 |
| [qazbnm456/awesome-web-security](https://github.com/qazbnm456/awesome-web-security) | Unknown | B 可读可练 | 系统边界、逆向分析、移动端安全、合规意识 | 只作为系统安全阅读，不写攻击型教程 |
| [yutiansut/QUANTAXIS](https://github.com/yutiansut/QUANTAXIS) | Python | B 可读可练 | 回测、约束建模、优化、事件驱动系统 | 抽取工程约束/回测思想，不当赚钱策略 |
| [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) | JavaScript | B 可读可练 | agent loop、skill、MCP、状态、工具边界 | 抽取 agent runtime、skill、MCP、评审流程 |
| [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | Python | B 可读可练 | agent loop、skill、MCP、状态、工具边界 | 抽取 agent runtime、skill、MCP、评审流程 |
| [shaxiu/XianyuAutoAgent](https://github.com/shaxiu/XianyuAutoAgent) | Python | B 可读可练 | agent loop、skill、MCP、状态、工具边界 | 抽取 agent runtime、skill、MCP、评审流程 |
| [lballabio/QuantLib](https://github.com/lballabio/QuantLib) | C++ | B 可读可练 | 性能瓶颈、kernel/runtime、硬件生态、benchmark | 保留为参考，后续按任务再读 |
| [Bistutu/FluentRead](https://github.com/Bistutu/FluentRead) | TypeScript | B 可读可练 | PDF/Markdown/引用/论文工作流/知识抽取 | 转化为论文/PDF/知识库处理流程 |
| [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh) | Unknown | B 可读可练 | agent loop、skill、MCP、状态、工具边界 | 抽取 agent runtime、skill、MCP、评审流程 |
| [punkpeye/awesome-mcp-clients](https://github.com/punkpeye/awesome-mcp-clients) | Unknown | B 可读可练 | agent loop、skill、MCP、状态、工具边界 | 抽取 agent runtime、skill、MCP、评审流程 |

## 隔离观察项目

下面这些项目不适合写进 LLM systems/chip 教程主线。可以用来训练“识别工具风险和合规边界”的能力，但不要把它们包装成学习成果。

| Repo | 语言 | 层级 | 可抽取知识 | 下一步 |
| --- | --- | --- | --- | --- |
| [7836246/aws-builder-id](https://github.com/7836246/aws-builder-id) | Python | D 隔离观察 | 识别合规风险和供应链风险 | 不纳入教程主线，只记录合规边界 |
| [7836246/cursor2api](https://github.com/7836246/cursor2api) | TypeScript | D 隔离观察 | 识别合规风险和供应链风险 | 不纳入教程主线，只记录合规边界 |
| [FakeOAI/tokens](https://github.com/FakeOAI/tokens) | Shell | D 隔离观察 | 识别合规风险和供应链风险 | 不纳入教程主线，只记录合规边界 |
| [kaitranntt/ccs](https://github.com/kaitranntt/ccs) | TypeScript | D 隔离观察 | 识别合规风险和供应链风险 | 不纳入教程主线，只记录合规边界 |
| [LainsNL/OutlookRegister](https://github.com/LainsNL/OutlookRegister) | Python | D 隔离观察 | 识别合规风险和供应链风险 | 不纳入教程主线，只记录合规边界 |
| [LightCountry/TokenPay](https://github.com/LightCountry/TokenPay) | C# | D 隔离观察 | 识别合规风险和供应链风险 | 不纳入教程主线，只记录合规边界 |
| [Loongphy/codex-auth](https://github.com/Loongphy/codex-auth) | Zig | D 隔离观察 | 识别合规风险和供应链风险 | 不纳入教程主线，只记录合规边界 |
| [massgravel/Microsoft-Activation-Scripts](https://github.com/massgravel/Microsoft-Activation-Scripts) | Batchfile | D 隔离观察 | 识别合规风险和供应链风险 | 不纳入教程主线，只记录合规边界 |
| [QuantumNous/new-api](https://github.com/QuantumNous/new-api) | Go | D 隔离观察 | 识别合规风险和供应链风险 | 不纳入教程主线，只记录合规边界 |
| [router-for-me/CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI) | Go | D 隔离观察 | 识别合规风险和供应链风险 | 不纳入教程主线，只记录合规边界 |
| [ryfineZ/codex-session-patcher](https://github.com/ryfineZ/codex-session-patcher) | Python | D 隔离观察 | 识别合规风险和供应链风险 | 不纳入教程主线，只记录合规边界 |
| [Ttungx/codex_auto_register](https://github.com/Ttungx/codex_auto_register) | HTML | D 隔离观察 | 识别合规风险和供应链风险 | 不纳入教程主线，只记录合规边界 |
| [WECENG/ticket-purchase](https://github.com/WECENG/ticket-purchase) | Python | D 隔离观察 | 识别合规风险和供应链风险 | 不纳入教程主线，只记录合规边界 |
| [Wei-Shaw/sub2api](https://github.com/Wei-Shaw/sub2api) | Go | D 隔离观察 | 识别合规风险和供应链风险 | 不纳入教程主线，只记录合规边界 |
| [yukkcat/gemini-business2api](https://github.com/yukkcat/gemini-business2api) | Python | D 隔离观察 | 识别合规风险和供应链风险 | 不纳入教程主线，只记录合规边界 |

## 这批 star 说明了什么

你的兴趣不是单点的“LLM 应用”，而是四条线纠缠在一起：

1. Agent runtime：Codex、OpenCode、skills、MCP、workflow、memory。
2. LLM 系统工程：文档解析、RAG、bot、metadata、模型工具链。
3. 芯片/性能：CUDA、ZLUDA、GPU kernel、优化建模、FDTD/GPR 这类科学计算。
4. 研究生产力：论文翻译、PDF 清洗、图表生成、academic writing workspace。

这其实是一个不错的组合：如果后续项目都围绕“让 AI Agent 读懂科学文档、跑实验、解释系统性能”来组织，就比单纯收藏工具更有辨识度。
