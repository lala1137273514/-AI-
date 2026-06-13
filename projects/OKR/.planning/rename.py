# -*- coding: utf-8 -*-
import json, subprocess
# (file_token, type, new_title)
items = [
 # 根层周报统一
 ("Yb37diIHNo2OHkxMlPNc3Cacnxg","docx","2026-04-20 ~ 2026-04-26 周报"),
 ("AqbFd81TDojihfxI5gzcPxBcnXg","docx","2026-04-13 ~ 2026-04-19 周报"),
 # 归档重复周报标注
 ("YVGfdUfIWouPvzxrj2ycworonKv","docx","2026-04-27 ~ 2026-05-03 周报（提前版·已被完整版取代）"),
 # 05月日报统一
 ("RqKXd8kCToSY6lx3FvEcr4BdnXg","docx","2026-05-11 日复盘"),
 ("H3k2dr3X7oeQ0YxmLhucLg8snTh","docx","2026-05-07 日复盘"),
 ("G7iFdCxyGorcXAx323DcmG7bnwA","docx","2026-05-06 日复盘"),
 ("TPKhdy4j3odhVmxzW8gcRtiXnTd","docx","2026-05-05 日复盘"),
 ("DpwmdPWSFoLQiaxvTelcR8SGnKf","docx","2026-05-04 日复盘"),
 ("SXEkduhCYoenlQxtLvNcK5wlnYe","docx","2026-05-03 日复盘"),
 ("F9f9dE42uo0KsjxeSKMcGUejnEI","docx","2026-05-01 日复盘"),
 # 04月日报统一
 ("WRdPdrP4qox7E5xP7JycHg8tnMD","docx","2026-04-30 日复盘"),
 ("LGOdd43PaovkTHxMWbGc28rZnTg","docx","2026-04-29 日复盘"),
 ("DQekd9mp5oEAQGxeSfOcWHp9n8d","docx","2026-04-28 日复盘"),
 ("Ss5qd0NcMopPOSxY4ngclEkcnhh","docx","2026-04-27 日复盘"),
 ("Qb0VdDdZVolGSwxtxyzcC7iqntd","docx","2026-04-26 日复盘"),
 ("CQOpdyZyQot5EoxsBspcdIMNnbd","docx","2026-04-25 日复盘"),
 ("EF9CdMgKeoMYbuxjgeqcaVgUn1l","docx","2026-04-24 日复盘"),
 ("Md2HdFvN0oQiLhxlPsJcCQBnnGh","docx","2026-04-22 日复盘"),
 ("KlHcdCyMEojXjsxc5V6cgtDPnSf","docx","2026-04-21 日复盘"),
 ("Hl9qdPp5foXigqxE2qXcZ4nPnnU","docx","2026-04-20 日复盘"),
 ("RDAXd8pjQoZa8xxEWAacqCiwn5y","docx","2026-04-19 日复盘"),
 ("A0NrdjTAtoOHQTxGPLXcXZJmnqb","docx","2026-04-18 日复盘"),
 ("DpJJdyRlNo23x0xSIYGcXMikndh","docx","2026-04-17 日复盘"),
]
import time
ok=fail=0
for tok,typ,title in items:
    params=json.dumps({"file_token":tok,"type":typ},ensure_ascii=False)
    data=json.dumps({"new_title":title},ensure_ascii=False)
    good=False
    for attempt in range(3):
        r=subprocess.run(["lark-cli","drive","files","patch","--params",params,"--data",data,"--as","user"],
                         capture_output=True,text=True,encoding="utf-8",shell=True)
        out=(r.stdout or "")+(r.stderr or "")
        good='"ok": true' in out
        if good: break
        if 'rate_limit' in out or '99991400' in out:
            time.sleep(2); continue
        break
    print(f"{'OK ' if good else 'FAIL'} {title}")
    if not good: print("   ",out[:160].replace("\n"," "))
    ok+=good; fail+=(not good)
    time.sleep(0.6)
print(f"\nrenamed ok={ok} fail={fail}")
