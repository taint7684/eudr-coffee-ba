# Decision log

Mỗi quyết định gồm: mã · bối cảnh · phương án đã xét · lựa chọn · lý do · ngày.

---

## DEC-01 — Đi tiếp đề tài sau kiểm tra khả thi (T0.5)

- **Ngày:** 2026-10-20
- **Bối cảnh:** T0.4 kiểm tra 3 điểm có thể làm hỏng đề tài.

| Điểm | Kết quả | Kết luận | Nguồn |
|---|---|---|---|
| 1. Mốc EUDR | Regulation (EU) 2025/2650 dời ngày áp dụng sang **30/12/2026**. DN siêu nhỏ/nhỏ thành lập trước 31/12/2024 áp dụng từ **30/06/2027** (Điều 38(2)–(3) mới). Rà soát đơn giản hóa (COM(2026) 191, 04/5/2026) không đề xuất sửa luật thêm [Unverified: mới đọc tóm tắt]. Việt Nam được xếp **rủi ro thấp** (Implementing Regulation 2025/1093). | **Đạt** — EUDR còn hiệu lực, có mốc cụ thể. Nhưng phải đổi cách đóng khung (DEC-03, DEC-04). | SRC-003, SRC-004, SRC-005 |
| 2. Diện tích cà phê theo huyện | Không tìm thấy niên giám Đắk Lắk bản điện tử công khai. Có số rời cho Cư M'gar (37.600–38.906 ha), Krông Búk (20.415 ha) [Unverified]. Cấp huyện kết thúc hoạt động từ 01/7/2025; Đắk Lắk hợp nhất với Phú Yên. | **Đạt có điều kiện** — phân tích theo 15 huyện cũ (DEC-05). Cập nhật: đã có niên giám 2024 (DEC-08). | SRC-017, SRC-018, SRC-019, SRC-021, SRC-022 |
| 3. Mất rừng theo huyện | Workbook thống kê quốc gia của GFW có số mất cây che phủ 2001–2025 cho **15 huyện cũ của Đắk Lắk**, kèm nguyên nhân (Sims 2025). Data API cần API key miễn phí. | **Đạt** — đã trích được (03-data/processed/). | SRC-008 |

- **Phương án đã xét:** (a) đi tiếp đúng kế hoạch; (b) phân tích ô lưới 5×5 km; (c) chuyển sang GEE ngay; (d) đổi khung "yêu cầu thị trường".
- **Lựa chọn:** (a) đi tiếp, kèm ba điều chỉnh DEC-03, DEC-04, DEC-05. GEE dùng cho T8.1 (so nguồn), không cần cho T5.1.
- **Lý do:** cả 3 điểm có dữ liệu; điểm 2 chỉ thiếu số diện tích cà phê, không chặn T5.1/T6.1.

## DEC-02 — Khách hàng giả định (T1.3)

- **Ngày:** 2026-10-20
- **Lựa chọn:** "Công ty XK Cà phê Giả định" (tên làm việc: **DakCoffee Export**) — DN xuất khẩu cà phê nhân Robusta cỡ vừa, trụ sở Buôn Ma Thuột, thu mua qua mạng lưới đại lý tại Đắk Lắk (ranh giới cũ).

| Thuộc tính | Giá trị likely (min–max) | Mã |
|---|---|---|
| Sản lượng thu mua/năm | 30.000 t (15.000–50.000) | ASM-01 |
| Tỷ trọng bán sang EU-27 | 45% (30–60%) | ASM-02 |
| Năng suất bình quân | 2,6 t/ha (2,3–3,0) | ASM-03 |
| Diện tích bình quân/nông hộ | 1,0 ha (0,5–2,0) | ASM-04 |
| ⇒ Diện tích cung ứng | ≈ 11.500 ha | suy ra từ ASM-01/03 |
| ⇒ Số nông hộ/lô cung ứng | ≈ 11.500 lô (5.000–33.000) | suy ra từ ASM-01/03/04 |
| Số đại lý | 60 (30–120) | ASM-05 |
| Hiện trạng công nghệ | ERP kế toán; không có dữ liệu lô đất; đại lý ghi sổ/Excel | ASM-06 |

- **Phương án đã xét:** DN lớn (FDI, đã có hệ thống truy xuất) · DN vừa nội địa · HTX.
- **Lý do:** DN vừa nội địa là nhóm chịu áp lực lớn nhất (không có sẵn hệ thống như FDI, không đủ nhỏ để hưởng chế độ đơn giản hóa). [Inference] — cần đối chiếu báo cáo IDH/RA ở T1.1.

