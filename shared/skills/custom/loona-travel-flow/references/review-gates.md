# Review Gates — 评审自检闸（Jianbo 9 把尺子）

> **What this file governs / 本文件管什么:** the **self-check gate** to run on every travel case this skill produces, before showing it to anyone. It freezes reviewer **Jianbo's 9 lenses (L1–L9)** into a checklist, marks which ones are **hard-fails**, and defines the close-out flow (self-check → `jianbo-review` → humanizer → optional `prompt-eval`).
> **When to read / 什么时候读:** read this right after you produce or revise a travel case (clarify cards, plan, TTS lines, closing). Don't ship a case until it clears this gate.

---

## 0. Pass bar / 通过线

A case passes **only if there is no L1 / L2 / L9 hard-fail.** Those three are 硬伤项 — **any one present = the whole case fails**, regardless of how good the rest is. L3–L8 are quality lenses: weak spots there are fixed-then-shipped, not auto-fail.

中文：一个 case 通过的唯一标准是**没有 L1 / L2 / L9 硬伤**。这三条出现任意一条 = 整个 case 判不通过，别的再好也没用。L3–L8 是质量尺子：弱了就改了再发，不是一票否决。

---

## 1. The 9 lenses / 九把尺子逐条

> Legend: **【硬伤】** = hard-fail (present → fail immediately). Others = quality, fix and re-ship.

| L | Lens / 尺子 | Check what / 检查什么 | Where to look in a travel case / 旅行 case 里看哪 | Fail symptom / 不通过的典型症状 |
|---|---|---|---|---|
| **L1** | 人味 Human-feel **【硬伤】** | Does it sound like a **real person**, not an AI script? | All TTS lines (clarify spoken lines, plan narration, closing). | 书面腔："为您打造""兼具""不妨"；三段排比；破折号抒情；通篇模板味。 |
| **L2** | 不墨迹 Concise **【硬伤】** | Is it **tight**, no padding, no repeating? | Clarify rounds (padded to hit 3?), TTS sentence length, closing. | 凑轮数问废话；一句话超 25 字还不断句；屏幕已显示的内容口播又复述一遍。 |
| **L3** | 主动 Proactive | Does Loona **lead**, not passively wait? | Clarify close-out, plan handoff, closing step. | 每轮都把球踢回给用户、以问句收尾；不主动带去下一步；干等用户发话。 |
| **L4** | 形式 Form | Is the **card / TTS split** sensible? | Every node: what's on the card vs what's spoken. | 该上卡的信息塞进口播、该口播的堆在卡上；口播复述卡面；卡片信息过载。 |
| **L5** | 信息完备 Completeness | Is the **info that should be there** present? | Plan nodes (spot + how to get there + why), closing (calendar + weather). | 给了景点没给怎么去；规划缺出发日期/天气挂钩；收尾没排进日历。 |
| **L6** | 出结果 Deliver | Real **delivery**, or just a pretty picture? | Closing step (see `tool-bounds.md` §2/§4). | 只给总结卡不排日历；假装能订房/算总账冒充"完整"。 |
| **L7** | 个性化 Personalized | Tailored to **this user / memory / weather**? | Clarify `confirmed`/`assumed`, plan choices, weather hookup. | 通用模板谁来都一样；不接已确认信息；不挂出发天气；忽略用户说过的偏好。 |
| **L8** | 准确 Accurate | **No fabricated facts**? | Any factual claim: spots, prices, weather, "需预约". | 编逐日天气；断言票价/预约结论；搜索失败后硬编事实（违反 `tool-bounds.md` §3）。 |
| **L9** | 覆盖 Coverage **【硬伤】** | Are the **key scenarios** all there? | The whole flow: clarify → plan → closing. | 漏澄清直接出方案；漏收尾不交付；关键场景（天气/日历/必去）缺失。 |

---

## 2. The 9 lenses — EN / 英文版

> Legend: **[HARD]** = hard-fail. Others = quality, fix and re-ship.

- **L1 — Human-feel [HARD]:** Sounds like a real person, not an AI script. *Look:* all TTS lines. *Fail:* written-register words, three-part parallelism, em-dash sighing, template tone.
- **L2 — Concise [HARD]:** Tight, no padding, no repetition. *Look:* clarify rounds, TTS length, closing. *Fail:* rounds padded to hit a count; sentences over the length limit without breaking; spoken line repeats what's already on screen.
- **L3 — Proactive:** Loona leads, doesn't passively wait. *Look:* clarify close-out, handoffs, closing. *Fail:* every turn lobs the question back; never moves to the next step; waits for the user.
- **L4 — Form:** Card/TTS split is sensible. *Look:* each node's card vs spoken content. *Fail:* card-worthy info spoken, spoken-worthy info on the card, spoken line restates the card, overloaded card.
- **L5 — Completeness:** The info that should be there is there. *Look:* plan nodes (spot + how to get there + why), closing (calendar + weather). *Fail:* spot with no route; plan missing departure date / weather hook; closing with no calendar entry.
- **L6 — Deliver:** Real delivery, not a pretty picture. *Look:* closing step (see `tool-bounds.md` §2/§4). *Fail:* summary card with no calendar; faking booking/budget to look "complete."
- **L7 — Personalized:** Tailored to this user / memory / weather. *Look:* `confirmed`/`assumed`, plan choices, weather hook. *Fail:* generic template; ignores confirmed info; no departure-weather hook; ignores stated preferences.
- **L8 — Accurate:** No fabricated facts. *Look:* any factual claim. *Fail:* invented day-by-day weather; asserted ticket prices / reservation conclusions; hard-coded facts after a search failure (violates `tool-bounds.md` §3).
- **L9 — Coverage [HARD]:** Key scenarios all present. *Look:* the whole flow. *Fail:* skips clarify and jumps to a plan; skips the closing/delivery; a key scenario (weather/calendar/must-go) is missing.

---

## 3. Close-out flow / 收口流程

Run these **in order** after producing a case:

1. **Self-check the 9 lenses** (this file). Confirm **no L1 / L2 / L9 hard-fail**. Fix anything flagged before moving on.（先自查这 9 条，确认无 L1/L2/L9 硬伤，flag 到的先改掉。）
2. **Call `jianbo-review` skill** — simulate the real Jianbo's pre-review in his voice, predict his per-node verdict, catch what the self-check missed.（再调 `jianbo-review` skill 模拟真人预审，逐节点预测他怎么评。）
3. **Run TTS lines through `shuorenhua` / `humanizer`** — de-AI every spoken line (this directly hardens L1).（口播段再过 `shuorenhua`/`humanizer` 去 AI 味——直接加固 L1。）
4. **Optional: `prompt-eval`** — score the case / A-B prompt versions when you want a number.（可选：`prompt-eval` 给 case 或 A/B 提示词版本打分。）

> Don't hand-roll a review agent — use `jianbo-review` for step 2 and `shuorenhua`/`humanizer` for step 3. When fabricating numbers for a demo case, add them so they stay plausible, and don't over-claim the result (per lessons on `jianbo-review`).

中文：产出 case 后**按序**收口——①自查 9 条、确认无 L1/L2/L9 硬伤、改完再走；②调 `jianbo-review` skill 模拟真人逐节点预审；③口播段过 `shuorenhua`/`humanizer` 去 AI 味（直接加固 L1）；④可选 `prompt-eval` 打分。别手搓评审 agent，第 2 步用 `jianbo-review`、第 3 步用 `shuorenhua`/`humanizer`；编演示数据要加得平、出结果别 over-claim。
