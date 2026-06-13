# Jarvis (Loona Protocol) · 架构文档

> 团队可读架构说明。来源：Jarvis 仓库 `.loona/` 验收文档 + Cortex `HANDOFF.md` + 本机会话逐字稿（2026-05-18~22）。
> 一句话定位：Jarvis 是**本地 Cortex 多 Agent 大脑的语音化 UI 壳**，三仓（Cortex / ToolHub / Jarvis）+ Bridge 在 `Loona Agent Interaction Protocol`（24 章 / 1273 行）下做了全栈对齐，并用 209-case 三层真验收 + R3→R4 链路追踪法确认接线。

---

## 1. 系统全景：四仓 + 一桥

```
浏览器 (Jarvis 前端, :7870)
   │  HTTP/SSE: /api/turn · /api/tool-demo · /api/trip-plan · /api/tts
   ▼
Bridge (FastAPI+SSE, :7860)  scripts/web_chat_bridge.py
   │  gRPC/网关帧监听 → 派生 Loona 协议帧 (AGENT_CARD/EMOTION_TAG/DECISION_RECORD)
   ▼
Cortex 多 Agent 大脑 (uvicorn, :8080)  Router→Planner→tool→generation
   │  工具调用
   ▼
ToolHub server (Python, :25003)  10+ 工具：Gmail/Calendar/Drive 真接 Google API + wttr.in 天气 + canned
   │
   └─ 依赖：Postgres 18 (:5432) · Redis 7.4 (:6381)
```

四个代码仓库（均在分支 `loona-protocol-align`）：

| 仓库 | 路径 | 角色 | remote |
|---|---|---|---|
| **Cortex** | `C:/Users/QYL/Downloads/cortex-refactor/cortex/` | 多 Agent 大脑：Router/Planner/generation + 记忆 + Loona 协议域模型 | 无 remote |
| **ToolHub** | `C:/Users/QYL/Desktop/toolhub/` | 工具执行层，ToolResult 信封产出 | `gitea.keyi.lan/pub/emb.data.toolhub.git` |
| **Jarvis** | `C:/Users/QYL/Desktop/Jarvis/` | 前端语音 UI 壳 + 三层验收 harness | 无 remote |
| **Bridge** | （在 Cortex 仓 `scripts/web_chat_bridge.py`） | 网关帧 → 协议帧派生，前端 SSE 出口 | （随 Cortex） |

**架构原则**：Cortex 产品代码不动（AGENTS.md 约束），所有适配只在 Bridge 监听层 / 前端 / ToolHub 包装层做（"外挂"脚本）。

---

## 2. 组件与职责

### 2.1 Cortex（大脑）
- **多 Agent 编排**：Router（意图分类）→ Planner（选工具/出 tool-call/confirm）→ tool 执行 → generation（生成回复）。任务型请求多趟 LLM 串行（~10-15s），闲聊单趟（~5s）。
- **默认模型** `deepseek-v4-flash`（`config/global.yaml`，`think: low` —— 该模型强制 reasoning_effort ≥ low，拒绝 none/minimal），fallback `qwen-plus`。
- **Loona 协议域模型**（`src/domain/loona/` 8 个新文件，本次对齐新增）：
  - `decision_record.py` —— DecisionRecord（§3，6+12 字段，Pydantic Literal 强校验）
  - `card_schemas.py` —— 9~11 种卡片 schema（§18）
  - `emotion.py` —— 6 emotion × 三路（halo/avatar/voice，§17）
  - `safety.py` —— 不可信隔离 + 注入信号检测（§13）
  - `active_state.py` —— ActiveState（§12）
  - `memory_layers.py` —— profile/world/short_term 三层 + 否定记忆（§6）
  - `checklist.py` —— §22 8 项验收 check + aggregator
- **原生记忆**：`cortex_user_memory` 表（uid+speaker 桶存 JSON），`memory_extract` LLM task，每 10 个合格请求触发一次。无通用 KB/RAG。