## DEC-03 — DN xuất khẩu VN không phải "operator" theo EUDR; ECTS sinh **gói dữ liệu DDS** chứ không tự nộp DDS

- **Ngày:** 2026-10-20
- **Bối cảnh:** ROADMAP mục 1.7 ghi nhóm chức năng 4 là "Lập & nộp DDS lên hệ thống EU". Đọc luật gốc:
  - Điều 2(15) (sửa bởi 2025/2650): *operator* là người đưa sản phẩm **vào thị trường EU** hoặc xuất khẩu **từ EU**.
  - Điều 7: khi người ngoài EU đưa hàng vào thị trường, **người đầu tiên thành lập tại EU** làm cho hàng có mặt trên thị trường được coi là operator.
  - Điều 4(2): operator nộp DDS qua hệ thống thông tin Điều 33.
  - Điều 6(1)–(2), Điều 2(22): đại diện được ủy quyền phải **thành lập tại EU**.
- **Phương án đã xét:** (a) giữ "nộp DDS" như ROADMAP; (b) ECTS sinh gói dữ liệu đủ trường Phụ lục II cho nhà nhập khẩu EU nộp, rồi nhận lại số tham chiếu DDS; (c) bỏ hẳn phần DDS.
- **Lựa chọn:** (b). Nhóm chức năng 4 đổi tên thành **"Lập gói dữ liệu DDS & theo dõi số tham chiếu"**. Tích hợp trực tiếp với hệ thống thông tin EU chuyển sang "Hướng mở rộng" (chỉ khả thi nếu DN có pháp nhân/đại diện tại EU).
- **Lý do:** DN VN không có tư cách pháp lý để nộp DDS. Giá trị DN cung cấp là dữ liệu Điều 9(1)(c)(d)(g)(h) cho operator EU. Bản đề xuất ban đầu đã hiểu sai điểm này (ghi ở ai-log).

## DEC-04 — Việt Nam rủi ro thấp: giữ module chấm rủi ro lô, đổi mục đích

- **Ngày:** 2026-10-20
- **Bối cảnh:** Implementing Regulation 2025/1093 xếp Việt Nam rủi ro thấp. Theo Điều 13(1), operator **không phải** đánh giá và giảm thiểu rủi ro (Điều 10, 11) nếu đã xác định toàn bộ hàng đến từ nước rủi ro thấp sau khi đánh giá độ phức tạp chuỗi cung ứng và rủi ro trộn lẫn. Tỷ lệ kiểm tra tối thiểu với hàng từ nước rủi ro thấp: 1% operator (Điều 16(10) mới).
- **Điều vẫn bắt buộc:** Điều 3 (không phá rừng sau 31/12/2020, hợp pháp); Điều 9(1)(d) tọa độ mọi lô; Điều 9(1)(g) "thông tin đủ kết luận và kiểm chứng được" rằng sản phẩm không phá rừng; Điều 13(2): có thông tin chỉ ra rủi ro (kể cả substantiated concern theo Điều 31) thì phải làm đủ Điều 10–11.
- **Phương án đã xét:** (a) bỏ chấm rủi ro vì VN rủi ro thấp; (b) giữ nguyên như rủi ro chuẩn; (c) giữ chấm rủi ro lô như **bằng chứng Điều 9(1)(g)** + chốt chặn trộn lẫn + phương án dự phòng khi xếp hạng đổi.
- **Lựa chọn:** (c).
- **Lý do:** Điều 9(1)(g) vẫn đòi bằng chứng kiểm chứng được cho từng lô; nhà nhập khẩu EU sẽ yêu cầu nhà cung cấp chứng minh. Điều 16(3) mới yêu cầu cơ quan có thẩm quyền ưu tiên kiểm tra lô **liền kề rừng**. Xếp hạng quốc gia được rà soát định kỳ (Điều 29) nên có thể đổi. Thêm kịch bản "VN bị xếp lại rủi ro chuẩn" vào business case (RSK-02).

## DEC-05 — Đơn vị phân tích: 15 huyện cũ của tỉnh Đắk Lắk (trước 01/7/2025)

