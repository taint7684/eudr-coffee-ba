# S17 — Test design

Danh sách test case đầy đủ: [S17-test-cases.csv](S17-test-cases.csv) (88 TC). RTM: [S17-rtm.csv](S17-rtm.csv). Độ phủ: [S17-coverage.md](S17-coverage.md).
Nguồn dữ liệu TC: [04-solution/trace/tc_design.csv](../04-solution/trace/tc_design.csv) và [ac.csv](../04-solution/trace/ac.csv). Sinh lại bằng `py 04-solution/trace/build_rtm.py`.

| Nhóm | Kỹ thuật | Mã TC | Số TC |
|---|---|---|:-:|
| Chấm rủi ro lô | Bảng quyết định | TC-001…008 | 8 |
| Ngưỡng định lượng | Giá trị biên | TC-009…025 | 17 |
| Trường nhập chính | Phân vùng tương đương | TC-026…030 | 5 |
| Chức năng | Mỗi AC một TC | TC-101…158 | 58 |

## 1. Bảng quyết định — chấm rủi ro lô (SRS §4.1)

Điều kiện: C1 giao rừng 2020 ≥ 10% · C2 có mất cây che phủ sau 31/12/2020 · C3 mất nằm trong phần giao · C4 cách vùng mất/rìa rừng < 50 m.

| # | C1 | C2 | C3 | C4 | Kết quả | Quy tắc | TC |
|---|:-:|:-:|:-:|:-:|---|---|---|
| 1 | N | N | — | N | Đạt | R1 | TC-001 |
| 2 | N | N | — | Y | Vùng xám | R5 | TC-005 |
| 3 | N | Y | — | — | Vùng xám | R2 | TC-002, TC-007 |
| 4 | Y | N | — | — | Vùng xám | R3 | TC-003 |
| 5 | Y | Y | N | — | Vùng xám | R3 | TC-008 |
| 6 | Y | Y | Y | — | Loại | R4 | TC-004 |
| 7 | Hình học không hợp lệ / > 4 ha không có đa giác | | | | Chưa chấm | R6 | TC-006 |

Mọi tổ hợp của C1–C4 đều quy về 7 dòng trên. Dấu "—" là điều kiện không ảnh hưởng tới kết quả.

## 2. Giá trị biên

| Tham số | Giá trị thử | Kỳ vọng | TC |
|---|---|---|---|
| Diện tích (ngưỡng đa giác 4 ha) | 3,99 · 4,00 · 4,01 ha | Điểm hợp lệ · hợp lệ · bắt buộc đa giác | TC-009…011 |
| Năm mất cây che phủ | 2020 · 2021 | Không tính · tính là sau mốc | TC-012, TC-013 |
| Ngày của bằng chứng xác minh | 30/12/2020 · 31/12/2020 · 01/01/2021 | Chấp nhận · chấp nhận · không đủ | TC-014…016 |
| Khoảng cách vùng đệm | 49 · 50 · 51 m | Vùng xám · Đạt · Đạt | TC-017…019 |
| Lệch diện tích | 20% · 21% | Không cảnh báo · cảnh báo | TC-020 |
| Chồng lấn | 10% · 11% | Cho lưu · chặn | TC-021 |
| Sản lượng lô 1,0 ha (tối đa 3,5 t/ha) | 3.500 · 3.501 kg | Lưu · cảnh báo | TC-022 |
| Tuổi Vùng xám | 14 · 15 ngày | Không cảnh báo · cảnh báo | TC-023 |
| Thời gian tới ngày tàu, chưa có số tham chiếu | 5 · 4 ngày | Không cảnh báo · cảnh báo | TC-024 |
| Số chữ số thập phân của tọa độ | 5 · 6 | Từ chối · lưu | TC-025 |

## 3. Phân vùng tương đương

| Trường | Lớp hợp lệ | Lớp không hợp lệ | TC |
|---|---|---|---|
| Diện tích khai báo | (0; 4] · (4; 50] | ≤ 0 · > 50 (cảnh báo) | TC-026 |
| Khối lượng giao dịch | 1–50.000 kg | ≤ 0 · > 50.000 | TC-027 |
| Pháp lý khi lập gói | Đủ | Thiếu · Mâu thuẫn | TC-028 |
| Kết quả chấm khi lập gói | Đạt | Vùng xám · Loại · Chưa chấm | TC-029 |
| Khoảng cách ảnh xác minh | ≤ 100 m | > 100 m | TC-030 |

## 4. Môi trường và dữ liệu

- Dữ liệu: [S16 synthetic data](../04-solution/S16-synthetic-data/) (seed 2026), có các ca biên LO-00001 (4,00 ha), LO-00002 (4,01 ha), lô thiếu giấy tờ, lô mâu thuẫn diện tích.
- Prototype: [docs/prototype/](../docs/prototype/index.html). Đã chạy kiểm thử khói bằng trình duyệt tự động: 7 màn mở được, không có lỗi JavaScript; luồng phân bổ → kiểm tra → lập gói DDS chạy đúng.
