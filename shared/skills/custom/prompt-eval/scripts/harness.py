#!/usr/bin/env python3
"""Lightweight local prompt-evaluation harness.

No external API, no cost: inside Claude Code the agent itself is BOTH the model
under test and the judge. This script only does the deterministic plumbing —
parameter extraction and report rendering. Every LLM judgement (scenarios,
outputs, scores) is produced by the agent and written into a results JSON.

Usage:
  python harness.py extract <prompt.md>      # print run-skeleton JSON (params + criteria)
  python harness.py render  <results.json>   # print a markdown scorecard

Stdlib only — runs on any Python 3.8+, Windows/macOS/Linux.
"""
import argparse
import json
import re
import statistics
from pathlib import Path

# [UPPER_SNAKE] placeholders or {{handlebars}} — the two common prompt-template styles.
PARAM_RE = re.compile(r"\[([A-Z][A-Z0-9_ ]{1,40})\]|\{\{\s*(\w+)\s*\}\}")

DEFAULT_CRITERIA = ["tone", "completeness", "usefulness", "accuracy", "authenticity"]


def extract_params(path: Path):
    text = path.read_text(encoding="utf-8")
    params = []
    for m in PARAM_RE.finditer(text):
        name = (m.group(1) or m.group(2)).strip()
        if name not in params:
            params.append(name)
    return params


def cmd_extract(args):
    skeleton = {
        "prompt_file": str(args.prompt),
        "prompt_name": args.prompt.stem,
        "criteria": DEFAULT_CRITERIA,
        "parameters": extract_params(args.prompt),
        "scenarios": [
            # Filled in by the agent. Shape of each scenario:
            # {"id": 1, "description": "...", "values": {"PARAM": "..."},
            #  "runs": [{"model": "claude", "output": "...",
            #            "scores": {"tone": 8, ...}, "overall": 7.6, "notes": "..."}]}
        ],
    }
    print(json.dumps(skeleton, ensure_ascii=False, indent=2))


def _avg(values):
    nums = [v for v in values if isinstance(v, (int, float))]
    return round(statistics.mean(nums), 2) if nums else None


def cmd_render(args):
    data = json.loads(args.results.read_text(encoding="utf-8"))
    criteria = data.get("criteria", DEFAULT_CRITERIA)

    rows = []  # (sid, desc, model, scores, overall, notes)
    for sc in data.get("scenarios", []):
        for run in sc.get("runs", []):
            scores = run.get("scores", {})
            overall = run.get("overall")
            if overall is None:
                overall = _avg(list(scores.values()))
            rows.append((sc.get("id"), sc.get("description", ""), run.get("model", "?"),
                         scores, overall, run.get("notes", "")))

    out = []
    out.append(f"# Prompt evaluation - {data.get('prompt_name', '(unnamed)')}")
    out.append("")
    out.append(f"Source: `{data.get('prompt_file', '')}`  |  "
               f"Scenarios: {len(data.get('scenarios', []))}  |  Runs: {len(rows)}")
    out.append("")

    if not rows:
        out.append("_No runs recorded yet._")
        print("\n".join(out))
        return

    # Per-run scorecard
    out.append("| Scenario | Model | " + " | ".join(criteria) + " | Overall |")
    out.append("|" + "---|" * (len(criteria) + 3))
    for sid, desc, model, scores, overall, _notes in rows:
        cells = " | ".join(str(scores.get(c, "-")) for c in criteria)
        label = f"{sid} {desc}".strip()[:28]
        out.append(f"| {label} | {model} | {cells} | **{overall}** |")

    # Averages by criterion
    crit_avgs = {c: _avg([r[3].get(c) for r in rows]) for c in criteria}
    out.append("")
    out.append("## Averages by criterion")
    out.append("")
    out.append("| Criterion | Avg |")
    out.append("|---|---|")
    for c in criteria:
        out.append(f"| {c} | {crit_avgs[c]} |")

    # Averages by model (when more than one)
    models = []
    for r in rows:
        if r[2] not in models:
            models.append(r[2])
    if len(models) > 1:
        out.append("")
        out.append("## Averages by model")
        out.append("")
        out.append("| Model | Overall |")
        out.append("|---|---|")
        for m in models:
            out.append(f"| {m} | {_avg([r[4] for r in rows if r[2] == m])} |")

    overall_all = _avg([r[4] for r in rows])
    out.append("")
    out.append(f"**Overall score: {overall_all} / 10**")
    scored = {c: a for c, a in crit_avgs.items() if a is not None}
    if scored:
        weakest = min(scored, key=scored.get)
        out.append("")
        out.append(f"**Weakest dimension:** `{weakest}` ({scored[weakest]}) - focus improvements here.")

    print("\n".join(out))


def main():
    ap = argparse.ArgumentParser(description="Local prompt-eval harness (no external API).")
    sub = ap.add_subparsers(required=True)

    e = sub.add_parser("extract", help="extract [PARAMS] from a prompt file; print run-skeleton JSON")
    e.add_argument("prompt", type=Path)
    e.set_defaults(func=cmd_extract)

    r = sub.add_parser("render", help="render a results JSON into a markdown scorecard")
    r.add_argument("results", type=Path)
    r.set_defaults(func=cmd_render)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
