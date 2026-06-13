#!/usr/bin/env python3
"""Weighted-rubric scorer — HeartBench scoring method, local agent as judge.

Fuses the scoring math of HeartBench (https://github.com/inclusionAI/HeartBench,
via cortex/prompt_opt/heartbench) into prompt-eval, but with NO external API:
the hit-vector (`detail`, 0/1 per rubric item) is produced by the in-session
Claude agent, not by a remote judge model. This file is pure stdlib.

Rubric item: {"dimension": str, "score": number, "content": str}
  score > 0  -> positive item: counts only when FULLY achieved (agent hit=1)
  score < 0  -> penalty item: counts when even touched (agent hit=1)
  dimension in {其他, other, gate} (score 0) -> anti-cheat gate: any hit zeroes the whole question

Input  (jsonl, one row per evaluated output):
  {"question_id","scenario_key","rubric":[{dimension,score,content}...],"detail":[0/1...],"reason"?}
Output:
  <out>              per-question detail
  <out>.summary.json {OVERALL, by_dimension, by_scenario, n_questions, n_gated}

Scoring inherited from HeartBench, including its two fixes:
  [FIX-1] robust parser lives in SKILL.md flow (agent emits clean JSON), not here.
  [FIX-2] gate fires when ANY 'other' rubric item is hit (original required score>0,
          which never triggered because those items are score 0).

Usage:
  python heartscore.py --input scored_in.jsonl --out scored.jsonl
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

try:  # UTF-8 output even on a GBK Windows console
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

GATE_DIMS = {"其他", "other", "gate", "GATE"}


def score_one(rubric: list[dict], detail: list[int]) -> dict[str, Any]:
    """HeartBench per-question scoring. detail = 0/1 hit per rubric item (from the agent)."""
    if not rubric:
        return {"dimension_score": [], "question_score": 0.0, "gated": False}
    detail = (list(detail) + [0] * len(rubric))[:len(rubric)]  # align length

    def is_gate(r):
        return r.get("dimension") in GATE_DIMS or float(r.get("score") or 0) == 0

    gated = any(d == 1 and is_gate(r) for r, d in zip(rubric, detail))

    ranges: dict[str, list[float]] = defaultdict(lambda: [0.0, 0.0])  # dim -> [min(neg sum), max(pos sum)]
    raw: dict[str, float] = defaultdict(float)
    for r in rubric:
        if is_gate(r):
            continue
        dim, s = r.get("dimension"), float(r.get("score") or 0)
        if dim is None:
            continue
        if s < 0:
            ranges[dim][0] += s
        elif s > 0:
            ranges[dim][1] += s
    for r, hit in zip(rubric, detail):
        if hit and not is_gate(r) and r.get("dimension") is not None:
            raw[r["dimension"]] += float(r.get("score") or 0)

    dims, norms = [], []
    for dim, (lo, hi) in ranges.items():
        span = hi - lo
        if gated or span <= 0:
            norm = 0.0
        else:
            num = max(raw.get(dim, 0.0) - lo, 0.0) + 1.0   # floor at neg-sum -> baseline >0 if no penalty hit
            norm = math.log(num) / math.log(span + 1.0) * 100  # log -> diminishing returns
        dims.append({"ability": dim, "raw_score": raw.get(dim, 0.0), "norm_score": round(norm, 2)})
        norms.append(norm)
    q = 0.0 if gated else (sum(norms) / len(norms) if norms else 0.0)
    return {"dimension_score": dims, "question_score": round(q, 2), "gated": gated}


def main() -> int:
    ap = argparse.ArgumentParser(description="Weighted-rubric scorer (HeartBench method, local judge).")
    ap.add_argument("--input", required=True, type=Path, help="jsonl with rubric + agent-produced detail")
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    rows = [json.loads(l) for l in args.input.read_text(encoding="utf-8").splitlines() if l.strip()]

    out_rows = []
    dim_sum: dict[str, float] = defaultdict(float)
    dim_cnt: dict[str, int] = defaultdict(int)
    scen_scores: dict[str, list[float]] = defaultdict(list)

    for i, row in enumerate(rows, 1):
        rubric = row["rubric"]
        detail = row.get("detail", [])
        res = score_one(rubric, detail)
        out_rows.append({
            "question_id": row.get("question_id", i),
            "scenario_key": row.get("scenario_key"),
            "detail": detail,
            "reason": row.get("reason", ""),
            "gated": res["gated"],
            "dimension_score": res["dimension_score"],
            "question_score": res["question_score"],
        })
        for d in res["dimension_score"]:
            dim_sum[d["ability"]] += d["norm_score"]
            dim_cnt[d["ability"]] += 1
        scen_scores[row.get("scenario_key")].append(res["question_score"])
        flag = " [GATED]" if res["gated"] else ""
        print(f"[{i}/{len(rows)}] {row.get('question_id', i)} "
              f"({row.get('scenario_key')}): {res['question_score']}{flag}")

    dim_avg = {d: round(dim_sum[d] / dim_cnt[d], 2) for d in sorted(dim_sum)}
    overall = round(sum(dim_avg.values()) / len(dim_avg), 2) if dim_avg else 0.0
    scen_avg = {k: round(sum(v) / len(v), 2) for k, v in sorted(scen_scores.items(), key=lambda kv: str(kv[0])) if v}

    args.out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in out_rows) + "\n",
                        encoding="utf-8")
    summary = {"OVERALL": overall, "by_dimension": dim_avg, "by_scenario": scen_avg,
               "n_questions": len(out_rows), "n_gated": sum(r["gated"] for r in out_rows)}
    Path(str(args.out) + ".summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n" + "=" * 56)
    print(f"OVERALL humanlike score: {overall} / 100   (n={len(out_rows)}, gated={summary['n_gated']})")
    print("by_dimension:", json.dumps(dim_avg, ensure_ascii=False))
    print("by_scenario :", json.dumps(scen_avg, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
