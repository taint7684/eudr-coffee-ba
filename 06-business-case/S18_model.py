"""T16.2-T16.4, T17.1-T17.2 - Mo hinh chi phi/loi ich 3 phuong an ECTS, ky 3 nam.

Moi tham so co min/likely/max va ma ASM/SRC (00-management/assumptions-log.csv).
Sinh: 06-business-case/model_results.json + bang GEN trong S18-business-case.md + tornado.svg
Chay: py 06-business-case/S18_model.py
"""
import csv
import json
import random
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

exp = list(csv.DictReader(open(ROOT / "03-data/processed/vn_coffee_exports_eu.csv", encoding="utf-8")))
last = exp[-1]
UNIT_PRICE = int(last["eu27_usd"]) / int(last["eu27_tonnes"])  # USD/t, SRC-013 (2023)
FX = 25400  # VND/USD - ASM-26

# name: (min, likely, max, ma, mo ta)
P = {
    "volume_t":        (15000, 30000, 50000, "ASM-01", "Sản lượng thu mua (t/năm)"),
    "eu_share":        (0.30, 0.45, 0.60, "ASM-02", "Tỷ trọng bán EU"),
    "yield_t_ha":      (2.3, 2.6, 3.0, "ASM-03", "Năng suất (t/ha)"),
    "plot_ha":         (0.5, 1.0, 2.0, "ASM-04", "Diện tích bình quân/lô (ha)"),
    "agents":          (30, 60, 120, "ASM-05", "Số đại lý"),
    "discount":        (0.03, 0.06, 0.10, "ASM-25", "Mức giảm giá khi phải bán sang thị trường khác"),
    "geo_vnd":         (50000, 150000, 400000, "ASM-16", "Chi phí thu tọa độ/lô (VND)"),
    "gray_rate":       (0.05, 0.10, 0.20, "ASM-14", "Tỷ lệ lô Vùng xám"),
    "verify_vnd":      (300000, 700000, 1500000, "ASM-17", "Chi phí xác minh/lô Vùng xám (VND)"),
    "officer_usd":     (8000, 12000, 18000, "ASM-27", "Chi phí nhân sự tuân thủ (USD/năm)"),
    "train_usd":       (50, 100, 200, "ASM-28", "Đào tạo/đại lý (USD)"),
    "build_usd":       (80000, 150000, 300000, "ASM-19", "A: chi phí tự xây (USD)"),
    "saas_usd":        (15000, 40000, 100000, "ASM-18", "B: phí SaaS (USD/năm)"),
    "consortium_share": (0.15, 0.30, 0.50, "ASM-20", "C: tỷ lệ chia sẻ chi phí so với tự xây"),
    "wacc":            (0.08, 0.10, 0.14, "ASM-30", "Suất chiết khấu"),
    "segregation_usd_t": (5, 15, 30, "ASM-31", "Chi phí tách dòng/kho riêng (USD/t EU)"),
    "farmer_support_usd_t": (0, 10, 30, "ASM-32", "Hỗ trợ nông hộ cung cấp dữ liệu (USD/t EU)"),
}
# Ty le loi ich nam 1 theo toc do trien khai (ASM-29): A 9 thang, B 3 thang, C 6 thang
RAMP = {"A": 0.5, "B": 0.9, "C": 0.7}
OPTIONS = {"A": "Tự xây ECTS", "B": "Thuê nền tảng SaaS", "C": "Liên minh ngành"}


def val(k, case="likely"):
    i = {"min": 0, "likely": 1, "max": 2}[case]
    return P[k][i]


def run(o, v, yr1_benefit=True, gray_mult=1.0):
    """Dong tien nam 0..3 (USD). Nam 0: dau tu ban dau. Nam 1-3: loi ich - chi phi van hanh."""
    plots = v["volume_t"] / v["yield_t_ha"] / v["plot_ha"]
    eu_t = v["volume_t"] * v["eu_share"]
    benefit = eu_t * UNIT_PRICE * v["discount"]  # gia tri giu duoc/nam
    geo = plots * v["geo_vnd"] / FX
    verify = plots * min(1, v["gray_rate"] * gray_mult) * v["verify_vnd"] / FX
    per_t = eu_t * (v["segregation_usd_t"] + v["farmer_support_usd_t"])
    if o == "A":
        sw0, sw = v["build_usd"], 0.2 * v["build_usd"]
    elif o == "B":
        sw0, sw = 5000, v["saas_usd"]
    else:
        b = v["consortium_share"] * v["build_usd"]
        sw0, sw = b, 0.2 * b + 3000
    capex = sw0 + geo + verify + v["agents"] * v["train_usd"]
    opex = sw + 0.10 * geo + 0.5 * verify + v["officer_usd"] + 0.3 * v["agents"] * v["train_usd"] + per_t
    ben = [0, benefit * (RAMP[o] if yr1_benefit else 0), benefit, benefit]
    cost = [capex, opex, opex, opex]
    net = [b - c for b, c in zip(ben, cost)]
    npv = sum(n / (1 + v["wacc"]) ** t for t, n in enumerate(net))
    cum, payback = 0.0, None
    for t, n in enumerate(net):
        if payback is None and cum < 0 and cum + n >= 0:
            payback = t - 1 + (-cum / n)
        cum += n
    return {"benefit": ben, "cost": cost, "net": net, "npv": npv, "payback_years": payback,
            "plots": plots, "cost_per_plot_3y": sum(cost) / plots}


