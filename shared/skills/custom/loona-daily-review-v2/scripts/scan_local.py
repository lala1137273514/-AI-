#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_local.py <YYYY-MM-DD> [--git repoA repoB ...]

扫本地三源（Claude session / Codex session / git commit）命中某日的工程产出，
按项目归类，输出 markdown 片段供日报第 1 节「本地工程线」使用。

- Claude: C:\\Users\\QYL\\.claude\\projects\\<proj>\\*.jsonl  (排除 subagents/)，按 mtime 命中当天
- Codex:  C:\\Users\\QYL\\.codex\\sessions\\2026\\MM\\DD\\rollout-*.jsonl
- git:    对传入的仓库跑 git log --since/--until

流式读、UTF-8 安全、大文件只取首条用户意图 + 文件尾部关键产出片段。只读。
"""
import os, sys, json, glob, subprocess, datetime

os.environ.setdefault("PYTHONIOENCODING", "utf-8")
os.environ.setdefault("PYTHONUTF8", "1")

CLAUDE_ROOT = r"C:\Users\QYL\.claude\projects"
CODEX_ROOT  = r"C:\Users\QYL\.codex\sessions\2026"
NOISE = ("reply with exactly", "codex-ok", "session_ready", "verify-codex",
         "omc-codex", "omx-exec", "你好", "测试", "你是什么模型", "?", "？")

def day_bounds(d):
    start = datetime.datetime.strptime(d, "%Y-%m-%d")
    return start.timestamp(), (start + datetime.timedelta(days=1)).timestamp()

def first_user_intent(path, limit_bytes=400_000):
    """流式读 jsonl 取首条真实 user 文本（剔除包装/噪声）。"""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            read = 0
            for line in f:
                read += len(line)
                if read > limit_bytes:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                txt = _extract_text(obj)
                if not txt:
                    continue
                low = txt.lower()
                if any(n in low for n in NOISE) or len(txt) < 8:
                    continue
                if txt.startswith(("<", "AGENTS.md", "environment_context", "Files-mentioned",
                                   "The following is the Codex", "Caveat:")):
                    continue
                return txt[:240].replace("\n", " ")
    except Exception as e:
        return None
    return None

def _extract_text(obj):
    # Claude transcript: {"type":"user","message":{"role":"user","content":[{"type":"text","text":..}]}}
    msg = obj.get("message") or obj
    if isinstance(msg, dict):
        if msg.get("role") not in (None, "user"):
            return None
        c = msg.get("content")
        if isinstance(c, str):
            return c
        if isinstance(c, list):
            for part in c:
                if isinstance(part, dict) and part.get("type") == "text":
                    return part.get("text", "")
    # Codex: {"type":"event_msg","payload":{"type":"user_message","message":..}} 或 {"type":"user_message",...}
    if obj.get("type") in ("user_message",) or (obj.get("payload", {}) or {}).get("type") == "user_message":
        p = obj.get("payload", obj)
        return p.get("message") or p.get("text") or ""
    return None

def scan_claude(d):
    lo, hi = day_bounds(d)
    hits = {}
    for proj in os.listdir(CLAUDE_ROOT):
        pdir = os.path.join(CLAUDE_ROOT, proj)
        if not os.path.isdir(pdir):
            continue
        for jf in glob.glob(os.path.join(pdir, "*.jsonl")):
            if os.sep + "subagents" + os.sep in jf:
                continue
            try:
                m = os.path.getmtime(jf)
            except OSError:
                continue
            if lo <= m < hi:
                intent = first_user_intent(jf)
                if intent:
                    hits.setdefault(proj, []).append(intent)
    return hits

def scan_codex(d):
    lo, hi = day_bounds(d)
    mm, dd = d[5:7], d[8:10]
    ddir = os.path.join(CODEX_ROOT, mm, dd)
    hits = []
    if os.path.isdir(ddir):
        for jf in glob.glob(os.path.join(ddir, "rollout-*.jsonl")):
            intent = first_user_intent(jf)
            if intent:
                hits.append(intent)
    return hits

def scan_git(d, repos):
    lo = d + " 00:00:00"
    hi = d + " 23:59:59"
    out = {}
    for repo in repos:
        if not os.path.isdir(repo):
            continue
        try:
            r = subprocess.run(["git", "-C", repo, "log", f"--since={lo}", f"--until={hi}",
                                "--oneline", "--no-color"],
                               capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
            if r.stdout.strip():
                out[os.path.basename(repo.rstrip("\\/"))] = r.stdout.strip().splitlines()
        except Exception:
            pass
    return out

def main():
    if len(sys.argv) < 2:
        print("usage: scan_local.py YYYY-MM-DD [--git repo ...]"); sys.exit(1)
    d = sys.argv[1]
    repos = []
    if "--git" in sys.argv:
        repos = sys.argv[sys.argv.index("--git") + 1:]

    claude = scan_claude(d)
    codex = scan_codex(d)
    git = scan_git(d, repos) if repos else {}

    print(f"# 本地工程线扫描 · {d}\n")
    print("## Claude session（按项目）")
    if claude:
        for proj, intents in sorted(claude.items(), key=lambda x: -len(x[1])):
            print(f"\n### {proj}  ({len(intents)} 会话)")
            for it in intents[:6]:
                print(f"- {it}")
    else:
        print("（当日无命中）")
    print("\n## Codex session")
    if codex:
        for it in codex[:12]:
            print(f"- {it}")
    else:
        print("（当日无会话）")
    print("\n## git commit")
    if git:
        for repo, lines in git.items():
            print(f"\n### {repo}")
            for ln in lines:
                print(f"- `{ln}`")
    elif repos:
        print("（当日无 commit）")
    else:
        print("（未传 --git 仓库）")

if __name__ == "__main__":
    main()
