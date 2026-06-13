# -*- coding: utf-8 -*-
import json, subprocess, sys
from datetime import datetime, timezone, timedelta
MODE=sys.argv[1] if len(sys.argv)>1 else "dry"
APP="EdlPbzsTwaMgANspA1mcbs6ynxe"; TBL="tblrCJermiV3VkvW"
CST=timezone(timedelta(hours=8)); UPD=int(datetime(2026,5,25,tzinfo=CST).timestamp()*1000)
def run(args):
    r=subprocess.run(["lark-cli"]+args,capture_output=True,text=True,encoding="utf-8",shell=True)
    return (r.stdout or "")+(r.stderr or "")

# 1. 读全部记录(markdown 解析 record_id + 名称)
md=run(["base","+record-list","--base-token",APP,"--table-id",TBL,"--as","user"])
orig=[]; dup=[]
for l in md.splitlines():
    if not l.strip().startswith("| rec"): continue
    cells=[c.strip() for c in l.split("|")]
    rid=cells[1]; name=cells[2] if len(cells)>2 else ""
    if rid.startswith("recvkB"): dup.append(rid)          # 我误加的
    elif rid.startswith("recvi0"): orig.append((rid,name)) # 原有14条
print("原有:",len(orig)," 重复待删:",len(dup))

# 原有14条按出现顺序 = O1-KR1..O4-KR4(与下方一致)
# 我的对齐数据(顺序与原表一致)
ALIGN=[
 (100,"done","100%｜入职1-2周完成六步产品认知+情感交互架构+新人项目交接+第一周汇报对齐,后续经周会/Agent指标/Wiki化持续校验。已达成收口。"),
 (75,"wip","75%｜承接≥3个非Agent小模块需求(手机端应用管理/430记忆管理/530三线MVP+旅游规划PRD),五要素齐全。DDL6/30按节奏推进。"),
 (75,"wip","75%｜日报近日更、周报W1-W6无断档、多场跨团队对齐;复盘升级为daily-review skill+cron自动化。DDL6/30按节奏。"),
 (75,"wip","75%｜独立识别定义≥3个AI赋能场景,主线=个人复盘/日报自动化skill(已开源)。DDL6/30按节奏。"),
 (70,"wip","70%｜复盘skill v3.1+人性化收束层评测器两层架构+Loona-Spec四层方案,需求拆解→方案设计闭环。DDL6/30按节奏。"),
 (75,"wip","75%｜复盘skill cron落地+开源、评测器Langfuse真流量验证、Jarvis 209 case真验收+rowboat v1.2 513测试。DDL6/30按节奏。"),
 (65,"wip","65%｜已出《复盘自动化项目阶段性复盘总结》(五要素);项目仍迭代,待6月正式收口。"),
 (100,"done","100%｜《4月Agent体验与问题分析(收口版)》7能力维度+11条核心问题(接口217用例/97.24%、humanizer约23% FAIL)。已完成收口。"),
 (80,"wip","80%｜《Agent产品化方法沉淀(总纲)》:需求定义(Loona-Spec223条)/体验设计/评估维度/16条常见问题清单。DDL5/31。"),
 (60,"wip","60%｜方向候选(可观测+评测/记忆+知识库/CC Persona)+Loona-Spec自迭代协议作路线图骨架;正式路线图6月输出。"),
 (100,"done","100%｜4.14全模块Agent需求PRD+200+case测试集(标注规范v1/v2/评测平台/接口报告);430顺延属外部因素。已完成。"),
 (80,"wip","80%｜69失败case归因+R4真验收7bug+5方向收敛→《面向6月版本需求迭代输入清单》20条(9条P0)。DDL5/31。"),
 (65,"wip","65%｜530三线MVP需求底盘+研发对齐(5/19周会接棒)+know-how场景对齐+工程化分工;正式评审6月。"),
 (60,"wip","60%｜验收基础设施(Loona-Spec223+Jarvis 209三层+评测器112)+真验收预演;6/30正式验收6月。"),
]
ST={"done":"已完成✅","wip":"进行中🟡"}

if len(orig)!=14:
    print("⚠️ 原有记录数!=14,请人工核对顺序后再更新。仅执行删除重复。")

if MODE=="real":
    # 删重复(分批,每批<=500)
    if dup:
        body=json.dumps({"records":dup},ensure_ascii=False)
        with open("del_body.json","w",encoding="utf-8") as f: f.write(body)
        out=run(["api","POST",f"/open-apis/bitable/v1/apps/{APP}/tables/{TBL}/records/batch_delete","--data","@del_body.json","--as","user"])
        print("删除:", "success" if '"msg": "success"' in out or '"code": 0' in out else out[:200])
        import os; os.remove("del_body.json")
    # 更新原有14条
    if len(orig)==14:
        recs=[]
        for (rid,name),(pct,st,note) in zip(orig,ALIGN):
            recs.append({"record_id":rid,"fields":{"当前进度":note,"状态":ST[st],"最近更新":UPD}})
        body=json.dumps({"records":recs},ensure_ascii=False)
        with open("upd_body.json","w",encoding="utf-8") as f: f.write(body)
        out=run(["api","POST",f"/open-apis/bitable/v1/apps/{APP}/tables/{TBL}/records/batch_update","--data","@upd_body.json","--as","user"])
        print("更新:", "success" if '"msg": "success"' in out or '"code": 0' in out else out[:300])
        import os; os.remove("upd_body.json")
else:
    print("DRY. 将删除",len(dup),"条重复; 更新原有",len(orig),"条")
    for (rid,name),(pct,st,note) in zip(orig,ALIGN):
        print(f"  {rid} {name[:20]:22} -> {pct}% {ST[st]}")
