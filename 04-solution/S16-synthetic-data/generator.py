"""T13.1 - Sinh du lieu gia lap (SYNTHETIC DATA) cho prototype va UAT. Seed co dinh -> sinh lai giong het.

Phan phoi (cong khai gia dinh):
- Nong ho: 200, gan 12 dai ly; xa thuoc 6 huyen cu (trong so theo xep hang S9).
- Lo: ~300 (1-3 lo/ho). Dien tich log-normal, trung vi ~1,0 ha (ASM-04), cat 0,2-8 ha.
  Lo > 4 ha co da giac; lo <= 4 ha co diem (mot so co da giac).
- Ket qua cham: muc tieu ~10% Vung xam (ASM-14), ~3% Loai (ASM-15); phan con lai Dat.
  Nguoi dung tham so cham (overlap, loss, dist) roi ap BR-010..014 de ra ket qua -> nhat quan voi SRS.
- Phap ly: ~85% Du, ~10% Thieu, ~5% Mau thuan.
- Giao dich: ~1.000, nien vu 2026/27 (11/2026-03/2027), san luong theo dien tich x nang suat 2,6 t/ha (ASM-03).
- Ca bien bat buoc cho UAT: lo dung 4,00 ha; lo 4,01 ha; lo thieu giay to; lo mau thuan ranh gioi.
Toa do nam trong hop bao cua cac huyen (xap xi, KHONG phai vi tri that).
"""
import csv
import json
import math
import random
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(__file__).resolve().parent
rng = random.Random(2026)

# (huyen cu, xa mau, tam lat, tam lon, trong so) - tam xap xi, chi de rai diem
DISTRICTS = [
    ("Cư M'gar", ["Ea Kiết", "Cư M'gar", "Quảng Hiệp"], 12.88, 108.07, 0.24),
    ("Krông Búk", ["Pơng Drang", "Cư Pơng"], 12.95, 108.22, 0.14),
    ("Krông Năng", ["Krông Năng", "Phú Xuân"], 12.99, 108.38, 0.14),
    ("Ea H'leo", ["Ea H'leo", "Ea Wy"], 13.20, 108.20, 0.16),
    ("Krông Pắc", ["Krông Pắc", "Ea Kly"], 12.70, 108.30, 0.18),
    ("Lắk", ["Liên Sơn Lắk", "Đắk Liêng"], 12.40, 108.15, 0.14),
]
AGENTS = [f"DL-{i:02d}" for i in range(1, 13)]
HO = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Y", "H'", "Võ", "Đặng", "Bùi"]
TEN = ["Văn An", "Thị Lan", "Văn Bình", "Thị Hoa", "Minh", "Bhim Niê", "Bia Êban", "Thị Mai", "Văn Hùng", "Thị Hạnh",
       "Kiều", "Đức", "Thanh", "Ngọc", "Quang"]


def wcho(items, weights):
    return rng.choices(items, weights=weights, k=1)[0]


def polygon(lat, lon, area_ha):
    r = math.sqrt(area_ha * 1e4 / math.pi)  # m
    n = rng.randint(5, 8)
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        rr = r * rng.uniform(0.85, 1.15)
        pts.append([round(lon + rr * math.cos(a) / (111320 * math.cos(math.radians(lat))), 6),
                    round(lat + rr * math.sin(a) / 110540, 6)])
    pts.append(pts[0])
    return pts


def score(overlap, loss_post, loss_in_overlap, dist):
    """Bang quyet dinh SRS 4.1 (thu tu R4 -> R3 -> R2 -> R5 -> R1)."""
    if overlap >= 0.10 and loss_post and loss_in_overlap:
        return "Loại", "R4"
    if overlap >= 0.10:
        return "Vùng xám", "R3"
    if loss_post:
        return "Vùng xám", "R2"
    if dist < 50:
        return "Vùng xám", "R5"
    return "Đạt", "R1"