def base(case="likely"):
    return {k: val(k, case) for k in P}


def breakeven(o, key, lo, hi):
    """Gia tri cua tham so key de NPV = 0 (chia doi)."""
    v = base()
    f = lambda x: run(o, {**v, key: x})["npv"]
    if f(lo) * f(hi) > 0:
        return None
    for _ in range(60):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if f(lo) * f(m) > 0 else (lo, m)
    return (lo + hi) / 2


def tornado(o):
    v0, out = base(), []
    for k in P:
        lo, hi = run(o, {**v0, k: val(k) * 0.8})["npv"], run(o, {**v0, k: val(k) * 1.2})["npv"]
        out.append((k, lo, hi, abs(hi - lo)))
    return sorted(out, key=lambda x: -x[3])


def monte_carlo(o, n=10000, seed=2026):
    rng = random.Random(seed)
    res = []
    for _ in range(n):
        v = {k: rng.triangular(a, c, b) for k, (a, b, c, *_r) in P.items()}
        res.append(run(o, v)["npv"])
    res.sort()
    return {"p_npv_pos": sum(x > 0 for x in res) / n, "p10": res[n // 10], "p50": res[n // 2], "p90": res[9 * n // 10]}


def svg_tornado(rows, base_npv, path):
    w, h, top, rh = 640, 30 + 26 * len(rows[:8]), 20, 26
    mn = min(min(r[1], r[2]) for r in rows[:8]); mx = max(max(r[1], r[2]) for r in rows[:8])
    sx = lambda x: 190 + (x - mn) / (mx - mn) * 420
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="system-ui,Segoe UI,sans-serif" font-size="12">',
         f'<line x1="{sx(base_npv):.1f}" x2="{sx(base_npv):.1f}" y1="10" y2="{h - 10}" stroke="#555" stroke-dasharray="3 3"/>']
    for i, (k, lo, hi, _) in enumerate(rows[:8]):
        y = top + i * rh
        a, b = sorted([lo, hi])
        g.append(f'<text x="182" y="{y + 15}" text-anchor="end" fill="#333">{P[k][4][:30]}</text>')
        g.append(f'<rect x="{sx(a):.1f}" y="{y + 4}" width="{max(1, sx(b) - sx(a)):.1f}" height="16" rx="2" fill="#2f6f4f"/>')
    g.append(f'<text x="{sx(base_npv):.1f}" y="{h - 1}" text-anchor="middle" fill="#555">NPV cơ sở {base_npv / 1e6:.2f} triệu USD</text></svg>')
    path.write_text("\n".join(g) + "\n", encoding="utf-8", newline="\n")


def m(x):
    return f"{x / 1e6:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main():
    R = {}
    for o in OPTIONS:
        R[o] = {c: run(o, base(c)) for c in ["min", "likely", "max"]}
        R[o]["mc"] = monte_carlo(o)
        R[o]["postpone"] = run(o, base(), yr1_benefit=False)
        R[o]["standard_risk"] = run(o, base(), gray_mult=2.5)
    best = max(OPTIONS, key=lambda o: R[o]["likely"]["npv"])
    tor = tornado(best)
    svg_tornado(tor, R[best]["likely"]["npv"], HERE / "tornado.svg")
    be_share = {o: breakeven(o, "eu_share", 0.001, 1.0) for o in OPTIONS}
    be_vol = {o: breakeven(o, "volume_t", 200, 200000) for o in OPTIONS}
    be_disc = {o: breakeven(o, "discount", 0.0001, 0.5) for o in OPTIONS}

    # Ma tran quyet dinh co trong so (T17.1): diem 1-5
    crit = [("Chi phí 3 năm", 0.30, 0.20), ("Tốc độ triển khai", 0.25, 0.15), ("Độ tin cậy dữ liệu", 0.20, 0.20),
            ("Khả năng mở rộng", 0.10, 0.10), ("Tác động tới nông hộ", 0.15, 0.35)]
    score = {"A": [2, 2, 5, 4, 3], "B": [4, 5, 3, 3, 2], "C": [5, 3, 4, 5, 5]}
    wsum = {o: {"DN": sum(s * c[1] for s, c in zip(score[o], crit)), "Nông hộ": sum(s * c[2] for s, c in zip(score[o], crit))} for o in OPTIONS}

    out = {"unit_price_usd_t": round(UNIT_PRICE), "fx": FX, "results": R, "best_npv": best,
           "breakeven": {"eu_share": be_share, "volume_t": be_vol, "discount": be_disc},
           "tornado": [(k, round(lo), round(hi)) for k, lo, hi, _ in tor], "weighted": wsum}
    (HERE / "model_results.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=float) + "\n",
                                            encoding="utf-8", newline="\n")

    T = ["| Chỉ số (USD) | " + " | ".join(f"{o}. {OPTIONS[o]}" for o in OPTIONS) + " |", "|---|---|---|---|"]
    rows = [("NPV 3 năm — min / likely / max (triệu)", lambda o: f"{m(R[o]['min']['npv'])} / **{m(R[o]['likely']['npv'])}** / {m(R[o]['max']['npv'])}"),
            ("Lợi ích năm 2 (triệu)", lambda o: m(R[o]['likely']['benefit'][2])),
            ("Tổng chi phí năm 0–3 (triệu)", lambda o: m(sum(R[o]['likely']['cost']))),
            ("Chi phí/lô/3 năm", lambda o: f"{R[o]['likely']['cost_per_plot_3y']:,.0f}".replace(",", ".")),
            ("Hoàn vốn (năm)", lambda o: f"{R[o]['likely']['payback_years']:.1f}".replace(".", ",") if R[o]['likely']['payback_years'] is not None else "> 3"),
            ("Xác suất NPV > 0 (Monte Carlo 10.000 lần)", lambda o: f"{R[o]['mc']['p_npv_pos']:.0%}"),
            ("NPV P10 / P50 / P90 (triệu)", lambda o: f"{m(R[o]['mc']['p10'])} / {m(R[o]['mc']['p50'])} / {m(R[o]['mc']['p90'])}"),
            ("Kịch bản EUDR hoãn thêm 1 năm — NPV (triệu)", lambda o: m(R[o]['postpone']['npv'])),
            ("Kịch bản VN thành rủi ro chuẩn (Vùng xám ×2,5) — NPV (triệu)", lambda o: m(R[o]['standard_risk']['npv'])),
            ("Hòa vốn: tỷ trọng EU tối thiểu", lambda o: f"{be_share[o]:.1%}".replace(".", ",") if be_share[o] else "—"),
            ("Hòa vốn: sản lượng tối thiểu (t/năm)", lambda o: f"{be_vol[o]:,.0f}".replace(",", ".") if be_vol[o] else "—"),
            ("Hòa vốn: mức giảm giá tối thiểu tránh được", lambda o: f"{be_disc[o]:.2%}".replace(".", ",") if be_disc[o] else "—")]
    for name, f in rows:
        T.append(f"| {name} | " + " | ".join(f(o) for o in OPTIONS) + " |")
    TT = ["| Tham số (±20%) | NPV khi −20% (triệu) | NPV khi +20% (triệu) | Biên độ |", "|---|---:|---:|---:|"]
    for k, lo, hi, d in tor[:6]:
        TT.append(f"| {P[k][4]} ({P[k][3]}) | {m(lo)} | {m(hi)} | {m(d)} |")
    W = ["| Tiêu chí | Trọng số DN | Trọng số nông hộ | A | B | C |", "|---|:-:|:-:|:-:|:-:|:-:|"]
    for i, (c, w1, w2) in enumerate(crit):
        W.append(f"| {c} | {w1:.0%} | {w2:.0%} | {score['A'][i]} | {score['B'][i]} | {score['C'][i]} |")
    W.append("| **Điểm có trọng số — góc nhìn DN** | | | " + " | ".join(f"**{wsum[o]['DN']:.2f}**" for o in OPTIONS) + " |")
    W.append("| **Điểm có trọng số — góc nhìn nông hộ** | | | " + " | ".join(f"**{wsum[o]['Nông hộ']:.2f}**" for o in OPTIONS) + " |")

    doc = HERE / "S18-business-case.md"
    txt = doc.read_text(encoding="utf-8")
    for key, body in [("RESULTS", "\n".join(T)), ("TORNADO", "\n".join(TT)), ("MCDA", "\n".join(W))]:
        txt = re.sub(rf"(<!-- GEN:{key}:START -->\n).*?(<!-- GEN:{key}:END -->)", lambda mm: mm.group(1) + body + "\n" + mm.group(2), txt, flags=re.S)
    doc.write_text(txt, encoding="utf-8", newline="\n")
    print("\n".join(T)); print(); print("\n".join(TT)); print(); print("\n".join(W))
    print("Giá đơn vị EU 2023:", round(UNIT_PRICE), "USD/t; số lô:", round(R['A']['likely']['plots']))


if __name__ == "__main__":
    main()
