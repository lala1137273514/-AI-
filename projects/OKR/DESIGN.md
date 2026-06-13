# 飞书 OKR Skill 设计文档（DESIGN.md）

> 单一事实源。定稿后据此搭建。最后更新：2026-05-22

---

## 1. 目标与定位

一个 Claude Code skill（暂名 **`lark-okr`**），把"飞书 OKR"和"我的本地工作"打通：

1. **增删改查**飞书 OKR（O / KR / 进展记录 / 对齐 / 指标）
2. 结合**本地任务**（Codex / Claude Code 会话、新增文档、浏览器记录、git）关联到对应 KR，自动生成**进展更新内容与产出物**
3. **自动执行**：交互式（喊一句就跑）+ 定时（无人值守生成草稿待审）
4. 结合**公司 OKR 文档**做实时分析（对齐、风险、复盘）

定位：**个人 OKR 副驾**（personal OKR copilot），第一人称视角。

---

## 2. 锁定的关键决策

| 决策 | 结论 | 理由 |
|------|------|------|
| 身份 | **纯用户身份**（`--as user`，秦宇龙） | OKR 是个人数据；写操作必须挂在本人名下；全局 default-as 是 `bot`，故每次调用**显式带 `--as user`** |
| 服务范围 | **只管自己的 OKR** | 不预留 tenant 只读层，架构最简；将来要看团队再扩 |
| 调用方式 | **全部走 lark-cli**，不裸调 HTTP API | 已认证、有 schema、官方维护 |
| 第一期范围 | **读 + 查询分析（零写入）** | 先建立信任与价值，写入风险后置 |
| 写入策略（二期起） | **草稿 → 卡片审批 → 写回**，永不静默写 | OKR 是正式数据，必须人确认 |

---

## 3. 权限与环境现状（已验证 2026-05-22）

- lark-cli **v1.0.38**，已登录用户 **秦宇龙**（open_id `ou_9e35d4bb77a72e6180e8f54417ff0532`），app `cli_a941969bd53a1bdd`
- **OKR 8 个 scope 全部开通并授予用户 token**（叠加，未影响原有 162 个）：
  - `okr:okr.period:readonly` 周期 ｜ `okr:okr.content:readonly/writeonly` 读写 O·KR
  - `okr:okr.setting:read` 设置 ｜ `okr:okr.progress:readonly/writeonly/delete` 进展记录 ｜ `okr:okr.progress.file:upload` 配图
- 其它已开通且本 skill 会用到：`base`(多维表格暂存) `docs/docx/wiki`(公司文档) `im`(推送) `cardkit`(审批卡片) `event`(实时触发) `task`
- 当前 Q2 周期 `7622051252293749950`（2026-04-01~06-30），4 Objectives / 14 KRs，进度全 0

---

## 4. 架构总览

```
┌─ 输入层 / 信号采集（本地，无需飞书权限）──────────────────┐
│  Codex     C:\Users\QYL\.codex\sessions\rollout-*.jsonl    │
│  Claude    C:\Users\QYL\.claude\projects\* / tasks\*       │
│  浏览器     Edge History (SQLite，需先复制再读)             │
│  git        commits / PR（如有仓库）                       │
└────────────────────────────────────────────────────────────┘
                    ↓  归一化为 Signal{时间, 来源, 标题, 摘要, 产出物链接}
┌─ 关联引擎（LLM）─────────────────────────────────────────┐
│  Signal → 最相关 KR（语义匹配 + 置信度 0~1 + 理由）        │
│  低于阈值 → 标"未关联"，不硬塞                              │
└────────────────────────────────────────────────────────────┘
                    ↓
┌─ 飞书层（lark-cli，全部 --as user）──────────────────────┐
│  读：cycle-list / cycle-detail / progress-list             │
│  写[二期]：progress-create/update/delete + upload-image    │
│           objectives/key_results create/patch/delete       │
│  公司文档：docs / wiki / base / sheets                     │
│  推送：im（周报/预警）   审批：cardkit（卡片确认后写回）   │
│  暂存兜底：base 多维表格（草稿先落表）                     │
└────────────────────────────────────────────────────────────┘
                    ↓
┌─ 执行层 ─────────────────────────────────────────────────┐
│  交互式：用户在 Claude Code 里触发                          │
│  定时[三期]：event 触发 / 计划任务，生成草稿 → im 待审      │
└────────────────────────────────────────────────────────────┘
```

---

## 5. lark-cli 命令映射

