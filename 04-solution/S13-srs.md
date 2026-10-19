# S13 — Software Requirements Specification: ECTS

**EUDR Coffee Traceability System** · Cấu trúc theo ISO/IEC/IEEE 29148:2018 · Phiên bản 1.0 · Ngày 2026-10-20
Khách hàng giả định: DakCoffee Export (DEC-02). Tài liệu nghiên cứu độc lập, không phải tư vấn pháp lý.

> Các bảng có mốc `GEN` được sinh từ [trace/](trace/) bằng `py 04-solution/trace/build_docs.py`. Muốn sửa yêu cầu thì sửa CSV, không sửa bảng trong file này.

## 1. Giới thiệu

### 1.1 Mục đích
Đặc tả yêu cầu cho ECTS. Mục tiêu của hệ thống: DN xuất khẩu cà phê cung cấp cho nhà nhập khẩu EU tọa độ và bằng chứng "không phá rừng", "hợp pháp" của mọi lô đất trong một lô hàng, đáp ứng EUDR (Regulation (EU) 2023/1115, sửa bởi 2025/2650).

### 1.2 Phạm vi
- **Trong phạm vi:** đăng ký nông hộ và lô · chấm rủi ro lô · ghi nhận thu mua và lô hàng · gói dữ liệu DDS · dashboard, audit, quản trị. Robusta, Đắk Lắk (ranh giới cũ, DEC-05).
- **Ngoài phạm vi:** nộp DDS trực tiếp lên hệ thống thông tin EU (DEC-03) · logistics · thanh toán · chứng nhận 4C/RA · mặt hàng khác.

### 1.3 Thuật ngữ
Xem [glossary](../01-discovery/glossary.md).

### 1.4 Tài liệu tham chiếu
SRC-001 (EUDR), SRC-003 (2025/2650), SRC-004 (IR 2025/1093), SRC-008/009/011 (dữ liệu vệ tinh). Danh mục đầy đủ: [source-log](../00-management/source-log.csv).

## 2. Mô tả tổng quan

### 2.1 Bối cảnh sản phẩm
ECTS là hệ thống độc lập (web cho văn phòng DN, ứng dụng di động offline cho đại lý). Sơ đồ ngữ cảnh: [context-dfd](S12-scope/context-dfd.md).

### 2.2 Người dùng

| Vai trò | Persona | Việc chính |
|---|---|---|
| Đại lý | P3 | Đăng ký nông hộ, lô; ghi giao dịch; khảo sát Vùng xám |
| Cán bộ thu mua | P1 | Nhập kho, lập lô hàng |
| Nhân viên tuân thủ | P2 | Xử lý Vùng xám, pháp lý, gói DDS |
| Quản lý DN | — | Dashboard, tham số, phê duyệt |
| Quản trị hệ thống | — | Người dùng, phân quyền |
| Nông hộ | P4 | Không đăng nhập; cung cấp thông tin qua đại lý |

### 2.3 Ràng buộc
- Tọa độ WGS84 ≥ 6 chữ số thập phân; lô > 4 ha bắt buộc đa giác (Điều 2(28)).
- Lưu hồ sơ ≥ 5 năm (Điều 9(1), 12(5)).
- Ngày áp dụng là tham số, mặc định 30/12/2026 (Điều 38(2)).
- Nguồn bản đồ: JRC GFC2020 (mốc rừng 2020), Hansen GFC (mất cây che phủ theo năm); lưu phiên bản dùng cho từng lần chấm.

### 2.4 Giả định và phụ thuộc
ASM-01…ASM-06 (quy mô DN), ASM-13 (vùng đệm 50 m), ASM-23 (dung sai diện tích 20%), ASM-24 (năng suất tối đa 3,5 t/ha). Phụ thuộc: nhà nhập khẩu chấp nhận định dạng gói GeoJSON/CSV; dữ liệu bản đồ tiếp tục được công bố miễn phí.

