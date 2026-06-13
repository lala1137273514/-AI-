# AI Agent Config Sync

这个仓库只同步可共享的 Agent 配置，不同步本机运行态、账号、token、日志和历史。

## 已同步内容

| 路径 | 用途 |
|---|---|
| `codex/AGENTS.md` | Codex 全局行为规则 |
| `codex/config.example.toml` | Codex 配置模板，不含本机路径和状态 |
| `claude/CLAUDE.md` | Claude 全局行为规则 |
| `claude/settings.example.json` | Claude 设置模板，不含鉴权 token |
| `shared/skills/cc-persona/` | CC 人格 skill 的源码部分，排除了状态和记忆 |
| `projects/OKR/` | OKR 项目资料与 `lark-okr` skill 源码，排除了本机设置和缓存 |
| `scripts/install.ps1` | 把共享配置安装到本机 |
| `scripts/export-safe.ps1` | 从本机重新导出白名单配置 |
| `scripts/check-secrets.ps1` | 提交前检查敏感文件和常见 token |
| `shared/memories/` | Codex 长期记忆的整理版：摘要、索引、rollout summaries 和 Feishu preflight memory skill |
| `automations/` | 自动化契约模板和人工维护记忆，不含运行态 |
| `shared/agents/` | Codex/Claude agent 模板 |
| `shared/skills/lark/` | Lark/Feishu CLI skills 源码 |
| `shared/skills/custom/` | 自定义和高价值工作流 skills |
| `codex/rules/default.rules` | Codex 默认规则 |

## 绝不进仓库

| 类型 | 例子 | 原因 |
|---|---|---|
| 鉴权 | `auth.json`、`.credentials.json`、`settings.json` | 可能包含 token |
| 本机状态 | `state_*.sqlite`、`logs_*.sqlite`、`session_index.jsonl` | 运行态和历史 |
| 会话历史 | `sessions/`、`history.jsonl`、`archived_sessions/` | 隐私和上下文泄露 |
| 缓存产物 | `cache/`、`tmp/`、`plugins/cache/` | 体积大且不可移植 |
| 项目本机设置 | `projects/**/.claude/settings.local.json`、`__pycache__/` | 机器权限和编译缓存 |
| 人格记忆 | `state.json`、`user_profile.json`、`memory/session_index.md` | 长期偏好和私人记忆 |
| 自动化运行态 | `tmp-profile/`、`.lark-cli/`、`run-*/`、`state*.json` | 可能包含账号态、绑定态或历史产物 |

## 当前刻意跳过

| 路径 | 原因 |
|---|---|
| `jianbo-review` skill | 源文件包含 Supabase publishable key 示例，暂不放入 Public 仓库 |
| `ui-ux-pro-max*` skill | 体积大，且包含大量 auth/password 示例文本，后续可单独清洗后再放 |
| `tavern-card-distiller` skill | 含私人化角色/素材资产，暂不适合放入 Public 配置仓库 |
| `prompt-eval/runs`、`skill-prompt-generator/extracted_results` | 运行产物和生成数据库，不作为源配置同步 |
| `.codex/memories/.omx`、`raw_memories.md` | 原始日志/原始记忆，不适合作为共享资产 |
| `.codex/automations/**/tmp-profile` | 本机 Lark/Codex 运行态 |

## 使用方式

先检查仓库里没有敏感内容：

```powershell
powershell -ExecutionPolicy Bypass -File ./scripts/check-secrets.ps1
```

安装到当前机器：

```powershell
powershell -ExecutionPolicy Bypass -File ./scripts/install.ps1
```

如果要覆盖本机已有规则，先让脚本备份再覆盖：

```powershell
powershell -ExecutionPolicy Bypass -File ./scripts/install.ps1 -Force
```

重新从本机导出白名单内容：

```powershell
powershell -ExecutionPolicy Bypass -File ./scripts/export-safe.ps1
```

## 配置密钥

`claude/settings.example.json` 里的 `ANTHROPIC_AUTH_TOKEN` 只放占位符。每台机器自己在本地 `~/.claude/settings.json` 或系统环境变量里配置真实 token，不要提交。
