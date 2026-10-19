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
