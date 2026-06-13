# Card Schemas / 卡片字段 Schema

> This file is the **field-level contract** for the four card types across Loona's travel-planning flow. It defines每个字段的名称、类型、长度约束、说明，并为每个需生成的字段配「字段生成提示词」(喂什么输入 → 吐哪个字段 → 风格/长度约束)。
>
> **何时读 / When to read:** 在生成或校验任意一类卡片（ClarifyCard / InspoFlow / TravelView / ListCard）之前必读；改字段、对前端字段、写生成提示词时以本文件为准。TravelView 部分的字段约束与 cortex `compose_trip.yaml` 对齐，二者冲突以 cortex 线上为准。
>
> **设备前提 / Device:** Loona 是语音优先、手机大小小屏的硬件桌宠。卡片一次只承载一个焦点，口播(TTS)是主线，卡片是辅助。

---

## 0. 全局口播/文案硬约束 (Voice & Copy Hard Rules)

适用于所有口播/文案类字段：`punchline`、`summary`、`reminder`（以及任何喂给 TTS 或展示给用户读的句子）。Applies to all spoken/copy fields.

| 规则 CN | Rule EN |
|---|---|
| 一句话 ≤25 全角字，能断句就断 | One sentence ≤25 full-width chars; break it up when you can |
| 禁书面词：为您 / 兼具 / 值得 / 不妨 / 堪称 / 打造 / 沉浸 | Ban written-register words: 为您, 兼具, 值得, 不妨, 堪称, 打造, 沉浸 |
| 禁排比三连 + 破折号抒情 | No rule-of-three parallelism; no em-dash lyrical asides |
| 用「你」不用「您」 | Use 你, never 您 |
| 主动收尾，不用反问句结尾 | End on a statement, never a rhetorical question |

> 去 AI 味的判断标准：读出来像真人朋友随口说，不像稿子。详略上只给亮点，不堆信息。屏幕上能看到的内容，口播不复述。

---

## 1. ClarifyCard 澄清卡

方案生成前的澄清环节产出，最多 3 轮。结构是 `understand:{known:[], memory:[]}`。
Produced in the clarification step before solution generation; up to 3 rounds.

### 字段表 / Fields

| 字段 Field | 类型 Type | 长度约束 Length | 说明 CN | Description EN |
|---|---|---|---|---|
| `understand` | object | — | 容器，含 known 与 memory 两个数组 | Container holding `known` and `memory` arrays |
| `understand.known` | string[] | 每条 ≤8 全角字 / ≤8 full-width chars each | 用户**已明确确认**的短语标签（目的地、天数、人员等） | Short phrase tags the user has **explicitly confirmed** (destination, days, party) |
| `understand.memory` | string[] | 每条 ≤8 全角字 / ≤8 full-width chars each | 从**记忆/历史对话推断**的短语标签，未经用户当面确认 | Short phrase tags **inferred from memory/prior dialogue**, not freshly confirmed |

> 约定：known 与 memory 都是短词标签，不是整句；总数建议 2-5 条，不堆砌。known 优先于 memory，同一信息不重复出现在两个数组。

### 字段生成提示词 / Field-generation prompts

**`understand.known`**
- 输入 Input：本轮及之前用户**亲口确认**的旅行要素。
- 输出 Output：短语标签数组，每条 ≤8 全角字（如「成都」「5 天」「带老人」）。
- 风格 Style：名词性短词，不带句号，不带语气词；只放用户确认过的，拿不准就别放进 known。
- EN：Array of noun-phrase tags, ≤8 full-width chars each, no punctuation; only what the user actually confirmed.

**`understand.memory`**
- 输入 Input：从用户画像/历史会话中**推断**的相关偏好（去过哪、口味、节奏偏好等）。
- 输出 Output：短语标签数组，每条 ≤8 全角字（如「爱吃辣」「偏慢节奏」）。
- 风格 Style：同 known 的短词格式；这是「我记得你…」的料，用于让澄清更像人，但要可被用户否认。不放进 known 的高置信项才放这里。
- EN：Same short-tag format; inferred prefs that make clarification feel personal yet deniable. Items not confident enough for `known`.

