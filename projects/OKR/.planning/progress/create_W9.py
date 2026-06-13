import json
import subprocess
import os

# lark-cli path
lark_cli = r"C:\Users\QYL\AppData\Roaming\npm\lark-cli.cmd"

# Week 9 progress records - 8 KRs with activity
records = [
    {
        "kr_id": "7626271435473177779",
        "label": "O1-KR2",
        "percent": 75,
        "content_blocks": [
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "【W9·06-13】修复 plan_options 路由 bug：compose_options 任务此前 0 次被调用，方案三选一卡从未生成，在 cortex-fresh/cortex refactor 分支定位并修复。", "style": {}}}]}},
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "将 loona-travel-flow skill 的旅行规划交互契约翻译为 compose_trip_options.yaml 和 compose_trip.yaml 的 LLM 提示词。先只读分析全链路避免过拟合，再做内容质量优化。当前：分析完成，具体提示词段落修改仍在迭代，未到可验收。", "style": {}}}]}},
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "分析 REC_20260610_193020 转录文本 review planner 提示词写法，对比非旅行规划提示词模式找可复用思路。", "style": {}}}]}},
        ]
    },
    {
        "kr_id": "7626271274969844667",
        "label": "O1-KR3",
        "percent": 75,
        "content_blocks": [
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "【W9·06-13】周报/日报持续输出：飞书六天日报（cron 06-07~10 掉线期间通过本地扫描+会议纪要补全），W9 周报完成三源合并（飞书+本地 Claude+Codex）经双质检。", "style": {}}}]}},
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "AI 产品实习生面试支持：完成苏丽琴（6/11 NLP 背景）和张越（6/12 JHU 系统工程）面试，创建面试 SOP 文档。面试反馈待补。", "style": {}}}]}},
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "CLAUDE.md 规则迭代：新增并行拆分规则——多 session/多 agent 并行，减少时间与上下文隔离。", "style": {}}}]}},
        ]
    },
    {
        "kr_id": "7626271568236547040",
        "label": "O2-KR1",
        "percent": 75,
        "content_blocks": [
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "【W9·06-13】AI 内部赋能专项正式启动（6/9 Kickoff，全员 9 人），确定三方向——AI Coach（教新人用 AI）、AI for design（生图锚点+双审计 agent+组件库规范输出）、AI for test（插扣读日志定位代码行+测试自动化）。", "style": {}}}]}},
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "6/11 对齐会三线 demo 展示：何尔宁项目驾驶舱/锚点方案/日志定位，秦宇龙 OpenClaw bot（sense-think-act），程楠测试框架+营销海报自动化。节奏：周二三做 demo→周四对齐→周五验收→第二周工程化。", "style": {}}}]}},
        ]
    },
    {
        "kr_id": "7626271828239060173",
        "label": "O2-KR2",
        "percent": 70,
        "content_blocks": [
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "【W9·06-13】旅行规划提示词从 skill 到 LLM 转换：loona-travel-flow → compose_trip_options.yaml + compose_trip.yaml，7 个 session 完成只读分析避免过拟合，进入初步调优，未到可验收阶段。", "style": {}}}]}},
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "Agent UI 协议对齐（6/9 会议，秦宇龙/何尔宁/刘旭）：覆盖天气/日程/邮件/餐厅/新闻/旅行规划 UI 链路，敲定 AtoUI 协议——agent 直控前端显示，往模板槽位填 JSON。旅行规划由秦宇龙整理完整文档发刘旭作为测试用例。", "style": {}}}]}},
        ]
    },
    {
        "kr_id": "7626271562145024990",
        "label": "O2-KR3",
        "percent": 75,
        "content_blocks": [
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "【W9·06-13】OpenClaw bot demo 展示（6/11 AI 内部赋能对齐会）：基于 sense-think-act 架构，可在飞书群接收消息、澄清需求、推荐 bot。当前功能较简单，后续可扩展到写 PRD 等流程。", "style": {}}}]}},
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "AI 赋能专项三线 demo 对齐：完成驾驶舱/锚点设计/测试自动化三线 demo 展示与方向收敛，周五 demo 验收 + 工程化落地可行性评估待推进。", "style": {}}}]}},
        ]
    },
    {
        "kr_id": "7627422941223472347",
        "label": "O3-KR2",
        "percent": 80,
        "content_blocks": [
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "【W9·06-13】Loona 交互工作台：立统一 UI Spec 铁律，本地调通基础交互（HTML/CSS/JS 零依赖），尚未正式演示。", "style": {}}}]}},
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "Agent UI 链路整理：完成天气/日程/邮件/餐厅/新闻/旅行规划 6 类工具 UI 链路文档化，明确 toast 交互、卡片互斥策略、轮播设计。旅行规划链路封装为 loona-travel-flow skill。", "style": {}}}]}},
        ]
    },
    {
        "kr_id": "7627422847853628596",
        "label": "O3-KR3",
        "percent": 60,
        "content_blocks": [
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "【W9·06-13】AI 赋能专项方向探索：参与 AI Coach / AI for design / AI for test 三方向 Kickoff 与对齐，确认 AI Coach 长期价值——降低公司内部 AI 使用门槛，将经验累积为知识库 + case/demo 复用。", "style": {}}}]}},
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "下周待办：整理云文档接入方式文档 + OpenClaw bot 经验库搭建，发团队共享，为后续路线图提供实践基础。", "style": {}}}]}},
        ]
    },
    {
        "kr_id": "7627422012026588105",
        "label": "O4-KR3",
        "percent": 65,
        "content_blocks": [
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "【W9·06-13】Agent UI 协议对齐（6/9）：敲定 AtoUI 协议方案——agent 直接控制前端显示，往固定模板槽位填 JSON 信息，产品侧定义 UI 规则时可直接影响 agent 输出。后续需子夏定义组件库规则和容器规则。", "style": {}}}]}},
            {"block_element_type": "paragraph", "paragraph": {"elements": [{"paragraph_element_type": "textRun", "text_run": {"text": "630 agent 文档产物生成（6/13 编辑）：推进 630 版本需求文档维护。旅行规划完整文档整理发刘旭作为 Agent UI 测试方案用例待完成。", "style": {}}}]}},
        ]
    },
]

