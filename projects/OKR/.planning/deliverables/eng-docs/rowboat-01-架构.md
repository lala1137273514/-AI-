# rowboat · 架构文档

> 团队可读架构说明。来源：rowboat 仓库 `.planning/codebase/ARCHITECTURE.md` + `CLAUDE.md` + `evals/humanization/DESIGN.md` + `.planning/v1.3-MEMORY-LOOP-DESIGN.md`。
> 一句话定位：rowboat 是一个**本地优先（local-first）的 Electron 桌面 AI agent**，目标是用户的"第二大脑"——本地知识库 + 记忆 + 关注层 + persona，跨 session 长期沉淀。本文聚焦两条工程主线：**KB/记忆回路** 与 **人性化收束层评测器**。

---

## 1. 系统全景

```
Electron 三进程
  main (Node.js)  ─ contextBridge ─  preload  ─ window.ipc ─  renderer (React/Vite)
    │  所有业务逻辑、文件系统、后台服务
    ▼
  @x/core  (apps/x/packages/core)   ← 全部 AI/KB/集成逻辑
  @x/shared (apps/x/packages/shared) ← 每个跨 IPC 边界的 Zod schema

  知识库 = ~/.rowboat/knowledge/ 下的 Obsidian-style markdown（无向量库/图DB，唯一事实源）
```

- **Local-first**：工作区与 KB 在 `~/.rowboat/`（或 `$ROWBOAT_WORKDIR`），无 server、无 SaaS 状态（语音/LLM 例外走外部 API）。
- **主力 LLM**：DashScope 上的 `qwen-plus`。Provider 走 Vercel AI SDK（OpenAI/Anthropic/Google/OpenRouter/Ollama 适配器）。
- **核心价值**：让用户觉得 AI 真的"懂他/记得他/敢挑战他"，而非每次从零。

### 仓库结构（monorepo）
| app | 角色 |
|---|---|
| `apps/x/` | **Electron 桌面 app（本文焦点）**，嵌套 pnpm workspace |
| `apps/rowboat/` | Next.js web dashboard |
| `apps/rowboatx/` / `apps/cli/` / `apps/python-sdk/` / `apps/docs/` | 周边 |

`apps/x` 内：`apps/main`（Electron 主进程）、`apps/renderer`（React UI）、`apps/preload`（IPC 桥）、`packages/core`（@x/core 业务逻辑）、`packages/shared`（@x/shared 类型契约）。
**构建依赖序**：shared → core → preload → renderer/main（`npm run deps` 建 shared→core→preload）。

---

## 2. 组件与职责（@x/core）

- `agents/` —— runtime（turn loop）、identity、persona humanizer、L1 card builder、隐式 artifact-card。
- `application/assistant/` —— copilot agent builder、instructions、skills、artifact 收尾。
- `application/lib/` —— builtin tools、exec-tool、bus、message-queue、command-executor。
- `knowledge/` —— KB pipeline（sync / label / build_graph / tag / summarize / agent_notes / live-note）。
- `runs/` —— JSONL repo、lock、abort registry。
- `attention/` —— 主动关注服务（孤立层：**不在 chat runtime 内**，只驱动通知 UI/toast）。
- 支撑：account / analytics / auth / billing / composio / di / mcp / models / observability(Langfuse) / search / slack / voice。

**DI via awilix**（`di/container.ts`）：所有 FS repo（`FSRunsRepo`/`FSAgentsRepo`/…）注册为单例。
**呈现 vs 后台 agent**：`PRESENTATION_AGENTS=['copilot','rowboatx']` 才走 artifact-card/persona humanization/Loona experience/CC persona 自动注入；其他后台 agent（live-note/note_creation/labeling/note_tagging/inline_task/agent_notes）只出原始 markdown/结构化数据。

---

## 3. 数据流：一个 turn 的生命周期

核心是 `streamAgent` 异步生成器（`agents/runtime.ts`，~2174 行单函数）：

1. 渲染层 `window.ipc.invoke('runs:appendMessage')` → main `ipc.ts` 把 `message` 事件追加进 run JSONL，触发 runtime。
2. `AgentRuntime.trigger(runId)` 取 per-run 锁，**重放 JSONL** 进 `AgentState`，调 `streamAgent`。
3. `streamAgent` boots：`loadAgent` → 呈现 agent 走 `buildCopilotAgent`（装配工具集 + 缓存指令）。
4. `buildTools` 按 `isAvailable()` 过滤工具，映射成 AI SDK Tool。
5. 模型在 run-create 时冻结；`resolveProviderConfig` + `createProvider` 实例化。
6. **主循环**：处理 pending tool calls（危险工具发 confirmation 请求 + L1 卡；CC persona 开时对 artifact-card payload 做 persona-humanize；可从 `toCard` mapper 合成隐式 card）→ 计算 turnPhase（normal/bridge/forced-finalization）→ **组装 prompt** → `streamLlm` → 由 deltas 构建 assistant message。
7. 退出：最后一条 assistant 消息纯文本且非 forced-finalization 时返回。

