"""T14.5 + T15.3 - Sinh RTM va kiem tra do phu hai chieu tu du lieu truy vet.

Nguon (sua o day, khong sua file sinh ra):
  02-regulatory/S7-eudr-requirements.csv · 04-solution/trace/{fr,br,us,ac,tc_design}.csv
Sinh ra:
  05-test/S17-test-cases.csv   (TC-001..: thiet ke ky thuat; TC-101..: moi AC mot TC)
  05-test/S17-rtm.csv          (req_eu, rc, fr, br, us, ac, scr, tc)
  05-test/S17-coverage.md      (ket qua kiem tra; thoat != 0 neu co loi)
Chay: py 04-solution/trace/build_rtm.py
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
T = ROOT / "04-solution" / "trace"
OUT = ROOT / "05-test"


def read(p):
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def split(s):
    return [x.strip() for x in (s or "").split(";") if x.strip()]


def write(path, rows, cols):
    with open(path, "w", newline="\n", encoding="utf-8") as f:
        w = csv.DictWriter(f, lineterminator="\n", fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def main():
    req = read(ROOT / "02-regulatory" / "S7-eudr-requirements.csv")
    fr, br, us, ac, tcd = (read(T / f"{n}.csv") for n in ["fr", "br", "us", "ac", "tc_design"])

    # --- Test cases ---
    tcs = []
    for t in tcd:
        tcs.append({"id": t["id"], "technique": t["technique"], "title": t["title"], "precondition": t["inputs"],
                    "steps": "Chạy quy tắc với dữ liệu đầu vào", "expected": t["expected"],
                    "br": t["br"], "ac": t["ac"]})
    ac_tc = defaultdict(list)
    for t in tcs:
        for a in split(t["ac"]):
            ac_tc[a].append(t["id"])
    for i, a in enumerate(ac, 101):
        tid = f"TC-{i:03d}"
        tcs.append({"id": tid, "technique": "Theo AC", "title": f"{a['id']} — {a['then'][:70]}",
                    "precondition": a["given"], "steps": a["when"], "expected": a["then"],
                    "br": a["br"], "ac": a["id"]})
        ac_tc[a["id"]].insert(0, tid)
    OUT.mkdir(exist_ok=True)
    write(OUT / "S17-test-cases.csv", tcs, list(tcs[0]))

    # --- RTM ---
    us_by_fr, ac_by_us = defaultdict(list), defaultdict(list)
    for u in us:
        for f in split(u["fr"]):
            us_by_fr[f].append(u)
    for a in ac:
        ac_by_us[a["us"]].append(a)
    fr_by_req = defaultdict(list)
    for f in fr:
        for r in split(f["req_eu"]):
            fr_by_req[r].append(f)

    rtm = []
    for r in req:
        frs = fr_by_req.get(r["id"], [])
        if not frs:
            rtm.append({"req_eu": r["id"], "level": r["level"], "rc": r["related_rc"], "fr": "", "br": "",
                        "us": "", "ac": "", "scr": "", "tc": "", "moscow": ""})
            continue
        for f in frs:
            for u in us_by_fr.get(f["id"], []) or [None]:
                acs = ac_by_us.get(u["id"], []) if u else []
                for a in acs or [None]:
                    rtm.append({
                        "req_eu": r["id"], "level": r["level"], "rc": f["rc"], "fr": f["id"],
                        "br": (a["br"] if a and a["br"] else (u["br"] if u else "")),
                        "us": u["id"] if u else "", "ac": a["id"] if a else "",
                        "scr": u["scr"] if u else f["scr"],
                        "tc": "; ".join(ac_tc.get(a["id"], [])) if a else "", "moscow": f["moscow"]})
    write(OUT / "S17-rtm.csv", rtm, list(rtm[0]))

    # --- Kiem tra do phu ---
    errs, warns = [], []
    br_ids = {b["id"] for b in br}
    for r in req:
        if r["level"] == "⛔":
            rows = [x for x in rtm if x["req_eu"] == r["id"]]
            if not any(x["tc"] for x in rows):
                errs.append(f"{r['id']} (⛔) chưa đi tới TC")
    for f in fr:
        if f["moscow"] == "Must" and not us_by_fr.get(f["id"]):
            errs.append(f"{f['id']} (Must) không có user story")
    for u in us:
        n = len(ac_by_us.get(u["id"], []))
        if n == 0:
            errs.append(f"{u['id']} không có AC")
        elif n > 4:
            warns.append(f"{u['id']} có {n} AC (> 4)")
    used_br = {b for a in ac for b in split(a["br"])} | {b for t in tcd for b in split(t["br"])}
    for b in sorted(br_ids - used_br):
        errs.append(f"{b} không có AC/TC kiểm")
    for b in sorted(used_br - br_ids):
        errs.append(f"{b} được tham chiếu nhưng không có trong br.csv")
    ac_ids = {a["id"] for a in ac}
    for t in tcs:
        if not split(t["ac"]):
            errs.append(f"{t['id']} không trỏ về AC")
        for a in split(t["ac"]):
            if a not in ac_ids:
                errs.append(f"{t['id']} trỏ AC không tồn tại: {a}")
    no_fr = [r["id"] for r in req if not fr_by_req.get(r["id"])]

    md = ["# S17 — Kết quả kiểm tra độ phủ RTM", "",
          "> File sinh tự động bởi `04-solution/trace/build_rtm.py`. Không sửa tay.", "",
          "| Chỉ số | Giá trị |", "|---|---|",
          f"| REQ-EU | {len(req)} (⛔ {sum(r['level'] == '⛔' for r in req)}) |",
          f"| FR · BR · US · AC | {len(fr)} · {len(br)} · {len(us)} · {len(ac)} |",
          f"| Test case | {len(tcs)} ({len(tcd)} thiết kế kỹ thuật + {len(ac)} theo AC) |",
          f"| Dòng RTM | {len(rtm)} |",
          f"| REQ-EU ⛔ đi tới TC | {sum(1 for r in req if r['level'] == '⛔') - sum('⛔' in e for e in errs)}"
          f"/{sum(r['level'] == '⛔' for r in req)} |",
          f"| Lỗi · Cảnh báo | {len(errs)} · {len(warns)} |", "",
          "## REQ-EU không có FR (ngoài phạm vi hệ thống, có lý do)", ""]
    for rid in no_fr:
        r = next(x for x in req if x["id"] == rid)
        md.append(f"- {rid} {r['level']} {r['article']} — {r['notes'] or r['vn_current_state']}")
    md += ["", "## Lỗi", ""] + ([f"- {e}" for e in errs] or ["- Không có"])
    md += ["", "## Cảnh báo", ""] + ([f"- {w}" for w in warns] or ["- Không có"])
    (OUT / "S17-coverage.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(md[6:15]))
    for e in errs:
        print("LỖI:", e)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