base_dir = "C:/Users/QYL/Desktop/OKR/.planning/progress"
os.makedirs(base_dir, exist_ok=True)

source_url = "https://f4x6dn8llc.feishu.cn/docx/MvtXdcTvBoTz0hx64eicXPMSnng"  # W8 weekly report URL placeholder
source_title = "W9周报 2026-06-07~06-13"

for r in records:
    # Write block JSON file
    block_path = os.path.join(base_dir, f"{r['label']}_W9.json")
    block_data = {"blocks": r["content_blocks"]}
    with open(block_path, "w", encoding="utf-8") as f:
        json.dump(block_data, f, ensure_ascii=False, indent=2)

    # Run progress-create (content @ needs relative path, cwd already set to base_dir)
    rel_path = f"{r['label']}_W9.json"
    cmd = [
        lark_cli, "okr", "+progress-create",
        "--target-type", "key_result",
        "--target-id", r["kr_id"],
        "--progress-percent", str(r["percent"]),
        "--progress-status", "normal",
        "--content", f"@{rel_path}",
        "--source-title", source_title,
        "--source-url", source_url,
        "--as", "user"
    ]

    print(f"\n{'='*60}")
    print(f"Creating progress for {r['label']} ({r['kr_id']}) at {r['percent']}%")
    print(f"Block file: {block_path}")

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=base_dir)
    print(f"STDOUT: {result.stdout.strip()}")
    if result.stderr.strip():
        print(f"STDERR: {result.stderr.strip()}")
    print(f"Exit: {result.returncode}")

print("\nDone!")