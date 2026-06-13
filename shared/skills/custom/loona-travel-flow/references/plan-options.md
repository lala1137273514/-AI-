# Plan Options · 方案生成 + 三选一环节设计规范

> 这是 loona-travel-flow 链路里【最重要的新增环节】的设计契约。
> 给硬件桌宠 Loona（语音优先、手机大小小屏）用。
> EN/CN 双语；字段说明、口播示例都给中英两版。

---

## 1. Position in the flow · 在链路里的位置

**EN**

cortex today: `user → router → planner(clarify → search) → compose_trip(itinerary card + TTS)`.
There is **no plan-generation / pick-one step**. This doc inserts one.

New flow:

```
user
 → router
 → planner: clarify (max 3 rounds) → search
 → [NEW] compose_trip_options: emit 3 plan cards (1 marked rec) → user picks one
 → compose_trip: itinerary, seeded with the picked plan
```

Rules:
- Trigger **only after clarify is done** (planner has gathered enough; clarify is capped at 3 rounds). Do not run plan options while still asking clarify questions.
- After the user picks a card, **go straight to compose_trip**. Do **not** add a confirmation gate — no "want to walk through it?" / "shall we go over it?" before laying it out; the pick IS the confirmation. (A soft invite to edit **after** the itinerary is fine — see §5.)
- Exactly one round of picking. No "pick again" loop. If the user rejects all three, that is a planner concern (re-clarify), not a re-roll of options.

**CN**

cortex 现状：`用户 → router → planner(澄清 → 搜索) → compose_trip(出日程卡 + 口播)`。
**完全没有"方案生成 + 三选一"环节**，本文档就是补这一环。

新链路：

```
用户
 → router
 → planner：澄清(最多 3 轮) → 搜索
 → [新增] compose_trip_options：出 3 张方案卡(标 1 张主推) → 用户三选一
 → compose_trip：按选中的方案出日程
```

规则：
- **澄清完成后才触发**（planner 收集够了；澄清最多 3 轮）。还在问澄清问题时不能出方案。
- 用户选完某张卡，**直接触发出日程**，不设确认门——不在出日程前问"要不要过一遍 / 要不要确认一下"，选择本身就是确认。（日程**讲完之后**软邀一句"要改随时说"是可以的——见 §5。）
- 只一轮三选一。没有"重选 / 再来一组"循环。三张全不满意属于 planner 重新澄清的事，不是重摇方案。

---

## 1b. Spoken beats around search · 搜索前后的口播节拍

**EN**

- **Before calling tools (NOTICE):** before any `web_search` / `get_weather`, planner first speaks a short progress NOTICE, *then* calls the tool. This is the Mode A `reply_text` progress cue, so the user isn't left in silence while the search runs.
  - e.g. `好的，稍等一下哦，这就给你看看有啥好玩的方案。`
- **When the options come back, open with one line first**, then go card by card. Don't dump straight into option 1.
  - e.g. `来啦，给你扒拉出三种不一样的玩法，我挨个说说。`

**CN**

- **调工具前先 NOTICE：** 任何 `web_search` / `get_weather` 之前，planner 先发一句简短进度 NOTICE 口播，**再**调工具。这是 Mode A 的 `reply_text` 进度提示，别让用户在搜索时干等没声。
  - 例：`好的，稍等一下哦，这就给你看看有啥好玩的方案。`
- **方案搜回来先一句开场**，再逐个方案讲。别上来就直接念第 1 个方案。
  - 例：`来啦，给你扒拉出三种不一样的玩法，我挨个说说。`

---

## 2. present_mode: `trip_options`

**EN**

A new present_mode named `trip_options` renders 3 InspoFlow plan cards. The frontend shows them as a horizontal pick-one set; one card carries a "主推 / Top pick" badge (`rec=true`).

Card schema (one object per card):

| field | type | meaning |
|---|---|---|
| `id` | string | `opt1` / `opt2` / `opt3`, stable handle for the pick callback |
| `rec` | bool | top pick. **Exactly one** card in the set is `true` |
| `title` | string | plan name, ≤14 full-width chars |
| `photo` | string\|null | a credible image URL already seen in history; if none → `null`. Never fabricate |
| `tags` | string[] | 2–4 short words, the plan's flavor (e.g. 骑行 / 深度 / 慢节奏) |
| `punchline` | string | the spoken line (TTS) for this card. Must describe the **whole-trip vibe** (how the N days play out as a shape) — **never** a single-day "morning…afternoon…evening" run-through (that belongs to the itinerary card, not a plan). rec card may sell; the other two are one quick line |

**CN**

新增 present_mode 叫 `trip_options`，渲染 3 张 InspoFlow 方案卡。前端横排三选一，其中一张挂"主推"角标（`rec=true`）。

方案卡字段 schema（每张卡一个对象）：

| 字段 | 类型 | 含义 |
|---|---|---|
| `id` | string | `opt1` / `opt2` / `opt3`，给选择回流用的稳定句柄 |
| `rec` | bool | 主推。一组里**正好一张**为 `true` |
| `title` | string | 方案名，≤14 全角字 |
| `photo` | string\|null | 历史里出现过的可信图 URL；没有就 `null`，禁编图 |
| `tags` | string[] | 2–4 个短词，方案的味道（如 骑行 / 深度 / 慢节奏） |
| `punchline` | string | 这张卡的口播(TTS)。必须讲**整个行程的调性**（这 N 天整体是个什么玩法），**严禁**写成"一早…下午…晚上"的单天流水（单天流水是日程卡的事，不是方案）。主推卡可 sell，另两张一句带过 |

---

## 3. How the 3 plans differ · 3 方案怎么差异化

**EN**