def write(name, rows):
    path = OUT / name
    with open(path, "w", newline="\n", encoding="utf-8") as f:
        f.write("# SYNTHETIC DATA — dữ liệu giả lập cho prototype/UAT, không phải dữ liệu thật. Seed 2026.\n")
        w = csv.DictWriter(f, lineterminator="\n", fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{name}: {len(rows)} dòng")


def main():
    farmers, plots, txns = [], [], []
    for i in range(1, 201):
        d = wcho(DISTRICTS, [x[4] for x in DISTRICTS])
        farmers.append({
            "farmer_id": f"NH-{i:05d}", "full_name": f"{rng.choice(HO)} {rng.choice(TEN)}",
            "birth_year": rng.randint(1958, 2000), "phone": f"09{rng.randint(10000000, 99999999)}",
            "commune_new": rng.choice(d[1]), "district_old": d[0], "agent_id": rng.choice(AGENTS),
            "consent": "Có", "consent_at": "2026-10-0" + str(rng.randint(1, 9)),
        })

    pid = 0
    for f in farmers:
        d = next(x for x in DISTRICTS if x[0] == f["district_old"])
        for _ in range(wcho([1, 2, 3], [0.55, 0.35, 0.10])):
            pid += 1
            area = round(min(8.0, max(0.2, rng.lognormvariate(0, 0.55))), 2)
            lat = round(d[2] + rng.uniform(-0.08, 0.08), 6)
            lon = round(d[3] + rng.uniform(-0.08, 0.08), 6)
            plots.append({"plot_id": f"LO-{pid:05d}", "farmer_id": f["farmer_id"], "district_old": d[0],
                          "commune_new": f["commune_new"], "area_declared_ha": area, "lat": lat, "lon": lon})

    # Ca bien cho UAT (gan vao 4 lo dau)
    plots[0]["area_declared_ha"] = 4.00
    plots[1]["area_declared_ha"] = 4.01
    edge_missing_doc, edge_conflict = plots[2]["plot_id"], plots[3]["plot_id"]

    for p in plots:
        area = p["area_declared_ha"]
        use_poly = area > 4 or rng.random() < 0.15
        geom = polygon(p["lat"], p["lon"], area) if use_poly else None
        p["geometry_type"] = "Polygon" if use_poly else "Point"
        p["geometry"] = json.dumps({"type": "Polygon", "coordinates": [geom]} if use_poly
                                   else {"type": "Point", "coordinates": [p["lon"], p["lat"]]})
        p["area_computed_ha"] = round(area * rng.uniform(0.9, 1.1), 2) if use_poly else ""
        p["gps_accuracy_m"] = round(rng.uniform(3, 15), 1)
        p["planting_year"] = rng.randint(1995, 2018)
        u = rng.random()
        if u < 0.03:      # nham Loai
            ov, lp, lio, dist = round(rng.uniform(0.15, 0.6), 2), True, True, 0
        elif u < 0.13:    # nham Vung xam
            case = rng.choice(["R2", "R3", "R5"])
            ov, lp, lio, dist = {"R2": (0.0, True, False, 0), "R3": (round(rng.uniform(0.1, 0.5), 2), False, False, 0),
                                 "R5": (0.0, False, False, rng.randint(5, 49))}[case]
        else:
            ov, lp, lio, dist = 0.0, False, False, rng.randint(50, 900)
        res, rule = score(ov, lp, lio, dist)
        p.update({"forest2020_overlap_pct": round(ov * 100), "loss_post2020": "Có" if lp else "Không",
                  "min_dist_m": dist, "risk_rule": rule, "risk_status": res})
        lr = rng.random()
        if p["plot_id"] == edge_missing_doc:
            lr = 0.9
        if p["plot_id"] == edge_conflict:
            lr = 0.99
        if lr < 0.85:
            p.update({"doc_type": "GCN QSDĐ", "doc_number": f"CS{rng.randint(100000, 999999)}",
                      "area_on_doc_ha": round(area * rng.uniform(0.92, 1.08), 2), "legal_status": "Đủ"})
        elif lr < 0.95:
            p.update({"doc_type": "Không có", "doc_number": "", "area_on_doc_ha": "", "legal_status": "Thiếu"})
        else:
            p.update({"doc_type": "GCN QSDĐ", "doc_number": f"CS{rng.randint(100000, 999999)}",
                      "area_on_doc_ha": round(area / 1.5, 2), "legal_status": "Mâu thuẫn"})
        p["map_version"] = "GFC2020-V3 + Hansen-v1.13"

    tid = 0
    for p in plots:
        cap = p["area_declared_ha"] * 2600  # kg nhan/nien vu (ASM-03)
        for _ in range(rng.randint(2, 5)):
            tid += 1
            eligible = p["risk_status"] == "Đạt" and p["legal_status"] == "Đủ"
            far = next(f for f in farmers if f["farmer_id"] == p["farmer_id"])
            m = rng.choice([11, 12, 1, 2, 3])
            y = 2026 if m >= 11 else 2027
            txns.append({"txn_id": f"GD-{tid:06d}", "txn_date": f"{y}-{m:02d}-{rng.randint(1, 28):02d}",
                         "plot_id": p["plot_id"], "farmer_id": p["farmer_id"], "agent_id": far["agent_id"],
                         "net_kg": int(round(cap / 3.5 * rng.uniform(0.6, 1.2), -1)),
                         "stream": "EU" if eligible and rng.random() < 0.7 else "Khác", "season": "2026/27"})
    txns.sort(key=lambda t: (t["txn_date"], t["txn_id"]))

    write("farmers_SYNTH.csv", farmers)
    write("plots_SYNTH.csv", plots)
    write("transactions_SYNTH.csv", txns)
    from collections import Counter
    print("Kết quả chấm:", dict(Counter(p["risk_status"] for p in plots)))
    print("Pháp lý:", dict(Counter(p["legal_status"] for p in plots)))
    print("Lô > 4 ha:", sum(p["area_declared_ha"] > 4 for p in plots))


if __name__ == "__main__":
    main()
