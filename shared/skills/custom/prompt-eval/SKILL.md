---
name: prompt-eval
description: Local, no-API-cost prompt evaluation harness. Stress-tests a text/work prompt by generating realistic scenarios, running the prompt under each (optionally blind via subagents), and scoring outputs 0-10 across tone/completeness/usefulness/accuracy/authenticity — producing a markdown scorecard plus improvement suggestions. A lightweight local reproduction of earino/prompt-harness that uses the in-session Claude as both model and judge instead of OpenRouter. Use when asked to "test a prompt", "evaluate this prompt", "score my prompt", "is this prompt any good", or before shipping a reusable work prompt (email/support/report templates, etc.).
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Agent
  - AskUserQuestion
---

# Prompt Eval — local prompt testing harness

Reproduces the [earino/prompt-harness](https://github.com/earino/prompt-harness) idea **without OpenRouter and without cost**: inside Claude Code, *you* are the model under test and the judge. The bundled `scripts/harness.py` (stdlib only) handles the deterministic plumbing — extracting `[PARAMETERS]` and rendering the scorecard. Everything that needs judgement (scenarios, outputs, scores) is produced by you and written into a results JSON.

This evaluates **text / work prompts** (email, support replies, summaries, reports, agent instructions). It does **not** generate prompts — it grades them.

## When to use

Trigger on: "test/evaluate/score this prompt", "is this prompt good", "which version is better", or before reusing a prompt template in production.

## Inputs

- A **prompt** — a file path (markdown) or pasted inline text. Placeholders are `[UPPER_SNAKE]` or `{{handlebars}}`.
- Optional: number of scenarios (default **3**), the criteria set (default below), and whether to run **blind** via subagents (default yes for rigor).

If the prompt is pasted inline, first write it to `runs/<name>.md` so the script can read it.

## Workflow

### 1. Extract parameters

```bash
python scripts/harness.py extract <prompt.md>
```

This prints a **run-skeleton JSON** (prompt name, criteria, the list of `[PARAMETERS]`, empty `scenarios`). Save it to `runs/<name>.results.json` and fill it in across the next steps.

### 2. Generate scenarios

Invent **N realistic, diverse** scenarios that fill every parameter with concrete values. Cover the spread the prompt must survive, not just the happy path:
- a **typical** case,
- an **edge/stress** case (missing info, hostile/irate user, unusually large or tiny values, ambiguous intent),
- a **boundary** case (tone or format easy to get wrong).

Write each as `{"id", "description", "values": {PARAM: value, ...}}`.

### 3. Run the prompt (blind)

For each scenario, substitute the values into the prompt and **execute it** to produce an output.

- **Default (rigorous):** spawn a fresh subagent per scenario via the Agent tool. Give it ONLY the filled prompt — **not** the rubric — so execution is blind to how it will be graded. Capture its output verbatim.
- **Quick mode:** produce the output inline yourself.
- **Multi-model (optional):** if the user pastes outputs from other models (GPT/Gemini/etc.) for the same filled prompt, add them as extra `runs` with the right `model` label to get a side-by-side comparison — still no API needed.

Record each as a `run`: `{"model": "claude-opus-4.8", "output": "..."}`.

### 4. Score each output (independent judge)

Score every output **separately from generation** — ideally a different pass or a dedicated judge subagent — to limit self-grading bias. Be a skeptical grader; reserve 9-10 for genuinely excellent output.

Default rubric (0-10 each):
- **tone** — appropriate voice/register for the audience and situation.
- **completeness** — covers everything the prompt asked for; no dropped requirements.
- **usefulness** — would the recipient actually act on / be satisfied by this?
- **accuracy** — factually correct, no hallucinated specifics, follows constraints.
- **authenticity** — sounds human and genuine, not generic AI filler.

For each run add `"scores": {criterion: int}`, an `"overall"` (mean unless you weight it), and a one-line `"notes"` justifying the lowest score.

### 5. Render the scorecard

```bash
python scripts/harness.py render runs/<name>.results.json
```

Save the markdown to `runs/<name>.report.md`. It shows the per-run table, per-criterion averages, per-model averages (if multiple), the overall score, and the weakest dimension.

### 6. Diagnose & improve

Close the loop — this is the point of testing:
1. Name the **weakest dimension** and the concrete failures behind it (cite specific outputs).
2. Propose a **revised prompt** that targets those failures (surgical edits, not a rewrite).
3. Offer to **re-run** the harness on the revised prompt and show an A/B (old overall vs new overall).

## Scoring mode B — weighted rubric (HeartBench method, still local)

Use this instead of the flat 0-10 rubric when the quality you care about is **graded, not binary** — e.g. "how human/warm/on-brand does this sound", persona voice, tone systems — or when flat 0-10 keeps coming back inflated. It ports the [HeartBench](https://github.com/inclusionAI/HeartBench) weighted-rubric math (via `cortex/prompt_opt/heartbench`) but keeps **you** as the judge: no `GOOGLE_API_KEY`, no network.

How it differs from the default mode: instead of you assigning 0-10 per criterion, you write a **weighted rubric** and judge each item as a **binary hit (0/1)** — which is more reliable for an LLM and resistant to grade inflation. The score math is asymmetric and gated.

**Rubric item** = `{"dimension": str, "score": number, "content": str}`:
- `score > 0` — positive item; counts only when the output **fully** achieves it (hit = 1).
- `score < 0` — penalty item; counts when the output even **touches** it (hit = 1).
- dimension `其他` / `other` / `gate` (score 0) — **anti-cheat gate**; any hit **zeroes the whole question** (off-topic, template-parroting, broke character).

Group rubric items by `scenario_key` (e.g. greet / complain / advice / …) so weak scenarios surface separately.

### Rubric design — calibrate so "merely compliant" ≠ ceiling

A flat rubric (one positive per dimension) makes every adequate reply score ~100, because hitting the lone positive maxes the dimension. Two rules fix that:

1. **Depth tiers per dimension** (HeartBench's 浅/深 idea): a small `+2` "达标/adequate" item AND a separate `+7` "出彩/excellent — genuinely human, precise, surprising" item. Ordinary-good hits only `+2` → lands ~70-90; reaching ~100 requires the `+7`. This is the lever that creates spread.
2. **Keep penalties modest** (`-2`…`-4`) and well-targeted; reserve `-8` for catastrophes (broke character, AI-identity leak). Counter-intuitively, piling large penalties *raises* the baseline (the log floor `min` widens), so don't fix leniency by adding big landmines — fix it with the `+7` gap and by **encoding every hard rule of the prompt as its own penalty item** (length over-limit, banned words, format violations) so real violations actually land.

Split coarse positives into sub-items where partial credit should be possible. Judge **strictly**: a positive is hit only if *fully* achieved; borderline → 0.

### Cross-check with multiple judges (recommended default)

To remove single-judge bias, have **2+ independent judge subagents** each judge all scenarios blind, emitting `{scenario_key: [0/1,...]}`. Merge them: **positive items = AND** (all judges must agree → strict credit), **penalty/gate items = OR** (any judge flags → strict penalty).

**Flow:**
1. Build a depth-tiered weighted rubric per scenario (jsonl). Worked example: `examples/loona_humanlike_rubric_v2.jsonl` here (depth-tiered), adapted from `cortex/prompt_opt/heartbench/loona_humanlike_rubric.jsonl`.
2. Generate the outputs to grade (blind subagents, as in mode A).
3. Spawn **2+ judge subagents**, each reads a brief (cases + numbered rubric items + strict rules) and outputs `{scenario_key:[0/1,...]}`. Save each to `runs/<name>.judgeN.json`.
4. Merge: `python scripts/merge_judges.py --rubric <rubric.jsonl> --judge runs/<name>.judgeA.json --judge runs/<name>.judgeB.json --out runs/<name>.score_in.jsonl` (warns on judge disagreement / malformed arrays).
5. Score: `python scripts/heartscore.py --input runs/<name>.score_in.jsonl --out runs/<name>.scored.jsonl`
6. Read `<...>.scored.jsonl.summary.json` → `OVERALL` (0-100), `by_dimension`, `by_scenario`, `n_gated`. Iterate by comparing rounds' `OVERALL` and `by_dimension` — and keep the rubric **fixed** across an A/B so a score change reflects the prompt, not the ruler. (Watch for rubric false-positives too: an over-literal penalty keyword can mis-fire on a homonym — fix the rubric, not the prompt.)

The two modes are independent axes: default 0-10 for general correctness/usefulness; mode B for graded "humanlike"/voice quality. Keep the rubric fixed across an A/B comparison.

## Output to the user

A short summary: overall score, weakest dimension, the 1-3 highest-leverage fixes, and the path to `report.md` (or `summary.json` in mode B). Then ask whether to apply the revised prompt and re-test.

## Notes

- Zero external API, zero cost — the session model does the work. No `OPENROUTER_API_KEY`.
- Scores are LLM judgement, not ground truth; their value is **relative** (A/B before vs after, model vs model), so keep the rubric fixed across a comparison.
- Keep runs under `skills/prompt-eval/runs/` (gitignored scratch) or wherever the user prefers.
