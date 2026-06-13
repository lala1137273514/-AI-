# -*- coding: utf-8 -*-
import json, subprocess, sys, os

os.chdir(r"C:\Users\QYL\Desktop\OKR")
MODE = sys.argv[1] if len(sys.argv) > 1 else "dry"  # dry | real

REPORT = "https://f4x6dn8llc.feishu.cn/docx/PNNfdUYkPoynF9xMkZicnDh3n28"
recs = [
 # id, percent, status, source_title, source_url, text
 ("7626271491483389119",100,"done","Q2 OKR反推映射总报告",REPORT,
  "入职1-2周完成六步产品认知+情感交互架构(11图)+新人项目交接报告+第一周汇报对齐;后续经周会/Agent指标/Wiki化持续校验。详见Q2 OKR反推映射总报告。"),
 ("7626271435473177779",100,"done","Q2 OKR反推映射总报告",REPORT,
  "承接≥3个非Agent小模块需求(手机端应用管理PRD/430记忆管理/530三线MVP),目标·场景·流程·异常·边界五要素齐全,并沉淀\"可验收PRD模板\"。"),
 ("7626271274969844667",92,"normal","Q2 OKR反推映射总报告",REPORT,
  "日报近乎日更、周报W1-W6无断档、跨团队对齐贯穿全程;复盘从习惯升级为daily-review skill(10步)+cron自动化+复盘日历。Q2进行中,持续保持。"),
 ("7626271568236547040",100,"done","Q2 OKR反推映射总报告",REPORT,
  "独立识别定义≥3个AI赋能场景,主线=个人复盘/日报自动化skill(已开源feishu-daily-review),另含人性化收束层评测器、语音唤醒。"),
 ("7626271828239060173",92,"done","Q2 OKR反推映射总报告",REPORT,
  "围绕主线场景完成需求拆解→方案设计→协作推进完整闭环;人性化收束层评测器为最项目化产出。"),
 ("7626271562145024990",100,"done","Q2 OKR反推映射总报告",REPORT,
  "推动落地三种结果全命中——复盘skill cron落地+GitHub开源、评测器Langfuse真流量验证、Jarvis 209 case真验收+rowboat v1.2 513测试。"),
 ("7626271889488743624",80,"normal","复盘自动化项目阶段性复盘总结","https://f4x6dn8llc.feishu.cn/docx/JPwUdy6cFobBTRx0CBecSg63n42",
  "输出复盘自动化项目阶段性复盘总结(五要素:场景问题/方案价值/验证结果/关键问题/下一步);项目仍在迭代,待主线收口后升级为正式项目末复盘。"),
 ("7627421948808973250",90,"done","4月Agent体验与问题分析(收口版)","https://f4x6dn8llc.feishu.cn/docx/Qc6wd4nzSoScx6xwUOMcx1mQn8b",
  "完成《4月Agent体验与问题分析(收口版)》:7能力维度体验分析+11条核心问题(含接口测试217用例/97.24%、humanizer约23% evidence FAIL等真实证据)。注:deadline 4/30,本记录为逾期补登。"),
 ("7627422941223472347",90,"normal","Agent产品化方法沉淀(总纲)","https://f4x6dn8llc.feishu.cn/docx/UZqCd3V20o24LHxnoMHcMHTDnff",
  "形成《Agent产品化方法沉淀(总纲)》:需求定义(Loona-Spec 223条机检)/体验设计(交互四环节+结果卡)/评估维度(评测三层+收束层评测器)/16条常见问题清单,四要素齐全。"),
 ("7627422847853628596",12,"normal","Q2 OKR反推映射总报告",REPORT,
  "6月窗口未到,尚未正式启动;已有方向候选(可观测+评测/记忆+知识库/CC Persona)及Loona-Spec自迭代协议可作中长期路线图雏形。"),
 ("7627422012026522569",100,"done","Q2 OKR反推映射总报告",REPORT,
  "围绕4/30版本输出全模块Agent需求+协助建200+case测试集(标注规范v1/v2/MVP模板/评测平台方案/接口测试报告);430版本顺延属外部因素,该KR工作已超额完成。"),
 ("7627423339209133261",90,"normal","面向6月版本需求迭代输入清单","https://f4x6dn8llc.feishu.cn/docx/XYpCdjwj0o5gCaxx7gXcZ2ONnch",
  "5月完成问题整理(69失败case归因+R4真验收7 bug)+体验复盘+5方向收敛,形成《面向6月版本需求迭代输入清单》20条(9条P0)。"),
 ("7627422012026588105",50,"normal","Q2 OKR反推映射总报告",REPORT,
  "6/30版本前期推进充分:需求底盘(530三线MVP)+交互规范(Loona-Spec 223条)+研发对齐(5/19周会接棒)+工程化分工;正式评审/研发对齐/落地跟进在6月,进行中。"),
 ("7628430235122666701",45,"normal","Q2 OKR反推映射总报告",REPORT,
  "验收基础设施已建并完成一次真验收预演(Loona-Spec 223条+Jarvis 209 case三层验收+评测器112 case,已抓修7 bug);针对6/30版本的正式验收Case集与上线验收在6月,进行中。"),
]

def content_json(text):
    return json.dumps({"blocks":[{"block_element_type":"paragraph","paragraph":{"elements":[
        {"paragraph_element_type":"textRun","text_run":{"text":text,"style":{}}}]}}]}, ensure_ascii=False)

items = recs[:1] if MODE=="dry" else recs
ok=0; fail=0
for i,(kid,pct,status,stitle,surl,text) in enumerate(items):
    fn = f"pc_{i}.json"
    with open(fn,"w",encoding="utf-8") as f: f.write(content_json(text))
    cmd = ["lark-cli","okr","+progress-create","--target-type","key_result","--target-id",kid,
           "--progress-percent",str(pct),"--progress-status",status,
           "--content",f"@{fn}","--source-title",stitle,"--source-url",surl,"--as","user"]
    if MODE=="dry": cmd.append("--dry-run")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", shell=True)
    out = (r.stdout or "") + (r.stderr or "")
    try:
        j = json.loads(r.stdout)
        good = j.get("ok", False)
    except Exception:
        good = ('"ok": true' in out) or (MODE=="dry" and r.returncode==0)
    print(f"[{i}] KR {kid} pct={pct} {status} -> {'OK' if good else 'FAIL'}")
    if not good: print("   ", out[:500].replace("\n"," "))
    if good: ok+=1
    else: fail+=1
    try: os.remove(fn)
    except: pass
print(f"\nMODE={MODE} done: ok={ok} fail={fail}")
