---
name: feishu-retro-review
description: Use when the user explicitly enters the exact command `review` and wants a Feishu work retrospective generated from the bound chat. This skill collects the day's multimodal chat content with lark-cli, asks the agent to synthesize it into a fixed 5+1 retrospective, then overwrites the same-day Feishu document and notifies the bound chat.
---

# Feishu Retro Review

Use this skill only for the exact trigger `review`.

## Workflow

1. Run `scripts/ensure_binding.py` to ensure the bound `工作复盘` chat exists.
2. Run `scripts/collect_inputs.py` to fetch the full same-day chat inputs plus `analysis_payload`.
3. Read `references/retro-template.md` and `references/multimodal-rules.md`, then analyze `analysis_payload` with the model while keeping raw collected inputs only as backup context.
4. Write one analytical Markdown retrospective using this exact structure:
   - `## 今日概览`
   - `## 推进时间线`
   - `## 当前现状`
   - `## 下一步待办`
   - `## 今日思考`
   - `## 信息缺口（如有）`
   Preferred styling:
   - Wrap `今日概览` in one concise callout block
   - Write `推进时间线` as timestamped bullets such as ``- `09:40` ...``
   - Render `当前现状` as a short stack of status cards, using light heading color plus small status emojis when helpful
   - Keep `下一步待办` as a checklist
   Writing distinction:
  - Let the model rewrite and compress the raw records instead of preserving their surface wording
  - Every section must analyze the full same-day chat inputs instead of only a local slice of messages
  - `推进时间线` is only for process nodes and may use timestamps
  - `当前现状` must summarize end-of-day status by theme, should usually avoid timestamps in the main sentence, can be grouped into `事项状态 / 知识沉淀 / 资源与线索 / 阶段判断 / 待确认项`, and must not repeat timeline bullets line by line
  - `下一步待办` must be rebuilt from the full-day action pool instead of only extracting explicit “明天/后续” phrases
  - `今日思考` should come from the full-day pattern of plans, progress, testing, and blockers rather than from one isolated sentence
5. Publish that Markdown with `scripts/publish_review.py --markdown-file <file>` or `--markdown`.
6. Confirm the bound chat received `今日日报复盘已完成：<链接>`.

## Hard Rules

- Do not trigger on natural-language variants. Only the exact command `review` applies.
- Do not ask the user follow-up questions during review generation; the skill must work from the collected same-day inputs alone.
- Do not publish the raw chat transcript or keyword buckets as the final retrospective.
- Always let the model synthesize, prioritize, and interpret the day's content.
- Prefer `analysis_payload` as the model-facing contract because it preserves text evidence, image evidence, and resource state explicitly.
- Group information by work theme and current status, not by raw message order.
- Prefer rich Lark-flavored Markdown when it improves readability, but do not add decorative blocks that make the document harder to maintain.
- Keep the final document useful for personal review: concise, specific, and honest about uncertainty.
- Same-day reruns must overwrite the same document, not create a new one.
- Treat downloaded images as first-class evidence even when OCR text is empty.
- OCR is only a fallback for images, not the main analysis path.
- If any multimodal item truly fails to prepare or cannot be incorporated, mention `部分内容解析失败` in the final retrospective.
- If evidence is weak, say `暂未明确` instead of inventing certainty.

## Output Standard

The final document must read like a durable personal work review:

- `今日概览` should let the user grasp the day in 30-60 seconds.
- `推进时间线` should keep only the key work nodes rather than replay the chat, and should include concrete timestamps whenever the input supports them.
- `当前现状` should freeze where the work stands at the end of the day, ideally as a compact set of status cards with concise item labels, clear status values, one short latest-record hint, and small emojis only where they improve scanability.
- `下一步待办` must be concrete and executable, avoiding vague phrases such as `继续跟进`.
- `今日思考` should keep only judgments or learnings truly supported by the input.
- `信息缺口（如有）` should be short, honest, and non-disruptive.

## References

- `references/retro-template.md`
- `references/multimodal-rules.md`
- `references/state-schema.md`
