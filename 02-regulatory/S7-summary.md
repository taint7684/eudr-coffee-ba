# S7 — Ma trận yêu cầu EUDR & gap analysis

> Ma trận đầy đủ: [S7-eudr-requirements.csv](S7-eudr-requirements.csv) · 40 yêu cầu · nguyên văn trích tự động từ văn bản gốc bằng [scripts/build_s7.py](scripts/build_s7.py).
> Not legal advice.

## 1. Phạm vi đọc (T3.1)

| Văn bản | Mã nguồn | Phần đã đọc |
|---|---|---|
| Regulation (EU) 2023/1115 — bản gốc | SRC-001 | Điều 2–13, 29, Phụ lục II |
| Regulation (EU) 2025/2650 — sửa đổi | SRC-003 | Toàn bộ Điều 1 (sửa Điều 2–6, 8–9, 16, 18–19, 24–28, 31, 33–35, 37–38; thêm Điều 4a, Phụ lục III) |
| Implementing Regulation (EU) 2025/1093 | SRC-004 | Phụ lục — danh sách quốc gia |
| Regulation (EU) 2024/3234 | SRC-002 | Đã bị 2025/2650 thay phần ngày áp dụng |

**Lý do chọn:** chỉ giữ các điều tác động tới chuỗi cà phê nhập khẩu từ nước thứ ba: định nghĩa, điều kiện đưa hàng vào thị trường, nghĩa vụ operator/downstream, thẩm định, xếp hạng quốc gia, kiểm tra, ngày áp dụng.
**Bản hợp nhất:** EUR-Lex chưa có bản hợp nhất sau 2025/2650 tại ngày truy cập [Unverified]. S7 ghép bản gốc với văn bản sửa đổi; cột `article` ghi rõ "(sửa bởi 2025/2650)".

## 2. Bốn điều cần nắm trước khi đọc ma trận

| # | Sự kiện | Căn cứ | Hệ quả thiết kế |
|---|---|---|---|
| 1 | Ngày áp dụng: **30/12/2026**; DN siêu nhỏ/nhỏ thành lập trước 31/12/2024: **30/06/2027** | Điều 38(2)–(3) mới | Tham số hóa ngày áp dụng |
| 2 | Việt Nam được xếp **rủi ro thấp** | IR 2025/1093, Phụ lục | Operator được thẩm định đơn giản hóa (Điều 13) nhưng **vẫn cần** tọa độ mọi lô (9(1)(d)) và bằng chứng không phá rừng (9(1)(g)) → DEC-04 |
| 3 | DN xuất khẩu VN **không phải operator**; nhà nhập khẩu EU nộp DDS | Điều 2(15), 7, 6, 2(22) | ECTS sinh gói dữ liệu DDS, không tự nộp → DEC-03 |
| 4 | Đồn điền nông nghiệp, kể cả nông lâm kết hợp, **không phải rừng** | Điều 2(4), 2(6) | Mất cây che phủ ≠ phá rừng; cần quy tắc Vùng xám → DEC-06 |

## 3. Kết quả chấm mức sẵn sàng (T3.3)

| Mức | Ý nghĩa | Số yêu cầu |
|---|---|---|
| ⛔ | Chưa đáp ứng | 14 |
| ⚠️ | Đáp ứng một phần / phụ thuộc bên khác | 12 |
| ✏️ | Cần làm rõ hoặc diễn giải | 14 |
| | **Tổng** | **40** |

Mọi dòng ⛔ đều trỏ tới ít nhất một GAP (S5) và một RC (S6).

## 4. Năm khoảng trống lớn nhất

| # | Khoảng trống | REQ-EU | GAP · RC | Bằng chứng |
|---|---|---|---|---|
| 1 | **Không có tọa độ lô.** Chỉ khoảng 1/10 nông hộ được khảo sát giữ dữ liệu cấp lô. | 007, 020, 038 | GAP-01 · RC-03 | SRC-027 |
| 2 | **Hàng bị trộn qua 4–5 tầng** nên không liệt kê được "mọi lô" cho một lô hàng. Điều này cũng làm mất điều kiện của thẩm định đơn giản hóa (13(1)). | 012, 020, 027, 028, 033 | GAP-02, GAP-03 · RC-01, RC-04 | [Inference] |
| 3 | **Không có bằng chứng "không phá rừng" kiểm chứng được** (chồng lớp với bản đồ rừng 2020 và mất cây che phủ sau 2020). | 001, 004, 023 | GAP-04 · RC-06 | SRC-011 |
| 4 | **Hồ sơ quyền sử dụng đất không số hóa hoặc thiếu**, nên không chứng minh được tính hợp pháp. | 002, 008, 024 | GAP-05 · RC-05 | SRC-027 |
| 5 | **Không có kênh dữ liệu sang operator EU** (gói DDS, số tham chiếu, lưu 5 năm). Hàng bị giữ tại hải quan EU nếu thiếu số tham chiếu. | 003, 010, 017, 032, 036 | GAP-06 · RC-02 | DEC-03 |

