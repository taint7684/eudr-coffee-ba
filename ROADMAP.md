# ROADMAP — EUDR-Ready Coffee

**Đề tài:** EUDR-Ready: Thiết kế giải pháp truy xuất nguồn gốc "không phá rừng" cho chuỗi cà phê nông hộ Đắk Lắk
**Loại dự án:** portfolio Senior Business Analyst · một người · bán thời gian (8–10 giờ/tuần) · tuần 0 + 18 tuần · chi phí 0đ
**Tiến độ chi tiết từng task (T0.1 → T18.7):** [00-management/tasks.csv](00-management/tasks.csv)

## 1. Bài toán

EUDR yêu cầu cà phê vào EU không đến từ đất phá rừng sau 31/12/2020, được sản xuất hợp pháp và có DDS kèm tọa độ từng lô. Cà phê VN chủ yếu do nông hộ nhỏ trồng, qua nhiều tầng trung gian và bị trộn, nên DN xuất khẩu khó chứng minh nguồn gốc. Dự án đóng vai BA cho một DN xuất khẩu giả định ở Đắk Lắk.

| Mã | Câu hỏi nghiên cứu | Sản phẩm trả lời |
|---|---|---|
| RQ1 | EUDR yêu cầu gì, chuỗi cà phê VN thiếu ở đâu? | S7 |
| RQ2 | Rủi ro tập trung ở huyện nào, giá trị nào bị đe dọa? | S9 |
| RQ3 | Dữ liệu vệ tinh công khai tin được đến đâu? | S10 |
| RQ4 | Hệ thống truy xuất cần đáp ứng gì để DN cung cấp dữ liệu DDS? | S11–S17 |
| RQ5 | Nên đầu tư phương án nào, khi nào không đáng? | S18 |

**Phạm vi:** Robusta · Đắk Lắk (ranh giới trước 07/2025) · luồng đăng ký lô → thu mua → chấm rủi ro → gói dữ liệu DDS · thiết kế mức SRS + prototype + test.
**Ngoài phạm vi (Hướng mở rộng):** cao su, gỗ, các tỉnh khác · logistics, thanh toán, chứng nhận 4C/RA · viết code, triển khai thật · dữ liệu nội bộ DN.

## 2. Giai đoạn và mốc

| Giai đoạn | Tuần | Sản phẩm | Mốc | Trạng thái |
|---|---|---|---|---|
| P0 Chuẩn bị | 0 | Repo, file quản lý, kiểm tra khả thi (DEC-01) | — | Xong |
| P1 Discovery | 1–3 | S1–S7 | M1 | Tài liệu xong; chờ review #1, bài LinkedIn #1, release v0.1-M1 |
| P2 Dữ liệu | 4–7 | S8, S9, dashboard | — | Xong; chờ niên giám (diện tích cà phê theo huyện) |
| P3 Phản biện | 8 | S10 | M2 | Xong; chờ chạy script GEE (T8.1b), bài LinkedIn #2 |
| P4 Thiết kế | 9–15 | S11–S17 | M3 | Xong; chờ vẽ BPMN .bpmn, review #2 |
| P5 Business case | 16–17 | S18 | — | Xong |
| P6 Đóng gói | 18 | S19, S20, README | M4 | Tài liệu xong; chờ đăng case study, video demo, release v1.0 |

## 3. Checklist mốc

**M1 (tuần 3)**
- [x] S1–S7 trên GitHub
- [x] README có Problem, Scope, Disclaimer
- [ ] Review #1 đã ghi và xử lý
- [ ] Bài LinkedIn #1
- [ ] Release v0.1-M1

**M2 (tuần 8)**
- [x] S8–S10; dashboard trong `docs/`
- [ ] Bật GitHub Pages
- [ ] Bài LinkedIn #2
- [ ] Release v0.2-M2

**M3 (tuần 15)**
- [x] S11–S17
- [x] Mọi REQ-EU ⛔ đi tới TC trong RTM (14/14)
- [ ] Backlog trên GitHub Projects (chạy `tools/github_setup.py`)
- [ ] Review #2
- [ ] Release v0.3-M3

**M4 (tuần 18) — định nghĩa hoàn thành dự án**
- [x] S1–S20 có trên GitHub (trừ một mục S19 đang chờ quyết định)
- [x] Mọi số liệu có SRC, mọi giả định có ASM
- [x] RTM đầy đủ hai chiều
- [ ] Mọi link (Pages, video) mở được ở cửa sổ ẩn danh
- [ ] Có 3 bài đăng
- [ ] Một người ngoài đọc README và nói lại được dự án trong 2 phút
- [ ] Release v1.0

## 4. Nhịp làm việc

| Chu kỳ | Việc |
|---|---|
| Cuối mỗi tuần | Chuyển issue sang Done · kiểm tra số liệu thiếu nguồn · commit |
| Tuần 4 · 8 · 12 · 16 | Kiểm tra EUR-Lex và trang EC xem EUDR có thay đổi không; có thì ghi risk-register và cập nhật S7 |
| Tuần 3 · 15 | Nhờ người review |

## 5. Danh sách cắt khi chậm hơn 1 tuần (cắt từ trên xuống)

1. Video demo → chuỗi ảnh có chú thích
2. So hai nguồn → giữ một nguồn, ghi giới hạn
3. GEE → chỉ dùng số GFW
4. Mock 5 màn → 3 màn (SCR-02, SCR-03, SCR-05)
5. Phương án C → chỉ so A và B
6. Persona nông hộ → gộp vào persona đại lý

**Không bao giờ cắt:** S7 · S10 · S17 RTM · T17.2.

## 6. Nguyên tắc chất lượng

1. Không có nguồn thì không dùng: mọi số liệu có mã SRC.
2. Giả định phải ghi ra: mã ASM, mức tin cậy, min/likely/max, hệ quả nếu sai.
3. Yêu cầu từ luật trích nguyên văn, có số điều khoản.
4. Dữ liệu giả lập ghi rõ là synthetic trong tên file và nội dung.
5. Ước lượng dùng khoảng, không dùng một con số.
6. Tương quan không phải nhân quả.
