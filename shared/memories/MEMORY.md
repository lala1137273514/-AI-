# Task Group: Feishu retro automation contract execution and repeated lark-cli collection blockage

scope: Scheduled `daily-feishu-retro` runs that must follow `feishu-retro-review` exactly, especially when collection dies before `analysis_payload` because the local `lark-cli` entrypoint is missing, unreadable, or broken.
applies_to: cwd=C:\Users\QYL\.codex\worktrees\46ec\work, C:\Users\QYL\.codex\worktrees\dc46\work, C:\Users\QYL\.codex\worktrees\7b31\work, C:\Users\QYL\.codex\worktrees\dec0\work, C:\Users\QYL\.codex\worktrees\45db\work, C:\Users\QYL\.codex\worktrees\6bbd\work, C:\Users\QYL\.codex\worktrees\782e\work, C:\Users\QYL\.codex\worktrees\7098\work, C:\Users\QYL\.codex\worktrees\1f13\work plus automation state under C:\Users\QYL\.codex\automations\daily-feishu-retro; reuse_rule=safe for this automation family across worktrees, but re-check local CLI install state, chat binding freshness, and persona-write permissions on each machine/session

## Task 1: Re-read the authoritative contract before any scheduled Feishu retro run

### rollout_summary_files

- rollout_summaries/2026-06-12T10-00-57-PYKn-daily_feishu_retro_blocked_by_missing_lark_cli.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\1f13\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\12\rollout-2026-06-12T18-01-04-019ebb47-0fe3-70e1-91d5-d40df59568f3.jsonl, updated_at=2026-06-12T10:05:17+00:00, thread_id=019ebb47-0fe3-70e1-91d5-d40df59568f3, latest repeat: the contract, bound chat, and stale state were re-validated before collection)
- rollout_summaries/2026-06-07T10-02-09-ExVP-daily_feishu_retro_blocked_by_missing_lark_cli.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\7098\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\07\rollout-2026-06-07T18-02-14-019ea188-6082-7172-abb3-db17cdc9bad5.jsonl, updated_at=2026-06-07T10:06:20+00:00, thread_id=019ea188-6082-7172-abb3-db17cdc9bad5, contract, automation memory, and skill references were re-read before collection)
- rollout_summaries/2026-06-05T10-01-22-cnmv-daily_feishu_retro_collect_inputs_lark_cli_file_not_found.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\6bbd\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\05\rollout-2026-06-05T18-01-27-019e973a-ef90-7f63-a901-054de8b0d2ef.jsonl, updated_at=2026-06-05T10:06:13+00:00, thread_id=019e973a-ef90-7f63-a901-054de8b0d2ef, contract and automation memory were re-read before collection)
- rollout_summaries/2026-06-03T10-02-08-LkJy-daily_feishu_retro_lark_cli_collection_blocked.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\45db\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\03\rollout-2026-06-03T18-02-13-019e8cee-e9c2-7323-bf42-af6b82241410.jsonl, updated_at=2026-06-03T10:08:20+00:00, thread_id=019e8cee-e9c2-7323-bf42-af6b82241410, contract + prior memory re-read before execution)
- rollout_summaries/2026-06-02T06-10-13-69jD-daily_feishu_retro_lark_cli_blocked.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\7b31\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\02\rollout-2026-06-02T14-10-20-019e86f4-3c12-7223-ad85-a055b11da245.jsonl, updated_at=2026-06-02T06:18:43+00:00, thread_id=019e86f4-3c12-7223-ad85-a055b11da245, strict contract-reading and environment prep passed before collection)

### keywords

- feishu-retro-review, daily-feishu-retro, analysis_payload, publish_review.py, retro-template.md, multimodal-rules.md, state-schema.md, images as first-class evidence, review trigger, bound chat confirmation

## Task 2: Verify the repeated blocker is the local lark-cli entrypoint, not Feishu content or publish logic

### rollout_summary_files

