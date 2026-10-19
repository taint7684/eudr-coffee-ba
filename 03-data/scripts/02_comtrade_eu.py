"""T6.3 - Kim ngach xuat khau ca phe (HS 0901) cua Viet Nam sang EU-27, theo so lieu
Viet Nam bao cao len UN Comtrade (SRC-013).

Input : 03-data/raw/comtrade/vnm_0901_{nam}.json
        (tai bang: curl "https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode=704&period={nam}&cmdCode=0901&flowCode=X")
Output: 03-data/processed/vn_coffee_exports_eu.csv
"""
import csv
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "03-data" / "raw" / "comtrade"
OUT = ROOT / "03-data" / "processed" / "vn_coffee_exports_eu.csv"

# Ma doi tac M49 theo cach Comtrade dung (Phap = 251, Y = 380/381).
EU27 = {
    40: "Austria", 56: "Belgium", 100: "Bulgaria", 191: "Croatia", 196: "Cyprus", 203: "Czechia",
    208: "Denmark", 233: "Estonia", 246: "Finland", 251: "France", 276: "Germany", 300: "Greece",
    348: "Hungary", 372: "Ireland", 380: "Italy", 381: "Italy", 428: "Latvia", 440: "Lithuania",
    442: "Luxembourg", 470: "Malta", 528: "Netherlands", 616: "Poland", 620: "Portugal",
    642: "Romania", 703: "Slovakia", 705: "Slovenia", 724: "Spain", 752: "Sweden",
}


def main():
    out = []
    for f in sorted(RAW.glob("vnm_0901_*.json")):
        rows = json.loads(f.read_text(encoding="utf-8")).get("data") or []
        if not rows:
            continue
        year = rows[0]["period"]
        world = next(r for r in rows if r["partnerCode"] == 0)
        eu = [r for r in rows if r["partnerCode"] in EU27]
        eu_val = sum(r["primaryValue"] for r in eu)
        eu_kg = sum(r["netWgt"] or 0 for r in eu)
        top = sorted(eu, key=lambda r: -r["primaryValue"])[:5]
        out.append({
            "year": year,
            "world_usd": round(world["primaryValue"]),
            "world_tonnes": round((world["netWgt"] or 0) / 1000),
            "eu27_usd": round(eu_val),
            "eu27_tonnes": round(eu_kg / 1000),
            "eu27_share_value": round(eu_val / world["primaryValue"], 4),
            "eu27_partners": len(eu),
            "top5_eu": "; ".join(f"{EU27[r['partnerCode']]}={r['primaryValue']/1e6:.0f}M" for r in top),
            "source": "SRC-013 UN Comtrade, reporter=Viet Nam, HS 0901, flow=X",
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="\n", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    for r in out:
        print(r)


if __name__ == "__main__":
    main()
