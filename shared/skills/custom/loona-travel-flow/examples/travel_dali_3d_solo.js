/* 大理 3 天 · 一个人（独行）—— loona-travel-flow 标杆 example（13 节点链路）
   这是 skill 自己的 examples 目录，case key=travel_dali_3d_solo，不覆盖 workbench 同名案。
   相对 workbench v4 案的三处新设计（验收标准）：
     ① 澄清 1→3 轮：每轮一张 ClarifyCard + 一段口播 QUESTION。
        轮1 几人/几天/出发日期；轮2 预算档(只搜参考不算总账)+会不会骑车；轮3 必去/节奏 + 沉淀前两轮进 confirmed。
     ② 方案三选一：InspoFlow 正好 3 张，正好 1 张 rec=true 主推（A 洱海骑行慢线[主推] / B 古城文艺 / C 苍山出片）；
        主推 punchline 带「这条我更推」个人倾向 + 一个立刻想去的具体理由；另两张各一句带过。
     ③ 选完直出规划：不再问「要不要过一遍」；规划第一段口播带 1-2 句过渡接上选中方案。
   收尾：排日历(ListCard) + 天气提醒；全程不算预算/不订房/不下单。
   出发日期：6/8 下午到（到达日 light）→ 6/8-6/10 三天。
   口播：能复用 workbench 已破透版的就复用（方案/规划/收尾段）；3 轮澄清是新写原创。
   照片/资源路径沿用 workbench 同款 assets/travel/*.jpg。 */