## 3. Yêu cầu chức năng

<!-- GEN:FR:START -->
| Mã | Nhóm | Chức năng | Mô tả | Actor | Nguồn REQ-EU | RC | MoSCoW | Đợt | Màn hình |
|---|---|---|---|---|---|---|---|---|---|
| FR-001 | EP-01 | Đăng ký nông hộ | Hệ thống cho phép Đại lý đăng ký nông hộ: họ tên, năm sinh, số định danh (tùy chọn), điện thoại, địa chỉ (xã mới), đại lý phụ trách, đồng ý xử lý dữ liệu cá nhân. | Đại lý | REQ-EU-021 | RC-02 | Must | MVP | SCR-01 |
| FR-002 | EP-01 | Đăng ký lô bằng điểm GPS | Hệ thống cho phép Đại lý đăng ký lô ≤ 4 ha bằng một điểm GPS lấy tại lô hoặc chọn trên bản đồ; lưu WGS84 ≥ 6 chữ số thập phân. | Đại lý | REQ-EU-007; REQ-EU-020; REQ-EU-038 | RC-02; RC-03 | Must | MVP | SCR-02 |
| FR-003 | EP-01 | Đăng ký lô bằng đa giác | Hệ thống cho phép Đại lý đăng ký ranh giới lô bằng đa giác (đi quanh ranh hoặc vẽ trên bản đồ); bắt buộc với lô > 4 ha. | Đại lý | REQ-EU-007; REQ-EU-020; REQ-EU-038 | RC-02; RC-03 | Must | MVP | SCR-02 |
| FR-004 | EP-01 | Kiểm tra hình học lô | Hệ thống kiểm tra tọa độ hợp lệ, đa giác khép kín/không tự cắt, chồng lấn lô khác, lệch diện tích khai báo. | Hệ thống | REQ-EU-007; REQ-EU-008 | RC-02 | Must | MVP | SCR-02 |
| FR-005 | EP-01 | Đính kèm giấy tờ đất | Hệ thống cho phép Đại lý nhập số GCN QSDĐ, diện tích trên giấy, ảnh giấy tờ hoặc xác nhận UBND xã. | Đại lý | REQ-EU-002; REQ-EU-024; REQ-EU-025 | RC-05 | Must | MVP | SCR-02 |
| FR-006 | EP-01 | Offline và đồng bộ | Hệ thống cho phép Đại lý đăng ký nông hộ/lô và ghi giao dịch khi mất mạng; tự đồng bộ khi có mạng; báo xung đột. | Đại lý | REQ-EU-007 | RC-03 | Should | R2 | SCR-01; SCR-02; SCR-04 |
| FR-007 | EP-01 | Nhập lô hàng loạt | Hệ thống cho phép Tuân thủ nhập nông hộ/lô từ tệp GeoJSON hoặc CSV (vd dữ liệu chứng nhận 4C/RA) và báo lỗi từng dòng. | Tuân thủ | REQ-EU-020 | RC-02; RC-03 | Could | R3 | SCR-01 |
| FR-008 | EP-02 | Chấm rủi ro lô tự động | Hệ thống chồng lô với rừng 2020 (JRC GFC2020) và mất cây che phủ sau 31/12/2020 (Hansen), áp vùng đệm, trả kết quả Đạt / Vùng xám / Loại / Chưa chấm theo bảng quyết định. | Hệ thống | REQ-EU-001; REQ-EU-004; REQ-EU-005; REQ-EU-006; REQ-EU-023; REQ-EU-035 | RC-06 | Must | MVP | SCR-03 |
| FR-009 | EP-02 | Chấm lại theo phiên bản bản đồ | Hệ thống chấm lại toàn bộ lô khi nguồn bản đồ có phiên bản mới; lưu lịch sử kết quả theo phiên bản. | Hệ thống | REQ-EU-029; REQ-EU-034 | RC-06 | Should | R3 | SCR-03 |
| FR-010 | EP-02 | Xác minh Vùng xám | Hệ thống cho phép Tuân thủ giao xác minh, ghi bằng chứng (ảnh lịch sử, ảnh thực địa gắn tọa độ) và quyết định Đạt/Loại kèm lý do. | Tuân thủ; Đại lý | REQ-EU-030; REQ-EU-012 | RC-06 | Must | MVP | SCR-03 |
| FR-011 | EP-02 | Đánh giá pháp lý lô | Hệ thống xác định trạng thái pháp lý lô (Đủ / Thiếu / Mâu thuẫn) từ giấy tờ đất và đối chiếu diện tích. | Tuân thủ | REQ-EU-002; REQ-EU-008; REQ-EU-024; REQ-EU-025 | RC-05 | Must | MVP | SCR-03 |
| FR-012 | EP-02 | Cảnh báo mất cây che phủ mới | Hệ thống phát hiện mất cây che phủ mới trên lô đã Đạt khi có dữ liệu năm mới; chuyển lô sang Vùng xám và khóa lô hàng chưa xuất liên quan. | Hệ thống | REQ-EU-034 | RC-06 | Should | R3 | SCR-03; SCR-05 |
| FR-013 | EP-03 | Ghi nhận giao dịch thu mua | Hệ thống cho phép Đại lý ghi giao dịch: nông hộ, lô, ngày, khối lượng, dòng EU/khác; chặn lô không đủ điều kiện cho dòng EU; cảnh báo vượt sản lượng tối đa của lô. | Đại lý | REQ-EU-012; REQ-EU-020; REQ-EU-027 | RC-01; RC-04 | Must | R2 | SCR-04 |
| FR-014 | EP-03 | Nhập kho DN từ đại lý | Hệ thống cho phép Thu mua lập phiếu nhập kho từ các giao dịch của đại lý; phiếu kế thừa danh sách lô và khối lượng. | Thu mua | REQ-EU-018; REQ-EU-027 | RC-04 | Must | R2 | SCR-04 |
| FR-015 | EP-03 | Lập lô hàng xuất | Hệ thống cho phép Thu mua lập lô hàng xuất (hợp đồng, nhà nhập khẩu, mã HS, ngày tàu), phân bổ khối lượng từ phiếu nhập dòng EU, kiểm tra cân đối khối lượng. | Thu mua | REQ-EU-018; REQ-EU-028; REQ-EU-033 | RC-04 | Must | R2 | SCR-05 |
| FR-016 | EP-03 | Quản lý đại lý & nhà cung cấp | Hệ thống cho phép Thu mua quản lý đại lý/điểm thu mua: tên, địa chỉ, email, mã số thuế, trạng thái. | Thu mua | REQ-EU-021 | RC-01 | Must | R2 | SCR-07 |
| FR-017 | EP-04 | Lập gói dữ liệu DDS | Hệ thống cho phép Tuân thủ lập gói dữ liệu DDS cho lô hàng: mã HS, mô tả, khối lượng kg tịnh, nước sản xuất, GeoJSON mọi lô, thời gian sản xuất, nhà cung cấp, kết luận chấm, giấy tờ pháp lý. | Tuân thủ | REQ-EU-003; REQ-EU-009; REQ-EU-010; REQ-EU-017; REQ-EU-019; REQ-EU-020; REQ-EU-023; REQ-EU-024; REQ-EU-037; REQ-EU-038 | RC-02 | Must | R2 | SCR-05 |
| FR-018 | EP-04 | Xuất & gửi gói | Hệ thống xuất gói (GeoJSON, CSV, PDF tóm tắt) và ghi nhận ngày gửi, người nhận phía nhà nhập khẩu. | Tuân thủ | REQ-EU-015; REQ-EU-016; REQ-EU-022 | RC-02 | Must | R2 | SCR-05 |
| FR-019 | EP-04 | Số tham chiếu DDS & xử lý từ chối | Hệ thống cho phép Tuân thủ ghi số tham chiếu DDS hoặc kết quả từ chối do nhà nhập khẩu báo; lô hàng bị từ chối quay về Nháp. | Tuân thủ | REQ-EU-011; REQ-EU-013; REQ-EU-036 | RC-02 | Must | R2 | SCR-05 |
| FR-020 | EP-04 | Lưu & truy vấn hồ sơ 5 năm | Hệ thống lưu hồ sơ lô hàng, gói DDS, kết quả chấm ≥ 5 năm và cho phép tra cứu theo lô hàng hoặc lô đất. | Tuân thủ | REQ-EU-017; REQ-EU-031; REQ-EU-032 | RC-02 | Must | R2 | SCR-05 |
| FR-021 | EP-05 | Dashboard rủi ro & KPI | Hệ thống hiển thị rủi ro theo huyện/xã, tỷ lệ lô có tọa độ hợp lệ, Vùng xám tồn, sản lượng đủ điều kiện EU. | Quản lý | REQ-EU-035 | RC-06 | Should | R3 | SCR-06 |
| FR-022 | EP-05 | Nhật ký audit | Hệ thống ghi mọi thao tác thêm/sửa/xóa/quyết định: người, thời điểm, giá trị trước/sau. | Quản trị | REQ-EU-029; REQ-EU-032 | RC-02 | Must | MVP | SCR-07 |
| FR-023 | EP-05 | Người dùng & phân quyền | Hệ thống cho phép Quản trị quản lý tài khoản và gán vai trò; quyền theo ma trận phân quyền. | Quản trị |  |  | Must | MVP | SCR-07 |
| FR-024 | EP-05 | Tham số hệ thống | Hệ thống cho phép Quản lý cấu hình ngày áp dụng EUDR, vùng đệm, ngưỡng giao, năng suất tối đa, phiên bản bản đồ, mã HS. | Quản lý | REQ-EU-040; REQ-EU-026 |  | Should | MVP | SCR-07 |
<!-- GEN:FR:END -->

