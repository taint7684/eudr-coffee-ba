# S9 — Phân tích rủi ro mất cây che phủ theo huyện (Đắk Lắk, ranh giới cũ)

> Trả lời **RQ2**: rủi ro tập trung ở huyện nào, giá trị xuất khẩu nào bị đe dọa.
> Dữ liệu: [district_master.csv](processed/district_master.csv) · [analysis_summary.json](processed/analysis_summary.json) · Scripts: [scripts/](scripts/) chạy theo thứ tự 01 → 05.
> Chỉ số trong file này là **chỉ số sàng lọc**, không kết luận phá rừng (DEC-06).

## 1. Phương pháp

| Bước | Cách làm | Nguồn |
|---|---|---|
| Mất cây che phủ | Hansen GFC tổng hợp theo huyện, ngưỡng tán 30%, giai đoạn 2021–2025 | SRC-008 |
| Nguyên nhân | Nguyên nhân chủ đạo 1 km (Sims 2025). "Do nông nghiệp" gồm *Permanent agriculture* và *Shifting cultivation* | SRC-010 |
| Chỉ số rủi ro **v0** (đang dùng) | `minmax(mất do nông nghiệp 2021+)`. Bám định nghĩa phá rừng của EUDR: chuyển sang mục đích nông nghiệp (Điều 2(3)) | DEC-06 |
| Chỉ số rủi ro **v1** (ROADMAP T6.2) | `minmax(mất do nông nghiệp) × minmax(diện tích cà phê)`. Script tự chuyển sang v1 khi đủ diện tích cà phê của 15 huyện | Chờ niên giám (RSK-03) |
| Phân mức | Tam phân vị → Cao / Trung bình / Thấp | ASM-12 |

## 2. Kết quả chính

| # | Phát hiện | Số liệu |
|---|---|---|
| F1 | Mất cây che phủ đang **giảm** | Toàn tỉnh: 2016–2020 = 30.669 ha; 2021–2025 = **15.873 ha** (−48%). 13/15 huyện giảm. |
| F2 | Rủi ro **tập trung** | **5/15 huyện (33%) chiếm 80%** diện tích mất cây che phủ 2021+: M'Đrắk, Krông Bông, Cư M'gar, Lắk, Ea Kar. |
| F3 | Nguyên nhân chia đôi | 2021–2025: **nông nghiệp 54,7%** (8.689 ha), khai thác gỗ 44,3% (7.025 ha), còn lại 1%. |
| F4 | Hai loại huyện khác nhau | Phía đông (M'Đrắk, Krông Bông): mất nhiều nhưng phần lớn do **khai thác gỗ** (nông nghiệp chỉ 20% và 53%). Vùng lõi cà phê (Cư M'gar, Krông Búk, Krông A Na): gần **100% do nông nghiệp**, nhiều khả năng là chặt/tái canh cây lâu năm trên đất đã canh tác (S10). |
| F5 | Huyện rủi ro **Cao** (v0) | Cư M'gar · Krông Bông · M'Đrắk · Lắk · Ea H'leo |

### Bảng xếp hạng (ngưỡng 30%, 2021–2025)

