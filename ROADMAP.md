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
**Ngoài phạm vi (Hướng mở rộng):** so Hansen × JRC GFC2020 · cao su, gỗ, các tỉnh khác · logistics, thanh toán, chứng nhận 4C/RA · viết code, triển khai thật · dữ liệu nội bộ DN.

## 2. Giai đoạn và mốc

| Giai đoạn | Tuần | Sản phẩm | Mốc | Trạng thái |
|---|---|---|---|---|
| P0 Chuẩn bị | 0 | Repo, file quản lý, kiểm tra khả thi (DEC-01) | — | Xong |
| P1 Discovery | 1–3 | S1–S7 | M1 | Xong |
| P2 Dữ liệu | 4–7 | S8, S9, dashboard | — | Xong (diện tích cà phê theo niên giám 2024, DEC-08) |
| P3 Phản biện | 8 | S10 | M2 | Xong (so Hansen × JRC chuyển Hướng mở rộng, DEC-08) |
| P4 Thiết kế | 9–15 | S11–S17 | M3 | Xong |
| P5 Business case | 16–17 | S18 | — | Xong |
| P6 Đóng gói | 18 | S19, S20, README | M4 | Xong |

## 3. Nguyên tắc chất lượng

1. Không có nguồn thì không dùng: mọi số liệu có mã SRC.
2. Giả định phải ghi ra: mã ASM, mức tin cậy, min/likely/max, hệ quả nếu sai.
3. Yêu cầu từ luật trích nguyên văn, có số điều khoản.
4. Dữ liệu giả lập ghi rõ là synthetic trong tên file và nội dung.
5. Ước lượng dùng khoảng, không dùng một con số.
6. Tương quan không phải nhân quả.
