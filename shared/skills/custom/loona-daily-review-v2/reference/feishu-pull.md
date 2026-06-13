# 飞书采集 / 回填命令（lark-cli · 全部 `--as user`）

> Bash 调 `/open-apis` 前先 `export MSYS_NO_PATHCONV=1`。
> 关键 token：个人复盘 folder `U0H3fNGXol8I2EdYfXwccLNxnRe`；Drive 根 `nodcnQZuGdHEsre9S5ovQeCN6ed`；
> 复盘日历 bitable `EdlPbzsTwaMgANspA1mcbs6ynxe`（OKR 表 `tblrCJermiV3VkvW`、复盘日历 `tbluAmesj88FBnoj`）。

## 读（采集）

```bash
# 当天日程
lark-cli calendar +agenda --as user

# 列「个人复盘」文件夹子文件（拿当天日复盘 / 周报 token）
export MSYS_NO_PATHCONV=1
lark-cli api GET /open-apis/drive/v1/files --params '{"folder_token":"U0H3fNGXol8I2EdYfXwccLNxnRe"}' --as user
# 根目录（智能纪要/文字记录在这里）
lark-cli api GET /open-apis/drive/v1/files --params '{"folder_token":"nodcnQZuGdHEsre9S5ovQeCN6ed"}' --as user

# 读 docx 原文（会议纪要务必读原文，不靠日报摘要）
lark-cli docs +fetch --api-version v2 --doc <docToken> --format pretty   # 去 HTML 标签后用

# 读复盘日历 / OKR bitable 记录（必须 record-list，不要 api GET records）
lark-cli base +record-list --base-token EdlPbzsTwaMgANspA1mcbs6ynxe --table-id tblrCJermiV3VkvW --as user

# 读 OKR 周期 + KR
lark-cli okr +cycle-list --user-id ou_9e35d4bb77a72e6180e8f54417ff0532 --as user
lark-cli okr +cycle-detail --cycle-id 7622051252293749950 --as user
```

## 写（仅用户同意后；红线：不动已有日报）

```bash
# 新建飞书 docx（cd 到 md 所在目录，content 只能相对路径）
cd /c/Users/QYL/Desktop/OKR/.planning/dailies-v2
lark-cli docs +create --api-version v2 --doc-format markdown --content @2026-05-22.md --parent-token U0H3fNGXol8I2EdYfXwccLNxnRe --as user

# 覆盖更新已有 docx（URL 稳定）
lark-cli docs +update --api-version v2 --command overwrite --doc-format markdown --content @file.md --doc <docToken> --as user

# 写 OKR 进展记录（状态恒 normal）
lark-cli okr +progress-create --target-type key_result --target-id <KRid> \
  --progress-percent N --progress-status normal --content @block.json \
  --source-title "<标题>" --source-url "<url>" --as user

# bitable 写记录（verify-before-write，先 record-list 读）
lark-cli api POST /open-apis/bitable/v1/apps/EdlPbzsTwaMgANspA1mcbs6ynxe/tables/<tbl>/records/batch_create --data @records.json --as user
```

## 防重复 / 防误删红线

- 写 docx 前先列 folder 看当天是否已有同名日报；**已有→不重建**，交用户决定。
- 写 OKR 进展前先 `cycle-detail` 看现有记录数；用 `.planning/apply_progress.py` 会先 delete 再 recreate（确认是自己建的记录再删）。
- bitable 读必须 `record-list`（GET 限权假空表会害你重复写）。
