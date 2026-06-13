# Multimodal Rules

Process same-day chat content as a multimodal evidence set, not as a transcript that must be flattened into text first.

## Model-Facing Contract

- The model-facing payload is `analysis_payload`.
- `analysis_payload` should be treated as the first source for analysis because it separates text evidence, image evidence, and other resources into explicit items.
- Raw collected `items` can still be used as backup context, but the main synthesis should be built from `analysis_payload`.

## Text

- `text` and `post` messages are usable directly.
- Text evidence should keep its original time, sender, and message-level context.

## Images

- Images are first-class evidence.
- A downloaded image with a valid `file_path` should still enter analysis even if no OCR text was extracted.
- The model should use `file_path`, `context_before`, and `context_after` together to judge whether the image matters for the review.
- OCR is only a fallback, not the main path.

## Audio

- Audio can use transcription when available.
- If transcription is missing but the resource is available, keep the resource in evidence rather than treating it as a hard parse failure.

## Files and Links

- Feishu doc links should be resolved and fetched when possible.
- Attachments or files should be analyzed when a readable text path exists, or preserved as evidence when a later model/tool step can inspect them.

## Failure Policy

- A single failed item must not fail the whole review.
- `resource_failed` means the resource could not be prepared.
- `analysis_skipped` means the resource is available but has not yet been interpreted by the model.
- The final review must mention `部分内容解析失败` only when a resource truly failed to prepare or an important item could not be incorporated.
