"""Dien cac bang GEN trong tai lieu tu du lieu truy vet (04-solution/trace/*.csv).
Chay: py 04-solution/trace/build_docs.py   (chay lai moi khi sua CSV)
"""
import csv
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
T = ROOT / "04-solution" / "trace"


def read(n):
    with open(T / f"{n}.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def table(cols, rows):
    out = ["| " + " | ".join(h for h, _ in cols) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        out.append("| " + " | ".join(str(r[k]).replace("|", "/").replace("\n", " ") for _, k in cols) + " |")
    return "\n".join(out)


def fill(path, key, body):
    txt = path.read_text(encoding="utf-8")
    pat = re.compile(rf"(<!-- GEN:{key}:START -->\n).*?(<!-- GEN:{key}:END -->)", re.S)
    if not pat.search(txt):
        sys.exit(f"Thieu moc GEN:{key} trong {path.name}")
    txt = pat.sub(lambda m: m.group(1) + body + "\n" + m.group(2), txt)
    path.write_text(txt, encoding="utf-8", newline="\n")


def main():
    fr, br, nfr = read("fr"), read("br"), read("nfr")
    srs = ROOT / "04-solution" / "S13-srs.md"
    fill(srs, "FR", table([("Mã", "id"), ("Nhóm", "group"), ("Chức năng", "title"), ("Mô tả", "description"),
                           ("Actor", "actor"), ("Nguồn REQ-EU", "req_eu"), ("RC", "rc"), ("MoSCoW", "moscow"),
                           ("Đợt", "release"), ("Màn hình", "scr")], fr))
    fill(srs, "BR", table([("Mã", "id"), ("Quy tắc", "rule_ears"), ("Nguồn", "source"), ("FR", "fr"),
                           ("Tham số", "param")], br))
    fill(srs, "NFR", table([("Mã", "id"), ("Loại", "category"), ("Yêu cầu", "requirement"), ("Đo lường", "measure"),
                            ("Nguồn", "source"), ("MoSCoW", "moscow")], nfr))
    print(f"S13-srs.md: {len(fr)} FR, {len(br)} BR, {len(nfr)} NFR")


if __name__ == "__main__":
    main()
