# Jarvis (Loona Protocol) · 设计决策记录 (ADR)

> ADR 式关键取舍与教训。每条：背景 → 决策 → 理由 → 后果/教训。
> 来源：`.loona/LOONA-VERIFICATION*.md` + Cortex `HANDOFF.md` + 会话逐字稿。

---

## ADR-1：协议是宪法 —— 以 Loona Agent Interaction Protocol 为唯一对齐基准

- **背景**：Jarvis/Cortex/ToolHub/Bridge 四仓各自演进，字段命名、卡片类型、风险/证据标注各说各话，跨层对不齐。
- **决策**：以 `Loona_Agent_Interaction_Protocol.md`（24 章 / 1273 行）为单一事实源，三仓同开 `loona-protocol-align` 分支做全栈对齐；commit 统一前缀 `[LOONA]`。
- **理由**：分布式系统跨进程契约必须有一个不可协商的字面基准，否则每层"自以为对齐"实际错位。
- **后果**：建立三个跨面不变量（字面契约统一 / 证据·风险全栈贯通 / 危险工具执行边界）；schema 层 209/209 = 100%。schema 行数超预算（120→496），因为"协议字面契约不可压"——用户批扩预算到 1000 行。

## ADR-2：不改 Cortex 产品代码，适配只走"外挂"层

- **背景**：Cortex 是产品代码（AGENTS.md 约束不能改），但前端需要协议帧、卡片、情绪三路。
- **决策**：所有适配只在 **Bridge 监听层 + 前端 + ToolHub 包装层**做。Bridge 从 Cortex 网关帧派生 AGENT_CARD/EMOTION_TAG/DECISION_RECORD，不动 Cortex 内部。
- **理由**：保持产品代码可独立演进；适配层失败不污染大脑。
- **后果**：Bridge 派生策略成为关键复杂点（READ_ONLY_TOOLS 旁路 / WRITE_TOOLS_ARGS_CARD args 卡 / QUESTION confirm 卡）。代价：agent 路径工具结果本不直推前端，必须在 Bridge 监听 TOOL_EVENT 副推——这是"§5🅑 agent 真出卡"的实现形态。

## ADR-3：接线在 ≠ 行为对 —— 从截图法转向链路追踪 + 真行为 QA（核心教训）

- **背景**：R3 用 browse.exe 截图法做 L3 视觉验收。教训：**截图法慢、且测不全交互**——按钮点击→执行、TTS 出声**从未被行为验证**；视觉层卡在 LIVE 渲染天花板（LIVE 没出卡，视觉就看不到，误判为视觉 bug）。
- **决策**：R4 改用**静态链路追踪 link-trace**（`.loona/tests/link_trace.py`）：声明式 51 链 × 209 case 跨两仓，每触发点 = `{id, layer, desc, cands:[(repo,file,regex)]}`，秒级断言代码里接线存在，无浏览器/LLM/截图；再用 browse.exe 对代表触发点做**真行为验证**（fetch 拦截器短路 /api/tts、/api/tool-demo → 零真写）。
- **理由**：分层定位（出 bug 能直接看断在哪一环），快（秒级跑全 209），且 locator 写**诚实断言**——不只看"是否 stash"，而是断言情绪指令真被消费进 `/api/tts` body。
- **后果**：全链覆盖 3628/3628 = 100%，暴露并补齐 **5 处截图法测不到的真断点**：
  1. `L5.emotion_tts` —— 情绪 `voice_instructions` stash 了但 send/speakOne 发的是面板空指令 → 情绪语音永不送达（"语音臂"死端，影响 27 case）。
  2. `L5.tts_filter` —— TTS 零过滤，URL/邮箱/JSON 被原样念出（违 §22.5，影响 34 case）。
  3. `L4.kind:ContactCard` / `DriveCard` —— 不在 `LoonaCardKinds` → 不 stamp `.loona-card.<kind>` → DOM 断言必失。
  4. `L4.render:DriveCard` —— 无 renderer。
