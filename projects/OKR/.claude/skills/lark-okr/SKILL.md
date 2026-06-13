---
name: lark-okr
description: 飞书个人 OKR 副驾。读取/分析我的飞书 OKR（周期、目标、关键结果、进展），计算健康分与风险雷达，回答关于 OKR 的自然语言问题，并做对齐分析。后续支持把本地任务（Codex/Claude Code/浏览器/git）关联到 KR 并生成进展更新。当用户提到「我的 OKR」「OKR 进展」「这季度目标」「KR 风险」「更新 OKR」「OKR 健康/达成率/对齐」时使用。基于 lark-cli，始终以用户身份调用。
---

# lark-okr — 飞书个人 OKR 副驾

帮助秦宇龙（open_id `ou_9e35d4bb77a72e6180e8f54417ff0532`）管理飞书 OKR。全部通过 `lark-cli okr` 调用。

## 铁律

1. **始终带 `--as user`**。全局 default-as 是 `bot`，OKR 必须用户身份，否则报权限错。
2. **第一期只读，绝不写入**。`progress-create/update/delete`、`objectives/key_results` 的 create/patch/delete 在 P1 一律不调用。需要写时先升级到 P2/P3 流程（草稿→卡片审批→写回）。
3. **OKR 内容是富文本 block JSON，不是纯文本**。读到的 objective/KR `content` 必须用 `scripts/blocks.py parse` 转成可读文本再展示。详见 `references/content-format.md`。
4. **open_id 不要硬编码**——可用 `lark-cli auth status --format json` 取 `userOpenId`，以适配换号。

## 常用动作

### 1. 拉取并展示我的当前 OKR
- 列周期：`lark-cli okr +cycle-list --user-id <open_id> --as user --format json`
- 选**当前日期所属**周期（start_time ≤ 今天 ≤ end_time；时间戳为毫秒字符串）
- 读详情：`lark-cli okr +cycle-detail --cycle-id <id> --as user --format json`
- 用 `blocks.py parse` 解析每个 O / KR 的 content
- 树状展示：O（权重、score）→ 其下 KR（权重、score）；给出整体加权达成率

### 2. KR 健康分 + 风险雷达
对每条 KR 评估并解释：
- **时间进度 vs 完成进度**：今天在周期中的时间占比 vs score。落后越多越红。
- **是否有近期进展**：用 `+progress-list` 看最近进展记录时间；长期无更新预警。
- **权重**：高权重且停滞的优先标红。
风险分级：🔴高危 / 🟡注意 / 🟢正常。每条给一句"为什么"和"建议动作"。

### 3. 自然语言查询
先拉取归一化 OKR 数据，再回答，如「哪些 KR 要翻车」「最久没更新的 KR」「整体达成率多少」。

### 4. 公司 OKR 对齐分析（只读）
读用户指定的公司/上级 OKR 文档（`lark-cli docs +fetch` / `wiki` / `base` / `sheets`），分析我的 O 与之的对齐缺口。文档位置需用户提供。

## 脚本

- `scripts/blocks.py` — `parse`（block JSON→文本）/ `build`（文本→block JSON，P2 用）
- `scripts/okr_pull.py` — 拉取并归一化当前周期 OKR

## 参考

- `references/commands.md` — lark-cli okr 命令速查
- `references/content-format.md` — block JSON 规范