### 读（第一期，已验证 ✅）
| 用途 | 命令 |
|------|------|
| 列周期 | `lark-cli okr +cycle-list --user-id <open_id> --as user` |
| 读周期内 O/KR | `lark-cli okr +cycle-detail --cycle-id <id> --as user` |
| 读某 O/KR 进展 | `lark-cli okr +progress-list ... --as user` |
| 读公司文档 | `lark-cli docs +fetch ...` / `wiki` / `base` / `sheets` |

### 写（第二期起，命令已存在，参数待用 `--dry-run` 核对）
| 用途 | 命令 |
|------|------|
| 新建/更新/删除进展 | `okr +progress-create / +progress-update / +progress-delete` |
| 进展配图 | `okr +upload-image` |
| 增删改 O/KR | `okr objectives|key_results create/patch/delete`（scope `content:writeonly`） |

### 推送 / 审批
| 用途 | 命令 |
|------|------|
| 发周报/预警 | `lark-cli im ...`（发给本人） |
| 交互审批卡片 | `lark-cli`（cardkit）|

---

## 6. 数据格式（关键实现细节）

OKR 的 O / KR / 进展**内容是飞书富文本 block JSON**，非纯文本：
```json
{"blocks":[{"block_element_type":"paragraph","paragraph":{"elements":[
  {"paragraph_element_type":"textRun","text_run":{"text":"...","style":{}}}]}}]}
```
- **读**：写一个 `parse_blocks()` 把 block JSON → 纯文本 / Markdown
- **写**：写一个 `build_blocks(text)` 把纯文本 → block JSON
- 两个函数放 `scripts/`，所有读写都经过它，避免散落。

---

## 7. 第一期详细范围（读 + 查询分析，零写入）

交付以下命令式能力（skill 内的"动作"）：

1. **拉取我的当前 OKR**：自动选当前日期所属周期 → cycle-detail → 解析成可读结构（O、KR、权重、score）
2. **OKR 总览**：树状展示 4 个 O / 14 个 KR、权重、当前进度、整体加权达成率
3. **KR 健康分**：每条 KR 按"进度 vs 时间进度 / 是否有近期进展 / 置信度"打分并解释扣分点
4. **风险雷达**：标出 ①长期无进展 ②临近周期末仍低进度 ③权重高但停滞 的 KR
5. **自然语言查询**：如"这季度哪些 KR 要翻车？""哪条 KR 最久没更新？"
6. **公司 OKR 对齐分析（只读）**：读指定公司/上级 OKR 文档（docs/wiki/base）→ 分析我的 O 与之的对齐缺口

> 第一期**不采集本地信号、不写任何飞书数据**。先把"看得清"做扎实。

---

## 8. 分期路线

| 期 | 范围 | 依赖 |
|----|------|------|
| **P1** 读+分析 | 第 7 节全部 | 已就绪 ✅ |
| **P2** 信号→进展草稿 | 采集 Codex/Claude/Edge/git → 关联 KR → 生成进展草稿 → **base 暂存** | block 构造、信号解析 |
| **P3** 审批写回 | cardkit 卡片确认 → `progress-create` 写回 OKR + 配图；O/KR 增删改 | P2 |
| **P4** 自动化 | event 触发 / 计划任务；周报 & 风险预警自动 im 推送 | P3 |

---

## 9. Skill 目录结构（拟）

```
.claude/skills/lark-okr/
  SKILL.md                 # 指令：何时用、如何用 lark-cli、调用约定（--as user）
  references/
    commands.md            # lark-cli okr 命令速查（已验证的读 + 待验证的写）
    content-format.md      # block JSON 解析/构造规范
    signals.md             # 本地信号源路径与解析方式（P2）
  scripts/
    okr_pull.(py|ps1)      # 拉取并归一化当前周期 OKR → JSON
    blocks.(py)            # parse_blocks / build_blocks
    okr_health.(py)        # 健康分 + 风险雷达
    signals_collect.(py)   # P2：采集本地信号
```
- 参考已安装的 `lark-skill-maker` 和 `lark-base` 等官方 skill 的写法。

---

## 10. 待确认 / 风险

- [ ] 写入接口（progress-create / objectives.patch）的**精确参数与 content 字段格式**——P2 启动时用 `--dry-run` 核对（本次因分类器临时不可用未抓全）
- [ ] 公司/上级 OKR 文档的**具体位置**（哪个 docs/wiki/base）——做对齐分析前需你提供
- [ ] 定时自动化的**承载方式**：Claude 定时任务 vs n8n vs Windows 计划任务——P4 再定
- [ ] 用户 token 刷新期：长期无人值守需注意（至少每数天跑一次即自动续）

---

## 11. 下一步

定稿本文档后，进入 **P1 实现**：先建 skill 骨架 + `okr_pull` + `blocks` 解析 + 总览/健康分/风险雷达，用你真实的 Q2 OKR 跑通。
```