- rollout_summaries/2026-06-12T10-00-57-PYKn-daily_feishu_retro_blocked_by_missing_lark_cli.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\1f13\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\12\rollout-2026-06-12T18-01-04-019ebb47-0fe3-70e1-91d5-d40df59568f3.jsonl, updated_at=2026-06-12T10:05:17+00:00, thread_id=019ebb47-0fe3-70e1-91d5-d40df59568f3, newest repeat: `Get-Command lark-cli,lark-cli.cmd,lark` found nothing usable and `npm list -g --depth=0` was still empty)
- rollout_summaries/2026-06-07T10-02-09-ExVP-daily_feishu_retro_blocked_by_missing_lark_cli.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\7098\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\07\rollout-2026-06-07T18-02-14-019ea188-6082-7172-abb3-db17cdc9bad5.jsonl, updated_at=2026-06-07T10:06:20+00:00, thread_id=019ea188-6082-7172-abb3-db17cdc9bad5, `quick_check.py` also looked healthy while `collect_inputs.py` still died before any same-day fetch)
- rollout_summaries/2026-06-06T10-01-13-kNr4-daily_feishu_retro_collection_blocked_lark_cli_missing.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\782e\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\06\rollout-2026-06-06T18-01-18-019e9c61-273d-78e3-b024-d026b85ea6c2.jsonl, updated_at=2026-06-06T10:07:36+00:00, thread_id=019e9c61-273d-78e3-b024-d026b85ea6c2, stale binding still looked healthy while `lark-cli.cmd` pointed at a missing JS target)
- rollout_summaries/2026-06-05T10-01-22-cnmv-daily_feishu_retro_collect_inputs_lark_cli_file_not_found.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\6bbd\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\05\rollout-2026-06-05T18-01-27-019e973a-ef90-7f63-a901-054de8b0d2ef.jsonl, updated_at=2026-06-05T10:06:13+00:00, thread_id=019e973a-ef90-7f63-a901-054de8b0d2ef, fresh confirmation that `run_cli` died before any same-day chat fetch)
- rollout_summaries/2026-06-03T10-02-08-LkJy-daily_feishu_retro_lark_cli_collection_blocked.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\45db\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\03\rollout-2026-06-03T18-02-13-019e8cee-e9c2-7323-bf42-af6b82241410.jsonl, updated_at=2026-06-03T10:08:20+00:00, thread_id=019e8cee-e9c2-7323-bf42-af6b82241410, `collect_inputs.py` still died in `run_cli` before `analysis_payload`)
- rollout_summaries/2026-06-03T07-35-30-ZfOq-daily_feishu_retro_blocked_by_lark_cli_entrypoint.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\dec0\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\03\rollout-2026-06-03T15-35-33-019e8c68-aa73-77e3-95b5-79edf4d5abda.jsonl, updated_at=2026-06-03T07:42:06+00:00, thread_id=019e8c68-aa73-77e3-95b5-79edf4d5abda, quick check looked healthy but collection still failed)
- rollout_summaries/2026-06-02T06-10-13-69jD-daily_feishu_retro_lark_cli_blocked.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\7b31\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\02\rollout-2026-06-02T14-10-20-019e86f4-3c12-7223-ad85-a055b11da245.jsonl, updated_at=2026-06-02T06:18:43+00:00, thread_id=019e86f4-3c12-7223-ad85-a055b11da245, same blocker verified with empty npm globals and missing target JS)
- rollout_summaries/2026-05-25T10-01-15-FfjZ-daily_feishu_retro_lark_cli_blocked_no_publish.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\dc46\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\05\25\rollout-2026-05-25T18-01-20-019e5e94-dfdc-7472-b344-963233ab336b.jsonl, updated_at=2026-05-25T10:04:55+00:00, thread_id=019e5e94-dfdc-7472-b344-963233ab336b, blocked run ended without publish and persona cleanup also failed)
- rollout_summaries/2026-05-25T06-54-10-U2Fz-daily_feishu_retro_lark_cli_entrypoint_blocked.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\46ec\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\05\25\rollout-2026-05-25T14-54-12-019e5de9-996a-72c3-acd2-d40a43bb7319.jsonl, updated_at=2026-05-25T07:01:28+00:00, thread_id=019e5de9-996a-72c3-acd2-d40a43bb7319, earliest repeated confirmation of missing/unusable local CLI)

### keywords

- collect_inputs.py, run_cli, lark-cli, lark-cli.cmd, lark, FileNotFoundError, WinError 2, Get-Command, where.exe, npm list -g --depth=0, @larksuiteoapi, quick_check.py, stale binding, last_review 2026-04-02, C:\Users\QYL\AppData\Roaming\npm\lark-cli.cmd, lark-cli.js missing, no analysis_payload

## Task 3: Persist the blocker in automation memory and stop cleanly instead of bypassing the contract

### rollout_summary_files