## 4. Quy tắc nghiệp vụ (EARS)

<!-- GEN:BR:START -->
| Mã | Quy tắc | Nguồn | FR | Tham số |
|---|---|---|---|---|
| BR-001 | KHI lưu tọa độ lô, HỆ THỐNG PHẢI lưu vĩ độ và kinh độ hệ WGS84 với ít nhất 6 chữ số thập phân. | REQ-EU-007 (Điều 2(28)) | FR-002; FR-003; FR-004 |  |
| BR-002 | KHI diện tích khai báo của lô lớn hơn 4 ha, HỆ THỐNG PHẢI yêu cầu đa giác ranh giới và từ chối lưu lô chỉ có một điểm. | REQ-EU-007 (Điều 2(28)) | FR-002; FR-003; FR-004 | polygon_threshold_ha=4 |
| BR-003 | KHI đa giác có ít hơn 3 đỉnh phân biệt, không khép kín hoặc tự cắt, HỆ THỐNG PHẢI từ chối lưu và chỉ ra lỗi. | REQ-EU-007 | FR-003; FR-004 |  |
| BR-004 | KHI diện tích khai báo lệch diện tích tính từ đa giác quá 20%, HỆ THỐNG PHẢI cảnh báo và yêu cầu người nhập xác nhận lý do. | REQ-EU-008; ASM-23 | FR-004 | area_tolerance=0.20 |
| BR-005 | KHI lô mới chồng lấn một lô đã đăng ký quá 10% diện tích lô mới, HỆ THỐNG PHẢI chặn lưu và hiển thị lô bị trùng. | REQ-EU-008 | FR-004 | overlap_max=0.10 |
| BR-006 | KHI đăng ký nông hộ, HỆ THỐNG PHẢI ghi nhận đồng ý xử lý dữ liệu cá nhân (người, thời điểm, phiên bản điều khoản) trước khi lưu. | NFR-007 | FR-001 |  |
| BR-010 | KHI lô không giao rừng 2020, không có mất cây che phủ sau 31/12/2020 trong lô và cách vùng mất/rìa rừng từ 50 m trở lên, HỆ THỐNG PHẢI gán kết quả Đạt. | REQ-EU-004; REQ-EU-023; S10 R1 | FR-008 | buffer_m=50 |
| BR-011 | KHI lô không giao rừng 2020 nhưng có mất cây che phủ sau 31/12/2020 trong lô, HỆ THỐNG PHẢI gán kết quả Vùng xám. | REQ-EU-006; S10 R2 | FR-008 |  |
| BR-012 | KHI lô giao rừng 2020 từ 10% diện tích trở lên và không có mất cây che phủ sau 31/12/2020, HỆ THỐNG PHẢI gán kết quả Vùng xám. | REQ-EU-005; REQ-EU-006; S10 R3 | FR-008 | forest_overlap_min=0.10 |
| BR-013 | KHI lô giao rừng 2020 từ 10% diện tích trở lên và có mất cây che phủ sau 31/12/2020 trong phần giao, HỆ THỐNG PHẢI gán kết quả Loại. | REQ-EU-004; REQ-EU-020; S10 R4 | FR-008 | forest_overlap_min=0.10 |
| BR-014 | KHI lô không thuộc BR-011 đến BR-013 nhưng cách vùng mất cây che phủ sau 2020 hoặc rìa rừng 2020 dưới 50 m, HỆ THỐNG PHẢI gán kết quả Vùng xám. | REQ-EU-035; S10 R5; ASM-13 | FR-008 | buffer_m=50 |
| BR-015 | KHI lô ở trạng thái Vùng xám quá 14 ngày, HỆ THỐNG PHẢI gửi cảnh báo cho Tuân thủ và Quản lý. | KPI S18 | FR-010 | grayzone_sla_days=14 |
| BR-016 | KHI Tuân thủ quyết định Đạt hoặc Loại cho lô Vùng xám, HỆ THỐNG PHẢI yêu cầu ít nhất một bằng chứng (ảnh lịch sử hoặc ảnh thực địa gắn tọa độ) và lý do. | REQ-EU-030 (Điều 11(1)) | FR-010 |  |
| BR-017 | KHI nguồn bản đồ có phiên bản mới, HỆ THỐNG PHẢI chấm lại mọi lô và lưu kết quả cũ kèm phiên bản. | REQ-EU-029 (Điều 10(4)) | FR-009 |  |
| BR-018 | KHI phát hiện mất cây che phủ mới trên lô đã Đạt, HỆ THỐNG PHẢI chuyển lô sang Vùng xám và khóa các lô hàng chưa xuất có chứa lô đó. | REQ-EU-034 (Điều 13(2)) | FR-012 |  |
| BR-020 | KHI lô không có số GCN QSDĐ và không có xác nhận UBND xã, HỆ THỐNG PHẢI gán trạng thái pháp lý Thiếu. | REQ-EU-024 (Điều 9(1)(h)) | FR-005; FR-011 |  |
| BR-021 | KHI diện tích đo từ đa giác/điểm lệch diện tích trên GCN QSDĐ quá 20%, HỆ THỐNG PHẢI gán trạng thái pháp lý Mâu thuẫn và đưa vào hàng đợi xác minh. | REQ-EU-008; SRS Rule conflicts | FR-011 | area_tolerance=0.20 |
| BR-030 | KHI ghi giao dịch dòng EU từ lô có kết quả khác Đạt hoặc pháp lý khác Đủ, HỆ THỐNG PHẢI từ chối giao dịch. | REQ-EU-012 (Điều 4(4)) | FR-013 |  |
| BR-031 | KHI tổng khối lượng thu mua từ một lô trong niên vụ vượt diện tích × năng suất tối đa (3,5 t/ha), HỆ THỐNG PHẢI cảnh báo và yêu cầu Tuân thủ xác nhận. | REQ-EU-028 (Điều 10(2)(j)); ASM-24 | FR-013 | max_yield_t_ha=3.5 |
| BR-032 | KHI phân bổ khối lượng từ phiếu nhập vào lô hàng xuất, HỆ THỐNG PHẢI không cho tổng phân bổ vượt khối lượng còn lại của phiếu. | REQ-EU-018; REQ-EU-028 | FR-014; FR-015 |  |
| BR-033 | KHI lập lô hàng dòng EU, HỆ THỐNG PHẢI chỉ chấp nhận phiếu nhập dòng EU (mô hình tách dòng, DEC-07). | REQ-EU-028; REQ-EU-033 | FR-015 |  |
| BR-040 | KHI lập gói dữ liệu DDS, HỆ THỐNG PHẢI kiểm tra mọi lô trong lô hàng có kết quả Đạt và pháp lý Đủ; có lô không đạt thì chặn và liệt kê lô đó. | REQ-EU-012; REQ-EU-023; REQ-EU-024 | FR-017 |  |
| BR-041 | KHI sinh gói dữ liệu DDS, HỆ THỐNG PHẢI xuất GeoJSON (điểm cho lô ≤ 4 ha, đa giác cho lô > 4 ha), mã HS, khối lượng kg tịnh, nước sản xuất VN và khoảng thời gian sản xuất. | REQ-EU-020; REQ-EU-037; REQ-EU-038 | FR-017; FR-018 |  |
| BR-042 | KHI nhà nhập khẩu báo DDS bị từ chối, HỆ THỐNG PHẢI chuyển lô hàng về trạng thái Nháp kèm lý do từ chối. | REQ-EU-013 | FR-019 |  |
| BR-043 | KHI còn dưới 5 ngày tới ngày tàu dự kiến đến mà lô hàng chưa có số tham chiếu DDS, HỆ THỐNG PHẢI cảnh báo Tuân thủ và Quản lý. | REQ-EU-036 (Điều 26(4)) | FR-019 | dds_ref_alert_days=5 |
| BR-050 | HỆ THỐNG PHẢI lưu hồ sơ lô hàng, gói DDS và kết quả chấm ít nhất 5 năm kể từ ngày gửi gói và không cho xóa cứng. | REQ-EU-017; REQ-EU-032 (Điều 9(1); 12(5)) | FR-020 | retention_years=5 |
| BR-051 | KHI người dùng thêm, sửa, xóa hoặc ra quyết định trên dữ liệu nghiệp vụ, HỆ THỐNG PHẢI ghi audit gồm người, thời điểm, giá trị trước và sau. | REQ-EU-029; REQ-EU-032 | FR-022 |  |
| BR-060 | KHI ngày hiện tại trước ngày áp dụng EUDR cấu hình, HỆ THỐNG PHẢI vẫn cho lập gói DDS và ghi chú "trước ngày áp dụng". | REQ-EU-040 (Điều 38) | FR-024 | eudr_apply_date=2026-12-30 |
<!-- GEN:BR:END -->

