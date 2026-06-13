# -*- coding: utf-8 -*-
import json, subprocess, sys, os, glob
os.chdir(r"C:\Users\QYL\Desktop\OKR")
MODE = sys.argv[1] if len(sys.argv) > 1 else "dry"

data = {}
for fp in ["O1.json","O2.json","O3.json","O4.json"]:
    with open(os.path.join(".planning","progress",fp),encoding="utf-8") as f:
        data.update(json.load(f))

def content_json(paragraphs):
    blocks=[{"block_element_type":"paragraph","paragraph":{"elements":[
        {"paragraph_element_type":"textRun","text_run":{"text":p,"style":{}}}]}} for p in paragraphs if p and p.strip()]
    return json.dumps({"blocks":blocks}, ensure_ascii=False)

def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True,encoding="utf-8",shell=True)
    out=(r.stdout or "")+(r.stderr or "")
    try: ok=json.loads(r.stdout).get("ok",False)
    except: ok='"ok": true' in out
    return ok,out

# validate
tot=sum(len(v["records"]) for v in data.values())
print(f"loaded {len(data)} KR, {tot} records total")

if MODE=="real":
    print("=== DELETE existing ===")
    delc=0
    for kid in data:
        ok,out=run(["lark-cli","okr","+progress-list","--target-type","key_result","--target-id",kid,"--as","user"])
        try: ids=[p["progress_id"] for p in json.loads(out)["data"]["progress_list"]]
        except: ids=[]
        for pid in ids:
            dok,dout=run(["lark-cli","okr","+progress-delete","--progress-id",str(pid),"--yes","--as","user"])
            if dok: delc+=1
            else: print("  del FAIL",pid,dout[:100])
    print(f"deleted={delc}")

print("=== CREATE enriched records ===")
ok=0; fail=0; idx=0
for kid,v in data.items():
    st=v["source_title"]; su=v["source_url"]
    for rec in v["records"]:
        pct=rec["percent"]; paras=rec["paragraphs"]
        fn=f"ap_{idx}.json"; idx+=1
        with open(fn,"w",encoding="utf-8") as f: f.write(content_json(paras))
        cmd=["lark-cli","okr","+progress-create","--target-type","key_result","--target-id",kid,
             "--progress-percent",str(pct),"--progress-status","normal",
             "--content",f"@{fn}","--source-title",st,"--source-url",su,"--as","user"]
        if MODE=="dry": cmd.append("--dry-run")
        cok,cout=run(cmd)
        print(f"  KR {kid[-4:]} {pct}% ({len(paras)}段) -> {'OK' if cok else 'FAIL '+cout[:150]}")
        ok+=cok; fail+=(not cok)
        try: os.remove(fn)
        except: pass
print(f"\nMODE={MODE}: ok={ok} fail={fail}")
