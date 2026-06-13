/* Dali · 3 days · solo —— loona-travel-flow benchmark example (13-node flow, EN mirror)
   English mirror of travel_dali_3d_solo.js. case key=travel_dali_3d_solo_en, doesn't clash with the CN case.
   三处新设计（验收标准）与 CN 版一一对应：
     ① 澄清 1→3 轮：每轮一张 ClarifyCard + 一段口播 QUESTION。
        轮1 几人/几天/出发日期；轮2 预算档(只搜参考不算总账)+会不会骑车；轮3 必去/节奏 + 沉淀前两轮进 confirmed。
     ② 方案三选一：InspoFlow 正好 3 张，正好 1 张 rec=true 主推（A 洱海骑行慢线[主推] / B 古城文艺 / C 苍山出片）；
        主推 punchline 带「这条我更推」个人倾向 + 一个立刻想去的具体理由；另两张各一句带过。
     ③ 选完直出规划：不再问「要不要过一遍」；规划第一段口播带 1-2 句过渡接上选中方案。
   收尾：排日历(ListCard) + 天气提醒；全程不算预算/不订房/不下单。
   出发日期：6/8 下午到（到达日 light）→ 6/8-6/10 三天。
   口播：英文版要像真人朋友说话，不是 AI 念稿——短句、口语、有个人倾向。
   照片/资源路径沿用同款 assets/travel/*.jpg。 */
