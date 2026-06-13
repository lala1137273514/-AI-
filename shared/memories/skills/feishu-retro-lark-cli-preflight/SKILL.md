---
name: feishu-retro-lark-cli-preflight
description: Preflight the recurring `daily-feishu-retro` collection blocker when the user wants the `feishu-retro-review` contract followed exactly and runs keep dying before `analysis_payload`.
argument-hint: "[date]"
disable-model-invocation: true
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# Feishu retro lark-cli preflight

## When to use

Use this before or during a `daily-feishu-retro` run when:

1. The flow must follow `feishu-retro-review` exactly.
2. A recent run died before `analysis_payload`.
3. You need to prove whether the blocker is the local `lark-cli` entrypoint.

Do not use this for general Feishu debugging outside the `daily-feishu-retro` contract.

## Inputs / context to gather

1. Read `C:\Users\QYL\.codex\skills\feishu-retro-review\SKILL.md`.
2. Read `references/retro-template.md`, `references/multimodal-rules.md`, and `references/state-schema.md`.
3. Read `C:\Users\QYL\.codex\automations\daily-feishu-retro\memory.md` for the last blocker note.
4. Read `C:\Users\QYL\.codex\memories\MEMORY.md` Feishu task group for the repeated failure signature.

## Procedure

1. Confirm the contract assumptions.
   - `analysis_payload` is the primary evidence set.
   - Images are first-class evidence.
   - Publish is valid only through `scripts/publish_review.py` plus bound-chat confirmation.
2. Run the binding checks first.
   - `python C:\Users\QYL\.codex\skills\feishu-retro-review\scripts\ensure_binding.py`
   - If available, run `quick_check.py` too.
3. Treat binding output as a hint only.
   - Record `chat_id`, `chat_name`, `daily_docs`, and `last_review`.
   - Do not treat stale values as proof the run is healthy.
4. Preflight the local CLI entrypoint before assuming collection can work.
   - `Get-Command lark-cli,lark-cli.cmd`
   - `where.exe lark-cli`
   - `where.exe lark-cli.cmd`
   - `npm list -g --depth=0`
   - Check whether `C:\Users\QYL\AppData\Roaming\npm\lark-cli.cmd` exists.
   - Check whether `C:\Users\QYL\AppData\Roaming\npm\node_modules\@larksuiteoapi\lark-cli\bin\lark-cli.js` exists.
5. Attempt collection only after the preflight facts are recorded.
   - `python C:\Users\QYL\.codex\skills\feishu-retro-review\scripts\collect_inputs.py --date $ARGUMENTS`
6. If collection fails before `analysis_payload`, stop the workflow.
   - Append a dated blocker note to `C:\Users\QYL\.codex\automations\daily-feishu-retro\memory.md`.
   - Preserve the exact error string and the no-publish outcome.
7. Only continue to synthesis/publish if `analysis_payload` was actually produced.

## Efficiency plan

1. Reuse the known failure signature first instead of rediscovering it from scratch.
2. Run `Get-Command`, `where.exe`, and `npm list -g --depth=0` before deeper exploration.
3. Stop early if `collect_inputs.py` fails in `skill_entry.py -> run_cli` with `FileNotFoundError: [WinError 2]`; that is already enough to prove the recurring blocker.
4. Do not spend time on publish logic if `analysis_payload` does not exist.

## Pitfalls and fixes

- Symptom: `ensure_binding.py` returns a chat id and old docs, so the run looks healthy.
  - Likely cause: persisted binding state is stale.
  - Fix: verify `collect_inputs.py` can actually spawn `lark-cli`.
- Symptom: `lark-cli.cmd` exists, but the run still dies in `run_cli`.
  - Likely cause: the shim exists but its target JS file is missing or unreadable.
  - Fix: check the target path under `...\@larksuiteoapi\lark-cli\bin\lark-cli.js`.
- Symptom: there is pressure to publish anyway.
  - Likely cause: collection failed but the contract is being bypassed.
  - Fix: stop and record the blocker; do not fake synthesis or publish.
- Symptom: persona cleanup appears to succeed.
  - Likely cause: cleanup was attempted but disk writes failed.
  - Fix: state plainly when persona persistence was unavailable.

## Verification checklist

1. Confirm whether `collect_inputs.py` produced `analysis_payload`.
2. If not, confirm the exact failure signature and whether `Get-Command` / `where.exe` / `npm list -g --depth=0` match the known broken-entrypoint pattern.
3. Confirm the automation memory file has a new dated blocker note.
4. Confirm no synthesis, no `publish_review.py`, and no bound-chat completion were claimed when `analysis_payload` was missing.
