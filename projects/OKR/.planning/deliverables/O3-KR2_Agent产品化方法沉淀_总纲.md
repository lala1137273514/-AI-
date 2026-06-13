# Agent 产品化方法沉淀（总纲）

> **定位**：O3-KR2 收口主文档。把 5 月的四源实战素材（Loona-Spec v1.0 / 用户体验 Know-how / 人性化收束层评测器 / bad-case 诊断）串成一套**可复用的 Agent 产品化方法论**，并显式覆盖四要素：**需求定义 / 体验设计 / 评估维度 / 常见问题清单**。
> **状态**：v1.0 · 2026-05-24（5 月窗口内收口）· 作者 秦宇龙
> **配套 KR 分析**：`C:\Users\QYL\Desktop\OKR\.planning\kr\O3-KR2.md`

---

## 0. 导言：什么是「Agent 产品化」

普通 LLM 应用关注「模型怎么回答得更好」；**Agent 产品化**关注的是一套更完整的工程问题：让一个**有记忆、能调工具、要对外产生后果**的 Agent，在每一轮交互里都能**理解对、判断对、交付对、并在该停的时候停下来**——而且这件事必须可写成规范、可设计成体验、可度量、可回归。

这套方法沉淀自 4-5 月围绕 Loona / Rowboat 的四条实战主线，恰好对应四要素：

| 要素 | 主干实战产物 | 一句话 |
|---|---|---|
| 需求定义 | **Loona-Spec（Know-How）v1.0** | 把「Agent 该做什么」写成 223 条可机检需求 |
| 体验设计 | **Loona 用户体验 Know-how** + 交互四环节 + 结果卡分类 + Agent-UI 通用范式 | 把交互拆成可复用的能力与载体分工 |
| 评估维度 | **可观测+评测体系三层** + **人性化收束层评测器** | 把「好不好」拆成确定性指标 + LLM judge + 外部校准 |
| 常见问题 | bad-case 方法诊断 + 评测器抓到的真实失败模式 | 把散点 bug 聚合成可复用的「问题→根因→应对」清单 |

核心产品观（贯穿全文）：**Agent 不是回答机器，而是「控制权分配器」**——它判断什么时候替用户省心、什么时候必须把后果交还用户拍板。

---

## 1. 要素一 · 需求定义：把 Agent 需求写成可机检规范

