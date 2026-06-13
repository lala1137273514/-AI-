/* Chengdu 3 days · two people —— loona-travel-flow English mirror case (v5 full · 39 steps)
   English mirror of travel_chengdu_3d.js: structure / events order / comp types / fields /
   card_id / asset paths / node comments map one-to-one with the CN version; only user-facing
   text is translated to natural English.
   v5 design kept: round1/2 are voice-only (no card), round3 has the single ClarifyCard;
   three options as one InspoFlow (A panda slow line rec★ / B Three Kingdoms / C food-blitz);
   revise touches Day2 only (drop the night skewers, trim to 3 slots · pace light).
   Images use the same workbench assets/travel/cd_*.jpg; null where unsure.
   Length caps: label≤18, place≤14, note≤42, reminder≤22. */
(function (g) {
  g.LOONA_CASES = g.LOONA_CASES || {};

  /* Three-day itinerary (one timeline day-card each). node fields match dali: time/place/note + reminder/highlight/star. */
  var CD_DAYS = [
    {
      id: 'cd_d1', day: 'Day1', place: 'Kuanzhai warm-up', tag: 'arrive·easy', thumb: 'assets/travel/cd_kuanzhai.jpg',
      label: 'Day 1 · Kuanzhai warm-up', pace: 'light', photo: 'assets/travel/cd_kuanzhai.jpg',
      theme: 'Kuanzhai warm-up', transport: 'walk', total: 'Arrive after noon, just chill, no rush',
      reminder: 'Arrive, chill, no rush',
      nodes: [
        { time: 'Afternoon', place: 'Arrive · Kuanzhai', note: 'You land after noon, just chill, no rush' },
        { time: 'Afternoon', place: 'Stroll Kuanzhai', note: 'Old brick courtyards in and out, grab street snacks' },
        { time: 'Evening', place: 'First hotpot', note: 'Red broth bubbling, dip the tripe and duck' }
      ],
      footer: 'Arrive, chill, old-lane stroll, hotpot'
    },
    {
      id: 'cd_d2', day: 'Day2', place: 'Panda + city life', tag: '★ big day', thumb: 'assets/travel/cd_panda.jpg',
      label: 'Day 2 · Panda+city life', pace: 'normal', photo: 'assets/travel/cd_panda.jpg',
      theme: 'Panda+city life', transport: 'taxi / walk', total: 'A day of pandas, food and wandering',
      reminder: 'Pandas early, late = sleeping',
      nodes: [
        { time: 'Morning', place: 'Panda base', note: 'Go early, the pandas hug trees and munch bamboo; late and you only get sleeping fuzzballs', highlight: true, star: true },
        { time: 'Noon', place: 'Sichuan diner', note: 'Mapo tofu, twice-cooked pork, order a few real dishes' },
        { time: 'Afternoon', place: 'Tea at the park', note: 'Sink into a bamboo chair, endless tea, get your ears cleaned' },
        { time: 'Evening', place: 'Jinli + skewers', note: 'Wander under the red lanterns, grab a few skewers' }
      ],
      footer: 'Pandas early, tea in the afternoon, skewers at night'
    },
    {
      id: 'cd_d3', day: 'Day3', place: 'Wuhou · fly home', tag: 'wrap-up', thumb: 'assets/travel/cd_wuhou.jpg',
      label: 'Day 3 · Wuhou·fly home', pace: 'normal', photo: 'assets/travel/cd_wuhou.jpg',
      theme: 'Wuhou · fly home', transport: 'taxi', total: 'Afternoon flight works out fine',
      reminder: 'Snack on the go, leave time',
      nodes: [
        { time: 'Morning', place: 'Wuhou + Jinli', note: 'Walk the red-walled lane, the Three Kingdoms folks come alive' },
        { time: 'Noon', place: 'Chengdu snacks', note: 'A plate of zhong dumplings and a plate of wontons' },
        { time: 'Afternoon', place: 'Catch the flight', note: 'Leave time to cab to the airport, nap on the way' }
      ],
      footer: 'Three Kingdoms walk, some snacks, afternoon flight'
    }
  ];

  /* Revise path: user wants to skip Day2 night Jinli skewers and head back early to rest → trim night skewers to 3 slots, pace light.
     Same card_id 'cd_plan' overwrite-resend; the change shows via pace/title, no "✓ adjusted" brag tag. */
  var CD_D2_ALT = {
    id: 'cd_d2', day: 'Day2', place: 'Panda + tea', tag: '★ big day', thumb: 'assets/travel/cd_panda.jpg',
    label: 'Day 2 · Panda+tea', pace: 'light', photo: 'assets/travel/cd_panda.jpg',
    theme: 'Panda+tea', transport: 'taxi / walk', total: 'Pandas, then tea and rest in the afternoon',
    reminder: 'Pandas early, late = sleeping',
    nodes: [
      { time: 'Morning', place: 'Panda base', note: 'Go early, the pandas hug trees and munch bamboo', highlight: true, star: true },
      { time: 'Noon', place: 'Sichuan diner', note: 'Order a few real dishes and refuel' },
      { time: 'Afternoon', place: 'Tea at the park', note: 'Bamboo chair, tea and ear-cleaning, rest your legs after the pandas' }
    ],
    footer: 'Dropped the night skewers, tea and rest after pandas'
  };

  function days() { return [CD_DAYS[0], CD_DAYS[1], CD_DAYS[2]]; }
  function daysRevised() { return [CD_DAYS[0], CD_D2_ALT, CD_DAYS[2]]; }

  g.LOONA_CASES['travel_chengdu_3d_en'] = {
    task_id: 'travel_chengdu_3d_en', title: 'Chengdu 3d · two people · 3-round clarify + pick-of-three v5', scene: 'travel', default_skin: 'glass',
    decision_record: { request_type: 'task', primary_need: '排成都三天', granularity: 'by_segment', evidence_level: 'E1', action_risk: 'R0', output_mode: 'document', tool_plan: 'query', confirmation_required: false },
    events: [
      /* ===== ① 起手 + 路由 ===== */
      { t: 0, gap_ms: 0, comp: 'user_query', text: 'Help me plan a three-day trip to Chengdu.' },
      { t: 250, gap_ms: 300, comp: 'agent_step', internal: true, label: 'ROUTER · 接需求',
        decision: 'travel=NEW → planner；已知 成都/3天，进 3 轮澄清（轮1/2 纯语音，不出卡）',
        fields: ['scene:travel', '已知:成都/3天', 'clarify=3轮'] },

      /* ===== ② 澄清轮1：纯语音·贴记忆（无卡） ===== */
      { t: 600, gap_ms: 500, comp: 'tts', text: "Sweet, the two of you again? When are you thinking of heading out? I'll check the forecast for those days.", pace: 'mid' },
      { t: 0, gap_ms: 800, comp: 'user_query', text: 'Yeah, two of us, leaving June 12.' },

      /* ===== ③ 澄清轮2：纯语音（无卡） ===== */
      { t: 300, gap_ms: 500, comp: 'tts', text: "What's the budget roughly? Oh, and you two can handle spicy, right?", pace: 'mid' },
      { t: 0, gap_ms: 800, comp: 'user_query', text: "Mid-range is fine, and yeah, the spicier the better." },

      /* ===== ④ 澄清轮3：语音 + 唯一一张 ClarifyCard（已确认→known，我猜→memory） ===== */
      { t: 300, gap_ms: 400, comp: 'agent_step', internal: true, label: 'CLARIFY·轮3 · 汇总确认(收口)',
        decision: '前两轮答的全沉淀进 known；只剩必去/节奏。答完即收口去搜索，不凑轮数。轮1/2 纯语音不出卡。',
        fields: ['ClarifyCard·R3', 'card_id:clarify_cd_r3', '问:必去/节奏'] },
      { t: 600, gap_ms: 800, comp: 'ClarifyCard', card_id: 'clarify_cd_r3', wait_for_user: true,
        tts: { text: "Got it all down. Anywhere you've already got your eye on? I know you hate crowds, so keep it easy and dodge the rush, yeah?", pace: 'mid' },
        content: {
          title: 'Must-sees and pace',
          understand: {
            known: ['Two people', 'Chengdu', '3 days', 'Leave 6-12', 'Mid-range', 'Can do spicy'],
            memory: ['Want to see pandas', 'Local-food focus', 'Hates crowds']
          }
        } },
      { t: 0, gap_ms: 800, comp: 'user_query', text: "Panda base is a must, and keep it easy, not too packed." },

      /* ===== ⑤ 进度 NOTICE → 搜索 → 方案开场 ===== */
      { t: 300, gap_ms: 500, comp: 'tts', notice: true, text: "Cool, sec — lemme pull up some Chengdu options.", pace: 'mid' },
      { t: 0, gap_ms: 300, comp: 'agent_step', internal: true, label: 'SEARCH · 取数',
        decision: '搜索：web_search 馆子/景点 + get_weather（6/12-6/14）',
        fields: ['web_search', 'get_weather'] },
      { t: 300, gap_ms: 400, comp: 'toast', text: 'Searching', state: 'searching', dismiss_on: 'card' },

      /* ===== ⑥ 方案三选一：一个 InspoFlow 三张大图，A 熊猫慢线主推 rec★ =====
         echo 用 mock 第12步开场那句；punchline 用各方案卡的「口播」字段。 */
      { t: 700, gap_ms: 1200, comp: 'InspoFlow', card_id: 'cd_plans', visual_state: 'active',
        content: {
          echo: "Okay, I came up with three different ways to do Chengdu — let me run you through them.",
          cards: [
            { id: 'A', rec: true, title: 'Panda + city slow line', photo: 'assets/travel/cd_panda.jpg',
              tags: ['pandas', 'hotpot', 'easy'],
              punchline: "This is the one I'd go with: three unhurried days, pandas, tea houses, hotpot and skewers back to back, all chill" },
            { id: 'B', title: 'Three Kingdoms line', photo: 'assets/travel/cd_wuhou.jpg',
              tags: ['culture', 'old sites', 'wander'],
              punchline: "Three days through Wuhou Shrine, Du Fu's Cottage and Kuanzhai — go for this one if you're into the history" },
            { id: 'C', title: 'Food blitz', photo: 'assets/travel/cd_jinli.jpg',
              tags: ['hole-in-walls', 'skewers', 'packed'],
              punchline: "Three days of hole-in-the-wall spots, skewers and snacks — grab this if you're here to eat, just expect a packed schedule" }
          ]
        } },
      { t: 1900, gap_ms: 500, comp: 'tts', highlight: 'A', text: "I'd go with the first one. Three easy days, pandas in the morning, tea houses and hotpot the rest. You two want it relaxed, so this fits.", pace: 'mid' },
      { t: 2400, gap_ms: 420, comp: 'tts', highlight: 'B', text: "If you're more into the history, go with the second — three slow days around Wuhou Shrine, Du Fu's Cottage and Kuanzhai, that quiet red-wall, bamboo-shade vibe.", pace: 'mid' },
      { t: 2800, gap_ms: 420, comp: 'tts', highlight: 'C', text: "And if you're just here to eat, the third's all your stuff — three days of hole-in-the-walls, skewers and snacks, just a packed one. Which way you leaning?", pace: 'mid' },

      /* ===== ⑦ 三选一：选 A → 直出日程，不问「要不要过一遍」 ===== */
      { t: 0, gap_ms: 800, comp: 'user_query', text: 'The first one.' },
      { t: 300, gap_ms: 300, comp: 'agent_step', internal: true, label: 'PICK · 选 A → 直出日程',
        decision: 'PICK：选 A → 直出日程，不问「要不要过一遍」',
        fields: ['picked:A', 'no确认追问', '→compose_trip'] },
      { t: 0, gap_ms: 500, comp: 'tts', text: "Nice, that's a great fit for you two — let me lay it out.", pace: 'mid' },

      /* ===== ⑧ 出日程：TravelView 三天横滑 + 逐天讲 ===== */
      { t: 0, gap_ms: 300, comp: 'agent_step', internal: true, label: 'PLANNER · 出三天横滑',
        decision: '按 A 排：熊猫+市井慢线。三天每天一张日程卡横滑，逐天讲靠 highlight 聚焦。Day2 熊猫重头(node ★)。',
        fields: ['TravelView·横滑', '每天一张', 'card_id:cd_plan'] },
      { t: 300, gap_ms: 1200, comp: 'TravelView', card_id: 'cd_plan', visual_state: 'active',
        content: { title: 'Panda + city slow line · Chengdu · 3 days', cards: days() } },
      { t: 1500, gap_ms: 500, comp: 'tts', highlight: 'cd_d1', text: "You land in the afternoon, so just take it easy around Kuanzhai, wander the old brick courtyards, first hotpot at night, nothing rushed.", pace: 'mid' },
      { t: 1900, gap_ms: 500, comp: 'tts', highlight: 'cd_d2', text: "Get up early this day, the pandas are liveliest in the morning, go late and they're all asleep. After that we head back to town, tea and ear-cleaning at the park in the afternoon, super relaxing. Then hotpot at night, I found you the most authentic spot. I know you can do spicy, so I picked a real fiery one.", pace: 'mid' },
      { t: 0, gap_ms: 500, comp: 'tts', highlight: 'cd_d3', text: "Last day, swing by Wuhou Shrine, see the old Three Kingdoms sites, some snacks at noon, then off to the airport, no rush.", pace: 'mid' },
      { t: 400, gap_ms: 500, comp: 'tts', text: "That's the whole plan. Take a look, tell me anytime if you want changes.", pace: 'mid' },

      /* ===== ⑨ 不满意改：砍 Day2 晚上串串收成 3 档 → 局部改 Day2，覆盖重发 ===== */
      { t: 0, gap_ms: 900, comp: 'user_query', text: "Drop the Jinli skewers on night two, I'd rather head back early to rest after the pandas." },
      { t: 300, gap_ms: 300, comp: 'agent_step', internal: true, label: 'REVISE · 只改 Day2',
        decision: 'REVISE：只改 Day2（砍晚上串串收成 3 档），Day1/Day3 不动，同卡覆盖重发',
        fields: ['改:Day2', 'Day1/3不动', 'card_id:cd_plan 覆盖'] },
      { t: 600, gap_ms: 1000, comp: 'TravelView', card_id: 'cd_plan', visual_state: 'active',
        content: { title: 'Panda + city slow line · Chengdu · 3 days', cards: daysRevised() } },
      { t: 1600, gap_ms: 500, comp: 'tts', highlight: 'cd_d2', text: "Done, dropped the night-two skewers; after the pandas and afternoon tea you head back to rest. Anything else to change? Or want me to add it to your calendar?", pace: 'mid' },

      /* ===== ⑩ 收尾：查日程冲突 → 排日历(ListCard) + 天气提醒；不算账/不订房 ===== */
      { t: 0, gap_ms: 900, comp: 'user_query', text: "Looks good, go ahead and add it to my calendar.", travel_back: true },
      { t: 300, gap_ms: 400, comp: 'tts', notice: true, text: "Sure, let me check your calendar.", pace: 'mid' },
      { t: 0, gap_ms: 300, comp: 'agent_step', internal: true, label: 'SETTLE · 查日程+天气',
        decision: 'SETTLE：查日程冲突 + 查天气；不算账/不订房',
        fields: ['查日程冲突', '查天气', 'no算账/no订房'] },
      { t: 300, gap_ms: 400, comp: 'toast', text: 'Checking', state: 'reading', dismiss_on: 'card' },
      { t: 700, gap_ms: 500, comp: 'tts', text: "Hold up — you've got a meeting the morning of June 12. I'll push it to noon so you can take off, cool?", pace: 'mid' },
      { t: 0, gap_ms: 700, comp: 'user_query', text: 'Sure.' },
      { t: 300, gap_ms: 400, comp: 'toast', text: 'Added to calendar', state: 'done', dismiss_on: 'card' },
      { t: 700, gap_ms: 900, comp: 'ListCard', card_id: 'cd_schedule', visual_state: 'done',
        content: {
          source_tool_name: 'list_events',
          title: 'Added to calendar',
          rows: [
            { id: 'meet_moved', title: 'Team sync (moved to noon)', sub: 'Was morning · cleared for departure', lead: 'cleared for departure',
              raw_start: '2026-06-12T12:00:00+08:00', raw_end: '2026-06-12T12:30:00+08:00', event_date: '6/12', event_start_sort: 720 },
            { id: 'd1', title: 'Chengdu Day1 · Kuanzhai', sub: 'Arrive PM · old-lane stroll, hotpot', lead: 'Arrive PM, old-lane stroll, hotpot',
              raw_start: '2026-06-12T14:00:00+08:00', raw_end: '2026-06-12T21:00:00+08:00', event_date: '6/12', event_start_sort: 840 },
            { id: 'd2', title: 'Chengdu Day2 · Panda+tea', sub: 'Pandas early · tea in afternoon', lead: 'Pandas early, tea in afternoon',
              raw_start: '2026-06-13T08:30:00+08:00', raw_end: '2026-06-13T17:00:00+08:00', event_date: '6/13', event_start_sort: 510 },
            { id: 'd3', title: 'Chengdu Day3 · Wuhou wrap-up', sub: 'Three Kingdoms walk · afternoon flight', lead: 'afternoon flight',
              raw_start: '2026-06-14T09:00:00+08:00', raw_end: '2026-06-14T15:00:00+08:00', event_date: '6/14', event_start_sort: 540 }
          ],
          footer: '<span class="lbl">Calendar</span> All three days are in, swipe left/right by day'
        } },
      { t: 1600, gap_ms: 500, comp: 'tts', text: "All set on your calendar. Oh, Chengdu's muggy in June and gets afternoon showers, so toss an umbrella in your bag, don't get soaked. Have a blast!", pace: 'mid' }
    ],
    annotations: []
  };
})(window);
