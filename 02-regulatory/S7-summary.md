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

## 7. Sau giải pháp: 14/14 yêu cầu ⛔ và 12/12 yêu cầu ⚠️ đều có lời giải

Mức ⛔ / ⚠️ / ✏️ ở trên mô tả **hiện trạng chuỗi cà phê VN (As-Is)**, không phải lỗi của dự án. Hai bảng dưới cho biết hệ thống ECTS xử lý từng yêu cầu thế nào, bằng chức năng (FR) và quy tắc (BR) nào, và có bao nhiêu test case kiểm chứng. Nguồn: [fr.csv](../04-solution/trace/fr.csv) · [br.csv](../04-solution/trace/br.csv) · [S17-rtm.csv](../05-test/S17-rtm.csv).

### 7.1 Yêu cầu ⛔ (ngành chưa đáp ứng)

| REQ-EU | Luật đòi | Hiện trạng ngành | Lời giải của ECTS | FR · BR | TC |
|---|---|---|---|---|---:|
| 003 | Hàng phải có DDS (Điều 3(c)) | Không có gói dữ liệu đủ trường cho DDS | Lập gói dữ liệu DDS (mã HS, khối lượng, tọa độ mọi lô, bằng chứng) gửi nhà nhập khẩu nộp | FR-017 · BR-040, 041 | 6 |
| 004 | Không phá rừng sau 31/12/2020 (2(13)) | Không có bằng chứng hiện trạng đất năm 2020 | Tự động chấm rủi ro lô: chồng lô lên bản đồ rừng 2020 và lớp mất cây che phủ sau 2020, ra Đạt / Vùng xám / Loại (R1–R6) | FR-008 · BR-010…014 | 18 |
| 007 | Tọa độ ≥ 6 chữ số thập phân; lô > 4 ha có đa giác (2(28)) | Khoảng 1/10 nông hộ có dữ liệu lô | Đại lý lấy điểm GPS hoặc vẽ đa giác trên điện thoại, dùng được khi mất sóng; kiểm tra hình học, chồng lấn, lệch diện tích | FR-002, 003, 004, 006 · BR-001…005 | 18 |
| 010 | Không có DDS thì không được bán (4(2)) | Không có kênh chuyển dữ liệu cho nhà nhập khẩu | Gói dữ liệu DDS kèm theo dõi trạng thái gửi | FR-017 · BR-040, 041 | 6 |
| 012 | Cấm bán khi rủi ro chưa xử lý (4(4)) | Hàng trộn, không tách được lô rủi ro | Lô Vùng xám phải được xác minh có bằng chứng; chỉ lô Đạt mới vào dòng EU; cảnh báo lô bán vượt sản lượng | FR-010, 013 · BR-015, 016, 030, 031 | 17 |
| 017 | Thu thập, lưu bằng chứng 5 năm (9(1)) | Ghi sổ, Excel; không lưu theo lô hàng | Gói DDS gom đủ bằng chứng; kho hồ sơ 5 năm, không cho xóa | FR-017, 020 · BR-040, 041, 050 | 8 |
| 020 | Tọa độ của mọi lô trong lô hàng (9(1)(d)) | Không có tọa độ; hàng trộn nhiều hộ | Mỗi giao dịch gắn mã lô; gói DDS liệt kê đủ mọi lô; nhập hàng loạt từ dữ liệu chứng nhận | FR-002, 003, 007, 013, 017 · BR-001…003, 030, 031, 040, 041 | 25 |
| 023 | Bằng chứng kiểm chứng được là không phá rừng (9(1)(g)) | Chưa có quy trình chồng lớp bản đồ | Kết quả chấm lưu kèm quy tắc áp dụng và phiên bản bản đồ, đưa vào gói DDS | FR-008, 017 · BR-010…014, 040, 041 | 24 |
| 024 | Bằng chứng hợp pháp, quyền sử dụng đất (9(1)(h)) | Giấy tờ đất thiếu hoặc chưa số hóa | Nhập số GCN QSDĐ hoặc xác nhận UBND xã; tự đánh giá pháp lý Đủ / Thiếu / Mâu thuẫn; thiếu thì không vào gói DDS | FR-005, 011, 017 · BR-020, 021, 040, 041 | 10 |
| 027 | Đánh giá độ phức tạp chuỗi (10(2)(i)) | Chuỗi 4–5 tầng | Giao dịch ghi từ nông hộ; phiếu nhập kế thừa danh sách lô, không đứt dữ liệu qua các tầng | FR-013, 014 · BR-030, 031, 032 | 7 |
| 028 | Rủi ro trộn với hàng không rõ nguồn (10(2)(j)) | Kho trộn hàng nhiều nguồn | Tách dòng EU: lô hàng chỉ nhận phiếu nhập dòng EU, không phân bổ vượt khối lượng | FR-015 · BR-032, 033 | 3 |
| 032 | Lưu toàn bộ hồ sơ thẩm định 5 năm (12(5)) | Không có kho hồ sơ số | Kho hồ sơ 5 năm và nhật ký thao tác (người, thời điểm, trước/sau) | FR-020, 022 · BR-050, 051 | 3 |
| 038 | DDS ghi tọa độ mọi lô (Phụ lục II mục 3) | Không có | GeoJSON: lô ≤ 4 ha là điểm, lô > 4 ha là đa giác | FR-002, 003, 017 · BR-001…003, 040, 041 | 17 |
| 040 | Áp dụng từ 30/12/2026 (38(2)) | Còn khoảng 2 tháng | Ngày áp dụng là tham số chỉnh được, không phải sửa hệ thống khi luật dời hạn | FR-024 · BR-060 | 2 |

