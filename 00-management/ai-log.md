# AI log

Mỗi dòng: ngày · task · việc giao AI · AI trả gì · sai ở đâu · đã sửa thế nào.
Công cụ AI tạo sinh được dùng để tóm tắt tài liệu dài và soạn bản nháp. Người thực hiện kiểm chứng với nguồn gốc và chốt mọi nội dung.

| Ngày | Task | Việc giao AI | AI trả gì | Sai ở đâu | Đã sửa thế nào |
|---|---|---|---|---|---|
| 2026-10-20 | Đề xuất đề tài | Soạn mô tả đề tài EUDR + cà phê | Bản đề xuất 9 mục, nhãn [Unverified] cho mốc pháp lý | Ghi "độ phân giải 30 m không phân biệt được cà phê xen canh với rừng thứ sinh" như giới hạn chung — bản đồ rừng 2020 của EU (JRC GFC2020) có độ phân giải **10 m** | Ghi rõ độ phân giải từng bộ trong S8; giới hạn 30 m chỉ áp cho Hansen |
| 2026-10-20 | Đề xuất đề tài / ROADMAP 1.7 | Thiết kế 5 nhóm chức năng ECTS | Nhóm 4 "Lập & nộp DDS lên hệ thống EU" | Sai tư cách pháp lý: DN xuất khẩu VN **không phải operator** (Điều 2(15), Điều 7); đại diện ủy quyền phải thành lập tại EU (Điều 2(22), Điều 6) | DEC-03: đổi thành "Lập gói dữ liệu DDS & theo dõi số tham chiếu" |
| 2026-10-20 | ROADMAP 1.2 | Tóm tắt bối cảnh pháp lý | "Ba điều kiện… (3) Có DDS"; "Mốc áp dụng đã bị hoãn ít nhất một lần" | Thiếu: (i) 2025/2650 thêm **tờ khai đơn giản hóa** cho nhà sản xuất siêu nhỏ/nhỏ ở nước rủi ro thấp (Điều 4a, Phụ lục III) — Điều 3(c) nay là "DDS **hoặc** tờ khai đơn giản hóa"; (ii) Việt Nam đã được xếp **rủi ro thấp** từ 05/2025 | Cập nhật S7 (REQ-EU-003, REQ-EU-033, REQ-EU-039), DEC-04 |
| 2026-10-20 | T0.4 | Tìm số mất rừng theo huyện | Gợi ý vào dashboard GFW nhập tay | Dashboard GFW đã chuyển sang globalnaturewatch.org; Data API đòi API key | Tìm được workbook thống kê quốc gia công khai (SRC-008), trích tự động bằng script `03-data/scripts/01_extract_gfw.py` |
| 2026-10-20 | T3.1 | Đoán danh sách điều khoản cần đọc | "Điều 9 (thông tin và tọa độ) · Điều 33 (hệ thống thông tin)…" và "Điều 4–5 nghĩa vụ operator/trader" | Đúng về số điều, nhưng Điều 5 và 6 đã bị **thay toàn bộ** bởi 2025/2650 (thêm *downstream operator*); Điều 4(8)–(10) đã bị xóa | S7 trích theo văn bản đã sửa đổi; cột `article` ghi rõ "(sửa bởi 2025/2650)" |
