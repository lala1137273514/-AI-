# Clarify — 3 Rounds / 三轮澄清问题集

> **What this file governs / 本文件管什么:** the design contract for Loona's travel-clarification phase — the **3 rounds** of questions asked before a trip plan is generated, what each round asks, the spoken-line (TTS) style, and the `confirmed / assumed / title` fields each round must output.
> **When to read / 什么时候读:** read this whenever you build, review, or change the clarify step of the travel flow, or when you wire the planner's clarification questions. The current cortex planner prompt says "ask follow-ups **at most once**" (zh: 「最多追问一轮」). This file **supersedes** that and moves clarification to **3 rounds**.

---

## 0. Hard rules (apply to every round) / 每轮通用硬规则

- **Only ask what truly changes the plan.** Never pad rounds to hit a count of 3. Padding triggers reviewer Jianbo's "L2 墨迹/啰嗦" hard-fail.
- **Clarify by confirming an inference, not by asking flat.** State what you assume, let the user correct it.
- Every round runs cortex **Mode C / `reply_type=QUESTION`**.
- Every round tracks three fields internally; only the **last round renders them onto the single card**:
  - `confirmed` → card's `已确认` line — what the user said out loud, as **short phrase tags**, comma-separated. Not full sentences.
  - `assumed` → card's `我猜` line — what you inferred from profile/memory, as **short phrase tags**, comma-separated. Not full sentences.
  - `title` — one short card title (only the final card needs one).
