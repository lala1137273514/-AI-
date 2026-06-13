# 外部资源库（学习教程 / 主流仓库 / 资讯源）

> 维护规则：
> - 每个分区标注「核验日期」。引用超过 90 天未核验的条目时，须附一句「链接 X 月前核验过，若失效告诉我」。
> - 只增量：新条目加在对应分区表格末尾，附核验日期；失效条目移入文末「已失效」区留痕，不直接删。
> - 回答「怎么学 / 有什么仓库 / 怎么跟进动态」类问题，必须先读本文件，禁止凭记忆给链接。

## 1. 新人上手路径（按角色，最短路径）

| 角色 | 路径 |
|---|---|
| PM / 设计 / 测试（零基础） | 菜鸟教程中文课 → Claude Code Quickstart → Anthropic Academy「Claude Code 101」「Introduction to agent skills」→ prompt 交互教程 Sheets 版 |
| 工程师 | Quickstart → 官方 best-practices → DeepLearning.AI Claude Code 课 → Skills/Hooks/MCP/Subagents 四篇文档 → Agent SDK Quickstart + claude-cookbooks |
| 全员长期 | 订阅 baoyu.io、guizang.ai、simonwillison.net/tags/claude-code（见第 7 节跟进法） |

## 2. Claude 官方学习资源（核验：2026-06-11）

| 资源 | URL | 适合谁 | 耗时 |
|---|---|---|---|
| Claude Code 文档首页 | https://code.claude.com/docs/en/overview | 新手 | 0.5h |
| Quickstart | https://code.claude.com/docs/en/quickstart | 新手 | 0.5-1h |
| Skills 文档 | https://code.claude.com/docs/en/skills | 进阶 | 1-2h |
| Hooks 文档 | https://code.claude.com/docs/en/hooks | 进阶 | 1h |
| MCP 文档 | https://code.claude.com/docs/en/mcp | 进阶 | 1-2h |
| Subagents 文档 | https://code.claude.com/docs/en/sub-agents | 进阶 | 1h |
| 官方最佳实践（有中文版） | https://code.claude.com/docs/zh-CN/best-practices | 全员 | 1h |
| Anthropic Academy 免费课（101/skills/subagents/MCP 等，含证书） | https://anthropic.skilljar.com/ | 新手→进阶 | 单课 0.5-2h |
| Anthropic 学习资源总入口 | https://www.anthropic.com/learn | 新手 | 0.2h |
| claude-cookbooks（可执行 notebook） | https://github.com/anthropics/claude-cookbooks | 会 Python | 每篇 0.5-1h |
| Agent SDK 概览/Quickstart | https://platform.claude.com/docs/en/agent-sdk/overview | 工程师 | 1-2h |
| Agent SDK 官方 demo | https://github.com/anthropics/claude-agent-sdk-demos | 工程师 | 1-2h |
| DeepLearning.AI：Claude Code 课（免费） | https://www.deeplearning.ai/courses/claude-code-a-highly-agentic-coding-assistant | 新手→进阶 | 1-2h |
| DeepLearning.AI：MCP 课 | https://www.deeplearning.ai/courses/mcp-build-rich-context-ai-apps-with-anthropic | 工程师 | 1-2h |
| DeepLearning.AI：Agent Skills 课 | https://www.deeplearning.ai/courses/agent-skills-with-anthropic | 进阶 | 1-2h |

注：Academy 课程免费，但 Claude Code 101 动手部分需 Pro/Max/Team 订阅或 API key。

## 3. Codex 学习资源（核验：2026-06-11）

| 资源 | URL | 适合谁 | 耗时 |
|---|---|---|---|
| Codex 文档首页 | https://developers.openai.com/codex | 新手 | 0.5h |
| Quickstart | https://developers.openai.com/codex/quickstart | 新手 | 0.5h |
| CLI 文档 | https://developers.openai.com/codex/cli | 新手→进阶 | 1h |
| AGENTS.md 指南（类比 CLAUDE.md） | https://developers.openai.com/codex/guides/agents-md | 进阶 | 0.5h |
| 官方最佳实践 | https://developers.openai.com/codex/learn/best-practices | 进阶 | 1h |
| Codex Skills 文档 | https://developers.openai.com/codex/skills | 进阶 | 1h |
| openai/codex 开源仓库 | https://github.com/openai/codex | 工程师 | 按需 |

## 4. 中文教程与博主（核验：2026-06-11）

| 资源 | URL | 说明 |
|---|---|---|
| 宝玉博客（Claude Code 中文解读第一站） | https://baoyu.io/ | 重点文：官方团队 10 个内部技巧、skill 第一性原理拆解、Agent SDK 译文、省 token 指南 |
| 宝玉 skills 仓库 | https://github.com/JimLiu/baoyu-skills | 20+ 现成 skill，照着学写法 |
| 歸藏官网（工具实测/skill 案例，含飞书玩法） | https://www.guizang.ai/ | X：@op7418；AIGC Weekly 周刊：https://quaily.com/op7418 |
| 菜鸟教程 Claude Code 中文课 | https://www.runoob.com/claude-code/claude-code-tutorial.html | 零基础系统课，2-3h |
| claude-code-guide（国内配置指南） | https://github.com/claude-code-chinese/claude-code-guide | 解决国内访问/配置问题 |
| shareAI-lab/learn-claude-code（源码级剖析） | https://github.com/shareAI-lab/learn-claude-code | 工程师进阶，理解 agent loop 底层 |

## 5. Prompt 工程（核验：2026-06-11）

