# State Schema

Store runtime state in a global JSON file outside the skill folder so upgrades do not erase bindings or daily document mappings.

## JSON Shape

```json
{
  "binding": {
    "chat_id": "",
    "chat_name": "工作复盘"
  },
  "daily_docs": {
    "2026-03-31": {
      "doc_id": "",
      "doc_url": ""
    }
  },
  "last_review": {
    "date": "",
    "status": "",
    "message": "",
    "updated_at": ""
  }
}
```

## Fields

- `binding.chat_id`: the single bound Feishu chat id
- `binding.chat_name`: defaults to `工作复盘`
- `daily_docs[YYYY-MM-DD].doc_id`: today's review document id
- `daily_docs[YYYY-MM-DD].doc_url`: today's review document url
- `last_review.date`: last processed date
- `last_review.status`: `ok` or `error`
- `last_review.message`: short execution summary
- `last_review.updated_at`: ISO timestamp

## Behavior

- First run creates the `工作复盘` chat if binding is empty.
- Same-day reruns overwrite the same document.
- The skill should never depend on skill-folder state for persistence.
