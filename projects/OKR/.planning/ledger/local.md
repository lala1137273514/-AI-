# 本机工作文档证据账本（Q2 时间戳化）

> 采集源：`G:\其他计算机\我的计算机\工作\可以科技`
> 采集窗口：2026-04-01 ~ 2026-05-24（重点 4/13 起）
> 采集方法：PowerShell `Get-ChildItem -Recurse` 按 mtime 筛 Q2 内文档（.md/.txt/.docx/.xlsx/.pptx/.pdf/.csv/.json）。文本读开头提炼一句话成果；二进制按文件名+目录语义+mtime 推断交付物。只读，未修改/移动/删除任何文件。
> 采集时间：2026-05-24

## 统计概览

- **全盘 Q2 内文件**：67,621 个 —— 其中 `AI workshop`（46,031）与 `loona-voice-demo`（17,690）绝大多数是 **三方代码仓 / 依赖树 / 编译产物**（ten-framework、node_modules、site-packages、.py/.c/.h 等），**非工作文档**，已剔除。
- **文档候选（过滤代码/依赖/缓存/图片后）**：395 个；再剔除 `graphify-out\cache\*`（约 90 个哈希缓存 json）、`.omc/.omx/.codex/.gemini` 会话与状态 json、demo case json、wiki-project 的 external/karpathy 模板、package/tsconfig 等工具噪声后，**真实交付文档约 100 篇**。
- **文档高度集中在 `Loona Deskmate`**（283 候选 / 真交付主力），其次 `AI workshop`（少量顶层 case 文档 + .planning + demo 需求/设计文档）、`docs/plans/Week1`（入职第一周认知产出）、`openspec`、`会议`、`loona-voice-demo`。
- **本机产出活跃周**：W0(早期)~W2 最密集（PRD/评测体系/4.14 与 430 需求/Wiki 化），W3~W4 转入 530 三线 MVP 与 Slack case，W6 出 Agent-UI/状态反馈范式 + 最新评测集聚合。**W1、W4 中段本机文档相对稀疏**（工程产出更多落在 C 盘 session，见 session 账本）。

## 周次定义

W0=4/13 前 · W1=04-13~19 · W2=04-20~26 · W3=04-27~05-03 · W4=05-04~10 · W5=05-11~17 · W6=05-18~24

## 时间戳账本（按 mtime 升序）

