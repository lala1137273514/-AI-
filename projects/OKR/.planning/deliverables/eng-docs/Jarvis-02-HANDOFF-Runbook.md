# Jarvis (Loona Protocol) · HANDOFF / Runbook

> 运维交接手册：服务清单、端口、启动/重启步骤、依赖、约束红线。
> 来源：Cortex `HANDOFF.md` + Jarvis `HANDOFF.md` + 验收报告红线复核。
> ⚠️ 本文档为**只读交接说明**；实操前确认是否在被授权窗口内。

---

## 1. 服务清单与端口

| 件 | 进程 | 端口 | 路径 / 备注 |
|---|---|---|---|
| Postgres 18 | docker `cortex-postgres` | `127.0.0.1:5432` | named volume `dev_dep_cortex_pg_data` |
| Redis 7.4 | docker `cortex-redis` | `127.0.0.1:6381` | named volume `cortex_redis_data`（6379 被占→改 6381） |
| ToolHub server | `python toolhub/server/python/main.py` | `127.0.0.1:25003` | 独立 git 仓，凭证 `server/python/.env`；cortex 启动会预热 |
| Cortex | `uvicorn src.app.main:cortex_app --factory` | `127.0.0.1:8080` | 健康 `/health/readiness` |
| Bridge | `python scripts/web_chat_bridge.py` | `127.0.0.1:7860` | `/api/turn`·`/api/tool-demo`·`/api/trip-plan`·`/api/tts` |
| Jarvis 静态 | `python -m http.server 7870 --directory ...Jarvis` | `127.0.0.1:7870` | 浏览器入口 `http://127.0.0.1:7870/index.html` |
| （验收用静态） | 同上不同端口 | `127.0.0.1:7861` | L3 VISUAL harness 真打用 |

**Python 环境**：conda env `py312`（项目要求 3.12，本机无系统 3.12）。所有 python 命令前缀 `conda run -n py312 ...`。

---

## 2. 启动顺序（容器 → ToolHub → Cortex → Bridge → 静态）

```powershell
# 1) PG/Redis
docker compose -f C:/Users/QYL/Downloads/cortex-refactor/cortex/dev_dep/docker-compose.yml up -d
# 2) ToolHub server（独立仓 C:/Users/QYL/Desktop/toolhub）
Set-Location C:/Users/QYL/Downloads/cortex-refactor/cortex
Start-Process -WindowStyle Hidden -FilePath "conda" -ArgumentList 'run','-n','py312','python','C:/Users/QYL/Desktop/toolhub/server/python/main.py'
# 3) Cortex（等 health 200，启动里预热 ToolHub）
Start-Process -WindowStyle Hidden -FilePath "conda" -ArgumentList 'run','-n','py312','python','-m','uvicorn','src.app.main:cortex_app','--factory','--host','127.0.0.1','--port','8080','--workers','1','--no-access-log'
# 4) Bridge（trip-plan 用 .env 的 DashScope key 直调 LLM）
Start-Process -WindowStyle Hidden -FilePath "conda" -ArgumentList 'run','-n','py312','python','scripts/web_chat_bridge.py','--uid','1001','--sid','jarvis','--redis-url','redis://127.0.0.1:6381/0','--host','127.0.0.1','--port','7860'
# 5) Jarvis 静态（mic/speechSynthesis 要 secure context → 必须 localhost）
Start-Process -WindowStyle Hidden -FilePath "conda" -ArgumentList 'run','-n','py312','python','-m','http.server','7870','--bind','127.0.0.1','--directory','C:/Users/QYL/Desktop/Jarvis'
```

---

## 3. 重启 / 杀进程（谨慎）

⚠️ **绝不按端口无差别 kill**：`com.docker.backend` 共享 `:::8080`，误杀会把整个 Docker 引擎搞挂（已吃过亏）。**按命令行精准 kill**：

```powershell
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | ?{ $_.CommandLine -match 'XXX' } | %{ Stop-Process -Id $_.ProcessId -Force }
# cortex: 'uvicorn.*src\.app\.main'  | bridge: 'web_chat_bridge'  | toolhub: 'server[/\\]python[/\\]main'
```

⚠️ **Docker 重启唯一靠谱方式 = `docker desktop restart`**（本机 `wsl --shutdown` 坏的 REGDB_E_CLASSNOTREG；当前账号非 admin，不能 Restart-Service）。

---

## 4. 健康检查三件套

```powershell
# 端口存活
foreach($p in @(@(5432,'pg'),@(6381,'redis'),@(25003,'toolhub'),@(8080,'cortex'),@(7860,'bridge'),@(7870,'jarvis'))){
  "$($p[1])=$((Test-NetConnection 127.0.0.1 -Port $p[0] -WarningAction SilentlyContinue).TcpTestSucceeded)"
}
# Cortex 健康
(Invoke-WebRequest 'http://127.0.0.1:8080/health/readiness' -UseBasicParsing).Content
# 闲聊（⚠️ PowerShell 中文 body 必须 UTF-8 编码，否则变 ?????）
$b=[Text.Encoding]::UTF8.GetBytes('{"text":"你好"}'); Invoke-RestMethod 'http://127.0.0.1:7860/api/turn' -Method Post -ContentType 'application/json' -Body $b -TimeoutSec 30
# 天气工具
$b=[Text.Encoding]::UTF8.GetBytes('{"name":"get_weather","arguments":{"location":"北京"}}'); (Invoke-RestMethod 'http://127.0.0.1:7860/api/tool-demo' -Method Post -ContentType 'application/json' -Body $b).result
```

