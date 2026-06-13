# -*- coding: utf-8 -*-
import json, subprocess, sys, os
from datetime import datetime, timezone, timedelta
APP="EdlPbzsTwaMgANspA1mcbs6ynxe"
T_WK="tbl3oRW8gxWFZKJf"; T_PROJ="tblyUnKMEfy3I7Kf"; T_LOG="tblKkZp4I91EpYrL"; T_CAL="tbluAmesj88FBnoj"
CST=timezone(timedelta(hours=8))
def ms(y,m,d): return int(datetime(y,m,d,tzinfo=CST).timestamp()*1000)
def run(args):
    r=subprocess.run(["lark-cli"]+args,capture_output=True,text=True,encoding="utf-8",shell=True)
    return (r.stdout or "")+(r.stderr or "")
def post(table,endpoint,body):
    with open("aux_body.json","w",encoding="utf-8") as f: json.dump(body,f,ensure_ascii=False)
    out=run(["api","POST",f"/open-apis/bitable/v1/apps/{APP}/tables/{table}/records/{endpoint}","--data","@aux_body.json","--as","user"])
    os.remove("aux_body.json")
    return ('"code": 0' in out or '"msg": "success"' in out), out
KR={"O1K1":"recvi0cKCWjNxz","O1K2":"recvi0cKCWcrUC","O1K3":"recvi0cKCWySlr","O2K1":"recvi0cKCWGaDy","O2K2":"recvi0cKCWxdeG","O2K3":"recvi0cKCWi1c9","O2K4":"recvi0cKCWdFgc","O3K1":"recvi0cKCWxj42","O3K2":"recvi0cKCWnS9C","O3K3":"recvi0cKCWMbQ3","O4K1":"recvi0cKCW2Jjh","O4K2":"recvi0cKCWfz5q","O4K3":"recvi0cKCWgTn4","O4K4":"recvi0cKCWzIVz"}
REPORT="https://f4x6dn8llc.feishu.cn/docx/PNNfdUYkPoynF9xMkZicnDh3n28"

# 1) 周报日历: 补 W6
ok1,_=post(T_WK,"batch_create",{"records":[{"fields":{
  "周范围":"2026-05-18 ~ 2026-05-22","状态":"完整✅","工作天数":5,
  "周报文档链接":{"link":"https://f4x6dn8llc.feishu.cn/docx/OBWJd7RtFo4tf6xHelucAqjnnAe","text":"2026-05-18 ~ 2026-05-22 周报"},
  "本周摘要":"Loona-Spec v1.0(四层/223条机检)+Loona Protocol R4真验收(209 case)+人性化收束层评测器(112 benchmark)+软件产品周会(6/30最小版本/5方向收敛/短链路)+旅游规划Agent PRD v0.1"}}]})
print("周报日历补W6:",ok1)

# 2) 项目: 更新6条
upd=[
 ("recvi0cClnBZNp","记忆功能需求 PRD V0.x;5/19周会定:前期仅用Persona画像记忆,长期记忆后推。",ms(2026,5,19)),
 ("recvi0cCluZtop","Slack场景case收束+UI交付+泛化测试;5/11批量发送/Search二步处理讨论;后续由王文俊接手推进。",ms(2026,5,19)),
 ("recvi0cCm3aB5J","三方对齐(旭哥+文俊):先理清存储方案再做PPT;列入6/30最小版本场景(文档生成)。",ms(2026,5,19)),
 ("recvi0cClZhPir","手机端应用管理PRD(V0.3→V0.7)已输出;待排期细化。",ms(2026,5,20)),
 ("recvi0cCnEUav4","知识库运营+AI Jam分享(Knowledge Loop);5/21-22升级为Loona知识体系四层+Loona-Spec v1.0(223条机检)。",ms(2026,5,22)),
 ("recvjVPabcTlZK","5/17需求文档完成(架构总览+接口契约+5卡Data Schema+Router/Planner/Persona Prompt模板+技术栈选型);承接6/30短链路方案。",ms(2026,5,22)),
]
recs=[{"record_id":r,"fields":{"当前进度":p,"最近更新":d,"状态":"进行中🟡"}} for r,p,d in upd]
recs[3]["fields"]["状态"]="未开始🔴"  # 手机端
ok2,o2=post(T_PROJ,"batch_update",{"records":recs}); print("项目更新6条:",ok2, "" if ok2 else o2[:160])