| 资源 | URL | 适合谁 |
|---|---|---|
| 官方 Prompting Best Practices | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | 全员 |
| 官方交互式教程（9 章习题，有免代码 Sheets 版） | https://github.com/anthropics/prompt-eng-interactive-tutorial | 新手→进阶（PM/测试用 Sheets 版） |
| anthropics/courses 官方课程仓库 | https://github.com/anthropics/courses | 进阶 |
| 工程博客：Effective context engineering for AI agents | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 进阶 |

## 6. 主流 GitHub 仓库（核验：2026-06-10，star 经 GitHub API 拉取）

**Agent 框架/SDK**

| 仓库 | URL | 干什么 / 我们何时用 | Star |
|---|---|---|---|
| anthropics/claude-agent-sdk-python | https://github.com/anthropics/claude-agent-sdk-python | 团队首选：第二周工程化写飞书 bot 后端 | 7k+ |
| langchain-ai/langgraph | https://github.com/langchain-ai/langgraph | 流程复杂到单 agent 撑不住（多步审批/长流程）再上 | 34k+ |
| crewAIInc/crewAI | https://github.com/crewAIInc/crewAI | 给新手演示多 agent 分工、快速 demo | 53k+ |
| run-llama/llama_index | https://github.com/run-llama/llama_index | 把团队文档库做成可检索知识库（RAG）时用 | 50k+ |

注：microsoft/autogen 已进维护模式，新项目别选；OpenHands 与 Claude Code 定位重叠，无需引入。

**Claude Code 生态**

| 仓库 | URL | 干什么 / 我们何时用 | Star |
|---|---|---|---|
| anthropics/claude-code | https://github.com/anthropics/claude-code | 查 bug、追新功能的第一入口 | 130k+ |
| anthropics/skills | https://github.com/anthropics/skills | 官方 skill 范本；文档自动化直接装 | 148k+ |
| obra/superpowers | https://github.com/obra/superpowers | 团队已装；新成员工作纪律必读 | 220k+ |
| modelcontextprotocol/servers | https://github.com/modelcontextprotocol/servers | 接外部系统前先找官方 MCP 实现 | 87k+ |
| punkpeye/awesome-mcp-servers | https://github.com/punkpeye/awesome-mcp-servers | 查「有没有现成 MCP 连 X」防造轮子 | 88k+ |

**工作流/低代码**

| 仓库 | URL | 干什么 / 我们何时用 | Star |
|---|---|---|---|
| n8n-io/n8n | https://github.com/n8n-io/n8n | 非工程成员搭定时任务首选；团队已接 n8n-mcp | 190k+ |
| langgenius/dify | https://github.com/langgenius/dify | 给非技术同事「填提示词就上线小应用」的界面 | 144k+ |
| FlowiseAI/Flowise | https://github.com/FlowiseAI/Flowise | 拖拽快速做 chatbot/RAG 原型给业务方看 | 53k+ |

**评测/可观测**

| 仓库 | URL | 干什么 / 我们何时用 | Star |
|---|---|---|---|
| langfuse/langfuse | https://github.com/langfuse/langfuse | bot 上线后查质量/成本；团队已有 langfuse skill | 28k+ |
| promptfoo/promptfoo | https://github.com/promptfoo/promptfoo | 提示词改版前跑 A/B 回归防改崩（2026-03 被 OpenAI 收购，仍 MIT） | 22k+ |
| confident-ai/deepeval | https://github.com/confident-ai/deepeval | 把输出质量写成 pytest 断言进 CI | 16k+ |

**awesome 总入口**

| 仓库 | URL | 干什么 | Star |
|---|---|---|---|
| Shubhamsaboo/awesome-llm-apps | https://github.com/Shubhamsaboo/awesome-llm-apps | 几百个带代码的 LLM 应用示例，没思路先来找同类 | 114k+ |
| hesreallyhim/awesome-claude-code | https://github.com/hesreallyhim/awesome-claude-code | 现成 slash command / CLAUDE.md / workflow 范例 | 46k+ |
| travisvn/awesome-claude-skills | https://github.com/travisvn/awesome-claude-skills | 找现成 skill、学写法 | 13k+ |

## 7. 资讯源与每周 30 分钟跟进法（核验：2026-06-11）

**必看源**

| 源 | 地址 | 频率 |
|---|---|---|
| Claude Code Changelog | https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md | 每周多次发版，GitHub Watch→Releases 收通知 |
| Anthropic news / engineering | https://www.anthropic.com/news 、https://www.anthropic.com/engineering | 每周数篇 |
| 宝玉 X | https://x.com/dotey | 每日 |
| 歸藏 AIGC Weekly | https://quaily.com/op7418 | 每周一期 |
| Simon Willison | https://simonwillison.net/ | 几乎每日 |

**可选源**：TLDR AI（https://tldr.tech/ai ，兜底日报）、Latent Space AINews（https://www.latent.space/s/ainews ）、Founder Park 公众号（深读访谈）、机器之心/量子位（重大发布自然刷屏，不必主动追）、r/ClaudeAI 周榜（https://www.reddit.com/r/ClaudeAI/ ，比官方更早暴露版本坑）、GitHub Trending（https://github.com/trending ，每周扫一次）。

**每周 30 分钟跟进法（教练执行，转播团队）**

| 时间 | 动作 |
|---|---|
| 10 min | 扫 Claude Code Changelog（有无影响内部自动化的变更）+ 歸藏周刊 |
| 10 min | 刷宝玉 + Simon Willison 本周文章，只收藏能落到我们工作流的 2-3 条 |
| 5 min | r/ClaudeAI 周榜 + HN 搜「Claude Code」查漏 |
| 5 min | 摘 3-5 条成飞书卡片发团队群，每条附一句「我们可以怎么用」 |

## 已失效（留痕区）

（暂无条目）
