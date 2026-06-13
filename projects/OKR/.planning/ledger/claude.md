# Claude 本机 Session 证据账本（Q2 时间戳化）

> 采集源：`C:\Users\QYL\.claude\projects`（54 个项目目录）
> 采集窗口：2026-04-01 ~ 2026-05-24（重点 4/13 起）
> 采集方法：按 mtime 筛 Q2 内 jsonl（排除 subagents/），逐会话提取首条用户意图 + 末尾关键产出（UTF-8 安全）。只读。
> 采集时间：2026-05-24

## 统计概览

- **Q2 内 jsonl 会话**：146 个（已排除 subagents 子目录）。其中约 30 个为打招呼/login-403/空文件等噪声，已合并或剔除；有意义会话约 110 个。
- **总字节量**：约 200 MB，最大单会话 19.5 MB（Loona-Knowledge-System spec 整理）、8.5 MB（rowboat 评测器扩充）、8.2 MB（Jarvis ToolHub 接入）。
- **按项目活跃度（会话数 / 字节）**：
  - `Jarvis`（含 4 个 worktree）：约 46 会话 / 73 MB —— **最活跃**，Loona Protocol agent 工程（Cortex/Bridge/ToolHub/前端 + 209 case 真验收）
  - `rowboat`（含约 30 个 worktree）：约 58 会话 / 88 MB —— 人性化收束层评测器 + 记忆回路 v1.3（GSD 流程）+ KB Lab + Loona 四层 UI/TTS
  - `Loona-Deskmate` 系列（G 盘 + C--Users-QYL 镜像）：约 16 会话 —— PRD 审查（手机端应用管理 / 530 三线 MVP / 记忆管理 / Slack case）
  - `9-----konw-how` / `Loona-Knowledge-System`：3 会话 —— Loona-Spec 四层架构整理
  - `OKR`：3 会话 —— 飞书 OKR skill（本任务）
  - `agent`：3 会话 —— nanobot / selfevo_agent 分析
  - 其余为环境配置（CLIProxyAPI / DashScope TTS / n8n / 飞书 CLI 联通）、个人画像/周报、case 表审查等。

## 周次定义

W0=4/13 前 · W1=04-13~19 · W2=04-20~26 · W3=04-27~05-03 · W4=05-04~10 · W5=05-11~17 · W6=05-18~24

## 时间戳账本（按日期升序）