| 日期(mtime) | 周 | 文件/目录 | 类型 | 一句话用途/成果 | 路径 | 候选KR |
|---|---|---|---|---|---|---|
| 2026-04-01 | W0 | 决策机｜服务器通讯架构梳理 | 会议md | 梳理任务执行逻辑不清/任务链切换死板等 4 个系统关键问题 | 会议\决策机｜服务器通讯架构梳理\ | O1-KR1 |
| 2026-04-01 | W0 | docs/plans/Week1 入职六步产出（产品总图/模块地图/主链路/Agent中枢/版本边界/产品判断） | 认知md×6 | 入职第一周系统化吃透产品线/架构/Agent中枢/版本边界，形成自己的产品判断 | docs\plans\Week1\ | O1-KR1 |
| 2026-04-01 | W0 | LoonaDeskmate-新人深水区黑话表 | 认知md | 整理产品/工程黑话术语，加速认知对齐 | docs\plans\Week1\ | O1-KR1 |
| 2026-04-02 | W0 | 总-情感交互架构1.0-2.0 | 架构md+图 | 梳理 V1/V2 情感交互基本逻辑、感知/决策架构（含 11 张架构图） | Loona Deskmate\总-情感交互架构1.0-2.0\ | O1-KR1 |
| 2026-04-02 | W0 | 飞书工作复盘 Agent PRD v2 | PRD md | 定义把飞书工作过程转结构化复盘文档的个人沉淀 Agent | docs\2026-04-02-feishu-work-retrospective-agent-prd-v2.md | O2-KR1, O2-KR2 |
| 2026-04-02 | W0 | weather-task-bubble MVP（3 版） | 需求md×3 | 主任务思考态与关键词气泡（天气场景 MVP）正式需求 | openspec\changes\ | O2-KR1, O2-KR2 |
| 2026-04-02 | W0 | Ruby数据库3.0-chain | csv | 情感交互链路数据表 | Loona Deskmate\ | O1-KR1 |
| 2026-04-03 | W0 | Loona Deskmate-新人交接版项目认知报告 | 认知md | 新人视角项目整体认知交接报告 | Loona Deskmate\ | O1-KR1 |
| 2026-04-04 | W0 | 入职第一周总结汇报稿 | 汇报md | 第一周认知对齐成果汇报 | docs\plans\Week1\ | O1-KR1, O1-KR3 |
| 2026-04-04 | W0 | Agent 服务迭代方向 2026.04 / planner·router 大模型测试 | 评估md×3 | Agent 服务迭代方向梳理 + planner/router 模型测试记录 | Loona Deskmate\评估\ | O3-KR1, O2-KR1 |
| 2026-04-04 | W0 | 评测完整链路预案 / 评测集与标注规范 v1 / 自动化评测实现方案 v1 | 评估md×3 | 定义 router/planner 评测集结构、标注规则、错误分类、指标口径与自动化方案 | Loona Deskmate\评估\ | O3-KR1, O2-KR1, O4-KR1 |
| 2026-04-08 | W0 | 4.14 优化版本需求 + 3.31 重点问题复盘 | 需求md+复盘md | 基于 3.31 版本问题复盘提出 4.14 集中优化版本需求 | Loona Deskmate\4.14\ | O4-KR1, O4-KR2 |
| 2026-04-08 | W0 | 4.14 模块需求集：语音交互/注意力/决策机/Agent能力/信息同步/电脑信息提取 | PRD md×多 | 4.14（→4/30）各模块 PRD：模块定义/场景/流程/异常边界 | Loona Deskmate\4.14\ | O4-KR1, O1-KR2, O2-KR2 |
| 2026-04-08 | W0 | 4.14 场景 case 集：Agent/语音/注意力/电脑信息提取 | case md×多 | 各模块用户真实场景 case（验收版） | Loona Deskmate\4.14\ | O4-KR1, O4-KR4 |
| 2026-04-08 | W0 | 4.14 版本需求宣讲逐字稿 + 语音-Agent-注意力评测口径拆解 | 会议md+评测md | 4.14 需求宣讲记录 + 三模块守门视角评测口径拆解 | Loona Deskmate\4.14\ | O4-KR1, O3-KR1 |
| 2026-04-09 | W1- | 测试专项 kickoff（草案/会议版/逐字稿）+ 多场会议文字记录 | 会议md×多 | 测试专项启动：对齐范围/分类/指标/case 模板/建集规则；产品周会/耦合/问题定位/算法建议纪要 | Loona Deskmate\评估\、Loona Deskmate\4.14\ | O3-KR1, O4-KR1 |
| 2026-04-09 | W1- | bug-loona DM_刘旭 / agent评测会议 | csv+txt | bug 清单 + 评测会议记录 | Loona Deskmate\评估\ | O4-KR2 |
| 2026-04-10 | W1- | langfuse phase0 design / importer + import_summary | 设计md+导入json | Langfuse 接入 phase0 设计与 trace 导入（多批 import_summary） | Loona Deskmate\评估\docs\superpowers\、eval\outputs\ | O3-KR1, O4-KR1 |
| 2026-04-11 | W1- | langfuse-trace-evaluator-design | 设计md | Langfuse trace evaluator 设计 | Loona Deskmate\评估\docs\superpowers\specs\ | O3-KR1 |
| 2026-04-13 | W1 | 评测集设计与执行规范 v1.0 / v2.0 + Langfuse 字段设计 v1 | 规范md×3 | 评测集设计执行规范（产品收口版）+ Langfuse 接入字段设计 | Loona Deskmate\评估\ | O3-KR1, O2-KR1, O4-KR1 |
| 2026-04-13 | W1 | agent测试用例_原始（王琳/请求体/后台补充）+ casespec benchmark/langfuse dataset | csv×多 | 原始 agent 测试用例集 + benchmark/Langfuse 数据集导入 | Loona Deskmate\评估\、eval\ | O4-KR1 |
| 2026-04-14 | W1 | llm_as_a_judge_v1 | prompt md | LLM-as-judge 评测 prompt v1 | Loona Deskmate\评估\eval\configs\prompts\ | O3-KR1, O3-KR2 |
| 2026-04-15 | W1 | 04-14 软件产品周会 / 430 版本需求范围确定 / 测试集专项会×2 | 会议md×多 | 周会纪要 + 4/30 版本需求范围确定 + 测试集专项会共识 | Loona Deskmate\、Loona Deskmate\评估\ | O4-KR1, O4-KR3 |
| 2026-04-15 | W1 | MVP测试集模板（带示例）+ MVP测试场景与用例模板 + DM Agent 评测集设计预案 | 模板md+csv | 给测试团队的 MVP 测试集/场景用例模板 + 评测集设计预案 | Loona Deskmate\评估\ | O4-KR1, O3-KR1 |
| 2026-04-15 | W1 | Agent服务大模型任务调用接口 | 接口md | Agent 服务大模型任务调用接口梳理 | Loona Deskmate\评估\ | O1-KR1 |
| 2026-04-16 | W1 | 基于 Langfuse 的 RouterPlanner 评测体系落地方案 | 方案md | Router/Planner 自动化评测闭环落地方案（执行→判分→聚合→badcase回流） | Loona Deskmate\评估\ | O3-KR1, O3-KR2, O4-KR1 |
| 2026-04-17 | W1 | agent评测集确定纪要 + agent测试字段样例（router/planner/req_id/task_id 原表） | 会议md+csv×6 | agent 评测集字段口径确定 + router/planner 字段样例表 | Loona Deskmate\评估\ | O4-KR1 |
| 2026-04-17 | W1 | implementation_plan / task / walkthrough | 工程md×3 | 评测平台实现计划/任务/走查文档 | Loona Deskmate\评估\ | O3-KR2, O4-KR1 |
| 2026-04-17 | W1 | MVP 评测考察场景（承接 4.14 测试专项会） | 评测md | 承接专项会的 MVP 评测考察场景（含 Router 弱包含/Planner 强匹配断言法则）；作者署名秦宇龙 | Loona Deskmate\评估\ | O4-KR1, O4-KR4 |
| 2026-04-18 | W1 | Agent任务与能力 Wiki 化（飞书文档Wiki化流程 + wiki-project 全量 wiki） | 流程md+wiki md×多 | 把 Agent 任务与能力系统飞书文档 Wiki 化（capabilities/concepts/scenarios/版本差异/learnings） | Loona Deskmate\2需求文档\Agent任务与能力\wiki-project\ | O1-KR1, O2-KR2 |
| 2026-04-18 | W1 | 需求对齐&AI推进 2026-04-17 文字记录 | 会议md | 需求对齐与 AI 推进会议纪要 | Loona Deskmate\、wiki-project\raw\transcripts\ | O1-KR3 |
| 2026-04-20 | W2 | Loona Agent 自动化测试与评估平台技术方案 | 技术方案md | pytest+Excel 数据驱动评测平台升级改造方案（接口测试/回归/链路评估/统计） | Loona Deskmate\评估\ | O3-KR2, O4-KR1 |
| 2026-04-20 | W2 | Loona Agent 接口测试报告（md+docx）+ 测试产出与PRD不一致汇总 | 报告md/docx | 接口测试报告 + 比对测试产出与 PRD 的不一致项汇总 | Loona Deskmate\评估\ | O4-KR1, O4-KR2 |
| 2026-04-20 | W2 | 语音交互/注意力需求-20260430 + 语音唤醒场景case与分级 + 注意力场景case与分级 | 需求md+case md | 4/30 语音/注意力需求 + 唤醒（应/不应唤醒/判停）场景分级 case；AI workshop 与评估目录各一份 | AI workshop\、Loona Deskmate\评估\ | O4-KR1, O2-KR1, O4-KR4 |
| 2026-04-20 | W2 | loona-voice-workbench 一期设计 | 设计md | 语音工作台一期：样本标注/评测回放/实时Demo 三模块统一 Web | docs\superpowers\specs\ | O2-KR2, O3-KR2 |
| 2026-04-21 | W2 | AI workshop .planning（PROJECT/ROADMAP/REQUIREMENTS + Phase1-3 SPEC/SOLUTION/HANDOFF） | 规划md×多 | 多模态语音唤醒 Demo 课题：需求锁定→方案定义→执行交接（GSD 流程） | AI workshop\.planning\ | O2-KR1, O2-KR2, O2-KR3 |
| 2026-04-21 | W2 | demo_loona_voice DEMO-REQUIREMENTS / DEMO-GAP-ANALYSIS / WORKSTREAMS | 需求md×多 | Wake/Endpoint 单页 Demo 需求汇总 + gap 分析 + 工作流 | AI workshop\demo_loona_voice\ | O2-KR2, O2-KR3 |
| 2026-04-21 | W2 | 产研 vibe coding 小组推进 2026-04-20 文字记录 | 会议md | 产研 vibe coding 小组推进会议纪要 | AI workshop\ | O2-KR3, O1-KR3 |
| 2026-04-21 | W2 | 文档生成与电脑端预览场景case（6.12） | case md | Agent 文档生成+电脑端预览链路场景 case | Loona Deskmate\2需求文档\Agent任务与能力\Agent场景case\ | O4-KR4, O2-KR1 |
| 2026-04-23 | W2 | demo_loona_voice STATE-MACHINE-DESIGN + OPTIMIZATION-PLAN | 设计md×2 | 唤醒/判停规则 V1 终稿（指导实现与 case 回归）+ 优化计划 | AI workshop\demo_loona_voice\ | O2-KR2, O2-KR3 |
| 2026-04-24 | W2 | Agent相关指标 | 指标md | 用户可感知的 Agent 任务结果/过程体验/对话质量/状态一致性指标体系 | Loona Deskmate\评估\ | O3-KR1, O3-KR2, O4-KR1 |
| 2026-04-25 | W2 | 手机端应用管理-竞品调研与需求迭代记录 + PRD 审查 artifacts | 调研md+审查md | 支撑手机端应用管理 PRD V0.3 的竞品调研（授权/权限/状态/重授权/任务恢复）+ Claude PRD 审查记录 | Loona Deskmate\2需求文档\基础功能\、.omx\artifacts\ | O1-KR2, O2-KR2 |
| 2026-04-26 | W2 | 手机端应用管理需求文档（md+pdf） | PRD md/pdf | 手机端应用管理（插件/授权）正式需求文档 | Loona Deskmate\2需求文档\基础功能\手机端应用管理需求文档\ | O1-KR2, O2-KR2 |
| 2026-04-27 | W3 | Slack功能UI需求文档 | 需求md | 在 DM 对话中接入 Slack 查/读/总结/发/回 thread 能力（混合方案 A） | Loona Deskmate\2需求文档\Agent任务与能力\Agent场景case\ | O1-KR2, O2-KR1, O2-KR2 |
| 2026-04-28 | W3 | memory-prd-review artifact | 审查md | 记忆管理 PRD 审查记录 | Loona Deskmate\.omx\artifacts\ | O1-KR2, O2-KR2 |
| 2026-05-05 | W3 | 530 三线 MVP 需求包（00总方案/01文档生成/02知识库/03记忆/04Backlog与验收/05审查采纳） | PRD md×6 | 530 三线 MVP：文档空间/知识库/记忆并行方案 + Backlog 与验收场景 + Claude 审查采纳记录 | Loona Deskmate\2需求文档\基础功能\530三线MVP需求包\ | O1-KR2, O2-KR2, O4-KR3 |
| 2026-05-06 | W4 | PRD-430-memory-management-v0.2 | PRD md | 430 版本记忆管理需求文档（Profile/短期/长期三层） | Loona Deskmate\2需求文档\基础功能\ | O1-KR2, O2-KR2, O4-KR1 |
| 2026-05-07 | W4 | Slack 消息管理（子功能与case收束稿 + 场景case）+ 审查 artifact | 收束md+case md | 基于 user token 接入后的 Slack 消息管理 PRD 与场景 case 修订收束 | Loona Deskmate\2需求文档\Agent任务与能力\Agent场景case\ | O2-KR2, O2-KR3, O4-KR1, O4-KR4 |
| 2026-05-13 | W5 | Agent任务状态反馈UI通用范式 + Agent-UI设计需求 | 设计md×2 | Agent 任务状态反馈 UI 通用范式 + Agent-UI（日程等）设计需求 | Loona Deskmate\2需求文档\Agent任务与能力\ | O2-KR2, O2-KR3, O3-KR2 |
| 2026-05-15 | W5 | loona-voice-demo（README/skills/requirements） | 工程md | LiveKit voice→Claude→voice 技术路线 1 demo + 复盘 skill | loona-voice-demo\ | O2-KR3 |
| 2026-05-18 | W6 | 最新评测集：427标注_聚合_204（req_id/task_id/异常聚合）+ Router_Planner_Case_Data（xlsx+合并/分块csv）+ Agent场景case | 评测csv/xlsx×多 | 最新 Router/Planner case 数据聚合与合并（427 标注 204 条）+ Agent 场景 case 交互效果整理 | Loona Deskmate\评估\最新评测集\、评估\ | O4-KR4, O4-KR1, O3-KR1 |

