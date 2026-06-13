from __future__ import annotations

from skill_entry import ensure_binding, print_json


def main() -> int:
    print_json(ensure_binding())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
