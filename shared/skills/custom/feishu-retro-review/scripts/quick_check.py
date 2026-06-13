from __future__ import annotations

from skill_entry import print_json, quick_check


def main() -> int:
    print_json(quick_check())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
