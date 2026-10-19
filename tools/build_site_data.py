"""T7.2 + T13.2 - Dong goi du lieu cho GitHub Pages (docs/).

Sinh:
  docs/data/dashboard.js   - so lieu huyen (S9) + ranh gioi 15 huyen (geoBoundaries, CC BY 3.0 IGO)
  docs/prototype/data.js   - du lieu gia lap S16 cho prototype
Chay: py tools/build_site_data.py   (sau khi chay 03-data/scripts/* va S16 generator)
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "03-data" / "processed"
GB = ROOT / "03-data" / "raw" / "geoboundaries" / "VNM_ADM2_simplified.geojson"
SYN = ROOT / "04-solution" / "S16-synthetic-data"

# Ten geoBoundaries -> ten GFW (SRC-008)
NAME_MAP = {"Buon Don": "Buôn Đôn", "Buon Ho": "Thị Xã Buôn Hồ", "Buon Ma Thuot": "Buôn Ma Thuột",
            "Cu Kuin": "Cư Kuin", "Cu Mgar": "Cư M'gar", "EA Hleo": "Ea H'leo", "Ea Kar": "Ea Kar",
            "Ea Sup": "Ea Súp", "Krong A Na": "Krông A Na", "Krong Bong": "Krông Bông", "Krong Buk": "Krông Búk",
            "Krong Nang": "Krông Năng", "Krong Pac": "Krông Pắc", "Lak": "Lắk", "Mdrak District": "M'Đrắk"}


def read(p, skip_comment=False):
    with open(p, encoding="utf-8") as f:
        if skip_comment:
            f.readline()
        return list(csv.DictReader(f))


def rnd(coords, nd=4):
    if isinstance(coords[0], (int, float)):
        return [round(coords[0], nd), round(coords[1], nd)]
    return [rnd(c, nd) for c in coords]


def js(path, var, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"// Sinh tự động bởi tools/build_site_data.py — không sửa tay.\nwindow.{var} = "
                    + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + ";\n",
                    encoding="utf-8", newline="\n")
    print(path.relative_to(ROOT), round(path.stat().st_size / 1024), "KB")


def main():
    gb = json.loads(GB.read_text(encoding="utf-8"))
    feats = []
    for f in gb["features"]:
        n = f["properties"]["shapeName"]
        if n in NAME_MAP:
            g = f["geometry"]
            feats.append({"type": "Feature", "properties": {"district": NAME_MAP[n]},
                          "geometry": {"type": g["type"], "coordinates": rnd(g["coordinates"])}})
    if len(feats) != 15:
        sys.exit(f"Can 15 huyen, thay {len(feats)}")

    yearly = defaultdict(int)
    for r in read(P / "forest_loss_by_district.csv"):
        yearly[int(r["year"])] += int(r["loss_ha"])
    drivers = defaultdict(int)
    for r in read(P / "loss_drivers_by_district.csv"):
        drivers[r["driver"]] += int(r["loss_2021_plus_ha"])
    sens = {r["district"]: r for r in read(P / "threshold_sensitivity.csv")}
    dash = {
        "districts": read(P / "district_master.csv"),
        "geo": {"type": "FeatureCollection", "features": feats},
        "summary": json.loads((P / "analysis_summary.json").read_text(encoding="utf-8")),
        "yearly": [{"year": y, "loss_ha": yearly[y]} for y in sorted(yearly) if y >= 2016],
        "drivers": dict(sorted(drivers.items(), key=lambda x: -x[1])),
        "threshold": {k: v for k, v in sens.items()},
        "exports": read(P / "vn_coffee_exports_eu.csv"),
    }
    js(ROOT / "docs" / "data" / "dashboard.js", "DASH", dash)

    plots = read(SYN / "plots_SYNTH.csv", True)
    for p in plots:
        p["geometry"] = json.loads(p["geometry"])
    proto = {"farmers": read(SYN / "farmers_SYNTH.csv", True), "plots": plots,
             "txns": read(SYN / "transactions_SYNTH.csv", True)}
    js(ROOT / "docs" / "prototype" / "data.js", "SYN", proto)


if __name__ == "__main__":
    main()
