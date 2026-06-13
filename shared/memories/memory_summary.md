v1

## User Profile

The user works in a Windows local-agent setup and wants real evidence before conclusions. They repeatedly split tasks into clear modes: strict contract-following for recurring automations, read-only analysis when they ask for audits or inventories, and copy-before-edit when they want a safer revision path. They dislike improvised side routes, fake completion, and polished prose that hides missing runtime proof. For document and form work, they often want an objective first pass that diagnoses what is missing before anyone starts rewriting. For communication drafts, they want something they can paste directly, then tighten with one or two precise follow-ups rather than a long exploration.

## User preferences

- When the user names an "only authoritative" flow, follow that contract exactly and do not invent alternate collection, repair, or publish paths.
- For `daily-feishu-retro`, treat `analysis_payload` as the primary evidence set, treat images as first-class evidence, and treat success as incomplete until `scripts/publish_review.py` runs and the bound chat shows the final link.
- In Feishu collection runs, ignore bot/system noise and the literal trigger `review` when the contract says they are noise.
- If `analysis_payload` was never produced, do not synthesize, publish, or imply the retro was completed.
- When the user asks "帮我客观研究一下..." or otherwise asks for analysis first, start with an objective audit instead of immediate rewriting.
- When the user asks for direct-to-forward copy, return paste-ready wording, not abstract messaging advice.
- If the user asks to add “使用 AI 过程中的问题”, make sure the draft explicitly covers AI-use blockers, not only desired use cases.
- If the user asks for emoji in group copy, keep them light and functional rather than decorative.
- When the user says "只读，不要修改任何文件" or "只看这个文档，不需要参考 demo", stay read-only, evidence-based, and doc-scoped.
- For strict spec reviews, bias toward "要挑刺，要怀疑，宁可多报" and return a structured issue list with evidence.
- When the user asks for "已验证 OK 的点", preserve confirmed-good items separately from defects.
- When asked to revise a reviewed document, default to copy-before-edit and keep the original untouched.
- If persona/session persistence cannot really write to disk, say that plainly instead of implying memory was saved.

## General Tips

- Windows/PowerShell is the normal context; for Chinese markdown that reads as mojibake, retry with explicit UTF-8 before analysis.
- Treat saved bindings, cached state, or leftover shim files as hints, not proof that the current run can execute.
- For blocked automations, verify the real executable path first; a leftover `lark-cli.cmd` is not enough if its target `...\@larksuiteoapi\lark-cli\bin\lark-cli.js` is missing. If collection cannot run, stop and record the blocker instead of faking downstream completion.
- Some shells here do not expose `CODEX_HOME`; absolute paths are safer for automation-memory inspection.
- In form/spec cleanup tasks, diagnose the gap first, then fix hard contradictions before polishing wording.
- In repo capability-analysis tasks, separate "wired in code" from "runtime proven" and call out what still needs live validation.
- For Rowboat repo scans, start with `rg --files` and narrow reads instead of broad recursive content searches.

## What's in Memory

### daily-feishu-retro automation family across Codex worktrees

#### 2026-06-12

- Feishu retro contract runs blocked by local CLI: feishu-retro-review, daily-feishu-retro, analysis_payload, collect_inputs.py, run_cli, lark-cli, FileNotFoundError, WinError 2, automation memory, CODEX_HOME
  - desc: Search here first for scheduled Feishu retro runs, contract-order questions, or repeated collection failures across Codex worktrees tied to `C:\Users\QYL\.codex\automations\daily-feishu-retro\memory.md`.
  - learnings: the newest repeat on 2026-06-12 still died before `analysis_payload`; stale binding still looked healthy, `Get-Command lark-cli,lark-cli.cmd,lark` found nothing usable, `npm list -g --depth=0` was empty, and absolute paths were safer because `CODEX_HOME` was missing.

### C:\Users\QYL\Documents\Codex\2026-06-12\ai-coach-ai-vibe-coding-ai

#### 2026-06-12

- AI Coach form audit and group-post copy: AI Coach, requirement collection form, objective review, group announcement, 使用 AI 过程中的问题, emoji, sensitive info
  - desc: Search here first for Chinese form-audit tasks that become group-announcement drafting, especially when the user wants analysis first and then paste-ready copy for a chat group.
  - learnings: the winning sequence was audit first, then direct-to-forward copy, then one tight pass to add AI-usage blockers and restrained emoji without making the announcement feel like marketing.

### C:\Users\QYL + C:\Users\QYL\Desktop\loona-workbench

#### 2026-05-26

- Chinese travel-planning spec audits and safe revision flow: 旅行规划_交付稿v1.md, TravelView, TravelDayFocus, ClarifyCard, sections[], cards[], days[], get_weather, get_travel_plan_template, copy-before-edit
  - desc: Search here first for Chinese spec audits, doc-only review requests, prompt/UI/tool contract drift, or follow-up revision flows that must preserve the original file.
  - learnings: start with UTF-8, compare the doc against real builders/tools before trusting prose claims, keep a separate "已验证 OK 的点" section, and if revision is requested, fix contract contradictions on a draft copy first.

### C:\Users\QYL\Desktop\rowboat

#### 2026-05-26

- Rowboat capability-state analysis and prioritization: rowboat, apps/x, ~/.rowboat/knowledge, live-note, attention, loona, google calendar, builtin-tools, runtime checklist
  - desc: Search here first for grounded capability inventories of Rowboat or for recommendation passes that need to turn a repo scan into a product-priority order without code edits.
  - learnings: `apps/x` is the product spine, the strongest demo loop is Calendar attention -> Loona -> TTS -> Live Notes, and all capability claims in this memory are static-code-backed unless runtime proof is added later.

### Older Memory Topics

- None currently; all supported high-signal topics are covered in the recent active window.
