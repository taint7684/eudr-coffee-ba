# S15 — Đặc tả màn hình

Prototype click được: [docs/prototype/index.html](../../docs/prototype/index.html), chạy trên dữ liệu giả lập S16. Ảnh chụp màn hình: [screens/](screens/).
Quy ước chung: trường có `*` là bắt buộc · ngày dạng dd/mm/yyyy · khối lượng dạng kg, phân tách hàng nghìn bằng dấu chấm · mọi thao tác ghi audit (BR-051).

Trạng thái màn chung: **Trống** (hướng dẫn + nút tạo mới) · **Đang tải** (khung xương) · **Lỗi** (thông báo + Thử lại) · **Không có quyền** (thông báo + liên hệ quản trị, AC-030.1).

---

## SCR-01 — Nông hộ & lô đất

| Mục | Nội dung |
|---|---|
| Mục đích | Tra cứu nông hộ, lô và tình trạng sẵn sàng EUDR của từng lô |
| Người dùng | Đại lý (của mình), Thu mua, Tuân thủ, Quản lý |
| Thao tác | Tìm/lọc · Thêm nông hộ (US-001) · Thêm lô (→ SCR-02) · Nhập hàng loạt (US-007) · Mở chi tiết lô (→ SCR-03) |
| Bộ lọc | Huyện cũ · xã mới · đại lý · kết quả chấm · pháp lý |
| Cột lưới | Mã lô · Nông hộ · Xã · Diện tích (ha) · Hình học (Điểm/Đa giác) · Kết quả chấm · Pháp lý · Cập nhật |

**Form Thêm nông hộ**

| Trường | Kiểu | Bắt buộc | Validate | Nguồn | Thông báo lỗi |
|---|---|:-:|---|---|---|
| Họ tên | Text 100 | * | Không rỗng | Nhập | "Nhập họ tên" |
| Năm sinh | Số | | 1930–năm hiện tại | Nhập | "Năm sinh không hợp lệ" |
| Số định danh | Text 12 | | 12 chữ số | Nhập | "Số định danh gồm 12 chữ số" |
| Điện thoại | Text | * | 10 chữ số, bắt đầu 0 | Nhập | "Số điện thoại không hợp lệ" |
| Xã (mới) | Chọn | * | Danh mục xã | Danh mục | "Chọn xã" |
| Đại lý phụ trách | Chọn | * | Tự điền với vai trò Đại lý | Phiên đăng nhập | — |
| Đồng ý xử lý dữ liệu | Checkbox | * | Phải chọn (BR-006) | Nhập | "Cần đồng ý xử lý dữ liệu cá nhân" |

## SCR-02 — Đăng ký / sửa lô (bản đồ)

| Mục | Nội dung |
|---|---|
| Mục đích | Ghi hình học lô đúng chuẩn Điều 2(28) và giấy tờ đất |
| Người dùng | Đại lý; Tuân thủ (sửa) |
| Thao tác | Lấy vị trí GPS (US-002) · Vẽ/đi quanh ranh (US-003) · Chụp giấy tờ (US-005) · Lưu → Chờ chấm |
| Hành vi | Diện tích khai báo > 4 ha thì nút "Lấy điểm" bị khóa, bắt buộc đa giác (BR-002). Diện tích tính tự động hiển thị cạnh diện tích khai báo; lệch > 20% thì cảnh báo vàng (BR-004). Chồng lấn > 10% thì tô đỏ lô trùng (BR-005). Offline: nhãn "Chưa đồng bộ" (FR-006). |

| Trường | Kiểu | Bắt buộc | Validate | Nguồn | Thông báo lỗi |
|---|---|:-:|---|---|---|
| Nông hộ | Chọn | * | Thuộc đại lý | SCR-01 | — |
| Diện tích khai báo (ha) | Số 2 lẻ | * | > 0; > 50 cảnh báo | Nhập | "Diện tích phải lớn hơn 0" |
| Hình học | Point/Polygon | * | BR-001, BR-002, BR-003 | GPS/bản đồ | "Lô trên 4 ha cần đa giác ranh giới" · "Đa giác tự cắt" |
| Độ chính xác GPS (m) | Số | * (khi lấy GPS) | Tự ghi từ thiết bị | Thiết bị | — |
| Năm trồng | Số | | 1970–năm hiện tại | Nhập | "Năm trồng không hợp lệ" |
| Loại giấy tờ | Chọn | | GCN QSDĐ / Xác nhận UBND xã / Không có | Nhập | — |
| Số giấy tờ | Text | Khi có giấy tờ | Không rỗng | Nhập | "Nhập số giấy tờ" |
| Diện tích trên giấy (ha) | Số | Khi có GCN | > 0 | Nhập | — |
| Ảnh giấy tờ | Ảnh | | ≤ 5 MB | Camera | "Ảnh quá lớn" |
| Lý do lệch diện tích | Chọn | Khi lệch > 20% | Danh mục lý do | Nhập | "Chọn lý do lệch diện tích" |

## SCR-03 — Kết quả chấm & hàng đợi Vùng xám