- **Ngày:** 2026-10-20
- **Bối cảnh:** Từ 01/7/2025, cấp huyện kết thúc hoạt động và Đắk Lắk hợp nhất với Phú Yên (SRC-021, SRC-022). GFW dùng ranh giới GADM 4.1 (63 tỉnh, huyện cũ). Niên giám thống kê đến năm 2024 theo huyện cũ.
- **Lựa chọn:** phân tích theo 15 huyện/thị xã/thành phố cũ của Đắk Lắk. Phú Yên cũ nằm ngoài phạm vi (vùng cà phê không đáng kể — [Inference], cần xác minh).
- **Lý do:** mọi bộ dữ liệu cùng ranh giới; ghép xã mới là "Hướng mở rộng". Trong hệ thống ECTS, địa chỉ lô đất dùng **xã mới** (vì là dữ liệu vận hành từ 2026), ánh xạ ngược huyện cũ để báo cáo.

## DEC-06 — Chỉ số rủi ro huyện là chỉ số **sàng lọc**, không kết luận phá rừng

- **Ngày:** 2026-10-20
- **Bối cảnh:** GFW đo "tree cover loss" (mọi cây cao > 5 m, kể cả cây trồng), khác định nghĩa "deforestation" của EUDR (Điều 2(3)–(4): chuyển **rừng** sang nông nghiệp; loại trừ đồn điền nông nghiệp).
- **Lựa chọn:** mọi nơi dùng số GFW ghi "mất cây che phủ"; chỉ số huyện dùng để ưu tiên thu tọa độ/xác minh, không dùng để loại lô. Quyết định Đạt/Loại ở mức lô dựa trên chồng lớp với bản đồ rừng 2020 (JRC GFC2020) + mất cây che phủ sau 2020 (BR ở SRS).

## DEC-07 — Mô hình chuỗi cung ứng cho dòng EU: tách dòng (segregation), không cân bằng khối lượng

- **Ngày:** 2026-10-20
- **Bối cảnh:** Điều 9(1)(d) yêu cầu tọa độ của **mọi** lô mà sản phẩm chứa; Điều 10(2)(j) coi trộn với hàng không rõ nguồn là tiêu chí rủi ro; Điều 13(1) chỉ cho thẩm định đơn giản hóa khi đã loại trừ rủi ro trộn.
- **Phương án đã xét:** (a) bảo toàn nguồn gốc từng hộ (identity preserved); (b) tách dòng: hàng EU từ nhiều lô Đạt được trộn với nhau nhưng không trộn với hàng khác; (c) cân bằng khối lượng.
- **Lựa chọn:** (b). Gói DDS liệt kê mọi lô đã đóng góp vào phiếu nhập dòng EU của lô hàng.
- **Lý do:** (a) quá tốn kho với nông hộ 1 ha; (c) không bảo đảm sản phẩm thực tế chỉ chứa hàng từ lô đã khai [Unverified: cần đối chiếu FAQ/Guidance của EC về mass balance]. Câu hỏi đưa vào S20.

## DEC-08 — Diện tích cà phê theo niên giám; so Hansen × JRC chuyển sang Hướng mở rộng

- **Ngày:** 2026-10-20
- **Bối cảnh:** Tìm được Niên giám thống kê Đắk Lắk 2024 bản PDF chính thức (SRC-033), biểu 170–172 có diện tích trồng, thu hoạch, sản lượng cà phê của 15 huyện, 2020–2024. Việc so Hansen với JRC (T8.1b) cần tài khoản Google Earth Engine.
- **Lựa chọn:** (1) Dùng biểu 170 năm 2024 làm `coffee_ha`; chỉ số rủi ro chuyển sang v1. Giữ niên giám 2024 (ranh giới cũ), không dùng niên giám 2025 (tỉnh mới sau hợp nhất) để không trộn hai hệ địa giới. (2) T8.1b chuyển sang Hướng mở rộng; script GEE giữ trong repo.
- **Lý do:** (1) Số chính thức thay giả định ASM-22. (2) So sánh hai bộ dữ liệu là phân tích độ nhạy bổ sung, không phải điều kiện của luồng chính; độ nhạy theo ngưỡng tán đã định lượng ở S10 §1a.
- **Giới hạn:** số cấp huyện không thay dữ liệu ranh giới từng lô; không dùng để kết luận tỷ lệ lô cà phê bị ảnh hưởng bởi phá rừng.

## DEC-09 — Phạm vi đóng gói

- **Ngày:** 2026-10-20
- **Lựa chọn:** Bỏ khỏi phạm vi dự án các hoạt động truyền thông và phát hành (review bên ngoài, bài đăng, video demo, release theo mốc). T18.5 gộp vào `ai-log.md`, không tạo file tổng kết riêng.
