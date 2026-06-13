# Retrospective Template

Generate one analytical Markdown review per day.

## Required Sections

```markdown
# 工作复盘 - YYYY-MM-DD

## 今日概览

## 推进时间线

## 当前现状

## 下一步待办

## 今日思考

## 信息缺口（如有）
```

## Preferred Styling

- `今日概览` should use one concise callout block when possible.
- `推进时间线` should use timestamped bullets, preferably with exact `HH:MM` values.
- `当前现状` should prefer a short stack of status cards instead of a Markdown table.
- Each status card can use a small status emoji plus a soft background color, for example `🚧 / 🕒 / 🔄 / 🚀 / ✅`.
- The `当前现状` heading may use a light heading color to improve scanability, but the section should stay simple and stable.
- `下一步待办` should remain a checklist.
- Use rich Lark-flavored Markdown to improve readability, but avoid decorative formatting that makes reruns fragile.

## Core Goal

This review is not a chat recap. It should help the user quickly understand:

- what actually moved today
- where the work stands at the end of the day
- what should happen next
- what judgment or learning is worth keeping

## Analysis Rules

- Use `analysis_payload` as the primary model-facing input when it is available.
- Treat raw collected `items` as backup context, not as the primary synthesis source.
- Base the review on the day's full collected inputs, not on isolated messages.
- Every section should look across the day's full collected inputs instead of analyzing only a narrow local slice.
- Rewrite and synthesize; do not dump the original transcript as bullets.
- Use the model to rewrite and compress the day's records into a cleaner narrative instead of preserving the raw wording.
- In multimodal days, treat image evidence in `analysis_payload` as first-class evidence rather than requiring OCR text first.
- Group content by work theme and current status, not by raw chat order.
- Prefer truthful synthesis over impressive-sounding overreach.
- Infer conclusions and next steps only when the evidence supports them.
- If evidence is weak, say `暂未明确` instead of inventing certainty.
- If content is sparse, output a shorter review rather than padding with generic language.

## Section Guidance

- `今日概览`
  - Use 2-4 sentences to summarize the day's main thread, the most material progress, and a short state judgment.
  - Make it readable in under a minute.
- `推进时间线`
  - Keep 3-6 key nodes that explain how the day moved forward.
  - Each item should capture a meaningful step, not a raw chat snippet.
  - Include exact timestamps when available; otherwise use coarse markers such as `上午` or `会后`.
  - This section is about process, not end-state.
- `当前现状`
  - Freeze the state as of the end of the day.
  - Prioritize confirmed facts, emerging conclusions, unresolved questions, blockers, and risks.
  - Prefer short item labels, a clear status label, and one compact “latest record” hint.
  - If Markdown tables are unstable in the current publishing path, use one callout card per item instead.
  - Prefer lightweight sub-groups such as `事项状态`, `知识沉淀`, `资源与线索`, `阶段判断`, and `待确认项` when the day's inputs support them.
  - This section must not repeat timeline bullets line by line.
  - It should usually avoid timestamps in the main sentence and focus on where the work currently stands.
  - It may group multiple same-theme records into one current-state item when that reduces duplication.
- `下一步待办`
  - Write concrete, executable actions that grow naturally from today's inputs.
  - Build this section from the full-day candidate action pool: explicit next steps, blocker follow-ups, testing closure, unresolved in-progress work, and resource follow-ups.
  - Avoid vague phrases such as `继续跟进` or `持续推进`.
- `今日思考`
  - Keep 1-3 judgments, insights, or methods worth reusing later.
  - Derive this section from the full-day pattern: progress rhythm, evidence quality, testing closure, and how plans turned into results.
  - If there is no solid insight, say less rather than force a pseudo-methodology.
- `信息缺口（如有）`
  - Mention partial parsing failures, missing decision basis, unclear ownership, or weak evidence.
  - Keep this section short and honest; it should not overtake the main review.

## Output Rules

- Rebuild the full document from the day's complete chat history each run.
- Overwrite the same day's document on rerun.
- If there were no usable items, explicitly say `今日日无有效工作记录。`
- If any item failed to parse, mention `部分内容解析失败` in `信息缺口（如有）`.
- After publishing, send `今日日报复盘已完成：<链接>` to the bound chat.
