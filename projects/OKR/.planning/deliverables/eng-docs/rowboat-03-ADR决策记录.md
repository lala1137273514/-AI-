# rowboat · 设计决策记录 (ADR)

> ADR 式关键取舍与教训。每条：背景 → 决策 → 理由 → 后果/教训。
> 来源：`evals/humanization/DESIGN.md`（§0-§19）+ `.planning/v1.3-MEMORY-LOOP-DESIGN.md` + `.planning/codebase/ARCHITECTURE.md` + `CLAUDE.md`。

---

## ADR-1：确定性事实门先于 LLM judge —— `facts > CC style > human-likeness` 字典序门控

- **背景**：人性化收束层把 LLM 答案改写得更像人。风险：改写可能腐蚀事实（commit hash/路径/版本号被改），或把 CC（故意刻薄的技术搭档 persona）的锋利钝化成温柔客服腔。
- **决策**：优先级是**字典序非加权**（`facts > CC style > human-likeness`），编码进一个 `composite` JS 函数（非加权均值）：① `evidence_diff==0` → FAIL（受保护 span 没逐字存活，任何文笔分救不回）；② `persona_fidelity<3` → CAPPED（钝化封顶，bland 永远拿不到"好"分）；③ overcorrection → OVERCORRECTED；④ 过双门后才由 human_likeness+preference 定分。
- **理由**：通用 naturalness/warmth 评测会把 CC 的锋利打成"不友好"，正好奖励 spec 禁止的 blandification。事实门是纯代码、零方差、judge-independent，是整个评测器最强的保证。
- **后果**：`evidence_diff` 是唯一硬 FAIL，最先建最先测；§7 内置 adversarial golden（改一位 commit hash digit 的高质量 CC 改写）必判 FAIL，用 stubbed judge 无网络可复现。判官 prompt 显式反 blandification（锋利是 persona 特性，不奖励温柔/客服腔/删"boss"求中性）。

## ADR-2：win-rate 是主指标，不能平均分类变量

- **背景**：`humanlike_preference` 是 pairwise 分类值 {original, tie, humanized}，不能取均值。
- **决策**：主数字 = dataset-level win-rate（run-evaluator 算，非 item 均值）：`winrate_humanized = (#humanized + 0.5·#tie)/N`；配 `fail_rate`（事实腐蚀率）+ `cap_rate`（钝化率）**三件套一起报**。pairwise 用 A/B 随机序去位置偏置。
- **理由**：一个更平滑但更 bland 的改写不能"赢"——只有更像人**且**保 persona **且**保事实才算赢。win-rate 单独不够，必须三件套。
- **后果/教训**：一个改写只"更平滑"时 preference 调整为 +0.5（不足以独自抬分），original 胜则 -1.5。

## ADR-3：生产 trace ≠ pair —— mode 显式区分，避免对真实流量误 FAIL

- **背景**：把 pair-mode 字典序门跑在真实生产 trace 上，**误 FAIL** 了真实 trace（任务系统提示词带 53 个路径/ID，短答案 echo 不全 → evidence_diff=0 → FAIL）。
- **决策**：`mode` 显式。`pair`（fixtures/--experiment）：全门，evidence_diff 硬 FAIL；`production`（--score-back）：evidence_diff → 信息性 `input_fidelity`（非门控），surface-aware 生产 verdict（OK/SLOPPY/WEAK_PERSONA/OVERCORRECTED）。
- **理由**：单条生产 trace 没有 `(original, humanized)` 对——generation observation 就是输出，humanizer 是后置 pass。
- **后果**：发现 100% 真实 trace 是 `note_tagging_agent`/`knowledge_sync`（humanizer 从不碰的内部结构化 agent），对它持 CC bar 是范畴错误 → `classify.mjs` 把 agent/tags 映射成 surface∈{internal, user-facing}，internal surface 不期望 CC persona。

## ADR-4：benchmark 要有"牙" —— 故意做难，用 adversarial 层分辨弱判官

- **背景**：第一版 benchmark 太宽（30 个漫画式极端 case），两个判官都 ~97-100%，测的是"能不能分辨卡通英雄和卡通反派"，不是真实校准。
- **决策**：v2 硬化：拆 headline 为**judge-discernment accuracy**（仅 judge-dependent case），确定性 case（fact_broken/legit_rephrase）分开报不灌水；加 **adversarial 层 13 boundary case**（diluted_persona/fake_sharp_ooc/fabricated/scene_mismatch/subtle_corruption…）；门重排（overcorrection 提到 facts tier，信息损害排在风格前）。
- **理由**：宽 benchmark 量不出判官强弱；危险模式（静默信息丢失、捏造、钝化、场景错配）才是 load-bearing。
- **后果**：headline 从假的 ~97% 落到真的 **qwen 74% / Claude 100%**，差距恰在危险模式上。教训沉淀：硬化 benchmark 立刻暴露了 (a) 门排序 bug、(b) overcorrection 定义不清（混进 persona）、(c) `evidence_diff` 对"3→三次"语义等价改写的 false-positive（保留在 benchmark，标 PASS 让缺口可见，列为未来工作）。

## ADR-5：跨 judge 一致性 —— 用盲独立模型证明 benchmark 不是自己批自己作业