### 4.1 Bảng quyết định chấm rủi ro lô (policy rule table)

| Quy tắc | Giao rừng 2020 ≥ 10% | Mất cây che phủ sau 31/12/2020 | Vị trí mất | Cách vùng mất/rìa rừng | Kết quả | BR |
|---|:-:|:-:|---|:-:|---|---|
| R1 | Không | Không | — | ≥ 50 m | **Đạt** | BR-010 |
| R2 | Không | Có | Trong lô | — | **Vùng xám** | BR-011 |
| R3 | Có | Không, hoặc chỉ ngoài phần giao | — | — | **Vùng xám** | BR-012 |
| R4 | Có | Có | Trong phần giao | — | **Loại** | BR-013 |
| R5 | Không | Không | — | < 50 m | **Vùng xám** | BR-014 |
| R6 | Hình học không hợp lệ hoặc > 4 ha không có đa giác | | | | **Chưa chấm** | BR-002, BR-003 |

Thứ tự áp dụng: R6 → R4 → R3 → R2 → R5 → R1. Kết quả Vùng xám và Loại có thể đổi sau xác minh (BR-016). Mọi kết quả lưu phiên bản dữ liệu và tham số (NFR-011).

## 5. Yêu cầu phi chức năng

<!-- GEN:NFR:START -->
| Mã | Loại | Yêu cầu | Đo lường | Nguồn | MoSCoW |
|---|---|---|---|---|---|
| NFR-001 | Khả dụng | Ứng dụng di động của Đại lý hoạt động offline cho đăng ký nông hộ, lô và giao dịch; tự đồng bộ khi có mạng. | Lưu được ≥ 500 bản ghi offline; đồng bộ ≤ 2 phút/500 bản ghi khi có 3G | PESTLE (sóng yếu); S4 P3 | Must |
| NFR-002 | Hiệu năng | Thời gian chấm rủi ro một lô. | ≤ 10 giây/lô (p95); chấm lại 20.000 lô ≤ 4 giờ | S9; ASM-01 | Should |
| NFR-003 | Lưu trữ | Lưu hồ sơ thẩm định và gói DDS. | ≥ 5 năm; không xóa cứng; khôi phục được trong ≤ 1 ngày làm việc | Điều 9(1); 12(5) | Must |
| NFR-004 | Sao lưu | Sao lưu dữ liệu. | Hằng ngày; RPO ≤ 24 giờ; RTO ≤ 8 giờ | Thực hành chuẩn | Must |
| NFR-005 | Ngôn ngữ | Giao diện tiếng Việt; gói DDS và tài liệu xuất cho nhà nhập khẩu bằng tiếng Anh. | 100% nhãn có bản dịch | S3; Điều 6(2) | Must |
| NFR-006 | Bảo mật | Xác thực và phân quyền theo vai trò; mã hóa đường truyền. | TLS 1.2+; mật khẩu băm; khóa tài khoản sau 5 lần sai | ISO/IEC 27001 (tham chiếu) | Must |
| NFR-007 | Dữ liệu cá nhân | Thu thập tối thiểu, có đồng ý, giới hạn người xem dữ liệu nông hộ. | Ghi nhận đồng ý 100% nông hộ; chỉ vai trò được cấp mới xem số định danh | GDPR; Nghị định 13/2023/NĐ-CP [Unverified] | Must |
| NFR-008 | Tọa độ | Độ chính xác tọa độ lưu trữ. | WGS84; ≥ 6 chữ số thập phân; ghi độ chính xác GPS (m) của thiết bị | Điều 2(28) | Must |
| NFR-009 | Khả năng tương tác | Gói DDS theo định dạng máy đọc được. | GeoJSON RFC 7946 + CSV UTF-8 | Điều 4(2); Phụ lục II | Must |
| NFR-010 | Khả năng mở rộng | Quy mô dữ liệu. | ≥ 50.000 lô; ≥ 500.000 giao dịch/năm; ≥ 150 người dùng đồng thời | ASM-01; ASM-05 | Should |
| NFR-011 | Truy vết | Mọi kết quả chấm lưu phiên bản dữ liệu bản đồ và tham số đã dùng. | 100% kết quả có phiên bản | Điều 10(4) | Must |
| NFR-012 | Khả dụng hệ thống | Thời gian hoạt động. | ≥ 99% giờ làm việc mùa vụ (11–3) | Thực hành chuẩn | Should |
<!-- GEN:NFR:END -->

