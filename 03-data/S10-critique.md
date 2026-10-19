# S10 — Báo cáo phản biện dữ liệu

> Trả lời **RQ3**: dữ liệu vệ tinh công khai tin được đến đâu, và xử lý chỗ không chắc chắn thế nào.

## 1. So nguồn và độ nhạy (T8.1)

### 1a. Độ nhạy theo ngưỡng tán (đã tính, [threshold_sensitivity.csv](processed/threshold_sensitivity.csv))

EUDR định nghĩa rừng ở ngưỡng tán > 10% (Điều 2(4)), còn GFW mặc định 30%.

| Ngưỡng tán | Mất 2021–2025, toàn tỉnh (ha) | So với 30% |
|---|---:|---:|
| 10% (sát định nghĩa EUDR) | 18.416 | +16% |
| 30% (mặc định GFW, dùng trong S9) | 15.873 | — |
| 50% | 13.233 | −17% |

Huyện nhạy nhất: Ea Súp (×1,95), Buôn Đôn (×1,67). Đây là vùng rừng khộp thưa, nhiều diện tích có độ tán 10–30%.
**Kết luận:** dùng ngưỡng 30% làm số liệu chính sẽ **đánh giá thấp** rủi ro ở vùng rừng khộp phía tây. Hệ thống ECTS chấm lô bằng bản đồ rừng 2020 (đã theo định nghĩa EU), không dùng ngưỡng tán.

### 1b. Hansen so với bản đồ rừng 2020 của EU — Hướng mở rộng (DEC-08)

