"""T3.2 + T3.3 - Sinh 02-regulatory/S7-eudr-requirements.csv.

Cot verbatim_text KHONG go tay: script tim doan van ban goc chua `anchor` trong file .txt
(sinh boi html2txt.py tu van ban tai ve tu Cellar) va chep nguyen doan. Anchor khong tim thay
hoac trung nhieu doan -> script dung lai, khong ghi file. Nhu vay moi cau trich deu truy duoc
ve van ban goc, khong co cau trich nao duoc go tay.

Chay: py 02-regulatory/scripts/build_s7.py
"""
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
BASE = Path(__file__).resolve().parents[1]
DOCS = {
    "O": BASE / "raw" / "eudr_32023R1115.txt",  # SRC-001 ban goc
    "A": BASE / "raw" / "32025R2650.txt",       # SRC-003 ban sua doi
}

# (article, doc, anchor, requirement_plain, applies_to, vn_current_state, level, evidence_src, related_gap, related_rc, notes)
# applies_to: OP = operator EU (nha nhap khau) · DS = downstream operator/trader EU · EXP = DN xuat khau VN (nha cung cap cua OP)
#             FARM = nong ho · CA = co quan co tham quyen EU
ROWS = [
    ("Điều 3(a)", "O", "they are deforestation-free;",
     "Hàng đưa vào EU phải không gây phá rừng.", "OP; EXP",
     "Việt Nam được xếp rủi ro thấp, nhưng phần lớn nông hộ không có dữ liệu lô để chứng minh từng lô.", "⚠️",
     "SRC-004; SRC-027", "GAP-01; GAP-04", "RC-02; RC-06", ""),
    ("Điều 3(b)", "O", "they have been produced in accordance with the relevant legislation of the country of production; and",
     "Hàng phải được sản xuất đúng luật nước sở tại.", "OP; EXP",
     "Hồ sơ quyền sử dụng đất của nông hộ không đầy đủ hoặc không số hóa; DN không lưu bản sao.", "⚠️",
     "SRC-027", "GAP-05", "RC-05", "Xem Điều 2(40) cho danh mục luật liên quan."),
    ("Điều 3(c) (sửa bởi 2025/2650)", "A", "they are covered by a due diligence statement or a simplified declaration",
     "Hàng phải có DDS hoặc tờ khai đơn giản hóa (chỉ cho nhà sản xuất siêu nhỏ/nhỏ ở nước rủi ro thấp tự đưa hàng vào EU).", "OP",
     "DDS do operator EU nộp; DN VN hiện không có gói dữ liệu đủ trường Phụ lục II để chuyển cho operator.", "⛔",
     "SRC-003; DEC-03", "GAP-06", "RC-02", "Nông hộ VN không tự xuất khẩu sang EU nên tờ khai đơn giản hóa không áp dụng cho luồng chính."),
    ("Điều 2(13)", "O", "that the relevant products contain, have been fed with or have been made using, relevant commodities that were produced on land that has not been subject to deforestation after 31 December, 2020; and",
     "Mốc cắt: đất trồng không bị phá rừng sau 31/12/2020.", "OP; EXP; FARM",
     "Không có bằng chứng hiện trạng đất tại 31/12/2020 cho từng lô.", "⛔",
     "SRC-011", "GAP-04", "RC-06", "Cần ảnh/bản đồ mốc 2020 (JRC GFC2020) làm tham chiếu."),
    ("Điều 2(4)", "O", "‘forest’ means land spanning more than 0,5 hectares",
     "Định nghĩa rừng của EUDR (> 0,5 ha, cây > 5 m, độ che phủ > 10%, loại trừ đất nông nghiệp/đô thị).", "OP; EXP",
     "Định nghĩa rừng trong Luật Lâm nghiệp VN khác ngưỡng [Unverified: cần trích Luật Lâm nghiệp 2017]; GFW đo cây che phủ chứ không đo rừng.", "✏️",
     "SRC-008", "GAP-04", "RC-06", "Phải thống nhất định nghĩa khi chấm rủi ro lô (DEC-06)."),
    ("Điều 2(6)", "O", "‘agricultural plantation’ means land with tree stands in agricultural production systems",
     "Đồn điền nông nghiệp, kể cả nông lâm kết hợp có cây trồng dưới tán, không phải là rừng.", "OP; EXP",
     "Cà phê trồng xen cây che bóng (sầu riêng, muồng, tiêu trên trụ sống) có thể bị vệ tinh nhận là cây che phủ.", "✏️",
     "SRC-008", "GAP-04", "RC-06", "Nguồn gốc của sai lệch giữa 'mất cây che phủ' và 'phá rừng' (S10)."),
    ("Điều 2(28)", "O", "‘geolocation’ means the geographical location of a plot of land",
     "Tọa độ lô: ít nhất 1 điểm, 6 chữ số thập phân; lô > 4 ha phải dùng đa giác.", "EXP; FARM",
     "Chỉ khoảng 1/10 nông hộ được khảo sát giữ dữ liệu cấp lô.", "⛔",
     "SRC-027", "GAP-01", "RC-03", "BR chính cho chức năng đăng ký lô."),
    ("Điều 2(27)", "O", "‘plot of land’ means land within a single real-estate property",
     "Lô đất là đất trong một bất động sản được luật nước sở tại công nhận, điều kiện đủ đồng nhất.", "EXP; FARM",
     "Ánh xạ lô EUDR ↔ thửa đất trên giấy chứng nhận QSDĐ chưa có quy ước; một nông hộ có thể có nhiều thửa.", "✏️",
     "[Inference]", "GAP-05", "RC-05", "Quyết định: 1 lô ECTS = 1 thửa trên giấy chứng nhận, hoặc 1 vùng canh tác liền khoảnh khi không có giấy."),
    ("Điều 4(1)", "O", "Operators shall exercise due diligence in accordance with Article 8 prior",
     "Operator phải thẩm định trước khi đưa hàng vào thị trường.", "OP",
     "Nghĩa vụ của nhà nhập khẩu EU; DN VN là nguồn dữ liệu đầu vào.", "⚠️",
     "SRC-001; DEC-03", "GAP-06", "RC-02", ""),
    ("Điều 4(2)", "O", "Operators shall not place relevant products on the market or export them without prior submission",
     "Không có DDS trên hệ thống thông tin Điều 33 thì không được đưa hàng vào thị trường.", "OP",
     "Không có cơ chế chuyển dữ liệu lô cho operator để lập DDS.", "⛔",
     "DEC-03", "GAP-06", "RC-02", ""),
    ("Điều 4(3) (sửa bởi 2025/2650)", "A", "By making the due diligence statement available to competent authorities or, in the case of micro",
     "Operator chịu trách nhiệm khi nộp DDS; lưu DDS 5 năm.", "OP",
     "Operator sẽ đòi nhà cung cấp cam kết và lưu bằng chứng tương ứng.", "⚠️",
     "SRC-003", "GAP-06", "RC-02", ""),
    ("Điều 4(4)", "O", "Operators shall not place relevant products on the market or export them where one or more",
     "Cấm đưa hàng khi không tuân thủ, có rủi ro không không đáng kể, hoặc không làm được thẩm định.", "OP; EXP",
     "Hàng trộn không tách được lô có rủi ro bị operator từ chối.", "⛔",
     "[Inference]", "GAP-02; GAP-03", "RC-01; RC-04", ""),
    ("Điều 4(7) (sửa bởi 2025/2650)", "A", "Operators shall communicate to downstream operators and to traders",
     "Operator chuyển số tham chiếu DDS cho downstream operator/trader.", "OP; DS",
     "DN VN cần nhận lại số tham chiếu DDS để liên kết hồ sơ lô hàng.", "⚠️",
     "SRC-003", "GAP-06", "RC-02", "FR theo dõi số tham chiếu DDS."),
    ("Điều 5(3) (sửa bởi 2025/2650)", "A", "Downstream operators and traders shall collect and keep the following information",
     "Downstream operator/trader lưu thông tin nhà cung cấp, khách hàng và số tham chiếu DDS.", "DS",
     "Ngoài phạm vi DN VN; nêu để hiểu chuỗi phía EU.", "✏️",
     "SRC-003", "", "", ""),
    ("Điều 7", "O", "Where a natural or legal person established outside the Union places relevant products",
     "Người đầu tiên thành lập tại EU làm cho hàng có mặt trên thị trường được coi là operator.", "OP; EXP",
     "DN VN dễ hiểu nhầm mình là operator phải nộp DDS.", "✏️",
     "SRC-001; DEC-03", "", "", "Căn cứ DEC-03."),
    ("Điều 6(1) (sửa bởi 2025/2650)", "A", "Operators may mandate an authorised representative to submit",
     "Operator có thể ủy quyền đại diện nộp DDS, nhưng vẫn chịu trách nhiệm.", "OP",
     "Đại diện phải thành lập tại EU (Điều 2(22)) nên DN VN không làm thay được.", "✏️",
     "SRC-003; DEC-03", "", "", ""),
    ("Điều 9(1)", "O", "Operators shall collect information, documents and data which demonstrate",
     "Thu thập, tổ chức và lưu 5 năm thông tin kèm bằng chứng cho từng sản phẩm.", "OP; EXP",
     "Đại lý ghi sổ/Excel; không lưu bằng chứng theo lô hàng.", "⛔",
     "ASM-06", "GAP-06", "RC-01; RC-02", "NFR lưu trữ ≥ 5 năm."),
    ("Điều 9(1)(b) (sửa bởi 2025/2650)", "A", "the quantity of the relevant products; for relevant products entering or leaving the market",
     "Khối lượng sản phẩm theo kg khối lượng tịnh, gắn mã HS.", "OP; EXP",
     "DN có số liệu khối lượng theo hợp đồng/vận đơn.", "✏️",
     "[Inference]", "", "", "Đáp ứng một phần sẵn có; cần gắn khối lượng với lô đất (cân bằng khối lượng)."),
    ("Điều 9(1)(c)", "O", "the country of production and, where relevant, parts thereof;",
     "Ghi nước sản xuất và vùng (nếu có).", "EXP",
     "DN biết vùng thu mua ở mức tỉnh.", "✏️",
     "[Inference]", "", "", "Đáp ứng được."),
    ("Điều 9(1)(d)", "O", "the geolocation of all plots of land where the relevant commodities that the relevant product contains",
     "Tọa độ của mọi lô đất và thời gian sản xuất; lô có phá rừng làm loại toàn bộ hàng từ lô đó.", "EXP; FARM",
     "Không có tọa độ; hàng trộn từ nhiều hộ nên không liệt kê được 'mọi lô'.", "⛔",
     "SRC-027", "GAP-01; GAP-02; GAP-03", "RC-02; RC-03; RC-04", "Yêu cầu cốt lõi của ECTS."),
    ("Điều 9(1)(e)", "O", "the name, postal address and email address of any business or person from whom",
     "Tên, địa chỉ, email của mọi bên cung cấp hàng.", "EXP",
     "Thương lái phi chính thức thường không có thông tin định danh đầy đủ.", "⚠️",
     "[Inference]", "GAP-07", "RC-01", ""),
    ("Điều 9(1)(f) (sửa bởi 2025/2650)", "A", "the name, postal address and email address of any business, downstream operator or trader",
     "Tên, địa chỉ, email của bên nhận hàng.", "OP",
     "DN có sẵn thông tin khách hàng EU.", "✏️",
     "[Inference]", "", "", "Đáp ứng được."),
    ("Điều 9(1)(g)", "O", "adequately conclusive and verifiable information that the relevant products are deforestation-free;",
     "Thông tin đủ kết luận và kiểm chứng được rằng hàng không phá rừng.", "OP; EXP",
     "Chưa có quy trình chồng lớp lô với bản đồ rừng 2020 và mất cây che phủ sau 2020.", "⛔",
     "SRC-011; DEC-04", "GAP-04", "RC-06", "Căn cứ giữ module chấm rủi ro lô dù VN rủi ro thấp."),
    ("Điều 9(1)(h)", "O", "adequately conclusive and verifiable information that the relevant commodities have been produced in accordance",
     "Thông tin kiểm chứng được về tính hợp pháp, gồm quyền sử dụng khu đất.", "OP; EXP; FARM",
     "Giấy tờ đất không số hóa; một phần nông hộ thiếu giấy tờ.", "⛔",
     "SRC-027", "GAP-05", "RC-05", ""),
    ("Điều 2(40)(a)", "O", "land use rights;",
     "Luật liên quan gồm quyền sử dụng đất (và môi trường, quyền bên thứ ba, lao động, nhân quyền, FPIC, thuế, chống tham nhũng, hải quan).", "EXP; FARM",
     "Chưa có danh mục luật VN tương ứng; EC dự kiến kho dữ liệu luật quốc gia đến 12/2026 [Unverified].", "✏️",
     "SRC-025", "GAP-05", "RC-05", "Phạm vi dự án: chỉ quyền sử dụng đất."),
    ("Điều 10(1)", "O", "Operators shall verify and analyse the information collected",
     "Operator đánh giá rủi ro; chỉ đưa hàng khi rủi ro bằng không hoặc không đáng kể.", "OP",
     "Được miễn khi đủ điều kiện Điều 13 (VN rủi ro thấp).", "✏️",
     "SRC-004", "", "", "Xem REQ-EU về Điều 13."),
    ("Điều 10(2)(i)", "O", "the complexity of the relevant supply chain and the stage of processing",
     "Tiêu chí: độ phức tạp chuỗi và khó khăn khi liên kết sản phẩm với lô đất.", "OP; EXP",
     "Chuỗi 4–5 tầng (nông hộ → thương lái → đại lý → nhà máy → XK).", "⛔",
     "[Inference]", "GAP-02; GAP-03", "RC-01; RC-04", "Cũng là điều kiện đánh giá trong Điều 13(1)."),
    ("Điều 10(2)(j)", "O", "the risk of circumvention of this Regulation or of mixing with relevant products of unknown origin",
     "Tiêu chí: rủi ro trộn với hàng không rõ nguồn gốc.", "OP; EXP",
     "Kho đại lý/nhà máy trộn hàng nhiều nguồn.", "⛔",
     "[Inference]", "GAP-03", "RC-04", "Mô hình tách dòng/cân bằng khối lượng phải chọn ở SRS."),
    ("Điều 10(4)", "O", "The operators shall document and review the risk assessments at least on an annual basis",
     "Ghi nhận và rà soát đánh giá rủi ro ít nhất mỗi năm.", "OP",
     "Không có hồ sơ đánh giá.", "⚠️",
     "[Inference]", "GAP-06", "RC-02", ""),
    ("Điều 11(1)", "O", "Except where a risk assessment carried out in accordance with Article 10 reveals",
     "Giảm thiểu rủi ro: thêm thông tin, khảo sát độc lập, hỗ trợ nhà cung cấp nhỏ.", "OP; EXP",
     "Chưa có quy trình xác minh thực địa cho lô nghi vấn.", "⚠️",
     "[Inference]", "GAP-04", "RC-06", "Cơ sở cho quy trình Vùng xám."),
    ("Điều 12(1)", "O", "In order to exercise due diligence in accordance with Article 8, operators shall establish",
     "Operator duy trì hệ thống thẩm định (quy trình và biện pháp).", "OP",
     "Không có.", "⚠️",
     "[Inference]", "GAP-06", "RC-02", ""),
    ("Điều 12(5)", "O", "Operators shall keep for at least five years all documentation related to due diligence",
     "Lưu toàn bộ hồ sơ thẩm định ít nhất 5 năm.", "OP; EXP",
     "Không có kho hồ sơ số.", "⛔",
     "ASM-06", "GAP-06", "RC-02", "NFR lưu trữ."),
    ("Điều 13(1)", "O", "When placing relevant products on the market or exporting them, operators shall not be required to fulfil the obligations under Articles 10 and 11",
     "Thẩm định đơn giản hóa: miễn Điều 10–11 khi chắc chắn toàn bộ hàng từ nước rủi ro thấp, sau khi đánh giá độ phức tạp chuỗi và rủi ro trộn.", "OP; EXP",
     "VN rủi ro thấp; điều kiện còn thiếu là chứng minh không trộn với hàng nước khác/hàng không rõ nguồn.", "⚠️",
     "SRC-004", "GAP-03", "RC-04", "DEC-04."),
    ("Điều 13(2)", "O", "Notwithstanding paragraph 1 of this Article, if the operator obtains or is made aware",
     "Có thông tin chỉ ra rủi ro (kể cả substantiated concern) thì phải thẩm định đầy đủ.", "OP; EXP",
     "DN không có kênh tiếp nhận/xử lý cảnh báo.", "⚠️",
     "SRC-004", "GAP-04", "RC-06", "FR cảnh báo khi lô nằm trong vùng mất cây che phủ mới."),
    ("Điều 16(3) (sửa bởi 2025/2650)", "A", "The competent authorities shall use a risk-based approach to identify the checks",
     "Cơ quan có thẩm quyền chọn đối tượng kiểm tra theo rủi ro, gồm việc lô có liền kề rừng hay không.", "CA; OP",
     "Lô cà phê ven rừng ở các huyện mất che phủ cao dễ bị chọn kiểm tra.", "✏️",
     "SRC-003; SRC-008", "GAP-04", "RC-06", "Căn cứ chỉ số rủi ro huyện (S9)."),
    ("Điều 26(4) (sửa bởi 2025/2650)", "A", "The reference number of the due diligence statement or the declaration identifier for micro or small primary operators shall be made available to customs",
     "Số tham chiếu DDS phải có trước khi hải quan EU thông quan.", "OP",
     "Thiếu số tham chiếu thì lô hàng bị giữ tại cảng EU.", "⚠️",
     "SRC-003", "GAP-06", "RC-02", "Mốc thời gian: gói dữ liệu DDS phải gửi trước ngày tàu đến."),
    ("Phụ lục II, mục 2", "O", "Harmonised System code, free-text description",
     "DDS gồm mã HS, mô tả, khối lượng.", "OP; EXP",
     "Có sẵn ở chứng từ xuất khẩu.", "✏️",
     "[Inference]", "", "", "Trường trong gói dữ liệu DDS."),
    ("Phụ lục II, mục 3", "O", "Country of production and the geolocation of all plots of land where the relevant commodities were produced.",
     "DDS gồm nước sản xuất và tọa độ mọi lô.", "OP; EXP",
     "Không có.", "⛔",
     "SRC-027", "GAP-01; GAP-02", "RC-02; RC-03", "Trường cốt lõi trong gói dữ liệu DDS."),
    ("Điều 4a(5) (thêm bởi 2025/2650)", "A", "For micro or small primary operators, the geolocation referred to in Article 9(1), point (d), may be replaced by the postal address",
     "Nhà sản xuất siêu nhỏ/nhỏ ở nước rủi ro thấp tự đưa hàng vào EU được dùng địa chỉ bưu chính thay tọa độ.", "FARM",
     "Không áp dụng cho luồng chính (nông hộ bán qua DN VN, không tự đưa hàng vào EU).", "✏️",
     "SRC-003", "", "", "Câu hỏi phỏng vấn S20: vì sao không dùng địa chỉ thay tọa độ."),
    ("Điều 38(2) (sửa bởi 2025/2650)", "A", "Subject to paragraph 3 of this Article, Articles 3 to 13",
     "Áp dụng từ 30/12/2026 (DN siêu nhỏ/nhỏ thành lập trước 31/12/2024: 30/06/2027 theo khoản 3).", "OP; EXP",
     "Còn khoảng 2 tháng tính từ 20/10/2026.", "⛔",
     "SRC-003", "GAP-01", "RC-03", "Tham số hóa ngày áp dụng trong hệ thống (RSK-01)."),
]

COLS = ["id", "article", "verbatim_text", "requirement_plain", "applies_to", "vn_current_state",
        "level", "evidence_src", "related_gap", "related_rc", "notes"]


def main():
    texts = {k: [ln for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()] for k, p in DOCS.items()}
    out, errors = [], []
    for i, (art, doc, anchor, plain, applies, state, level, ev, gap, rc, notes) in enumerate(ROWS, 1):
        hits = [ln for ln in texts[doc] if anchor in ln]
        if len(hits) != 1:
            errors.append(f"{art}: anchor tim thay {len(hits)} doan: {anchor[:60]}")
            continue
        src = "SRC-001" if doc == "O" else "SRC-003"
        out.append(dict(zip(COLS, [f"REQ-EU-{i:03d}", f"{art} [{src}]", hits[0], plain, applies, state,
                                   level, ev, gap, rc, notes])))
    if errors:
        sys.exit("Loi anchor:\n" + "\n".join(errors))
    dst = BASE / "S7-eudr-requirements.csv"
    with open(dst, "w", newline="\n", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(out)
    from collections import Counter
    c = Counter(r["level"] for r in out)
    print(f"{len(out)} yeu cau -> {dst.name}; muc: {dict(c)}")


if __name__ == "__main__":
    main()
