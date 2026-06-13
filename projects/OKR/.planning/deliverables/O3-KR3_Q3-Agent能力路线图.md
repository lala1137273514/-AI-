# Q3 Agent 能力发展方向与路线图

> **定位**：O3-KR3 收口主交付物。把 Q2 积累的分散方向素材（Loona-Spec 自我迭代协议、Agent 决策小组方向提案、三份方向介绍、rowboat v1.3 记忆回路、Jarvis Loona Protocol 现状、6/30 最小版本目标）综合成一份**带现状盘点 + 方向候选 + 优先级排序 + 阶段里程碑 + 风险依赖**的中长期 Agent 能力发展规划/路线图。
> **KR**：O3-KR3「6 月内提出中长期 Agent 能力发展方向与优先级建议，输出 1 份阶段性规划/优化路线图」（KR id `7627422847853628596`，O3 = 建立长期 Agent 发展规划意识）
> **状态**：v1.0 · 收口于 6 月窗口 · 作者 秦宇龙
> **配套分析**：`C:\Users\QYL\Desktop\OKR\.planning\kr\O3-KR3.md`；上游输入 = O3-KR1（问题分析）、O3-KR2（产品化方法沉淀）

---

## 0. 导读：这份路线图解决什么问题

Q2 末盘点发现：Agent 能力的**方向素材已经很齐**（评测器、Protocol 规范、记忆回路、人格系统、决策小组 10+ 提案），但它们**彼此并列、无统一优先级、未排里程碑**——是「素材齐、缺收口」的状态。本路线图的唯一目标，就是把这些散点收口成一条**可执行、按价值×可行性排序、有月度里程碑**的主线，让 6 月～Q3 的能力建设有据可依、不再凭手感取舍。

阅读顺序：先看 §1 现状（我们已经站在哪）→ §2 方向候选清单（能往哪走）→ §3 优先级（先走哪条，明确取舍）→ §4 阶段路线图（按月怎么落）→ §5 风险与依赖。

---

## 1. 现状盘点：当前已具备 / 已验证的能力

> 原则：只盘点**有真实产出与可核验证据**的能力，区分「已验证（跑通且有数据）」与「已具备框架（设计成型待落地）」。

### 1.1 已验证（有真实数据，可作路线图地基）