## 5. Chỗ cần làm rõ (✏️) quan trọng

- **Định nghĩa rừng VN và EU:** cần trích Luật Lâm nghiệp 2017 để so ngưỡng diện tích, chiều cao và độ che phủ [Unverified].
- **Lô EUDR và thửa đất:** quy ước 1 lô = 1 thửa trên giấy chứng nhận, hoặc 1 vùng canh tác liền khoảnh nếu không có giấy. Xử lý ở SRS (Rule conflicts).
- **Nông lâm kết hợp:** cà phê xen cây che bóng. Quy tắc phân loại lô đặt ở S10, mục 3.
- **Một DDS cho nhiều lô hàng:** Guidance/FAQ cập nhật kèm báo cáo rà soát COM(2026) 191 cho phép một DDS bao nhiều lô hàng (SRC-005). Gói dữ liệu ECTS vì vậy có thể gộp nhiều lô hàng của cùng nhà nhập khẩu (Hướng mở rộng của FR-017).
- **Tờ khai đơn giản hóa (Điều 4a):** không áp dụng cho luồng chính vì nông hộ không tự đưa hàng vào EU.

## 6. Việc người thực hiện phải tự kiểm chứng

1. Mở SRC-001, SRC-003 trên EUR-Lex và đối chiếu ngẫu nhiên 10 dòng `verbatim_text`.
2. Kiểm tra trên EUR-Lex xem đã có bản hợp nhất sau 2025/2650 chưa.
3. Đọc bản gốc COM(2026) 191 (SRC-005): có đề xuất nào ảnh hưởng tới cà phê không.
4. Xác nhận các đánh giá `vn_current_state` gắn nhãn [Inference] bằng báo cáo IDH (SRC-023) và Forest Trends (SRC-027).

## 7. Sau giải pháp: 14/14 yêu cầu ⛔ đều có chức năng xử lý

Mức ⛔ / ⚠️ / ✏️ ở trên mô tả **hiện trạng chuỗi cà phê VN (As-Is)**, không phải lỗi của dự án. Bảng dưới cho biết chức năng ECTS nào đáp ứng từng yêu cầu ⛔ và ở đợt nào. Truy vết đầy đủ tới test case: [S17-rtm.csv](../05-test/S17-rtm.csv) · [S17-coverage.md](../05-test/S17-coverage.md).

| REQ-EU | Điều | Hiện trạng | Chức năng xử lý (đợt) |
|---|---|---|---|
| 003 | 3(c) | ⛔ Không có gói dữ liệu cho DDS | FR-017 (R2) |
| 004 | 2(13) | ⛔ Không có bằng chứng hiện trạng đất tại 31/12/2020 | FR-008 (MVP) |
| 007 | 2(28) | ⛔ Không có tọa độ lô | FR-002, FR-003, FR-004 (MVP) · FR-006 (R2) |
| 010 | 4(2) | ⛔ Không chuyển được dữ liệu cho nhà nhập khẩu lập DDS | FR-017 (R2) |
| 012 | 4(4) | ⛔ Hàng trộn, không tách được lô | FR-010 (MVP) · FR-013 (R2) |
| 017 | 9(1) | ⛔ Không lưu bằng chứng theo lô hàng | FR-017, FR-020 (R2) |
| 020 | 9(1)(d) | ⛔ Không liệt kê được mọi lô của lô hàng | FR-002, FR-003 (MVP) · FR-013, FR-017 (R2) · FR-007 (R3) |
| 023 | 9(1)(g) | ⛔ Không có quy trình chồng lớp bản đồ rừng | FR-008 (MVP) · FR-017 (R2) |
| 024 | 9(1)(h) | ⛔ Giấy tờ đất thiếu / không số hóa | FR-005, FR-011 (MVP) · FR-017 (R2) |
| 027 | 10(2)(i) | ⛔ Chuỗi 4–5 tầng, mất liên kết lô | FR-013, FR-014 (R2) |
| 028 | 10(2)(j) | ⛔ Kho trộn hàng nhiều nguồn | FR-015 (R2), mô hình tách dòng (DEC-07) |
| 032 | 12(5) | ⛔ Không có kho hồ sơ 5 năm | FR-022 (MVP) · FR-020 (R2) |
| 038 | Phụ lục II-3 | ⛔ DDS thiếu tọa độ mọi lô | FR-002, FR-003 (MVP) · FR-017 (R2) |
| 040 | 38(2) | ⛔ Còn khoảng 2 tháng tới ngày áp dụng | FR-024 (MVP), tham số hóa ngày áp dụng |

Các yêu cầu ⚠️ và ✏️ được xử lý qua FR tương ứng (xem cột `req_eu` trong [fr.csv](../04-solution/trace/fr.csv)) hoặc qua quyết định diễn giải (DEC-03 đến DEC-07). Hai yêu cầu nằm ngoài phạm vi có lý do: REQ-EU-014, REQ-EU-039.
