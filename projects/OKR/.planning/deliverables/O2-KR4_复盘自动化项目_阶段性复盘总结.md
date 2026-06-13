# 复盘自动化 skill 项目 · 阶段性复盘总结

> **文档定位:阶段性复盘(项目仍在迭代)。** 本文按 O2-KR4 要求的五要素(场景问题 / 方案价值 / 验证结果 / 关键问题 / 下一步建议)对主线 AI 场景做一次完整收口。但需诚实标注:O2 主线项目目前**均仍在迭代**——复盘 skill 仍每日 cron 运行(无明确"结束"时点)、第二验证案例评测器已进 v1.3 记忆回路、配套 Jarvis Loona Protocol 仍在改 live bug。因此本文不是"项目末复盘",而是把现有里程碑级素材(4 月月报 + rowboat v1.2 归档 + 评测器成果展示 + OKR 反推映射表)聚合成单篇、按五要素结构化的**阶段性复盘**。
>
> **对应 KR**:O2-KR4「项目结束后输出复盘总结(场景问题/方案价值/验证结果/关键问题/下一步)」(KR id `7626271889488743624`)
> **所属 O**:O2「主导一个简单 AI 场景的验证闭环,证明具备小型 AI 项目独立推进能力」
> **主线场景 A**:个人复盘/日报自动化 skill(feishu-daily-review)
> **第二验证案例 B**:人性化收束层评测器(rowboat)
> **成文时间**:2026-05-24(Q2,W6) ｜ **覆盖时间窗**:2026-04-01 ~ 2026-05-24

---

## 一、场景问题(为什么做这个 AI 场景)

入职后从真实内部流程里识别出一个执行型、重复、可被 AI 替代的痛点,作为 O2 主线场景。

- **手动写日报/周报成本高、易漏**:每日工作横跨飞书会议、本地工程(Codex/Claude session)、GitHub 提交等多源,手工汇总既耗时又容易漏记关键产出。
- **OKR 与实际工作脱节**:产出大量落在本机(G 盘 + Claude/Codex session)和 GitHub,没有回填飞书 OKR 进展,导致 leader 侧"看不到 = 没发生"(此根因在 SYNTHESIS.md 中被明确点出)。
- **缺少结构化沉淀**:零散记录无法支撑"项目末复盘"这类按五要素结构化的输出,需要一个能持续把过程转成结构化复盘文档的机制。

场景定义最早成文于 **2026-04-02《飞书工作复盘 Agent PRD v2》**(本机 `docs\2026-04-02-feishu-work-retrospective-agent-prd-v2.md`),明确目标:把飞书工作过程转结构化复盘文档的个人沉淀 Agent。该场景完全契合 KR1 措辞"入职/需求变更整理或其他执行型流程",来自真实内部流程、执行型、本人独立识别。

---

## 二、方案价值(做了什么,解决了什么)

围绕主线场景构建了一套"三层复盘体系 + skill 化 + 自动化 + 结构化追踪"的闭环:

1. **三层复盘体系**:日复盘 → 周报 → 月报,逐层聚合,W1-W6 系统化运行。
2. **skill 化(daily-review skill,10 步)**:2026-04-27 从 0 到 1 建成 10 步 skill,把"采集多源工作记录 → 生成结构化复盘"固化为可复用流程。
3. **cron 自动化落地**:2026-04-30 把日报/多维表格维护拆成独立 cron(18:20 / 18:30 两个定时任务),实现每日无人值守自动产出。
4. **bitable 结构化追踪**:创建「复盘日历与状态追踪」多维表格 + OKR 四表,把复盘结果落成可查询、可追踪的结构化数据。
5. **GitHub 开源**:复盘 skill 于 W3 发布开源 —— **github.com/lala1137273514/feishu-daily-review**,可复用、可对外展示。
6. **第二验证案例(评测器)**:作为方案能力的横向延伸,在 rowboat 项目里建成人性化收束层评测器(两层评测:确定性指标 + LLM judge),验证了同一套"需求拆解→方案设计→工程落地"方法可迁移到评估类场景。

**解决了什么**:把"手工写复盘 + 易漏 + OKR 脱节"的痛点,转成"每日自动产出结构化复盘 + 可追踪 bitable + 可对外开源"的自动化闭环。本次按 OKR 反推映射做的逐条证据梳理本身,就是这套复盘机制产出的二阶产物。

---

## 三、验证结果(实际跑通的证据)

主线场景已不止"原型",而是**初步落地并持续运行**;第二案例已**真流量验证**。可量化处尽量量化:

