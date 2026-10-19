"""T5.2 - Trich dien tich trong, dien tich thu hoach, san luong ca phe theo huyen 2020-2024
tu Nien giam thong ke tinh Dak Lak 2024 (SRC-033), bang 170-172, trang in 393-395.

Input : 03-data/raw/gso/ng2024.pdf  (tai: xem 03-data/README.md)
Output: 03-data/processed/gso_coffee_by_district_2020_2024.csv  (dang dai, giu nguyen ky hieu "-")
        03-data/processed/coffee_area_by_district.csv            (nam 2024, ten huyen theo GFW, dau vao 04_analysis)
Can: pypdf
"""
import csv
import re
import sys
from pathlib import Path

from pypdf import PdfReader

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "03-data" / "raw" / "gso" / "ng2024.pdf"
OUT = ROOT / "03-data" / "processed"
TABLES = {393: ("planted_area_ha", "170"), 394: ("harvested_area_ha", "171"), 395: ("production_t", "172")}
TO_GFW = {"TP. Buôn Ma Thuột": "Buôn Ma Thuột", "Thị xã Buôn Hồ": "Thị Xã Buôn Hồ", "Huyện Ea H'leo": "Ea H'leo",
          "Huyện Ea Súp": "Ea Súp", "Huyện Buôn Đôn": "Buôn Đôn", "Huyện Cư M'Gar": "Cư M'gar",
          "Huyện Krông Búk": "Krông Búk", "Huyện Krông Năng": "Krông Năng", "Huyện Ea Kar": "Ea Kar",
          "Huyện M'Đrắk": "M'Đrắk", "Huyện Krông Bông": "Krông Bông", "Huyện Krông Pắc": "Krông Pắc",
          "Huyện Krông Ana": "Krông A Na", "Huyện Lăk": "Lắk", "Huyện Cư Kuin": "Cư Kuin"}
YEARS = [2020, 2021, 2022, 2023, 2024]
ROW = re.compile(r"^\s*\d+\.\s+(.+?)\s+((?:[\d.]+|-)(?:\s+(?:[\d.]+|-)){4})\s*$")


def num(s):
    return "" if s == "-" else int(s.replace(".", ""))


def main():
    r = PdfReader(PDF)
    long, by = [], {}
    for page, (metric, table) in TABLES.items():
        txt = r.pages[page - 1].extract_text()
        rows = [m for m in (ROW.match(ln) for ln in txt.splitlines()) if m]
        if len(rows) != 15:
            sys.exit(f"Trang {page}: can 15 huyen, doc duoc {len(rows)}")
        tot = re.search(r"TỔNG SỐ - TOTAL\s+((?:[\d.]+\s*){5})", txt).group(1).split()
        for m in rows:
            name = " ".join(m.group(1).split())
            vals = m.group(2).split()
            for y, v in zip(YEARS, vals):
                long.append({"district_gso": name, "district": TO_GFW[name], "year": y, "metric": metric,
                             "value": v.replace(".", "") if v != "-" else "-",
                             "source": f"SRC-033 Niên giám TK Đắk Lắk 2024, biểu {table}, tr. {page}"})
                by.setdefault((TO_GFW[name], metric), {})[y] = num(v)
        s = sum(by[(d, metric)][2024] or 0 for d in TO_GFW.values())
        if s != num(tot[-1]):
            sys.exit(f"{metric}: tong 15 huyen {s} != TONG SO {tot[-1]}")
        print(f"{metric}: 15 huyen, tong 2024 = {s:,}".replace(",", "."))
    with open(OUT / "gso_coffee_by_district_2020_2024.csv", "w", newline="\n", encoding="utf-8") as f:
        w = csv.DictWriter(f, lineterminator="\n", fieldnames=list(long[0]))
        w.writeheader()
        w.writerows(long)
    with open(OUT / "coffee_area_by_district.csv", "w", newline="\n", encoding="utf-8") as f:
        w = csv.DictWriter(f, lineterminator="\n", fieldnames=["district", "coffee_ha", "production_t", "year", "status", "source", "notes"])
        w.writeheader()
        for d in sorted(TO_GFW.values()):
            a, p = by[(d, "planted_area_ha")][2024], by[(d, "production_t")][2024]
            w.writerow({"district": d, "coffee_ha": a if a != "" else 0, "production_t": p if p != "" else 0, "year": 2024,
                        "status": "Chính thức", "source": "SRC-033 biểu 170, 172",
                        "notes": "Niên giám ghi '-' (2023–2024); quy ước '-' = không phát sinh [Inference]" if a == "" else ""})


if __name__ == "__main__":
    main()
