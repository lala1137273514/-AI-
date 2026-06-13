"""
blocks.py — 飞书 OKR 富文本 Block JSON 双向转换

用法（CLI）：
  echo '<json>' | python blocks.py parse   -> 纯文本
  python blocks.py build "文本内容"        -> block JSON 字符串
"""

import json
import sys


def parse_blocks(content: str | dict) -> str:
    """Block JSON（str 或 dict）-> 可读纯文本。"""
    if isinstance(content, str):
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return content  # 已经是纯文本，直接返回
    else:
        data = content

    if not isinstance(data, dict):
        return str(data)

    blocks = data.get("blocks", [])
    lines = []
    for block in blocks:
        btype = block.get("block_element_type", "")
        if btype == "paragraph":
            para = block.get("paragraph", {})
            elements = para.get("elements", [])
            line_parts = []
            for el in elements:
                etype = el.get("paragraph_element_type", "")
                if etype == "textRun":
                    line_parts.append(el.get("text_run", {}).get("text", ""))
                elif etype == "docsLink":
                    url = el.get("docs_link", {}).get("url", "")
                    text = el.get("docs_link", {}).get("title", url)
                    line_parts.append(f"[{text}]({url})" if url else "")
                elif etype == "person":
                    line_parts.append(f"@{el.get('person', {}).get('open_id', '')}")
                # 其他类型忽略
            lines.append("".join(line_parts))
        # 其他 block 类型（heading、bullet 等）可后续扩展
    return "\n".join(lines).strip()


def build_blocks(text: str) -> str:
    """纯文本 -> Block JSON 字符串（按换行符分段落）。"""
    paragraphs = text.split("\n")
    blocks = []
    for para in paragraphs:
        blocks.append({
            "block_element_type": "paragraph",
            "paragraph": {
                "elements": [
                    {
                        "paragraph_element_type": "textRun",
                        "text_run": {"text": para, "style": {}},
                    }
                ]
            },
        })
    return json.dumps({"blocks": blocks}, ensure_ascii=False)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: blocks.py parse | blocks.py build <text>", file=sys.stderr)
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "parse":
        raw = sys.stdin.read().strip()
        print(parse_blocks(raw))
    elif mode == "build":
        text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else sys.stdin.read().strip()
        print(build_blocks(text))
    else:
        print(f"未知模式: {mode}", file=sys.stderr)
        sys.exit(1)
