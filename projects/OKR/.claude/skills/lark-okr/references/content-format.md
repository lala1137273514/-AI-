# OKR 富文本 Block JSON 规范

飞书 OKR 的 Objective / KR 内容字段（`content`）、进展记录正文均为 Block JSON，不是纯文本。

## 格式结构

```json
{
  "blocks": [
    {
      "block_element_type": "paragraph",
      "paragraph": {
        "elements": [
          {
            "paragraph_element_type": "textRun",
            "text_run": {
              "text": "这里是正文内容",
              "style": {}
            }
          }
        ]
      }
    }
  ]
}
```

- 一个 blocks 数组对应多个段落
- 每个 paragraph 有一或多个 elements
- element 类型主要是 `textRun`，也可能有 `docsLink`、`person` 等
- 读取时只取 `textRun.text`，其他类型跳过或用占位符

## 使用 blocks.py

```bash
# 解析：block JSON → 纯文本（传 JSON 字符串）
echo '<block_json>' | python scripts/blocks.py parse

# 或直接在 Python 里调用
from scripts.blocks import parse_blocks, build_blocks

text = parse_blocks(content_json_str)   # str -> str
json_str = build_blocks(text)           # str -> str（P2 写回时用）
```

## 写回格式（P2 起）

构造进展记录正文时，用 `build_blocks(text)` 把纯文本转回 block JSON，再传给 `+progress-create` 的 content 参数。
