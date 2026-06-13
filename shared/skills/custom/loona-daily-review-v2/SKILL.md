---
name: loona-daily-review-v2
description: >
  三源合并日报/周报生成器（牛马一号·升级版）。在「飞书侧记会议」之外补回「本地工程线」
  （Claude/Codex session + git commit），按项目线归并三源、自动给每条成果打 OKR KR 标签，
  按 6 节日报 / 7 节周报结构输出，可选回填飞书文档与 OKR 进展记录。
  当用户说"写日报/周报""复盘""三源合并""补回工程线""回填 OKR"时使用。
metadata:
  type: workflow
  author: 秦宇龙
  upstream: feishu-daily-review (牛马一号 / GitHub cron 版)
  backbone: lark-cli (--as user)
---

# loona-daily-review-v2 — 三源合并日报/周报

> 这是 cron 版日报 skill「牛马一号」(GitHub `feishu-daily-review`) 的升级版。
> 旧版只抓飞书侧（日程/会议/文档），**漏掉了本地工程线**（Jarvis/rowboat/Loona-Spec/Codex 等
> 真正的代码与方案产出）。本版新增三件事：
> ① **本地工程线**（扫 Claude/Codex session + git commit）；
> ② **KR 下沉**（每条成果带 `【O?-KR?】` 标签，14 个 KR 见 `reference/kr-map.md`）；
> ③ **数据源覆盖标注**（暴露盲区：✅飞书 / ✅本地 / ⚪Codex / ⚠️IM）。

## 何时用

- 写**今日/某日日报**（默认当天，可传日期）。
- 写**本周/某周周报**。
- **回填**历史日报/周报到本地（不动飞书已有文档）。

## 核心原则（务必遵守）

1. **三源合并，不偏废**：飞书（会议/日程/文档）+ 本地 Claude/Codex session + git commit，
   按**项目线**归并，同一天同一项目的三源证据合到一条。旧日报最大的病是只记会议、漏掉工程——本版必须把工程线补回。
2. **会议读纪要原文，不靠日报摘要**：飞书日报把会议压成一句话，信息损失大。
   关键会议要读 `智能纪要：<topic>` / `文字记录：<topic>` docx 原文（见 `reference/feishu-pull.md`）。
3. **每条成果打 KR 标签**：动作 + 产出 + 量化 + 📎链接 + `【O?-KR?】`。映射规则见 `reference/kr-map.md`。
4. **进度按 DDL 节奏，状态恒为 normal**：写 OKR 进展时遵守用户偏好——百分比由 KR 的有效 DDL 决定
   （已过期→100% / 5月底→80% / 6/30→60-75%），**永不写"逾期/overdue"**，状态一律 `normal`。
5. **红线：不动飞书已有日报**。回填只写本地文件。是否同步飞书由用户拍板。
6. **诚实**：没有证据的成果不编。当日无某源 → 在第 6 节如实标 ⚪/⚠️ 并暴露盲区。
7. **落文档前必过双质检（强制）**：周报/日报/OKR 文案在写本地或回填飞书**之前**，必须先过一遍
   `shuorenhua` skill（去 AI 套路、说人话）再过 `jianbo-review` skill（模拟评审人 8 把尺子预审），
   按两者反馈修改优化后才允许落文档。详见工作流 **C+**。

## 工作流

### A. 采集（三源）

1. **飞书源** —— 用 `lark-cli ... --as user`，命令清单见 `reference/feishu-pull.md`：
   - 当天日程：`lark-cli calendar +agenda --as user`
   - 个人复盘 / 会议纪要 docx：列「个人复盘」文件夹 + 根目录，按日期取 `智能纪要：*` / `*个人日复盘`。
   - 读 docx 原文：`lark-cli docs +fetch --api-version v2 --doc <token> --format pretty`（去 HTML 标签）。
2. **本地源** —— 跑 `scripts/scan_local.py <YYYY-MM-DD>`：
   - 扫 `C:\Users\QYL\.claude\projects\**\*.jsonl`（按 mtime 命中当天，排除 `subagents/`），
     提取每会话首条用户意图 + 关键产出，按项目目录归类。
   - 扫 `C:\Users\QYL\.codex\sessions\2026\MM\DD\rollout-*.jsonl`，取首条 `user_message`。
   - 扫 git：对已知工程仓（Jarvis/rowboat/Cortex/ToolHub 等）跑 `git log --since/--until --oneline`。
   - 大文件**流式读**，先 `export PYTHONIOENCODING=utf-8 PYTHONUTF8=1`。
