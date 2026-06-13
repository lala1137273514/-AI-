from __future__ import annotations

import argparse
from pathlib import Path

from skill_entry import (
    ensure_binding,
    print_json,
    publish_review_markdown,
    today_str,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish a review document and notify the chat.")
    parser.add_argument("--date", help="Target date in YYYY-MM-DD format.")
    parser.add_argument("--markdown", help="Inline markdown to publish directly.")
    parser.add_argument("--markdown-file", type=Path, help="Path to a markdown file to publish.")
    return parser.parse_args()


def load_markdown(args: argparse.Namespace, state: dict[str, object], day: str) -> str:
    if args.markdown_file:
        return args.markdown_file.read_text(encoding="utf-8")
    if args.markdown is not None:
        return args.markdown
    raise ValueError("publish_review.py requires --markdown or --markdown-file; analysis must be provided by the agent")


def main() -> int:
    args = parse_args()
    state = ensure_binding()
    day = args.date or today_str()
    markdown = load_markdown(args, state, day)
    print_json(publish_review_markdown(state, day, markdown))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