### 2.2 ToolHub（工具层）
- `catalog.py` 注册工具 schema（source of truth）；`tools/*.py` 分模块实现；`main.py:_dispatch` 路由。
- 工具集：`get_weather`(wttr.in 真) · Gmail（`get_mail_list`/`get_mail_detail`/`send_mail`）· Calendar（`list_events`/`get_event`/`create_event`/`update_event`/`delete_event`）· Drive（`search_drive_files`/`get_drive_file`）· canned（`web_search`/`list_contacts`/`search_contacts`）· 后增 restaurant/travel/meeting_actions 卡背工具。
- 每个工具产出 **ToolResult 信封**（见 §4.2）。凭证在 `server/python/.env`（gitignored）。

### 2.3 Bridge（桥）
- 监听 Cortex 网关帧，派生三类前端 SSE 协议帧。详见 §4.3。
- 自带端点：`/api/turn`（SSE 对话）、`/api/tool-demo`（直连 ToolHub）、`/api/trip-plan`（服务端直调 deepseek 出严格 JSON 行程卡）、`/api/tts`、`/api/traces`（R1 加的 TaskTrace 回放）。

### 2.4 Jarvis 前端（壳）
- `claudeStream`（async generator，连 `/api/turn`，已弃 Anthropic 直连）。
- `proceedWithText` 状态机，贴 Cortex 生命周期：**ACK → THINKING → 首帧 SPEAKING → SETTLE → DORMANT**（空回复 → UNCERTAIN）。
- `JarvisTTS`（浏览器 speechSynthesis，保 connected/connect/send/flush/interrupt/onEnd 接口）。
- `routeUserText` 统一入口：weather → trip → chat 粗筛路由。
- 卡片渲染器：11 种 kind（含后补的 ContactCard/DriveCard）+ `augmentLastAgentCard` 统一补 `.loona-card.<Kind>` 类 + risk/evidence/source/untrusted 徽章。

---

## 3. 数据流：一个 turn 的生命周期

1. 用户在前端输入（文字或语音）→ `routeUserText` 粗筛 → `claudeStream` POST `/api/turn`。
2. Bridge 转发到 Cortex；Cortex Router 分类 → Planner 选工具 → ToolHub 执行（产出 ToolResult 信封）→ generation。
3. Bridge 监听网关帧，按 §4.3 规则派生协议帧流式回推前端。
4. 前端 `claudeStream` 分发：`delta`→字幕+TTS切句；`EMOTION_TAG`→orb halo+TTS情绪指令；`AGENT_CARD`→对应 renderer；`DECISION_RECORD`→（落盘已在后端）。
5. 状态机推进；TTS 按标点切句朗读（§22.5 过滤 URL/邮箱/JSON）；危险写操作出 confirm 卡，用户点 Confirm 才真执行。

**Turn-end 判定（Bridge 关键修复）**：`is_req_end == 1` ONLY（不再 `is_last || is_req_end`）—— 工具任务里"正在为您查询..."NOTICE 也是 `is_last=1` 但 `is_req_end=0`，旧逻辑会提前 break 吞掉最终回复。

---

## 4. 关键接口协议

### 4.1 DecisionRecord（§3 / §22 —— 决策记录契约）
每个 turn 产出一条 DecisionRecord，Pydantic 校验（Literal 枚举强校验），落盘 `logs/decision_records.jsonl`，并以 `DECISION_RECORD` 帧推前端。核心字段族：
- `request_type`（§16，9 种 Literal：chat/emotion/query/...）
- `intent_structure` / `continuity`（§4）
- `required_slots` / `missing_required_slots` / `strong_impact_slots` / `default_assumptions`（§5 缺槽先问）
- `output_mode`（§8，6 枚举：voice/voice_card/...）+ granularity
- `action_risk`（§9.1，R0-R4）+ ConfirmationCard + emotion_priority
- `evidence_level`（§10，E0-E5）+ tool_plan
- `failure_state` + `final_next_step`（§14）

**§22 8 项验收 checklist**（`checklist.py` 8 独立 check + aggregator）：主需求 / 信息 / 记忆 / 证据 / 输出 / 行动 / 失败 / 连续。

