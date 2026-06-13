# -*- coding: utf-8 -*-
import json, subprocess, sys, time
from datetime import datetime, timezone, timedelta
MODE = sys.argv[1] if len(sys.argv)>1 else "dry"
APP="EdlPbzsTwaMgANspA1mcbs6ynxe"; TBL="tblrCJermiV3VkvW"
CST=timezone(timedelta(hours=8))
def ms(dtstr):  # "2026-06-30 00:00:00" -> ms
    return int(datetime.strptime(dtstr,"%Y-%m-%d %H:%M:%S").replace(tzinfo=CST).timestamp()*1000)
UPDATED=int(datetime(2026,5,25,tzinfo=CST).timestamp()*1000)

def run(args):
    r=subprocess.run(["lark-cli"]+args,capture_output=True,text=True,encoding="utf-8",shell=True)
    return r.stdout or ""
def jload(s):
    try: return json.loads(s)
    except: return {}

# 1. 选项精确字符串
fdoc=jload(run(["api","GET",f"/open-apis/bitable/v1/apps/{APP}/tables/{TBL}/fields","--params",'{"page_size":50}',"--as","user"]))
objopts={}; wopts=set(); stopts={}
for f in fdoc.get("data",{}).get("items",[]):
    if f["field_name"]=="所属Objective":
        for o in f["property"]["options"]:
            objopts[o["name"][:2]]=o["name"]   # "O1"->full
    if f["field_name"]=="权重":
        wopts={o["name"] for o in f["property"]["options"]}
    if f["field_name"]=="状态":
        for o in f["property"]["options"]:
            if o["name"].startswith("已完成"): stopts["done"]=o["name"]
            elif o["name"].startswith("进行中"): stopts["wip"]=o["name"]
            elif o["name"].startswith("未开始"): stopts["none"]=o["name"]
print("objopts",objopts); print("wopts",wopts); print("stopts",stopts)

# 2. OKR 真实 weight/deadline/content
ok=jload(run(["okr","+cycle-detail","--cycle-id","7622051252293749950","--as","user"]))
krmeta={}
for o in ok["data"]["objectives"]:
    Op=o["position"]
    for kr in o["key_results"]:
        try: txt=json.loads(kr["content"])["blocks"][0]["paragraph"]["elements"][0]["text_run"]["text"]
        except: txt=""
        krmeta[kr["id"]]={"O":Op,"weight":kr.get("weight"),"deadline":kr.get("deadline"),"desc":txt}

# 3. 我的进度/短名/note (kr_id: (Opos,KRpos,shortname,pct,note))
P={
"7626271491483389119":(1,1,"认知对齐",100,"入职1-2周完成六步产品认知+情感交互架构+新人项目交接+第一周汇报对齐,后续经周会/Agent指标/Wiki化持续校验。已达成收口。"),
"7626271435473177779":(1,2,"承接非Agent小模块需求",75,"承接≥3个非Agent小模块需求(手机端应用管理/430记忆管理/530三线MVP+旅游规划PRD v0.1),目标/场景/流程/异常/边界五要素齐全。DDL6/30按节奏75%。"),
"7626271274969844667":(1,3,"稳定需求输出与协作习惯",75,"日报近日更、周报W1-W6无断档、多场跨团队对齐;复盘升级为daily-review skill+cron自动化。DDL6/30按节奏75%。"),
"7626271568236547040":(2,1,"识别定义AI赋能场景",75,"独立识别定义≥3个场景,主线=个人复盘/日报自动化skill(已开源feishu-daily-review)。DDL6/30按节奏75%。"),
"7626271828239060173":(2,2,"需求拆解→方案设计闭环",70,"复盘skill v3.1+人性化收束层评测器两层架构+Loona-Spec四层方案。DDL6/30按节奏70%。"),
"7626271562145024990":(2,3,"推动实现/试运行/验证",75,"复盘skill cron落地+GitHub开源、评测器Langfuse真流量验证、Jarvis 209 case真验收+rowboat v1.2 513测试。DDL6/30按节奏75%。"),
"7626271889488743624":(2,4,"项目末复盘总结",65,"已出《复盘自动化项目阶段性复盘总结》(五要素);项目仍迭代,待6月正式收口。65%。"),
"7627421948808973250":(3,1,"Agent体验分析+问题文档",100,"《4月Agent体验与问题分析(收口版)》7能力维度+11条核心问题(接口217用例/97.24%、humanizer约23% FAIL)。已完成收口。"),
"7627422941223472347":(3,2,"Agent产品化方法沉淀",80,"《Agent产品化方法沉淀(总纲)》:需求定义(Loona-Spec223条)/体验设计/评估维度/16条常见问题清单。DDL5/31,80%。"),
"7627422847853628596":(3,3,"中长期方向/路线图",60,"方向候选(可观测+评测/记忆+知识库/CC Persona)+Loona-Spec自迭代协议作路线图骨架;正式路线图6月输出。60%。"),
"7627422012026522569":(4,1,"430版本需求+测试集",100,"4.14全模块Agent需求PRD+200+case测试集(标注规范v1/v2/评测平台/接口报告);430顺延属外部因素。已完成。"),
"7627423339209133261":(4,2,"问题整理→6月迭代输入",80,"69失败case归因+R4真验收7bug+5方向收敛→《面向6月版本需求迭代输入清单》20条(9条P0)。DDL5/31,80%。"),
"7627422012026588105":(4,3,"6/30需求+评审+研发对齐",65,"530三线MVP需求底盘+研发对齐(5/19周会接棒)+know-how场景对齐+工程化分工;正式评审6月。65%。"),
"7628430235122666701":(4,4,"6/30验收标准+关键Case",60,"验收基础设施(Loona-Spec223+Jarvis 209三层+评测器112)+真验收预演;6/30正式验收6月。60%。"),
}

records=[]
for kid,(Op,Kp,name,pct,note) in P.items():
    m=krmeta.get(kid,{})
    fields={
        "KR名称": f"O{Op}-KR{Kp} {name}",
        "KR描述": m.get("desc",""),
        "当前进度": f"{pct}%｜{note}",
        "最近更新": UPDATED,
    }
    # Objective
    oo=objopts.get(f"O{Op}")
    if oo: fields["所属Objective"]=oo
    # 状态
    fields["状态"]= stopts["done"] if pct>=100 else stopts["wip"]
    # 权重
    w=m.get("weight")
    if w is not None:
        wp=f"{int(round(w*100))}%"
        if wp in wopts: fields["权重"]=wp
    # 截止日期
    dl=m.get("deadline")
    if dl: fields["截止日期"]=ms(dl)
    records.append({"fields":fields})

print(f"\nbuilt {len(records)} records. sample:")
print(json.dumps(records[0],ensure_ascii=False)[:400])

if MODE in ("real","build"):
    body=json.dumps({"records":records},ensure_ascii=False)
    with open("bt_body.json","w",encoding="utf-8") as f: f.write(body)
    print(f"wrote bt_body.json with {len(records)} records")