- rollout_summaries/2026-06-12T10-00-57-PYKn-daily_feishu_retro_blocked_by_missing_lark_cli.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\1f13\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\12\rollout-2026-06-12T18-01-04-019ebb47-0fe3-70e1-91d5-d40df59568f3.jsonl, updated_at=2026-06-12T10:05:17+00:00, thread_id=019ebb47-0fe3-70e1-91d5-d40df59568f3, blocker note appended and the run stopped before synthesis/publish; `CODEX_HOME` was absent so absolute paths were safer)
- rollout_summaries/2026-06-07T10-02-09-ExVP-daily_feishu_retro_blocked_by_missing_lark_cli.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\7098\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\07\rollout-2026-06-07T18-02-14-019ea188-6082-7172-abb3-db17cdc9bad5.jsonl, updated_at=2026-06-07T10:06:20+00:00, thread_id=019ea188-6082-7172-abb3-db17cdc9bad5, blocker note appended for 2026-06-07 and the run stopped before synthesis/publish)
- rollout_summaries/2026-06-06T10-01-13-kNr4-daily_feishu_retro_collection_blocked_lark_cli_missing.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\782e\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\06\rollout-2026-06-06T18-01-18-019e9c61-273d-78e3-b024-d026b85ea6c2.jsonl, updated_at=2026-06-06T10:07:36+00:00, thread_id=019e9c61-273d-78e3-b024-d026b85ea6c2, blocker note appended for 2026-06-06 and the run stopped before synthesis/publish)
- rollout_summaries/2026-06-05T10-01-22-cnmv-daily_feishu_retro_collect_inputs_lark_cli_file_not_found.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\6bbd\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\05\rollout-2026-06-05T18-01-27-019e973a-ef90-7f63-a901-054de8b0d2ef.jsonl, updated_at=2026-06-05T10:06:13+00:00, thread_id=019e973a-ef90-7f63-a901-054de8b0d2ef, blocker note appended and persona cleanup permission failure was preserved)
- rollout_summaries/2026-06-03T10-02-08-LkJy-daily_feishu_retro_lark_cli_collection_blocked.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\45db\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\03\rollout-2026-06-03T18-02-13-019e8cee-e9c2-7323-bf42-af6b82241410.jsonl, updated_at=2026-06-03T10:08:20+00:00, thread_id=019e8cee-e9c2-7323-bf42-af6b82241410, blocker note appended and run intentionally stopped before synthesis/publish)
- rollout_summaries/2026-06-03T07-35-30-ZfOq-daily_feishu_retro_blocked_by_lark_cli_entrypoint.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\dec0\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\03\rollout-2026-06-03T15-35-33-019e8c68-aa73-77e3-95b5-79edf4d5abda.jsonl, updated_at=2026-06-03T07:42:06+00:00, thread_id=019e8c68-aa73-77e3-95b5-79edf4d5abda, durable blocker note preserved after patch-context recovery)
- rollout_summaries/2026-06-02T06-10-13-69jD-daily_feishu_retro_lark_cli_blocked.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\7b31\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\02\rollout-2026-06-02T14-10-20-019e86f4-3c12-7223-ad85-a055b11da245.jsonl, updated_at=2026-06-02T06:18:43+00:00, thread_id=019e86f4-3c12-7223-ad85-a055b11da245, automation memory updated; persona cleanup permission issue recorded)
- rollout_summaries/2026-05-25T10-01-15-FfjZ-daily_feishu_retro_lark_cli_blocked_no_publish.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\dc46\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\05\25\rollout-2026-05-25T18-01-20-019e5e94-dfdc-7472-b344-963233ab336b.jsonl, updated_at=2026-05-25T10:04:55+00:00, thread_id=019e5e94-dfdc-7472-b344-963233ab336b, no publish path was fabricated after the verified blocker)
- rollout_summaries/2026-05-25T06-54-10-U2Fz-daily_feishu_retro_lark_cli_entrypoint_blocked.md (cwd=\\?\C:\Users\QYL\.codex\worktrees\46ec\work, rollout_path=C:\Users\QYL\.codex\sessions\2026\05\25\rollout-2026-05-25T14-54-12-019e5de9-996a-72c3-acd2-d40a43bb7319.jsonl, updated_at=2026-05-25T07:01:28+00:00, thread_id=019e5de9-996a-72c3-acd2-d40a43bb7319, durable memory note added after verifying the same broken entrypoint)

### keywords

- automation memory, C:\Users\QYL\.codex\automations\daily-feishu-retro\memory.md, blocked run, no publish, no chat confirmation, apply_patch context mismatch, session_cleanup.py, PermissionError, hook_error.log, CODEX_HOME

## User preferences