**主干证据**：Loona-Spec（Know-How）v1.0
[飞书](https://f4x6dn8llc.feishu.cn/docx/ROGudTNWPoF2pdx9FHccEH35nmg) · GitHub `lala1137273514/loona-spec` · 本机 `Loona-Knowledge-System`

### 方法：需求不是话术，是「行为一致性规范」

Loona-Spec 的定位明确——**它不是话术库，是 Agent 操作系统**。普通 prompt 管「怎么说」（要温柔、聪明、简洁）；这套规范管「怎么想 → 怎么判 → 怎么推 → 怎么交」。它对标 WCAG/POSIX 那一类**行为一致性规范**，但符合性由 LLM 软判定（"提案级"而非"已采纳"）。

**写法 1 · 四/三层架构**（让规范既稳又能落到每个场景）：
- **Layer 0 全局协议**：Loona「始终是谁」——六条核心原则（理解 / 补全 / 记忆 / 感知 / 交付 / 边界）+ 全局优先级（安全 → 用户偏好 → 场景规则）+ 每轮必判决策字段（请求类型 / 主需求 / 情绪 / 连续性）+ 信息槽位分级 + **动作风险分级 P0/P1/P2**。
- **Layer 1 场景 Know-how**：9 个场景（陪聊 / 天气 / 新闻 / 邮件 / 日程 / 邮件日程联动 / 餐厅 / 旅行 / 会议总结）的执行链路与交付规则。
- **Layer 2 评测与治理**：风险注册表 / 证据注册表 / Active State 规则 / Component Schema / Eval Cases / 上线验收。

**写法 2 · RFC2119 分级的可机检需求**：223 条机检需求，按 blocker 64 / major 147 / minor 12 分级（MUST / SHOULD / MAY），每条 MUST 至少绑一个可评分用例（Eval Case Pack）。这把「需求定义」直接接到了「评估维度」——需求写出来就能被打分回归。

**写法 3 · 核心产品思想固化为需求**：「控制权分配器」——判断可由 Agent 代劳，**后果必须由用户拍板**。落成动作风险分级：P0 查询/总结/推荐/起草可自动；P1 需确认；P2（发送/改日程/删除/支付/长期记忆写入）必须用户执行。

**成熟度（v1.0）**：8 个质量闸门 G1-G8 全绿，可用于团队对齐与 PPT 演示；下一轮加强方向是把 Schema 拆成机器可读文件、Eval Case 拆成 YAML/JSON、补跨场景混合用例。

> **可复用结论**：一份合格的 Agent 需求文档 = 全局协议（人格/边界/风险分级）+ 场景链路 + 一套带分级、每条可机检、能直接喂给 planner/UI/TTS/评测的需求条目。

---

## 2. 要素二 · 体验设计：交互链路 + 载体分工 + UI 范式

**主干证据**：
- Loona 用户体验 Know-how [飞书](https://f4x6dn8llc.feishu.cn/docx/T0j6d5M9So4oRuxrEEpcBrCIndg)
- 交互四环节链路 + 结果卡分类（与何尔宁）[飞书](https://f4x6dn8llc.feishu.cn/docx/R20UdZMlco0w6LxYmj0co62gnsd)
- Agent 任务状态反馈 UI 通用范式（本机 `Loona Deskmate\2需求文档\Agent任务与能力\`，5/13）
- CC Persona 性格+人性化 [飞书](https://f4x6dn8llc.feishu.cn/docx/KHtldKia5omBQJxigQicnuAznGe)

### 方法 1 · 交互四环节：开始 → 澄清 → 执行 → 结果

把每一轮 Agent 交互拆成稳定的四环节链路，每个环节有明确的设计规则：
- **开始**：先判用户要的是哪类帮助（情绪承接 / 信息扫读 / 决策代劳 / 工具行动 / 风险校准）——同一句话在不同状态需要不同回应。
- **澄清**：能补的不问、该问的一轮解决。缺必填才问，低影响默认，**不把推荐变成表单**；误解时用 conversational repair（给两个重述方向）而非「请重新输入」。
- **执行**：干活有存在感不抢戏（"正在查…"），P0 主动推进、P1/P2 进确认态。
- **结果**：只说用户关心的（发给谁 / 改到几点 / 哪步失败）；内部 id / 工具字段 / trace / JSON **不进主回复**。

### 方法 2 · 五种产品能力（按能力写，不按场景堆）

用户体验 Know-how 的关键方法论选择：**不按「聊天/新闻/邮件」逐项堆规则，而按 Agent 应具备的产品能力写**，因此可跨场景复用：
1. **情绪承接**——识别"只陪不解"信号（烦/丢脸/算了…），接住原话、降压、留在现场。
2. **信息扫读**——把信息压成可立即行动的主线；inbox 变行动队列（必处理/可留意/可略过）；日程变应对策略而非时间表。
3. **决策代劳**——默认给一个主张（主张+理由+亮点+边界），不甩五选一菜单；推荐必须带可执行细节。
4. **记忆使用**——隐式贴合结果，**不表演"我记得你"**（禁说"根据你的用户画像"）；缺信息时只问一个关键问题或给默认。
5. **可执行 skill path**——信息后面接动作；**草稿与发送分开**（可主动 draft，不默认发送/改日程）；单条展开沿用户注意力走，不重开全局总结。

### 方法 3 · 载体分工（口播 / 卡片 / 文档 / TTS）

- **口播讲判断**（要不要带伞、哪封先处理），**卡片放证据**（邮箱、完整标题、来源层级、时间、链接），**文档承载方案**（旅行规划、深度汇总）。
- **结果卡三/九分类** + Component Schema：UI 卡片 / TTS 播报有结构定义；9 场景 UI/TTS/卡片/文档分工已明确。
- **TTS 对应规则**：口播**不念邮箱地址、不念完整长标题、不念内部字段**——念什么由载体分工决定（这条直接预防了「TTS 念标点 / 邮箱被切段」类问题，见要素四）。
- **Agent-UI 通用范式**：Agent 任务状态反馈 UI 的可复用范式（任务进行态 / 关键词气泡 / 状态一致性），跨 Agent 通用。

> **可复用结论**：体验设计 = 四环节链路（每环节有判断/确认规则）× 五种产品能力（跨场景）× 载体分工（口播/卡片/文档/TTS 各司其职）。

---

## 3. 要素三 · 评估维度：三层评测 + 收束层评测器 + 可感知指标

**主干证据**：
- 方向介绍：可观测+评测体系 [飞书](https://f4x6dn8llc.feishu.cn/docx/PDvBdqJ3Qo6OBQxnasZcghkwnmL)
- 人性化收束层评测器—成果展示 [飞书](https://f4x6dn8llc.feishu.cn/docx/CdnJdNJlyo7tvDxiOMBcR1fbnoc) · 本机 `C:/Users/QYL/Desktop/rowboat` `evals/humanization/DESIGN.md`
- Rowboat 收束层 Benchmark v1（112 条 ground-truth）[飞书 sheet](https://f4x6dn8llc.feishu.cn/sheets/TE54sr459hGX7stykO4clNnLnzc)
- Agent 相关指标（本机 `Loona Deskmate\评估\`）

### 方法 1 · 评测三层（可观测 / 确定性指标 / LLM judge）

1. **可观测层**：Langfuse trace——把 Agent 每一步（router/planner/工具/收束）落成可追溯 trace，是一切度量的地基。
2. **确定性指标层（零方差，承重）**：纯代码、无 LLM、可重放。这是护城河级资产——结论**判官无关**。
3. **LLM judge 层**：G-Eval 评委（rubric、temp 0、JSON、A/B 位置随机化），度量人格/像不像人/语域校准这类**只能软判**的维度。

**核心原则（强可复用）**：评测价值是**非对称**的——确定性那一半零方差可证；LLM judge 那一半的**质量上限 = 评委模型本身**。所以「事实门用确定性的，人格/过度改写别用弱模型自评，用强评委（Claude）」。

### 方法 2 · 人性化收束层评测器（一个完整范例）

度量 `humanizeLoonaResponse`（把 LLM 输出改写得像人、保人格、绝不损坏事实）。三个必须同时防的失败模式，**优先级词典序：facts > persona > human-likeness**。
- **A 层 确定性指标**：`evidence_diff`（受保护 span——路径/hash/命令/数字/报错/版本/引号 id——逐字存活，**唯一硬 FAIL 闸门**）、`burstiness`（句长波动）、`gptism_density`（AI 套话密度）、`structure_deviation`（报告腔痕迹）。
- **B 层 LLM judge**：`persona_fidelity` / `human_likeness` / `scene_calibration` / `humanlike_preference` / `overcorrection`（仅信息层损坏）+ 中文 note。
- **复合门**：词典序一票否决（一个 JS 纯函数，不取均值）：ev=0→FAIL，overcorrection→OVERCORRECTED，pf<3→CAPPED，pf==3 且该场景期待声音→DILUTED，scene≤1→OFF_SCENE，否则 PASS。
- **外部校准**：盲评 Claude 100% 复现作者标注；qwen-plus 84.3%（κ=0.727）——证明 benchmark 标签不是单模型偏好。
- **复用性**：人格是声明式参数（`personas{cc, loona-deskmate, neutral}`），加新 Agent = 注册表 + 种子，**零评测器代码**；CC 重构后字节级零回归（确定性回放 83/83 = 100%）。
- **Benchmark**：112 条 ground-truth（5 scene × 7 scenario × 3 persona + 13 对抗边界用例）；准确度按 judge-dependent / deterministic 拆分上报，防确定性用例灌水。

### 方法 3 · Agent 可感知指标

用户**可感知**的指标体系（本机 `Loona Deskmate\评估\Agent相关指标`）：任务结果 / 过程体验 / 对话质量 / 状态一致性——评测不只看内部正确性，更要看用户那一端能否感知到「做对了」。

> **可复用结论**：评估维度 = 可观测（trace）打底 + 确定性指标做铁闸门 + LLM judge（必须外部校准、用强评委）做软判 + 可感知指标对齐用户体感；判定逻辑用词典序门而非取均值。

---

## 4. 要素四 · 常见问题清单（重点补全）

> 把分散在 bad-case 诊断、评测器成果、测试集会议、深度问题报告里的真实失败，聚合成一张可复用清单。每条：**问题 / 典型表现 / 根因 / 应对方法**。证据散见 4/15 测试集构建会、5/18 bad-case 诊断、收束层评测器成果展示、Loona-Spec、UX Know-how。

### A 类 · 对话/生成质量

| # | 问题 | 典型表现 | 根因 | 应对方法 |
|---|---|---|---|---|
| 1 | **重复回复** | 同一意思反复说、车轱辘话 | 上下文管理弱 / 无去重；未沿用户注意力推进 | 测试集三痛点之一固定考察（[4/15 测试集构建会](https://f4x6dn8llc.feishu.cn/docx/PCtRdfBwEoTaBLxKryfcG7MwnAF)）；交互四环节「结果」环节只说增量；`burstiness` 诊断 |
| 2 | **幻觉 / 编造事实** | 编招牌菜、编来源、编没发生的进展 | 工具无证据时硬编；改写时捏造 | 证据协议（引用来源/标注置信度/暴露不确定性）；无证据把推荐理由放在场景匹配上而非编内容；`overcorrection` judge 维度抓捏造 |
| 3 | **上下文承接断裂** | "第二条展开"重做全局；切场景丢前文 | Active State / 指代消解缺失 | Loona-Spec Layer 0 Active State 规则（连续/指代/场景切换）；单条展开「沿用户手指走」 |
| 4 | **AI 套话 / 报告腔（blandification）** | "综上所述""值得注意的是""很高兴帮到你"；人格被磨平成客服腔 | 模型默认回归礼貌通用助手；收束层过度改写 | `gptism_density` + `structure_deviation` 确定性诊断；judge `persona_fidelity<3 → CAPPED`；UX Know-how「语气服务任务不抢戏」 |

### B 类 · 收束/改写层（humanizer 真实 bug）

| # | 问题 | 典型表现 | 根因 | 应对方法 |
|---|---|---|---|---|
| 5 | **事实损坏（改写丢/改 protected span）** | 把 commit hash/路径/命令/数字/版本改错（实测 `v1.2`→`v1.1.2`） | humanizer 改写时未保护关键 span | `evidence_diff` 确定性硬闸门（受保护 span 逐字存活，唯一硬 FAIL）；实测真实生产 humanizer **约 23% evidence_diff FAIL** |
| 6 | **过度改写（overcorrection）** | 丢关键警告/事实、语义糊、自相矛盾 | 为「像人」牺牲信息层 | judge `overcorrection` 维度（仅信息层）；词典序门 facts>persona>human |
| 7 | **弱评委漏判** | qwen 偏松、漏判 blandification/捏造、run 间抖动 | 用弱模型做 LLM judge | 评测器外部校准；人格/过度改写层「用 Claude 不用 qwen 自评」；新人格 byPersona 先 Claude 回放复核 |

### C 类 · 评测方法本身的坑

| # | 问题 | 典型表现 | 根因 | 应对方法 |
|---|---|---|---|---|
| 8 | **精确匹配假阴性** | 刘雪峰 4 条 bad-case「看着错其实对」 | 用 `String.includes`/全字段精确匹配当尺子，产生假阴性 | **结论：是评测方法问题不是模型 bug**；尺子按字段分层（Router 弱包含 / Planner 强匹配）；验收标准归产品定义权（[5/18 诊断](https://f4x6dn8llc.feishu.cn/docx/F4nfdN81poj4A4xkgLSc0Wz3n8b)） |
| 9 | **确定性用例灌水头条** | 评测准确率虚高 | 确定性用例 `includes` 白送分混进总分 | benchmark 准确度按 judge-dependent / deterministic 拆分上报，头条只算判官辨别力 |
| 10 | **松评测器（奖励坏输出/误伤合法改写）** | 假装锋利但矛盾原文却 PASS；合法改写被误判 | 评测器边界设计松 | 13 条对抗边界用例（fake_sharp_ooc→OVERCORRECTED、legit_rephrase→PASS）专打门边界 |

### D 类 · 「接线在但行为错」与 UI/TTS

| # | 问题 | 典型表现 | 根因 | 应对方法 |
|---|---|---|---|---|
| 11 | **接线在但行为错（静态检查盲区）** | 工具/接口都接上了，端到端行为却错 | 静态/单测查不到行为级偏差；规范只查"有没有"不查"对不对" | Loona-Spec 定性为 behavioral conformance spec；每条 MUST 绑可评分用例做行为级验收（209 case 真验收）；Cortex 5/20 深度问题报告 |
| 12 | **TTS 念标点 / 念邮箱 / 邮箱被切段** | 口播把邮箱地址、长标题、标点一起念出来 | 载体分工缺失，口播直接念了该进卡片的内容 | 载体分工：口播只讲判断主线，邮箱/完整标题/字段进卡片；UX Know-how「口播不念邮箱地址」 |
| 13 | **卡片乱码 / 信息错位** | 卡片字段渲染异常、结构对不上 | Component Schema 未统一 | Layer 2 Component Schema 统一定义 UI 卡片/TTS 结构 |
| 14 | **长链路延时** | 多步 workflow（读→查→起草→确认→写入）端到端慢、无存在感 | 长链路无中间反馈 | Agent-UI 任务状态反馈通用范式（进行态/存在感）；执行环节"正在查…"反馈 |
| 15 | **静默高危动作** | 未确认就发邮件/改日程/删除 | 把 P2 当 P0 自动执行 | 动作风险分级 P0/P1/P2；草稿与发送分开，P2 必须用户拍板 |
| 16 | **任务失败不诚实 / 部分成功不交代** | 失败装成功、部分成功不说哪步挂了（Cortex task 失败约 6.25%） | 缺失败处理协议 | Layer 0 失败处理（诚实暴露/部分成功/降级路径）；结果只说用户关心的「哪步失败」 |

**清单合计：16 条**，分 A 对话质量(4) / B 收束改写(3) / C 评测方法(3) / D 行为·UI·TTS(6) 四类。

---

## 5. 小结：这套方法如何指导 6 月及后续

1. **需求先行**：新场景/新 Agent 一律先写成 Loona-Spec 式规范（全局协议 + 场景链路 + RFC2119 可机检需求 + 风险分级），需求即验收尺子。
2. **体验按能力复用**：用「四环节 × 五能力 × 载体分工」框架做交互设计，而非逐场景堆规则——6 月新场景可直接套。
3. **评测嵌进开发**：trace 打底、确定性指标做铁闸门、LLM judge 必外部校准用强评委；判定用词典序门。收束层评测器已可零代码挂新 Agent 人格。
4. **常见问题清单当 checklist**：本文第 4 节 16 条直接作为开发自检 + code review + 上线验收的 checklist，新发现的 bad-case 持续按「问题/表现/根因/应对」回流扩充。
5. **下一步收口**：把 Schema 拆成机器可读文件、Eval Case 拆 YAML/JSON、补跨场景混合用例、推进人类标定（评测器 future work）。

> **一句话**：这套方法把 Agent 产品化从「靠手感」变成了「需求可机检、体验有框架、评测有铁闸门、问题有清单」的可复用工程闭环。

---

## 5.5 收口补遗（W7 + 周末，5/25–5/31）：方法第一次跑穿真功能

> 5/24 总纲成型后，W7 用一条真实功能（旅行规划 v1）把四要素从「方法论存在」走到「被一条功能完整用上」，5/31 DDL 收口。本节为补遗证据，不改前文框架。

- **要素一·需求定义** 在旅行规划 v1（T1）上验证：边界/槽位/主 prompt+澄清子 prompt+口播子 prompt/TravelPayload 数据契约/12 条 A1-A12 验收场景五件套齐全，需求写出来即可机检回归。
- **要素二·体验设计** 落到载体分工实战：日程/邮件轮播由「逐条」重构为「按天聚合单卡」、口播升级为主要内容载体（每卡 2-4 句、不泄露内部切分机制）、卡片切分统一公式 span=ceil(总天数/5) 替代经验分档；澄清卡（name=clarify+type=question）成为追问用户的标准载体。
- **要素三·评估维度** 扩到 700+ case 回归框架（router 200 + planner 520+，76.8%→目标 85%）+ 分级执行（P0/P1 跑 3-5 次、P2/P3 跑 1-2 次）+ 失败重跑规则；prompt_opt golden+rubric+judge 回归闭环持续迭代。
- **要素四·常见问题清单** 新增真实失败：旅行卡轮播中消失、日程删除确认卡失效、新闻轮播留白、回复啰嗦——均已回流为「问题/表现/根因/应对」并进 530 问题跟踪。
- **CC 风格化提示词**定稿（两步管道：先去模板说人话 → 再注入人格上色；事实保真>风格>人性化收束；protected spans 1:1 保留；毒舌 Lv0-3；提交前两遍回读）[飞书](https://f4x6dn8llc.feishu.cn/docx/FhtSd9xAQobIJzxwXgjcIcynnyp)，是要素二/四的可复用范例。
- **周末（5/30-31）persona 收尾**：口语化重写、移除未接入 Whispering、配置平台二次迭代——产品化方法在人设线完成端到端验证。
- **收口结论**：O3-KR2「产品化方法沉淀（4 要素总纲）」5/31 DDL 达成 100%，方法已可复用于 6 月新场景。

---

## 附录 · 证据索引

| 要素 | 证据 | 链接/路径 |
|---|---|---|
| 需求定义 | Loona-Spec（Know-How）v1.0（223 条机检） | [飞书](https://f4x6dn8llc.feishu.cn/docx/ROGudTNWPoF2pdx9FHccEH35nmg) · GitHub `lala1137273514/loona-spec` · 本机 `Loona-Knowledge-System` |
| 需求定义 | know-how 对齐（Spec=交互规范/分层规则/澄清一次完成） | [飞书](https://f4x6dn8llc.feishu.cn/docx/VpiZdZTi0oW0aJxf982cLklgnZf) |
| 体验设计 | Loona 用户体验 Know-how | [飞书](https://f4x6dn8llc.feishu.cn/docx/T0j6d5M9So4oRuxrEEpcBrCIndg) |
| 体验设计 | 交互四环节 + 结果卡分类 | [飞书](https://f4x6dn8llc.feishu.cn/docx/R20UdZMlco0w6LxYmj0co62gnsd) |
| 体验设计 | Agent 任务状态反馈 UI 通用范式 | 本机 `Loona Deskmate\2需求文档\Agent任务与能力\` |
| 体验设计 | CC Persona 性格+人性化 | [飞书](https://f4x6dn8llc.feishu.cn/docx/KHtldKia5omBQJxigQicnuAznGe) |
| 评估维度 | 方向介绍：可观测+评测体系 | [飞书](https://f4x6dn8llc.feishu.cn/docx/PDvBdqJ3Qo6OBQxnasZcghkwnmL) |
| 评估维度 | 人性化收束层评测器—成果展示 | [飞书](https://f4x6dn8llc.feishu.cn/docx/CdnJdNJlyo7tvDxiOMBcR1fbnoc) · 本机 `rowboat/evals/humanization/DESIGN.md` |
| 评估维度 | 收束层 Benchmark v1（112 条） | [飞书 sheet](https://f4x6dn8llc.feishu.cn/sheets/TE54sr459hGX7stykO4clNnLnzc) |
| 评估维度 | Agent 相关指标（可感知） | 本机 `Loona Deskmate\评估\Agent相关指标` |
| 常见问题 | 测试集构建会（重复回复/幻觉/上下文承接三痛点） | [飞书](https://f4x6dn8llc.feishu.cn/docx/PCtRdfBwEoTaBLxKryfcG7MwnAF) |
| 常见问题 | 刘雪峰 4 条 bad-case 诊断（精确匹配假阴性） | [飞书 5/18 日报](https://f4x6dn8llc.feishu.cn/docx/F4nfdN81poj4A4xkgLSc0Wz3n8b) |
| 汇总 | 周报：Loona-Spec v1.0 + Protocol R4 真验收(209 case) + 评测器 v1.2 | [飞书](https://f4x6dn8llc.feishu.cn/docx/OBWJd7RtFo4tf6xHelucAqjnnAe) |

*v1.0 · 2026-05-24*