Three plans must be **genuinely different in shape**, not the same itinerary re-skinned. Differentiate by **pace + theme + who-it-fits**, not by swapping one attraction. A good split (Erhai Lake example):

| card | shape | who/what |
|---|---|---|
| rec (主推) | Erhai cycling deep-dive | active, on the bike around the lake, into the villages most people skip |
| #2 | classic must-sees | first-timer, hits the headline spots, safe and full |
| #3 | slow / lie-flat | minimal moving, lakeside cafés, sleep in, one spot a day |

Test for "real difference": if you swapped the titles, would the day-shapes still read as the same trip? If yes, they are too similar — re-differentiate.

Keep all three honest to the clarify info (same city, same days, same party). The axis that moves is **intensity and intent**, not the destination.

**CN**

三个方案必须**形态上真有区别**，不是同一行程换皮。沿**节奏 + 主题 + 适合谁**这条轴分，不是换掉一个景点。一个好拆法（洱海例）：

| 卡 | 形态 | 适合谁/什么 |
|---|---|---|
| 主推 (rec) | 洱海骑行深度版 | 爱动，骑车环湖，钻别人不去的村子 |
| #2 | 经典打卡版 | 第一次来，把头部景点扫一遍，稳妥且满 |
| #3 | 慢节奏躺平版 | 几乎不挪窝，湖边咖啡，睡到自然醒，一天一个点 |

"真有区别"自检：把标题互换，三张的"每天形态"还会读成同一趟行程吗？会的话就太像了，重分。

三张都要忠于澄清信息（同城、同天数、同人）。动的是**强度和意图**，不是目的地。

---

## 4. rec card vs. the other two · 主推卡口播怎么 sell

**EN**

- **rec card (`rec=true`)**: **about 2–3 sentences, plain and conversational — don't oversell.** Carry a soft personal lean keyed to the trip's overall shape, plus a concrete reason. **Avoid hype/templated tone** ("我最推荐这个方案！特别适合…", "主打一个X"); say it like a person leaning in, e.g. `我比较推第一个，你俩想松着玩，这条正合适…`. Concrete whole-trip vibe, not adjectives, not a single-day run-through.
  - e.g. `我比较推第一个。整趟都贴着洱海走，骑两天、歇两天，不赶；绕湖那段才看得到游客到不了的那片海，正好这季节水最清。`
- **the other two**: **two sentences each, just a quick summary**, enough to tell them apart. No selling. State the whole-trip shape + who it suits; can lean on memory (e.g. `都是你爱吃的那口`).
  - e.g. `第二个稳一点，几天把头部那几个点扫全，第一次来不踩雷。` / `第三个最躺，一天就一个点，湖边咖啡睡到醒，全程都是你爱吃的那口。`

Do not sell all three equally — that flattens the recommendation and the user can't feel which one you actually back.

**CN**

- **主推卡（`rec=true`）**：**约 2-3 句，平实口语别用力。** 带一点贴着整程调性的个人倾向，再给一个具体理由。**别用激情/套路腔**（"我最推荐这个方案！特别适合…""主打一个X"），像人凑过来说，例：`我比较推第一个，你俩想松着玩，这条正合适…`。讲整程的调性，要具体、别堆形容词、别写成单天流水。
  - 例：`我比较推第一个。整趟都贴着洱海走，骑两天、歇两天，不赶；绕湖那段才看得到游客到不了的那片海，正好这季节水最清。`
- **另两张**：**各两句概括即可**，够区分就行。不 sell。说清整程形态 + 适合谁，可贴记忆（如 `都是你爱吃的那口`）。
  - 例：`第二个稳一点，几天把头部那几个点扫全，第一次来不踩雷。` / `第三个最躺，一天就一个点，湖边咖啡睡到醒，全程都是你爱吃的那口。`

别三张一样使劲 sell——那样推荐就被拉平了，用户感觉不出你到底押哪张。

---

## 5. Pickback → compose_trip · 选择后的回流

**EN**

When the user picks a card:
1. Take the picked option's `title` + `tags` + its core shape (pace/theme) and feed them to `compose_trip` as the seed, so the itinerary is built **on that plan**, not a generic one.
2. The itinerary's first spoken line (compose_trip `summary` of stage 1) adds **1–2 sentences** to bridge: "you picked X, so I'll lay it out this way." Natural, not a re-announcement.
   - e.g. `行，那就按骑行这条来，我把环湖的路顺着排，先近后远不绕回头路。`
3. Don't re-list the three options or re-justify the pick. One bridge line, then into the itinerary.
4. **No confirmation gate before laying it out.** But **after the day-by-day is done**, you may close with one soft invite to edit — `你看看咋样，要改随时说。` This is an exit for changes, **not** a "shall we go over it?" gate, and it comes only at the end.

The pick is passed as the chosen `id` plus its fields; planner's clarify info (confirmed/assumed) still flows through unchanged.

**CN**

用户选了某张卡后：
1. 把选中方案的 `title` + `tags` + 核心形态（节奏/主题）喂给 `compose_trip` 当种子，让日程**按这个方案**排，不是排个通用的。
2. 日程第一句口播（compose_trip 第 1 个 stage 的 `summary`）加 **1–2 句**过渡："你选了 X，那我就按这个给你排。"自然衔接，别重新报一遍。
   - 例：`行，那就按骑行这条来，我把环湖的路顺着排，先近后远不绕回头路。`
3. 别重列三个方案、别再论证为什么选它。一句过渡，直接进日程。
4. **出日程前不设确认门。** 但**逐天讲完之后**，可以软征询一句 `你看看咋样，要改随时说。`——这是给改的出口，**不是**"要不要过一遍"的确认门，且只在结尾出现。

回流时传选中的 `id` 加它的字段；planner 的澄清信息（confirmed/assumed）原样继续往下走。
