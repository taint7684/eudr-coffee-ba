# S15 — Ma trận phân quyền, audit và dữ liệu cá nhân

## 1. Phân quyền

X = Xem · T = Thêm · S = Sửa · Ó = Xóa (xóa mềm) · D = Duyệt/Quyết định · — = không có quyền

| Chức năng | Đại lý | Thu mua | Tuân thủ | Quản lý | Quản trị |
|---|:-:|:-:|:-:|:-:|:-:|
| FR-001 Nông hộ | X T S (của mình) | X | X S | X | — |
| FR-002/003 Lô đất | X T S (của mình) | X | X S | X | — |
| FR-005 Giấy tờ đất | X T S (của mình) | — | X S | X | — |
| FR-007 Nhập lô hàng loạt | — | — | T | X | — |
| FR-008 Kết quả chấm | X (của mình) | X | X | X | — |
| FR-010 Xác minh Vùng xám | X T (nhiệm vụ được giao) | — | X T D | X | — |
| FR-011 Pháp lý | X | — | X D | X | — |
| FR-013 Giao dịch | X T S (của mình, chưa nhập kho) | X | X D (BR-031) | X | — |
| FR-014 Phiếu nhập | — | X T S | X | X | — |
| FR-015 Lô hàng | — | X T S Ó (Nháp) | X | X D | — |
| FR-016 Đại lý | — | X T S | X | X | — |
| FR-017–019 Gói DDS | — | X | X T S | X | — |
| FR-020 Hồ sơ 5 năm | — | X | X | X | — |
| FR-021 Dashboard | — | X | X | X | — |
| FR-022 Audit log | — | — | X | X | X |
| FR-023 Người dùng | — | — | — | X | X T S Ó |
| FR-024 Tham số | — | — | X | X S | X |

## 2. Sự kiện ghi audit (BR-051)

Mỗi bản ghi: người · thời điểm · đối tượng · hành động · giá trị trước · giá trị sau.

| Nhóm | Sự kiện |
|---|---|
| Lô đất | Tạo, sửa hình học, sửa diện tích, đổi giấy tờ, đổi trạng thái pháp lý |
| Chấm rủi ro | Mỗi lần chấm (kèm phiên bản bản đồ, tham số), quyết định xác minh |
| Thu mua | Tạo/sửa/hủy giao dịch, xác nhận vượt sản lượng, phiếu nhập, phân bổ |
| Gói DDS | Lập, xuất, gửi, nhập số tham chiếu, từ chối |
| Hệ thống | Đăng nhập thất bại, đổi vai trò, đổi tham số, cập nhật phiên bản bản đồ |

## 3. Dữ liệu cá nhân

[Unverified] Cần đối chiếu Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân (và các văn bản thay thế, nếu có) cùng GDPR. GDPR liên quan khi dữ liệu chuyển sang nhà nhập khẩu EU.

| Trường | Mục đích | Cơ sở | Thời hạn lưu | Ai được xem | Có trong gói DDS |
|---|---|---|---|---|---|
| Họ tên nông hộ | Định danh nhà cung cấp | Đồng ý (BR-006) | 5 năm sau lô hàng cuối | Đại lý phụ trách, Tuân thủ, Quản lý | Không (dùng mã lô) |
| Số định danh cá nhân | Đối chiếu giấy tờ đất | Đồng ý | Như trên | Tuân thủ | Không |
| Số điện thoại | Liên hệ xác minh | Đồng ý | Như trên | Đại lý phụ trách, Tuân thủ | Không |
| Tọa độ/đa giác lô | Điều 9(1)(d) EUDR | Nghĩa vụ hợp đồng với nhà nhập khẩu | 5 năm (Điều 9(1)) | Tất cả vai trò nghiệp vụ | **Có** |
| Số GCN QSDĐ | Điều 9(1)(h) | Đồng ý | 5 năm | Tuân thủ | Có (khi nhà nhập khẩu yêu cầu) |
| Ảnh xác minh | Bằng chứng Vùng xám | Lợi ích hợp pháp | 5 năm | Tuân thủ, Quản lý | Không (tóm tắt kết luận) |

Nguyên tắc: thu tối thiểu; gói DDS chỉ chứa mã lô và hình học, không chứa tên nông hộ.
