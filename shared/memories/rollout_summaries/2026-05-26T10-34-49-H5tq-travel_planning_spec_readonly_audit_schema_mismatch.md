thread_id: 019e63d9-f7bc-7491-97a8-6aeb5991102c
updated_at: 2026-05-26T10:42:39+00:00
rollout_path: C:\Users\QYL\.codex\sessions\2026\05\26\rollout-2026-05-26T18-34-49-019e63d9-f7bc-7491-97a8-6aeb5991102c.jsonl
cwd: \\?\C:\Users\QYL

# Read-only audit of the travel-planning delivery spec found multiple high-severity contract mismatches against the real UI and toolhub code, with the biggest issue being that the doc’s `cards[]` schema does not match the actual `TravelView` / `TravelDayFocus` builders, so the spec was not directly shippable.

Rollout context: The user asked for a strict, skeptical, read-only review of `C:\Users\QYL\Desktop\loona-workbench\旅行规划_交付版_v1.md`, explicitly requested no edits, and required cross-checking against real source files in `js/scenario-forms.js`, `js/components.js`, `cases/travel_chengdu_5d_full.js`, and ToolHub Python code. The requested output format was a one-sentence verdict, a structured issue table with evidence and suggested fixes, and a final “verified OK” section.

## Task 1: Audit the travel planning delivery spec against real UI/tool sources

Outcome: success

Preference signals:
- when the user said “只读、不要修改任何文件” and “挑剔、要怀疑，宁可多报” -> future similar audits should default to read-only skepticism, not implementation planning or optimistic acceptance
- when the user required “给证据” and a structured table with severity/position/problem/fix -> future similar document reviews should produce evidence-anchored, decision-ready findings rather than a loose narrative
- when the user specified “已验证 OK 的点” at the end -> future similar reviews should preserve confirmed-correct items separately so the user does not have to rediscover what already passed
- when the user insisted on comparing the delivery doc against real source-of-truth files -> future similar tasks should start from actual code/tool schemas instead of trusting the prose spec

Key steps:
- Loaded the delivery spec and the real UI builders; confirmed `TravelView` and `TravelDayFocus` do not consume the doc’s top-level `cards[]` shape directly.
- Cross-checked `scenario-forms.js` and `components.js` to map what the actual builders read: `TravelView` expects `sections[]`, `section.label`, `section.badge`, `section.text`; `TravelDayFocus` expects `title`, `badge`, `photo`, `nodes`, `footer`.
- Cross-checked the ToolHub Python sources: `get_weather` returns only current weather (`current.temp_c`, `current.condition`) and rejects multi-city strings; `web_search` returns `results[].image_url` but fallback behavior is different; `get_travel_plan_template` is a canned stub, not a real itinerary engine.
- Checked the travel case file; the runnable case still uses `sections[]/footer/badge/text`, not the new `cards[]/span/card_footer/trip_footer/evidence` contract.
- Read the companion `旅行规划_system_prompt_v1.md` and found it still uses the older `days[]/period/reliability/transport_notes/image_url/markdownArtifact` schema, so the “directly pasteable” prompt bundle is inconsistent with the delivery spec.

Failures and how to do differently:
- The main failure mode in the spec is contract drift: it repeatedly renames data fields (`cards[]`, `trip_footer`, `card_footer`, `summary`, `pace`) without matching the actual component field names.
- The travel section’s split rules are not self-consistent at the boundaries: the prose says 8–14 days should be every 3 days, but the example for 10 days uses every 2 days; this means the same input can lead to conflicting cuts.
- The doc overstates weather capability by implying day-level weather planning from `get_weather`, but the actual tool only provides current conditions.
- The doc should not claim “1:1 对齐组件” unless it also provides a concrete mapping layer or uses the component-native names directly.

Reusable knowledge:
- `js/scenario-forms.js` is the authoritative read path for travel cards in this repo: `TravelView` reads `c.sections`, and `TravelDayFocus` reads `c.title`, `c.badge`, `c.photo`, `c.nodes`, and `c.footer`.
- `js/components.js` confirms the actual low-level row rendering: `lcRow` consumes `lead/title/sub/right/badge`, while `SectionCard` consumes `sections[]` and `ClarifyCard` renders `slots.required/optional` plus options; `source` strings are not automatically displayed by the component.
- `toolhub/server/python/tools/weather.py` is current-weather only; it returns `current.{temp_c, feels_like_c, humidity, condition}` and does not implement forecast output even though `catalog.py` exposes a `days` parameter.
- `toolhub/server/python/tools/travel.py` is a dry-run template stub and explicitly not a booked itinerary tool.
- `toolhub/server/python/tools/search.py` returns `results[].image_url`, but when real search fails, `main.py` can fall back to canned data that is not equivalent to the real search payload.
- The user’s preferred review style for similar document audits is strict, evidence-first, and skeptical, with explicit separation between confirmed-good points and defects.

References:
- [1] `C:\Users\QYL\Desktop\loona-workbench\js\scenario-forms.js:105-163` — `TravelView` uses `c.sections || []`; `TravelDayFocus` uses `c.title`, `c.badge`, `c.photo`, `c.nodes`, and `c.footer`.
- [2] `C:\Users\QYL\Desktop\loona-workbench\js\components.js:369-479` — `lcRow`, `sectionCard`, and `clarifyCard` field expectations; `sectionCard` reads `sections[]`, not `cards[]`.
- [3] `C:\Users\QYL\Desktop\loona-workbench\cases\travel_chengdu_5d_full.js:63-78, 94-102` — runnable travel case still uses `sections[]`, `footer`, `badge`, `text`, and `photo`.
- [4] `C:\Users\QYL\Desktop\toolhub\server\python\tools\weather.py:11-57` — current-only weather payload, multi-city rejection, E2/E0 envelope.
- [5] `C:\Users\QYL\Desktop\toolhub\server\python\tools\search.py:20-89` and `tools/canned.py:13-34` — real web search result shape includes `image_url`, but fallback canned data differs and should not be treated as the real payload.
- [6] `C:\Users\QYL\Desktop\toolhub\server\python\tools\travel.py:1-47` and `catalog.py:135-141` — `get_travel_plan_template` is a canned stub.
- [7] `C:\Users\QYL\Desktop\loona-workbench\旅行规划_system_prompt_v1.md:75-80, 157-176` — still uses `days[]`, `granularity`, `period`, `transport_notes`, `image_url`, `markdownArtifact`, which conflicts with the delivery spec’s new schema.

## Task 2: Capture durable review-style preferences from the rollout

Outcome: success

Preference signals:
- when the user asked for a “严格的技术文档审核员” and demanded “要挑剔、要怀疑，宁可多报” -> future document reviews should err on the side of surfacing extra inconsistencies rather than under-reporting them
- when the user mandated “输出结构化清单” with an explicit table and a final verified-OK section -> future similar responses should preserve structure and evidence density, not just summarize the verdict
- when the user emphasized “只读，不要修改任何文件” -> future similar review tasks should default to inspection-only behavior and avoid any accidental implementation drift

Reusable knowledge:
- The user values direct comparisons against real code and tools more than trusting a doc’s own claims.
- For this repo, travel-planning docs can drift across multiple artifacts (`交付版`, `system_prompt`, and runnable case files); a strong review should check all of them together before concluding the spec is consistent.

References:
- User instruction wording worth reusing verbatim in similar contexts: “只读、不要修改任何文件”, “挑剔、要怀疑，宁可多报”, “已验证 OK 的点”.
- The review produced a ranked list of concrete defects, with the highest-severity items centered on schema/component mismatches and weather/tool capability overclaims.