| 日期(mtime) | 周 | 项目 | 会话主题/意图 | 关键产出 | 候选KR |
|---|---|---|---|---|---|
| 2026-04-25 | W2 | Loona-Deskmate (+C--Users-QYL 镜像) | 多轮只读审核「手机端应用管理/插件管理」PRD 初稿（含 3 张原型图） | 模板符合度核对 + P0~P3 分级审核结论：本期范围模糊、Slack 能力缺研发背书、Agent 任务恢复路径未闭环、命名自相矛盾；建议先修一轮 P0 再进研发评审 | O1-KR2, O2-KR2 |
| 2026-04-25 | W2 | Loona-Deskmate | PRD「瘦身与图表化」后多轮复核（Mermaid 状态图/页面总表/竞品调研下沉附录） | 逐项核对上轮建议已闭环，无 P0/P1，确认可进正式 PRD 评审；指出原型图分组命名等 P2 一致性问题 | O1-KR2, O2-KR2, O2-KR4 |
| 2026-04-25 | W2 | AI-workshop | 搭 Cloudflare tunnel + cloudflared 内网穿透；修 cliproxyapi 502（codex-auto-review 别名）+ Codex Desktop sandbox 写回问题 | cloudflared 装好；审查器 502 已修，sandbox 写回定位到 Desktop 本体 | （环境/工具，弱相关） |
| 2026-04-26 | W2 | Codex-430-release-prd | 审阅 Loona 430 版本 PRD V0.2（工作流/记忆/对话/UI/声纹）对齐性 | 八关注点逐项核查：流程只画 happy path、缺边界态（打断/超时/声纹居中/多人）、会话生命周期不清；建议补异常态流程图 | O4-KR1, O2-KR2 |
| 2026-05-05 | W3 | Loona-Deskmate | 审查 + 最终复查 530 三线 MVP 需求包（文档空间/知识库/记忆 5 份 PRD + Backlog） | 「有条件通过」：记忆对象自相矛盾(致命)、跨端同步规则全缺、上下文生命周期、可验收性需补；二轮复查采纳记录 | O1-KR2, O2-KR2, O4-KR3 |
| 2026-05-06 | W4 | Loona-Deskmate | 430 记忆管理 PRD（Profile/短期/长期三层）讨论；桌面文件盘点 | 记忆三层方案规则梳理（生成/来源/冲突/清空/换机场景） | O1-KR2, O2-KR2 |
| 2026-05-07 | W4 | Loona-Deskmate (+C--Users-QYL) | 产品验收评审：Slack 消息管理场景 case 6.1-6.23 能否用 user token 工具实现 | 逐 case 可行性评估表（list/send/thread/search 工具映射），指出消歧走 list_users、确认预览归 Gateway | O2-KR3, O4-KR1, O4-KR4 |
| 2026-05-07 | W4 | C--Users-QYL / notebooklm | agent 个性化风格快速迭代约束探索（痛点：只能加 few-shot 太慢）；逐字稿 + Slack PRD 优化 | 提出 Actor/Judge/Optimizer 三角色分离的最小可信进化闭环设计；Slack PRD user token 口径改写 | O3-KR1, O3-KR2, O2-KR1 |
| 2026-05-07~08 | W4 | agent | 分析 nanobot / selfevo_agent 仓库（含 bridge/webui/case/tests） | 摸清 nanobot 工程结构与依赖关系（最终命中 Bedrock 502） | O1-KR1 |
| 2026-05-10 | W4 | cli-proxy-api / agent | 系统排查修复本机 CLIProxyAPI（Tailscale 远程调用失败）；tavern-card skill 评估 | 定位调用链问题；拒绝执行绕过审查的成人内容 skill | （环境/工具） |
| 2026-05-13 | W5 | rowboat (+relaxed-swanson) | 分析 Loona 四层 UI/TTS 集成 + agent 编排 UI；DashScope WS 实时 TTS 接入 | 关键 insight：Loona 是 Copilot 的「语音化输出适配器」非新 agent，未动编排层；DashScope dashscope.ts 接入（WS 协议） | O2-KR3, O3-KR1 |
| 2026-05-13 | W5 | rowboat (多会话) | artifact-card 自动渲染 gap 排查；sidebar 读 4877 run 文件性能问题；auto mode/GSD 落点盘点 | 定位强制走 artifact-card 的触发缺口；4877 run 仅 39 copilot（99.2% 浪费）；GSD = 81 skills+33 agents+11 hooks | O2-KR3, O3-KR1 |
| 2026-05-13 | W5 | C--Users-QYL | DashScope Qwen3-TTS 实时接口实测 + 写成可交付任务规格；飞书 MCP 接入指引 | 产出「阿里云 DashScope 实时 TTS 调用」实测任务规格（端点/协议/字段/坑全写死） | （工具/赋能） |
| 2026-05-14 | W5 | rowboat (naughty-nobel) | 结合项目填「第一周结果汇总」表（性格/说人话/交互/记忆方向） | CC Persona「毒舌技术搭档」人格运行系统成果归纳（7 子系统 + 独立 humanizer 收束）；产出可交付表行 | O3-KR2, O1-KR3 |
| 2026-05-14 | W5 | rowboat (+多 worktree) | 性格/人性化内容分析；接入 Google Maps/Gmail/Calendar 排查；clawd-on-desk 桌宠接 attention | cc-persona 推到 GitHub（5 commit）；Maps 推迟 v1.3 并存 memory；clawd 接 attention/service 事件映射 | O3-KR1, O3-KR2, O2-KR3 |
| 2026-05-14 | W5 | C--Users-QYL | 飞书 CLI 能完成哪些任务盘点；本地数据源可挖性验证 | 列出本地真实数据源（Claude/Codex session、git、PowerShell 历史、OMC notepad）作为产出面挖掘 | O2-KR1 |
| 2026-05-14 | W5 | rowboat (beautiful-panini) | 人性化收束层评测器：能独立交付的产物盘点（langfuse skill 上下文） | 列出 60 条 seed dataset / 20 golden / L1 程序化检查 / L2L3 prompt / 校准脚本 等可交付物清单 | O3-KR1, O3-KR2, O2-KR3 |
| 2026-05-14 | W5 | rowboat (charming-aryabhata) | GSD 自治执行 v1.2「Knowledge Compounding」里程碑，单会话单 phase 节奏；rowboat 项目顿悟（放弃 TTS/loona 长线、转 MVP 快验证） | Phase 11/12 交付（飞书 Calendar Ingest，253 测试，8 项审查全修）；确立单 phase/session 节奏 | O2-KR3, O4-KR3 |
| 2026-05-14 | W5 | Loona-Deskmate-2-Agent | 飞书 CLI 联通确认 + 个人 5 月中旬观察报告 | 读月报/周报/日报/日历产出「秦宇龙观察报告」（数据来源透明化 + 5 条 insight + 能力边界） | O1-KR3 |
| 2026-05-15 | W5 | rowboat (charming-aryabhata) | GSD 自治继续：v1.2 飞书接入 Block A（Calendar/Base/Sync） | Phase 13 Feishu Base Ingest（~1.06M token）、Phase 15 Sync Orchestration + Health UI（19 commit）shipped | O2-KR3, O4-KR3 |
| 2026-05-15 | W5 | rowboat (+worktrees) | 飞书新建会议（卡 vc:reserve scope）；接入 Google Map（推迟 v1.3） | 定位 OAuth app 未启用 vc:reserve scope；Maps 路由 v1.3 并记录 recipe | O2-KR3 |
| 2026-05-15 | W5 | G--------------------- | 周报不够专业，结合飞书文档/聊天/会议重写 | 产出给周报 agent 的处理说明 + 内容包：主线只有 Agent 决策小组 Web Coding workshop，禁用无证据表述 | O1-KR3, O2-KR4 |
| 2026-05-16 | W5 | rowboat (charming-aryabhata) | GSD 自治：v1.2 Block B（Chat→KG）Phase 14 | Phase 14 shipped（8 commit，326 测试绿）；单 phase 节奏多次确认 | O2-KR3, O4-KR3 |
| 2026-05-17 | W5 | rowboat (+多会话) | GSD 自治 v1.2 Phase 16-19（Chat→KG 抽取/路由/runner）；项目演进轴总结 | Phase 17 fact→note 路由（395 测试）、Phase 18、Phase 19 Chat→KG runner（Block B 闭环，9/13）；总结 v1.0→v1.2 演进 | O2-KR3, O3-KR2, O4-KR3 |
| 2026-05-17 | W5 | Jarvis | 安装 N8N + N8N MCP；飞书机器人能力/scope 排查 | 区分「应用能力」vs「权限 scope」：bot 能力没开(11205) + scope 加了没发布；n8n 装好 | O2-KR3, （工具） |
| 2026-05-17 | W5 | rowboat (relaxed-leavitt / interesting-chandrasekhar) | 把大模型调用转 n8n 工作流可行性；项目逐 phase 改动实证 | 两层稳定性分析（n8n 只解决编排层，KG 抽取/建图的模型不稳它碰不到）；v1.0→v1.2 git 实证 | O2-KR3 |
| 2026-05-18 | W6 | rowboat (多会话) | GSD 自治 v1.2 Block C 记忆智能 Phase 20-23 收尾 + v1.2 milestone 收尾 | Phase 20 Recency+Decay / 21 Similarity Retrieval / 22 Archived Prefs / 23 冲突检测 lint 全 shipped（513 测试）；v1.2 13/13 完成；Phase 24 移出 v1.2 | O2-KR3, O3-KR2, O4-KR3 |
| 2026-05-18 | W6 | rowboat (inspiring-curran) | GSD complete-milestone：v1.2 Knowledge Compounding 归档打 tag | milestone 归档 + tag `knowledge-compounding-v1.2` @809d350d；21 open 项（8 UAT+13 verification）记 Deferred | O2-KR4, O4-KR2 |
| 2026-05-18 | W6 | rowboat (heuristic-gould) | 为人性化收束层做 benchmark + 评测标准（之前接 langfuse 研究过） | 找回已收束的两层评测设计（确定性指标 + LLM judge），打包给新会话的自包含 prompt | O3-KR1, O3-KR2, O4-KR4 |
| 2026-05-18 | W6 | rowboat (dreamy-turing) | 检查项目进度 | 里程碑总览：v1.0/v1.1 已发布、v1.2 代码 13/13 但 live UAT 发现真实缺陷不可关闭 | O2-KR4 |
| 2026-05-18 | W6 | rowboat / C--Users-QYL | 分析 Tencent DB-Agent-Memory 仓库；记忆 recency/archive G3G4 真实验证 | 解析 confidence token 语法（last_seen 重算、>70天<0.3 丢弃、<=0.2 归档）；设计 G3/G4 真机验证步骤 | O3-KR1, O2-KR3 |
| 2026-05-18 | W6 | G--------------------- | 检查飞书 CLI 联通；DashScope key TTS 403 排查 | 证明所给 key 在全部 TTS 路径 403（ASR/LLM 通）= 该 key 无 TTS 授权；拒绝从别会话扒 key | （工具/赋能） |
| 2026-05-18 | W6 | Loona-Deskmate--------- | 评审「agent 测试群」进度 + 刘雪峰 4 条评测 bad-case（174 用例/202 Router/433 Planner） | 核心判断：4 条不是模型 bug 是 1 个评测方法问题（精确匹配产生假阴性）；尺子要按字段分层，验收标准是产品定义权 | O4-KR4, O4-KR1, O3-KR1 |
| 2026-05-18 | W6 | rowboat (46ded776 / sweet-mayer) | KB Lab 项目启动 + Cortex 仓库接入起点 | KB Lab 双进程启动（Web 47184/API 47183），可并排 A/B 测模型×KB×记忆×人格；Cortex HANDOFF 文档 + 三工作流 brief | O2-KR3, O3-KR1 |
| 2026-05-18 | W6 | Jarvis | GSD Jarvis LifeOS 项目：Phase 1-3 规划/讨论/执行（第二大脑 + 教练引擎） | Phase 1 认知内核（second-brain/brain/coach.js 离线确定性）交付 4/4；Phase 2/3 discuss+plan（确认/持久化/回顾环） | O2-KR3, O2-KR2 |
| 2026-05-18 | W6 | C--Users-QYL | CLI 能否用 + OKR 反推映射 | 产出 `OKR反推映射表.md`（15 条 KR 反推里程碑→逐条证据→覆盖率%）；反推出硬缺口（Agent 问题分析文档已超期等） | O2-KR4, O3-KR1 |
| 2026-05-19 | W6 | rowboat (gallant-cori) | 核对飞书 sheets 测试集标注（Agent-Case CSV）逻辑对错 | 逐用例实测：行内收件人域名矛盾(008/012/018/023)、判定规则指向 API 不存在工具(6 条) | O4-KR4, O4-KR1 |
| 2026-05-19 | W6 | rowboat (magical-shirley / kind-villani / elegant-neumann) | KB Lab 更新评估；项目进度复查；记忆回路 v1.3 GSD 正规化启动 | KB Lab 定位为「知识/记忆护城河基准台」介绍；本地 local-first 存储分层盘点；v1.3 记忆回路（Agent Notes 蒸馏+Chat→KG+Feishu）起步 | O2-KR3, O3-KR2, O4-KR3 |
| 2026-05-19 | W6 | rowboat (quizzical-buck ×2) | 人性化收束层评测器全量构建 + shuorenhua 语料并入 + Langfuse 真 trace 跑通 | evidence_diff 等确定性指标 + L2/L3 judge；shuorenhua 66 条按原样用（SF→slop_recall、SNF→误杀门）；results.jsonl 868→251 清理 | O3-KR1, O3-KR2, O4-KR4, O2-KR3 |
| 2026-05-19 | W6 | rowboat (hungry-darwin) | 安装 karpathy skills；连带清理全局 CLAUDE.md OMC 残留 | CLAUDE.md 87→38 行，OMC 可逆移走，修掉指向不存在 agent 的失效编排指令 | （工具/环境） |
| 2026-05-19 | W6 | rowboat (epic-williams / intelligent-dubinsky) | 个人 360 画像；飞书 CLI 联通 + OKR 逐周反推应然计划 | 360 画像（多视角：自我/上级杨健勃/同事）；以每个 KR 的 DDL 回推逐周应然工作内容（W1-W15） | O1-KR3, O2-KR4 |
| 2026-05-20 | W6 | Jarvis (+多 worktree) | Jarvis 可视化 Demo（orb/今日简报）；Cortex HANDOFF 三工作流（TTS/场景卡片/记忆KB）；前端 UI 优化 | 今日简报图文编排（orb 上浮+错峰生长 4 卡 + mock TTS 同步）；qwen3-tts instruct 参数实测；记忆面板；PTT 语音输入 | O2-KR3, O3-KR1 |
| 2026-05-20 | W6 | Jarvis / Downloads | 检查 agent 模块场景 case CSV（49 条/具体 Case 库）字段问题 | 按严重度列出：Case_001 XXX 占位符、空闲时段前后不一致等硬伤；Cortex 提示词体系梳理（3层+1旁路+1外挂） | O4-KR4, O4-KR1 |
| 2026-05-20 | W6 | rowboat (sweet-mayer) | 访问 Cortex gitea 仓库 + 整理交付 | HANDOFF.md 主文档（6 服务/端口/重启 runbook/约束/全 diff）+ 三工作流分头 brief | O2-KR3, O1-KR1 |
| 2026-05-21 | W6 | Jarvis (多会话, 跨 3 项目整理) | Jarvis×Cortex×ToolHub 大改动后整理（归档/文档/git 判断/未决项）；ToolHub 拉取联通 | TTS 真同步修复（onStart 回调+预热缓存）；旅游规划 lifecycle 8 阶段重构；ToolHub 接飞书工具方案 A（lark-oapi SDK）；5/20 Cortex 深度问题报告（task 失败 6.25%） | O2-KR3, O3-KR1, O4-KR4 |
| 2026-05-21 | W6 | Jarvis | 全栈对齐 Loona Agent Interaction Protocol（24章/6原则/9卡/40+Case/8验收）；DashScope key 真权限实测 | Jarvis×Cortex×ToolHub×Bridge 全量诊断重构（loona-protocol-align 分支）；8 个可用 Chat 模型延迟实测表 | O4-KR4, O2-KR3, O3-KR2 |
| 2026-05-22 | W6 | Jarvis (多会话, /goal harness 自迭代) | Loona Protocol 全链路场景真验收 · Harness 自迭代（三层全 PASS 标尺：后端 DecisionRecord §3+§22 8/8 + ToolHub + 前端卡片/TTS） | R4 链路追踪行为 QA：schema 209/209、LIVE 102/125(81.6%)、state-inject 36/36、halo ~98%；修 7 个 live bug（卡乱码/loona-card 类/TTS 标点/双重朗读等）；loona-workbench v1 地基 | O4-KR4, O2-KR3, O4-KR1 |
| 2026-05-22 | W6 | 9-----konw-how / Loona-Knowledge-System | 深度分析 md 整理 Loona-Spec 四层架构（总协议/场景 know-how/跨场景注册表/Eval Case Pack） | 四层 spec 整理（RFC2119 MUST/SHOULD/MAY 223 条 + 9 卡 schema + golden cases）；定性为 behavioral conformance spec（类比 WCAG）；交互链路审 9 case | O3-KR2, O3-KR3, O4-KR4, O2-KR3 |
| 2026-05-22 | W6 | OKR | 飞书 OKR skill 构建（lark-cli backbone，get_open_id/auth status 调试） | 调试 OKR skill 的 open_id 解析与 auth status subprocess 返回 | O2-KR3 (本任务) |
| 2026-05-24 | W6 | OKR | 周报：结合飞书 CLI 收集本周成果 + 参考本地 claude session（本采集任务的母会话） | 派发 4 个采集 subagent 各扫一源写账本（含本账本） | O2-KR4, O1-KR3 |