3. **历史回填模式**：若在做 Q2 回填，**优先读已建账本** `.planning/ledger/{feishu,local,claude,codex}.md`
   （已按周/日时间戳化采集好），按当天行取证据，必要时再回原始 session 补细节。

### B. 归并 + 打标签

- 按**项目线**聚合（🅰️ Loona交互规范/知识体系、🅱️ Loona Protocol工程(Jarvis)、
  © rowboat 评测器/记忆回路、Ⓓ Loona-Deskmate PRD、Ⓔ 评测体系/测试集、Ⓕ 复盘体系/AI赋能 等）。
- 每条用 `reference/kr-map.md` 的"项目线→KR"启发式打 `【O?-KR?】`（可多 KR）。
- 三源去重：同一成果在飞书 doc + 本地 session 都出现时合一条，链接都挂上。

### C. 输出结构

- **日报 6 节** / **周报 7 节**：模板见 `reference/structure.md`，**严格照抄结构**。
- 写到：日报 `→ .planning/dailies-v2/YYYY-MM-DD.md`；周报 `→ .planning/weeklies-v2/W{n}-{起}~{止}.md`
  （回填模式）；当天实时模式可直接产出正文供用户审阅 / 写飞书。

### C+. 落文档前双质检（强制，不可跳过）

生成正文后、写本地文件或回填飞书**之前**，按顺序过两道质检并据反馈修改：

1. **`shuorenhua` skill —— 去 AI 味**：把周报/日报正文 + OKR 进展 content 过一遍，清掉 AI 套路、
   空话套话、模板腔，控制力度（保留事实、术语、数字、链接、责任主体）。把"体验良好/性能优化/赋能"
   这类空词换成可观察的具体陈述。
2. **`jianbo-review` skill —— 模拟评审预审**：用 Jianbo 的 8 把尺子（人味/主动/形式/信息完备/
   个性化/出结果/准确/覆盖）预审，标〔还原〕/〔推测〕。重点抓：成果是否 over-claim、量化是否站得住、
   KR 标签是否对得上、叙事是否程序化。
3. **据反馈修改优化**：两道质检的问题逐条改进正文，改完才进入 C 落文档 / D 回填。

> 红线：未过双质检不得 `docs +create/update`、不得 `okr +progress-create`。

### D.（可选）回填飞书 / OKR

- **仅在用户明确同意后**写飞书。命令见 `reference/feishu-pull.md` 的"写"段。
- 写 OKR 进展：`lark-cli okr +progress-create --target-type key_result --target-id <KRid>
  --progress-percent N --progress-status normal --content @block.json ... --as user`。
  规则见原则 4 + `reference/kr-map.md`。**注意**：progress-create 只加时间线记录，不改 KR headline
  `progress_rate`（UI 自行从最新记录推导），也不设 score。
- 复盘日历 bitable 写入用 `api POST .../records/batch_*`；**读**记录必须用
  `lark-cli base +record-list --base-token <app> --table-id <tbl> --as user`（GET 被限权会误判空表→造重复）。

## Cron 兼容（牛马一号节奏）

旧版 cron：**18:20 日报 / 18:30 bitable / 22:00 周报**。本版保持兼容：
- 18:20 触发 → 走"A 采集 + B 归并 + C 日报"，落本地 + （配置开则）写飞书当日复盘 docx。
- 18:30 → 复盘日历 bitable 更新（先 record-list 读，verify-before-write）。
- 22:00（周五/周日）→ 周报，落 `.planning/weeklies-v2/`。
本地工程线扫描（scan_local.py）插在采集阶段，相对旧版纯飞书是增量、不破坏原 cron 产物。

## 关键 gotchas（必读）

- lark-cli 所有命令加 `--as user`（全局默认 as=bot）。
- Bash 调 `/open-apis` 路径前 `export MSYS_NO_PATHCONV=1`，否则路径被 Git Bash 破坏。
- 读 bitable 记录用 `base +record-list`，**别**用 `api GET .../records`（限权→假空表→重复写）。
- 读 jsonl 先 `export PYTHONIOENCODING=utf-8 PYTHONUTF8=1`，大文件流式、别整读。
- 写飞书 docx：`docs +create --api-version v2 --doc-format markdown --content @相对路径.md --parent-token <folder>`（先 cd 到目录，只能相对路径）。
- 飞书 folder：个人复盘 `U0H3fNGXol8I2EdYfXwccLNxnRe`；Q2 周期 `7622051252293749950`；open_id `ou_9e35d4bb77a72e6180e8f54417ff0532`。
