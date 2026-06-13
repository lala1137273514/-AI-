# -*- coding: utf-8 -*-
# W8 周报 OKR 进展（增量 progress-create，不删既有；status 恒 normal；W8 值 >= 当前最新值，只升不降）
import json, subprocess, sys, os
os.chdir(r"C:\Users\QYL\Desktop\OKR")
MODE = sys.argv[1] if len(sys.argv) > 1 else "dry"  # dry | real

WEEKLY = "https://f4x6dn8llc.feishu.cn/docx/MvtXdcTvBoTz0hx64eicXPMSnng"   # W8 周报 docx
GPRD   = "https://f4x6dn8llc.feishu.cn/docx/UbHOdpMfdoEEPUxCqLgcjkI0nYe"   # 谷歌文档生成 PRD（MVP）
GREQ   = "https://f4x6dn8llc.feishu.cn/docx/WkRsdvHBkonTEYxFSfNcohu3naf"   # 文档生成需求梳理纪要
P630   = "https://f4x6dn8llc.feishu.cn/docx/XsFbdvxs2op0VOxhR6Vc4IHNnng"   # 630 agent 文档产物生成
CASE   = "https://f4x6dn8llc.feishu.cn/docx/U1JKdxDXdo09hrxFBVecCr12nUE"   # 文档生成场景 Case 集

# (kid, pct, source_title, source_url, [paragraphs])
RECS = [
 ("7626271435473177779", 78, "Loona 谷歌全家桶内容生成 PRD（MVP）", GPRD, [
   "【W8·0601-0607】本周承接「谷歌文档生成」这一非 Agent 小模块需求，从一句话需求拆成 8 段式 PRD + API 能力对照 + UI 规范 + OAuth 鉴权对齐稿，并出 MVP 释放稿，范围当周锁定（只做 Docs/Slides/Sheets、drive.file 最小权限、PPT 先砍图）。五要素齐全，已进研发交接。同时 Slack 统一分诊 Triage 作为独立模块全栈落地。",
 ]),
 ("7626271274969844667", 78, "2026-06-01 ~ 2026-06-07 周报（W8）", WEEKLY, [
   "【W8·0601-0607】本周参与 7 场对齐会（agent 问题对齐、slack UI、软件周会、文档生成需求、电脑端更新、agent 拉齐），日报周报无断档。复盘体系继续工程化：封装 jianbo-review skill、给周报 skill 固化「多 agent 并行 + 落文档前双质检（shuorenhua+jianbo-review）」两条规则。",
 ]),
 ("7626271568236547040", 78, "2026-06-01 ~ 2026-06-07 周报（W8）", WEEKLY, [
   "【W8·0601-0607】新增「语音遥控派活」AI 赋能场景：clawd glassbox 黑客松 demo 把截图捕获→轻模型编排→派活给 claude/codex 整条链路跑通，并搭好「hey, cc」唤醒词骨架——语音唤醒+遥控这套能力可迁移到 Loona 的主动交互。同时推进 AI 旅行助手数据结构与流程迭代。",
 ]),
 ("7626271828239060173", 75, "文档生成需求梳理&优化方向对齐 纪要", GREQ, [
   "【W8·0601-0607】谷歌文档生成需求走完闭环：6/3 需求梳理会定方向 → 当天产出 PRD 套件 → 拆「PM 决策 vs 研发交接」两层 → 出研发交接规格与 4 个 prompt 草稿，周壮一天内开 API 对接。从需求拆解到协作落地都接上了。",
 ]),
 ("7626271562145024990", 81, "2026-06-01 ~ 2026-06-07 周报（W8）", WEEKLY, [
   "【W8·0601-0607】本周多条交互线在工程上跑通落地：cortex Slack Triage v1 全栈（约 25 文件含 9 测试）端到端跑通、线上旅行卡两阶段钻取上线。方案层 present_plans 新链路（+13 单测）已验证健康但暂回退留备份，待拍板是否重上。clawd glassbox 语音遥控 demo 全量 3647 测试通过。",
 ]),
 ("7627422012026588105", 70, "630 agent 文档产物生成", P630, [
   "【W8·0601-0607】630 版本需求持续细化：文档生成需求梳理并交研发、产出「630 agent 文档产物生成」文档；6/2 软件周会拍定 630 底线为「体验极致、不堆功能」，明确多语言先稳中文、优先 Claude、记忆方案 6/30 前体现用户 preference。下一步需安排正式评审过会。",
 ]),
 ("7628430235122666701", 68, "文档生成 — 场景 Case 集", CASE, [
   "【W8·0601-0607】验收物料继续补齐：文档生成「场景 Case 集」成稿、clawd glassbox 写出 9 条验收标准、loona-workbench 产出 9 类卡片组件规范（字段从真实 builder 提取、标必填/选填、22 张组件图）。下一步需把验收 Case 逐条映射到 630 功能。",
 ]),
]

def content_json(paragraphs):
    blocks=[{"block_element_type":"paragraph","paragraph":{"elements":[
        {"paragraph_element_type":"textRun","text_run":{"text":p,"style":{}}}]}} for p in paragraphs if p and p.strip()]
    return json.dumps({"blocks":blocks}, ensure_ascii=False)

def run(cmd):
    out=""
    for _ in range(3):  # retry transient EOF
        r=subprocess.run(cmd,capture_output=True,text=True,encoding="utf-8",shell=True)
        out=(r.stdout or "")+(r.stderr or "")
        if '"ok": true' in out or (("--dry-run" in cmd) and r.returncode==0 and "EOF" not in out):
            return True,out
        if "EOF" in out:  # transient, retry
            continue
        break
    return ('"ok": true' in out),out

items = RECS[:1] if MODE=="dry" else RECS
ok=0; fail=0; idx=0
print(f"== W8 OKR progress  MODE={MODE}  ({len(items)}/{len(RECS)} records) ==")
for kid,pct,st,su,paras in items:
    fn=f"w8_{idx}.json"; idx+=1
    with open(fn,"w",encoding="utf-8") as f: f.write(content_json(paras))
    cmd=f'lark-cli okr +progress-create --target-type key_result --target-id {kid} --progress-percent {pct} --progress-status normal --content @{fn} --source-title "{st}" --source-url "{su}" --as user'
    if MODE=="dry": cmd+=" --dry-run"
    cok,cout=run(cmd)
    print(f"  KR ...{kid[-4:]} {pct}% ({len(paras)}p) -> {'OK' if cok else 'FAIL: '+cout[:200]}")
    ok+=cok; fail+=(not cok)
    try: os.remove(fn)
    except: pass
print(f"\nMODE={MODE}: ok={ok} fail={fail}")