## 按项目归纳

### Jarvis（Loona Protocol agent 工程 · 最核心 · 强映射 O4-KR4）
W5 末起爆发，W6（5/20-5/22）为最高峰。从「Jarvis 可视化 Demo（orb + 今日简报）」起步，接 Cortex 后端 + ToolHub + Bridge，按 **Loona Agent Interaction Protocol（24 章/6 原则/9 卡/40+Case/8 验收 checklist）** 做全栈对齐重构，最终用 **harness 自迭代** 跑 **209/209 schema + 125 LIVE case（81.6% 三票通过）真验收**，并修一批 live bug。这是 **O4-KR4「6/30 验收标准 + 关键 Case」+ O2-KR3「推动实现/跑通/落地」** 的最强证据，同时沉淀方法（O3-KR2）。配套：DashScope TTS 接入、ToolHub 接飞书工具、Cortex 提示词体系/深度问题报告（O3-KR1）。

### rowboat（人性化收束层评测器 + 记忆回路 + KB Lab · 强映射 O3-KR1/KR2 + O4-KR4）
两条主线并行整个 W5-W6：
1. **GSD 自治工程**：v1.2「Knowledge Compounding」13 phase 全 shipped（飞书接入 Block A + Chat→KG Block B + 记忆智能 Block C，513 测试，已打 tag），随后启动 v1.3 记忆回路。单 phase/session 节奏（O2-KR3 闭环 + O4-KR3）。
2. **人性化收束层评测器 + benchmark**：两层评测（确定性指标 + LLM judge），用 Langfuse 真 trace 跑通，并入 shuorenhua 语料，强映射 **O3-KR1（体验/问题分析）+ O3-KR2（产品化方法沉淀：评估维度）+ O4-KR4（关键 case）**。
3. **KB Lab**：知识/记忆护城河基准台，可并排 A/B 测模型×KB×记忆×人格。
4. CC Persona 人格系统（O3-KR2）、Loona 四层 UI/TTS、clawd 桌宠 attention。

