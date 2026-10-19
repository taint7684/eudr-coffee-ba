"""T5.1 (cach A) - Trich so mat cay che phu (tree cover loss) theo huyen cua Dak Lak
tu workbook thong ke quoc gia cua Global Forest Watch (SRC-008).

Input : 03-data/raw/gfw/2025_VNM.xlsx  (khong commit - tai lai bang lenh trong README cua 03-data)
Output: 03-data/processed/forest_loss_by_district.csv   (dang dai: district, year, loss_ha, ...)
        03-data/processed/forest_loss_province_summary.csv

Ranh gioi hanh chinh: GADM 4.1 (63 tinh, cap huyen truoc 01/7/2025) - dung ranh gioi GFW dung.
Nguong do che phu: 30% (mac dinh cua GFW dashboard). Chay lai voi nguong khac qua tham so.
"""
import csv
import sys
from pathlib import Path

import openpyxl

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "03-data" / "raw" / "gfw" / "2025_VNM.xlsx"
OUT = ROOT / "03-data" / "processed"
PROVINCE = "Đắk Lắk"
THRESHOLD = int(sys.argv[1]) if len(sys.argv) > 1 else 30


def norm(s):
    return (s or "").replace("Đ", "D").replace("đ", "d")


def main():
    wb = openpyxl.load_workbook(RAW, read_only=True)
    rows = list(wb["Subnational 2 tree cover loss"].iter_rows(values_only=True))
    head = rows[0]
    idx = {h: i for i, h in enumerate(head)}
    years = [h for h in head if str(h).startswith("tc_loss_ha_")]

    data = [r for r in rows[1:] if r[idx["subnational1"]] == PROVINCE and r[idx["threshold"]] == THRESHOLD]
    if not data:
        cands = sorted({r[idx["subnational1"]] for r in rows[1:] if "L" in norm(r[idx["subnational1"]])})
        sys.exit(f"Khong thay tinh {PROVINCE}. Ung vien: {cands}")

    OUT.mkdir(parents=True, exist_ok=True)
    long_rows = []
    for r in sorted(data, key=lambda r: r[idx["subnational2"]]):
        for y in years:
            long_rows.append({
                "district": r[idx["subnational2"]],
                "year": int(y[-4:]),
                "loss_ha": r[idx[y]],
                "extent_2000_ha": r[idx["extent_2000_ha"]],
                "area_ha": r[idx["area_ha"]],
                "threshold_pct": THRESHOLD,
                "source": "SRC-008 GFW country stats 2025_VNM.xlsx v20260427 (Hansen GFC, GADM 4.1)",
            })
    with open(OUT / "forest_loss_by_district.csv", "w", newline="\n", encoding="utf-8") as f:
        w = csv.DictWriter(f, lineterminator="\n", fieldnames=list(long_rows[0]))
        w.writeheader()
        w.writerows(long_rows)

    summ = []
    for r in sorted(data, key=lambda r: r[idx["subnational2"]]):
        pre = sum(r[idx[f"tc_loss_ha_{y}"]] for y in range(2016, 2021))
        post = sum(r[idx[y]] for y in years if int(y[-4:]) >= 2021)
        summ.append({
            "district": r[idx["subnational2"]],
            "area_ha": r[idx["area_ha"]],
            "extent_2000_ha": r[idx["extent_2000_ha"]],
            "loss_2016_2020_ha": pre,
            "loss_2021_plus_ha": post,
            "last_year": int(years[-1][-4:]),
        })
    with open(OUT / "forest_loss_district_summary.csv", "w", newline="\n", encoding="utf-8") as f:
        w = csv.DictWriter(f, lineterminator="\n", fieldnames=list(summ[0]))
        w.writeheader()
        w.writerows(summ)
    for s in summ:
        print(f"{s['district']:<20} loss21+={s['loss_2021_plus_ha']:>7}  loss16-20={s['loss_2016_2020_ha']:>7}")
    print("Tong 2021+:", sum(s["loss_2021_plus_ha"] for s in summ), "ha | so huyen:", len(summ))


if __name__ == "__main__":
    main()