---

## 2. InspoFlow 方案卡

方案生成环节产出，固定 **3 张**。结构 `{id, rec, title, photo, tags, punchline}`。
Produced in the solution-generation step; exactly **3 cards**.

### 字段表 / Fields

| 字段 Field | 类型 Type | 长度约束 Length | 说明 CN | Description EN |
|---|---|---|---|---|
| `id` | string | — | 卡片唯一标识 | Unique card id |
| `rec` | boolean | — | 是否主推（3 张中恰好 1 张为 true） | Recommended flag (exactly one of the 3 is true) |
| `title` | string | ≤14 全角字 / ≤14 full-width chars | 方案标题 | Solution title |
| `photo` | string \| null | — | 封面图 URL，须历史可信图，无则 null | Cover image URL (trusted历史 image), null if none |
| `tags` | string[] | 2-4 个短词 / 2–4 short words | 方案特征标签 | Feature tags for the solution |
| `punchline` | string | 口播句，遵全局口播约束 / spoken, see §0 | 该卡的口播 | The card's spoken line |

> 约定：3 张里恰好 1 张 `rec:true`；`photo` 禁编图，没有可信图就 null（前端走占位）。

### 字段生成提示词 / Field-generation prompts

**`rec`**
- 输入 Input：3 个候选方案 + 用户已知偏好(known/memory)。
- 输出 Output：布尔。最贴合用户偏好的那张设 true，其余 false。有且仅有一张 true。
- EN：Boolean; the single best-fit card is true, the rest false.

**`title`**
- 输入 Input：该方案的核心卖点/主题。
- 输出 Output：≤14 全角字的标题。
- 风格 Style：具体、有画面，不用空泛大词；不带书名号引号。
- EN：≤14 full-width chars; concrete and vivid, no vague big words, no brackets.

**`photo`**
- 输入 Input：方案对应的历史可信图库。
- 输出 Output：图 URL 或 null。
- 风格 Style：只用已有可信图；没有就 null，禁编造 URL。
- EN：Existing trusted image URL, or null. Never fabricate a URL.

**`tags`**
- 输入 Input：方案的节奏/主题/适配人群等特征。
- 输出 Output：2-4 个短词数组（如「轻松」「亲子」「美食」）。
- 风格 Style：每个 ≤4 全角字，名词或形容词短词，互不重复。
- EN：2–4 short words, each ≤4 full-width chars, distinct.

**`punchline`**
- 输入 Input：该方案最打动人的一个点 + 用户偏好。
- 输出 Output：1-2 句口播，整体读起来像朋友推荐。
- 风格 Style：遵 §0 全局口播约束（≤25 字/句、禁书面词、用「你」、主动收尾）；只说这张最心动的一个画面，不复述 tags。
- EN：1–2 spoken sentences per §0; sell one heart-moving image, don't restate tags.

---

## 3. TravelView 日程卡

出日程环节产出，复用 cortex `compose_trip` 的 `stages`。结构 `{label, pace, summary, photo, nodes, reminder}`。
Produced in the itinerary step; reuses cortex `compose_trip` `stages`.

> **来自 cortex compose_trip 的硬约束（照搬关键点）：**
> - 输出严格 JSON，**无缩进无换行**。`stages` 非空且**最多 5 张**，按旅行顺序。`nodes` 非空。
> - `photo` 只用历史已有可信图 URL，没有 = null，**禁编图**。
> - 前端**最多显示前 4 个 node**。

### 字段表 / Fields

