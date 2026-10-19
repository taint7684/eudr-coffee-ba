# Definition of Ready / Definition of Done

## Definition of Ready (story được đưa vào phát triển khi)

1. Viết theo mẫu "Là {persona}, tôi muốn {việc}, để {giá trị}"; persona có trong S4.
2. Trỏ tới ít nhất 1 FR; FR trỏ tới REQ-EU hoặc RC.
3. Có 2–4 AC dạng Given/When/Then, kiểm thử được.
4. BR liên quan đã viết theo EARS và có tham số rõ.
5. Màn hình liên quan có trong screen-spec (SCR-xx).
6. Phụ thuộc dữ liệu/ngoài hệ thống đã được nêu (bản đồ, nhà nhập khẩu).
7. Đã ước lượng độ phức tạp tương đối (S/M/L).
8. Product Owner đã xác nhận mức MoSCoW và đợt phát hành.

## Definition of Done (story hoàn thành khi)

1. Mọi AC đạt trên môi trường kiểm thử.
2. Mọi TC liên kết trong RTM đã chạy và đạt.
3. Không còn lỗi mức Nghiêm trọng/Cao.
4. Audit log ghi đúng thao tác của story (BR-051).
5. Phân quyền đúng ma trận (permissions.md).
6. RTM cập nhật: chạy `build_rtm.py` không lỗi.
7. Nhãn giao diện tiếng Việt; dữ liệu xuất cho nhà nhập khẩu bằng tiếng Anh (NFR-005).
8. Tài liệu người dùng cho chức năng được cập nhật.
