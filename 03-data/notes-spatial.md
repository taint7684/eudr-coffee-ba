# Ghi chú dữ liệu không gian (T4.1)

| # | Câu hỏi | Trả lời ngắn | Nguồn |
|---|---|---|---|
| 1 | Raster khác vector? | **Raster** là lưới ô vuông, mỗi ô một giá trị (mất/không mất cây che phủ). **Vector** là điểm, đường, đa giác có tọa độ (ranh giới huyện, ranh giới lô). Chấm rủi ro lô là phép chồng vector (lô) lên raster (bản đồ rừng). | — |
| 2 | 30 m nghĩa là gì với lô cà phê 1 ha? | 1 ô Hansen = 900 m², nên 1 ha ≈ 11 ô. Lô 0,5 ha chỉ có khoảng 5–6 ô, và sai số GPS điện thoại 5–15 m [Inference] đủ đẩy ranh giới lệch 1 ô. Kết luận: không chấm lô nhỏ chỉ bằng một nguồn 30 m; cần vùng đệm và quy tắc Vùng xám. | SRC-009 |
| 3 | "Tree cover loss" có phải "deforestation"? | **Không.** GFW: mất cây che phủ là việc cây > 5 m bị loại bỏ hoặc chết, kể cả khi thu hoạch cây trồng; *loss does not equate to deforestation*. EUDR: phá rừng = chuyển **rừng** sang mục đích nông nghiệp (Điều 2(3)); đồn điền nông nghiệp không phải rừng (Điều 2(6)). | SRC-008; SRC-001 |
| 4 | Hansen khác JRC TMF ở đâu? | Hansen đo **cây che phủ** (mọi cây > 5 m, theo ngưỡng % tán). TMF đo **rừng ẩm nhiệt đới**, phân biệt suy thoái và phá rừng theo chuỗi thời gian. Hansen vì thế tính cả chu kỳ chặt cây trồng; TMF thì không bao phủ rừng khô. [Unverified: chưa đọc tài liệu TMF gốc] | SRC-009; SRC-012 |
| 5 | Bản đồ rừng mốc 2020 của EU là gì? | JRC GFC2020: bản đồ có/không có rừng năm 2020, độ phân giải **10 m**, phục vụ EUDR nhưng **không bắt buộc, không ràng buộc pháp lý**. Trên GEE: `JRC/GFC2020/V3` (V2 đã deprecated). | SRC-011 |
| 6 | Giấy phép? | Hansen: CC BY 4.0. GFW workbook, GFC2020: CC BY 4.0 [Unverified]. geoBoundaries: CC BY 3.0 IGO. GADM: chỉ học thuật, **không phân phối lại**, nên bản đồ công bố dùng geoBoundaries. | S8 |
