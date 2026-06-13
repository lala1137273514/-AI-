#!/usr/bin/env python3
"""Merge N independent judges into one strict hit-vector, then a score-input row.

Dual/multi-judge cross-check for the weighted-rubric (HeartBench) mode:
  - positive item (score > 0): hit only if ALL judges agree (AND / intersection) -> strict credit
  - penalty/gate item (score <= 0): hit if ANY judge flags it (OR / union)       -> strict penalty

Each judge file is JSON: {scenario_key: [0/1, ...], ...} (arrays in rubric order).
A judge array that is missing or the wrong length for a scenario is dropped for
that scenario (with a warning); remaining judges still merge.

Output: score-input jsonl ({question_id, scenario_key, rubric, detail}) ready for heartscore.py.

Usage:
  python merge_judges.py --rubric loona_rubric_v2.jsonl \
      --judge judgeA.json --judge judgeB.json --out score_in.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def main() -> int:
    ap = argparse.ArgumentParser(description="Merge N judges (positive=AND, penalty=OR) into score-input.")
    ap.add_argument("--rubric", required=True, type=Path, help="rubric jsonl: {scenario_key, rubric:[{dimension,score,content}]}")
    ap.add_argument("--judge", required=True, action="append", type=Path, help="judge JSON {scenario_key:[0/1...]}; repeatable")
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    rubric = {json.loads(l)["scenario_key"]: json.loads(l)["rubric"]
              for l in args.rubric.read_text(encoding="utf-8").splitlines() if l.strip()}
    judges = [json.loads(p.read_text(encoding="utf-8")) for p in args.judge]

    rows = []
    for sk, items in rubric.items():
        n = len(items)
        vecs = []
        for ji, j in enumerate(judges):
            v = j.get(sk)
            if not isinstance(v, list) or len(v) != n:
                print(f"  [warn] judge#{ji+1} dropped for '{sk}' (len {len(v) if isinstance(v, list) else 'n/a'} != {n})")
                continue
            vecs.append([1 if x else 0 for x in v])
        if not vecs:
            print(f"  [warn] no valid judge for '{sk}', detail all 0")
            detail = [0] * n
        else:
            detail = []
            for i, r in enumerate(items):
                col = [v[i] for v in vecs]
                detail.append(min(col) if r.get("score", 0) > 0 else max(col))  # AND positives, OR penalties/gates
        rows.append({"question_id": sk, "scenario_key": sk, "rubric": items, "detail": detail})

    args.out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    print(f"merged {len(judges)} judges -> {len(rows)} rows -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
