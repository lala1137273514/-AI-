# OKR KR 映射参考（Q2 2026 · 周期 7622051252293749950）

> 14 个 KR。open_id `ou_9e35d4bb77a72e6180e8f54417ff0532`。
> 进度按**有效 DDL 节奏**（已过期→100% / 5月底→80% / 6/30→60-75%），状态**恒 normal**，永不写"逾期"。

## 14 KR 全表

| 标签 | KR id | KR 名称（简） | 有效 DDL | DDL-paced 当前% |
|---|---|---|---|---|
| **O1-KR1** | 7626271491483389119 | 业务/产品/架构认知对齐 | 入职1-2周（已过期） | 100% |
| **O1-KR2** | 7626271435473177779 | 承接非 Agent 小模块需求（≥1-2 个，五要素齐全） | 6/30 | 75% |
| **O1-KR3** | 7626271274969844667 | 稳定需求输出 + 协作习惯（日/周报、对齐） | 全 Q2 / 6/30 | 75% |
| **O2-KR1** | 7626271568236547040 | 识别并定义 AI 赋能场景（≥3） | 全 Q2 / 6/30 | 75% |
| **O2-KR2** | 7626271828239060173 | 需求拆解→方案设计→协作闭环 | 6/30 | 70% |
| **O2-KR3** | 7626271562145024990 | 推动 AI 场景实现/跑通/落地 | 6/30 | 75% |
| **O2-KR4** | 7626271889488743624 | 项目末五要素复盘总结 | 项目末（6月） | 65% |
| **O3-KR1** | 7627421948808973250 | Agent 体验分析 + 问题分析文档 | 4 月内（已过期，诚实补登） | 100% |
| **O3-KR2** | 7627422941223472347 | 产品化方法沉淀（4 要素总纲） | 5 月内（5/31） | 80% |
| **O3-KR3** | 7627422847853628596 | 中长期方向 / 路线图 | 6 月内 | 60% |
| **O4-KR1** | 7627422012026522569 | 430 版本需求 + 测试集 | 4/30（已过期） | 100% |
| **O4-KR2** | 7627423339209133261 | 5 月问题整理 → 6 月迭代输入 | 5 月内（5/31） | 80% |
| **O4-KR3** | 7627422012026588105 | 6/30 版本需求 + 评审 + 研发对齐 | 6/30 | 65% |
| **O4-KR4** | 7628430235122666701 | 6/30 验收标准 + 关键 Case | 6 月 | 60% |

## 项目线 → KR 启发式（打日报标签用）

| 项目线 / 信号 | 主 KR | 次 KR |
|---|---|---|
| 🅰️ Loona 交互规范 / 知识体系（konw-how / Loona-Spec / Know-How docx） | O3-KR2 | O3-KR3, O2-KR2 |
| 🅱️ Loona Protocol 工程验收（Jarvis：Cortex/Bridge/ToolHub/前端、209 case 真验收） | O4-KR4 | O2-KR3, O4-KR1, O3-KR1 |
| © rowboat（人性化收束层评测器 / 记忆回路 GSD / KB Lab / benchmark） | O2-KR3 | O3-KR1, O3-KR2, O4-KR4, O4-KR3 |
| Ⓓ Loona-Deskmate PRD 审查（应用管理 / 530 三线 MVP / 记忆 / Slack case） | O1-KR2 | O2-KR2, O4-KR1, O4-KR3 |
| Ⓔ 评测体系 / 测试集（本机评估目录、case 库、标注、Langfuse） | O4-KR1 | O3-KR1, O4-KR4 |
| Ⓕ AI workshop（多模态语音唤醒 demo / 声纹 / 判停） | O2-KR1 | O2-KR2, O2-KR3 |
| Ⓖ 入职认知（Week1 六步产出 / 黑话表 / 架构图） | O1-KR1 | — |
| Ⓗ 复盘体系 / skill / OKR / 周报 / 360 画像 / 反推映射 | O1-KR3 | O2-KR4 |
| Ⓘ 会议 / 周会 / 对齐（决策 + 分工） | 视主题 | O1-KR3 |
| Ⓙ Codex 多 agent 编排 / PRD 工具 / 能力探索 | O2-KR3 | O1-KR2, O2-KR1 |
| AI Jam / 知识库分享 / notebookLM 推广 | O3-KR2 | O1-KR1 |

## 写 OKR 进展记录（可选回填，仅用户同意后）

- 命令：`lark-cli okr +progress-create --target-type key_result --target-id <KRid> --progress-percent N --progress-status normal --content @block.json --source-title "<标题>" --source-url "<url>" --as user`
- 每个 KR 多条周记录、按周递增（`【W?·date】` 前缀），ramp 到 DDL-paced 目标。
- content 用 ContentBlock JSON（blocks 数组，2-3 段/条，专业且贴合实际）。
- progress-create 不改 headline `progress_rate`、不设 score。
- 已建脚本可复用：`.planning/redo_progress.py`（DDL-paced）+ `.planning/apply_progress.py real`（读 `.planning/progress/O{1-4}.json`）。
