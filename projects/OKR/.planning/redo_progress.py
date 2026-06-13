# -*- coding: utf-8 -*-
import json, subprocess, sys, os
os.chdir(r"C:\Users\QYL\Desktop\OKR")
MODE = sys.argv[1] if len(sys.argv) > 1 else "dry"

R     ="https://f4x6dn8llc.feishu.cn/docx/PNNfdUYkPoynF9xMkZicnDh3n28"
D_O2KR4="https://f4x6dn8llc.feishu.cn/docx/JPwUdy6cFobBTRx0CBecSg63n42"
D_O3KR1="https://f4x6dn8llc.feishu.cn/docx/Qc6wd4nzSoScx6xwUOMcx1mQn8b"
D_O3KR2="https://f4x6dn8llc.feishu.cn/docx/UZqCd3V20o24LHxnoMHcMHTDnff"
D_O4KR2="https://f4x6dn8llc.feishu.cn/docx/XYpCdjwj0o5gCaxx7gXcZ2ONnch"

# 进度按"有效DDL节奏"定:已过DDL→100;5/31→80;6/30→60-80。全部 status=normal。
KRS = {
 "7626271491483389119": ("Q2 OKR反推映射总报告", R, [  # O1-KR1  DDL≈4/11(已过)→100
   (60,"【W0·入职首周】六步产品认知(产品总图/模块地图/主链路/Agent中枢/版本边界)+情感交互架构1.0-2.0(11图)+黑话表。"),
   (85,"【W1·4/13-17】新人项目交接认知报告+第一周汇报对齐;Agent服务接口梳理、Slack MCP能力边界验证。"),
   (100,"【W1末·入职认知DDL到期】产品线/业务/Agent能力边界/协作流程认知对齐完成,后续经周会/Agent指标/Wiki化持续校验,达成100%。"),
 ]),
 "7626271435473177779": ("Q2 OKR反推映射总报告", R, [  # O1-KR2  DDL 6/30→75
   (40,"【W2·4/20-26】启动手机端应用管理需求(早期PRD)+430需求Index梳理,开始承接非Agent小模块。"),
   (60,"【W4·5/4-7】手机端应用管理PRD多轮迭代+430记忆管理需求+Slack场景case 4处PRD级修订。"),
   (75,"【W6·5/18-22】旅游规划Agent PRD v0.1+530三线MVP,五要素齐全。DDL 6/30,按节奏推进至75%。"),
 ]),
 "7626271274969844667": ("Q2 OKR反推映射总报告", R, [  # O1-KR3  DDL 6/30→75
   (35,"【W1·4/13-19】日报复盘+周报W1起步,形成需求输出与协作记录习惯。"),
   (55,"【W3·4/27-5/3】三层复盘体系建成、周报方法论成熟。"),
   (70,"【W4·5/4-10】复盘升级为daily-review skill(10步)+cron自动化+复盘日历。"),
   (75,"【W6·5/18-22】周报W1-W6无断档+跨团队对齐贯穿,需求/沟通/文档已较独立。DDL 6/30,推进至75%。"),
 ]),
 "7626271568236547040": ("Q2 OKR反推映射总报告", R, [  # O2-KR1  DDL 6/30→75
   (45,"【W0·4/2-3】识别'个人复盘/日报自动化'为AI赋能场景,产出复盘Agent PRD v2。"),
   (65,"【W2·4/20-26】扩展候选:AI workshop多模态语音唤醒、Slack消息管理场景。"),
   (75,"【W6·5/18-22】评测器场景确立;主线场景(复盘自动化skill)成形并开源。DDL 6/30,推进至75%。"),
 ]),
 "7626271828239060173": ("Q2 OKR反推映射总报告", R, [  # O2-KR2  DDL 6/30→70
   (40,"【W3·4/27-5/3】复盘skill v3.1完成需求拆解+方案设计(决策表/风险分层/CardKit)。"),
   (58,"【W5·5/12-17】人性化收束层评测器:两层评测架构需求拆解→方案设计闭环。"),
   (70,"【W6·5/18-22】Loona-Spec四层方案成形;评测器为最项目化产出。DDL 6/30,推进至70%。"),
 ]),
 "7626271562145024990": ("Q2 OKR反推映射总报告", R, [  # O2-KR3  DDL 6/30→75
   (45,"【W3·4/27-5/3】复盘skill接入B站热点cron跑通,推动方案实际运行。"),
   (60,"【W4·5/4-6】个人复盘skill发布GitHub(feishu-daily-review),cron稳定产出。"),
   (75,"【W6·5/18-22】评测器Langfuse真流量验证+Jarvis 209 case真验收+rowboat v1.2 513测试。DDL 6/30,推进至75%。"),
 ]),
 "7626271889488743624": ("复盘自动化项目阶段性复盘总结", D_O2KR4, [  # O2-KR4  项目末/6月→65
   (30,"【W3·4/27-5/3】三层复盘机制建成(日/周/月)。"),
   (50,"【W6·5/18-22】周报实现日报+会议纪要+本地session三源合并复盘。"),
   (65,"【W6·5/24】输出《复盘自动化项目阶段性复盘总结》(五要素)。项目末复盘待6月收口,推进至65%。"),
 ]),
 "7627421948808973250": ("4月Agent体验与问题分析(收口版)", D_O3KR1, [  # O3-KR1  DDL 4/30(已过)→100
   (40,"【W1·4/13-19】Agent评测体系前期调研(Langfuse接入)+接口测试,启动能力体验分析。"),
   (65,"【W2·4/20-26】梳理Agent指标体系+测试产出与PRD不一致项,归集体验问题。"),
   (85,"【W3·4/29】结合4/28周会与可感知指标(任务结果/过程体验/对话质量)深化问题分析。"),
   (100,"【4/30 DDL到期·收口5/24】《4月Agent体验与问题分析(收口版)》7能力维度+11条核心问题(接口217用例/97.24%、humanizer约23% FAIL),达成100%。"),
 ]),
 "7627422941223472347": ("Agent产品化方法沉淀(总纲)", D_O3KR2, [  # O3-KR2  DDL 5/31→80
   (40,"【W4·5/6-9】Knowledge Loop知识闭环方法+AI Jam分享,沉淀产品化方法雏形。"),
   (65,"【W6·5/21-22】Loona-Spec v1.0(223条机检)+用户体验Know-how+评测器方法论,四要素素材成形。"),
   (80,"【W6·5/24】《Agent产品化方法沉淀(总纲)》四要素+16条常见问题清单。DDL 5/31,推进至80%。"),
 ]),
 "7627422847853628596": ("Q2 OKR反推映射总报告", R, [  # O3-KR3  DDL 6/30→60
   (30,"【W6·5/24】方向候选(可观测+评测/记忆+知识库/CC Persona)+Loona-Spec自迭代协议作中长期路线图骨架。"),
   (60,"【6月窗口】中长期Agent方向与优先级建议成型中。DDL 6/30,按节奏推进至60%。"),
 ]),
 "7627422012026522569": ("Q2 OKR反推映射总报告", R, [  # O4-KR1  DDL 4/30(已过)→100
   (35,"【W0·4/8-9】版本规划+测试集会、长链路方案会,明确4/30版本需求与测试集方向。"),
   (60,"【W1·4/14-15】4.14全模块Agent需求PRD+430版本需求范围确定+测试集专项会共识。"),
   (85,"【W2·4/20-26】测试标注规范v1/v2+200+case;Planner 100条97%通过。"),
   (100,"【4/30 DDL到期·5/8跑测203 case】Agent需求输出+测试集建立完成,达成100%。"),
 ]),
 "7627423339209133261": ("面向6月版本需求迭代输入清单", D_O4KR2, [  # O4-KR2  DDL 5/31→80
   (40,"【W4·5/6】基于4月版本结果,在5/6转型周会做体验复盘与问题梳理。"),
   (62,"【W6·5/18-20】R4真验收抓修7 bug+5方向收敛(说人话/动态人设/记忆/播报/新场景)。"),
   (80,"【W6·5/24】《面向6月版本需求迭代输入清单》20条(9条P0)。DDL 5/31,推进至80%。"),
 ]),
 "7627422012026588105": ("Q2 OKR反推映射总报告", R, [  # O4-KR3  DDL 6/30→65
   (30,"【W5·5/12-17】整理530三线MVP需求底盘,作为6/30版本需求起点。"),
   (50,"【W6·5/19-22】研发对齐(5/19周会接棒)+know-how场景对齐+工程化分工。"),
   (65,"【6月窗口】6/30版本需求/评审/研发对齐/落地跟进推进中。DDL 6/30,按节奏推进至65%。"),
 ]),
 "7628430235122666701": ("Q2 OKR反推映射总报告", R, [  # O4-KR4  DDL 6/30→60
   (40,"【W6·5/18-22】搭建验收基础设施+真验收预演(Loona-Spec 223条+Jarvis 209 case三层+评测器112 case,抓修7 bug)。"),
   (60,"【6月窗口】6/30版本正式验收Case集(核心/异常/风险)与上线前验收推进中。DDL 6/30,按节奏推进至60%。"),
 ]),
}

