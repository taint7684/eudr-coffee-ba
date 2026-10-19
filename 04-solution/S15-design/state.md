# S15 — State machine

## Lô đất (kết quả chấm)

```mermaid
stateDiagram-v2
  [*] --> Nhap: Đại lý tạo lô
  Nhap --> ChoCham: Lưu hình học hợp lệ [BR-001…005]
  Nhap --> Nhap: Hình học lỗi [BR-003]
  ChoCham --> Dat: R1 [BR-010]
  ChoCham --> VungXam: R2 / R3 / R5 [BR-011, BR-012, BR-014]
  ChoCham --> Loai: R4 [BR-013]
  VungXam --> Dat: Xác minh có bằng chứng [BR-016]
  VungXam --> Loai: Xác minh có bằng chứng [BR-016]
  Loai --> Dat: Xác minh chứng minh canh tác trước 31/12/2020 [BR-016]
  Dat --> VungXam: Mất cây che phủ mới [BR-018]
  Dat --> ChoCham: Phiên bản bản đồ mới [BR-017]
  Nhap: Nháp
  ChoCham: Chờ chấm
  Dat: Đạt
  VungXam: Vùng xám
  Loai: Loại
```

Trạng thái pháp lý chạy song song: **Thiếu → Đủ** (bổ sung giấy tờ, BR-020) · **Đủ ↔ Mâu thuẫn** (lệch diện tích > 20%, BR-021). Lô chỉ vào dòng EU khi **Đạt + Đủ** (BR-030, BR-040).

## Lô hàng / gói DDS

```mermaid
stateDiagram-v2
  [*] --> Nhap: Thu mua tạo lô hàng
  Nhap --> SanSang: Phân bổ đủ khối lượng dòng EU [BR-032, BR-033] và mọi lô Đạt + Đủ [BR-040]
  SanSang --> Nhap: Lô bị chuyển Vùng xám [BR-018]
  SanSang --> DaGui: Lập và gửi gói DDS [BR-041]
  DaGui --> DuocChapNhan: Có số tham chiếu DDS
  DaGui --> BiTuChoi: Nhà nhập khẩu báo từ chối
  BiTuChoi --> Nhap: Tự động, kèm lý do [BR-042]
  DuocChapNhan --> [*]: Lưu hồ sơ ≥ 5 năm [BR-050]
  Nhap: Nháp
  SanSang: Sẵn sàng
  DaGui: Đã gửi
  DuocChapNhan: Được chấp nhận
  BiTuChoi: Bị từ chối
```

Cảnh báo theo thời gian: lô Vùng xám > 14 ngày (BR-015); lô hàng Đã gửi, còn < 5 ngày tới ngày tàu, chưa có số tham chiếu (BR-043).
