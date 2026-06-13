---
name: loona-travel-flow
description: >-
  Design contract and generator for Loona's voice-first travel-planning flow (hardware desk companion,
  phone-sized screen). Use this whenever you are designing, iterating, or reviewing Loona's travel /
  trip-planning interaction — the 3-round clarification, the new "generate 3 options → pick one" step,
  the day-by-day itinerary cards, or the TTS broadcast copy. Also use it when generating a concrete
  travel case (case.js) for the workbench, or when figuring out how to change cortex's travel prompts
  (planner.yaml / compose_trip_options.yaml / compose_trip.yaml). Trigger even if the user just says
  "做一个旅行 case / 改一下旅行规划链路 / Loona 旅游流程 / 旅行方案三选一 / trip flow"
  without naming this skill. This skill owns the link/logic/rules; UI tweaks belong in the workbench.
---

# loona-travel-flow

把 Loona 的「旅行规划」交互链路封装成可复用的设计契约 + case 生成器。

## 这个 skill 是什么 / 不是什么

- **是**：链路结构、澄清逻辑、方案三选一规则、卡片字段 schema、口播去AI味规则的**单一真相源**。产物两类：① 工作台能播的 `case.js`；② 喂 cortex 的提示词改动方案（EN/CN）。
- **不是生产运行时**：真正跑的是 cortex `web_ui`，提示词在 `config/llm_tasks/*.yaml`。本 skill 是设计规范，最终落到那几个 yaml。
- **防漂移铁律**：链路/逻辑/规则的结构性改动 → 改本 skill 再重生成；纯一次性 UI 微调 → 工作台。**别在工作台手改 events 结构**。

## 设备前提（决定一切设计）

Loona 是硬件桌宠：**语音优先**，屏幕只有**手机大小**。所以——用户主要靠"听"（口播是命门），卡片一次一焦点、信息精简，不是大屏工作台。

## 全链路（13 节点）

详细模板见 `references/link-template.md`。一句话串起来：

```
起手 → 澄清3轮 → 搜索 → 方案生成(三选一) → 选完直出日程 → 逐天讲 → 不满意改 → 收尾交付
```

| # | 节点 | 产出 | 规范文件 |
|---|---|---|---|
| 1 | 起手/触发（router 判 travel=NEW） | — | link-template.md |
| 2 | 澄清轮1：几人/几天/**出发日期** | ClarifyCard | clarify-3rounds.md |
| 3 | 澄清轮2：预算档(只做搜索参考)+会不会骑车 | ClarifyCard | clarify-3rounds.md |
| 4 | 澄清轮3：必去/节奏 + 沉淀已确认 | ClarifyCard | clarify-3rounds.md |
| 5 | 搜索：web_search + get_weather | — | tool-bounds.md |
| 6 | **方案生成：出3张方案卡标主推** | InspoFlow ×3 | plan-options.md |
| 7 | 用户三选一 | — | plan-options.md |
| 8 | 出日程：按选中方案排 | TravelView 日程卡 | card-schemas.md |
| 9 | 逐天讲：每张卡口播 | summary 口播 | tts-rules.md |
| 10 | 不满意改：局部改 node/换方案 | — | link-template.md |
| 11-13 | 收尾交付：排日历 + 天气提醒 | ListCard | tool-bounds.md |

**相对现状(cortex)的三处关键变化**：
1. 澄清 **1 轮 → 3 轮**（现状 planner.yaml 明文"最多追问一轮"）。
2. **新增"方案生成+三选一"环节**（现状完全没有）——最大新增，已落地 `compose_trip_options` 提示词 + 新 `present_mode`。
3. 选完方案**直出规划**，不再问"要不要过一遍"；进规划的口播多带 1-2 句把过渡接上。

## 怎么生成一个 case（两段式：内容先行，JS 后置）

**铁律：先出内容稿让用户逐句对齐，对齐后才落 JS。别一上来直接吐 case.js**——用户要先能指着某句口播说"这句改"、某个节点说"这环节调一下"，JS 是机器格式不利于对齐。

### Phase A · 内容稿（产出 `<case>.spec.md`，给人看、给人改）
1. **读规范**：先读 `references/link-template.md` 拿全链路骨架；按节点需要再读对应 reference（卡片字段→card-schemas.md，口播→tts-rules.md，方案环节→plan-options.md，澄清→clarify-3rounds.md，工具边界→tool-bounds.md）。
2. **填三轮澄清**：按 clarify-3rounds.md 的问题集，沉淀 confirmed/assumed。轮2 第二槽是**因城而异的关键偏好问题**（最能决定主推方案走向的那一项：大理=会不会骑车，成都=吃不吃辣）——二元优先但不强求，正常开放问也行；按城市挑，不是写死骑车。
3. **出 3 方案**：按 plan-options.md 差异化（真有区别不换皮），标 1 张主推。
4. **按选中方案出日程卡 + 不满意改 + 收尾**：字段严格守 card-schemas.md 长度上限；收尾=日历+天气提醒，守 tool-bounds.md（不算总账/不订房）。
5. **写成内容稿 `<case>.spec.md`**：① 口播逐句、**每句标编号**（口播01、口播02…）便于用户精确指；② 卡片内容用表格列字段（ClarifyCard/InspoFlow/TravelView/ListCard）。所有口播先过 tts-rules.md 的 8 条 + 说出口自检三关。范例见 `examples/travel_chengdu_3d.spec.md`。
6. **交给用户对齐**：明确请用户按编号指出哪句要改、哪个环节要调。**停在这里等反馈，别自作主张往下落 JS。**

### Phase B · 落 JS（对齐通过后）
7. **按对齐后的内容稿生成 `<case>.js`**：照 `examples/travel_dali_3d_solo.js` 的数据结构（IIFE 注册、events 数组、comp 类型、tts.text 承载口播）。`node --check` 验语法。
8. **自检**：按 `references/review-gates.md` 过 Jianbo 9 把尺子；**无 L1/L2/L9 硬伤**才算过。口播段再过 `shuorenhua`/`humanizer`，可选 `prompt-eval` 打分。
9. **双版本**：case 与示例都要 CN + EN（缺一非法）。

## reference 文件清单

| 文件 | 管什么 |
|---|---|
| `references/link-template.md` | 13 节点全链路模板 + 不满意改/收尾 |
| `references/clarify-3rounds.md` | 三轮澄清问题集（EN/CN）+ confirmed/assumed/title |
| `references/plan-options.md` | 方案生成+三选一环节 + present_mode + 回流 |
| `references/compose_options.draft.yaml` | cortex compose_trip_options.yaml 的镜像（已落地，2026-06-10 同步） |
| `references/card-schemas.md` | 4 类卡片字段 schema + 字段生成提示词 |
| `references/tts-rules.md` | TTS 去AI味 8 硬规则 + persona 素材 + 自检三关 |
| `references/tool-bounds.md` | 工具边界（只搜索+天气，不算账不订房）+ 降级 |
| `references/review-gates.md` | Jianbo 9 把尺子自检闸 + shuorenhua/humanizer |
| `references/cortex-prompt-changes.md` | 要改 cortex 哪些 yaml、怎么改（EN/CN） |
| `examples/travel_dali_3d_solo.js` | 标杆 case（大理3天单人，CN） |
| `examples/travel_dali_3d_solo.en.js` | 英文版标杆 |

## 工具边界（一句话）

只有 `web_search` + `get_weather`。**不算预算总账、不订房、不下单**。预算只在澄清轮2 问一下做搜索档位。收尾真交付 = 排日历 + 天气提醒。详见 tool-bounds.md。
