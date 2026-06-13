"""
okr_health.py — KR 健康分 + 风险雷达

输入：okr_pull.py 的归一化 JSON（stdin 或文件）
输出：带健康评估的 JSON + 可读报告

用法：
  python scripts/okr_pull.py | python scripts/okr_health.py
  python scripts/okr_health.py okr.json
  python scripts/okr_health.py okr.json --report   # 输出可读报告而非 JSON
"""

import json
import sys
import argparse
from datetime import datetime


RISK_HIGH   = "🔴 高危"
RISK_MEDIUM = "🟡 注意"
RISK_OK     = "🟢 正常"

# 进展记录超过多少天未更新算"长期无更新"
STALE_DAYS = 14


def days_ago(dt_str: str | None) -> int | None:
    """距今多少天（None = 从未更新）。"""
    if not dt_str:
        return None
    try:
        dt = datetime.strptime(dt_str[:19], "%Y-%m-%d %H:%M:%S")
        return (datetime.now() - dt).days
    except Exception:
        return None


def assess_kr(kr: dict, time_progress: float) -> dict:
    """给单条 KR 打健康分并给出风险等级与建议。"""
    score = kr["score"]            # 0~1，完成进度
    weight = kr["weight"]
    last_days = days_ago(kr.get("last_progress_time"))

    issues = []
    risk = RISK_OK

    # 1. 时间 vs 进度落差
    gap = time_progress - score
    if gap > 0.4:
        issues.append(f"时间进度 {time_progress:.0%} 但完成度仅 {score:.0%}，落后 {gap:.0%}")
        risk = RISK_HIGH
    elif gap > 0.2:
        issues.append(f"时间进度 {time_progress:.0%}，完成度 {score:.0%}，略有落后")
        if risk == RISK_OK:
            risk = RISK_MEDIUM

    # 2. 长期无进展记录
    if last_days is None:
        issues.append("从未有进展记录")
        if risk == RISK_OK:
            risk = RISK_MEDIUM
    elif last_days > STALE_DAYS:
        issues.append(f"{last_days} 天未更新进展")
        if risk == RISK_OK:
            risk = RISK_MEDIUM

    # 3. 高权重且停滞
    if weight >= 0.3 and score == 0:
        issues.append(f"权重 {weight:.0%} 但进度为 0")
        risk = RISK_HIGH

    # 4. 临近 deadline 未完成
    if kr.get("deadline"):
        try:
            dl = datetime.strptime(kr["deadline"][:10], "%Y-%m-%d")
            days_left = (dl - datetime.now()).days
            if 0 <= days_left <= 14 and score < 0.8:
                issues.append(f"距截止仅剩 {days_left} 天，完成度 {score:.0%}")
                risk = RISK_HIGH
        except Exception:
            pass

    # 建议动作
    if risk == RISK_HIGH:
        suggestion = "⚡ 立即行动：补充进展记录，重新评估能否达成，必要时调整 KR 描述或拆分"
    elif risk == RISK_MEDIUM:
        suggestion = "📋 近期关注：本周内更新一次进展，重新评估完成把握"
    else:
        suggestion = "继续保持"

    return {
        **kr,
        "risk": risk,
        "issues": issues,
        "suggestion": suggestion,
        "days_since_update": last_days,
    }


def assess(data: dict) -> dict:
    time_progress = data["time_progress"]
    objectives = []
    high_count = medium_count = ok_count = 0

    for obj in data["objectives"]:
        krs = [assess_kr(kr, time_progress) for kr in obj["key_results"]]
        for kr in krs:
            if kr["risk"] == RISK_HIGH:
                high_count += 1
            elif kr["risk"] == RISK_MEDIUM:
                medium_count += 1
            else:
                ok_count += 1
        objectives.append({**obj, "key_results": krs})

    return {
        **data,
        "objectives": objectives,
        "summary": {
            "time_progress_pct": f"{time_progress:.0%}",
            "overall_score_pct": f"{data['overall_score']:.0%}",
            "kr_risk": {"high": high_count, "medium": medium_count, "ok": ok_count},
        },
    }


def render_report(data: dict) -> str:
    """把 assess() 的输出渲染成可读报告。"""
    s = data["summary"]
    lines = [
        f"# OKR 健康报告 — {data['user']['name']}",
        f"周期：{data['cycle']['start'][:10]} ~ {data['cycle']['end'][:10]}",
        f"时间进度：{s['time_progress_pct']}　整体达成率：{s['overall_score_pct']}",
        f"风险：🔴×{s['kr_risk']['high']}  🟡×{s['kr_risk']['medium']}  🟢×{s['kr_risk']['ok']}",
        "",
    ]
    for i, obj in enumerate(data["objectives"], 1):
        lines.append(f"## O{i}（权重 {obj['weight']:.0%}）{obj['text']}")
        for j, kr in enumerate(obj["key_results"], 1):
            lines.append(f"  KR{i}.{j} {kr['risk']}  进度 {kr['score']:.0%}  权重 {kr['weight']:.0%}")
            lines.append(f"    {kr['text'][:60]}{'…' if len(kr['text']) > 60 else ''}")
            for issue in kr["issues"]:
                lines.append(f"    ⚠ {issue}")
            lines.append(f"    → {kr['suggestion']}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OKR 健康分与风险雷达")
    parser.add_argument("file", nargs="?", help="okr_pull 输出的 JSON 文件（默认 stdin）")
    parser.add_argument("--report", action="store_true", help="输出可读报告而非 JSON")
    args = parser.parse_args()

    raw = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    data = json.loads(raw)
    result = assess(data)

    if args.report:
        print(render_report(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