- **Only ONE ClarifyCard, on the last round.** Rounds 1–2 are **pure spoken Q&A — no card**. Only the final round (once you've gathered enough) emits **one** summary card. Don't drop a Tag card every round. (Reviewer Jianbo: "Don't dump a pile of Tag cards up front — just show what's confirmed.")
- **The card has exactly two lines:** `已确认` (known — roll up what the user said out loud across rounds 1–2) and `我猜` (memory — what you inferred from profile/memory).

### Spoken-line (TTS) style — mandatory / 口播话术硬约束（必须遵守）
- One sentence ≤ 25 chars (CN); break it if you can.
- Banned written-register words: 为您 / 兼具 / 值得 / 不妨 / 堪称 / 打造.
- No three-part parallelism, no em-dash lyrical sighing.
- Use spoken connectors: 就 / 那 / 其实 / 直接 / 顺手.
- Use 你, never 您.
- Close actively, don't end on a question back at the user.
- **Don't re-read confirmed info aloud** — the card shows it. Spend the spoken line on **one extra memory / profile detail** instead. (E.g. round 3, not "two of you, 3 days, mid budget, can eat spicy" but "Got it, all noted. Anywhere you've already got your eye on? You don't like crowds, so I'm guessing a slower pace, right?")
- **The round-2 key preference question can lean on memory.** It's the per-city question that most shapes the plan (Dali = can you ride a bike, Chengdu = can you eat spicy). A crisp yes/no is best, but it need not be strictly binary — an open question to gather the deciding preference is fine. If memory holds a relevant preference, **state it as confirmation** ("You two can handle spicy, right?") instead of asking flat; only ask as an open question if memory has nothing.

---

## 1. The 3 rounds / 三轮问题集

| Round | Ask / 问什么 | Why it's load-bearing / 为什么关键 |
|---|---|---|
| **1** | destination if the user hasn't given one / how many people / how many days / **departure date** （目的地——用户没给时本轮先问 / 几人 / 几天 / 出发日期） | destination gates round 2's city-specific question; date drives the schedule + weather（目的地是轮2关键偏好问题的前提；日期定排期+天气）|
| **2** | budget tier (search reference only, **not** a full cost tally) + can you ride a bike?（预算档次只做搜索参考、不算总账 + 会不会骑车）| Dali's headline is the Erhai-lake bike ride — if they can't ride, the plan collapses; budget sets the search tier for inns and food（大理主推=洱海骑行，不会骑方案就崩；预算定客栈/吃的搜索档位）|
| **3** | must-go spots / pace + roll rounds 1–2 answers into "confirmed"（必去地方 / 节奏 + 把前两轮答的沉淀进"已确认"）| **the only card** — two lines: `已确认` (rolled-up) + `我猜` (memory)（全程唯一一张卡，两行：已确认汇总 + 我猜推断）|

---

## 2. Per-round spec — EN / 英文版

### Round 1 — people / days / departure date — **no card, spoken only**
- **Spoken line (TTS):** "Quick check first — how many of you, how many days, and roughly when you leave? I'll lock the dates so the weather's right."
- **Tracked internally (not rendered yet):** `confirmed`: `Dali, solo` · `assumed`: `weekend trip, short break`

### Round 2 — budget tier + key preference question — **no card, spoken only**
- **Spoken line (TTS), memory has nothing on biking (ask flat):** "What's the rough budget? Just so I search inns and food at the right level — I'm not adding up a total. Oh, and can you ride a bike?"
- **Spoken line (TTS), memory says they bike (confirm, don't ask):** "Budget-wise, what level? I'll just match the search. You ride, right? — I'll keep the Erhai loop in."
- **Tracked internally:** `confirmed`: `mid budget, can ride bike` · `assumed`: `wants lakeside inn, casual local food`

### Round 3 — must-go / pace — **the single summary card**
- **Spoken line (TTS) — don't re-read confirmed info, add a memory detail:** "Got it, all noted. Anywhere you've already got your eye on? You don't like crowds, so I'm guessing a slower pace, right?"
- **Card (two lines):**
  - `已确认` (from `confirmed`): `Dali, solo, 3 days, mid budget, can ride bike`
  - `我猜` (from `assumed`): `relaxed pace, Erhai ride as the highlight`
  - `title`: `Must-haves & pace`

---

## 3. 分轮规格 — 中文版 / CN

### 第 1 轮 — 几人 / 几天 / 出发日期 — **不出卡，纯语音**
- **口播示例话术:** "先确认下，几个人，玩几天，大概啥时候出发？我把日期定了，天气才准。"
- **内部跟踪（先不渲染）:** `confirmed`: `大理, 单人` · `assumed`: `周末出行, 短途`

### 第 2 轮 — 预算档次 + 关键偏好问题 — **不出卡，纯语音**
- **口播示例话术（记忆里没骑车偏好，疑问句问）:** "预算大概什么档，我搜客栈和吃的好有个准——不算总账啊。对了，你会骑车不？"
- **口播示例话术（记忆里有骑车偏好，陈述确认句、别问）:** "预算啥档，我对着搜就行。你会骑车吧？——那我把洱海那圈留上。"
- **内部跟踪:** `confirmed`: `中档预算, 会骑车` · `assumed`: `想住洱海边客栈, 吃本地小馆`

### 第 3 轮 — 必去 / 节奏 — **全程唯一一张汇总卡**
- **口播示例话术（别复述已确认信息，多贴一条记忆）:** "好嘞，都记住啦。有没有已经看上的地方？我记得你不爱扎堆，那节奏想松点吧？"
- **卡片（两行）:**
  - `已确认`（取自 `confirmed`）: `大理, 单人, 3 天, 中档预算, 会骑车`
  - `我猜`（取自 `assumed`）: `节奏偏松, 洱海骑行当主线`
  - `title`: `必去和节奏`

---

## 4. When to close early / 何时收口

Don't force all 3 rounds. End clarification early when:

- The user already volunteered the round's info in an earlier turn (e.g. they said "3 days, just me, leaving Saturday" up front → skip round 1's questions, just confirm).
- You have **enough to plan**: people + days + date + (for Dali) the bike answer. Once these are in `confirmed`, stop asking and go plan.
- The user shows impatience ("随便安排就行" / "just sort it out") → collapse remaining rounds into one confirmation card and proceed.
- A round's only open item doesn't change the plan → fold it into `assumed` instead of asking.

When you close early, still emit the **single** final card — two lines, `已确认` (full rolled-up `confirmed`) + `我猜` (`assumed`) — so the user sees what you locked in. Earlier rounds stay card-less either way.

中文：别硬凑 3 轮。用户前面已经说了的别再问，只确认；人数+天数+日期+（大理的）骑车答案到齐就直接去规划；用户不耐烦就把剩下的并成一张确认卡往下走；某轮唯一的待问项不影响方案，就塞进 `assumed` 别问。提前收口也只出**那一张**卡，两行：已确认（全部 `confirmed` 沉淀）+ 我猜（`assumed`）；前面几轮一律不出卡。

---

## 5. Full worked example — Dali, 3 days, solo / 完整三轮示例（大理3天单人游）

### EN

**Round 1 — no card**
- `QUESTION`: "Quick check first — how many of you, how many days, and roughly when you leave? I'll lock the dates so the weather's right."
- _(tracked: `confirmed` = `Dali, solo, 3 days`; `assumed` = `leaving this weekend`)_

**Round 2 — no card** (memory has nothing on biking, so ask flat)
- `QUESTION`: "What's the rough budget? Just so I search inns and food at the right level — I'm not adding up a total. And can you ride a bike?"
- _(tracked: `confirmed` = `Dali, solo, 3 days, mid budget, can ride bike`; `assumed` = `lakeside inn, local food`)_

**Round 3 — the single card**
- `QUESTION` (don't re-read confirmed info, add a memory detail): "Got it, all noted. Anything you must hit? You don't like crowds, so I'm keeping it chill, yeah?"
- **Card (two lines):**
  - `已确认`: `Dali, solo, 3 days, mid budget, can ride bike, relaxed pace`
  - `我猜`: `Erhai ride as the highlight, Dali old town a must`
  - `title`: `Must-haves & pace`

### CN

**第 1 轮 — 不出卡**
- `QUESTION`: "先确认下，几个人，玩几天，大概啥时候出发？我把日期定了，天气才准。"
- _(内部跟踪：`confirmed` = `大理, 单人, 3 天`；`assumed` = `这周末出发`)_

**第 2 轮 — 不出卡**（记忆里没骑车偏好，疑问句问）
- `QUESTION`: "预算大概什么档，我搜客栈和吃的好有个准——不算总账啊。对了，你会骑车不？"
- _(内部跟踪：`confirmed` = `大理, 单人, 3 天, 中档预算, 会骑车`；`assumed` = `洱海边客栈, 本地小馆`)_

**第 3 轮 — 全程唯一一张卡**
- `QUESTION`（别复述已确认信息，多贴一条记忆）: "好嘞，都记住啦。有啥必去的不？我记得你不爱扎堆，那就给你安排松一点哈？"
- **卡片（两行）:**
  - `已确认`: `大理, 单人, 3 天, 中档预算, 会骑车, 节奏偏松`
  - `我猜`: `洱海骑行当主线, 大理古城必去`
  - `title`: `必去和节奏`

### CN — 成都变体（关键偏好=吃不吃辣，能贴记忆就贴）

**第 2 轮 — 不出卡**（记忆里有吃辣偏好，用陈述确认句、别问）
- `QUESTION`: "预算啥档，我对着搜就行。你俩能吃辣吧？——那我把火锅串串都给你排上。"
- _(内部跟踪：`confirmed` = `成都, 两人, 3 天, 中档预算, 能吃辣`；`assumed` = `想住市中心, 爱小馆子`)_
