"""T3.1 - Chuyen van ban EUR-Lex (XHTML lay tu Cellar) sang van ban thuan de trich nguyen van.

Tai van ban goc (khong commit, xem 02-regulatory/README.md):
  curl -L -H "Accept: application/xhtml+xml" -H "Accept-Language: eng" \
       -o 02-regulatory/raw/{CELEX}.html http://publications.europa.eu/resource/celex/{CELEX}
Chay: py 02-regulatory/scripts/html2txt.py
"""
import html
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAW = Path(__file__).resolve().parents[1] / "raw"


def to_text(src: str) -> str:
    src = re.sub(r"(?is)<(script|style|head).*?</\1>", "", src)
    src = re.sub(r"(?i)<br\s*/?>", "\n", src)
    src = re.sub(r"(?i)</(p|div|tr|li|h\d|table)>", "\n", src)
    src = re.sub(r"(?i)</td>", "\t", src)
    src = re.sub(r"<[^>]+>", "", src)
    src = html.unescape(src).replace("\xa0", " ")
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in src.splitlines()]
    out, blank = [], False
    for ln in lines:
        if not ln:
            if not blank:
                out.append("")
            blank = True
        else:
            out.append(ln)
            blank = False
    return "\n".join(out).strip() + "\n"


def main():
    for f in sorted(RAW.glob("*.html")):
        txt = to_text(f.read_text(encoding="utf-8"))
        dst = f.with_suffix(".txt")
        dst.write_text(txt, encoding="utf-8", newline="\n")
        print(f"{f.name} -> {dst.name}: {len(txt.splitlines())} dong")


if __name__ == "__main__":
    main()
