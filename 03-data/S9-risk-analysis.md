# S9 — Phân tích rủi ro mất cây che phủ theo huyện (Đắk Lắk, ranh giới cũ)

> Trả lời **RQ2**: rủi ro tập trung ở huyện nào, giá trị xuất khẩu nào bị đe dọa.
> Dữ liệu: [district_master.csv](processed/district_master.csv) · [analysis_summary.json](processed/analysis_summary.json) · Scripts: [scripts/](scripts/), chạy theo thứ tự 00 → 05.
> Chỉ số trong file này là **chỉ số sàng lọc**, không kết luận phá rừng (DEC-06).

## 1. Phương pháp

| Bước | Cách làm | Nguồn |
|---|---|---|
| Mất cây che phủ | Hansen GFC tổng hợp theo huyện, ngưỡng tán 30%, giai đoạn 2021–2025 | SRC-008 |
| Nguyên nhân | Nguyên nhân chủ đạo 1 km (Sims 2025). "Do nông nghiệp" = *Permanent agriculture* + *Shifting cultivation* | SRC-010 |
| Diện tích cà phê | Niên giám thống kê Đắk Lắk 2024, biểu 170 (diện tích trồng, năm 2024) | SRC-033 |
| Chỉ số rủi ro **v1** | `minmax(mất do nông nghiệp 2021+) × minmax(diện tích cà phê)`: nơi vừa có nhiều mất cây che phủ do chuyển sang nông nghiệp (sát định nghĩa phá rừng, Điều 2(3)), vừa có nhiều cà phê | ROADMAP T6.2; DEC-06 |
| Phân mức | Tam phân vị → Cao / Trung bình / Thấp | ASM-12 |

## 2. Kết quả chính

| # | Phát hiện | Số liệu |
|---|---|---|
| F1 | Mất cây che phủ đang **giảm** | Toàn tỉnh: 2016–2020 = 30.669 ha; 2021–2025 = **15.873 ha** (−48%). 13/15 huyện giảm. |
| F2 | Mất cây che phủ **tập trung** | **5/15 huyện (33%) chiếm 80%** diện tích mất 2021+: M'Đrắk, Krông Bông, Cư M'gar, Lắk, Ea Kar. |
| F3 | Nguyên nhân chia đôi | 2021–2025: **nông nghiệp 54,7%** (8.689 ha), khai thác gỗ 44,3% (7.025 ha), còn lại 1%. |
| F4 | Nơi mất nhiều nhất không phải nơi có nhiều cà phê | M'Đrắk mất 5.665 ha nhưng chỉ có 1.977 ha cà phê, và 80% số mất do khai thác gỗ. Vùng lõi cà phê (Cư M'gar 37.882 ha, Krông Búk, Krông A Na) có gần **100% số mất do nông nghiệp**, nhiều khả năng là chặt/tái canh cây lâu năm trên đất đã canh tác (S10). |
| F5 | Huyện rủi ro **Cao** (v1) | Cư M'gar · Ea H'leo · Krông Bông · Krông Búk · Krông Pắc. Năm huyện này chiếm **55,9% diện tích cà phê** toàn tỉnh (119.617/214.006 ha). |

### Bảng xếp hạng (ngưỡng 30%, 2021–2025; cà phê năm 2024)

| Huyện | Mất 2021+ (ha) | Do nông nghiệp (ha) | % nông nghiệp | So 2016–20 | Cà phê (ha) | Điểm v1 | Mức |
|---|---:|---:|---:|---:|---:|---:|---|
| Cư M'gar | 1.636 | 1.634 | 99,9% | −34% | 37.882 | 1,000 | **Cao** |
| Ea H'leo | 874 | 749 | 85,7% | −68% | 32.520 | 0,361 | **Cao** |
| Krông Bông | 3.072 | 1.629 | 53,0% | −36% | 8.920 | 0,235 | **Cao** |
| Krông Búk | 408 | 407 | 99,8% | −17% | 19.979 | 0,104 | **Cao** |
| Krông Pắc | 422 | 345 | 81,8% | −6% | 20.316 | 0,084 | **Cao** |
| Lắk | 1.368 | 955 | 69,8% | −60% | 5.076 | 0,074 | Trung bình |
| Krông Năng | 333 | 267 | 80,2% | −66% | 24.990 | 0,069 | Trung bình |
| Ea Kar | 980 | 502 | 51,2% | −44% | 9.239 | 0,063 | Trung bình |
| M'Đrắk | 5.665 | 1.145 | 20,2% | −48% | 1.977 | 0,035 | Trung bình |
| TX Buôn Hồ | 214 | 201 | 93,9% | −62% | 14.532 | 0,024 | Trung bình |
| Krông A Na | 173 | 173 | 100% | −49% | 10.135 | 0,012 | Thấp |
| Cư Kuin | 160 | 155 | 96,9% | +3% | 12.118 | 0,010 | Thấp |
| Buôn Ma Thuột | 169 | 141 | 83,4% | −33% | 11.107 | 0,007 | Thấp |
| Ea Súp | 289 | 279 | 96,5% | −77% | — | 0,000 | Thấp |
| Buôn Đôn | 110 | 107 | 97,3% | +18% | 5.215 | 0,000 | Thấp |

