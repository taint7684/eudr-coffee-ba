"""T6.1 - Mat cay che phu sau 2020 theo nguyen nhan chu dao (Sims et al. 2025, SRC-010),
theo huyen cu cua Dak Lak, nguong 30%. Nguon: tab 'Subnational 2 drivers' cua SRC-008.

Output: 03-data/processed/loss_drivers_by_district.csv (district, driver, loss_2021_plus_ha, share)
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

import openpyxl

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "03-data" / "raw" / "gfw" / "2025_VNM.xlsx"
OUT = ROOT / "03-data" / "processed" / "loss_drivers_by_district.csv"


def main():
    wb = openpyxl.load_workbook(RAW, read_only=True)
    rows = list(wb["Subnational 2 drivers"].iter_rows(values_only=True))
    idx = {h: i for i, h in enumerate(rows[0])}
    agg = defaultdict(float)
    for r in rows[1:]:
        if r[idx["subnational1"]] == "Đắk Lắk" and r[idx["year"]] >= 2021:
            agg[(r[idx["subnational2"]], r[idx["driver"]])] += r[idx["tc_loss_ha"]]
    tot = defaultdict(float)
    for (d, _), v in agg.items():
        tot[d] += v
    out = [{"district": d, "driver": k, "loss_2021_plus_ha": round(v),
            "share": round(v / tot[d], 3) if tot[d] else 0,
            "source": "SRC-008 tab 'Subnational 2 drivers' (Sims 2025, SRC-010)"}
           for (d, k), v in sorted(agg.items())]
    with open(OUT, "w", newline="\n", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    prov = defaultdict(float)
    for (_, k), v in agg.items():
        prov[k] += v
    s = sum(prov.values())
    for k, v in sorted(prov.items(), key=lambda x: -x[1]):
        print(f"{k:<30}{v:>8.0f} ha {v / s:>6.1%}")


if __name__ == "__main__":
    main()