(function (g) {
  g.LOONA_CASES = g.LOONA_CASES || {};

  /* 三天日程（各天一张时间轴日程卡）。
     单天完整天铺满 上午/中午/下午/晚上 四档；到达日(Day1 下午到)按到达时段铺。
     node 字段：time/place/note + 衔接 transport_to_next/distance_to_next/duration_to_next/highlight/star。
     长度守上限：label≤18、place≤14、note≤42、reminder≤22。 */
  var DALI_DAYS = [
    {
      id: 'dali_d1', day: 'Day1', place: 'Old Town warm-up', tag: 'Walk', thumb: 'assets/travel/dl_gucheng.jpg',
      label: 'Day 1 · Old Town', pace: 'light', photo: 'assets/travel/dl_gucheng.jpg',
      theme: 'Old Town warm-up', transport: 'Walk', total: 'All day in the Old Town',
      reminder: 'Land, ease in, rush nothing',
      nodes: [
        { time: 'Afternoon', place: 'Arrive · Old Town', note: 'Land midday, ease in, no rushing today',
          transport_to_next: 'walk', distance_to_next: '5-min walk' },
        { time: 'Afternoon', place: 'Renmin Road', note: 'Wander the old street, duck into whatever looks good',
          transport_to_next: 'walk', distance_to_next: 'Same street' },
        { time: 'Evening', place: 'Erkuai noodles', note: 'Hot erkuai noodles with grilled rushan, that\'s a wrap' }
      ],
      footer: 'All in the Old Town, on foot, half a beat slow'
    },
    {
      id: 'dali_d2', day: 'Day2', place: 'Erhai · sunset', tag: '★ Big one', thumb: 'assets/travel/dl_erhai.jpg',
      label: 'Day 2 · Erhai ride', pace: 'normal', photo: 'assets/travel/dl_erhai.jpg',
      theme: 'Erhai bike loop', transport: 'Bike', total: 'About 25k total',
      reminder: 'Lakeside gets windy at dusk, bring a jacket',
      nodes: [
        { time: 'Morning', place: 'Caicun dock', note: 'Grab a bike, head out along the west shore road',
          transport_to_next: 'bike', distance_to_next: 'ride 8k', duration_to_next: 'about 40 min' },
        { time: 'Midday', place: 'Lakeside trail', note: 'Hug the water, stop wherever, grab a bite by the lake',
          transport_to_next: 'bike', distance_to_next: 'ride 12k', duration_to_next: 'about an hour' },
        { time: 'Afternoon', place: 'Lixiangbang', note: 'Cluster of white houses, shoot at your own pace',
          transport_to_next: 'bike', distance_to_next: 'ride 5k', duration_to_next: 'about 25 min' },
        { time: 'Evening', place: 'Longkan dock', note: 'Sun dips and the whole lake turns gold, sit and watch it sink', highlight: true, star: true }
      ],
      footer: 'Loop the lake, end at Longkan for sunset'
    },
    {
      id: 'dali_d3', day: 'Day3', place: 'Xizhou · head out', tag: 'Wrap', thumb: 'assets/travel/dl_xizhou.jpg',
      label: 'Day 3 · Xizhou · home', pace: 'normal', photo: 'assets/travel/dl_xizhou.jpg',
      theme: 'Xizhou · head out', transport: 'Bus / coach', total: 'Afternoon flight lines up nicely',
      reminder: 'Eat the cake on the go, leave buffer for the flight',
      nodes: [
        { time: 'Morning', place: 'Town → Xizhou', note: 'Take the bus, watch the fields roll by',
          transport_to_next: 'bus', distance_to_next: 'about 40 min' },
        { time: 'Midday', place: 'Xizhou town', note: 'Old white-walled town, wander and shoot by the rice fields',
          transport_to_next: 'walk', distance_to_next: 'In town' },
        { time: 'Afternoon', place: 'Xizhou → airport', note: 'Grab a hot Xizhou cake to eat on the way, then coach to the airport' }
      ],
      footer: 'Wrap up in Xizhou, catch the afternoon flight easy'
    }
  ];

  /* 节点10「不满意改」用：用户嫌 Day3 喜洲去过了，换成古城没逛够的慢收尾。
     同 card_id 'dali_plan' 覆盖重发，靠 pace/标题体现改过，不贴「✓已调整」表功标签。 */
  var DALI_D3_ALT = {
    id: 'dali_d3', day: 'Day3', place: 'Slow Old Town', tag: 'Wrap', thumb: 'assets/travel/dl_gucheng.jpg',
    label: 'Day 3 · slow Old Town', pace: 'light', photo: 'assets/travel/dl_gucheng.jpg',
    theme: 'Slow Old Town', transport: 'Walk', total: 'Easy afternoon flight',
    reminder: 'Leave when it\'s time, keep flight buffer',
    nodes: [
      { time: 'Morning', place: 'Lanes you missed', note: 'Hit the few lanes you didn\'t get to day one, take it slow',
        transport_to_next: 'walk', distance_to_next: 'In town' },
      { time: 'Midday', place: 'Courtyard spot', note: 'Find a courtyard place, sit down for a proper local meal' },
      { time: 'Afternoon', place: 'Town → airport', note: 'Coach to the airport, nap on the way' }
    ],
    footer: 'Skip Xizhou, finish the Old Town you missed, even chiller'
  };

  function days() { return [DALI_DAYS[0], DALI_DAYS[1], DALI_DAYS[2]]; }
  function daysRevised() { return [DALI_DAYS[0], DALI_DAYS[1], DALI_D3_ALT]; }

  g.LOONA_CASES['travel_dali_3d_solo_en'] = {
    task_id: 'travel_dali_3d_solo_en', title: 'Dali 3 days · solo (quiet · loves photos) · 3-round clarify + pick one of three', scene: 'travel', default_skin: 'glass',
    decision_record: { request_type: 'task', primary_need: '排大理三天', granularity: 'by_segment', evidence_level: 'E1', action_risk: 'R0', output_mode: 'document', tool_plan: 'query', confirmation_required: false },
    events: [
      /* ===== ① 起手：开放求建议 ===== */
      { t: 0, gap_ms: 0, comp: 'user_query', text: 'Thinking about Dali for a few days soon — got any ideas?' },
      { t: 250, gap_ms: 300, comp: 'agent_step', internal: true, label: 'ROUTER · 接需求',
        decision: 'travel=NEW → planner。已知目的地=大理；缺人数/天数/日期/预算/骑车/必去/节奏。进 3 轮澄清：轮1 人数天数日期。',
        fields: ['scene:travel', '缺:人数/天数/日期', 'clarify=3轮'] },

      /* ===== ② 澄清轮1：几人 / 几天 / 出发日期 ===== */
      { t: 600, gap_ms: 500, comp: 'agent_step', internal: true, label: 'CLARIFY·轮1 · 人数天数日期',
        decision: 'Mode C / QUESTION。问几人几天 + 出发日期(日期定排期和天气)。confirmed=大理；assumed=短途/这阵子走。',
        fields: ['ClarifyCard·R1', 'card_id:clarify_dali_r1', '问:人数/天数/日期'] },
      { t: 1000, gap_ms: 800, comp: 'ClarifyCard', card_id: 'clarify_dali_r1', wait_for_user: true,
        tts: { text: 'Sweet, I know Dali well. How many of you, how many days? And roughly when — I\'ll peek at the weather for those days.', pace: 'mid' },
        content: {
          title: 'When are you going',
          understand: {
            known: ['Dali'],
            memory: ['Likes it quiet', 'Loves shooting photos', 'Hates crowds']
          }
        } },
      { t: 0, gap_ms: 800, comp: 'user_query', text: 'Just me, 3 days, leaving the day after tomorrow.' },

      /* ===== ③ 澄清轮2：预算档(只搜参考不算总账) + 会不会骑车 ===== */
      { t: 300, gap_ms: 400, comp: 'agent_step', internal: true, label: 'CLARIFY·轮2 · 预算+骑车',
        decision: 'Mode C / QUESTION。预算只定搜索档位、不算总账；问会不会骑车(大理主推=环洱海骑行，不会骑方案就崩)。',
        fields: ['ClarifyCard·R2', 'card_id:clarify_dali_r2', '问:预算档/骑车', 'no总账'] },
      { t: 600, gap_ms: 800, comp: 'ClarifyCard', card_id: 'clarify_dali_r2', wait_for_user: true,
        tts: { text: "What's your budget, roughly? Just so I look at the right kind of stays and food — I'm not tallying up a bill. Oh, and can you ride a bike?", pace: 'mid' },
        content: {
          title: 'Budget and biking',
          understand: {
            known: ['Solo', 'Dali', '3 days', 'leaving in 2 days'],
            memory: ['Wants a place with a courtyard', 'Eats at local spots']
          }
        } },
      { t: 0, gap_ms: 800, comp: 'user_query', text: 'Mid-range is fine, and yeah I can ride.' },

      /* ===== ④ 澄清轮3：必去 / 节奏 + 沉淀前两轮进 confirmed ===== */
      { t: 300, gap_ms: 400, comp: 'agent_step', internal: true, label: 'CLARIFY·轮3 · 必去+节奏(收口)',
        decision: 'Mode C / QUESTION。前两轮答的全沉淀进 known；只剩必去/节奏影响方案。答完即收口去搜索，不凑轮数。',
        fields: ['ClarifyCard·R3', 'card_id:clarify_dali_r3', '问:必去/节奏', 'known沉淀齐'] },
      { t: 600, gap_ms: 800, comp: 'ClarifyCard', card_id: 'clarify_dali_r3', wait_for_user: true,
        tts: { text: 'Cool — 3 days, solo, mid-range, you can ride. Anything you have to see? And do you want it packed or chill?', pace: 'mid' },
        content: {
          title: 'Must-sees and pace',
          understand: {
            known: ['Solo', 'Dali', '3 days', 'leaving in 2 days', 'mid-range', 'can ride'],
            memory: ['Erhai ride as the spine', 'Loves photos']
          }
        } },
      { t: 0, gap_ms: 800, comp: 'user_query', text: 'Nothing specific, you pick. Keep it chill, don\'t cram it.' },
      { t: 300, gap_ms: 300, comp: 'agent_step', internal: true, label: 'PLANNER · 完备 → 搜索',
        decision: '核心输入齐：一个人/3天/后天走/中档/会骑车/节奏松/必去=授权挑+爱拍(记忆)。进搜索→出 3 方案。', fields: ['完备', '去搜索', '3方案'] },

      /* ===== ⑤⑥ 搜索 + 方案生成：InspoFlow 三张等宽大图，A 主推 rec★ =====
         echo 只共情(不评方案不导购)；A 主推 punchline 带「这条我更推」+ 一个立刻想去的具体理由；B/C 各一句带过、不剧透日落。 */
      { t: 600, gap_ms: 400, comp: 'toast', text: 'Searching', state: 'searching', dismiss_on: 'card' },
      { t: 1000, gap_ms: 1200, comp: 'InspoFlow', card_id: 'dali_plans', visual_state: 'active',
        content: {
          echo: "The big three in Dali are Erhai, the Old Town and Cangshan — biking the lake, drifting the lanes, going up for the cloud sea. Quiet and into photos like you, here's three ways to do it",
          cards: [
            { id: 'A', rec: true, title: 'Erhai slow ride', photo: 'assets/travel/dl_erhai.jpg',
              tags: ['Bike', 'Slow', 'Photos'],
              punchline: 'This is the one I\'d go with — you only get that view by riding the whole loop, and the water\'s clearest this season' },
            { id: 'B', title: 'Old Town arty', photo: 'assets/travel/dl_gucheng.jpg',
              tags: ['Lanes', 'Arty', 'Eat & wander'],
              punchline: 'Want it safe and easy? This one — tons of lanes, grab a bite whenever you get hungry' },
            { id: 'C', title: 'Cangshan shots', photo: 'assets/travel/dl_cangshan.jpg',
              tags: ['Climb', 'Photos', 'Views'],
              punchline: 'Just here to shoot? This one — hike up Cangshan, the angles are up top' }
          ]
        } },
      { t: 2200, gap_ms: 500, comp: 'tts', highlight: 'A', text: 'Of the three my favorite\'s the first — just ride along Erhai nice and slow, and when you\'re tired pull over at some little lakeside stall. No rush at all.', pace: 'mid' },
      { t: 2700, gap_ms: 420, comp: 'tts', highlight: 'B', text: "The lanes are a whole other vibe — coffee in the sun by day, Renmin Road buzzing at night, you can wander pretty late.", pace: 'mid' },
      { t: 3100, gap_ms: 420, comp: 'tts', highlight: 'C', text: 'Want more shots? Go up Cangshan — get lucky with a cloud sea and the view\'s wide open. Which one do you want?', pace: 'mid' },

      /* ===== ⑦ 三选一：用户选 A → 选择即确认，不问「要不要过一遍」 ===== */
      { t: 0, gap_ms: 800, comp: 'user_query', text: 'The first one.' },
      { t: 300, gap_ms: 300, comp: 'agent_step', internal: true, label: 'PICK · 选 A → 直出日程',
        decision: '选中 A 洱海骑行慢线，写入 history 当 compose_trip 种子。不问「要不要过一遍」——选择本身就是确认，直接出日程。',
        fields: ['picked:A', 'no确认追问', '→compose_trip'] },

      /* ===== ⑧ 出日程：TravelView 三天横滑；第一段口播带过渡接上选中方案 ===== */
      { t: 0, gap_ms: 300, comp: 'agent_step', internal: true, label: 'PLANNER · 出三天横滑',
        decision: '按 A 排：环洱海当主线。三天每天一张日程卡横滑，逐天讲靠 highlight 聚焦。Day2 环洱海重头(node ★)。',
        fields: ['TravelView·横滑', '每天一张', 'card_id:dali_plan'] },
      { t: 300, gap_ms: 1200, comp: 'TravelView', card_id: 'dali_plan', visual_state: 'active',
        content: { title: 'Erhai slow ride · Dali · 3 days', cards: days() } },
      { t: 1500, gap_ms: 500, comp: 'tts', text: 'Alright, you went with the Erhai one, so I\'ll build around that — follow the loop, near stuff first then far, no doubling back.', pace: 'mid' },

      /* ===== ⑨ 逐天讲：概括一句 + 王牌段(Day2 日落)给具体心动画面 ===== */
      { t: 1900, gap_ms: 500, comp: 'tts', highlight: 'dali_d1', text: 'You land late day one, so just ease in around the Old Town, wander Renmin Road, grab a hot bowl of erkuai at night. Rush nothing.', pace: 'mid' },
      { t: 2300, gap_ms: 500, comp: 'tts', text: 'That\'s the whole vibe — land easy day one, the lake loop\'s the big one in the middle, Xizhou and your flight on the last. Nothing tiring. The dusk bit\'s the best part, I\'ll get to that. Swipe to see each day.', pace: 'mid' },
      { t: 0, gap_ms: 900, comp: 'tts', highlight: 'dali_d2', text: 'This day you ride around Erhai solo, stop wherever you feel like. The best bit\'s at dusk — you hit Longkan right as the sun drops into the lake, and the whole surface goes gold, so bright it stings but you won\'t want to blink. Sit down and watch it sink, inch by inch. It gets really quiet.', pace: 'mid' },

      /* ===== ⑩ 不满意改：用户嫌 Day3 喜洲去过了 → 局部改 Day3，覆盖重发；只讲改了啥不复述全程 ===== */
      { t: 0, gap_ms: 900, comp: 'user_query', text: 'I\'ve been to Xizhou — swap the last day for something else.' },
      { t: 300, gap_ms: 300, comp: 'agent_step', internal: true, label: 'REVISE · 只改 Day3',
        decision: '只动 Day3（喜洲→古城没逛够的慢收尾），Day1/Day2 不动；同 card_id dali_plan 覆盖重发，不重出方案、不复述全程。',
        fields: ['改:Day3', 'Day1/2不动', 'card_id:dali_plan 覆盖'] },
      { t: 600, gap_ms: 1000, comp: 'TravelView', card_id: 'dali_plan', visual_state: 'active',
        content: { title: 'Erhai slow ride · Dali · 3 days', cards: daysRevised() } },
      { t: 1600, gap_ms: 500, comp: 'tts', highlight: 'dali_d3', text: 'Done — last day skips Xizhou, you finish the Old Town lanes you missed, sit down somewhere nice for lunch, then drift to the airport. First two days stay put.', pace: 'mid' },

      /* ===== ⑪⑫⑬ 收尾：查日程冲突 → 排日历(ListCard) + 天气提醒；不算预算/不订房/不下单 ===== */
      { t: 0, gap_ms: 900, comp: 'user_query', text: 'Works — add it to my calendar.', travel_back: true },
      { t: 300, gap_ms: 300, comp: 'agent_step', internal: true, label: 'SETTLE · 查日程+天气',
        decision: '查天气+查日程；后天上午有冲突→主动提示挪到中午(基于真日历)。客栈只搜口碑给入口，不报房价、不下单。',
        fields: ['查日程冲突', '查天气', 'no房价/no下单'] },
      { t: 600, gap_ms: 400, comp: 'toast', text: 'Checking', state: 'reading', dismiss_on: 'card' },
      { t: 1000, gap_ms: 500, comp: 'tts', text: 'Hold on — you\'ve got something the morning you leave. I\'ll push your departure to midday, that good?', pace: 'mid' },
      { t: 0, gap_ms: 700, comp: 'user_query', text: 'Yeah.' },
      { t: 300, gap_ms: 400, comp: 'toast', text: 'Added to calendar', state: 'done', dismiss_on: 'card' },
      { t: 700, gap_ms: 900, comp: 'ListCard', card_id: 'dali_schedule', visual_state: 'done',
        content: {
          source_tool_name: 'list_events',
          title: 'Added to calendar',
          rows: [
            { id: 'meet_moved', title: 'Team sync (moved to noon)', sub: 'Was morning · making room to leave', lead: 'Starts 12:00, clear of departure',
              raw_start: '2026-06-08T12:00:00+08:00', raw_end: '2026-06-08T12:30:00+08:00', event_date: '6/8', event_start_sort: 720 },
            { id: 'd1', title: 'Dali Day1 · Old Town', sub: 'Land midday · wander, erkuai noodles', lead: 'Land afternoon, ease in',
              raw_start: '2026-06-08T14:30:00+08:00', raw_end: '2026-06-08T21:00:00+08:00', event_date: '6/8', event_start_sort: 870 },
            { id: 'd2', title: 'Dali Day2 · Erhai sunset', sub: 'Ride the loop · Longkan sunset', lead: 'Sunset at Longkan',
              raw_start: '2026-06-09T09:30:00+08:00', raw_end: '2026-06-09T19:30:00+08:00', event_date: '6/9', event_start_sort: 570 },
            { id: 'd3', title: 'Dali Day3 · slow Old Town', sub: 'Finish the lanes · afternoon flight', lead: 'Easy afternoon flight',
              raw_start: '2026-06-10T09:30:00+08:00', raw_end: '2026-06-10T15:00:00+08:00', event_date: '6/10', event_start_sort: 570 }
          ],
          footer: '<span class="lbl">Calendar</span> Three days are in, swipe day to day'
        } },
      { t: 1600, gap_ms: 500, comp: 'tts', text: 'All in your calendar, just follow it. Oh — the sunset day, it gets windy by Erhai at dusk, so bring a jacket. Don\'t get so into shooting you freeze yourself.', pace: 'mid' }
    ],
    annotations: []
  };
})(window);