(function (g) {
  g.LOONA_CASES = g.LOONA_CASES || {};

  /* 三天日程（各天一张时间轴日程卡）。
     单天完整天铺满 上午/中午/下午/晚上 四档；到达日(Day1 下午到)按到达时段铺。
     node 字段：time/place/note + 衔接 transport_to_next/distance_to_next/duration_to_next/highlight/star。
     长度守上限：label≤18、place≤14、note≤42、reminder≤22。 */
  var DALI_DAYS = [
    {
      id: 'dali_d1', day: 'Day1', place: '古城热身', tag: '步行', thumb: 'assets/travel/dl_gucheng.jpg',
      label: 'Day 1 · 古城热身', pace: 'light', photo: 'assets/travel/dl_gucheng.jpg',
      theme: '古城热身', transport: '步行', total: '当天都在古城里',
      reminder: '午后到先松松，啥也别赶',
      nodes: [
        { time: '下午', place: '到大理 · 进古城', note: '午后到，先松松，啥也不赶',
          transport_to_next: 'walk', distance_to_next: '步行 5 分钟' },
        { time: '下午', place: '人民路', note: '顺着老街瞎晃，看哪家顺眼进哪家',
          transport_to_next: 'walk', distance_to_next: '同条街' },
        { time: '晚上', place: '古城吃饵丝', note: '热乎的饵丝配烤乳扇，第一天就这么收' }
      ],
      footer: '都在古城里，全程步行，慢半拍'
    },
    {
      id: 'dali_d2', day: 'Day2', place: '环洱海 · 看日落', tag: '★ 重头', thumb: 'assets/travel/dl_erhai.jpg',
      label: 'Day 2 · 环洱海骑行', pace: 'normal', photo: 'assets/travel/dl_erhai.jpg',
      theme: '环洱海骑行', transport: '骑行', total: '全程约 25km',
      reminder: '傍晚湖边风大，带件外套',
      nodes: [
        { time: '上午', place: '才村码头', note: '取车出发，沿环海西路骑',
          transport_to_next: 'bike', distance_to_next: '骑行 8km', duration_to_next: '约 40 分' },
        { time: '中午', place: '海西生态廊道', note: '贴着湖骑，顺眼就停下拍，湖边随便吃口歇腿',
          transport_to_next: 'bike', distance_to_next: '骑行 12km', duration_to_next: '约 1 小时' },
        { time: '下午', place: '理想邦', note: '白房子一片，慢慢拍',
          transport_to_next: 'bike', distance_to_next: '骑行 5km', duration_to_next: '约 25 分' },
        { time: '晚上', place: '龙龛码头', note: '太阳落那会儿湖面金晃晃的，坐下看它沉到水里', highlight: true, star: true }
      ],
      footer: '环洱海一圈，傍晚收在龙龛看日落'
    },
    {
      id: 'dali_d3', day: 'Day3', place: '喜洲 · 返程', tag: '收尾', thumb: 'assets/travel/dl_xizhou.jpg',
      label: 'Day 3 · 喜洲 · 返程', pace: 'normal', photo: 'assets/travel/dl_xizhou.jpg',
      theme: '喜洲 · 返程', transport: '公交 / 大巴', total: '午后赶飞机正好',
      reminder: '粑粑边走边吃，留够赶机时间',
      nodes: [
        { time: '上午', place: '古城 → 喜洲', note: '公交过去，路上看田',
          transport_to_next: 'bus', distance_to_next: '约 40 分' },
        { time: '中午', place: '喜洲古镇', note: '白墙黛瓦的老镇子，稻田边走走拍拍',
          transport_to_next: 'walk', distance_to_next: '镇子里' },
        { time: '下午', place: '喜洲 → 机场', note: '热乎的喜洲粑粑买一个边走边吃，再坐大巴去机场' }
      ],
      footer: '喜洲收个尾，午后从容赶飞机'
    }
  ];

  /* 节点10「不满意改」用：用户嫌 Day3 喜洲去过了，换成古城没逛够的慢收尾。
     同 card_id 'dali_plan' 覆盖重发，靠 pace/标题体现改过，不贴「✓已调整」表功标签。 */
  var DALI_D3_ALT = {
    id: 'dali_d3', day: 'Day3', place: '古城慢收尾', tag: '收尾', thumb: 'assets/travel/dl_gucheng.jpg',
    label: 'Day 3 · 古城慢收尾', pace: 'light', photo: 'assets/travel/dl_gucheng.jpg',
    theme: '古城慢收尾', transport: '步行', total: '午后从容赶飞机',
    reminder: '逛到点就走，留够赶机时间',
    nodes: [
      { time: '上午', place: '古城没逛的巷子', note: '挑头天没走到的几条巷子，慢慢晃',
        transport_to_next: 'walk', distance_to_next: '古城里' },
      { time: '中午', place: '院子餐馆', note: '找个院子吃顿正经的，把没尝的本地菜补上' },
      { time: '下午', place: '古城 → 机场', note: '大巴去机场，路上眯一会儿' }
    ],
    footer: '不去喜洲了，古城没逛够的补上，更松'
  };

  function days() { return [DALI_DAYS[0], DALI_DAYS[1], DALI_DAYS[2]]; }
  function daysRevised() { return [DALI_DAYS[0], DALI_DAYS[1], DALI_D3_ALT]; }

  g.LOONA_CASES['travel_dali_3d_solo'] = {
    task_id: 'travel_dali_3d_solo', title: '大理3天 · 独行（清静·爱拍）· 3轮澄清+三选一', scene: 'travel', default_skin: 'glass',
    decision_record: { request_type: 'task', primary_need: '排大理三天', granularity: 'by_segment', evidence_level: 'E1', action_risk: 'R0', output_mode: 'document', tool_plan: 'query', confirmation_required: false },
    events: [
      /* ===== ① 起手：开放求建议 ===== */
      { t: 0, gap_ms: 0, comp: 'user_query', text: '最近想去大理玩几天，你有什么建议吗？' },
      { t: 250, gap_ms: 300, comp: 'agent_step', internal: true, label: 'ROUTER · 接需求',
        decision: 'travel=NEW → planner。已知目的地=大理；缺人数/天数/日期/预算/骑车/必去/节奏。进 3 轮澄清：轮1 人数天数日期。',
        fields: ['scene:travel', '缺:人数/天数/日期', 'clarify=3轮'] },

      /* ===== ② 澄清轮1：几人 / 几天 / 出发日期 ===== */
      { t: 600, gap_ms: 500, comp: 'agent_step', internal: true, label: 'CLARIFY·轮1 · 人数天数日期',
        decision: 'Mode C / QUESTION。问几人几天 + 出发日期(日期定排期和天气)。confirmed=大理；assumed=短途/这阵子走。',
        fields: ['ClarifyCard·R1', 'card_id:clarify_dali_r1', '问:人数/天数/日期'] },
      { t: 1000, gap_ms: 800, comp: 'ClarifyCard', card_id: 'clarify_dali_r1', wait_for_user: true,
        tts: { text: '行，大理我熟。几个人去、待几天？大概啥时候走，我顺手把那几天天气看了。', pace: 'mid' },
        content: {
          title: '啥时候走',
          understand: {
            known: ['大理'],
            memory: ['爱清静', '出门爱拍', '不爱扎堆']
          }
        } },
      { t: 0, gap_ms: 800, comp: 'user_query', text: '就我一个人，待 3 天，后天出发。' },

      /* ===== ③ 澄清轮2：预算档(只搜参考不算总账) + 会不会骑车 ===== */
      { t: 300, gap_ms: 400, comp: 'agent_step', internal: true, label: 'CLARIFY·轮2 · 预算+骑车',
        decision: 'Mode C / QUESTION。预算只定搜索档位、不算总账；问会不会骑车(大理主推=环洱海骑行，不会骑方案就崩)。',
        fields: ['ClarifyCard·R2', 'card_id:clarify_dali_r2', '问:预算档/骑车', 'no总账'] },
      { t: 600, gap_ms: 800, comp: 'ClarifyCard', card_id: 'clarify_dali_r2', wait_for_user: true,
        tts: { text: '预算大概啥档，我搜客栈和吃的好有个准，不算总账啊。对了，你会骑车不？', pace: 'mid' },
        content: {
          title: '预算和骑车',
          understand: {
            known: ['一个人', '大理', '3 天', '后天走'],
            memory: ['想住带院子的', '吃本地小馆']
          }
        } },
      { t: 0, gap_ms: 800, comp: 'user_query', text: '中档就行，会骑车。' },

      /* ===== ④ 澄清轮3：必去 / 节奏 + 沉淀前两轮进 confirmed ===== */
      { t: 300, gap_ms: 400, comp: 'agent_step', internal: true, label: 'CLARIFY·轮3 · 必去+节奏(收口)',
        decision: 'Mode C / QUESTION。前两轮答的全沉淀进 known；只剩必去/节奏影响方案。答完即收口去搜索，不凑轮数。',
        fields: ['ClarifyCard·R3', 'card_id:clarify_dali_r3', '问:必去/节奏', 'known沉淀齐'] },
      { t: 600, gap_ms: 800, comp: 'ClarifyCard', card_id: 'clarify_dali_r3', wait_for_user: true,
        tts: { text: '好嘞，3 天你一个人，中档，会骑车。有啥非去不可的不？想玩满点还是松点？', pace: 'mid' },
        content: {
          title: '必去和节奏',
          understand: {
            known: ['一个人', '大理', '3 天', '后天走', '中档', '会骑车'],
            memory: ['洱海骑行当主线', '爱拍照']
          }
        } },
      { t: 0, gap_ms: 800, comp: 'user_query', text: '没特别想去的，你挑。松一点吧，别太赶。' },
      { t: 300, gap_ms: 300, comp: 'agent_step', internal: true, label: 'PLANNER · 完备 → 搜索',
        decision: '核心输入齐：一个人/3天/后天走/中档/会骑车/节奏松/必去=授权挑+爱拍(记忆)。进搜索→出 3 方案。', fields: ['完备', '去搜索', '3方案'] },

      /* ===== ⑤⑥ 搜索 + 方案生成：InspoFlow 三张等宽大图，A 主推 rec★ =====
         echo 只共情(不评方案不导购)；A 主推 punchline 带「这条我更推」+ 一个立刻想去的具体理由；B/C 各一句带过、不剧透日落。 */
      { t: 600, gap_ms: 400, comp: 'toast', text: '搜索中', state: 'searching', dismiss_on: 'card' },
      { t: 1000, gap_ms: 1200, comp: 'InspoFlow', card_id: 'dali_plans', visual_state: 'active',
        content: {
          echo: '大理必去就洱海、古城、苍山，好玩的是环湖骑行、巷子瞎逛、上山看云海。按你清静又爱拍，我归成三种走法',
          cards: [
            { id: 'A', rec: true, title: '洱海骑行慢线', photo: 'assets/travel/dl_erhai.jpg',
              tags: ['骑行', '慢', '出片'],
              punchline: '这条我更推，绕湖骑一圈才看得到那片海，正好这季节水最清' },
            { id: 'B', title: '古城文艺', photo: 'assets/travel/dl_gucheng.jpg',
              tags: ['巷子', '文艺', '逛吃'],
              punchline: '想稳点就这个，古城巷子多，逛饿了随手找口吃的' },
            { id: 'C', title: '苍山出片', photo: 'assets/travel/dl_cangshan.jpg',
              tags: ['登高', '出片', '视野'],
              punchline: '只想多拍就这个，上苍山爬一段，机位在上头' }
          ]
        } },
      { t: 2200, gap_ms: 500, comp: 'tts', highlight: 'A', text: '这三条我最喜欢第一条，就沿着洱海慢慢骑，骑累了找个湖边小摊坐下歇会儿，真不用赶。', pace: 'mid' },
      { t: 2700, gap_ms: 420, comp: 'tts', highlight: 'B', text: '想往巷子里钻是另一种玩法，白天泡咖啡馆晒太阳，晚上人民路热闹，能逛挺晚。', pace: 'mid' },
      { t: 3100, gap_ms: 420, comp: 'tts', highlight: 'C', text: '想多拍点就上苍山，运气好碰上云海，视野很开。你挑哪个？', pace: 'mid' },

      /* ===== ⑦ 三选一：用户选 A → 选择即确认，不问「要不要过一遍」 ===== */
      { t: 0, gap_ms: 800, comp: 'user_query', text: '第一个吧。' },
      { t: 300, gap_ms: 300, comp: 'agent_step', internal: true, label: 'PICK · 选 A → 直出日程',
        decision: '选中 A 洱海骑行慢线，写入 history 当 compose_trip 种子。不问「要不要过一遍」——选择本身就是确认，直接出日程。',
        fields: ['picked:A', 'no确认追问', '→compose_trip'] },

      /* ===== ⑧ 出日程：TravelView 三天横滑；第一段口播带过渡接上选中方案 ===== */
      { t: 0, gap_ms: 300, comp: 'agent_step', internal: true, label: 'PLANNER · 出三天横滑',
        decision: '按 A 排：环洱海当主线。三天每天一张日程卡横滑，逐天讲靠 highlight 聚焦。Day2 环洱海重头(node ★)。',
        fields: ['TravelView·横滑', '每天一张', 'card_id:dali_plan'] },
      { t: 300, gap_ms: 1200, comp: 'TravelView', card_id: 'dali_plan', visual_state: 'active',
        content: { title: '洱海骑行慢线 · 大理 · 3 天', cards: days() } },
      { t: 1500, gap_ms: 500, comp: 'tts', text: '行，你选了洱海那条，那我就按这个排，把环湖的路顺着走，先近后远不绕回头路。', pace: 'mid' },

      /* ===== ⑨ 逐天讲：概括一句 + 王牌段(Day2 日落)给具体心动画面 ===== */
      { t: 1900, gap_ms: 500, comp: 'tts', highlight: 'dali_d1', text: '头天到得晚，就在古城里松松，人民路顺着逛，晚上来碗热饵丝，啥也不赶。', pace: 'mid' },
      { t: 2300, gap_ms: 500, comp: 'tts', text: '三天大致就这调子，头天落地松松，中间环洱海是重头，最后喜洲逛逛赶飞机，都不累。傍晚那段最值，我单说。左右划能看每天。', pace: 'mid' },
      { t: 0, gap_ms: 900, comp: 'tts', highlight: 'dali_d2', text: '这天你一个人骑车绕洱海，想停哪就停哪。最值的是傍晚，骑到龙龛刚好太阳往湖里落，整片湖面金晃晃的，晃得眼睛疼也舍不得眨。坐下看它一点点沉下去，那会儿特别安静。', pace: 'mid' },

      /* ===== ⑩ 不满意改：用户嫌 Day3 喜洲去过了 → 局部改 Day3，覆盖重发；只讲改了啥不复述全程 ===== */
      { t: 0, gap_ms: 900, comp: 'user_query', text: '最后一天喜洲我去过了，换个别的呗。' },
      { t: 300, gap_ms: 300, comp: 'agent_step', internal: true, label: 'REVISE · 只改 Day3',
        decision: '只动 Day3（喜洲→古城没逛够的慢收尾），Day1/Day2 不动；同 card_id dali_plan 覆盖重发，不重出方案、不复述全程。',
        fields: ['改:Day3', 'Day1/2不动', 'card_id:dali_plan 覆盖'] },
      { t: 600, gap_ms: 1000, comp: 'TravelView', card_id: 'dali_plan', visual_state: 'active',
        content: { title: '洱海骑行慢线 · 大理 · 3 天', cards: daysRevised() } },
      { t: 1600, gap_ms: 500, comp: 'tts', highlight: 'dali_d3', text: '成，那最后一天不去喜洲了，就在古城把头天没逛到的巷子补上，中午找个院子吃顿好的，午后慢慢去机场。前两天不动。', pace: 'mid' },

      /* ===== ⑪⑫⑬ 收尾：查日程冲突 → 排日历(ListCard) + 天气提醒；不算预算/不订房/不下单 ===== */
      { t: 0, gap_ms: 900, comp: 'user_query', text: '可以，帮我添加到日程里吧。', travel_back: true },
      { t: 300, gap_ms: 300, comp: 'agent_step', internal: true, label: 'SETTLE · 查日程+天气',
        decision: '查天气+查日程；后天上午有冲突→主动提示挪到中午(基于真日历)。客栈只搜口碑给入口，不报房价、不下单。',
        fields: ['查日程冲突', '查天气', 'no房价/no下单'] },
      { t: 600, gap_ms: 400, comp: 'toast', text: '查询中', state: 'reading', dismiss_on: 'card' },
      { t: 1000, gap_ms: 500, comp: 'tts', text: '等下，你后天上午有个约，出发我给你挪到中午，行不？', pace: 'mid' },
      { t: 0, gap_ms: 700, comp: 'user_query', text: '行。' },
      { t: 300, gap_ms: 400, comp: 'toast', text: '已加进日程', state: 'done', dismiss_on: 'card' },
      { t: 700, gap_ms: 900, comp: 'ListCard', card_id: 'dali_schedule', visual_state: 'done',
        content: {
          source_tool_name: 'list_events',
          title: '已加进日程',
          rows: [
            { id: 'meet_moved', title: '部门同步会（挪中午）', sub: '原在上午 · 给出发让路', lead: '12:00 开，错开出发',
              raw_start: '2026-06-08T12:00:00+08:00', raw_end: '2026-06-08T12:30:00+08:00', event_date: '6/8', event_start_sort: 720 },
            { id: 'd1', title: '大理 Day1 · 古城热身', sub: '午后到 · 古城慢逛吃饵丝', lead: '下午到，先松松',
              raw_start: '2026-06-08T14:30:00+08:00', raw_end: '2026-06-08T21:00:00+08:00', event_date: '6/8', event_start_sort: 870 },
            { id: 'd2', title: '大理 Day2 · 环洱海看日落', sub: '骑行环湖 · 傍晚龙龛日落', lead: '傍晚龙龛看落日',
              raw_start: '2026-06-09T09:30:00+08:00', raw_end: '2026-06-09T19:30:00+08:00', event_date: '6/9', event_start_sort: 570 },
            { id: 'd3', title: '大理 Day3 · 古城慢收尾', sub: '古城补逛 · 午后赶飞机', lead: '午后从容赶飞机',
              raw_start: '2026-06-10T09:30:00+08:00', raw_end: '2026-06-10T15:00:00+08:00', event_date: '6/10', event_start_sort: 570 }
          ],
          footer: '<span class="lbl">日程</span> 三天已排进日历，按天左右滑'
        } },
      { t: 1600, gap_ms: 500, comp: 'tts', text: '都给你排进日程了，照着走就成。对了，看日落那天傍晚洱海边风大，带件外套，别光顾着拍把自己冻着。', pace: 'mid' }
    ],
    annotations: []
  };
})(window);