- Đây là phân tích độ nhạy giữa hai bộ dữ liệu. Hai bộ khác nhau về định nghĩa, phạm vi và phương pháp, nên không bộ nào được dùng để "xác nhận" bộ kia.
- **Giả thuyết:** ở vùng lõi cà phê (Cư M'gar, Krông Búk, Krông A Na), tỷ lệ mất cây che phủ 2021+ nằm trong đất mà JRC GFC2020 coi là rừng năm 2020 là thấp. Nghĩa là phần lớn số mất là chặt, tái canh cây lâu năm hoặc cây che bóng trên đất đã canh tác, không phải phá rừng theo Điều 2(3), 2(6).
- **Cách làm sẵn có:** (A) script GEE [notebooks/T8.1_hansen_vs_gfc2020.js](notebooks/T8.1_hansen_vs_gfc2020.js); (B) không dùng GEE: tải raster JRC TMF/GFC2020 và kiểm tra trong QGIS trên một vùng nhỏ.
- Không chặn luồng chính: hệ thống chấm lô (BR-010…014) vẫn dùng cả hai lớp, và lô có kết quả trái nhau vào Vùng xám.

### 1c. Hai nguồn số liệu thương mại

UN Comtrade (Việt Nam báo cáo) cho năm 2023: 1,08 triệu tấn, 3,18 tỷ USD. Số này thấp hơn số Hải quan VN thường được báo chí trích [Inference, cần đối chiếu số Hải quan]. Business case dùng **khoảng** min–max của 2021–2023, không dùng một năm.

## 2. Chất lượng dữ liệu (T8.2) — thang 1–3

| Bộ (S8) | Đầy đủ | Chính xác | Kịp thời | Nhất quán | Lý do chính |
|---|:-:|:-:|:-:|:-:|---|
| D-01 Hansen/GFW | 3 | 2 | 3 | 2 | Đủ 15 huyện, có số đến 2025; đo cây che phủ chứ không đo rừng; phương pháp đổi giữa các phiên bản |
| D-02 Nguyên nhân 1 km | 3 | 2 | 3 | 2 | Phủ đủ; 1 km quá thô so với lô 1 ha |
| D-03 JRC GFC2020 | 3 | 2 | 2 | 3 | 10 m, đúng mốc 2020; có danh sách lỗi đã biết, nông lâm kết hợp dễ bị nhầm thành rừng |
| D-05 Niên giám | 3 | 3 | 2 | 3 | Đủ 15 huyện, 2020–2024, số chính thức; trễ khoảng 1 năm |
| D-06 Comtrade | 2 | 2 | 1 | 2 | Thiếu 2024–2025; lệch với số Hải quan |
| D-09 geoBoundaries | 3 | 2 | 2 | 3 | Đơn giản hóa; ranh giới trước 01/7/2025 |

## 3. Quy tắc Vùng xám (T8.3) → chuyển thành BR ở SRS

Nguyên tắc: **khi dữ liệu không chắc, hệ thống không tự kết luận.** Lô Vùng xám chờ xác minh và không được đưa vào gói DDS.

| # | Điều kiện | Kết quả | BR |
|---|---|---|---|
| R1 | Lô không giao rừng 2020 · không có mất cây che phủ sau 31/12/2020 trong lô · cách vùng mất/rìa rừng ≥ 50 m | **Đạt** | BR-010 |
| R2 | Lô không giao rừng 2020 · **có** mất cây che phủ sau 2020 trong lô | **Vùng xám** (khả năng cao là chặt cây che bóng/tái canh; cần ảnh lịch sử) | BR-011 |
| R3 | Lô **giao** rừng 2020 · không có mất cây che phủ sau 2020 | **Vùng xám** (bản đồ có thể nhầm nông lâm kết hợp thành rừng) | BR-012 |
| R4 | Lô **giao** rừng 2020 · **có** mất cây che phủ sau 2020 | **Loại** (tạm khóa; chỉ mở khi xác minh chứng minh đất đã canh tác trước 31/12/2020) | BR-013 |
| R5 | Không thuộc R2–R4 nhưng cách vùng mất/rìa rừng < 50 m | **Vùng xám** (ven rìa, vượt sai số GPS và pixel) | BR-014 |
| R6 | Tọa độ không hợp lệ, hoặc lô > 4 ha không có đa giác | **Chưa chấm** | BR-002, BR-003 |

- Ngưỡng 50 m = ASM-13 (min 30, max 100 m). Tỷ lệ "giao" tính theo diện tích lô ≥ 10% [ASM-13 mở rộng, cần xác định ở SRS].
- Xác minh Vùng xám: (1) đối chiếu ảnh lịch sử 2019–2021 tại bàn; (2) nếu chưa kết luận được thì khảo sát thực địa có ảnh gắn tọa độ. SLA ≤ 14 ngày (KPI ở S18).

## 4. Tự phản biện theo ba góc nhìn (T8.4)

| Góc nhìn | Điểm yếu được chỉ ra | Đánh giá | Xử lý |
|---|---|---|---|
| **Nhà nhập khẩu EU** | 1. Chỉ số huyện không chứng minh được lô nào sạch | Đúng | Đã nêu rõ là chỉ số sàng lọc (DEC-06); chứng minh ở mức lô bằng R1–R6 |
| | 2. Ngưỡng 30% đánh giá thấp mất rừng thưa | Đúng | Thêm 1a; hệ thống chấm theo GFC2020 |
| | 3. Không chứng minh được tính hợp pháp đất | Đúng | Thêm chiều "pháp lý" vào chấm lô (BR-020…) |
| | 4. VN rủi ro thấp thì không cần chấm rủi ro | Sai một phần | Điều 9(1)(g) vẫn đòi bằng chứng; Điều 13(2) có thể kích hoạt thẩm định đầy đủ (DEC-04) |
| | 5. Dữ liệu 2025 có thể bị hiệu chỉnh | Đúng | Ghi giới hạn S9 §5; chạy lại script khi GFW cập nhật |
| **Thương lái** | 6. Hệ thống loại thương lái khỏi chuỗi | Đúng một phần | Thiết kế vai trò "điểm thu mua đã đăng ký": thương lái được nhập giao dịch nếu khai nguồn lô |
| | 7. Thu tọa độ tốn thời gian, không ai trả tiền | Đúng | Chi phí tính vào business case; DN chịu chi phí thu tọa độ (ASM-16) |
| | 8. Nông hộ không có smartphone | Đúng một phần | Đại lý thu tọa độ thay nông hộ (persona đại lý) |
| | 9. Hàng ít, tách dòng không đáng | Đúng | Cho phép mô hình cân bằng khối lượng có kiểm soát ở R2 [cần làm rõ tính hợp lệ theo EUDR — câu hỏi S20] |
| | 10. Dữ liệu cá nhân bị lộ | Đúng | Ma trận phân quyền + mục dữ liệu cá nhân (S15) |
| **Kiểm lâm** | 11. Ranh giới GPS khác hồ sơ địa chính | Đúng | Phụ lục Rule conflicts ở SRS |
| | 12. Định nghĩa rừng VN khác EUDR | Đúng | REQ-EU-005 ✏️; hệ thống theo định nghĩa EU |
| | 13. Mất cây che phủ do khai thác rừng trồng hợp pháp | Đúng | F4 (S9): M'Đrắk/Krông Bông chủ yếu do khai thác gỗ, không gán cho cà phê |
| | 14. Huyện cũ không còn | Đúng | DEC-05; địa chỉ lô dùng xã mới |
| | 15. Không có số liệu hiện trường | Đúng | Giới hạn của dự án (không khảo sát thực địa) |

## 5. Năm giả định yếu nhất

| ASM | Giả định | Tin cậy | Vì sao nguy hiểm |
|---|---|:-:|---|
| ASM-07 | Mất cây che phủ ≈ mất rừng | L | Có thể thổi phồng rủi ro ở vùng lõi cà phê, nơi gần 100% số mất là do nông nghiệp |
| ASM-21 | Đắk Lắk chiếm 25–33% xuất khẩu cà phê VN | M | Quyết định cả hai lăng kính của giá trị bị đe dọa; tính theo diện tích, chưa theo sản lượng xuất khẩu |
| ASM-13 | Vùng đệm 50 m | L | Quyết định tỷ lệ Vùng xám, tức chi phí xác minh |
| ASM-16 | Chi phí thu tọa độ/lô | L | Tham số nhạy nhất của business case [Inference, kiểm ở T16.4] |
| ASM-01 | 30.000 t/năm | L | Định cỡ toàn bộ business case |

Risk register: 10 rủi ro ([risk-register.csv](../00-management/risk-register.csv)).
