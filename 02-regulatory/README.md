# 02-regulatory — Ma trận yêu cầu EUDR (S7)

Văn bản gốc không commit. Tải lại vào `02-regulatory/raw/` rồi chạy hai script:

```bash
for c in 32023R1115 32024R3234 32025R2650 32025R1093; do
  curl -L -H "Accept: application/xhtml+xml" -H "Accept-Language: eng" \
       -o 02-regulatory/raw/$c.html http://publications.europa.eu/resource/celex/$c
done
mv 02-regulatory/raw/32023R1115.html 02-regulatory/raw/eudr_32023R1115.html
py 02-regulatory/scripts/html2txt.py   # XHTML -> văn bản thuần
py 02-regulatory/scripts/build_s7.py   # sinh S7-eudr-requirements.csv (nguyên văn trích tự động)
```