## 按子目录归纳

### Loona Deskmate\评估（评测体系 · 最密集 · 强映射 O3-KR1 + O4-KR1）
本机最活跃的交付目录，从 W0 持续到 W6。交付物谱系完整：评测集与标注规范（v1→v2.0）、Langfuse 接入（字段设计/phase0 importer/trace evaluator）、基于 Langfuse 的 Router/Planner 评测体系落地方案、自动化测试与评估平台技术方案、接口测试报告、Agent 相关指标体系、MVP 评测考察场景（秦宇龙署名）、测试产出与 PRD 不一致汇总，以及大量 agent 测试用例/字段样例 csv。最近活跃 5/18（最新评测集：427 标注 204 条聚合 + Router_Planner_Case_Data）。这是 **O3-KR1（体验/问题分析）+ O4-KR1（版本需求+测试集）** 的最强本机证据。

### Loona Deskmate\4.14（4.14→4/30 版本需求 · 强映射 O4-KR1）
W0（4/8-4/9）集中产出：3.31 重点问题复盘 → 4.14 优化版本需求 → 各模块 PRD（语音交互/注意力/决策机/Agent 能力/电脑·手机信息同步/电脑信息提取）+ 配套场景 case（验收版）+ 需求宣讲逐字稿 + 三模块评测口径拆解。映射 **O4-KR1（4/30 版本需求+测试集）+ O1-KR2/O2-KR2（模块需求拆解）**。4/15 后由 430 版本需求范围确定接棒。

