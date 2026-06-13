# 团队能力注册表（唯一事实源）

> 条目格式（新增照抄）：
> ```
> ## <能力名>
> - 干什么：一句话
> - 触发词：成员会说出的关键词，逗号分隔
> - 调用：可直接复制执行的指令
> - owner：负责人
> - 状态：可用 | 试验中 | 已废弃    登记/更新：YYYY-MM-DD
> ```
> 规则：只增量修改条目，禁止整体重排；废弃不删行，状态改「已废弃」留痕。

## loona-daily-review-v2
- 干什么：三源合并（飞书侧记会议 + Claude/Codex session + git commit）生成日报/周报，可回填飞书文档与 OKR 进展
- 触发词：周报、日报、复盘、进展汇总、写日报
- 调用：对 Claude 说「用 loona-daily-review-v2 生成本周周报」
- owner：QYL
- 状态：可用    登记：2026-06-10

## 会议纪要套件（lark-minutes / lark-vc / summarize-meeting）
- 干什么：拉取妙记/历史会议的总结、待办、逐字稿；或把纪要文本结构化成行动项
- 触发词：会议纪要、妙记、逐字稿、会议总结、待办提取
- 调用：对 Claude 说「用 lark-minutes 拉取这个妙记的总结和待办：<链接>」
- owner：QYL
- 状态：可用    登记：2026-06-10

## PM 文档套件（create-prd / user-stories / test-scenarios / wwas）
- 干什么：PRD 八段式成文、拆用户故事、生成验收测试场景
- 触发词：PRD、需求文档、用户故事、测试用例、验收标准
- 调用：斜杠命令 `/create-prd`、`/test-scenarios` 等，附上需求背景
- owner：QYL
- 状态：可用    登记：2026-06-10

## 飞书文档操作套件（lark-doc / lark-wiki / lark-base / lark-sheets / lark-im / lark-mail）
- 干什么：终端直接读写飞书文档、知识库、多维表格、电子表格、消息、邮件
- 触发词：读文档、写文档、多维表格、知识库、发消息、发邮件、批量改表格
- 调用：对 Claude 说「读取这篇飞书文档并总结：<链接>」（自动路由到对应 lark skill）
- owner：QYL
- 状态：可用    登记：2026-06-10

## AI 出图套件（skill-prompt-generator：design-master / art-master / product-master / video-master）
- 干什么：按主题（海报/UI、艺术、产品图、视频运镜）生成专业 AI 图像提示词
- 触发词：出图、海报、提示词、产品图、设计图、midjourney、即梦
- 调用：对 Claude 说「用 design-master 生成一张 <主题> 海报的提示词」
- owner：QYL
- 状态：可用    登记：2026-06-10

## 定时/工作流自动化（n8n）
- 干什么：搭定时任务和多步自动化流（定时抓取、监控、推送飞书群），已接 n8n-mcp 可直接建工作流
- 触发词：定时、监控、轮询、自动推送、爬取、每天跑一次
- 调用：对 Claude 说「用 n8n 建一个工作流：<描述触发条件和步骤>」
- owner：QYL
- 状态：可用    登记：2026-06-10

## prompt 评测（prompt-eval）
- 干什么：零 API 成本测试/打分一个工作 prompt（生成场景→盲跑→评分出记分卡），适合 A/B prompt 版本
- 触发词：测 prompt、评估提示词、prompt 打分、A/B
- 调用：对 Claude 说「用 prompt-eval 评估这个 prompt：<内容>」
- owner：QYL
- 状态：可用    登记：2026-06-10

## skill 制作（lark-skill-maker / superpowers writing-skills）
- 干什么：把流程固化成可复用 skill；lark 域用 lark-skill-maker，通用域用 writing-skills（TDD 式写 skill）
- 触发词：做个 skill、沉淀、固化流程、封装
- 调用：对 Claude 说「用 writing-skills 把 <流程> 做成 skill」
- owner：QYL
- 状态：可用    登记：2026-06-10

## 去 AI 味改写（shuorenhua / humanizer）
- 干什么：清理文本里的 AI 套路腔，中文用 shuorenhua，英文用 humanizer
- 触发词：去 AI 味、说人话、自然一点、别像模板
- 调用：对 Claude 说「用 shuorenhua 改写这段：<文本>」
- owner：QYL
- 状态：可用    登记：2026-06-10

## 深度调研（deep-research）
- 干什么：多源网络搜索 + 交叉验证 + 引用出处的深度调研报告
- 触发词：调研、竞品分析、行业报告、查一下全网
- 调用：对 Claude 说「/deep-research <要研究的问题>」
- owner：QYL
- 状态：可用    登记：2026-06-10
