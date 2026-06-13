thread_id: 019e5deb-33d0-7b50-ad1e-c89b4952f6f5
updated_at: 2026-05-26T03:55:44+00:00
rollout_path: C:\Users\QYL\.codex\sessions\2026\05\25\rollout-2026-05-25T14-56-05-019e5deb-33d0-7b50-ad1e-c89b4952f6f5.jsonl
cwd: \\?\C:\Users\QYL\Desktop\rowboat

# Rowboat capability-state analysis and recommendation pass

Rollout context: The user asked in Chinese to "梳理这个项目的目前能力现状" for the Rowboat workspace at `C:\Users\QYL\Desktop\rowboat`. The assistant performed a read-only analysis, explicitly avoided code edits, and used existing docs/ code to map the current capability surface. It also noticed the workspace was dirty (`.gitignore`, `CLAUDE.md`, and a few untracked files) and did not touch them.

## Task 1: Analyze the current capability state of the Rowboat repo

Outcome: success

Preference signals:

- when the user said `/goal 梳理这个项目的目前能力现状`, that indicates they want a grounded inventory of current capabilities, not a fix or implementation plan.
- the user did not ask for edits, so the assistant treated the task as read-only analysis; future similar requests should default to static repo evidence first.

Key steps:

- read the repo-level README and `docs/capability-map.md` as orientation, but treated them as evidence to re-check rather than as authoritative truth.
- inspected `apps/x/package.json`, `apps/x/apps/main/src/main.ts`, `apps/x/packages/shared/src/ipc.ts`, `apps/x/packages/core/src/application/lib/builtin-tools.ts`, `apps/x/packages/core/src/knowledge/README.md`, `apps/x/packages/core/src/attention/service.ts`, `apps/x/packages/core/src/voice/voice.ts`, and Loona-related renderer files.
- used `rg --files` to locate the relevant app surfaces and tests, then searched for capability anchors such as `workspace:*`, `live-note:*`, `attention:*`, `browser:*`, `voice:*`, `Composio`, `MCP`, `google-calendar`, `slack`, `lark-cli`, and `Loona`.
- checked that `apps/x` is the main desktop app, while `apps/rowboat`, `apps/rowboatx`, `apps/cli`, and `apps/python-sdk` are supporting/adjacent surfaces rather than the primary product spine.

Failures and how to do differently:

- the first recursive lesson-file search timed out; the assistant pivoted to `rg --files` and narrower reads. Future similar repo scans should start with `rg --files` / targeted file reads instead of broad recursive `Get-Content` searches.
- no runtime build/dev validation was performed, so capability status is static-code-backed, not live-proven. Future similar analyses should clearly separate "wired in code" from "proven in runtime."

Reusable knowledge:

- `apps/x` is the main capability hub: Electron + renderer + core/shared IPC, with the richest product functionality concentrated there.
- the local memory model is centered on `~/.rowboat/knowledge` and Markdown notes; the knowledge graph is explicitly not the same thing as live service state.
- `main.ts` initializes multiple subsystems at startup, including Gmail sync, Calendar sync, Fireflies, Granola, Feishu health/sync, graph builder, inline tasks, agent notes, calendar notifications, live-note scheduler/event processor, and proactive attention.
- the repo already has explicit evidence for a live-note subsystem with `manual | cron | window | event` triggers, proactive attention via Google Calendar polling, and Loona as an experience mode on existing runs rather than a separate agent.
- `apps/x/tests` contains a significant static regression surface, including Loona, attention, KG, Feishu, and KB-resolve tests.

References:

- [1] `README.md` states Rowboat is an "Open-source AI coworker that turns work into a knowledge graph and acts on it," and documents Google setup, voice input/output, web search, external tools, and local workspace additions.
- [2] `apps/x/packages/core/src/knowledge/README.md` defines the knowledge graph surface (`People`, `Organizations`, `Projects`, `Topics`, `Meetings`) and explicitly separates it from live integration state.
- [3] `apps/x/apps/main/src/main.ts` imports and initializes the major services at startup: `initGmailSync`, `initCalendarSync`, `initFirefliesSync`, `initGranolaSync`, `initFeishuHealth`, `initFeishuSync`, `initGraphBuilder`, `initInlineTasks`, `initAgentNotes`, `initCalendarNotifications`, `initAgentNotesArchive`, `initAgentNotesConflict`, `initLiveNoteScheduler`, `initLiveNoteEventProcessor`, and `initAttentionService`.
- [4] `apps/x/packages/shared/src/ipc.ts` exposes the capability channels for `workspace:*`, `runs:*`, `voice:*`, `live-note:*`, `attention:*`, and `browser:*`.
- [5] `apps/x/packages/core/src/application/lib/builtin-tools.ts` contains the agent-facing capability set: workspace ops, search, parse, MCP, browser-control, Google Calendar, web search, save-to-memory, Composio, run-live-note-agent, and notify-user.
- [6] `apps/x/packages/core/src/attention/service.ts` shows proactive attention is enabled by env flag, polls Google Calendar, and emits attention events / cold-start summaries.
- [7] `apps/x/packages/core/src/voice/voice.ts` shows DashScope is preferred when configured; otherwise ElevenLabs/Rowboat proxy is used, so TTS availability is configuration-dependent.
- [8] `.omx/wiki/loona-mode-uses-experience-mode-not-separate-agent.md` records the decision that Loona is an experience mode on the existing run schema, not a standalone agent.
- [9] `apps/x/ANALYTICS.md` documents PostHog identity and `llm_usage` instrumentation, which means the app has analytics plumbing for usage, sign-in, and sign-out events.
- [10] `apps/x/tests/loona/four-layer-flow.test.tsx`, `apps/x/tests/attention/*`, and other test files show there is a non-trivial regression suite for the product’s advanced surfaces.

## Task 2: Give follow-up suggestions for the capability state

Outcome: success

Preference signals:

- when the user followed up with "有什么建议吗", they were asking for prioritization guidance based on the capability inventory, not another raw audit.

Key steps:

- distilled the analysis into a practical recommendation order rather than re-listing every subsystem.
- emphasized a single demo-worthy closed loop: Google Calendar authorization -> proactive attention -> Loona display -> TTS -> Live Notes persistence.
- framed the recommendation around runtime-proofing and product simplification rather than adding more long-tail features.

Failures and how to do differently:

- the suggestion pass leaned on static evidence only; future recommendation passes should call out which items still need runtime proof before being treated as product-ready.

Reusable knowledge:

- for this repo, a strong product narrative is "local-first desktop AI coworker with persistent Markdown memory, proactive reminders, voice, and action-taking," not a generic chat app.
- the shortest path to a convincing demo is to tighten the existing Loona / Attention / Live Notes loop instead of broadening surface area.
- capability prioritization should treat Google Calendar as the most natural proactive source, with Slack/Feishu/Composio/MCP as later or more conditional extensions.

References:

- [1] The assistant’s recommendation was to focus on `apps/x`, build a runtime checklist, repair Loona/TTS gaps, then close the Calendar Attention + Live Notes demo loop.
- [2] The workspace currently had dirty/untracked files, and the assistant explicitly avoided touching them during analysis.