# 3) 项目: 新增4个
new=[
 {"项目名称":"Loona Protocol 工程验收(Jarvis)","状态":"进行中🟡","最近更新":ms(2026,5,22),
  "当前进度":"Cortex多agent+Bridge SSE+ToolHub+前端全栈Protocol对齐;209 case三层真验收(schema 209/209,LIVE 102/125),R4链路追踪法抓修7个live bug(天气卡/TTS/邮箱/新闻)。",
  "描述":"Loona Agent协议在真实栈上的逐case三层(后端/传输/前端)真验收","关联OKR":[KR["O2K3"],KR["O4K4"],KR["O3K1"]]},
 {"项目名称":"人性化收束层评测器(Rowboat)","状态":"进行中🟡","最近更新":ms(2026,5,19),
  "当前进度":"112条benchmark+Langfuse真流量回写(抓真实humanizer约23% evidence_diff FAIL)+人格参数化;确定性指标(evidence_diff/burstiness/gptism)+LLM judge;v1.2 13phase shipped/513测试,v1.3记忆回路立项。",
  "描述":"为人性化收束层做独立、外部校准的评测器+benchmark","关联OKR":[KR["O3K1"],KR["O3K2"],KR["O2K3"]]},
 {"项目名称":"Loona-Spec 交互规范","状态":"进行中🟡","最近更新":ms(2026,5,22),
  "当前进度":"v1.0四层架构(总协议→9场景插件→跨场景登记表→评测用例包)+223条机检需求(blocker64/major147/minor12),8闸门全绿;核心思想'Loona是控制权分配器'。",
  "描述":"Loona交互规范文档化+机检覆盖(GitHub: lala1137273514/loona-spec)","关联OKR":[KR["O3K2"],KR["O2K2"]]},
 {"项目名称":"旅游规划 Agent","状态":"进行中🟡","最近更新":ms(2026,5,20),
  "当前进度":"PRD v0.1(10功能模块/~2000字);know-how设计:交互四环节+结果卡三分类+多卡与TTS one-by-one对应+澄清一次完成。",
  "描述":"短链路最小版本首个落地需求样本","关联OKR":[KR["O1K2"],KR["O4K3"]]},
]
proj_new=[{"fields":f} for f in new]
ok3,o3=post(T_PROJ,"batch_create",{"records":proj_new}); print("项目新增4个:",ok3, "" if ok3 else o3[:160])

# 4) 进度日志: 修笔误 + 补5条
oktp,_=post(T_LOG,"batch_update",{"records":[{"record_id":"recvi4XSlOFvmg","fields":{"日期":ms(2026,4,28)}}]}); print("进度日志修笔误:",oktp)
logs=[
 (ms(2026,5,21),"know how会议:建立Loona交互体验框架(四环节链路开始→澄清→执行→结果 + 结果卡三分类 无卡/单卡/多卡);旅游规划场景方案(最小条件时间+目的地/澄清卡/多卡与TTS对应)。",[KR["O3K2"],KR["O1K2"]]),
 (ms(2026,5,22),"Loona-Spec v1.0发布:四层架构+223条机检需求(blocker64/major147/minor12)+8闸门全绿;know how对齐会确定Spec=Loona交互规范、分层规则、澄清一次完成、多卡+TTS对应。",[KR["O3K2"],KR["O2K2"]]),
 (ms(2026,5,22),"Jarvis Loona Protocol R4全链路真验收:209 case三层(schema 209/209,LIVE 102/125),链路追踪法替代截图法,真·行为QA抓修7个live bug(天气卡乱码/TTS念标点/双重朗读/邮箱被切/新闻失败等)。",[KR["O2K3"],KR["O4K4"]]),
 (ms(2026,5,24),"Q2 OKR全量反推映射:四源证据采集(飞书/G盘/Claude/Codex)+14个KR反推-映射分析+5份收口/总报告文档+14KR进展回填飞书OKR。",[KR["O2K4"],KR["O3K1"]]),
 (ms(2026,5,25),"复盘体系运维:个人复盘文件夹整理(33→11项,归档/去重/统一命名)+多维表格OKR表14条对齐+项目/进度日志/周报日历同步对齐。",[KR["O1K3"]]),
]
lr=[{"fields":{"日期":d,"风险标记":"无风险","进展描述":t,"关联OKR-KR":k}} for d,t,k in logs]
okl,ol=post(T_LOG,"batch_create",{"records":lr}); print("进度日志补5条:",okl, "" if okl else ol[:160])

# 5) 复盘日历: 修2处年份笔误(日期字段)
okc,oc=post(T_CAL,"batch_update",{"records":[
  {"record_id":"recvi4XSlXSbzH","fields":{"日期":ms(2026,4,28)}},
  {"record_id":"recviw5VMLfZM7","fields":{"日期":ms(2026,5,2)}},
]}); print("复盘日历修2笔误:",okc, "" if okc else oc[:160])
