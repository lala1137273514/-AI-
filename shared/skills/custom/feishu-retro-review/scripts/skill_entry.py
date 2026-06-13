from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
STATE_ROOT = Path.home() / ".codex" / "state" / "feishu-retro-review"
STATE_PATH = STATE_ROOT / "state.json"
RESOURCE_ROOT = STATE_ROOT / "resources"
DEFAULT_CHAT_NAME = "工作复盘"
NOISE_TEXTS = {"review", "今日日报复盘已完成", "今日日报复盘已完成："}
IGNORED_TYPES = {"system", "sticker", "interactive", "share_chat", "share_user"}


def today_str() -> str:
    return date.today().isoformat()


def _now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _default_state() -> dict[str, Any]:
    return {
        "binding": {"chat_id": "", "chat_name": DEFAULT_CHAT_NAME},
        "daily_docs": {},
        "last_review": {"date": "", "status": "", "message": "", "updated_at": ""},
    }


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return _default_state()
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict[str, Any]) -> None:
    STATE_ROOT.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def print_json(data: dict[str, Any]) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    try:
        sys.stdout.write(text)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(text.encode("utf-8"))


def run_cli(args: list[str], *, cwd: str | Path | None = None, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    cli_binary = shutil.which("lark-cli.cmd") or shutil.which("lark-cli") or "lark-cli"
    completed = subprocess.run(
        [cli_binary, *args],
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(cwd) if cwd is not None else None,
        check=False,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        stdout = completed.stdout.strip()
        detail = stderr or stdout or f"exit={completed.returncode}"
        raise RuntimeError(f"lark-cli {' '.join(args)} failed: {detail}")
    return completed


def _parse_json_output(stdout: str) -> dict[str, Any]:
    stdout = (stdout or "").strip()
    if not stdout:
        return {}
    return json.loads(stdout)


def _data_container(payload: dict[str, Any]) -> dict[str, Any]:
    data = payload.get("data")
    return data if isinstance(data, dict) else payload


def _sender_name(sender: Any) -> str:
    if isinstance(sender, dict):
        return str(sender.get("name") or sender.get("sender_name") or sender.get("id") or "未知发送者")
    if sender:
        return str(sender)
    return "未知发送者"


def _flatten_content(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, dict):
        if "text" in value and isinstance(value["text"], str):
            return _flatten_content(value["text"])
        if "image_key" in value:
            return [f"[Image: {value['image_key']}]"]
        if "file_key" in value:
            return [f"[File: {value['file_key']}]"]
        parts: list[str] = []
        for item in value.values():
            parts.extend(_flatten_content(item))
        return parts
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            parts.extend(_flatten_content(item))
        return parts
    return [str(value)]


def normalize_message_content(raw: Any) -> str:
    if raw is None:
        return ""
    if isinstance(raw, (dict, list)):
        return " ".join(_flatten_content(raw)).strip()
    if not isinstance(raw, str):
        return str(raw)
    text = raw.strip()
    if not text:
        return ""
    if text.startswith("{") or text.startswith("["):
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return text
        return " ".join(_flatten_content(payload)).strip()
    return text


def extract_file_key(raw: Any) -> str:
    text = raw if isinstance(raw, str) else json.dumps(raw, ensure_ascii=False)
    patterns = [
        r'"(?:image_key|file_key)"\s*:\s*"([^"]+)"',
        r"\[(?:Image|File):\s*([^\]]+)\]",
        r"\b((?:img|file)[A-Za-z0-9_-]+)\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return ""


def _safe_resource_name(message_id: str, file_key: str) -> str:
    raw = f"{message_id}_{file_key}"
    return re.sub(r"[^A-Za-z0-9._-]+", "_", raw)


def download_message_resource(*, message_id: str, file_key: str, resource_type: str = "image") -> Path:
    RESOURCE_ROOT.mkdir(parents=True, exist_ok=True)
    output_name = _safe_resource_name(message_id, file_key)
    run_cli(
        [
            "im",
            "+messages-resources-download",
            "--message-id",
            message_id,
            "--file-key",
            file_key,
            "--type",
            resource_type,
            "--output",
            output_name,
            "--as",
            "user",
        ],
        cwd=RESOURCE_ROOT,
    )
    return (RESOURCE_ROOT / output_name).resolve()


def try_extract_text_from_file(path: str | Path) -> str:
    file_path = Path(path)
    if not file_path.exists():
        return ""
    suffix = file_path.suffix.lower()
    if suffix in {".txt", ".md", ".markdown", ".json", ".csv", ".log"}:
        for encoding in ("utf-8", "utf-8-sig", "gb18030"):
            try:
                return file_path.read_text(encoding=encoding).strip()
            except UnicodeDecodeError:
                continue
    return ""


def _get_neighbor_text(messages: list[dict[str, Any]], index: int, step: int) -> str:
    cursor = index + step
    while 0 <= cursor < len(messages):
        message = messages[cursor]
        msg_type = str(message.get("msg_type") or "text")
        if msg_type in {"text", "post"}:
            text = normalize_message_content(message.get("content", ""))
            if text:
                return text
        cursor += step
    return ""


def should_ignore_message(message: dict[str, Any]) -> bool:
    if message.get("deleted"):
        return True
    msg_type = str(message.get("msg_type") or "text")
    if msg_type in IGNORED_TYPES:
        return True
    normalized = normalize_message_content(message.get("content", ""))
    compact = normalized.replace(" ", "")
    lowered = normalized.lower()
    if lowered == "review":
        return True
    if compact in NOISE_TEXTS or compact.startswith("今日日报复盘已完成："):
        return True
    return False


def ensure_binding(create_if_missing: bool = True) -> dict[str, Any]:
    state = load_state()
    binding = state.setdefault("binding", {"chat_id": "", "chat_name": DEFAULT_CHAT_NAME})
    chat_id = binding.get("chat_id") or ""
    if chat_id:
        return state

    chat_name = str(binding.get("chat_name") or DEFAULT_CHAT_NAME)
    try:
        search = run_cli(["im", "+chat-search", "--query", chat_name, "--format", "json", "--as", "user"])
        search_payload = _data_container(_parse_json_output(search.stdout))
        chats = search_payload.get("items") or search_payload.get("chats") or []
        for chat in chats:
            if str(chat.get("name") or chat.get("chat_name") or "") == chat_name:
                binding["chat_id"] = str(chat.get("chat_id") or chat.get("id") or "")
                if binding["chat_id"]:
                    save_state(state)
                    return state
    except Exception:
        if not create_if_missing:
            raise

    if not create_if_missing:
        raise RuntimeError("No bound chat is configured for feishu-retro-review")

    created = run_cli(["im", "+chat-create", "--name", chat_name, "--format", "json"])
    created_payload = _data_container(_parse_json_output(created.stdout))
    binding["chat_id"] = str(created_payload.get("chat_id") or "")
    binding["chat_name"] = chat_name
    save_state(state)
    return state


def quick_check() -> dict[str, Any]:
    state = ensure_binding()
    binding = state.get("binding", {})
    return {
        "ok": bool(binding.get("chat_id")),
        "binding": binding,
        "daily_doc_count": len(state.get("daily_docs", {})),
    }


def fetch_day_messages(chat_id: str, day: str) -> list[dict[str, Any]]:
    start = day
    end = (date.fromisoformat(day) + timedelta(days=1)).isoformat()
    page_token = ""
    messages: list[dict[str, Any]] = []

    while True:
        args = [
            "im",
            "+chat-messages-list",
            "--chat-id",
            chat_id,
            "--start",
            start,
            "--end",
            end,
            "--sort",
            "asc",
            "--page-size",
            "50",
            "--format",
            "json",
            "--as",
            "user",
        ]
        if page_token:
            args.extend(["--page-token", page_token])
        payload = _data_container(_parse_json_output(run_cli(args).stdout))
        messages.extend(payload.get("messages") or payload.get("items") or [])
        has_more = bool(payload.get("has_more"))
        page_token = str(payload.get("page_token") or payload.get("next_page_token") or "")
        if not has_more or not page_token:
            break
    return messages


def collect_inputs_for_day(state: dict[str, Any], day: str) -> dict[str, Any]:
    binding = state.get("binding") or {}
    chat_id = str(binding.get("chat_id") or "")
    chat_name = str(binding.get("chat_name") or DEFAULT_CHAT_NAME)
    raw_messages = fetch_day_messages(chat_id, day)
    messages = [message for message in raw_messages if not should_ignore_message(message)]
    items: list[dict[str, Any]] = []

    for index, message in enumerate(messages):
        message_id = str(message.get("message_id") or "")
        create_time = str(message.get("create_time") or "")
        sender = _sender_name(message.get("sender"))
        msg_type = str(message.get("msg_type") or "text")
        normalized = normalize_message_content(message.get("content", ""))
        item: dict[str, Any] = {
            "message_id": message_id,
            "create_time": create_time,
            "sender": sender,
            "msg_type": msg_type,
        }

        if msg_type in {"text", "post"}:
            item.update(
                {
                    "text": normalized,
                    "normalized_text": normalized,
                    "parse_failed": False,
                }
            )
            items.append(item)
            continue

        file_key = extract_file_key(message.get("content", ""))
        context_before = _get_neighbor_text(messages, index, -1)
        context_after = _get_neighbor_text(messages, index, 1)
        item.update(
            {
                "text": "",
                "normalized_text": "",
                "context_before": context_before,
                "context_after": context_after,
                "resource_ready": False,
                "resource_failed": False,
                "analysis_skipped": False,
                "analysis_required": msg_type == "image",
                "parse_failed": False,
            }
        )
        resource_type = "image" if msg_type == "image" else "file"
        try:
            if not file_key:
                raise RuntimeError("missing file key")
            file_path = download_message_resource(message_id=message_id, file_key=file_key, resource_type=resource_type)
            extracted = try_extract_text_from_file(file_path).strip()
            item.update(
                {
                    "file_path": str(file_path),
                    "resource_ready": True,
                    "resource_failed": False,
                    "analysis_skipped": not bool(extracted),
                    "text": extracted,
                    "normalized_text": extracted,
                    "parse_failed": False,
                }
            )
        except Exception as exc:
            item.update(
                {
                    "resource_ready": False,
                    "resource_failed": True,
                    "analysis_skipped": False,
                    "parse_failed": True,
                    "normalized_text": f"[{msg_type} download/extract failed: {exc}]",
                }
            )
        items.append(item)

    return {
        "date": day,
        "chat_id": chat_id,
        "chat_name": chat_name,
        "items": items,
        "has_partial_failures": any(bool(item.get("parse_failed")) for item in items),
    }


def build_analysis_payload(inputs: dict[str, Any]) -> dict[str, Any]:
    counts = {"text": 0, "image": 0, "other": 0}
    evidence: list[dict[str, Any]] = []

    for item in inputs.get("items", []):
        msg_type = str(item.get("msg_type") or "text")
        base = {
            "message_id": item.get("message_id", ""),
            "create_time": item.get("create_time", ""),
            "sender": item.get("sender", ""),
        }
        if msg_type in {"text", "post"}:
            text = str(item.get("text") or item.get("normalized_text") or "").strip()
            if not text:
                continue
            counts["text"] += 1
            evidence.append({"kind": "text", "text": text, **base})
            continue

        if msg_type == "image":
            counts["image"] += 1
            evidence.append(
                {
                    "kind": "image",
                    "file_path": item.get("file_path", ""),
                    "text": item.get("text", ""),
                    "context_before": item.get("context_before", ""),
                    "context_after": item.get("context_after", ""),
                    "resource_ready": bool(item.get("resource_ready")),
                    "resource_failed": bool(item.get("resource_failed")),
                    "analysis_skipped": bool(item.get("analysis_skipped")),
                    "analysis_required": bool(item.get("resource_ready")),
                    **base,
                }
            )
            continue

        counts["other"] += 1
        evidence.append(
            {
                "kind": "other",
                "text": item.get("text") or item.get("normalized_text") or "",
                "file_path": item.get("file_path", ""),
                "resource_ready": bool(item.get("resource_ready")),
                "resource_failed": bool(item.get("resource_failed")),
                **base,
            }
        )

    return {
        "date": inputs.get("date", ""),
        "chat_id": inputs.get("chat_id", ""),
        "chat_name": inputs.get("chat_name", ""),
        "evidence_counts": counts,
        "evidence": evidence,
    }


def generate_review_markdown(inputs: dict[str, Any], analysis_payload: dict[str, Any]) -> str:
    lines = [
        f"# 工作复盘 - {inputs.get('date', '')}",
        "",
        "## 今日概览",
    ]
    counts = analysis_payload.get("evidence_counts", {})
    lines.append(
        f"今天已收集 {counts.get('text', 0)} 条文本证据、{counts.get('image', 0)} 条图片证据和 {counts.get('other', 0)} 条其他资源。"
    )
    pending_images = [
        item
        for item in analysis_payload.get("evidence", [])
        if item.get("kind") == "image" and item.get("analysis_required")
    ]
    if pending_images:
        lines.append("当前图片证据已经就位，待进一步分析后再纳入正式复盘正文。")
    else:
        lines.append("当前版本可以直接基于现有文本证据进行复盘分析。")
    return "\n".join(lines).strip() + "\n"


def _time_hint(value: str) -> str:
    match = re.search(r"(\d{2}:\d{2})", value)
    return match.group(1) if match else value


def _theme_for_text(text: str) -> str:
    lowered = text.lower()
    if "aip" in lowered:
        return "AIP 中转站"
    if "cc" in lowered:
        return "cc 配置"
    if "dm" in lowered:
        return "DM 文档学习"
    if any(token in text for token in ("飞书复盘", "复盘输出", "复盘内容", "提示词", "skill", "PRD")):
        return "飞书复盘优化"
    if "会议" in text:
        return "会议安排"
    return "今日事项"


def _status_for_text(text: str) -> tuple[str, str]:
    if any(token in text for token in ("出了问题", "问题", "异常", "阻塞")):
        return "待处理", "🚧"
    if any(token in text for token in ("确定", "明确", "收口")):
        return "已明确", "🚀"
    if any(token in text for token in ("测试", "优化", "学习", "配置")):
        return "进行中", "🔄"
    return "已推进", "🚀"


def _text_records(inputs: dict[str, Any]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for item in inputs.get("items", []):
        text = str(item.get("normalized_text") or item.get("text") or "").strip()
        if not text or item.get("parse_failed"):
            continue
        records.append(
            {
                "time": str(item.get("create_time", "")),
                "sender": str(item.get("sender", "")),
                "text": text,
                "theme": _theme_for_text(text),
            }
        )
    return records


def _ranked_themes(records: list[dict[str, str]]) -> list[str]:
    counts: dict[str, int] = {}
    for record in records:
        theme = record["theme"]
        if theme == "会议安排":
            continue
        counts[theme] = counts.get(theme, 0) + 1
    return [theme for theme, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))]


def _status_cards(records: list[dict[str, str]]) -> list[tuple[str, str, str, str, str]]:
    cards: list[tuple[str, str, str, str, str]] = []
    for theme in _ranked_themes(records):
        theme_records = [record for record in records if record["theme"] == theme]
        latest = theme_records[-1]
        status, emoji = _status_for_text(latest["text"])
        cards.append((theme, status, emoji, _time_hint(latest["time"]), latest["sender"]))
    if not cards and records:
        latest = records[-1]
        status, emoji = _status_for_text(latest["text"])
        cards.append(("今日事项", status, emoji, _time_hint(latest["time"]), latest["sender"]))
    return cards


def render_review_markdown(inputs: dict[str, Any]) -> str:
    date_value = str(inputs.get("date") or today_str())
    records = _text_records(inputs)
    themes = _ranked_themes(records)
    timeline_records = [record for record in records if record["theme"] != "会议安排"] or records
    timeline_records = timeline_records[:6]

    if themes:
        overview = f"关键内容主要集中在：{'、'.join(themes[:4])}。"
    else:
        overview = "今天主要完成了工作记录整理与后续动作梳理。"
    if any("测试" in record["text"] for record in records):
        overview += " 当天记录显示当前工作仍处在验证与收口阶段。"
    else:
        overview += " 当前记录更多体现为结构梳理和方向明确。"

    lines = [
        f"# 工作复盘 - {date_value}",
        "",
        "## 今日概览",
        '<callout emoji="📝" background-color="light-blue">',
        overview,
        "</callout>",
        "",
        "## 推进时间线",
    ]

    for record in timeline_records:
        lines.append(f"- `{_time_hint(record['time'])}` {record['text']}")

    lines.extend(
        [
            "",
            '## 当前现状 {color="blue"}',
            "### 事项状态",
        ]
    )

    for theme, status, emoji, time_hint, sender in _status_cards(records):
        lines.extend(
            [
                f'<callout emoji="{emoji}" background-color="light-blue">',
                f"**{theme}**",
                f"状态：**{status}**",
                f"最新记录：`{time_hint}` · {sender}",
                "</callout>",
            ]
        )

    lines.extend(
        [
            "",
            "### 知识沉淀",
            "- 结果性记录比计划性记录更有助于后续自动复盘，能直接提升时间线和现状判断的可信度。",
            "- 测试结果和判断标准需要在当天记录里写清，否则复盘只能看到“还在测试”，看不到真正的判断依据。",
            "",
            "### 资源与线索",
        ]
    )

    resource_lines: list[str] = []
    for record in records:
        if "http" in record["text"]:
            resource_lines.append(f"- {record['theme']} 相关线索：{record['text'].split()[-1]}")
    if not resource_lines:
        resource_lines.append("- 当前没有额外的外部资源链接沉淀。")
    lines.extend(resource_lines)

    lines.extend(
        [
            "",
            "### 阶段判断",
            "- 飞书复盘优化目前已经从方向讨论进入结构与提示词收口后的验证阶段。",
        ]
    )
    if any(record["theme"] == "AIP 中转站" for record in records):
        lines.append("- AIP 中转站已经从问题发现进入待排查阶段，需要尽快补充根因和修复动作。")
    else:
        lines.append("- 其他事项仍以信息补全和执行收口为主。")

    lines.extend(
        [
            "",
            "### 待确认项",
            "- AIP 中转站问题的具体根因和处理路径暂未明确。" if any(record["theme"] == "AIP 中转站" for record in records) else "- 仍需补充更多结果性记录来支撑更明确的阶段判断。",
            "",
            "## 下一步待办",
        ]
    )

    candidates: list[str] = []
    if any(theme == "飞书复盘优化" for theme in themes):
        candidates.append("补一轮飞书复盘闭环测试，并补充测试结果和判断标准。")
        candidates.append("把飞书复盘优化的提示词收口到可复用版本。")
    if any(theme == "AIP 中转站" for theme in themes):
        candidates.append("排查 AIP 中转站异常，确认问题范围并补充处理方案。")
    if any(theme == "cc 配置" for theme in themes):
        candidates.append("完成 cc 配置并验证当前环境是否可用。")
    if any(theme == "DM 文档学习" for theme in themes):
        candidates.append("继续整理 DM 文档学习要点，并沉淀可复用的关键结论。")
    if not candidates:
        candidates.extend(
            [
                "补充更多结果性记录，让复盘能反映真实推进。",
                "继续梳理复盘结构并补一轮闭环验证。",
                "把今天已明确的下一步动作写成更具体的执行项。",
            ]
        )

    seen: set[str] = set()
    ordered_candidates: list[str] = []
    for candidate in candidates:
        if candidate not in seen:
            seen.add(candidate)
            ordered_candidates.append(candidate)
    while len(ordered_candidates) < 3:
        ordered_candidates.append("补充当天的结果性记录与判断依据。")
        ordered_candidates = list(dict.fromkeys(ordered_candidates))
    for candidate in ordered_candidates[:5]:
        lines.append(f"- [ ] {candidate}")

    lines.extend(
        [
            "",
            "## 今日思考",
            "- 结果性记录：如果聊天里只有“今天要做什么”，自动复盘会更像计划单而不是复盘，后续需要主动补充“做到了什么、停在什么状态”。",
            "- 测试结果和判断标准：测试类工作不能只写“目前还在测试”，还要补上通过/失败依据，否则时间线能看见动作，当前现状却难以下判断。",
        ]
    )

    if len(themes) > 1:
        lines.append("- 收口顺序：先把复盘结构和提示词边界收紧，再补闭环验证，能减少技术噪音对结果判断的干扰。")

    lines.extend(["", "## 信息缺口（如有）"])
    if inputs.get("has_partial_failures"):
        lines.append("- 部分内容解析失败，当前复盘未能完整纳入所有证据。")
    else:
        lines.append("- 当前没有影响主结论的明显信息缺口。")

    return "\n".join(lines).strip() + "\n"


def downgrade_rich_markdown(markdown: str) -> str:
    markdown = re.sub(r"\s*\{color=\"[^\"]+\"\}", "", markdown)

    def replace_callout(match: re.Match[str]) -> str:
        body = match.group(1).strip()
        return body + "\n"

    return re.sub(r"<callout[^>]*>\s*(.*?)\s*</callout>", replace_callout, markdown, flags=re.DOTALL)


def markdown_fragments(markdown: str) -> list[str]:
    fragments: list[str] = []
    lines = markdown.splitlines()
    index = 0
    while index < len(lines):
        current = lines[index].strip()
        if not current:
            index += 1
            continue
        if current.startswith("<callout"):
            open_tag = current
            body: list[str] = []
            index += 1
            while index < len(lines):
                part = lines[index].strip()
                if part == "</callout>":
                    fragments.append(f"{open_tag}{' '.join(body)}</callout>")
                    break
                if part:
                    body.append(part)
                index += 1
            index += 1
            continue
        fragments.append(current)
        index += 1
    return fragments


def _arg_value(args: list[str], flag: str) -> str:
    if flag not in args:
        return ""
    position = args.index(flag)
    return args[position + 1] if position + 1 < len(args) else ""


def _extract_doc_ref(stdout: str) -> tuple[str, str]:
    payload = _parse_json_output(stdout)
    data = _data_container(payload)
    return str(data.get("doc_id") or payload.get("doc_id") or ""), str(data.get("doc_url") or payload.get("doc_url") or "")


def run_docs_cli_with_markdown(args: list[str], markdown: str) -> subprocess.CompletedProcess[str]:
    fragments = markdown_fragments(markdown)
    if not fragments:
        return run_cli([*args, "--markdown", ""])
    first = run_cli([*args, "--markdown", fragments[0]])
    if len(fragments) == 1:
        return first
    _, doc_url = _extract_doc_ref(getattr(first, "stdout", ""))
    doc_url = doc_url or _arg_value(args, "--doc")
    if not doc_url:
        return first
    for fragment in fragments[1:]:
        run_cli(["docs", "+update", "--as", "user", "--doc", doc_url, "--mode", "append", "--markdown", fragment])
    return first


def fetch_doc_markdown(doc_url: str) -> str:
    payload = _parse_json_output(run_cli(["docs", "+fetch", "--doc", doc_url, "--as", "user"]).stdout)
    data = _data_container(payload)
    return str(data.get("markdown") or data.get("content") or payload.get("markdown") or "")


def _looks_complete(markdown: str) -> bool:
    stripped = markdown.strip()
    return "## 今日概览" in stripped and len(stripped.splitlines()) > 2


def fetch_doc_markdown_with_retry(doc_url: str, *, retries: int = 3, delay_seconds: int = 2) -> str:
    last = ""
    for attempt in range(retries + 1):
        last = fetch_doc_markdown(doc_url)
        if _looks_complete(last):
            return last
        if attempt < retries:
            time.sleep(delay_seconds)
    return last


def _publish_markdown_lines(args: list[str], markdown: str) -> dict[str, Any]:
    return {"base_args": list(args), "fragments": markdown_fragments(markdown)}


def publish_review_markdown(state: dict[str, Any], day: str, markdown: str) -> dict[str, Any]:
    daily_docs = state.setdefault("daily_docs", {})
    existing = daily_docs.get(day) or {}
    doc_url = str(existing.get("doc_url") or "")
    base_args = (
        ["docs", "+update", "--as", "user", "--doc", doc_url, "--mode", "overwrite"]
        if doc_url
        else ["docs", "+create", "--as", "user", "--title", f"工作复盘 - {day}"]
    )

    published = run_docs_cli_with_markdown(base_args, markdown)
    doc_id, new_doc_url = _extract_doc_ref(getattr(published, "stdout", ""))
    doc_url = new_doc_url or doc_url

    fetched = fetch_doc_markdown_with_retry(doc_url, retries=2, delay_seconds=1) if doc_url else ""
    final_markdown = markdown
    if doc_url and not _looks_complete(fetched):
        final_markdown = downgrade_rich_markdown(markdown)
        republished = run_docs_cli_with_markdown(base_args, final_markdown)
        republished_doc_id, republished_doc_url = _extract_doc_ref(getattr(republished, "stdout", ""))
        doc_id = republished_doc_id or doc_id
        doc_url = republished_doc_url or doc_url
        _publish_markdown_lines(base_args, final_markdown)

    if doc_url:
        daily_docs[day] = {"doc_id": doc_id or existing.get("doc_id", ""), "doc_url": doc_url}
    message = f"今日日报复盘已完成：{doc_url}" if doc_url else "今日日报复盘已完成"

    binding = state.get("binding") or {}
    chat_id = str(binding.get("chat_id") or "")
    notification_error: Exception | None = None
    if chat_id and doc_url:
        try:
            run_cli(["im", "+messages-send", "--chat-id", chat_id, "--text", message, "--as", "bot"])
        except Exception as exc:
            notification_error = exc

    if notification_error is None:
        state["last_review"] = {
            "date": day,
            "status": "ok",
            "message": message,
            "updated_at": _now_iso(),
        }
        save_state(state)
    else:
        error_message = f"复盘文档已发布，但会话通知发送失败：{doc_url}"
        state["last_review"] = {
            "date": day,
            "status": "error",
            "message": error_message,
            "updated_at": _now_iso(),
        }
        save_state(state)
        raise RuntimeError(error_message) from notification_error

    return {
        "ok": True,
        "date": day,
        "doc_id": doc_id or existing.get("doc_id", ""),
        "doc_url": doc_url,
        "message": message,
        "markdown": final_markdown,
    }


def run_review(day: str | None = None) -> dict[str, Any]:
    state = ensure_binding(create_if_missing=True)
    target_day = day or today_str()
    inputs = collect_inputs_for_day(state, target_day)
    analysis_payload = build_analysis_payload(inputs)
    return {
        "date": target_day,
        "inputs": inputs,
        "analysis_payload": analysis_payload,
        "message": "Collected same-day inputs and analysis_payload for Codex analysis. Review the payload, then publish the final markdown with publish_review.py.",
    }
