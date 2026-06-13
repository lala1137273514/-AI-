# Q2 复盘三源回填总览（2026-04-13 ~ 05-22）

> 生成时间:2026-05-26｜工具:`loona-daily-review-v2` skill（牛马一号·升级版）
> 范围:**只生成本地文件**(`.planning/dailies-v2/` + `.planning/weeklies-v2/`),**未触碰飞书任何已有日报/文档**。
> 是否同步飞书 = 待你拍板。

## 一、交付物

| 交付物 | 位置 | 数量 |
|---|---|---|
| 可复用 skill | `C:\Users\QYL\.claude\skills\loona-daily-review-v2\` | SKILL.md + 3 reference + scan_local.py |
| Q2 日报（新结构） | `.planning\dailies-v2\YYYY-MM-DD.md` | **35 篇**（28 工作日满格 + 7 周末/假期日） |
| Q2 周报（新结构） | `.planning\weeklies-v2\W{n}-起~止.md` | **6 篇**（W1–W6） |

- 28 个工作日均为完整 6 节日报；3 篇极简日报（05-03 五一系统复盘 / 05-04 假期休整 / 05-10 周日归档）为 3 节有意为之；4 篇周末加班日（04-25/26、05-09、05-17）按证据满格补出。
- 05-22 与官方样板 `日报示例-新结构-2026-05-22.md` 1:1 对齐（209/209、102/125、loona-card、"控制权分配器"等关键标记全部一致）。

## 二、覆盖日历

| 周 | 工作日（满格 6 节） | 周末/假期补充 | 周报 |
|---|---|---|---|
| **W1** 04-13~19 | 04-13,14,15,16,17 | — | ✅ |
| **W2** 04-20~26 | 04-20,21,22,23,24 | 04-25(六·加班)、04-26(日·加班) | ✅ |
| **W3** 04-27~05-03 | 04-27,28,29,30 | 05-03(五一系统复盘·极简);05-01 劳动节无证据跳过 | ✅ |
| **W4** 05-04~10 | 05-05,06,07,08 | 05-04(假期休整·极简)、05-09(六·AI Jam+决策小组)、05-10(日·归档·极简) | ✅ |
| **W5** 05-11~17 | 05-11,12,13,14,15 | 05-17(六·GSD Block B 收尾·极简) | ✅ |
| **W6** 05-18~24 | 05-18,19,20,21,22 | 05-23/24 周末并入周报 | ✅ |

## 三、补回的"过去漏掉的工程线"（核心价值）

旧 cron 日报只抓飞书侧（会议/日程/文档），系统性漏掉本地工程线。本次按当天逐条补回并打 KR 标签:

### W1 — 评测体系冷启动（旧日报只记会议）
- 本机评估目录:评测集执行规范 v1/v2.0 + Langfuse 字段设计 + agent 原始用例 csv（4/13）、llm_as_a_judge_v1（4/14）、基于 Langfuse 的 RouterPlanner 评测闭环方案（4/16）、MVP 评测考察场景·Router 弱包含/Planner 强匹配断言法则·秦宇龙署名（4/17）。
- Codex:Slack MCP 能力边界验证（四类 case，7 会话，4/16）、周会深度分析×3（4/15）。

### W2 — AI workshop 语音唤醒 demo 全套（旧日报只记 Wiki/Slack）
- AI workshop GSD 立项 .planning（Phase1-3 SPEC→SOLUTION→HANDOFF）+ demo_loona_voice 需求/状态机 V1 终稿（4/21、4/23）。
- 评测平台技术方案（pytest+Excel）+ 接口测试报告 + Agent 相关指标体系（4/20、4/24）。
- Loona-Deskmate PRD 审查:手机端应用管理 P0~P3 分级 + 瘦身图表化 + 430 记忆三层 PRD（4/25、4/26）。

### W3 — 复盘体系自动化 + Agent 方法（旧日报记 skill 但漏 Codex 线）
- Codex:430 case UI 期望响应链路、可验收 PRD 模板、Agent 指标体系（三类可感知指标）、Figma MCP 读设计稿（4/27-4/29，4/29 是被漏最多的一天）。
- daily-review skill 0→1（10 步）+ 复盘日历 + OKR 四表 + 日报/bitable 拆独立 cron（4/27、4/30）。

### W4 — 530 MVP + Agent 进化方法（旧日报记会议，漏工程）
- 530 三线 MVP 6 份 PRD + Claude「有条件通过」审查（5/5）；**Actor/Judge/Optimizer 三角色进化闭环**（5/7）；Agent 个性化风格迭代约束专项（5/8）；430 文本生成存放歧义方案（5/5-5/6）。
- 关键节点写厚:5/6 转型专项制·秦宇龙任「用户记忆与个性化」Owner；5/9 AI Jam 主持（~40 人）+ Agent 决策小组 Kickoff。

### W5 — 漏得最狠的一周（飞书侧承认"主力在本地工程"）
- **rowboat:GSD 自治 v1.2 Phase 11-15 连续 shipped**（飞书 Calendar/Base Ingest ~1.06M token、Sync+Health UI，253→19 commit 量级）（5/14、5/15）。
- **CC Persona「毒舌技术搭档」7 子系统人格运行系统 + 推 GitHub 5 commit**（5/14）。
- **DashScope WS 实时 TTS 接入**（dashscope.ts）+「Loona=语音化输出适配器」关键 insight（5/13）。
- Codex 单日 19 会话 rowboat Loona Mode 六专项并行（5/12）、11 段提示词 6 wave 多 agent 编排（5/13）。
- 三大方向文档:可观测+评测体系 / 记忆+知识库框架 / CC Persona 人性化（5月中）。

### W6 — Jarvis 真验收 + Loona-Spec（旧日报记会议，漏全部工程验收）
- **Jarvis R4 全链路真验收**:schema 209/209、LIVE 102/125（81.6%）、state-inject 36/36，修 7 个 live bug（5/22）。
- **Loona Agent Interaction Protocol 全栈对齐**（24 章/8 验收 checklist）+ TTS 真同步修复 + 旅游 lifecycle 8 阶段 + ToolHub 接飞书（5/21）。
- **Loona-Spec v1.0**:223 条机检需求 + behavioral conformance spec（5/22）。
- rowboat v1.2 归档打 tag（513 测试）+ 人性化收束层评测器全量构建 + Langfuse 真 trace + 112 benchmark（5/18、5/19）。
- KB Lab 启动、Jarvis LifeOS Phase1-3、Cortex 深度问题报告、bad-case 评测方法分析（174 用例）。

## 四、数据源覆盖与盲区（如实标注）

- ✅ **飞书**:日程 / 会议智能纪要 / 日复盘 / 周报 docx 链接全程接入（取自 `.planning/ledger/feishu.md`）。
- ✅ **本地 Claude**:Jarvis / rowboat / Loona-Deskmate / konw-how / OKR 等项目 session 逐日归并（账本有效命中 4/25 起，W5-W6 最密集）。
- ⚪ **Codex**:有效会话 4/15–5/15；**5/18 起账本无 Codex 会话**，W6 各日 Codex 均如实标 ⚪。
- ⚠️ **IM 单聊/群聊**:cron 权限受限，全程未抓取——这是已知盲区，关键对话需手动补。

## 五、合规性自检

- ✅ 仅写本地文件，**飞书已有日报/文档零改动**（无 docs +create/+update、无 OKR 写入、无 bitable 写入）。
- ✅ OKR 措辞全程 `normal`，**未使用"逾期/延期"**（W1 周报中出现的"延期/逾期"仅为说明规则本身的元文字）。
- ✅ 进度百分比按 DDL 节奏（已过期→100% / 5月底→80% / 6/30→60-75%），取自 `.planning/progress/O{1-4}.json`。
- ✅ 旧 `.planning/W5周报.md` 未改动；新版 W5 周报另存于 `weeklies-v2/`。

## 六、下一步（待你决定）

1. **同步飞书**:如要把 v2 日报/周报推飞书，用 `loona-daily-review-v2` skill 的「写」流程——但需先列「个人复盘」folder 确认无同名文档，避免与旧 cron 产物重复。
2. **接管 cron**:可让牛马一号 cron（18:20/18:30/22:00）改调本 skill，使日后日报自带本地工程线 + KR 标签。
3. **回填 OKR 进展**:若要把这季工程线落成 OKR 进展记录，复用 `.planning/apply_progress.py real`（已 DDL-paced、状态 normal、多周递增）。