| 字段 Field | 类型 Type | 长度约束 Length | 说明 CN | Description EN |
|---|---|---|---|---|
| `label` | string | ≤18 全角字 / ≤18 full-width chars | 「日期/天序 · 主题」 | "date/day · theme" |
| `pace` | enum | light \| normal \| intense | 当天节奏，默认 normal | Day pace, default normal |
| `summary` | string | 约 4 句 / 90-125 全角字 | TTS 口播，每张换结构 | TTS spoken line, vary structure per card |
| `photo` | string \| null | — | 历史可信图 URL，无则 null | Trusted历史 image URL, null if none |
| `nodes` | object[] | 非空；前端显前 4 / non-empty, front shows first 4 | 当天节点 | Day's nodes |
| `nodes[].time` | string | 单天完整天：上午/中午/下午/晚上 四档 | 时段 | Time slot |
| `nodes[].place` | string | ≤14 全角字 / ≤14 full-width chars | 地点 | Place |
| `nodes[].note` | string | ≤42 全角字（推荐 26-34）/ ≤42 (rec 26–34) | 怎么玩 + 一个亮点，两小句 | How-to-play + one highlight, two clauses |
| `reminder` | string | ≤22 全角字 / ≤22 full-width chars | 像朋友叮嘱的一句提醒 | One friend-style reminder |

### 字段生成提示词 / Field-generation prompts

**`label`**
- 输入 Input：该 stage 的日期(或天序) + 主题。
- 输出 Output：「日期/天序 · 主题」，≤18 全角字。
- 风格 Style：有具体日期用「6/1 · 主题」；无日期：单天用「Day N · 主题」，多天用「Day 起-止 · 主题」。
- EN："date/day · theme", ≤18 full-width chars. With a date → "6/1 · theme"; without → "Day N · theme" (single day) / "Day start-end · theme" (multi-day).

**`pace`**
- 输入 Input：当天节点密度 + 人员构成(是否含老人/婴幼儿) + 是否到达/返程日。
- 输出 Output：light / normal / intense，默认 normal。
- 风格 Style：到达日、返程日设 light；含老人/婴幼儿**禁 intense**。
- EN：light/normal/intense, default normal. Arrival/return day → light. Party with elderly/infant → never intense.

**`summary`**
- 输入 Input：当天 nodes 的玩法与亮点。
- 输出 Output：约 4 句、90-125 全角字的 TTS 口播。
- 风格 Style：遵 §0；每张卡换着结构来，**禁套同一模板**；去 AI 味，像人随口说；屏幕能看到的(nodes)不逐条复述，只串亮点。
- EN：~4 sentences, 90–125 full-width chars per §0. Vary structure every card, no template. Don't recap nodes verbatim; thread the highlights.

**`photo`**
- 输入 Input：该 stage 对应的历史可信图库。
- 输出 Output：图 URL 或 null。
- 风格 Style：只用已有可信图，禁编图。
- EN：Existing trusted URL or null. Never fabricate.

**`nodes[].time`**
- 输入 Input：节点在当天的时间段 + 当天类型(完整天/到达日/返程日)。
- 输出 Output：时段字符串。
- 风格 Style：**单天完整天**只能用「上午/中午/下午/晚上」四档且**必须铺满 4 个**；**到达日**按到达时段铺(中午到→3 个/下午到→2 个/晚上到→1 个)；**返程日**排 2-3 个且**禁排晚上**。
- EN：Single full day → only the four slots上午/中午/下午/晚上, must fill all 4. Arrival day → fill by arrival (noon→3 / afternoon→2 / evening→1). Return day → 2–3 nodes, never evening.

**`nodes[].place`**
- 输入 Input：节点的具体地点名。
- 输出 Output：≤14 全角字的地点名。
- 风格 Style：用通俗易认的名字，不堆全称。
- EN：≤14 full-width chars; common, recognizable name.

**`nodes[].note`**
- 输入 Input：该地点怎么玩 + 一个具体亮点。
- 输出 Output：≤42 全角字(推荐 26-34)，结构「怎么玩 + 一个亮点」两小句。
- 风格 Style：**禁泛词**(漫步/感受/韵味)，**禁堆信息**；给具体能做的事和一个让人心动的细节。
- EN：≤42 full-width chars (rec 26–34), "how-to-play + one highlight" in two clauses. No vague words (漫步/感受/韵味), no info dumping.

**`reminder`**
- 输入 Input：当天最要紧的**一件**实操注意事项。
- 输出 Output：≤22 全角字，像朋友叮嘱。
- 风格 Style：说人话(「记得先约，去晚排长队」)，**禁报告腔**(需提前预约/建议携带)；只说一件最要紧的事；遵 §0。
- EN：≤22 full-width chars, friend-style ("记得先约,去晚排长队"). No report tone (需提前预约/建议携带). One most-important thing only; per §0.