### Loona Deskmate\2需求文档（Agent能力 + 基础功能 PRD · 强映射 O1-KR2 + O2-KR2）
两条线：(1) **Agent任务与能力**——W1 把飞书文档 Wiki 化（wiki-project 全量 capabilities/concepts/scenarios），W2-W6 产出场景 case（文档生成与电脑端预览、Slack 功能 UI/消息管理收束稿、Agent 任务状态反馈 UI 范式、Agent-UI 设计需求）；(2) **基础功能**——手机端应用管理 PRD（W2，含竞品调研+pdf）、530 三线 MVP 需求包（W3，文档空间/知识库/记忆 6 份）、430 记忆管理 PRD v0.2（W4）。强映射 **O1-KR2（承接非 Agent 小模块需求）+ O2-KR2（拆解→方案→协作）+ O4-KR3（6/30 版本需求）**。最近活跃 5/13-5/14。

### AI workshop（语音唤醒 Demo 课题 · 映射 O2-KR1/KR2/KR3）
顶层少量真文档（语音交互/注意力需求-20260430、语音唤醒/注意力场景 case 与分级、产研 vibe coding 纪要）+ `.planning`（GSD：PROJECT/ROADMAP/Phase1-3 SPEC→SOLUTION→HANDOFF）+ `demo_loona_voice`（DEMO-REQUIREMENTS/STATE-MACHINE-DESIGN V1 终稿/OPTIMIZATION-PLAN）。这是 **O2-KR1（识别定义 AI 赋能场景：多模态语音唤醒）+ O2-KR2/KR3（拆解→方案→推进 demo）** 的证据。注意：该目录 4.6 万文件主体是 ten-framework 三方仓，与个人产出无关。最近活跃 W2（4/21-4/24）。