| Huyện | Mất 2021+ (ha) | Do nông nghiệp (ha) | % nông nghiệp | So 2016–20 | Điểm v0 | Mức |
|---|---:|---:|---:|---:|---:|---|
| Cư M'gar | 1.636 | 1.634 | 99,9% | −34% | 1,000 | **Cao** |
| Krông Bông | 3.072 | 1.629 | 53,0% | −36% | 0,997 | **Cao** |
| M'Đrắk | 5.665 | 1.145 | 20,2% | −48% | 0,680 | **Cao** |
| Lắk | 1.368 | 955 | 69,8% | −60% | 0,555 | **Cao** |
| Ea H'leo | 874 | 749 | 85,7% | −68% | 0,420 | **Cao** |
| Ea Kar | 980 | 502 | 51,2% | −44% | 0,259 | Trung bình |
| Krông Búk | 408 | 407 | 99,8% | −17% | 0,196 | Trung bình |
| Krông Pắc | 422 | 345 | 81,8% | −6% | 0,156 | Trung bình |
| Ea Súp | 289 | 279 | 96,5% | −77% | 0,113 | Trung bình |
| Krông Năng | 333 | 267 | 80,2% | −66% | 0,105 | Trung bình |
| TX Buôn Hồ | 214 | 201 | 93,9% | −62% | 0,062 | Thấp |
| Krông A Na | 173 | 173 | 100% | −49% | 0,043 | Thấp |
| Cư Kuin | 160 | 155 | 96,9% | +3% | 0,031 | Thấp |
| Buôn Ma Thuột | 169 | 141 | 83,4% | −33% | 0,022 | Thấp |
| Buôn Đôn | 110 | 107 | 97,3% | +18% | 0,000 | Thấp |

Biểu đồ Pareto, bản đồ và xu hướng theo năm: xem [dashboard](../docs/index.html).

## 3. Giá trị bị đe dọa (Value at risk, USD/năm)

| Thành phần | min | likely | max | Mã |
|---|---:|---:|---:|---|
| Kim ngạch cà phê VN → EU-27 (2021–2023) | 0,98 tỷ | 1,41 tỷ (2023) | 1,43 tỷ | SRC-013 |
| × Tỷ trọng Đắk Lắk | 25% | 29% | 33% | ASM-21 |
| **= Lăng kính 1 — thiếu dữ liệu tọa độ** | **245 triệu** | **408 triệu** | **472 triệu** | |
| × Tỷ trọng diện tích ở huyện rủi ro Cao (tạm) | 20% | 35% | 50% | ASM-22 |
| **= Lăng kính 2 — sàng lọc phá rừng** | **49 triệu** | **143 triệu** | **236 triệu** | |

**Diễn giải.** Rủi ro lớn nhất không nằm ở phá rừng mà ở **thiếu dữ liệu**. Không có tọa độ lô thì không lập được DDS, nên toàn bộ phần xuất khẩu sang EU (lăng kính 1) bị chặn, kể cả khi đất sạch. Lăng kính 2 chỉ là phần cần xác minh kỹ hơn. Kết luận này định hướng ưu tiên MVP: **thu tọa độ trước, chấm rủi ro sau** (S14 release plan).

## 4. Dashboard spec (T7.1)

| Mục | Nội dung |
|---|---|
| Người dùng | Quản lý DN, nhân viên tuân thủ |
| 3 câu hỏi | (1) Huyện nào rủi ro cao nhất? (2) Bao nhiêu % diện tích cà phê nằm ở huyện rủi ro Cao? (3) Giá trị bị đe dọa bao nhiêu? |
| Chỉ số | Mất cây che phủ 2021+ · % do nông nghiệp · điểm rủi ro · mức · giá trị bị đe dọa (min/likely/max) |
| Thành phần | Bản đồ choropleth 15 huyện · Pareto · xu hướng 2016–2025 · bảng xếp hạng · thẻ KPI |
| Bộ lọc | Mức rủi ro; ngưỡng tán (10/30/50%) |
| Nguồn | SRC-008, 010, 013, 031 (ghi ở chân trang) |
| Cập nhật | Hằng năm, khi GFW phát hành số năm mới (thường quý II) [Inference] |

## 5. Giới hạn

- Câu hỏi (2) chưa trả lời được cho đến khi có diện tích cà phê theo huyện (RSK-03). Dashboard hiển thị "chờ dữ liệu".
- Ranh giới huyện cũ (DEC-05); số 2025 là năm đầu của phiên bản dữ liệu mới, có thể được hiệu chỉnh.
- Lăng kính 2 dùng ASM-22 tin cậy thấp; phải tính lại khi có niên giám.
