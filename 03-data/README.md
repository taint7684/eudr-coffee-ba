# 03-data — Dữ liệu, phân tích rủi ro (S8–S10)

Dữ liệu thô (`raw/`) không commit. Tải lại:

```bash
mkdir -p 03-data/raw/gfw 03-data/raw/comtrade 03-data/raw/geoboundaries
curl -L -o 03-data/raw/gfw/2025_VNM.xlsx https://gfw2-data.s3.amazonaws.com/country-pages/country_stats/download/2025/VNM.xlsx
for y in 2021 2022 2023; do curl -o 03-data/raw/comtrade/vnm_0901_$y.json "https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode=704&period=$y&cmdCode=0901&flowCode=X"; done
curl -L -o 03-data/raw/geoboundaries/VNM_ADM2_simplified.geojson https://github.com/wmgeolab/geoBoundaries/raw/main/releaseData/gbOpen/VNM/ADM2/geoBoundaries-VNM-ADM2_simplified.geojson
```

Chạy theo thứ tự `scripts/01` → `05`. Kết quả ở `processed/`. Khi có niên giám, điền `processed/coffee_area_by_district.csv` rồi chạy lại `04_analysis.py`; chỉ số tự chuyển sang v1.
Script GEE cho T8.1: `notebooks/T8.1_hansen_vs_gfc2020.js` (chạy trên code.earthengine.google.com).