### 4.2 ToolResult envelope（§10 + §9.1 —— 工具结果信封）
ToolHub 14 工具全部 `ToolResult.to_dict()`，全栈贯通字段：
- `ok` / `result` / `error`（`_ERR_RULES` 5 类错误分类，**无 repr(e)/类型名/traceback**，§14.3）
- `evidence_level`（E0-E3）、`risk`（R0-R4）、`source`（ToolSource）
- `untrusted_fields`（§13.2 —— 如 `get_mail_detail` 标 `['body_text','subject','snippet']` 最大 PI 面）

### 4.3 SSE 帧序（Bridge 派生策略）
Bridge `_listener.on_response` 三个派生分支 + NOTICE 补卡：

| 触发帧 | 条件 | 推什么 |
|---|---|---|
| `TOOL_EVENT` | tool ∈ READ_ONLY_TOOLS | 旁路调 ToolHub 拿结构化结果推 ready 卡（每个 read 工具一卡，幂等无副作用） |
| `TOOL_EVENT` | tool ∈ WRITE_TOOLS_ARGS_CARD | 用 args 当 result 推 `status='requested'` 卡（不旁路，避免重复写） |
| `QUESTION` | `is_confirm == 1` | 推 `mode='confirm'` 卡（危险工具执行前可编辑确认） |

实测帧序（`live_turn_probe.py` 真打 `/api/turn`）：
- `[chat] 你好` → delta×3 + EMOTION_TAG + DECISION_RECORD（5 帧）
- `[emotion] 我急死了` → delta×5 + EMOTION_TAG + DECISION_RECORD（7 帧，emo 正确识别 request_type=emotion）
- `[query] 今天上海天气` → delta×2 + EMOTION_TAG + AGENT_CARD + DECISION_RECORD（5 帧，AGENT_CARD 15 字段全到位）

### 4.4 三个跨面不变量（已验证）
1. **字面契约统一**：Bridge `LOONA_FRAMES` ↔ Cortex Literal 枚举 ↔ 前端 `LoonaCardKinds` ↔ ToolHub `DEFAULT_RISK` 用同一字符串集。
2. **证据/风险全栈贯通**：ToolHub `ToolResult` → Cortex `DecisionRecord.evidence_level/action_risk` → Bridge `AGENT_CARD` → 前端 `.risk-badge/.evidence-badge`。
3. **危险工具执行边界**：见 HANDOFF/红线文档（注：截至 commit `027e5dc`，ToolHub 已按用户指令切到 **真实 Google 写**，早期 dry-run 状态已改）。

---

## 5. 验收架构（209 case 三层 + R3→R4）

三层真验收（标尺：≥95% overall + 视觉层 ≥90% + 红线案例 100%）：
- **L1 Schema**（§3+§22+§10+§9.1）：209/209 = 100%。每 case 跑 DecisionRecord Pydantic + 卡 schema + ToolResult + §22 8 项 + emotion + 注入检测。
- **L2 LIVE SSE**（§18+§17+§15）：102/125 = 81.6%（R3）。真打 `/api/turn` 桥端校验帧序。
- **L3 VISUAL DOM/halo**（§17+§18+§20）：browse.exe 真打开 `:7861` 真渲染真截图；halo 58/58=100%、state-inject 36/36=100%、card-render 受 LIVE 渲染天花板制约 51.2%。

**R4 链路追踪法（link-trace）**：R3 教训是截图法慢且测不全交互（按钮点击→执行、TTS 出声从未行为验证）。R4 改用 `.loona/tests/link_trace.py`：声明式 51 链 × 209 case，跨 Cortex+Jarvis 两仓，每个触发点 = `{id, layer, desc, cands:[(repo,file,regex)]}`，秒级静态断言代码里接线存在（无浏览器/LLM/截图）。结果：全链覆盖 **3628/3628 = 100%**，暴露并补齐 **5 处截图法测不到的真断点**（情绪语音指令断线、§22.5 TTS 未过滤、Contact/DriveCard kind 缺失/无渲染器），4 个代表触发点经 browse.exe 真打验证通过。详见验收/ADR 文档。

---

*架构来源：`.loona/LOONA-VERIFICATION.md`(V1) + `LOONA-VERIFICATION-V2.md` + Cortex `HANDOFF.md` + 会话逐字稿。所有数字均取自验收报告原文。*