- when the user says "Use [feishu-retro-review] as the only authoritative scheduled retrospective flow. Follow the current skill contract exactly" -> do not invent alternate collection, synthesis, or publishing paths for this automation family [Task 1][Task 2]
- when the user says "use `analysis_payload` as the primary evidence set" -> build the retro from `analysis_payload`, not from a raw transcript retell; if `analysis_payload` does not exist, the run is not ready for synthesis [Task 1][Task 2]
- when the user says "Treat images as first-class evidence" -> keep multimodal evidence in the main path and do not require OCR-first handling [Task 1]
- when the user says "publish only through `scripts/publish_review.py` and confirm the bound chat receives the final document link" -> success requires both the script and the bound-chat confirmation message [Task 1]
- when the user says to ignore bot/system noise and the exact trigger `review` -> filter those during collection instead of treating them as work evidence [Task 1][Task 2]
- when the user says not to use legacy image-only repair flows or ad-hoc markdown publishing paths -> if collection is blocked, persist the blocker and stop instead of improvising a side route [Task 2][Task 3]
- when persona/session persistence cannot really write to disk, state that plainly instead of implying cleanup succeeded [Task 3]

## Reusable knowledge

- the contract order is fixed: `ensure_binding.py` -> `collect_inputs.py` -> model synthesis from `analysis_payload` -> `publish_review.py` -> confirm `今日日报复盘已完成：<link>` in the bound chat [Task 1]
- `retro-template.md`, `multimodal-rules.md`, and `state-schema.md` all reinforce the same shape: `analysis_payload` is the model-facing input and raw `items` are only backup context [Task 1][Task 2]
- `ensure_binding.py` and even `quick_check.py` can return historical binding state that looks healthy; stale `chat_id`, stale `daily_docs`, or a saved `last_review` do not prove same-day collection is working. The persisted binding was still frozen at `2026-04-02` in the 2026-06-12 repeat. [Task 1][Task 2]
- the repeated blocker signature is stable: `collect_inputs.py --date <day>` fails in `skill_entry.py -> run_cli` with `FileNotFoundError: [WinError 2]`, `Get-Command lark-cli,lark-cli.cmd,lark` and `where.exe lark-cli*` return nothing, `npm list -g --depth=0` is `(empty)`, `lark-cli.cmd` may exist but be unreadable, and `...\@larksuiteoapi\lark-cli\bin\lark-cli.js` is missing [Task 2]
- clearing `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, `GIT_HTTP_PROXY`, and `GIT_HTTPS_PROXY` did not change the failure mode in repeated runs, so proxy cleanup is not the meaningful fix when the local CLI entrypoint itself is broken [Task 2]
- the durable blocker log belongs in `C:\Users\QYL\.codex\automations\daily-feishu-retro\memory.md`; each note should preserve the date/time, stale binding facts, exact `lark-cli` failure signature, and the no-`analysis_payload` / no-publish outcome [Task 3]
- the shell environment may not expose `CODEX_HOME`; when that happens, use absolute paths for automation memory inspection and blocker logging [Task 3]
- `cc-persona` cleanup may fail because this environment cannot write under `C:\Users\QYL\.codex\skills\cc-persona\memory\...`; do not assume persona state was saved just because cleanup was attempted [Task 3]
- Related skill: skills/feishu-retro-lark-cli-preflight/SKILL.md [Task 2][Task 3]

## Failures and how to do differently

- symptom: `ensure_binding.py` or `quick_check.py` returns a chat id and old `daily_docs`, so the run looks healthy at first glance -> cause: binding state is historical, not proof that current message fetch works -> fix: validate that `collect_inputs.py` can actually spawn `lark-cli` before assuming the workflow is unblocked [Task 1][Task 2]
- symptom: the retro stops before `analysis_payload` exists -> cause: the local `lark-cli` executable is absent, unreadable, or points to a missing target JS file -> fix: diagnose the local CLI install first; until `lark-cli` can spawn, synthesis, publish, and chat confirmation are impossible [Task 2]
- symptom: there is pressure to repair the run with an ad-hoc publish path -> cause: the contract is blocked at collection, tempting a shortcut -> fix: do not bypass the contract; record the blocker in automation memory and stop before synthesis/publish [Task 3]
- symptom: an automation-memory patch fails even though the file should be writable -> cause: the tail drifted and the patch context no longer matches -> fix: re-open the file tail and patch against the observed trailing lines before retrying [Task 3]
- symptom: automation helper code assumes `CODEX_HOME` exists -> cause: this shell can omit it -> fix: fall back to absolute paths instead of environment-derived joins when writing blocker evidence [Task 3]
- symptom: persona cleanup appears to run but no durable state shows up later -> cause: `session_cleanup.py` hit `PermissionError` while writing under the cc-persona memory path -> fix: say explicitly that persona persistence was unavailable in this environment [Task 3]

# Task Group: AI Coach requirement form audit and group-post copy iteration

scope: Analysis-first review of AI Coach requirement collection forms plus direct-to-forward group announcement copy that may need one or two follow-up tweaks for coverage and light emoji.
applies_to: cwd=C:\Users\QYL\Documents\Codex\2026-06-12\ai-coach-ai-vibe-coding-ai; reuse_rule=safe for similar Chinese form-audit plus group-copy tasks in this project/workspace family, but keep reuse at the workflow level rather than assuming the same form fields or audience

## Task 1: Audit the AI Coach requirement collection form before proposing changes

### rollout_summary_files

- rollout_summaries/2026-06-12T02-24-04-IIAX-ai_coach_form_analysis_and_group_post_copy.md (cwd=\\?\C:\Users\QYL\Documents\Codex\2026-06-12\ai-coach-ai-vibe-coding-ai, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\12\rollout-2026-06-12T10-24-04-019eb9a4-c93a-7080-80d1-d6b9d5c61f63.jsonl, updated_at=2026-06-12T08:09:45+00:00, thread_id=019eb9a4-c93a-7080-80d1-d6b9d5c61f63, audit stayed objective and diagnosed the form before any rewrite)

### keywords

- AI Coach, requirement collection form, form audit, objective review, analyze, Evidence / Inference / Unknown, sensitive info, success criteria, output standard, priority, reuse

## Task 2: Write a direct-to-forward group announcement and iterate for coverage plus light emoji

### rollout_summary_files

- rollout_summaries/2026-06-12T02-24-04-IIAX-ai_coach_form_analysis_and_group_post_copy.md (cwd=\\?\C:\Users\QYL\Documents\Codex\2026-06-12\ai-coach-ai-vibe-coding-ai, rollout_path=C:\Users\QYL\.codex\sessions\2026\06\12\rollout-2026-06-12T10-24-04-019eb9a4-c93a-7080-80d1-d6b9d5c61f63.jsonl, updated_at=2026-06-12T08:09:45+00:00, thread_id=019eb9a4-c93a-7080-80d1-d6b9d5c61f63, group-post copy was revised to include AI-usage problems and restrained emoji)

### keywords

- group announcement, direct-to-forward copy, 使用 AI 过程中的问题, emoji, low-friction wording, not formal requirements, vibe coding, sensitive material reminder

## User preferences

- when the user asks "帮我客观研究一下下面的表格有什么不足" -> start with an objective audit, not praise or immediate rewriting [Task 1]
- when the user asks for analysis before any rewrite -> diagnose first, then talk about optimization; do not slide from review into implementation too early [Task 1]
- when the user asks "接下来要把这个表格发到群里，我该怎么描述" -> give copy they can forward directly, not abstract guidance about messaging [Task 2]
- when the user adds "再加一个以及使用AI过程中的问题" -> make sure the announcement explicitly covers problems users hit during AI usage, not only desired use cases [Task 2]
- when the user says "加一些表情呗" -> the user accepts a lighter group-chat tone with some emoji, but the emoji should stay restrained and functional instead of turning the post into marketing fluff [Task 2]

## Reusable knowledge

- the key diagnosis was not “too few questions”; it was that the form collected many clues but still could not stably answer “is this worth doing, can it be done, and how risky is it” [Task 1]
- the high-value missing fields in this form family were output standard, priority/value, affected people or business metric, system/permission boundary, input-format stability, reusability, and success criteria [Task 1]
- if a form asks people to upload materials, the sensitive-information check should come before the upload step so users do not send something they should never upload in the first place [Task 1]
- a reliable group-announcement shape here was: say what is being collected first (real work scenarios plus AI-usage pain points), lower the response barrier next (“you do not need to write a formal requirement”), then explain how submissions will be processed, and end with a sensitive-material reminder [Task 2]
- the final intro line that worked combined both lanes in one sentence: repeated, time-consuming, error-prone work that AI or vibe coding could help with, plus problems encountered while using AI [Task 2]
- restrained emoji worked better than a plain notice, but the accepted style was still closer to utility markers than hype; use a few separators like `👀`, `✍️`, `⬇️` rather than dense decorative emoji [Task 2]

## Failures and how to do differently

- symptom: a form-review request quickly turns into editing suggestions or solution design -> cause: the audit goal was ignored -> fix: keep the first pass diagnostic and evidence-based before proposing fixes [Task 1]
- symptom: a group-post draft sounds like internal process documentation -> cause: the copy was written as advice instead of a ready-to-forward message -> fix: write the post in forwardable chat language from the start [Task 2]
- symptom: the announcement only talks about desired AI tasks and misses current blockers -> cause: AI-usage problems were not surfaced explicitly -> fix: reserve a phrase for “使用 AI 过程中的问题” so pain points are included alongside scenarios [Task 2]
- symptom: the user asks for emoji after seeing the first draft -> cause: the initial version was too flat or formal -> fix: default to preparing a light-chat variant with restrained emoji for similar group-post tasks [Task 2]

# Task Group: Chinese travel-planning spec review and copy-before-edit revision

scope: Strict read-only audits of the Loona travel-planning delivery spec and follow-up draft-only revisions that must keep the original untouched while fixing contract drift before prose polish.
applies_to: cwd=C:\Users\QYL and C:\Users\QYL\Desktop\loona-workbench; reuse_rule=safe for similar Chinese markdown spec-review and copy-based revision tasks in this workspace family, but re-check exact line handles, prompt/schema names, and tool capabilities on the current files

## Task 1: Audit the travel-planning delivery spec against real UI, prompt, and tool sources

### rollout_summary_files

- rollout_summaries/2026-05-26T11-00-14-kHjR-travel_planning_spec_review_and_revision_copy.md (cwd=\\?\C:\Users\QYL, rollout_path=C:\Users\QYL\.codex\sessions\2026\05\26\rollout-2026-05-26T19-00-14-019e63f1-3a68-7942-a736-37a013ab973b.jsonl, updated_at=2026-05-26T11:12:15+00:00, thread_id=019e63f1-3a68-7942-a736-37a013ab973b, strict review stayed doc-scoped and set up the later copy-based revision)
- rollout_summaries/2026-05-26T10-46-20-IvQB-travel_plan_spec_audit_contract_mismatches.md (cwd=\\?\C:\Users\QYL, rollout_path=C:\Users\QYL\.codex\sessions\2026\05\26\rollout-2026-05-26T18-46-20-019e63e4-8218-7bb3-ac9f-7f852a06ebc9.jsonl, updated_at=2026-05-26T10:53:16+00:00, thread_id=019e63e4-8218-7bb3-ac9f-7f852a06ebc9, prompt/UI/code contract drift confirmed)
- rollout_summaries/2026-05-26T10-34-49-H5tq-travel_planning_spec_readonly_audit_schema_mismatch.md (cwd=\\?\C:\Users\QYL, rollout_path=C:\Users\QYL\.codex\sessions\2026\05\26\rollout-2026-05-26T18-34-49-019e63d9-f7bc-7491-97a8-6aeb5991102c.jsonl, updated_at=2026-05-26T10:42:39+00:00, thread_id=019e63d9-f7bc-7491-97a8-6aeb5991102c, UI/tool capability mismatch cross-check completed)

### keywords

- 旅行规划_交付稿v1.md, 只读，不要修改任何文件, 要挑刺，要怀疑，宁可多报, 结构化清单, TravelView, TravelDayFocus, ClarifyCard, sections[], cards[], days[], narrationSegments, get_weather, get_travel_plan_template

## Task 2: Preserve confirmed-good points separately while surfacing defects

### rollout_summary_files

- rollout_summaries/2026-05-26T10-34-49-H5tq-travel_planning_spec_readonly_audit_schema_mismatch.md (cwd=\\?\C:\Users\QYL, rollout_path=C:\Users\QYL\.codex\sessions\2026\05\26\rollout-2026-05-26T18-34-49-019e63d9-f7bc-7491-97a8-6aeb5991102c.jsonl, updated_at=2026-05-26T10:42:39+00:00, thread_id=019e63d9-f7bc-7491-97a8-6aeb5991102c, final format required a structured table plus an explicit verified-OK section)

### keywords

- 已验证 OK 的点, evidence-anchored findings, structured issue table, severity, position, suggested fix, doc-only review

## Task 3: Copy the original spec and revise only the draft

### rollout_summary_files

- rollout_summaries/2026-05-26T11-00-14-kHjR-travel_planning_spec_review_and_revision_copy.md (cwd=\\?\C:\Users\QYL, rollout_path=C:\Users\QYL\.codex\sessions\2026\05\26\rollout-2026-05-26T19-00-14-019e63f1-3a68-7942-a736-37a013ab973b.jsonl, updated_at=2026-05-26T11:12:15+00:00, thread_id=019e63f1-3a68-7942-a736-37a013ab973b, separate revision draft created and original preserved)

### keywords

- copy-before-edit, 修订稿, TravelPayload, evidence_refs, base_span, acceptance scenarios, original untouched, revised copy, UTF-8 Chinese markdown

## User preferences

- when the user says "只读，不要修改任何文件" and "只看这个文档，不需要参考 demo" -> default to a read-only, evidence-based, doc-scoped audit and do not pull in external demo context unless explicitly asked [Task 1]
- when the user says "要挑刺，要怀疑，宁可多报" -> bias toward exhaustive inconsistency hunting instead of a soft summary [Task 1]
- when the user asks for a "结构化清单" or a table with evidence/fixes -> return evidence-anchored findings rather than loose narrative criticism [Task 1][Task 2]
- when the user explicitly asks for "已验证 OK 的点" -> preserve confirmed-good items in a separate final section so they do not get buried in the defect list [Task 2]
- when the user asks whether you can copy a file and revise it -> default to creating a separate draft copy first, not editing the original in place [Task 3]

## Reusable knowledge

- Chinese markdown in this workspace may read as mojibake on the first pass; when that happens, re-open with explicit UTF-8 before doing any review or line references [Task 1][Task 3]
- the high-risk places to inspect first in this spec family are scope boundary, tool boundary, schema/data-contract consistency, split rules, evidence traceability, and acceptance tests [Task 1]
- actual UI/prompt contracts drifted in multiple directions at once: `TravelView` consumes `sections[]`, `TravelDayFocus` consumes `title` / `badge` / `photo` / `nodes` / `footer`, `ClarifyCard` consumes `question` + structured slots, while the delivery doc used `cards[]` and the runnable prompt still used `days[]` plus `markdownArtifact` / `sources[]` [Task 1]
- `toolhub/server/python/tools/weather.py` is current-weather only, `toolhub/server/python/tools/travel.py` is a canned `get_travel_plan_template` stub, and `toolhub/server/python/tools/search.py` can expose `results[].image_url`; doc claims should not exceed those real tool capabilities [Task 1]
- the most important contradictions confirmed in these audits were T1/T2/T3 boundary ambiguity, `get_travel_plan_template` usage ambiguity, `budget{}` / `route{}` type mismatch, `day1` vs `d1` ref drift, and a 10-day example that contradicted the stated 8-14 day split rule [Task 1]
- a reliable cleanup order for similar revisions is: hard scope contradictions first, then tool boundary, then data contract, then evidence tracking, then split rules and acceptance coverage, and only after that prose polish [Task 3]
- the validated revision shape here added `TravelPayload`, explicit `evidence_refs`, stricter T1 boundaries, deterministic `base_span` split rules, and explicit acceptance scenarios while keeping the revision grounded in current real capabilities [Task 3]

## Failures and how to do differently

- symptom: the first file read is unreadable noise -> cause: Chinese markdown was read without explicit UTF-8 -> fix: rerun with `-Encoding UTF8` before reviewing content or line references [Task 1]
- symptom: a strict document review starts drifting into demo assumptions or broader product context -> cause: external knowledge is filling gaps the document never resolved -> fix: separate "the document says X" from "the document does not specify Y" and stay inside the target file when the user asked for doc-only review [Task 1]
- symptom: the doc claims cross-check alignment but the builders still do not consume its schema -> cause: prose contract drifted from the real `scenario-forms.js`, `components.js`, prompt, and ToolHub sources -> fix: compare the delivery schema to the actual component props and tool payloads before trusting any "1:1 alignment" claim [Task 1]
- symptom: example math and multi-destination rules look plausible but generate contradictory cuts -> cause: the prose split rule and examples are inconsistent -> fix: sanity-check boundary arithmetic and example inputs against the stated rule before accepting the contract [Task 1]
- symptom: revision work starts by patching the original file -> cause: the copy boundary was not treated as a hard rule -> fix: create the `_修订稿` draft first and edit only that copy [Task 3]
- symptom: revision effort gets consumed by wording polish while the spec is still internally contradictory -> cause: cosmetic cleanup happened before contract cleanup -> fix: resolve scope, contract, split-rule, and acceptance conflicts before polishing prose [Task 3]

# Task Group: Rowboat capability-state analysis and recommendation pass

scope: Read-only capability inventory of the Rowboat repo plus grounded next-step prioritization that distinguishes static code wiring from runtime-proven readiness.
applies_to: cwd=C:\Users\QYL\Desktop\rowboat; reuse_rule=safe for similar Rowboat capability-analysis and prioritization requests in this repo, but treat runtime readiness as unverified until someone actually runs the app/integrations

## Task 1: Inventory the current capability surface of the Rowboat repo

### rollout_summary_files

- rollout_summaries/2026-05-25T06-55-55-fGrb-rowboat_capability_state_analysis.md (cwd=\\?\C:\Users\QYL\Desktop\rowboat, rollout_path=C:\Users\QYL\.codex\sessions\2026\05\25\rollout-2026-05-25T14-56-05-019e5deb-33d0-7b50-ad1e-c89b4952f6f5.jsonl, updated_at=2026-05-26T03:55:44+00:00, thread_id=019e5deb-33d0-7b50-ad1e-c89b4952f6f5, grounded static repo inventory completed without edits)

### keywords

- rowboat, apps/x, knowledge graph, ~/.rowboat/knowledge, main.ts, builtin-tools.ts, ipc.ts, live-note, attention, loona, google calendar, feishu, slack, composio, browser-control, Electron, Next.js

## Task 2: Turn the inventory into a product-priority recommendation

### rollout_summary_files

- rollout_summaries/2026-05-25T06-55-55-fGrb-rowboat_capability_state_analysis.md (cwd=\\?\C:\Users\QYL\Desktop\rowboat, rollout_path=C:\Users\QYL\.codex\sessions\2026\05\25\rollout-2026-05-25T14-56-05-019e5deb-33d0-7b50-ad1e-c89b4952f6f5.jsonl, updated_at=2026-05-26T03:55:44+00:00, thread_id=019e5deb-33d0-7b50-ad1e-c89b4952f6f5, follow-up prioritization stayed grounded in the capability inventory)

### keywords

- 有什么建议吗, runtime checklist, calendar attention, loona, tts, live notes, product narrative, static vs runtime proven, dirty worktree

## User preferences

- when the user asks "/goal 梳理这个项目的目前能力现状" -> they want a grounded inventory of current capabilities, not an implementation plan or code changes [Task 1]
- because the request was for analysis, future similar asks should default to read-only repo evidence first [Task 1]
- when the user follows up with "有什么建议吗" -> shift from raw inventory to prioritization guidance based on the evidence already gathered, not another audit dump [Task 2]

## Reusable knowledge

- `apps/x` is the main product spine: Electron + renderer + core/shared IPC, with the richest product capability surface concentrated there [Task 1]
- Rowboat’s local memory model centers on `~/.rowboat/knowledge` Markdown notes, and the knowledge graph is explicitly separated from live service state [Task 1]
- `apps/x/apps/main/src/main.ts` initializes Gmail sync, Calendar sync, Fireflies, Granola, Feishu health/sync, graph builder, inline tasks, agent notes, calendar notifications, live-note scheduler/event processor, and proactive attention at startup [Task 1]
- shared IPC exposes `workspace:*`, `runs:*`, `voice:*`, `live-note:*`, `attention:*`, and `browser:*`; built-in tools include workspace ops, search/parse, MCP, browser-control, Google Calendar, web search, save-to-memory, Composio, run-live-note-agent, and notify-user [Task 1]
- live-note supports `manual | cron | window | event` triggers, proactive attention polls Google Calendar, and Loona is an experience mode on existing runs rather than a separate agent [Task 1]
- `apps/x/tests` already covers Loona, attention, KG, Feishu, KB-resolve, and related surfaces, so there is a meaningful regression bed even though runtime proof was not gathered in this pass [Task 1]
- the shortest path to a convincing demo is a closed loop: Google Calendar authorization -> proactive attention -> Loona display -> TTS -> Live Notes persistence [Task 2]
- for this repo, a stronger product narrative is "local-first desktop AI coworker with persistent Markdown memory, proactive reminders, voice, and action-taking," and Google Calendar is the most natural first proactive source; Slack/Feishu/Composio/MCP are later or more conditional extensions [Task 2]

## Failures and how to do differently

- symptom: a broad repo scan times out early -> cause: recursive file reading was too wide -> fix: start with `rg --files` and narrow file reads first in this repo [Task 1]
- symptom: a capability inventory sounds more certain than the evidence supports -> cause: static code wiring was flattened into runtime readiness -> fix: explicitly separate "wired in code" from "proven in runtime" and build a runtime checklist before calling features ready [Task 1][Task 2]
