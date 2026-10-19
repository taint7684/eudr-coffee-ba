"""T8.1 (phan lam duoc khong can GEE) - Do nhay cua so mat cay che phu 2021+ theo nguong tan.
EUDR dinh nghia rung o nguong tan > 10% (Dieu 2(4)); GFW mac dinh 30% (ASM-11).

Output: 03-data/processed/threshold_sensitivity.csv
"""
import csv
import sys
from pathlib import Path

import openpyxl

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "03-data" / "raw" / "gfw" / "2025_VNM.xlsx"
OUT = ROOT / "03-data" / "processed" / "threshold_sensitivity.csv"
TH = [10, 30, 50]


def main():
    wb = openpyxl.load_workbook(RAW, read_only=True)
    rows = list(wb["Subnational 2 tree cover loss"].iter_rows(values_only=True))
    i = {h: k for k, h in enumerate(rows[0])}
    yrs = [h for h in rows[0] if str(h).startswith("tc_loss_ha_") and int(h[-4:]) >= 2021]
    d = {}
    for r in rows[1:]:
        if r[i["subnational1"]] == "Đắk Lắk" and r[i["threshold"]] in TH:
            d.setdefault(r[i["subnational2"]], {})[r[i["threshold"]]] = sum(r[i[y]] for y in yrs)
    out = []
    for name in sorted(d):
        v = d[name]
        out.append({"district": name, **{f"loss21_t{t}_ha": v[t] for t in TH},
                    "ratio_t10_vs_t30": round(v[10] / v[30], 3) if v[30] else ""})
    tot = {t: sum(r[f"loss21_t{t}_ha"] for r in out) for t in TH}
    out.append({"district": "TỔNG", **{f"loss21_t{t}_ha": tot[t] for t in TH},
                "ratio_t10_vs_t30": round(tot[10] / tot[30], 3)})
    with open(OUT, "w", newline="\n", encoding="utf-8") as f:
        w = csv.DictWriter(f, lineterminator="\n", fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(out[-1])


if __name__ == "__main__":
    main()
