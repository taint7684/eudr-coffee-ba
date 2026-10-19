# S17 — Kịch bản UAT

Chạy trên prototype ([docs/prototype/](../docs/prototype/index.html)) với dữ liệu S16. Ngày giả lập của hệ thống: 08/12/2026.
Cột **Kết quả** để người kiểm thử ghi Đạt/Không đạt và ngày chạy.

| # | Mục tiêu | Tiền điều kiện | Các bước | Kết quả mong đợi | US / AC | Kết quả |
|---|---|---|---|---|---|---|
| UAT-01 | Đại lý đăng ký nông hộ mới | Vai trò Đại lý | SCR-01 → Thêm nông hộ → nhập đủ trường, bỏ chọn đồng ý → Lưu → chọn đồng ý → Lưu | Lần 1 bị chặn với lỗi đồng ý; lần 2 tạo NH-xxxxx; audit có bản ghi | US-001 · AC-001.1, AC-001.2 | |
| UAT-02 | Lô ≤ 4 ha dùng điểm GPS | Vai trò Đại lý | SCR-02 → diện tích 1,20 → Lấy điểm GPS → bấm bản đồ → Lưu | Tọa độ 6 chữ số thập phân; lô được chấm tự động | US-002 · AC-002.1 | |
| UAT-03 | Lô > 4 ha bắt buộc đa giác | Vai trò Đại lý | SCR-02 → diện tích 4,01 → kiểm tra nút Lấy điểm → vẽ đa giác 4 đỉnh → Lưu | Nút Lấy điểm bị khóa; đa giác lưu được; lệch > 20% thì phải chọn lý do | US-002, US-003, US-004 · AC-002.3, AC-003.1, AC-004.2 | |
| UAT-04 | Đa giác tự cắt và chồng lấn bị chặn | Vai trò Đại lý | Vẽ đa giác hình số 8; sau đó vẽ đè lên một lô đã có | Báo "Đa giác tự cắt"; báo chồng lấn và tô đỏ lô trùng | US-003, US-004 · AC-003.2, AC-004.1 | |
| UAT-05 | Hiểu lý do kết quả chấm | Vai trò Tuân thủ | SCR-03 → chọn một lô R3 và một lô R5 | Thấy quy tắc, % giao rừng 2020, khoảng cách, phiên bản dữ liệu, bản đồ | US-009 · AC-009.1, AC-009.2 | |
| UAT-06 | Hàng đợi Vùng xám theo SLA | Vai trò Tuân thủ | SCR-03 → xem hàng đợi | Sắp theo tuổi; lô > 14 ngày ghi "Quá hạn" | US-010 · AC-010.1, AC-010.2 | |
| UAT-07 | Quyết định Vùng xám phải có bằng chứng | Vai trò Tuân thủ | Chọn lô Vùng xám → chọn Đạt, không đính kèm → Ghi → đính kèm ảnh, ngày 15/06/2019, lý do → Ghi | Lần 1 bị chặn; lần 2 lô chuyển Đạt; SCR-07 audit có trước/sau | US-011, US-029 · AC-011.1, AC-011.2, AC-029.1 | |
| UAT-08 | Lô chưa đủ điều kiện không vào dòng EU | Vai trò Đại lý | SCR-04 → chọn nông hộ có lô Vùng xám → chọn lô đó | Dòng EU bị khóa, có thông báo BR-030 | US-016 · AC-016.2 | |
| UAT-09 | Cảnh báo vượt sản lượng tối đa | Vai trò Đại lý | SCR-04 → lô nhỏ đã bán gần tối đa → ghi thêm 5.000 kg | Giao dịch lưu ở trạng thái chờ Tuân thủ xác nhận | US-017 · AC-017.1 | |
| UAT-10 | Phân bổ không vượt khối lượng phiếu | Vai trò Thu mua | SCR-05 → SH-2026-014 → nhập phân bổ lớn hơn "Còn lại" → Lưu → sửa đúng → Lưu | Lần 1 báo vượt; lần 2 lưu; thẻ "tấn khả dụng" giảm tương ứng | US-019, US-020 · AC-019.1, AC-020.1 | |
| UAT-11 | Lập gói DDS và theo dõi số tham chiếu | Vai trò Tuân thủ, sau UAT-10 | SCR-05 → kiểm tra 4 điều kiện → Lập & tải gói → mở tệp GeoJSON → nhập số tham chiếu → Ghi chấp nhận | Tệp có `hs_code` 0901, `net_mass_kg`, `country_of_production` VN, Point/Polygon từng lô; trạng thái Đã gửi → Được chấp nhận; có hạn lưu 5 năm | US-022, US-024, US-025, US-027 · AC-022.1, AC-022.2, AC-024.1, AC-025.1 | |
| UAT-12 | Từ chối DDS đưa lô hàng về Nháp | Vai trò Tuân thủ | Lô hàng Đã gửi → Ghi từ chối, lý do "Thiếu đa giác lô LO-xxxxx" | Trạng thái về Nháp; lý do hiển thị; lịch sử có dòng từ chối | US-026 · AC-026.1 | |
| UAT-13 | Phân quyền theo vai trò | Đổi vai trò lần lượt | Đại lý mở SCR-05; Thu mua mở SCR-02; Tuân thủ sửa tham số SCR-07 | Đại lý và Thu mua thấy "Không có quyền"; Tuân thủ không sửa được tham số | US-030 · AC-030.1 | |
| UAT-14 | Đổi tham số có hiệu lực và ghi audit | Vai trò Quản lý | SCR-07 → vùng đệm 50 → 30 → Lưu → SCR-03 xem lô R5 | Tham số mới hiển thị ở chi tiết lô; audit ghi 50 → 30 | US-031 · AC-031.1 | |

**Tiêu chí chấp nhận UAT:** 14/14 kịch bản Đạt. Không có lỗi mức Nghiêm trọng. Lỗi mức Trung bình có kế hoạch sửa trước R2.
