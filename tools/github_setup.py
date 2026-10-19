"""T0.2 + T12.2 - Tao nhan, milestone va issue tren GitHub tu du lieu trong repo.

Can: bien moi truong GITHUB_TOKEN (fine-grained token, quyen Issues: Read and write tren repo).
Chay thu (khong goi API):  py tools/github_setup.py --dry-run
Chay that:                 py tools/github_setup.py --repo taint7684/eudr-coffee-ba
Chay lai an toan: bo qua nhan/milestone/issue da ton tai (so theo tieu de).
Project board ("Roadmap", "ECTS Backlog") tao tren giao dien web roi them issue theo nhan.
"""
import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"

LABELS = {
    "task": "5319e7", "epic": "0e8a16", "story": "1d76db", "must": "b60205", "should": "d93f0b",
    "could": "fbca04", "wont": "cccccc", "mvp": "006b75", "R2": "0052cc", "R3": "5319e7",
    **{f"P{i}": "c5def5" for i in range(7)}, **{f"EP-0{i}": "0e8a16" for i in range(1, 6)},
}
MILESTONES = {"M1": "Tuần 3 — Discovery", "M2": "Tuần 8 — Dữ liệu & phản biện",
              "M3": "Tuần 15 — Thiết kế giải pháp", "M4": "Tuần 18 — Đóng gói"}


def read(p):
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f))


class GH:
    def __init__(self, repo, token, dry):
        self.repo, self.token, self.dry = repo, token, dry

    def call(self, method, path, body=None):
        if self.dry and method != "GET":
            print(f"[dry-run] {method} {path} {body.get('title') or body.get('name') if body else ''}")
            return {}
        req = urllib.request.Request(f"{API}/repos/{self.repo}{path}", method=method,
                                     data=json.dumps(body).encode() if body else None)
        req.add_header("Accept", "application/vnd.github+json")
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        try:
            with urllib.request.urlopen(req) as r:
                return json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            if self.dry:
                return []
            sys.exit(f"{method} {path} -> {e.code} {e.read().decode()[:200]}")

    def all(self, path):
        if self.dry:
            return []
        out, page = [], 1
        while True:
            chunk = self.call("GET", f"{path}{'&' if '?' in path else '?'}per_page=100&page={page}")
            out += chunk
            if len(chunk) < 100:
                return out
            page += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="taint7684/eudr-coffee-ba")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    if not token and not a.dry_run:
        sys.exit("Thieu GITHUB_TOKEN")
    gh = GH(a.repo, token, a.dry_run)

    have = {x["name"] for x in gh.all("/labels")}
    for name, color in LABELS.items():
        if name not in have:
            gh.call("POST", "/labels", {"name": name, "color": color})

    ms = {x["title"]: x["number"] for x in gh.all("/milestones?state=all")}
    for t, d in MILESTONES.items():
        if t not in ms:
            ms[t] = gh.call("POST", "/milestones", {"title": t, "description": d}).get("number")

    titles = {x["title"] for x in gh.all("/issues?state=all")}
    for t in read(ROOT / "00-management" / "tasks.csv"):
        title = f"{t['id']}: {t['title']}"
        if title in titles:
            continue
        body = f"**Output:** {t['output']}\n\n**Trạng thái:** {t['status']}\n\n{t['note']}"
        issue = {"title": title, "body": body, "labels": ["task", t["phase"]], "milestone": ms.get(t["milestone"])}
        res = gh.call("POST", "/issues", issue)
        if t["status"].startswith("Done") and res.get("number"):
            gh.call("PATCH", f"/issues/{res['number']}", {"state": "closed"})

    trace = ROOT / "04-solution" / "trace"
    acs = read(trace / "ac.csv")
    for u in read(trace / "us.csv"):
        title = f"{u['id']}: {u['story'][:90]}"
        if title in titles:
            continue
        g = "\n".join(f"Scenario: {x['id']}\n  Given {x['given']}\n  When {x['when']}\n  Then {x['then']}"
                      for x in acs if x["us"] == u["id"])
        body = (f"## Story\n{u['story']}\n\n## FR liên quan\n{u['fr']}\n\n## BR liên quan\n{u['br'] or '—'}\n\n"
                f"## Tiêu chí chấp nhận\n```gherkin\n{g}\n```\n\n## Màn hình\n{u['scr']}\n")
        labels = ["story", u["epic"], u["moscow"].lower()] + (["mvp"] if u["release"] == "MVP" else [u["release"]])
        gh.call("POST", "/issues", {"title": title, "body": body, "labels": labels, "milestone": ms.get("M3")})
    print("Xong.")


if __name__ == "__main__":
    main()
