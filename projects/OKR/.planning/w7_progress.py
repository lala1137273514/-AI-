# -*- coding: utf-8 -*-
# W7 周报 OKR 进展（增量 progress-create，不删除既有记录；status 恒 normal；W7 值 >= 当前最新值）
import json, subprocess, sys, os
os.chdir(r"C:\Users\QYL\Desktop\OKR")
MODE = sys.argv[1] if len(sys.argv) > 1 else "dry"  # dry | real

WEEKLY = "https://f4x6dn8llc.feishu.cn/docx/MDfJddB3Lotq3ix2tT3cRZTbnJc"  # W7 周报 docx
TRAVEL = "https://f4x6dn8llc.feishu.cn/docx/YUusdlMvUoM5DbxPtEtc32b0nMb"  # 旅行规划 v1
CC     = "https://f4x6dn8llc.feishu.cn/docx/FhtSd9xAQobIJzxwXgjcIcynnyp"  # CC 风格化提示词
TESTSET= "https://f4x6dn8llc.feishu.cn/docx/BmOqdhWjkocu6Txi9jacBBhmnZb"  # 测试集专项纪要
UICHK  = "https://f4x6dn8llc.feishu.cn/docx/QTiKdCkOpoI39nxSU59cYgx9nvo"  # UI 核对纪要
DEVWIKI= "https://f4x6dn8llc.feishu.cn/docx/If7Wwz0zLiwo4dk8nzXctL5Yn1g"  # 本地开发 Wiki