def content_json(text):
    return json.dumps({"blocks":[{"block_element_type":"paragraph","paragraph":{"elements":[
        {"paragraph_element_type":"textRun","text_run":{"text":text,"style":{}}}]}}]}, ensure_ascii=False)
def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True,encoding="utf-8",shell=True)
    out=(r.stdout or "")+(r.stderr or "")
    try: ok=json.loads(r.stdout).get("ok",False)
    except: ok='"ok": true' in out
    return ok,out

print("=== DELETE existing ===")
delc=0
for kid in KRS:
    ok,out=run(["lark-cli","okr","+progress-list","--target-type","key_result","--target-id",kid,"--as","user"])
    try: ids=[p["progress_id"] for p in json.loads(out)["data"]["progress_list"]]
    except: ids=[]
    for pid in ids:
        if MODE=="real":
            dok,dout=run(["lark-cli","okr","+progress-delete","--progress-id",str(pid),"--yes","--as","user"])
            if dok: delc+=1
            else: print("  del FAIL",pid,dout[:100])
print(f"deleted={delc}")

print("=== CREATE (DDL-paced, all normal) ===")
ok=0; fail=0; idx=0
for kid,(stitle,surl,trail) in KRS.items():
    for pct,text in trail:
        fn=f"rp_{idx}.json"; idx+=1
        with open(fn,"w",encoding="utf-8") as f: f.write(content_json(text))
        cmd=["lark-cli","okr","+progress-create","--target-type","key_result","--target-id",kid,
             "--progress-percent",str(pct),"--progress-status","normal",
             "--content",f"@{fn}","--source-title",stitle,"--source-url",surl,"--as","user"]
        if MODE=="dry": cmd.append("--dry-run")
        cok,cout=run(cmd)
        print(f"  KR {kid[-4:]} {pct}% -> {'OK' if cok else 'FAIL '+cout[:150]}")
        ok+=cok; fail+=(not cok)
        try: os.remove(fn)
        except: pass
print(f"\nMODE={MODE}: created_ok={ok} fail={fail}")
