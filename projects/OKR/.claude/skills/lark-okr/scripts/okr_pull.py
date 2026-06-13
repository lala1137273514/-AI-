"""
okr_pull.py — 拉取并归一化当前周期的飞书 OKR

输出 JSON：
{
  "user": {"open_id": "...", "name": "..."},
  "cycle": {"id": "...", "start": "...", "end": "...", "time_progress": 0.55},
  "time_progress": 0.55,
  "overall_score": 0.0,
  "objectives": [
    {
      "id": "...", "text": "...", "weight": 0.3, "score": 0.0,
      "deadline": "...", "weighted_score": 0.0,
      "key_results": [
        {"id": "...", "text": "...", "weight": 0.25, "score": 0.0,
         "deadline": "...", "weighted_score": 0.0,
         "last_progress_time": null}
      ]
    }
  ]
}

用法：
  python scripts/okr_pull.py
  python scripts/okr_pull.py --cycle-id 7622051252293749950
"""

import json
import subprocess
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

# 把 scripts/ 加入路径，方便直接 import blocks
sys.path.insert(0, str(Path(__file__).parent))
from blocks import parse_blocks


def run_lark(args: list[str]) -> dict:
    """调用 lark-cli，返回解析后的 JSON data 字段。"""
    cmd = "lark-cli " + " ".join(args) + " --as user --format json"
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", shell=True)
    try:
        out = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"[ERROR] lark-cli 返回非 JSON: {result.stdout[:200]}", file=sys.stderr)
        sys.exit(1)
    if not out.get("ok"):
        err = out.get("error", {})
        print(f"[ERROR] {err.get('message', out)}", file=sys.stderr)
        sys.exit(1)
    return out.get("data", out)


def get_open_id() -> tuple[str, str]:
    """从 auth status 取 userOpenId 和 userName。"""
    cmd = "lark-cli auth status"
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", shell=True)
    d = json.loads(result.stdout)
    return d["userOpenId"], d.get("userName", "")


def parse_dt(s: str) -> datetime:
    """'YYYY-MM-DD HH:MM:SS' -> datetime (naive, local)."""
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def find_current_cycle(cycles: list, today: datetime) -> dict | None:
    """找今天所属的最精确（时间跨度最小）周期。"""
    candidates = []
    for c in cycles:
        start = parse_dt(c["start_time"])
        end = parse_dt(c["end_time"])
        if start <= today <= end:
            candidates.append((end - start, c))
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[0])
    return candidates[0][1]


def get_last_progress_time(target_id: str, target_type: str) -> str | None:
    """拉进展记录，返回最新一条的 create_time（或 None）。"""
    try:
        data = run_lark([
            "okr", "+progress-list",
            "--target-id", target_id,
            "--target-type", target_type,
        ])
        records = data.get("items", data.get("progress_list", []))
        if not records:
            return None
        # 按 create_time 降序取最新
        records.sort(key=lambda r: r.get("create_time", ""), reverse=True)
        return records[0].get("create_time")
    except Exception:
        return None


def pull(cycle_id: str | None = None, with_progress: bool = True) -> dict:
    open_id, user_name = get_open_id()
    today = datetime.now()

    # 1. 获取周期列表
    cycle_data = run_lark(["okr", "+cycle-list", "--user-id", open_id])
    cycles = cycle_data.get("cycles", [])

    # 2. 选周期
    if cycle_id:
        cycle = next((c for c in cycles if c["id"] == cycle_id), None)
        if not cycle:
            print(f"[ERROR] 找不到周期 {cycle_id}", file=sys.stderr)
            sys.exit(1)
    else:
        cycle = find_current_cycle(cycles, today)
        if not cycle:
            print("[ERROR] 找不到包含今天的周期", file=sys.stderr)
            sys.exit(1)

    start = parse_dt(cycle["start_time"])
    end = parse_dt(cycle["end_time"])
    span = (end - start).total_seconds()
    time_progress = max(0.0, min(1.0, (today - start).total_seconds() / span)) if span > 0 else 0.0

    # 3. 拉周期详情
    detail = run_lark(["okr", "+cycle-detail", "--cycle-id", cycle["id"]])
    raw_objectives = detail.get("objectives", [])

    # 4. 归一化
    objectives = []
    total_weighted_score = 0.0
    total_weight = 0.0

    for obj in raw_objectives:
        obj_text = parse_blocks(obj.get("content", ""))
        obj_weight = float(obj.get("weight", 0))
        obj_score = float(obj.get("score", 0))

        key_results = []
        for kr in obj.get("key_results", []):
            kr_text = parse_blocks(kr.get("content", ""))
            kr_weight = float(kr.get("weight", 0))
            kr_score = float(kr.get("score", 0))

            last_progress = None
            if with_progress:
                last_progress = get_last_progress_time(kr["id"], "key_result")

            key_results.append({
                "id": kr["id"],
                "text": kr_text,
                "weight": kr_weight,
                "score": kr_score,
                "deadline": kr.get("deadline"),
                "weighted_score": round(kr_weight * kr_score, 4),
                "last_progress_time": last_progress,
            })

        obj_entry = {
            "id": obj["id"],
            "text": obj_text,
            "weight": obj_weight,
            "score": obj_score,
            "deadline": obj.get("deadline"),
            "weighted_score": round(obj_weight * obj_score, 4),
            "key_results": key_results,
        }
        objectives.append(obj_entry)
        total_weighted_score += obj_weight * obj_score
        total_weight += obj_weight

    overall_score = round(total_weighted_score / total_weight, 4) if total_weight > 0 else 0.0

    return {
        "user": {"open_id": open_id, "name": user_name},
        "cycle": {
            "id": cycle["id"],
            "start": cycle["start_time"],
            "end": cycle["end_time"],
            "time_progress": round(time_progress, 4),
        },
        "time_progress": round(time_progress, 4),
        "overall_score": overall_score,
        "objectives": objectives,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="拉取并归一化当前飞书 OKR")
    parser.add_argument("--cycle-id", help="指定周期 ID（默认自动选当前周期）")
    parser.add_argument("--no-progress", action="store_true", help="跳过拉取进展记录（更快）")
    args = parser.parse_args()

    data = pull(cycle_id=args.cycle_id, with_progress=not args.no_progress)
    print(json.dumps(data, ensure_ascii=False, indent=2))