| 证据 | 时间 | 量化/事实 | 链接/路径 |
|---|---|---|---|
| daily-review skill 0→1 建成 | 04-27 | 10 步;复盘日历 + OKR 四表创建 | [飞书日复盘](https://f4x6dn8llc.feishu.cn/docx/Ss5qd0NcMopPOSxY4ngclEkcnhh) |
| 拆独立 cron 定时运行 | 04-30 | 2 个 cron(18:20/18:30),每日自动跑 | [飞书日复盘](https://f4x6dn8llc.feishu.cn/docx/WRdPdrP4qox7E5xP7JycHg8tnMD) |
| 复盘 Skill 展示 + GitHub 发布 | W3(04-27~05-03) | 开源 github.com/lala1137273514/feishu-daily-review | [飞书周报](https://f4x6dn8llc.feishu.cn/docx/YVGfdUfIWouPvzxrj2ycworonKv) |
| 持续自动运行 | 04-02 起 / 5月多次 | Daily/Morning Feishu Retro 自动化运行记录(Codex 账本多次) | Codex 会话(W0-W5) |
| 三层复盘无断档 | W1-W6 | 4 月日/周/月报 15 份归档;周报 W1-W6 系统化(W1 早期 4/14-4/16 有标注缺口,其余无断档) | 飞书「个人复盘」文件夹 |
| 4 月个人月报 | 约4月初 | 入职首月四线冷启动(产品认知/评测/Wiki/复盘自动化从 0 到 1) | [飞书](https://f4x6dn8llc.feishu.cn/docx/GkRadP0gEoK3lExKjmlcNOq8nUf) |
| OKR 反推映射表 | 05-18 | 15 条 KR 逐条证据 + 覆盖率%,反推出硬缺口(复盘机制的二阶产物) | 本机 `OKR反推映射表.md` |
| 第二案例:评测器真流量验证 | 05-19 | Langfuse 真 trace 跑通;shuorenhua 66 条并入;results.jsonl 868→251 清理 | Claude 会话(W6) |
| 第二案例:rowboat v1.2 归档 | 05-18 | 「Knowledge Compounding」13 phase 全 shipped,513 测试,已打 tag `knowledge-compounding-v1.2` | Claude 会话(W6) |
| 评测器成果展示 | 约5月下 | 独立可跨 Agent 复用评测器 + ground-truth benchmark;事实门铁闸 + 人格评委 | [飞书](https://f4x6dn8llc.feishu.cn/docx/CdnJdNJlyo7tvDxiOMBcR1fbnoc) |

**小结**:主线 A 是 KR1→KR4 链条上**唯一真正"落地上线"**的一条(cron + GitHub + 持续运行);第二案例 B 提供真流量验证与里程碑级归档。KR3"原型验证/流程跑通/初步落地"三种结果全部命中。

---

## 四、关键问题(暴露的局限)

1. **双源未合并**:工作记录分两源——飞书侧(会议/日报)与本地侧(Codex/Claude session 工程产出)。当前复盘 skill 抓取偏飞书源,本地工程线(rowboat/Jarvis 等 session)未自动纳入日报,需人工补;两源需合并抓取才能完整。
2. **subagent 不继承 OAuth / scope 受限**:派发 subagent 各扫一源时不继承母会话 OAuth;且飞书 OAuth app 部分 scope 未启用(如 5/15 卡 `vc:reserve`、OKR scope 尚未启用),限制了自动化覆盖面。
3. **context 溢出**:单会话采集体量大(最大单会话达 19.5 MB / 88 MB 级仓库),长链路复盘易触发 context 溢出,需分源/分会话切分处理。
4. **OKR 回填未自动化**:复盘产出未自动回填飞书 OKR 进展记录,目前靠人工(本次反推映射即为补救),"看不到 = 没发生"的根因尚未从机制上闭环。
5. **五要素此前分散、未成单文**:在本文之前,五要素分散在 v1.2 归档 / 月报 / 反推映射表 / 评测器成果展示多份文档中,缺一份按 KR4 结构化的单篇主线复盘(本文即为补齐)。
6. **"项目末"时点不存在**:主线项目仍在迭代,严格意义的"项目结束后复盘"尚无时点,故只能做阶段性复盘。
7. **协作维度偏弱**:主线 A 是个人独立落地,协作方参与较弱(主要自驱 + 工具链);协作面更多体现在第二案例 B 与 Jarvis 的研发对接上。

---

## 五、下一步建议

1. **OKR 进展自动回填**:启用飞书 OKR scope,把复盘 skill 产出的 KR 进展自动写回飞书 OKR(score + 进展记录),从机制上消除"看不到 = 没发生"。
2. **双源合并抓取**:把本地工程线(Codex/Claude session、GitHub 提交)纳入日报采集,与飞书源合并,产出真正全口径的每日复盘。
3. **本地工程线纳入日报**:把 rowboat/Jarvis 等本地仓库的当日产出(commit、phase shipped、测试结果)结构化进日报,补齐当前偏飞书源的盲区。
4. **解决 subagent OAuth / context**:为多源采集设计可继承凭证的执行方式,并按源分会话切分以规避 context 溢出。
5. **待项目收口后产出正式"项目末复盘"**:当主线 skill / 评测器迭代收口、出现明确结束时点时,在本文基础上升级为正式项目末复盘总结。
6. **同步飞书提升可见性**:把本文同步至飞书「个人复盘」文件夹,作为 O2-KR4 的可指向交付物。

---

## 附:证据链接索引

- 主线场景定义 PRD v2:本机 `docs\2026-04-02-feishu-work-retrospective-agent-prd-v2.md`
- GitHub 开源:https://github.com/lala1137273514/feishu-daily-review
- 4 月个人月报:https://f4x6dn8llc.feishu.cn/docx/GkRadP0gEoK3lExKjmlcNOq8nUf
- 04-27 daily-review skill 建成:https://f4x6dn8llc.feishu.cn/docx/Ss5qd0NcMopPOSxY4ngclEkcnhh
- 04-30 拆 cron 落地:https://f4x6dn8llc.feishu.cn/docx/WRdPdrP4qox7E5xP7JycHg8tnMD
- W3 周报(复盘 Skill 展示 + GitHub 发布):https://f4x6dn8llc.feishu.cn/docx/YVGfdUfIWouPvzxrj2ycworonKv
- 人性化收束层评测器成果展示:https://f4x6dn8llc.feishu.cn/docx/CdnJdNJlyo7tvDxiOMBcR1fbnoc
- 05-18 全量 OKR 进展梳理日报:https://f4x6dn8llc.feishu.cn/docx/F4nfdN81poj4A4xkgLSc0Wz3n8b
- OKR 反推映射表:本机 `OKR反推映射表.md`;反推-映射分析:本机 `.planning\kr\O2-KR1~KR4.md`
- 复盘日历追踪 bitable:`EdlPbzsTwaMgANspA1mcbs6ynxe`