Ea Súp: niên giám ghi "—" cho năm 2023–2024 (26 ha các năm 2020–2022), chỉ số tính là 0.
Biểu đồ Pareto, bản đồ, xu hướng theo năm: [dashboard](https://taint7684.github.io/eudr-coffee-ba/).

## 3. Giá trị bị đe dọa (Value at risk, USD/năm)

| Thành phần | min | likely | max | Nguồn |
|---|---:|---:|---:|---|
| Kim ngạch cà phê VN → EU-27 (2021–2023) | 0,98 tỷ | 1,41 tỷ (2023) | 1,43 tỷ | SRC-013 |
| × Tỷ trọng Đắk Lắk | 25% | 29% | 33% | ASM-21 |
| **= Lăng kính 1 — thiếu dữ liệu tọa độ** | **245 triệu** | **408 triệu** | **472 triệu** | |
| × Tỷ trọng diện tích cà phê ở 5 huyện rủi ro Cao | 55,9% | 55,9% | 55,9% | SRC-033 |
| **= Lăng kính 2 — sàng lọc phá rừng** | **137 triệu** | **228 triệu** | **264 triệu** | |

**Diễn giải.**
- Rủi ro lớn nhất là **thiếu dữ liệu**. Không có tọa độ lô thì không lập được DDS, nên toàn bộ phần xuất sang EU (lăng kính 1) bị chặn, kể cả khi đất sạch.
- Lăng kính 2 cho biết hơn một nửa diện tích cà phê nằm ở các huyện cần xác minh kỹ. Các huyện này cũng là vùng lõi cà phê. Vì vậy MVP **thu tọa độ ưu tiên 5 huyện rủi ro Cao** (S14 release plan, S18 lộ trình).

## 4. Dashboard spec (T7.1)

| Mục | Nội dung |
|---|---|
| Người dùng | Quản lý DN, nhân viên tuân thủ |
| 3 câu hỏi | (1) Huyện nào rủi ro cao nhất? (2) Bao nhiêu % diện tích cà phê nằm ở huyện rủi ro Cao? (3) Giá trị bị đe dọa bao nhiêu? |
| Chỉ số | Mất cây che phủ 2021+ · % do nông nghiệp · diện tích cà phê · điểm rủi ro · mức · giá trị bị đe dọa (min/likely/max) |
| Thành phần | Bản đồ choropleth 15 huyện · Pareto · xu hướng 2016–2025 · nguyên nhân · bảng xếp hạng · thẻ KPI |
| Bộ lọc | Mức rủi ro; ngưỡng tán (10/30/50%) |
| Nguồn | SRC-008, 010, 013, 031, 033 (chân trang) |
| Cập nhật | Hằng năm, khi GFW phát hành số năm mới và niên giám mới [Inference] |

## 5. Giới hạn

- Số cấp huyện không thay dữ liệu ranh giới từng lô; không dùng để kết luận tỷ lệ lô cà phê bị ảnh hưởng bởi phá rừng (DEC-08).
- v1 nhân với diện tích cà phê nên huyện có nhiều cà phê được xếp cao. Đây là đúng mục đích ưu tiên thu tọa độ, không phải xếp hạng mức độ phá rừng.
- Ranh giới huyện cũ (DEC-05). Số năm 2025 của GFW có thể được hiệu chỉnh ở phiên bản sau.
