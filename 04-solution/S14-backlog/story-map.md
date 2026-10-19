# S14 — Epic & Story map

| Epic | Tên | FR |
|---|---|---|
| EP-01 | Đăng ký nông hộ & lô đất | FR-001…007 |
| EP-02 | Chấm rủi ro lô | FR-008…012 |
| EP-03 | Ghi nhận thu mua | FR-013…016 |
| EP-04 | Gói dữ liệu DDS | FR-017…020 |
| EP-05 | Dashboard, audit, quản trị | FR-021…024 |

## Story map

Trục ngang là hành trình người dùng, trục dọc là mức ưu tiên. Dòng **MVP** nằm trên đường cắt.

| | Đăng ký | Chấm | Thu mua | Lập gói DDS | Nộp & theo dõi | Giám sát |
|---|---|---|---|---|---|---|
| **MVP** | US-001 Đăng ký nông hộ<br>US-002 Lô bằng điểm<br>US-003 Lô bằng đa giác<br>US-004 Báo trùng/lệch<br>US-005 Giấy tờ đất | US-008 Chấm tự động<br>US-009 Lý do trên bản đồ<br>US-010 Hàng đợi Vùng xám<br>US-011 Quyết định có bằng chứng<br>US-012 Khảo sát thực địa<br>US-013 Trạng thái pháp lý | | | | US-029 Audit<br>US-030 Phân quyền<br>US-031 Tham số |
| *— đường cắt MVP —* | | | | | | |
| **R2** | US-006 Offline | | US-016 Giao dịch theo lô<br>US-017 Cảnh báo vượt sản lượng<br>US-018 Phiếu nhập<br>US-019 Lô hàng tách dòng<br>US-020 Tấn đủ điều kiện<br>US-021 Thông tin đại lý | US-022 Lập gói<br>US-023 Chặn lô chưa Đạt<br>US-024 Xuất GeoJSON/CSV | US-025 Số tham chiếu<br>US-026 Xử lý từ chối<br>US-027 Hồ sơ 5 năm | |
| **R3** | US-007 Nhập hàng loạt | US-014 Chấm lại theo phiên bản<br>US-015 Cảnh báo mất mới | | | | US-028 Dashboard |

**Lý do đặt đường cắt:** S9 §3 cho thấy rủi ro lớn nhất là thiếu tọa độ. MVP vì vậy tập trung thu tọa độ và chấm lô, để có dữ liệu sạch trước mùa vụ 2026/27. R2 nối dữ liệu lô vào luồng hàng và gói DDS.