---

## 4. ListCard 收尾日程卡

收尾环节产出，复用 `list_events` 工具结构。结构 `{source_tool_name, rows}`。
Produced in the wrap-up step, reusing the `list_events` tool shape.

### 字段表 / Fields

| 字段 Field | 类型 Type | 长度约束 Length | 说明 CN | Description EN |
|---|---|---|---|---|
| `source_tool_name` | string | 固定 `'list_events'` / literal | 来源工具名 | Source tool name |
| `rows` | object[] | — | 日程条目数组 | Schedule rows |
| `rows[].title` | string | ≤14 全角字 / ≤14 full-width chars | 条目标题 | Row title |
| `rows[].sub` | string | ≤18 全角字 / ≤18 full-width chars | 副标题/补充 | Subtitle |
| `rows[].lead` | string | ≤22 全角字 / ≤22 full-width chars | 引导/提示语 | Lead line |
| `rows[].raw_start` | string | ISO 时间戳 / ISO timestamp | 起始时间原值 | Raw start time |
| `rows[].event_date` | string | 日期，如 6/1 / date | 展示用日期 | Display date |

> 约定：`source_tool_name` 恒为 `'list_events'`，前端据此走列表渲染。这是「收尾日程卡」非「结果卡」，呈现的是已排进日程的安排，不是规划结果。

### 字段生成提示词 / Field-generation prompts

**`source_tool_name`**
- 固定输出字符串 `'list_events'`，不生成。Literal `'list_events'`, not generated.

**`rows[].title`**
- 输入 Input：该条日程的核心事项。
- 输出 Output：≤14 全角字标题。
- 风格 Style：具体到「做什么」，不空泛。
- EN：≤14 full-width chars; concrete action.

**`rows[].sub`**
- 输入 Input：该条的时间/地点等补充。
- 输出 Output：≤18 全角字副标题。
- 风格 Style：补关键信息，不重复 title。
- EN：≤18 full-width chars; key supplement, no repeat of title.

**`rows[].lead`**
- 输入 Input：该条要给用户的一句提示。
- 输出 Output：≤22 全角字引导语，遵 §0。
- 风格 Style：像朋友提醒，主动收尾。
- EN：≤22 full-width chars, friend-style per §0.

**`rows[].raw_start` / `rows[].event_date`**
- 输入 Input：该条日程的真实时间。
- 输出 Output：`raw_start` = ISO 时间戳；`event_date` = 展示日期(如 6/1)。
- 风格 Style：取真实时间，禁编造；二者指向同一时刻。
- EN：`raw_start` = ISO timestamp, `event_date` = display date (e.g. 6/1); from real time, never fabricated, same moment.

---

## 5. 全链路卡片出现顺序 / Card Flow

```
ClarifyCard ×3 轮          InspoFlow ×3 张           TravelView 日程            ListCard 收尾
(澄清, ≤3 rounds)   →     (方案, exactly 3)   →     (出日程, stages≤5)   →    (wrap-up, list_events)

[understand:           [rec / title /          [label / pace /           [source_tool_name:
  known[] /             photo / tags[] /        summary / photo /          'list_events',
  memory[]]             punchline]              nodes[] / reminder]        rows[]]
   语音逐轮确认            主推 1 张, 横滑选        大图+口播驱动钻取           已排进日程的收尾列表
```

| 阶段 Stage | 卡片 Card | 数量 Count | 说明 CN | Note EN |
|---|---|---|---|---|
| 澄清 Clarify | ClarifyCard | ×3 轮 / ≤3 rounds | 逐轮确认 known，补 memory | Confirm known, add memory, round by round |
| 方案 Inspo | InspoFlow | ×3 张 / 3 cards | 横滑选，恰 1 张主推 | Swipe to pick, exactly 1 recommended |
| 日程 Itinerary | TravelView | stages ≤5 | 大图封面 + 口播驱动钻取 | Big-photo cover + voice-driven drill-down |
| 收尾 Wrap-up | ListCard | rows[] | 已排进日程的收尾列表 | Final list of scheduled items |
