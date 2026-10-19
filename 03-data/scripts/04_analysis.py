"""T5.3 + T6.1 + T6.2 + T6.3 - Ghep bang huyen, Pareto, xep hang rui ro, gia tri bi de doa.

Input : processed/forest_loss_district_summary.csv   (01_extract_gfw.py)
        processed/loss_drivers_by_district.csv        (03_drivers.py)
        processed/coffee_area_by_district.csv         (nhap tay tu nien giam - SRC ghi trong file)
        processed/vn_coffee_exports_eu.csv            (02_comtrade_eu.py)
Output: processed/district_master.csv
        processed/analysis_summary.json  (so lieu cho S9 va dashboard)

Chi so rui ro (DEC-06: chi so SANG LOC, khong ket luan pha rung):
  v0 (dang dung khi thieu dien tich ca phe): risk_score = minmax(agri_loss_2021_plus_ha)
       agri_loss = mat cay che phu do 'Permanent agriculture' + 'Shifting cultivation' (Sims 2025)
       -> dung sat dinh nghia EUDR Dieu 2(3): chuyen rung sang muc dich nong nghiep.
  v1 (ROADMAP T6.2, tu bat khi du dien tich ca phe 15 huyen):
       risk_score = minmax(agri_loss_2021_plus_ha) x minmax(coffee_ha)
  Muc: tam phan vi -> Cao / Trung binh / Thap (ASM-12).
"""
import csv
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path(__file__).resolve().parents[1] / "processed"
AGRI = {"Permanent agriculture", "Shifting cultivation"}

# ASM cho gia tri bi de doa (00-management/assumptions-log.csv)
DL_SHARE = {"min": 0.25, "likely": 0.29, "max": 0.33}      # ASM-21 ty trong Dak Lak trong san luong VN
HIGH_SHARE = {"min": 0.20, "likely": 0.35, "max": 0.50}    # ASM-22 ty trong dien tich ca phe Dak Lak o huyen rui ro Cao (tam)


def read(name):
    with open(P / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def minmax(vals):
    lo, hi = min(vals), max(vals)
    return [(v - lo) / (hi - lo) if hi > lo else 0.0 for v in vals]


def main():
    loss = read("forest_loss_district_summary.csv")
    drivers = read("loss_drivers_by_district.csv")
    coffee = {r["district"]: r for r in read("coffee_area_by_district.csv")}
    exports = read("vn_coffee_exports_eu.csv")

    agri = {}
    for r in drivers:
        if r["driver"] in AGRI:
            agri[r["district"]] = agri.get(r["district"], 0) + int(r["loss_2021_plus_ha"])

    rows = []
    for r in loss:
        d = r["district"]
        if d not in coffee:
            sys.exit(f"Ten huyen khong khop giua 2 bang: {d}")
        c = coffee[d]["coffee_ha"]
        rows.append({
            "district": d,
            "area_ha": int(r["area_ha"]),
            "extent_2000_ha": int(r["extent_2000_ha"]),
            "loss_2016_2020_ha": int(r["loss_2016_2020_ha"]),
            "loss_2021_plus_ha": int(r["loss_2021_plus_ha"]),
            "agri_loss_2021_plus_ha": agri.get(d, 0),
            "agri_share": round(agri.get(d, 0) / int(r["loss_2021_plus_ha"]), 3) if int(r["loss_2021_plus_ha"]) else 0,
            "loss_trend_pct": round(int(r["loss_2021_plus_ha"]) / int(r["loss_2016_2020_ha"]) - 1, 3),
            "coffee_ha": int(c) if c else "",
            "coffee_status": coffee[d]["status"],
            "loss_ratio": round(int(r["loss_2021_plus_ha"]) / int(c), 4) if c else "",
        })

    full_coffee = all(r["coffee_ha"] != "" for r in rows)
    a = minmax([r["agri_loss_2021_plus_ha"] for r in rows])
    if full_coffee:
        b = minmax([r["coffee_ha"] for r in rows])
        scores = [x * y for x, y in zip(a, b)]
        method = "v1 = minmax(agri_loss_2021_plus_ha) x minmax(coffee_ha)"
    else:
        scores = a
        method = "v0 = minmax(agri_loss_2021_plus_ha) (cho du dien tich ca phe de chuyen v1)"
    srt = sorted(scores)
    t1, t2 = srt[len(srt) // 3], srt[2 * len(srt) // 3]
    for r, s in zip(rows, scores):
        r["risk_score"] = round(s, 3)
        r["risk_level"] = "Cao" if s >= t2 else ("Trung bình" if s >= t1 else "Thấp")
        r["method"] = method.split(" =")[0]

    # Pareto theo mat cay che phu 2021+
    rows.sort(key=lambda r: -r["loss_2021_plus_ha"])
    tot = sum(r["loss_2021_plus_ha"] for r in rows)
    cum = 0
    for r in rows:
        cum += r["loss_2021_plus_ha"]
        r["cum_share"] = round(cum / tot, 3)
    n80 = next(i for i, r in enumerate(rows, 1) if r["cum_share"] >= 0.8)

    with open(P / "district_master.csv", "w", newline="\n", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    # Gia tri bi de doa (USD/nam) - hai lang kinh
    eu = [int(r["eu27_usd"]) for r in exports]
    eu_rng = {"min": min(eu), "likely": int(exports[-1]["eu27_usd"]), "max": max(eu)}
    data_gap = {k: round(eu_rng[k] * DL_SHARE[k]) for k in eu_rng}
    defor = {k: round(data_gap[k] * HIGH_SHARE[k]) for k in eu_rng}

    summary = {
        "method": method,
        "thresholds": {"tertile_low_mid": round(t1, 3), "tertile_mid_high": round(t2, 3)},
        "loss_2021_plus_total_ha": tot,
        "agri_loss_2021_plus_total_ha": sum(r["agri_loss_2021_plus_ha"] for r in rows),
        "pareto": {"districts_for_80pct": n80, "of": len(rows), "share_districts": round(n80 / len(rows), 3),
                   "top": [r["district"] for r in rows[:n80]]},
        "high_risk_districts": [r["district"] for r in rows if r["risk_level"] == "Cao"],
        "eu27_export_usd": eu_rng,
        "value_at_risk_usd": {
            "data_gap_lens": data_gap,
            "deforestation_screening_lens": defor,
            "assumptions": {"ASM-21 Dak Lak share": DL_SHARE, "ASM-22 share in high-risk districts": HIGH_SHARE},
        },
        "years": f"2021-{loss[0]['last_year']}",
        "threshold_canopy_pct": 30,
    }
    (P / "analysis_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                                             encoding="utf-8", newline="\n")
    for r in rows:
        print(f"{r['district']:<16}{r['loss_2021_plus_ha']:>6}{r['agri_loss_2021_plus_ha']:>6}"
              f"{r['agri_share']:>7}{r['loss_trend_pct']:>8}{r['risk_score']:>7} {r['risk_level']:<11}{r['cum_share']}")
    print(json.dumps({k: summary[k] for k in ["pareto", "high_risk_districts", "value_at_risk_usd"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
