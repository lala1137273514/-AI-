# O4-KR4 反推-映射分析

> **KR**:针对 6 月 30 日版本制定验收标准和关键 Case(核心/异常/风险场景),推动上线前验收完成。
> **O4**:跟随版本迭代完成 Agent 需求输出、测试协同与交付跟进,支撑版本高质量落地。
> **KR id** `7628430235122666701` ｜ **名义时间窗** 6 月 ｜ **周次** W6(5/18-24)起前置基础设施密集成型,正式期(6 月)未到
> **关键区分**:**"验收基础设施已建(进行中,W5-W6 大量产出)"** vs **"针对 6.30 版本的正式验收(要 6 月做,今天 5/24 未到期)"**。本 KR 据"基础设施成熟度 + 前置预演"评分,正式验收本身留待 6 月。

---

## 一、反推:为达成该 KR,每周应做什么 + 应有产出

| 周 | 应做什么 | 应有产出 |
|---|---|---|
| W4-W5(铺垫) | 沉淀验收方法论(评测分层/judge)+ 关键 case 体系 | 评测器两层(确定性指标+LLM judge);Backlog 与验收场景;case 库 |
| W6(5/18-24) | 把验收标准与关键 case 工程化、可执行;做前置真验收预演 | Loona-Spec 209 case 三层验收框架 + harness 自迭代真验收;rowboat 评测器 112 case benchmark |
| 6 月(未到) | 针对 6.30 版本正式验收 + 推动上线前 close | 6.30 版本验收报告 + bug close + 上线放行 |

**判定标准**:① 有可执行的验收标准(分层 PASS 标尺/judge);② 有覆盖核心/异常/风险三类场景的关键 case;③ 推动上线前验收——基础设施期看"是否已能跑真验收并暴露问题",正式期(6 月)看"6.30 版本验收闭环"。

---

## 二、实际产出(四源证据 · 时间范围 / 成果描述 / 产物链接)

