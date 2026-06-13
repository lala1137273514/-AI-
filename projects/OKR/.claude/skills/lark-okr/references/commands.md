# lark-cli OKR 命令速查

> 环境：lark-cli ≥ 1.0.38，用户 秦宇龙，app `cli_a941969bd53a1bdd`。**所有命令带 `--as user`**。

## 读（P1 已验证 ✅）

```bash
# 列出我的所有 OKR 周期（时间戳为毫秒字符串）
lark-cli okr +cycle-list --user-id <open_id> --as user --format json

# 读某周期内的全部 Objective + Key Result（含 content 富文本、score、weight）
lark-cli okr +cycle-detail --cycle-id <cycle_id> --as user --format json

# 读某 O 或 KR 的进展记录列表
lark-cli okr +progress-list <flags> --as user --format json
```

## 写（P2/P3，用前必须 `--dry-run` 核对参数）

```bash
# 进展记录 CRUD
lark-cli okr +progress-create <flags> --as user
lark-cli okr +progress-update <flags> --as user
lark-cli okr +progress-delete <flags> --as user
lark-cli okr +progress-get    <flags> --as user
lark-cli okr +upload-image -o <file>  --as user

# O / KR 增删改（scope: okr:okr.content:writeonly）
lark-cli okr objectives  create|patch|delete ... --as user
lark-cli okr key_results create|patch|delete ... --as user
lark-cli okr objective.key_results create ...    --as user
lark-cli okr objective.alignments  create ...    --as user
```

## 已授予 OKR scopes（8 个）

```
okr:okr.period:readonly        okr:okr.content:readonly      okr:okr.content:writeonly
okr:okr.setting:read           okr:okr.progress:readonly     okr:okr.progress:writeonly
okr:okr.progress:delete        okr:okr.progress.file:upload
```

## 辅助

```bash
lark-cli auth status --format json   # 取 userOpenId / 校验 token
lark-cli schema okr                  # 全部 OKR 接口 schema
lark-cli okr <cmd> --dry-run         # 打印请求不执行
```