### 事件溯源（核心模式）
每一步（message / tool-invocation / tool-result / llm-stream-event / error / confirmation-request…）追加进 `runs/<runId>/` 的 JSONL；`AgentState.ingest()` 重放日志重建内存态。生成器-with-processEvent 包装：每个 emit 的事件同时 ingest 进本地 AgentState，无需重读盘。

---

## 4. 关键接口协议

### 4.1 Prompt 组装顺序 —— 非对称召回注入（load-bearing）
`runtime.ts:1637-1712` 按精确顺序拼一个 `instructionsWithDateTime` 串。核心两行**自动注入、每 turn 读盘**：
- **行 7 Session Persona**：`loadCcPersonaContext()` 读 `knowledge/Topics/CC Persona/cc-core.md` + `Notes/CC Profile.md`。
- **行 8 Agent Memory**：`loadAgentNotesContext()` 读 `knowledge/Agent Notes/user.md` + `preferences.md`（P20 起带 confidence 过滤）。

**非对称的核心观察**：只有 Session Persona + Agent Memory 自动注入；Knowledge Graph（People/Projects/Topics/Meetings/Notes）、Source Logs（gmail/calendar/fireflies/granola sync）、Session Logs（runs/）**全是工具访问**（`workspace-grep`/`readFile`/`readdir`/`glob`）。召回链在 `instructions.ts:229-239` 明示：Session Persona → Agent Memory → 命名工作上下文（grep knowledge/）→ 实时第三方工具 → Session Logs（仅审计）。

### 4.2 写记忆侧
`save-to-memory` 工具 → 追加一条时间戳 bullet 到 `Agent Notes/inbox.md`；后台 `agent_notes_agent` 蒸馏器把 inbox 提炼进 `user.md`/`preferences.md`（行 8 下 turn 注入的文件）。

### 4.3 KB pipeline 后台服务（各自轮询）
sync_gmail/calendar/fireflies/granola（写 Source Log markdown）· label_emails · build_graph（→ People/Org/Projects/Topics/Meetings）· tag_notes · summarize_meeting · inline_tasks · agent_notes · live-note scheduler · agent-schedule runner · notify_calendar_meetings · **kg_runner**（v1.2 Block B：chat→KG fact 扩散）。

### 4.4 两层评测契约（人性化收束层评测器）
被测对象 = `humanizeLoonaResponse`（`agents/persona-humanizer.ts`）——把 LLM 答案改写得更像人、保 CC persona、**不腐蚀证据**。优先级是**字典序非加权**：`facts > CC style > human-likeness`。

- **Layer A 确定性指标**（纯代码、零方差、无 LLM）：
  - **A1 `evidence_diff`** —— 唯一硬 FAIL 门：original 里受保护 span（commit hash/路径/命令/错误串/config key/版本号…critical 族）必须在 humanized 里逐字存活，否则 FAIL，任何文笔分救不回。
  - A2 `burstiness`（句长方差）、A3 `gptism_density`（双语 AI-slop 标记/1k token）、A4 `structure_signals`（contraction/list/emdash 指纹）——诊断非门控。
- **Layer B LLM judge**（G-Eval 式，temp=0，JSON out）：persona_fidelity(0-5)、human_likeness(0-5)、scene_calibration(0-5)、**humanlike_preference**（pairwise A/B 去位置偏置，**主指标 win-rate**）、overcorrection(0/1)。judge prompt 显式反 blandification（CC 的锋利是 persona 特性，不奖励温柔/客服腔）。
- **Composite 字典序门**（一个 JS 函数，非均值）：`evidence_diff==0`→FAIL；`persona_fidelity<3`→CAPPED（钝化封顶）；overcorrection→OVERCORRECTED；过双门后才由 human_likeness+preference 定分。run-level 主数字 = `winrate_humanized`，配 `fail_rate`+`cap_rate` 三件套一起报。

详见评测器 ADR 文档。

---

## 5. 关键里程碑数字（真实）

- **v1.0** KB Recall Optimization（Phase 1-4，shipped 2026-05-14）。
- **v1.1** Memory Hygiene（Phase 5-10，shipped 2026-05-14，7/8 + 1 partial）。
- **v1.2 Knowledge Compounding**（Phase 11-23，shipped 2026-05-18，**13/13 100%**，**513 测试**，tag `knowledge-compounding-v1.2` @809d350d）：Block A Feishu Ingest（11-15）+ Block B Chat→KG（16-19）+ Block C Memory Intelligence（20-23）三链全 WIRED。
- **评测器 benchmark**：112 条 ground-truth（CSV 导出），fused shuorenhua 后 128 case；判别准确率 qwen-plus 88% / claude-opus-4-7 100%（byScenario，n=83 judge-dependent）；Cohen's κ 0.727。
- **v1.3 记忆回路再连贯化**（Phase 25，设计底稿）：Agent Notes 蒸馏器 + Chat→KG + Feishu，B1-B7 子任务。

---

*架构来源：`.planning/codebase/ARCHITECTURE.md`（2026-05-14）+ `CLAUDE.md` + `evals/humanization/DESIGN.md` + git log/tag。所有数字取自仓库文档原文。*
