from __future__ import annotations

import argparse

from skill_entry import build_analysis_payload, collect_inputs_for_day, ensure_binding, print_json, today_str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect review inputs for one day.")
    parser.add_argument("--date", help="Target date in YYYY-MM-DD format.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    state = ensure_binding()
    day = args.date or today_str()
    inputs = collect_inputs_for_day(state, day)
    payload = dict(inputs)
    payload["analysis_payload"] = build_analysis_payload(inputs)
    print_json(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
