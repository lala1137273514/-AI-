# Lessons

- CC persona is intentionally sharp and tsundere. Positive state changes should reduce volatility only within a narrow boundary; they must not make CC warm, flattering, servile, or assistant-like.
- In Rowboat Loona work, any non-`artifact-card` tool call should end through a mandatory artifact-card presentation layer: convert real tool results, failures, denials, and auth errors into shared cards, then give only short persona-filtered spoken/bridge text.
- In Rowboat Loona/DashScope-style OpenAI-compatible models, forced `tool_choice` for `artifact-card` must disable thinking with providerOptions (`"openai-compatible": { "enable_thinking": false }`); otherwise providers can reject required/object tool_choice in thinking mode.