### Loona-Deskmate 系列（PRD 审查 · 强映射 O1-KR2 + O2-KR2 + O4-KR1/KR3）
W2-W4 主要承接**非 Agent 小模块的 PRD 审查/迭代**：手机端应用管理/插件管理 PRD（多轮瘦身图表化至可评审）、530 三线 MVP 需求包（文档空间/知识库/记忆）、430 记忆管理 PRD、Slack 消息管理场景 case 可行性评审。映射 **O1-KR2（承接非 Agent 小模块需求）+ O2-KR2（需求拆解→方案→协作）+ O4-KR1/KR3（版本需求与测试集）**。后期（5/18）评审 Agent 测试集 bad-case，点出「评测尺子按字段分层、验收标准是产品定义权」（O4-KR4 + O3-KR1）。

### Loona-Knowledge-System / 9-konw-how（Loona-Spec 四层架构 · 映射 O3-KR2/KR3）
W6（5/22）把零散 md 整理成四层 spec（总协议 + 场景 know-how + 跨场景注册表 + Eval Case Pack），定性为 behavioral conformance spec。这是 **Agent 产品化方法沉淀（O3-KR2）** 和**中长期方向（O3-KR3）** 的结构化产物，并直接喂给 Jarvis 的 Protocol 对齐验收。

