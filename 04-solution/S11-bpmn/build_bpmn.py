"""T9.1 - Sinh file BPMN 2.0 (co Diagram Interchange) cho quy trinh To-Be cap 1 cua ECTS.
Mo bang Camunda Modeler hoac https://demo.bpmn.io. Anh PNG: tools/render_bpmn.js.
Chay: py 04-solution/S11-bpmn/build_bpmn.py
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(__file__).resolve().parent / "ects-to-be.bpmn"

LANES = ["Đại lý", "Hệ thống ECTS", "Tuân thủ (DN)", "Thu mua (DN)", "Nhà nhập khẩu EU"]
LH, LX, X0, COL = 150, 30, 60, 165   # chieu cao lane, le trai, x pool, buoc cot

# id: (loai, ten, lane, cot)
N = {
    "start": ("startEvent", "Nông hộ đồng ý tham gia", 0, 0),
    "t1": ("userTask", "Đăng ký nông hộ + đồng ý dữ liệu [BR-006]", 0, 1),
    "g1": ("exclusiveGateway", "Lô > 4 ha?", 0, 2),
    "t2a": ("userTask", "Lấy điểm GPS [BR-001]", 0, 3),
    "t2b": ("userTask", "Vẽ đa giác ranh lô [BR-002, BR-003]", 1, 3),
    "g2": ("exclusiveGateway", "", 0, 4),
    "t3": ("userTask", "Nhập giấy tờ đất [BR-020]", 0, 5),
    "t4": ("serviceTask", "Kiểm tra hình học, chồng lấn, pháp lý [BR-004, 005, 021]", 1, 5.6),
    "t5": ("businessRuleTask", "Chấm rủi ro lô R1–R6 [BR-010…014]", 1, 6.6),
    "g3": ("exclusiveGateway", "Kết quả chấm?", 1, 7.6),
    "t6": ("userTask", "Xác minh Vùng xám: ảnh lịch sử / thực địa [BR-016]", 2, 7.6),
    "g4": ("exclusiveGateway", "Kết luận?", 2, 8.6),
    "endx": ("endEvent", "Lô không bán dòng EU", 2, 9.6),
    "t8": ("userTask", "Ghi giao dịch dòng EU theo lô [BR-030, 031]", 0, 9.2),
    "t9": ("userTask", "Nhập kho, lập lô hàng EU tách dòng [BR-032, 033]", 3, 10.0),
    "t10": ("userTask", "Lập gói dữ liệu DDS [BR-040, 041]", 2, 10.6),
    "t11": ("sendTask", "Gửi gói cho nhà nhập khẩu", 2, 11.6),
    "t12": ("userTask", "Nộp DDS lên hệ thống thông tin EU (ngoài ECTS)", 4, 11.6),
    "g5": ("exclusiveGateway", "Kết quả DDS?", 4, 12.6),
    "endok": ("endEvent", "Có số tham chiếu — thông quan", 4, 13.6),
}
# (tu, den, nhan)
F = [("start", "t1", ""), ("t1", "g1", ""), ("g1", "t2a", "Không"), ("g1", "t2b", "Có"), ("t2a", "g2", ""),
     ("t2b", "g2", ""), ("g2", "t3", ""), ("t3", "t4", ""), ("t4", "t5", ""), ("t5", "g3", ""),
     ("g3", "t8", "Đạt"), ("g3", "t6", "Vùng xám"), ("g3", "endx", "Loại"), ("t6", "g4", ""),
     ("g4", "t8", "Đạt"), ("g4", "endx", "Loại"), ("t8", "t9", ""), ("t9", "t10", ""), ("t10", "t11", ""),
     ("t11", "t12", ""), ("t12", "g5", ""), ("g5", "endok", "Chấp nhận"), ("g5", "t10", "Từ chối [BR-042]")]

SIZE = {"startEvent": (36, 36), "endEvent": (36, 36), "exclusiveGateway": (50, 50)}


def box(nid):
    k, _, lane, col = N[nid]
    w, h = SIZE.get(k, (130, 80))
    cx = X0 + LX + 70 + col * COL
    cy = 20 + lane * LH + LH / 2
    return cx - w / 2, cy - h / 2, w, h


def center(nid):
    x, y, w, h = box(nid)
    return x + w / 2, y + h / 2


VFIRST = {("g1", "t2b"), ("g3", "t8")}  # di doc truoc de khong cat qua phan tu khac


def waypoints(a, b):
    (ax, ay), (bx, by) = center(a), center(b)
    xa, ya, wa, ha = box(a)
    xb, yb, wb, hb = box(b)
    if abs(ay - by) < 1:
        if bx > ax:
            return [(xa + wa, ay), (xb, by)]
        top = min(ya, yb) - 30
        return [(ax, ya), (ax, top), (bx, top), (bx, yb)]
    if bx < ax:  # quay lui (Tu choi -> lap lai goi)
        return [(ax, ya if by < ay else ya + ha), (ax, by + hb / 2 + 25 if by < ay else by), (bx, by + hb / 2 + 25), (bx, yb + hb)]
    if abs(bx - ax) < 1:
        return [(ax, ya + ha if by > ay else ya), (bx, yb if by > ay else yb + hb)]
    if (a, b) in VFIRST:
        return [(ax, ya + ha if by > ay else ya), (ax, by), (xb, by)]
    return [(xa + wa, ay), (bx, ay), (bx, yb if by > ay else yb + hb)]


def main():
    pw = X0 + LX + 70 + 13.6 * COL + 120 - X0
    ph = LH * len(LANES)
    sem, di = [], []
    for nid, (k, name, _, _) in N.items():
        inc = "".join(f"<bpmn:incoming>f_{a}_{b}</bpmn:incoming>" for a, b, _ in F if b == nid)
        out = "".join(f"<bpmn:outgoing>f_{a}_{b}</bpmn:outgoing>" for a, b, _ in F if a == nid)
        sem.append(f'    <bpmn:{k} id="{nid}" name="{escape(name)}">{inc}{out}</bpmn:{k}>')
        x, y, w, h = box(nid)
        lbl = f'<bpmndi:BPMNLabel><dc:Bounds x="{x - 30:.0f}" y="{y + h + 4:.0f}" width="{w + 60:.0f}" height="28" /></bpmndi:BPMNLabel>' if k in SIZE else ""
        di.append(f'      <bpmndi:BPMNShape id="{nid}_di" bpmnElement="{nid}"{" isMarkerVisible=\"true\"" if k == "exclusiveGateway" else ""}>'
                  f'<dc:Bounds x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" />{lbl}</bpmndi:BPMNShape>')
    for a, b, lab in F:
        sem.append(f'    <bpmn:sequenceFlow id="f_{a}_{b}" name="{escape(lab)}" sourceRef="{a}" targetRef="{b}" />')
        wp = "".join(f'<di:waypoint x="{x:.0f}" y="{y:.0f}" />' for x, y in waypoints(a, b))
        di.append(f'      <bpmndi:BPMNEdge id="f_{a}_{b}_di" bpmnElement="f_{a}_{b}">{wp}</bpmndi:BPMNEdge>')
    lanes_sem, lanes_di = [], []
    for i, ln in enumerate(LANES):
        refs = "".join(f"<bpmn:flowNodeRef>{nid}</bpmn:flowNodeRef>" for nid, v in N.items() if v[2] == i)
        lanes_sem.append(f'      <bpmn:lane id="lane{i}" name="{escape(ln)}">{refs}</bpmn:lane>')
        lanes_di.append(f'      <bpmndi:BPMNShape id="lane{i}_di" bpmnElement="lane{i}" isHorizontal="true">'
                        f'<dc:Bounds x="{X0 + LX}" y="{20 + i * LH}" width="{pw - LX:.0f}" height="{LH}" /></bpmndi:BPMNShape>')
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" id="ects_defs" targetNamespace="https://github.com/taint7684/eudr-coffee-ba">
  <bpmn:collaboration id="collab">
    <bpmn:participant id="pool" name="ECTS — Quy trình To-Be cấp 1 (S11)" processRef="ects_tobe" />
  </bpmn:collaboration>
  <bpmn:process id="ects_tobe" isExecutable="false">
    <bpmn:laneSet id="ls">
{chr(10).join(lanes_sem)}
    </bpmn:laneSet>
{chr(10).join(sem)}
  </bpmn:process>
  <bpmndi:BPMNDiagram id="d">
    <bpmndi:BPMNPlane id="p" bpmnElement="collab">
      <bpmndi:BPMNShape id="pool_di" bpmnElement="pool" isHorizontal="true"><dc:Bounds x="{X0}" y="20" width="{pw:.0f}" height="{ph}" /></bpmndi:BPMNShape>
{chr(10).join(lanes_di)}
{chr(10).join(di)}
    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>
</bpmn:definitions>
'''
    OUT.write_text(xml, encoding="utf-8", newline="\n")
    print(OUT.name, len(N), "phần tử,", len(F), "luồng")


if __name__ == "__main__":
    main()