## 6. Giao diện ngoài

| Giao diện | Hướng | Nội dung | Định dạng |
|---|---|---|---|
| Nguồn bản đồ (JRC GFC2020, Hansen GFC) | Vào | Lớp rừng 2020, năm mất cây che phủ | Raster/tile; cập nhật hằng năm |
| Nhà nhập khẩu EU | Ra | Gói dữ liệu DDS | GeoJSON (RFC 7946) + CSV UTF-8 + PDF tóm tắt |
| Nhà nhập khẩu EU | Vào | Số tham chiếu DDS, kết quả từ chối | Nhập tay (MVP); API (R3) |
| ERP của DN | Hai chiều | Hợp đồng, đại lý, phiếu nhập | CSV (MVP); API (Hướng mở rộng) |

**Cấu trúc gói dữ liệu DDS** (ánh xạ Phụ lục II EUDR):

| Trường gói | Phụ lục II | Nguồn trong ECTS |
|---|---|---|
| `hs_code`, `description`, `net_mass_kg` | Mục 2 | Lô hàng (FR-015) |
| `country_of_production` = VN | Mục 3 | Cố định |
| `plots[]`: `plot_id`, `geometry` (Point/Polygon), `area_ha`, `production_period` | Mục 3; Điều 9(1)(d) | Lô đất + giao dịch (FR-002/003/013) |
| `suppliers[]` | Điều 9(1)(e) | Đại lý (FR-016) |
| `risk_evidence[]`: kết quả, quy tắc, phiên bản dữ liệu | Điều 9(1)(g) | Kết quả chấm (FR-008/010) |
| `legality_evidence[]`: số GCN QSDĐ / xác nhận xã | Điều 9(1)(h) | Giấy tờ đất (FR-005/011) |
| `exporter` | Điều 9(1)(e) đối với operator | Cố định |

