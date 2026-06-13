from __future__ import annotations

import argparse

from skill_entry import print_json, run_review, today_str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect review materials for Codex analysis.")
    parser.add_argument("--date", help="Target date in YYYY-MM-DD format.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    day = args.date or today_str()
    print_json({"ok": True, **run_review(day)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