- **教训沉淀**：**"接线存在"和"接线会触发正确行为"是两件事**；初版 link-trace 还踩过假阳性（宽正则把 stash 行当命中，收紧为"`instructions:` 赋值的 RHS 引用情绪槽"才正确暴露断线）—— locator 必须写到行为级。

## ADR-4：诚实的分项验收 —— 不让聚合数字掩盖契约真相

- **背景**：L3 VISUAL subset 53.4% < 65% 出口标尺，看似不达标。
- **决策**：把视觉层拆诚实分项 —— halo 端到端 58/58=100%、state-machine inject 36/36=100%、card-render 22/43（受 LIVE 81.6% 渲染天花板制约）。把转瞬的 §20 state-class 选择器移交 visual_state_inject（确定性）；主跑只断言 kind+badge+halo。
- **理由**：card-render 低不是视觉**契约** bug，而是 LIVE 上游没出卡的传导。聚合一个数会误导团队去修没坏的视觉层。
- **后果**：诚实结论是"视觉契约全对（halo+state 双 100%），card-render 受 LIVE 上游制约"，触发 ScheduleWakeup 报根因求 R4 确认，而非假装达标。

## ADR-5：危险写操作要 confirm 卡门控；后续按用户意愿切真实写

- **背景**：send_mail/create_event/update_event/delete_event 是危险写操作。
- **决策（V1）**：危险工具 dry-run（零真实 Google 写）；`delete_event` 走 `dangerous_tool_confirm` → QUESTION+is_confirm → 前端 `mode='confirm'` 可编辑确认卡，用户点 Confirm 才真执行。clarify/confirm 二选一满足§9.3 写前门（两者都"未静默执行写"）。
- **决策（后续，commit `027e5dc`）**：用户主动 opt out dry-run → ToolHub 切**真实 Google 写**。
- **理由**：演示期安全优先（dry-run）；用户确认要真效果后再放开，但 confirm 卡门控保留。
- **后果/教训**：写操作的"安全态"是可配置的产品决策，不是工程默认；文档必须同步真实态（验收旧文档仍写 dry-run，已在 HANDOFF 标注变更）。

## ADR-6：planner nudge 要"窄" —— 无歧义直接执行，有歧义才澄清

- **背景**：R2 决策面 gap —— 写动作要么泛化澄清拖延，要么鲁莽执行。
- **决策**：G1 planner nudge（cortex `9edb027`）——无歧义写动作直接产 tool-call + confirm，不再泛化澄清；歧义输入（"把10点的会改"多候选 / "这条新闻"无指代）仍正确澄清。
- **理由**：澄清是为消歧而非拖延；§5 缺槽先问，但不该把能直接做的事也拖成一轮问答。
- **后果**：C-112 从 1/3 升到 5/5，C-19/051/053/056/072/228（clarify-as-write-gate）从 0/7 升到 7/7；LIVE 72.8%→81.6%（+8.8pp）。

## ADR-7：状态机贴 Cortex 生命周期，废弃旧 coach 模型

- **背景**：Jarvis 原是 Anthropic 直连壳，状态机是旧 coach 的 REMEMBERING/卡片/confirm。
- **决策**：弃 Anthropic，`claudeStream` 改连本地 Bridge `/api/turn`（保 async generator 契约）；状态机重写贴 Cortex 生命周期 **ACK→THINKING→首帧 SPEAKING→SETTLE→DORMANT**（空回复→UNCERTAIN）。
- **理由**：UI 状态必须映射真实大脑生命周期，否则字幕/动效与后端脱节。
- **后果/教训**：`#goal-input` 回车提交改成**文档级委托绑定**（原 IIFE 在元素出现前执行拿到 null，bug 已修——别改回 IIFE）。旧 coach/brain/second-brain 脚本换防崩哑桩，`hasConfig=()=>true`。

---

*ADR 来源：Jarvis `.loona/LOONA-VERIFICATION.md` + `LOONA-VERIFICATION-V2.md` + Cortex `HANDOFF.md` §4.5/§2 + 三仓 git log。*
