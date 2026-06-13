# rowboat · HANDOFF / Runbook

> 运维交接手册：构建、运行、依赖、仓库状态、约束红线。
> 来源：rowboat `CLAUDE.md` + `.planning/codebase/STACK.md` + 仓库 git 状态。
> ⚠️ 只读交接说明。

---

## 1. 仓库状态（只读快照，2026-05-25）

| 项 | 值 |
|---|---|
| 路径 | `C:/Users/QYL/Desktop/rowboat` |
| 分支 | `main` |
| HEAD | `e61ae9f5` `docs(evals): DESIGN §19.4 + SHOWCASE 16.4 + NOTICE — full shuorenhua corpus` |
| 最新 tag | `v0.4.7`（GSD 里程碑 tag `knowledge-compounding-v1.2` @809d350d 标 v1.2） |
| 工作区 | 有未提交改动：`M .gitignore`、`M CLAUDE.md`；未跟踪 `.planning/v1.3-PHASE25-B7-MEMVIZ-SPEC.md`、kb-lab reports |

---

## 2. 构建 / 运行（apps/x Electron app）

```bash
cd apps/x && pnpm install          # 装依赖（pnpm 必需，workspace:* 协议）
cd apps/x && npm run deps          # 建 workspace 包：shared → core → preload
cd apps/x && npm run dev           # 开发模式（建 deps + 跑 app；renderer Vite :5173，main 等它再启）
cd apps/x && npm run lint          # lint
cd apps/x/apps/main && npm run package   # 生产构建 (.app)
cd apps/x/apps/main && npm run make      # 出 DMG
# 编译校验
cd apps/x && npm run deps && npm run lint
```

**构建顺序（依赖）**：shared(无依赖) → core(依赖 shared) → preload(依赖 shared) → renderer/main(依赖 shared+core)。
**为何 esbuild bundle**：pnpm 用 symlink 接 workspace 包，Electron Forge 的依赖walker(flora-colossus) 跟不了 symlink → esbuild 把所有依赖 inline 进单个 .cjs，`prune:false` + `ignore:[/node_modules/]` 跳过 node_modules。

| 组件 | 入口 | 产物 |
|---|---|---|
| main | `apps/x/apps/main/src/main.ts` | `.package/dist/main.cjs` |
| renderer | `apps/x/apps/renderer/src/main.tsx` | `apps/renderer/dist/` |
| preload | `apps/x/apps/preload/src/preload.ts` | `apps/preload/dist/preload.js` |

---

## 3. 数据 / 配置位置

- **工作区 + KB**：`~/.rowboat/`（或 `$ROWBOAT_WORKDIR`），无 server。
  - 知识库 markdown：`~/.rowboat/knowledge/`（People/Org/Projects/Topics/Meetings/Notes/Agent Notes…）
  - run JSONL：`runs/<runId>/`
  - embedding cache：`~/.rowboat/embeddings/`
  - 归档：`Agent Notes/archive/preferences-<YYYY-MM>.md`
- **LLM 配置**：`~/.rowboat/config/models.json`（`{provider:{flavor,apiKey?,baseURL?}, model}`），主模型 `qwen-plus` via DashScope OpenAI-compatible。models 目录缓存 `models.dev.json`。
- **运行时 env**：`ROWBOAT_WORKDIR`、`API_URL`、`POSTHOG_*`、`LANGFUSE_*`（`.env`/`.env.local`）、`COMPOSIO_API_KEY`。
- **打包签名 env（仅生产）**：`APPLE_ID`/`APPLE_PASSWORD`/`APPLE_TEAM_ID`。

---

## 4. 技术栈

| 层 | 技术 |
|---|---|
| Desktop | Electron 39.2.7 |
| UI | React 19.2 + Vite 7.2 + TailwindCSS 4.1 + Radix/shadcn(new-york) |
| AI | Vercel AI SDK `ai`^5.0.133；@ai-sdk openai/anthropic/google/openai-compatible；OpenRouter；Ollama |
| 集成 | @composio/core、@modelcontextprotocol/sdk（Fireflies/Slack/MCP）、googleapis（Gmail/Calendar/Drive）、openid-client |
| 观测 | @langfuse/otel + @langfuse/tracing（**纯 OTel tracing**，无 score/dataset）、posthog-node |
| 其它 | awilix(DI)、chokidar(file watch)、cron-parser(live-note)、express(本地 HTTP)、isomorphic-git(版本史)、ws(DashScope TTS WS) |
| Build | TypeScript 5.9 (ES2022/NodeNext)、esbuild 0.24、Electron Forge 7.10、Vitest 4.1 |