浏览器：`http://127.0.0.1:7870/index.html` → "北京天气" / "我想去杭州两天" / "你好" / 🔊 测试语音。

---

## 5. 依赖与配置改动（与原始 Cortex 源 diff）

- `config/global.yaml`：`default_llm.model: deepseek-v4-flash`、`think: low`、`max_tokens: 32768`；fallback `bailian/qwen-plus`。
- `config/llm_tasks/{router,quick_chat,gen_resp,tool_confirm}.yaml`：去掉硬编码内网 sglang 端点，继承 `default_llm`。
- `dev_dep/docker-compose.yml`：Redis 端口 6379→6381；PG/Redis 改命名卷（Win 绑定挂载卡 PG18 权限）。
- `.env`（gitignored）：`SKIP_NACOS=1` / `CORTEX_SIGNOZ__ENABLED=false` / PG+Redis URL / `BAILIAN_API_KEY` / 占位 ENV。
- 新增 `logs/`、`run/` 目录（RotatingFileHandler 需要）。
- 外挂脚本（不改 Cortex 产品代码，符合 AGENTS.md）：`scripts/web_chat_bridge.py`；ToolHub server（已搬独立仓）。

---

## 6. 约束红线（务必先记住）

### 6.1 不可触碰的生产端口
**别动 8080 / 50051 / 7800 / 8000 / 6379**（原始红线端口列表）。注意：本部署里 Cortex 跑在 8080、Redis 改用 6381（非 6379）；Bridge :7860 不在原始红线列表，重启需用户授权。

### 6.2 工程红线（验收报告 9/9 复核项）
| 红线 | 说明 |
|---|---|
| ❌ push gitea | Jarvis/Cortex 无 remote；ToolHub 有 remote `gitea.keyi.lan/pub/emb.data.toolhub.git` 但**不 push** |
| ❌ 端口无差别 kill 长跑服务 | 见 §3，按命令行精准 kill |
| ❌ 动 BAILIAN/SERPER/GMAIL 凭证 | `.env` 不读写 |
| ❌ `.env` / `_gmail_oauth_result.json` 入 git | `.gitignore` 已覆盖 |
| ✅ 新分支 `loona-protocol-align` | 三仓同名 |
| ✅ commit 前缀 `[LOONA]` | 所有 commit |
| ✅ 改前先 read | 全程遵循 |

### 6.3 中止条件
- 改造 > 800 行 → 触线（实际 ~1034，用户已批 1000 预算）。
- 三轮 pass < 80% → 触发 ScheduleWakeup 报根因。

### 6.4 真实写操作状态（重要变更）
V1 验收时 `send_mail`/`create_event`/`update_event`/`delete_event` 全 **dry-run**。截至 ToolHub commit `027e5dc`「enable REAL Google writes (user opted out of dry-run/mock)」，已切到**真实 Google 写**。涉及邮件/日程写操作时按真实生产对待。

---

## 7. 关键环境约束（省时间）

1. **DashScope key 模型权限极窄**：仅 `qwen-plus`/`deepseek-v4-flash`/`deepseek-v3.2-exp` 可用；`qwen-tts`/`qwen3-tts-flash`/`cosyvoice-*` 全 access-denied → **DashScope TTS 走不通**，TTS 走浏览器 speechSynthesis（或换 edge-tts/Azure/ElevenLabs）。
2. **deepseek-v4-flash 强制 reasoning_effort ≥ low**（拒 none/minimal，400 错）。
3. **任务型请求架构本质慢**（~10-15s 多趟 LLM 串行），闲聊 ~5s。
4. **PowerShell 中文 body 必须 UTF-8 编码**（`[Text.Encoding]::UTF8.GetBytes`），否则满屏 NO_MEANING/?????。

---

## 8. 当前 git 状态（只读快照，2026-05-25）

| 仓库 | 分支 | HEAD | 备注 |
|---|---|---|---|
| Jarvis | `loona-protocol-align` | `839439b` | 含 Replay R0-R4 + V2 R4.1 修 6 live bug；工作区有未提交的截图/probe 改动 |
| Cortex | `loona-protocol-align` | `dc41d14` | router.yaml 写动作硬映射修复 |
| ToolHub | `loona-protocol-align` | `027e5dc` | 已 enable REAL Google writes，有 remote 未 push |

---

## 9. 未解决 / 未验证

- TTS 真实可听性（无头浏览器无音频，链路通但人工冒烟待做）。
- 任务型请求慢（架构本质，单轮不可解）。
- 长地名识别（"北京市朝阳区天气"可能抽不准 → 回退闲聊）。
- §22 4 项运行时验收（问题不超一轮 / 不重复问 / 不炫耀记忆 / TTS 不念 URL）需真 SSE+LLM 人工冒烟。

---

*交接来源：`HANDOFF.md`(Cortex) + `HANDOFF.md`(Jarvis) + `.loona/LOONA-VERIFICATION*.md` 红线复核段。*
