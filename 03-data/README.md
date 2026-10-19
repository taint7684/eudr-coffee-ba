# 03-data — Dữ liệu, phân tích rủi ro (S8–S10)

Dữ liệu thô (`raw/`) không commit. Tải lại:

```bash
mkdir -p 03-data/raw/gfw 03-data/raw/comtrade 03-data/raw/geoboundaries 03-data/raw/gso
curl -L -o 03-data/raw/gso/ng2024.pdf https://thongkedaklak.nso.gov.vn/storage/manager/niengiam_tk/tnf04FI-92dae9de-172a-47c3-8313-e0e42313043d.pdf
curl -L -o 03-data/raw/gfw/2025_VNM.xlsx https://gfw2-data.s3.amazonaws.com/country-pages/country_stats/download/2025/VNM.xlsx
for y in 2021 2022 2023; do curl -o 03-data/raw/comtrade/vnm_0901_$y.json "https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode=704&period=$y&cmdCode=0901&flowCode=X"; done
curl -L -o 03-data/raw/geoboundaries/VNM_ADM2_simplified.geojson https://github.com/wmgeolab/geoBoundaries/raw/main/releaseData/gbOpen/VNM/ADM2/geoBoundaries-VNM-ADM2_simplified.geojson
```

Chạy theo thứ tự `scripts/00` → `05` (cần `openpyxl`, `pypdf`). Kết quả ở `processed/`.
Hướng mở rộng: script GEE `notebooks/T8.1_hansen_vs_gfc2020.js` (so Hansen × JRC GFC2020).