## 7. Dữ liệu

Thực thể chính: Farmer · Plot · PlotDocument · PlotRiskAssessment · Verification · Agent · PurchaseTransaction · GoodsReceipt · Shipment · DDSPackage · MapVersion · Parameter · User · AuditLog. Chi tiết: [ERD](S15-design/erd.md). Vòng đời: [state](S15-design/state.md).

## Phụ lục A — Xử lý rule mâu thuẫn

| # | Mâu thuẫn | Cách xử lý | BR |
|---|---|---|---|
| C1 | Ranh giới GPS khác diện tích trên GCN QSDĐ | Lệch ≤ 20%: chấp nhận; > 20%: pháp lý = Mâu thuẫn → xác minh, ưu tiên số đo thực địa có chữ ký đại lý + nông hộ | BR-004, BR-021 |
| C2 | Nông hộ không có GCN QSDĐ | Chấp nhận xác nhận UBND xã về quyền canh tác; không có cả hai: pháp lý = Thiếu, không vào gói DDS | BR-020 |
| C3 | Bản đồ EU coi lô là rừng 2020, nhưng nông hộ canh tác từ trước | Vùng xám (R3); bằng chứng: ảnh lịch sử trước 31/12/2020 | BR-012, BR-016 |
| C4 | Hansen báo mất cây che phủ, nhưng thực tế là chặt cây che bóng/tái canh | Vùng xám (R2); Điều 2(6) loại đồn điền nông nghiệp khỏi định nghĩa rừng | BR-011, BR-016 |
| C5 | Một thửa trên GCN chứa nhiều vùng canh tác khác nhau | Lô ECTS = vùng canh tác liền khoảnh; nhiều lô có thể chung một GCN | BR-005 |
| C6 | Định nghĩa rừng VN khác EUDR | Hệ thống theo định nghĩa EU (Điều 2(4)) vì nhà nhập khẩu chịu luật EU | — |
| C7 | Địa chỉ theo xã mới, dữ liệu phân tích theo huyện cũ | Lưu xã mới; bảng ánh xạ xã mới → huyện cũ cho báo cáo | — |

## Phụ lục B — Kiểm tra độ phủ MoSCoW

Mọi REQ-EU bắt buộc (⛔) có ít nhất một FR mức **Must** và đi tới test case. Kết quả máy kiểm: [S17-coverage.md](../05-test/S17-coverage.md).