---

## 5. 评测器运行（人性化收束层 evaluator）

零依赖 `.mjs` 脚本，三模式（`scripts/eval-humanization.mjs`）：

```bash
# 离线（仅 Node，stubbed judge）→ 打表 + §7 gate 断言，零依赖可复现
node scripts/eval-humanization.mjs --offline
# 真 Langfuse trace 评分回写（需 Langfuse creds）
node scripts/eval-humanization.mjs --score-back --trace <id>
# experiment（需 @langfuse/client + creds）
node scripts/eval-humanization.mjs --experiment
# ground-truth benchmark（30→128 case，live judge）
node scripts/eval-humanization.mjs --benchmark
# 真实生产 humanizer 端到端
node scripts/eval-humanization.mjs --humanize-live
# 跨 judge 一致性
node scripts/eval-humanization.mjs --cross-judge
```

- **Langfuse env**：`LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY`/`LANGFUSE_BASE_URL`（v4；`LANGFUSE_HOST`/`LANGFUSE_BASEURL` 别名）。
- **Judge env**：`EVAL_JUDGE_BASE_URL`/`EVAL_JUDGE_API_KEY`/`EVAL_JUDGE_MODEL`（fallback `OPENAI_API_KEY`）。
- 文件：`evals/humanization/{DESIGN.md, SHOWCASE.md, NOTICE, fixtures/, evaluators/}`。生成产物（`runs/`、`dashboard.html`）git-ignored，源 = `.mjs` + DESIGN.md 契约。

---

## 6. KB lint / 工具脚本

```bash
node ~/.rowboat/scripts/kb-lint-conflicts.mjs   # 冲突检测 lint（Phase 23），append-only 到 inbox.md，exit 0
node ~/.rowboat/scripts/kb-lab.mjs --with-resolver  # KB Lab resolver（Phase 21 相似度验证）
```

---

## 7. 约束红线

- **仓库状态**：`main` 分支，工作区有未提交改动（见 §1）；评测器并发 actor 在 main，v1.3 记忆回路工作在隔离分支（落地需 merge 非 ff）。
- **重 chat runtime 不改**：`runtime.ts:streamAgent`（2000+ 行单函数）太脆；v1.x 只动 instructions.ts 一行 + 加 builtin tool，不重构 turn loop。
- **Local-first 不破**：数据全在 `~/.rowboat/`，无 server/SaaS（语音/LLM 例外）。
- **KG schema 只增不破**：Phase 20 加 `last_seen_at`+`confidence`，既有字段不动。
- **lark-cli 是唯一 Feishu surface**：不加新 connector 框架（无 Composio Feishu plugin）。
- **GSD 流程**：改文件前走 GSD 命令（`/gsd-quick`/`/gsd-debug`/`/gsd-execute-phase`），原子 commit + 状态跟踪。
- **Solo dev + yolo + opus（quality profile）**：verifier 不挂不停。每 phase 单 session 节奏（不一个 phase 装 5 小时活）。
- **off-limits 字节零 diff**：每 phase 验收要求 6 个 off-limits 文件 byte-zero-diff（runtime.ts/knowledge_index.ts/identity.ts/kb-resolve.ts 等）。

---

## 8. 已知 live 缺陷 / 待办（v1.2 milestone audit）

- **D-AUDIT-02（CONFIRMED）**：`lark-cli calendar event.attendees list --as user` live 对每个探测事件失败 → FEI-02 attendee→[[People]] 链接在真实环境未满足（code 8/8 过，live UAT 抓到）。
- **D-AUDIT-03（SUSPECT）**：`feishu_sync_state.json` calendar/base/doc 键 post-cycle 为空 → 增量游标未持久化 → 二次 sync 去重有风险。
- 14× deferred live-Electron UAT（全 13 phase code/test 层验证，live E2E 人工观察 deferred）。
- OBS-01（watch）：qwen-plus openai-compatible 端点无原生 responseFormat schema，generateObject 降级 prompt-JSON。

---

*交接来源：`CLAUDE.md` + `.planning/codebase/STACK.md` + `.planning/milestones/v1.2-MILESTONE-AUDIT.md` + git status/log。*