### 7.2 Yêu cầu ⚠️ (đáp ứng một phần hoặc phụ thuộc bên khác)

| REQ-EU | Luật đòi | Hiện trạng | Lời giải của ECTS | FR · BR | TC |
|---|---|---|---|---|---:|
| 001 | Hàng không phá rừng (3(a)) | VN rủi ro thấp nhưng thiếu dữ liệu từng lô | Chấm rủi ro từng lô để có bằng chứng cấp lô | FR-008 · BR-010…014 | 18 |
| 002 | Sản xuất đúng luật nước sở tại (3(b)) | Hồ sơ đất không đầy đủ | Giấy tờ đất và đánh giá pháp lý | FR-005, 011 · BR-020, 021 | 4 |
| 009 | Operator phải thẩm định (4(1)) | Nghĩa vụ của nhà nhập khẩu; DN VN cấp dữ liệu | Gói dữ liệu DDS làm đầu vào thẩm định cho nhà nhập khẩu | FR-017 · BR-040, 041 | 6 |
| 011 | Operator chịu trách nhiệm, lưu DDS 5 năm (4(3)) | Nhà nhập khẩu đòi bằng chứng tương ứng | Ghi số tham chiếu DDS; bị từ chối thì lô hàng về Nháp kèm lý do | FR-019 · BR-042, 043 | 4 |
| 013 | Truyền số tham chiếu DDS xuống chuỗi (4(7)) | DN cần nhận lại số tham chiếu | Lưu số tham chiếu vào hồ sơ lô hàng | FR-019 · BR-042, 043 | 4 |
| 021 | Tên, địa chỉ, email nhà cung cấp (9(1)(e)) | Thương lái thiếu thông tin định danh | Đăng ký nông hộ (có đồng ý dữ liệu) và quản lý đại lý; email bắt buộc | FR-001, 016 · BR-006 | 4 |
| 029 | Rà soát đánh giá rủi ro hằng năm (10(4)) | Không có hồ sơ đánh giá | Chấm lại khi bản đồ có phiên bản mới, giữ kết quả cũ; nhật ký thao tác | FR-009, 022 · BR-017, 051 | 2 |
| 030 | Biện pháp giảm thiểu rủi ro (11(1)) | Chưa có quy trình xác minh thực địa | Quy trình Vùng xám: ảnh lịch sử, thực địa, hạn 14 ngày, bắt buộc bằng chứng | FR-010 · BR-015, 016 | 11 |
| 031 | Duy trì hệ thống thẩm định (12(1)) | Không có | Kho hồ sơ và tra cứu theo lô hàng hoặc lô đất | FR-020 · BR-050 | 2 |
| 033 | Điều kiện thẩm định đơn giản hóa (13(1)) | Thiếu bằng chứng không trộn hàng | Tách dòng EU chứng minh hàng chỉ đến từ lô đã khai, ở Việt Nam | FR-015 · BR-032, 033 | 3 |
| 034 | Có cảnh báo thì phải thẩm định đầy đủ (13(2)) | Không có kênh xử lý cảnh báo | Cảnh báo khi lô đã Đạt có mất cây che phủ mới: lô chuyển Vùng xám, khóa lô hàng chưa xuất | FR-009, 012 · BR-017, 018 | 2 |
| 036 | Số tham chiếu có trước khi thông quan (26(4)) | Thiếu số thì hàng bị giữ ở cảng EU | Cảnh báo khi còn dưới 5 ngày tới ngày tàu đến mà chưa có số tham chiếu | FR-019 · BR-042, 043 | 4 |

Các yêu cầu ✏️ được xử lý qua quyết định diễn giải (DEC-03 đến DEC-07) và FR tương ứng trong [fr.csv](../04-solution/trace/fr.csv). Hai yêu cầu nằm ngoài phạm vi có lý do: REQ-EU-014, REQ-EU-039.