| Mục | Nội dung |
|---|---|
| Mục đích | Xem lý do kết quả chấm; xử lý Vùng xám; xem pháp lý |
| Người dùng | Tuân thủ (quyết định); Đại lý (nhiệm vụ khảo sát); Quản lý (xem) |
| Thao tác | Mở chi tiết lô (US-009) · Lọc hàng đợi theo hạn (US-010) · Giao khảo sát (US-012) · Ghi bằng chứng + quyết định (US-011) |
| Bố cục | Trái: hàng đợi Vùng xám (mã lô, quy tắc R2/R3/R5, ngày còn lại; > 14 ngày tô đỏ). Phải: bản đồ lô + lớp rừng 2020 + lớp mất cây che phủ + vùng đệm; thẻ kết quả gồm quy tắc, % giao rừng, khoảng cách, phiên bản dữ liệu. |

| Trường (form quyết định) | Kiểu | Bắt buộc | Validate | Thông báo lỗi |
|---|---|:-:|---|---|
| Phương pháp | Chọn | * | Ảnh lịch sử / Thực địa | — |
| Bằng chứng | Tệp/ảnh | * | ≥ 1 (BR-016); ảnh thực địa cách lô ≤ 100 m | "Cần ít nhất một bằng chứng" |
| Ngày của bằng chứng | Ngày | * | Với R4: ≤ 31/12/2020 mới chứng minh được canh tác trước mốc | "Bằng chứng sau mốc 31/12/2020 không đủ chứng minh" |
| Quyết định | Chọn | * | Đạt / Loại | — |
| Lý do | Text 500 | * | Không rỗng | "Nhập lý do" |

## SCR-04 — Thu mua (giao dịch & phiếu nhập)

| Mục | Nội dung |
|---|---|
| Mục đích | Ghi giao dịch gắn lô; lập phiếu nhập kho DN |
| Người dùng | Đại lý (giao dịch); Thu mua (phiếu nhập); Tuân thủ (xác nhận vượt sản lượng) |
| Thao tác | Ghi giao dịch (US-016) · Xác nhận vượt sản lượng (US-017) · Lập phiếu nhập (US-018) |
| Hành vi | Chọn lô Vùng xám/Loại/pháp lý chưa Đủ thì dòng "EU" bị khóa (BR-030). Thanh tiến độ "đã bán / sản lượng tối đa" của lô (BR-031). |

| Trường | Kiểu | Bắt buộc | Validate | Thông báo lỗi |
|---|---|:-:|---|---|
| Nông hộ | Chọn | * | Thuộc đại lý | — |
| Lô | Chọn | * | Thuộc nông hộ | — |
| Ngày | Ngày | * | ≤ hôm nay; trong niên vụ | "Ngày ngoài niên vụ" |
| Khối lượng (kg) | Số | * | 1–50.000 | "Khối lượng không hợp lệ" |
| Dòng | Chọn | * | EU / Khác; EU chỉ khi lô Đạt + Đủ | "Lô chưa đủ điều kiện dòng EU" |

## SCR-05 — Lô hàng & gói dữ liệu DDS

| Mục | Nội dung |
|---|---|
| Mục đích | Lập lô hàng EU, sinh gói DDS, theo dõi số tham chiếu, tra hồ sơ 5 năm |
| Người dùng | Thu mua (lô hàng); Tuân thủ (gói DDS); Quản lý (duyệt, xem) |
| Thao tác | Tạo lô hàng · Phân bổ phiếu nhập EU (US-019) · Lập gói (US-022/023) · Xuất GeoJSON/CSV/PDF (US-024) · Nhập số tham chiếu / từ chối (US-025/026) · Tra hồ sơ (US-027) |
| Bố cục | Đầu trang: thẻ "Tấn đủ điều kiện EU khả dụng" (US-020). Danh sách lô hàng theo trạng thái. Chi tiết: phân bổ · danh sách lô · bản đồ lô · kiểm tra trước khi lập gói (tích xanh/đỏ từng điều kiện) · lịch sử trạng thái. |

| Trường | Kiểu | Bắt buộc | Validate | Thông báo lỗi |
|---|---|:-:|---|---|
| Số hợp đồng | Text | * | Duy nhất | "Số hợp đồng đã tồn tại" |
| Nhà nhập khẩu | Text | * | — | — |
| Mã HS | Text | * | Mặc định 0901 | — |
| Ngày tàu đến dự kiến | Ngày | * | > hôm nay | — |
| Khối lượng phân bổ (kg) | Số | * | ≤ khối lượng còn lại của phiếu (BR-032) | "Vượt khối lượng còn lại" |
| Số tham chiếu DDS | Text | Khi được chấp nhận | Không rỗng | — |
| Lý do từ chối | Text | Khi bị từ chối | Không rỗng | — |

## SCR-06 — Dashboard

Thẻ KPI: % lô có tọa độ hợp lệ · Vùng xám tồn (quá hạn) · tấn đủ điều kiện EU · lô hàng chờ số tham chiếu. Bản đồ rủi ro theo huyện (S9). Biểu đồ: kết quả chấm theo huyện; xu hướng mất cây che phủ. Bản công khai của phần rủi ro huyện: [docs/index.html](../../docs/index.html).

## SCR-07 — Quản trị

Ba thẻ: **Người dùng** (US-030; tài khoản, vai trò, đại lý gắn) · **Tham số** (US-031; ngày áp dụng 30/12/2026, vùng đệm 50 m, ngưỡng giao 10%, dung sai diện tích 20%, năng suất tối đa 3,5 t/ha, cảnh báo số tham chiếu 5 ngày, SLA Vùng xám 14 ngày, phiên bản bản đồ) · **Nhật ký audit** (US-029; lọc theo người, đối tượng, ngày). Thẻ **Đại lý** (US-021): tên*, địa chỉ*, email*, mã số thuế, trạng thái.
