# Tool Bounds — 工具边界

> **What this file governs / 本文件管什么:** the **hard boundary** of what Loona's travel flow can and cannot do — the exact tools available, what is explicitly out of scope, what counts as real delivery, and how to degrade honestly when a tool fails.
> **When to read / 什么时候读:** read this whenever you design or review a travel case, write the planner/closing prompts, or answer "can Loona book / pay / budget this?". This file is the source of truth for capability claims. If a case promises something not listed here, it fails.

---

## 0. The two tools — that's all / 只有两个工具

Loona's travel planning has **exactly two** information tools:

| Tool | Use for / 用来干什么 |
|---|---|
| `web_search` | spots / inns / food（搜景点、客栈、吃的）|
| `get_weather` | weather **within 14 days** of departure（出发 14 天内的天气）|

There is nothing else for gathering travel info. Don't invent map tools, price APIs, booking tools, or review-scraping tools. If a case relies on a capability not in this table, it is out of bounds.

中文：旅行规划只有两个查信息的工具——`web_search`（搜景点/客栈/吃的）和 `get_weather`（出发 14 天内天气）。别臆造地图、票价 API、订房、爬评论之类的工具。case 依赖表外能力 = 越界。

---

## 1. Out of scope — never do these / 【不做】清单

- **No total-budget accounting.** Never add up a trip cost on the card.（不算预算总账，卡上绝不算总钱。）
- **No booking** of inns/hotels.（不订房。）
- **No ordering / placing orders.**（不下单。）
- **No buying tickets.**（不买票。）

**Budget's only role:** asked **once**, in clarify round 2, purely as a **search tier** — so `web_search` pulls inns and food at the right level. It never becomes a number on a card, never a sum. Saying "中档" steers the search; it does not start a calculation.

中文：预算只在第 2 轮澄清问**一次**，纯做**搜索档位**参考（让 `web_search` 搜对档次的客栈和吃的）。它绝不变成卡上的数字、绝不求和。用户说"中档"只是定搜索方向，不是开始算账。

---

## 2. What counts as real delivery / 收尾真交付是什么

The closing step must hand over something **real**, not a pretty summary card. Real delivery =

1. **Put the itinerary on the calendar** — `create_event` (check existing with `list_events` first to avoid clashes).（把行程排进日历。）
2. **Departure-day weather reminder** — surfaced via `get_weather`.（出发当天天气提醒。）

**Optional:** a trip document. This needs **no extra tool** — it's assembled from what's already planned.（可选：行程文档，不需要额外 tool，用已规划内容拼出来。）

The test for "did we actually deliver?" is: **is it on the user's calendar, and do they know the weather for the day they leave?** A card alone is not delivery.

中文：收尾必须交付**真东西**，不是好看的总结卡。真交付 = ①把行程排进日历（`create_event`，先 `list_events` 查冲突）+ ②出发当天天气提醒（`get_weather`）。可选行程文档不需要额外 tool。判断"到底有没有交付"的标准：**行程进没进日历、用户知不知道出发那天的天气**。光给张卡不算交付。

---

## 3. Degrade rules — fail honestly, never fabricate / 降级规则：诚实降级，绝不编造

| When / 什么情况 | Do / 怎么做 | Never / 绝不 |
|---|---|---|
| `get_weather` fails / 天气查不到 | Write "**confirm again before you leave**"（写"出行前再确认"）| Never fabricate day-by-day weather（禁编逐日天气）|
| `web_search` fails / 搜索失败 | Fall back to **common-sense classic spots**; mark the reminder "**confirm before departure**"（用常识排经典景点，reminder 标"出行前确认"）| Never assert ticket prices / booking-required conclusions（禁断言票价、是否需预约这类结论）|

The principle: a failed tool downgrades the **certainty** of the claim, never replaces it with invented facts. When unsure, frame it as "confirm before you go," don't dress a guess up as fact.

中文：工具失败只降低结论的**确定性**，绝不用编的事实顶上。天气挂了就写"出行前再确认"，不编每天的天气；搜索挂了就用常识排经典景点、reminder 标"出行前确认"，不断言票价和预约结论。拿不准就框成"出行前确认"，别把猜测包装成事实。

---

## 4. For reviewer Jianbo's L6 (deliver a result) / 应对评审人 Jianbo 的 L6（出结果）

Jianbo's L6 asks: did you actually **deliver a result**, or just paint a picture? Loona's way to pass L6 is **not** by pretending to book or budget — it's by **honestly framing the capability boundary**:

- Tell the user plainly **what Loona can do** (plan the route, search spots/inns/food, put it on the calendar, flag the weather) and **what it can't** (book, pay, buy tickets, tally the bill).
- Delivering = the itinerary is on the calendar + weather is flagged. That **is** a real result, and it's an honest one.
- Never fake booking, never fake a total cost to look more "complete." A faked result fails L8 (accuracy) even if it looks like it passes L6.

中文：Jianbo 的 L6 问的是"你到底**出没出结果**，还是只画了张饼"。Loona 过 L6 靠的**不是**假装能订房算账，而是**诚实框定能力边界**：明确告诉用户能做什么（排路线、搜景点客栈吃的、排进日历、提醒天气）、不能做什么（订房、付款、买票、算总账）。交付 = 行程进日历 + 天气提醒，这本身就是真结果，而且是诚实的结果。绝不为了显得"更完整"假装订房、假装算出总价——假结果即便看着过了 L6，也会栽在 L8（准确）。
