# 全链路模板（13 节点） · Link Template

> 读这个文件拿旅行规划的骨架。每个节点标明：触发条件、走 cortex 哪个模式/提示词、产出什么卡、口播要点。
> Read this for the skeleton. Each node states: trigger, which cortex mode/prompt, what card, broadcast notes.
> 节点细节按需下钻对应 reference 文件。

## 链路总览 / Overview

```
起手 → 澄清轮1(纯语音) → 澄清轮2(纯语音) → 澄清轮3(出汇总卡) → 搜索预告 → 搜索 → 方案生成(3卡) → 三选一
   → 出日程 → 逐天讲(逐天讲完再总结) → (不满意改) → 日程预告 → 收尾:排日历 → 天气提醒 → 结束
```

相对 cortex 现状的三处变化：澄清 1→3 轮；新增方案生成+三选一；选完直出不再问"要不要过一遍"。

## 节点详表 / Node table

| # | 节点 Node | 触发 Trigger | cortex 模式/提示词 | 产出卡 Card | 下钻 |
|---|---|---|---|---|---|
| 1 | 起手 Kickoff | 用户说想去某地玩 | router 判 travel=NEW → planner | — | — |
| 2 | 澄清轮1 Clarify-1 | 进入 planner | Mode C / QUESTION | 纯语音、不出卡 voice-only | clarify-3rounds.md |
| 3 | 澄清轮2 Clarify-2 | 轮1 答完 | Mode C / QUESTION | 纯语音、不出卡 voice-only | clarify-3rounds.md |
| 4 | 澄清轮3 Clarify-3 | 轮2 答完 | Mode C / QUESTION | 一张汇总卡(已确认+我猜两行) 1 summary card | clarify-3rounds.md |
| 4b | 搜索预告 Notice-Search | 轮3 答完 | Mode B / NOTICE 口播 | — | tts-rules.md |
| 5 | 搜索 Search | 预告后 | Mode A / web_search + get_weather | — | tool-bounds.md |
| 6 | 方案生成 Options | 搜索回来 | **compose_trip_options（已落地）** / present_mode=trip_options | InspoFlow ×3 | plan-options.md |
| 7 | 三选一 Pick | 方案出完 | 用户选 → 选中方案写入 history | — | plan-options.md |
| 8 | 出日程 Itinerary | 用户选完 | compose_trip / present_mode=trip | TravelView | card-schemas.md |
| 9 | 逐天讲 Narrate | 每张日程卡 | compose_trip summary 口播 | — | tts-rules.md |
| 10 | 不满意改 Revise | 用户要调 | planner 局部改 | TravelView(局部、不带表功标签) | 本文件 §不满意改 |
| 10b | 日程预告 Notice-Calendar | 用户认可/要落地 | Mode B / NOTICE 口播 | — | tts-rules.md |
| 11 | 收尾排日历 Calendar | 预告后 | create_event / list_events | ListCard | tool-bounds.md |
| 12 | 天气提醒 Weather | 收尾时 | get_weather 复用 | — | tool-bounds.md |
| 13 | 结束 Close | 交付完成 | Mode B / 收尾口播 | — | tts-rules.md |

## 关键节点说明

### 节点 2-4：三轮澄清（核心变化①）
- 现状 planner.yaml 明文「最多追问一轮」，新设计放到 3 轮。三轮问题集是拍定的，见 clarify-3rounds.md。
- 每轮走 Mode C（reply_type=QUESTION），输出 confirmed / assumed / title 三字段。
- **澄清卡只在最后一轮出**：轮1、轮2 纯语音问答，**不出卡**；只有轮3 出**一张**汇总卡（已确认 + 我猜两行）。别每轮都弹卡。
- 第3轮把前两轮答案沉淀进 confirmed。**只问真影响方案的，信息够了提前收口，别凑轮数**（否则触 L2 墨迹硬伤）。

### 节点 4b / 10b：工具前必有 NOTICE 口播
- 调工具前先来一句进度预告口播（Mode B / NOTICE），让用户知道在干嘛，别静默卡顿。
- 搜索前（节点 4b）：类似「这就给你看看方案」，再调 web_search。
- 收尾查日程前（节点 10b）：类似「我查一下日程」，再调 create_event / list_events。
- 口播一句即可，短、像人，别念稿。
- **关键帧不配图**：NOTICE 这类中间口播在 case 数据里标 `notice: true`，工作台 storyboard 只出文字帧、不克隆上一张卡的残留快照——否则一帧进度口播配着张莫名其妙的图，会让评审/领导困惑。

### 节点 6-7：方案生成 + 三选一（核心变化②，最大新增）
- cortex 已落地这一环： cortex `compose_trip_options` 提示词（镜像见 compose_options.draft.yaml）+ present_mode=`trip_options`。
- 出**正好 3 张** InspoFlow 方案卡，**正好 1 张** rec=true（主推）。三方案靠"节奏+主题+适合谁"真差异化，不换皮。
- 用户选完，把选中方案要点写入 history，作为触发 compose_trip 的前置。

### 节点 8-9：选完直出日程 + 逐天讲完再总结（核心变化③）
- 选完**不再问"要不要过一遍"**，直接出日程卡（不在出规划前设确认门）。
- 进规划的第一段口播多带 1-2 句过渡，把"你选了 X，那我就按这个给你排"接上，别突兀。
- **逐天讲完再总结**：一次给全三天（横滑）→ 逐天讲（含最后一天，别漏）→ **最后才总结 + 软征询**（"你看看咋样，要改随时说"）。软邀改 OK，但不是确认门。
- 日程卡字段严格守 card-schemas.md（label≤18 / place≤14 / note≤42 / reminder≤22，单天铺满4档等）。

### 节点 10：不满意改
- 用户对某天/某点不满意 → **局部改**：只动相关 node，别整链重出。
- 用户要换方案 → 回到节点 8 按另一张方案重排（方案卡还在，不用重出 3 卡）。
- **改版卡不 self-report**：不写"(不变)/✓已调整/改动"这类表功标签，靠 pace + 标题体现改过。
- 改完口播只讲改了什么，别从头复述整个行程；过渡 / 确认口播要短。

### 节点 11-13：收尾交付
- 真交付 = 排进日历（create_event）+ 出发天气提醒。可选行程文档（不需额外 tool）。
- **不算预算总账、不订房、不下单**（tool-bounds.md）。
- 收尾口播主动收口，不反问"还需要我做什么吗"。

## 自检收口
产出整条链路的 case 后，按 `review-gates.md` 过 Jianbo 9 把尺子，**无 L1/L2/L9 硬伤**才算过；口播段再过 shuorenhua/humanizer。