| 能力 | 当前状态 | 关键数据 / 证据 |
|---|---|---|
| **Loona Agent Interaction Protocol 真验收** | 全栈对齐 + harness 自迭代跑通三层真验收 | schema 209/209；LIVE 102/125（81.6% 三票通过）；state-inject 36/36；halo ~98%；修复 7 个 live bug（卡乱码/loona-card 类/TTS 标点/双重朗读等）。证据：Jarvis `loona-protocol-align` 分支、loona-workbench v1（5/22） |
| **人性化收束层评测器** | 两层评测（确定性指标 + LLM judge）跑通，Langfuse 真 trace，benchmark 成型 | 112 条 ground-truth（5 scene × 7 scenario × 3 persona + 13 对抗边界用例）；`evidence_diff` 唯一硬 FAIL 闸门；实测真实生产 humanizer 约 **23% evidence_diff FAIL**；外部校准盲评 Claude 100% 复现、qwen-plus 84.3%（κ=0.727）；CC 重构后确定性回放 83/83=100% 零回归。证据：rowboat `evals/humanization/DESIGN.md`、[飞书评测器展示](https://f4x6dn8llc.feishu.cn/docx/CdnJdNJlyo7tvDxiOMBcR1fbnoc) |
| **Loona-Spec（Know-How）v1.0** | 四/三层 behavioral conformance spec，可机检 | 223 条机检需求（blocker 64 / major 147 / minor 12，RFC2119 MUST/SHOULD/MAY）；8 个质量闸门 G1-G8 全绿；9 卡 Component Schema + golden cases。证据：[飞书](https://f4x6dn8llc.feishu.cn/docx/ROGudTNWPoF2pdx9FHccEH35nmg)、本机 `Loona-Knowledge-System` |
| **rowboat 记忆/知识 GSD 工程** | v1.2「Knowledge Compounding」13 phase 全 shipped，已打 tag | 飞书接入 Block A（Calendar/Base/Sync）+ Chat→KG Block B + 记忆智能 Block C（Recency+Decay/Similarity/Archived/冲突检测），513 测试，tag `knowledge-compounding-v1.2`；KB Lab 双进程基准台（可并排 A/B 测 模型×KB×记忆×人格） |
| **Persona / 人性化（CC Persona）** | 「毒舌技术搭档」人格运行系统上线，独立 humanizer 收束 | 7 子系统 + 独立 humanizer；人格为声明式参数（`personas{cc, loona-deskmate, neutral}`），加新人格 = 注册表 + 种子、零评测器代码。证据：GitHub `cc-persona`、[飞书 Persona](https://f4x6dn8llc.feishu.cn/docx/KHtldKia5omBQJxigQicnuAznGe) |
| **可观测 + 评测体系三层** | trace 打底 + 确定性指标铁闸门 + LLM judge 软判，已落地 | Langfuse trace；确定性指标零方差判官无关；judge 用强评委（Claude）。证据：[飞书可观测+评测](https://f4x6dn8llc.feishu.cn/docx/PDvBdqJ3Qo6OBQxnasZcghkwnmL) |

### 1.2 已具备框架 / 短链路（设计成型，待 6 月落地）

- **短链路（短意图直达）**：Cortex 提示词体系 3 层 + 1 旁路 + 1 外挂；Router「加重职责产生第一步反馈」机制设计成型。
- **人格过滤 / Persona 记忆**：人格声明式 + humanizer 收束链路已通；Persona 记忆（隐式贴合，不表演"我记得你"）规则在 Loona-Spec Layer 0 已定义。
- **动作风险分级 P0/P1/P2**：P0 查询/总结/推荐/起草可自动；P1 需确认；P2（发送/改日程/删除/支付/长期记忆写入）必须用户拍板——已写入规范，待全链路强制执行。
- **TTS / 载体分工**：DashScope Qwen3-TTS 实时（WS 协议）接入；口播/卡片/文档/TTS 载体分工规则成型。

### 1.3 当前缺口（路线图要填的）

1. **Loona Protocol 红线未通项**：云盘 / 日历 / 邮件三类能力尚未全部跑通真验收（Jarvis Loona Protocol 现状）。
2. **6/30 最小版本未收口**：邮件/日程/地图/文档生成/天气五场景的短链路 + 人格过滤 + Persona 记忆尚未端到端打通成可演示版本。
3. **记忆回路 v1.3 未闭环**：Agent Notes 蒸馏器 + Chat→KG + Feishu 回写在 5/19 GSD 正规化启动，尚未 shipped。
4. **方向无统一优先级**：决策小组 10+ 提案、三份方向介绍彼此并列，缺一份取舍后的主线（本路线图正在补）。

---

## 2. 方向候选清单（价值 / 成熟度 / 依赖）

> 来源：Agent 决策小组 5/7 Kickoff 的 10+ 方向提案、三份方向介绍、Loona-Spec 自我迭代协议、rowboat v1.3 记忆回路、Live2D/数字人调研。每个方向标注**价值**、**成熟度**（已验证 / 框架成型 / 雏形 / 调研）、**依赖**。

| # | 方向 | 价值 | 成熟度 | 主要依赖 |
|---|---|---|---|---|
| D1 | **6/30 最小可用版本**（邮件/日程/地图/文档生成/天气 + 短链路 + 人格过滤 + Persona 记忆） | 极高——直接决定 6/30 能否对外演示，是 Q3 一切场景的承载体 | 框架成型（各组件单点已通，缺端到端收口） | Cortex/ToolHub/Bridge 链路、TTS、人格 humanizer、Persona 记忆 |
| D2 | **Loona Protocol 自我迭代协议 + 跨场景登记表**（路线图骨架） | 极高——把「Agent 该做什么」固化为可机检规范 + 自迭代闭环，是其余方向的统一尺子 | 已验证（v1.0 223 条机检 + 209 case 真验收） | harness 自迭代、Eval Case Pack、评测器 |
| D3 | **量化评测 / 可观测体系**（确定性指标 + LLM judge + 收束层评测器） | 极高——是所有能力「好不好」的度量地基，护城河级资产 | 已验证（112 ground-truth benchmark，外部校准过） | Langfuse、强评委模型（Claude） |
| D4 | **记忆架构 + 知识库耦合**（rowboat v1.3 记忆回路：Agent Notes 蒸馏器 + Chat→KG + Feishu 回写） | 高——长期记忆是 Agent 从「会话工具」升级到「长期伙伴」的核心壁垒 | 框架成型（v1.2 记忆智能已 shipped，v1.3 回路启动） | Chat→KG 抽取稳定性、KB Lab 基准台、Feishu 写回 |
| D5 | **性格 / 人性化自动化**（CC Persona 声明式人格 + humanizer 收束自动化） | 高——决定产品「像不像人」的体感差异化；声明式已可零代码挂新人格 | 已验证（CC Persona 上线 + 评测器零回归保障） | 收束层评测器、人格注册表 |
| D6 | **主动任务 / 主动感知**（注意力、主动提醒、任务气泡） | 中高——从「问答式」走向「主动陪伴」，但易踩静默高危动作红线 | 雏形（注意力/气泡 MVP 需求成型，未端到端） | 动作风险分级 P0/P1/P2 强制、感知层 |
| D7 | **并行规划 / 多 session 编排**（GSD 单 phase 节奏 + 多 agent wave 编排） | 中——提升交付吞吐，已是当前工程实际工作方式 | 框架成型（rowboat/Codex worktree 多 agent 实证） | 编排稳定性、n8n（仅编排层） |
| D8 | **具身执行 / 物联网联动 / Live2D 数字人** | 中——长期形态探索，决定 Agent 的「身体」 | 调研（Live2D/数字人/Real-Time-Pose 仓库试跑） | 硬件、运动控制、唤醒词/决策机 |
| D9 | **自动化测试平台**（pytest+Excel 数据驱动评测平台升级） | 中——把评测从手工跑变成可回归流水线 | 框架成型（技术方案 + 接口测试报告已出） | 评测集标注规范、case 库 |

---

## 3. 优先级排序（价值 × 可行性，明确取舍 P0/P1/P2）

> 排序逻辑：**价值**（对 6/30 版本与长期壁垒的贡献）× **可行性**（成熟度越高、依赖越少越可行）。不并列、做取舍——把当前主线压缩到 3 个 P0，避免精力分散。

### P0（6 月必做，决定能否交付）

- **P0-1 = D1 6/30 最小可用版本**：这是 6 月唯一的硬交付，所有其他方向都为它服务或在它之后。理由：价值极高（对外演示门槛）+ 组件可行性已具备，只缺端到端收口。
- **P0-2 = D2 Loona Protocol 自我迭代协议 + 跨场景登记表**：作为路线图骨架与统一验收尺子，6/30 版本的每个场景都要按它做行为级验收。理由：已验证、可机检，是「接线在但行为错」唯一的防线。
- **P0-3 = D3 量化评测 / 收束层评测器**：6/30 版本要敢说「做对了」，必须有铁闸门兜底（尤其 humanizer 23% evidence_diff FAIL 的事实门）。理由：护城河级、已验证、判官无关。

> **取舍说明**：D5 人性化在 6 月不独立立项——它已通过 D3 评测器获得零回归保障、随 D1 版本附带交付，不再单列 P0。

### P1（Q3 内做，构建长期壁垒）

- **P1-1 = D4 记忆架构 + 知识库耦合**（v1.3 记忆回路闭环）：长期伙伴的核心壁垒，承接 v1.2 已 shipped 的地基，7 月主攻。
- **P1-2 = D5 性格/人性化自动化**：声明式人格 + humanizer 自动收束做成可复用模块，跨 Agent 复用。
- **P1-3 = D9 自动化测试平台**：把评测从手工升级为可回归流水线，支撑 D1/D2 持续验收。

### P2（Q3 末或之后，方向探索/择机）

- **P2-1 = D6 主动任务 / 主动感知**：价值高但红线风险大，须等 P0/P1 的风险分级强制执行成熟后再推。
- **P2-2 = D7 并行规划 / 多 session 编排**：已是工作方式，作为基础设施持续优化，不单独抢里程碑。
- **P2-3 = D8 具身/物联网/Live2D 数字人**：长期形态探索，保持调研节奏，不在 Q3 占用主力。

---

## 4. 阶段路线图（Q3 按月 / 里程碑）

> 主轴：**6 月收口 6/30 最小可用版本（P0）→ 7 月构建记忆 + 人性化壁垒（P1）→ 8 月评测流水线 + 主动能力试点 → 9 月整合验收 + 方向探索**。

### 6 月（收口期 · P0 三件套 → 6/30 版本）

| 时段 | 里程碑 | 交付物 |
|---|---|---|
| 6 月上 | 能力现状盘点 + 缺口清单（以 O3-KR1 问题分析 / O3-KR2 方法沉淀为输入） | 现状盘点（本文 §1）+ 缺口清单（§1.3） |
| 6 月中 | 方向候选整合 + 优先级矩阵；Loona Protocol 红线未通项（云盘/日历/邮件）补真验收 | 方向候选清单（§2）+ 优先级（§3）；Protocol 验收补齐 |
| 6 月下 | **6/30 最小可用版本端到端打通**：邮件/日程/地图/文档生成/天气 + 短链路 + 人格过滤 + Persona 记忆；按 Loona-Spec 做行为级验收，收束层评测器把关事实门 | **6/30 可演示版本** + 本路线图 v1.0 收口 |

### 7 月（壁垒期 · P1）

- **M7.1 记忆回路 v1.3 闭环**：Agent Notes 蒸馏器 + Chat→KG + Feishu 回写 shipped；KB Lab 基准台跑通记忆/知识 A/B 评测。
- **M7.2 人性化自动化模块化**：humanizer 收束 + 声明式人格做成可复用模块，新 Agent 零代码挂人格 + 评测零回归。
- **M7.3 评测平台 v1**：pytest+Excel 数据驱动评测平台升级，把 D2/D3 验收变成可回归流水线（承接 P1-3）。

### 8 月（扩展期）

- **M8.1 评测流水线常态化**：6/30 版本的每次迭代自动跑回归（schema + LIVE + 收束层 + 记忆）。
- **M8.2 主动任务/感知试点**：在风险分级 P0/P1/P2 强制执行成熟后，试点注意力/主动提醒（P2-1），小范围灰度。
- **M8.3 跨场景登记表扩充**：把 6/30 五场景的 know-how 沉淀回 Loona-Spec 跨场景注册表，扩 Eval Case Pack。

### 9 月（整合验收期）

- **M9.1 Q3 能力整合验收**：记忆 + 人格 + 主动 + 评测在 6/30 版本上整合，跑一次完整三层真验收。
- **M9.2 Q3 复盘 + Q4 方向输入**：复盘 P0/P1 达成度，输出 D8（具身/数字人）等长期方向的 Q4 立项建议。
- **M9.3 路线图 v2.0**：基于 Q3 实绩更新优先级与里程碑。

---

## 5. 风险与依赖

| 类别 | 风险 / 依赖 | 影响 | 缓解 |
|---|---|---|---|
| **架构一致性** | Jarvis×Cortex×ToolHub×Bridge 多服务链路，改动易引入行为级偏差（「接线在但行为错」） | 6/30 版本端到端行为错 | 一律按 Loona-Spec 做行为级验收（D2）；收束层评测器事实门兜底（D3）；harness 自迭代回归 |
| **红线（云盘/日历/邮件）** | Loona Protocol 三类能力尚未全部跑通真验收 | 6/30 版本场景缺口 | 6 月中优先补这三项真验收，纳入 P0-1 范围 |
| **高危动作** | 主动任务易触发静默高危动作（未确认就发邮件/改日程） | 用户信任损伤、红线事件 | 动作风险分级 P0/P1/P2 强制执行；P2 必须用户拍板；主动能力（D6）推迟到风险分级成熟后 |
| **评测可信度** | LLM judge 质量上限 = 评委模型本身，弱评委漏判 | 评测虚高、错误放行 | 事实门用确定性指标；人格/过度改写用强评委（Claude），外部校准（已做：Claude 100% / qwen 84.3% κ=0.727） |
| **记忆稳定性** | Chat→KG 抽取/建图的模型不稳定，n8n 只解决编排层碰不到 | v1.3 记忆回路质量不稳 | KB Lab 基准台持续 A/B 评测抽取质量；记忆冲突检测 lint（v1.2 已 shipped）兜底 |
| **人力 / 优先级** | 单人主力，P0/P1/P2 同时推会分散 | 6/30 收口延期 | 严格按 §3 取舍：6 月只压 P0 三件套，P1 推迟到 7 月，P2 不抢里程碑 |
| **外部决策（旭哥/团队对齐）** | 路线图优先级、6/30 版本范围需与团队/上级对齐 | 方向返工 | 本路线图作为对齐基线提交评审；Loona-Spec 跨场景登记表作为团队共识载体 |

---

## 6. 小结

- **现状**：站点不低——Protocol 真验收（209/209 schema + 81.6% LIVE）、收束层评测器（112 benchmark + 外部校准）、Loona-Spec v1.0（223 机检）、记忆 v1.2 已 shipped、CC Persona 上线，均为有数据的已验证资产。
- **取舍**：6 月只压 **P0 三件套**（6/30 版本 / Loona Protocol 自迭代协议 / 量化评测），其余排进 7-9 月 P1/P2，明确不并列。
- **主轴**：6 月收口 6/30 版本 → 7 月记忆+人性化壁垒 → 8 月评测流水线+主动试点 → 9 月整合验收+Q4 方向输入。
- **最大风险**：架构一致性（「接线在但行为错」）与高危动作红线——靠 Loona-Spec 行为级验收 + 收束层事实门 + 风险分级强制执行三道防线兜底。

---

## 附录 · 证据索引

| 方向 | 证据 | 链接 / 路径 |
|---|---|---|
| Loona Protocol 真验收 | 209 case schema + 125 LIVE 三层真验收 | Jarvis `loona-protocol-align` 分支、loona-workbench v1（本机 session 5/22） |
| Loona-Spec v1.0 | 223 条机检 + 8 闸门 + 自我迭代协议 + 跨场景注册表 | [飞书](https://f4x6dn8llc.feishu.cn/docx/ROGudTNWPoF2pdx9FHccEH35nmg) · GitHub `lala1137273514/loona-spec` · 本机 `Loona-Knowledge-System` |
| 收束层评测器 | 112 ground-truth + evidence_diff + 外部校准 | [飞书展示](https://f4x6dn8llc.feishu.cn/docx/CdnJdNJlyo7tvDxiOMBcR1fbnoc) · 本机 `rowboat/evals/humanization/DESIGN.md` |
| 可观测+评测 | 方向介绍：可观测+评测体系（三层） | [飞书](https://f4x6dn8llc.feishu.cn/docx/PDvBdqJ3Qo6OBQxnasZcghkwnmL) |
| 记忆+知识库 | 方向介绍：记忆+知识库框架 | [飞书](https://f4x6dn8llc.feishu.cn/docx/IXgAdUy5JohEURx5RMYct8mmn4z) |
| Persona | 方向介绍：CC Persona 性格+人性化 | [飞书](https://f4x6dn8llc.feishu.cn/docx/KHtldKia5omBQJxigQicnuAznGe) |
| 记忆回路 v1.3 | rowboat v1.2 13 phase shipped + v1.3 回路启动 | 本机 `rowboat`，tag `knowledge-compounding-v1.2` |
| Agent 决策小组 | 5/7 Kickoff 方向提案 | [飞书](https://f4x6dn8llc.feishu.cn/docx/My0bdLJ66oT0w3x4CB1cliJAnjg) |
| 上游输入 | O3-KR1 问题分析 / O3-KR2 方法沉淀 | 本机 `.planning/deliverables/O3-KR1_*.md` / `O3-KR2_*.md` |

*v1.0 · 收口于 6 月窗口 · 作者 秦宇龙*