### docs/plans/Week1 + 会议 + openspec（入职认知 + 早期需求 · 映射 O1-KR1）
W0 入职第一周六步认知产出（产品总图/模块地图/主链路/Agent 中枢/版本边界/产品判断）+ 黑话表 + 第一周汇报稿；`会议`决策机通讯架构梳理（4 个系统问题）；`openspec`天气场景气泡 MVP 需求（3 版）；`docs`飞书工作复盘 Agent PRD v2。映射 **O1-KR1（认知对齐）+ O2-KR1（早期场景定义）**。集中在 4/1-4/4，W1 后基本无更新。

### loona-voice-demo（语音 demo 工程 · 弱映射 O2-KR3）
W5（5/15）LiveKit voice→Claude→voice 技术路线 1 demo（README + retrospective skill），代码仓本体，文档面薄。

## 与 KR 强相关结论（本机文档视角）

- **O4-KR1（版本需求 + 测试集）**：最强证据线 —— 4.14/4.30 模块 PRD + 评估目录全套测试集/标注规范/评测体系（W0-W1 密集，W6 最新评测集聚合）。
- **O1-KR2 + O2-KR2（非 Agent 模块需求 + 拆解协作闭环）**：手机端应用管理 PRD、530 三线 MVP、430 记忆管理、Slack 场景 case（W2-W5）。
- **O3-KR1/KR2（Agent 体验/问题分析 + 产品化方法沉淀）**：评测口径拆解、Agent 相关指标、测试产出与 PRD 不一致汇总、自动化评估平台技术方案。
- **O1-KR1（认知对齐）**：入职六步认知产出 + 情感交互架构 + Wiki 化（W0-W1）。
- **O2-KR1/KR2/KR3（AI 赋能场景闭环）**：AI workshop 多模态语音唤醒 Demo 课题（需求→方案→demo，W2）。
- **本机相对缺口**：O3-KR3（中长期路线图）、O2-KR4（项目末复盘）、O4-KR4（6/30 验收标准+关键 Case 的完整定稿）在本机文档中偏弱，主要落在 C 盘 session（Jarvis/rowboat 工程验收，见 session 账本）。