# (kid, pct, source_title, source_url, [paragraphs])
RECS = [
 ("7626271435473177779", 77, "旅行规划 · 交付版 v1（T1）", TRAVEL, [
   "【W7·5/25-5/31】把「旅行规划」彻底拆为一条独立可交付的小模块需求线，五要素齐全：边界（只复用 TravelView 轮播两卡、只调 get_weather/web_search，禁用地图/POI/住宿/比价/订票）、槽位（必填 destination/duration_days + 6 选填）、流程（Router→抽槽→澄清停等→合槽→并行查→按 span 切卡→填点位）、异常（工具失败降级、JSON 不合法重试不交半截）、验收（12 条 A1-A12 场景）。",
   "同步产出《CC 风格化输出提示词》作为另一独立可复用模块：两步管道（去模板+注入人格）、事实保真>风格铁律、毒舌 Lv0-3 分层、protected spans 1:1 保真，可作通用风格化重写组件。",
   "两个模块均为「目标·场景·流程·异常·边界」齐备的可验收交付，KR 按 6/30 节奏推进至 77%。",
 ]),
 ("7626271274969844667", 77, "2026-05-25 ~ 2026-05-31 周报（W7）", WEEKLY, [
   "【W7·5/25-5/31】日报周报持续无断档（W7 周报三源合并落地：飞书 12 篇 + 本地 git 6 仓 75 commits + Claude/Codex session），跨团队协作贯穿全周：测试集专项会、标准对齐分工会、轮播卡片样式会、旅行规划+搜索 UI 核对会四场对齐，每场均沉淀决策+分工。",
   "复盘体系持续工程化：搭建个人复盘归档结构（日复盘/作品交付物/月度归档），晨检 09:30 自动推送 Todo 卡片、日复盘文档自动生成八大块。",
   "稳定需求输出与协作习惯持续保持，KR 进行中 77%。",
 ]),
 ("7626271568236547040", 77, "2026-05-25 ~ 2026-05-31 周报（W7）", WEEKLY, [
   "【W7·5/25-5/31】新增并定义实时语音交互场景：loona-live 从 0 到开源级 showcase（2 天 25 commits），打通中文实时 STT（GPU CUDA ~0.3s/句）+ 自然轮次/barge-in + 流式 TTS + LiveKit 自定义 UX frames + HITL 确认门 + 本地 RAG 混检知识库（BM25+向量 RRF）。",
   "识别并立项「主动提醒/通用定时任务」赋能场景（用户用话描述→定时执行→通知），完成功能框架（记录聊天事件→提前 1 天/2 小时触发→未在线检测适配）。",
   "AI 赋能场景识别与定义持续推进，KR 77%。",
 ]),
 ("7626271828239060173", 73, "Agent 服务本地开发 + 轮播/旅行规划说明", DEVWIKI, [
   "【W7·5/25-5/31】旅行规划完成「需求拆解→方案设计→协作落地」闭环：T1 规格（主/澄清/口播三段 prompt + TravelPayload 契约）→ v2 卡片切分（span=ceil(总天数/5) 封顶 5 张）与口播重构 → 刘旭拍板字段结构（6+3 字段、去 ref）→ 周子夏出 UI 图协作落地。",
   "人设提示词拆解为主人设 + 场景功能人设（新闻播报员/旅行规划师）+ 情绪三层，明确迭代与整合方案；轮播交互（单卡左右滑/list 高亮）与本地开发方式一次会拍板。",
   "需求拆解到协作闭环能力稳步推进，KR 73%。",
 ]),
 ("7626271562145024990", 78, "2026-05-25 ~ 2026-05-31 周报（W7）", WEEKLY, [
   "【W7·5/25-5/31】本周是 Q2 落地最厚的一周：旅行规划轮播通道在真栈打通（澄清→承接句→卡片流+轮播），修复 create_event/dance tool/重复回复三个 Bug，planner 旅游段重构为状态机门控+强化防重播，集成 Unsplash 补图；本地 cortex 仓 33 commits 落地。",
   "loona-live 实时语音 Agent 从 0 跑通到开源级 showcase（GPU STT/流式 TTS/Docker 一键栈/CER eval/CI），loona-workbench v1.2 九场景理想交互链路 demo + Jarvis Replay 真验收引擎（R0-R4）+ A/B 引擎切换。",
   "AI 场景实现/跑通/落地全面推进，KR 按 6/30 节奏 78%。",
 ]),
 ("7627422941223472347", 85, "CC 风格化输出提示词", CC, [
   "【W7·5/25-5/31】方法沉淀逼近 5/31 DDL 收口：产出《CC 风格化输出提示词》，把「输出该长什么样」方法化——两步管道（说人话去模板→注入 CC 人格上色）、优先级铁律（事实保真 > CC 风格 > 人性化收束）、protected spans 1:1 保真清单、毒舌 Lv0-3 与说人话禁用项三 Tier、提交前两遍回读。",
   "旅行规划沉淀两条可复用产品判断：「口播为主要内容载体（卡片信息量小是结构性限制）」、「卡片切分用 span=ceil(总天数/5) 统一公式替代经验分档」；评测侧建「代码级 + LLM 断言」双重主观场景评估标准。",
   "四要素（需求定义/体验设计/评估维度/常见问题）持续加厚，KR 冲至 85%。",
 ]),
 ("7627422012026522569", 100, "智能纪要：测试集专项 2026年5月25日", TESTSET, [
   "【W7·5/25-5/31】4/30 版本测试集工作已达成，本周以回归框架延伸佐证：测试集 700+ case（router 200 / planner 520+）全功能全工具覆盖，大模型标注+人工校正后通过率 76.8%；确立分级执行（P0/P1 跑 3-5 次、P2-P3 跑 1-2 次）、失败重跑 1→2-3 次综合判定、badcase 阈值方法（50%/75%）。",
   "沉淀 12 条 A1-A12 旅行规划验收场景作 case 库（标准链路/强制澄清/多城切卡/工具失败降级/schema 校验），明确「实现不能只看成都示例」。",
   "KR 保持 100% 达成，持续以回归 case 库巩固。",
 ]),
 ("7627423339209133261", 83, "旅行规划和搜索UI核对讨论 智能纪要", UICHK, [
   "【W7·5/25-5/31】持续把 5 月暴露问题转为 6 月迭代输入：诊断人设 fewshot 过多致过拟合、人设过高冷，定方向减少负面约束 + 换旗舰/量化模型对比；loona_agent_test 三轮均 ~25% 失败率（176-182/757）纳入排查清单。",
   "测试集结构性噪声归因（断言假阴性约 20+ 条 + 响应体字段不稳定），给出「解掉两类噪声后通过率可上 85%」的迭代路径；赵静三场景轮播播报暴露 P0/P1 合并播报问题，转为播报验收规则。",
   "6 月迭代输入清单持续加厚，KR 逼近 5/31 收口至 83%。",
 ]),
 ("7627422012026588105", 68, "2026-05-25 ~ 2026-05-31 周报（W7）", WEEKLY, [
   "【W7·5/25-5/31】研发对齐密集推进：确定 5/30 Demo 展示方案（治利手机端优先 / 刘旭 webUI 兜底）、代码合并方案（qyl+testHEN 合主分支后全员重拉）、线上模型选型评估（伽马≈GPT-3.5 但快 vs 千问 3.5 35B/27B 量化）。",
   "打通 Agent 服务本地开发链路（refactor 分支 + 本地 redis/postgres + 日本测试服务器工具服务），Cortex 仓写权限开通、配置指南 Wiki 落地，摆脱依赖单点飞书操作。",
   "6/30 版本研发对齐与需求推进按节奏至 68%。",
 ]),
 ("7628430235122666701", 65, "旅行规划 · 交付版 v1（A1-A12 验收）", TRAVEL, [
   "【W7·5/25-5/31】验收标准与关键 Case 显著加厚：旅行规划交付 12 条 A1-A12 可回归验收场景 + cards≤5/ref 合法/无 trip_footer 的输出 schema 校验规则 + TravelPayload 可验证数据契约（顶层 9 字段 / TravelCard 7 字段 / TravelNode 3 字段，每字段带长度预算防破版）。",
   "播报验收规则定版（P0+P1 全念 / P1≤3 条、P2+P3 概括），作为轮播交付的关键验收口径。",
   "6/30 验收标准与关键 Case 集持续成形，KR 推进至 65%。",
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
print(f"== W7 OKR progress  MODE={MODE}  ({len(items)}/{len(RECS)} records) ==")
for kid,pct,st,su,paras in items:
    fn=f"w7_{idx}.json"; idx+=1
    with open(fn,"w",encoding="utf-8") as f: f.write(content_json(paras))
    cmd=f'lark-cli okr +progress-create --target-type key_result --target-id {kid} --progress-percent {pct} --progress-status normal --content @{fn} --source-title "{st}" --source-url "{su}" --as user'
    if MODE=="dry": cmd+=" --dry-run"
    cok,cout=run(cmd)
    print(f"  KR …{kid[-4:]} {pct}% ({len(paras)}段) -> {'OK' if cok else 'FAIL: '+cout[:200]}")
    ok+=cok; fail+=(not cok)
    try: os.remove(fn)
    except: pass
print(f"\nMODE={MODE}: ok={ok} fail={fail}")
