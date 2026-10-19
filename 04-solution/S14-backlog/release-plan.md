# Release plan

Không chia sprint, không gán story point: dự án không có đội phát triển, nên velocity giả định không có ý nghĩa.

| Đợt | Mục tiêu | Epic / Story | KPI kỳ vọng | Mốc đề xuất [Inference] |
|---|---|---|---|---|
| **MVP** — Dữ liệu lô sạch | Có tọa độ, giấy tờ và kết quả chấm cho lô của mạng lưới đại lý | EP-01 (US-001…005) · EP-02 (US-008…013) · EP-05 (US-029…031) | ≥ 90% lô có tọa độ hợp lệ sau 6 tháng; Vùng xám xử lý ≤ 14 ngày | Trước mùa thu hoạch chính (11/2026–01/2027) |
| **R2** — Từ lô tới lô hàng | Giao dịch gắn lô, tách dòng EU, gói DDS, số tham chiếu | US-006 · EP-03 (US-016…021) · EP-04 (US-022…027) | 100% lô hàng EU có gói DDS trước ngày tàu; % DDS bị từ chối ≤ 2% | Trước 30/12/2026 (ngày áp dụng EUDR) |
| **R3** — Giám sát & mở rộng | Chấm lại tự động, cảnh báo mất mới, dashboard, nhập dữ liệu chứng nhận; API với nhà nhập khẩu; mở cho liên minh ngành | US-007 · US-014 · US-015 · US-028 | Chấm lại 100% lô trong ≤ 30 ngày khi có dữ liệu năm mới | 2027 |

Phụ thuộc chính: định dạng gói DDS được nhà nhập khẩu chấp nhận (R2); quyền truy cập dữ liệu bản đồ cho chấm tự động (MVP).