| 时间范围 | 成果描述 | 产物链接/路径 |
|---|---|---|
| 04-08 | 4.14 场景 case 集(验收版,核心场景 case 起点) | 本机 `Loona Deskmate\4.14\` |
| 04-17 | MVP 评测考察场景:Router 弱包含/Planner 强匹配**断言法则**(验收标准雏形) | 本机 `Loona Deskmate\评估\` |
| 05-07 | Session:Slack 消息管理 case 6.1-6.23 **产品验收评审**(逐 case 可行性,异常/消歧场景) | Claude 会话(W4) |
| 05-14~18 | Session(rowboat):人性化收束层**评测器两层标准**(确定性指标 evidence_diff + L2/L3 LLM judge)+ 60 seed/20 golden 可交付清单 | rowboat 会话(W5-W6) |
| 约5月下 | **人性化收束层评测器—成果展示**:独立可跨 Agent 复用评测器 + ground-truth benchmark;事实门铁闸+人格评委(异常/风险场景门控) | [飞书](https://f4x6dn8llc.feishu.cn/docx/CdnJdNJlyo7tvDxiOMBcR1fbnoc) |
| 约5月下 | **Rowboat 人性化收束层 Benchmark v1(112 条 ground-truth)**(关键 case 数据集) | [飞书](https://f4x6dn8llc.feishu.cn/sheets/TE54sr459hGX7stykO4clNnLnzc) |
| 05-19 | Session(rowboat):评测器全量构建 + shuorenhua 66 条语料并入(SF→slop_recall、SNF→误杀门)+ Langfuse 真 trace 跑通;results 868→251 清理 | rowboat 会话(W6) |
| 05-18 | Session:评审 agent 测试群 + 4 条 bad-case → **"验收标准是产品定义权""尺子按字段分层"**(验收方法论定调) | Claude 会话(W6) |
| 05-19 | Session(rowboat):核对飞书测试集标注,查出域名矛盾(4 条)+判定规则指向不存在工具(6 条)(关键 case 质量门) | rowboat 会话(W6) |
| 05-20 | Session(Jarvis):检查 agent 模块场景 case CSV(49 条 Case 库),按严重度列硬伤 | Jarvis 会话(W6) |
| 05-21 | Session(Jarvis):全栈对齐 **Loona Agent Interaction Protocol(24 章/6 原则/9 卡/40+Case/8 验收 checklist)** = 验收标准框架 | Jarvis 会话(W6) |
| 05-22 | Session(Jarvis,/goal harness 自迭代):**三层全 PASS 标尺真验收**:schema **209/209**、LIVE **102/125(81.6%)**、state-inject 36/36、halo ~98%;修 7 个 live bug(前置验收预演) | Jarvis 会话(W6) |
| 05-22 | **Loona-Spec (Know-How) v1.0**:223 条机检需求(MUST/SHOULD/MAY)+ 9 卡 schema + golden cases,定性 behavioral conformance spec(验收标准本体) | [飞书](https://f4x6dn8llc.feishu.cn/docx/ROGudTNWPoF2pdx9FHccEH35nmg) |
| 05-18~22 | 周报:Loona-Spec v1.0(223 条机检)+ **Protocol R4 真验收(209 case)** + 评测器 v1.2 收尾 | [飞书](https://f4x6dn8llc.feishu.cn/docx/OBWJd7RtFo4tf6xHelucAqjnnAe) |

---

## 三、逐周映射(反推 vs 实际)

| 周 | 反推要求 | 实际 | 覆盖 |
|---|---|---|---|
| W4-W5(铺垫) | 验收方法论 + case 体系 | 评测器两层标准 + Slack case 验收评审 + 评测数据集清单 | ✅ 达成 |
| W6(5/18-24) | 验收标准/关键 case 工程化 + 前置真验收预演 | Loona Protocol 8 验收 checklist + Loona-Spec v1.0 223 条 + 209 case 三层验收(schema 209/209、LIVE 102/125)+ rowboat 评测器 112 case benchmark + case 库质量门 | ✅ 超额 |
| 6 月(未到) | 6.30 版本正式验收 + 上线前 close | 未开始(KR 时间窗在 6 月) | 🔴 未到期 |

**三维判定**:验收标准 ✅ 超额(Loona Protocol 8 验收 checklist + Loona-Spec v1.0 223 条机检 + 评测器两层标尺,均可执行)｜关键 case 三类场景 ✅(209 case schema 三层 + 125 LIVE + 112 条 benchmark + shuorenhua 误杀门覆盖异常/风险)｜推动上线前验收 🟡 基础设施已能跑真验收并暴露 7 bug(预演完成),但**针对 6.30 版本的正式验收 🔴 未到期**。

---

## 四、结论与 Gap

- **结论:验收基础设施已建成且超额、并完成前置真验收预演;但"6.30 版本正式验收"按定义在 6 月,今天 5/24 未到期。** 必须区分两层:
  - **基础设施层(已达成 · W5-W6)**:Jarvis 的 Loona Protocol 8 验收 checklist + 209 case 三层验收框架(schema 209/209、LIVE 102/125、state-inject 36/36)、Loona-Spec v1.0(223 条机检 + golden cases)、rowboat 评测器两层标准 + 112 条 ground-truth benchmark + shuorenhua 误杀门。验收标准、关键 case(核心/异常/风险)、可执行的判分标尺三者齐备,且已用 harness 自迭代真跑通并抓出 7 个 live bug——这等同于一次**预演性上线前验收**。
  - **正式验收层(未到期 · 6 月)**:这些 case 和标尺目前跑的是 Jarvis/rowboat 工程内的 Loona Protocol 对齐,**尚未对"6.30 发货版本的实际构建物"做正式上线前验收**。
- **Gap**:
  1. **验收对象错位/待对齐**:现有 209/112 case 围绕 Loona Protocol 与评测器自身,需在 6 月映射/裁剪为"6.30 版本验收 Case 集"并绑定实际发货构建物。
  2. **正式验收闭环(过会标准、上线放行、bug close 跟踪)未启动**——属 6 月主体工作。
  3. 验收标准散落在 Jarvis(8 checklist)、Loona-Spec(223 条)、rowboat 评测器三处,**尚未收口成一份"6.30 版本验收标准"统一文档**。

## 五、建议动作

- **进度/打分**:建议 **progress 40~50%、score 暂不结分(进行中,标 0.4~0.5 或留空待 6 月)**。验收基础设施与前置预演已占该 KR 的相当比重,但正式验收(6 月)是后半程核心,故不宜按完成结分。
- **写 1 条进展记录(草稿)**:
  > 为 6.30 版本验收提前搭好基础设施并完成前置预演:制定可执行验收标准——Loona Agent Interaction Protocol 8 项验收 checklist + Loona-Spec v1.0(223 条机检需求,含核心/异常/风险分层)+ 评测器两层标尺(确定性指标 + LLM judge);沉淀关键 case——209 case 三层验收框架(schema 209/209、LIVE 102/125、state-inject 36/36)、rowboat 112 条 ground-truth benchmark、shuorenhua 误杀门;并用 harness 自迭代做了一次真验收预演,暴露并修复 7 个 live bug。6 月将把这套标准与 case 映射到 6.30 发货版本,推动正式上线前验收闭环。
- **6 月跟进重点**:① 把 209/112 case 裁剪映射为《6.30 版本验收 Case 集(核心/异常/风险)》并绑定实际构建物;② 收口一份统一《6.30 版本验收标准》;③ 走正式上线前验收 → bug close → 放行,形成验收报告。