### OKR（飞书 OKR skill · 本任务）
W6（5/22-5/24）构建飞书 OKR skill（lark-cli backbone），调试 open_id 解析；5/24 母会话派发本采集任务。

### 其余（环境/工具/赋能 · 弱相关）
CLIProxyAPI 修复、DashScope TTS 实测、n8n + MCP 安装、飞书 CLI 联通排查、karpathy skill 安装 + OMC 清理、个人 360 画像 / OKR 反推映射表 / 周报。其中「OKR 反推映射表」「逐周应然计划」「个人观察报告」直接服务复盘与对齐（O2-KR4 / O1-KR3）。

## 与 KR 强相关结论（本地工程视角）

- **O4-KR4（验收标准 + 关键 Case）**：Jarvis 209 case schema 真验收 + 125 LIVE case + rowboat 评测器 —— **最强、最密集证据**（W6）。
- **O2-KR3（推动实现/跑通/落地）**：贯穿全 Q2 主力，rowboat v1.2 13 phase shipped、Jarvis 全链路跑通、KB Lab 启动、DashScope/ToolHub 接入。
- **O3-KR1（Agent 体验/问题分析）**：Cortex 5/20 深度问题报告、评测集 bad-case 方法分析、人性化收束层问题诊断。
- **O3-KR2（产品化方法沉淀）**：人性化评测维度、Loona-Spec 四层 conformance spec、CC Persona、评估器设计 —— W5-W6 集中沉淀。
- **O1-KR2 + O2-KR2（非 Agent 模块需求 + 拆解协作闭环）**：Loona-Deskmate 系列 PRD 审查（W2-W4）。
- **O4-KR1/KR3（版本需求 + 测试集）**：430/530 PRD、Agent 测试集标注审查、case 库字段核对。
- **O2-KR4（复盘）**：v1.2 milestone 归档、OKR 反推映射表、周报与观察报告。