- **背景**：benchmark 的 expected 标签是作者assign 的，公平质疑：是不是单模型/作者特异性？
- **决策**：`--cross-judge` 用两个独立判官（live qwen-plus + 盲 replay Claude，Claude 只见 scene+original+humanized，从不见 variant/expected）跑同一 pipeline，算 accuracy-vs-ground-truth + 原始一致率 + Cohen's κ。
- **理由**：盲独立模型复现作者标签才能去作者偏置。
- **后果**：Claude 盲跑 100% 复现 ground-truth，κ=0.727（substantial）；13 处分歧**全单向**（Claude=ground-truth，qwen 更宽松，从无反向）。两个诚实结论：(1) 去作者偏置 PASS；(2) **生产判官是弱链，不是 benchmark**——qwen 给 blandification 盖章、且漏掉 fabrication，生产 LLM-judge 层应用 Claude/同级模型，事实门（judge-independent）无论如何保留。

## ADR-6：复用现有判官形状 + 零依赖 .mjs，把评测器做成"可跨 agent 复用的仪器"

- **背景**：内置 no-code LLM-as-a-judge 是死路（单 prompt、单 call、无 pairwise、无门控）。
- **决策**：evaluator 是 SDK/CLI **脚本**（zero-dep `.mjs`，复用 `kb-lab/server/judge.ts` 的 proven shape：rubric in prompt / temp 0 / JSON out / 容错抽取 / clamp），dataset/run/score 仍在 Langfuse。judge LLM 注入（DI），SDK 不可导入时 fallback 到直接 `POST /api/public/scores`。后续 §18 把 evaluator **persona-参数化**（`{id, targetRegister, failureMode, voiceScenes}`），CC 用 verbatim legacy rubric by reference 保字节不漂移。
- **理由**：目标是**共享** benchmark + evaluator 每个 agent 都能用，不是 CC-only 仪器；事实门和 slop 信号本就 persona-agnostic，只有 persona-judgment 层硬编码。
- **后果**：加 persona = 加一个 registry 条目 + seeds，无 evaluator 代码改动；CC 全程 100%(83/83) 不动证明重构纯加性。

## ADR-7（v1.3 记忆回路）：三分流入口纯度 —— 真实记忆 / 运维诊断 / 待审隔离绝不混进同一注入文件

- **背景**：v1.2 后发现"召不回"症状（user.md 冻在 5/13、inbox 只增不减、Feishu 参会人乱码注入、低置信 KG 事实即丢）。根因不是缺功能——**零件都在，但桥断了、入口混了**。
- **决策（v1.3 核心契约）**：写入按性质分三类去三个**不同**目标：① 真实记忆（save-to-memory/偏好观察）→ `inbox.md` → 蒸馏 → user/preferences；② 运维诊断（Unknown attendee/sync 失败/conflict-lint 报告）→ 独立诊断面（**不进注入**）；③ 待审隔离（低置信 KG 事实）→ `Inbox-KG.md` + **必须有提升回路 drain 它**。
- **理由**：注入窗口被运维噪声和冲突复读污染（`loadAgentNotesContext` 裸注入 inbox 末尾 4000 字、42/74 行是冲突复读）；隔离了没提升 = 墓地。
- **后果/教训**：诊断出 #1 根因是**蒸馏器 livelock**（`agent_notes_agent` 1815 次"exiting loop: pending asks/permissions/confirmations"，0 次蒸馏——它杀死了整个 A 回路）；Inbox-KG 提升回路**整条缺失**（19 处全 append，无 read/promote）。v1.3 Phase 25 收编为单一 phase（B1 修 livelock 优先 → B2 蒸馏器重做 → B3 conflict-lint 去重改投 review 面 → B4 Inbox-KG 提升回路 → B5 kg_runner 增量去重 → B6 Feishu 编码归一 → B7 Mermaid 可视化）。

## ADR-8：knowledge/ markdown 是唯一事实源 —— 无向量库/图DB，召回非对称注入

- **背景**：要做"知识图谱"和记忆，但 solo dev 不想维护独立向量库/图DB。
- **决策**：plain markdown 在 `knowledge/` 是记忆的唯一事实源，backlink 是 Obsidian-style `[[...]]`，"知识图谱"由轮询服务写 markdown 构成。召回**非对称**：只 Session Persona + Agent Memory 自动注入（每 turn 读盘），KG/Source Log/Session Log 全工具访问。
- **理由**：local-first + solo dev，markdown 可人读可 grep，避免独立存储的运维负担；非对称注入控制 prompt 预算（KG 很大，不能全注入）。
- **后果/教训**：Phase 21 加 embedding cache（`~/.rowboat/embeddings/`，sha256 O(changed)）做 top-K 相似度，但不引向量库；KG 是 *memory* 不是 live inbox（召回链明确"实时外部状态走第三方工具，不查 KG"）。attention 层刻意**不在 chat runtime 内**（grep runtime.ts 0 命中），只驱动通知 UI——避免把通知逻辑混进召回。

---

*ADR 来源：`evals/humanization/DESIGN.md` §0/§4/§11/§13/§16/§17/§18 + `.planning/v1.3-MEMORY-LOOP-DESIGN.md` §1/§2/§3 + `ARCHITECTURE.md`。所有数字取自仓库文档原文。*
