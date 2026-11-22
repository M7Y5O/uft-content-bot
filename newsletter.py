#!/usr/bin/env python3
"""The Stack Sheet sender: Notion (subscribers + issues) -> SMTP.

Commands:
  send          send every issue marked Ready whose Send date is today or earlier
  test [N]      send issue N (or the next Ready one) to TEST_TO only
  list          print subscriber counts, send nothing

Env:
  NOTION_TOKEN            Notion internal integration secret (shared with the UFT page)
  NOTION_SUBSCRIBERS_DB   Subscribers database id
  NOTION_ISSUES_DB        Issues database id
  SMTP_HOST SMTP_PORT SMTP_USER SMTP_PASS
  FROM_EMAIL  FROM_NAME   e.g. hello@usefulfoundertools.me / The Stack Sheet
  REPLY_TO                optional, e.g. info@usefulfoundertools.me
  TEST_TO                 inbox for `test`
  MAX_PER_RUN             default 400 (Gmail allows ~500 a day; the rest go out next run)
  DRY_RUN                 "true" prints instead of sending
  TELEGRAM_BOT_TOKEN TELEGRAM_CHANNEL   optional: post a short report
"""
import json, os, smtplib, ssl, sys, time, urllib.parse, urllib.request
from datetime import datetime
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
TODAY = datetime.now(ZoneInfo("Europe/Paris")).date().isoformat()
UNSUB_FORM = "https://tally.so/r/EqxP54"
E = os.environ.get
DRY = E("DRY_RUN", "true").lower() != "false"


def notion(method, path, body=None):
    req = urllib.request.Request(
        "https://api.notion.com/v1/" + path, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "Bearer " + E("NOTION_TOKEN", ""),
                 "Notion-Version": "2022-06-28", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Notion {method} {path} failed: {e.code} {e.read().decode()[:400]}")


def query(db, flt=None):
    out, cursor = [], None
    while True:
        body = {"page_size": 100}
        if flt: body["filter"] = flt
        if cursor: body["start_cursor"] = cursor
        r = notion("POST", f"databases/{db}/query", body)
        out += r["results"]
        if not r.get("has_more"): return out
        cursor = r["next_cursor"]


def text(prop):
    if not prop: return ""
    t = prop["type"]
    v = prop.get(t)
    if t in ("title", "rich_text"): return "".join(x["plain_text"] for x in v).strip()
    if t == "select": return (v or {}).get("name", "")
    if t == "email": return v or ""
    if t == "number": return v
    if t == "date": return (v or {}).get("start", "")
    return ""


def subscribers():
    """One entry per email. The newest row wins, so an unsubscribe row cancels an older signup."""
    rows = sorted(query(E("NOTION_SUBSCRIBERS_DB")), key=lambda p: p["created_time"])
    people = {}
    for p in rows:
        pr = p["properties"]
        email = text(pr.get("Email")).lower()
        if "@" not in email: continue
        status = text(pr.get("Status")) or "Subscribed"
        prev = people.get(email, {})
        people[email] = {"email": email, "status": status, "page": p["id"],
                         "last_sent": text(pr.get("Last sent")) or prev.get("last_sent", "")}
    return people


def render(issue_no, email):
    html = (ROOT / "newsletter" / f"issue-{issue_no:03d}.html").read_text()
    unsub = UNSUB_FORM + "?" + urllib.parse.urlencode({"email": email, "status": "Unsubscribed"})
    return html.replace("{{unsubscribe_url}}", unsub), unsub


def plain_text(html):
    import re, html as h
    t = re.sub(r"(?is)<(style|head).*?</\1>", "", html)
    t = re.sub(r"(?i)<br\s*/?>|</(p|tr|h\d|li|div)>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    return re.sub(r"\n\s*\n+", "\n\n", h.unescape(t)).strip()


class Mailer:
    def __init__(self):
        self.s = None
        if DRY: return
        host, port = E("SMTP_HOST", "smtp.gmail.com"), int(E("SMTP_PORT", "465"))
        ctx = ssl.create_default_context()
        if port == 465:
            self.s = smtplib.SMTP_SSL(host, port, context=ctx, timeout=60)
        else:
            self.s = smtplib.SMTP(host, port, timeout=60); self.s.starttls(context=ctx)
        self.s.login(E("SMTP_USER"), E("SMTP_PASS"))

    def send(self, to, subject, preview, html, unsub):
        m = EmailMessage()
        frm = E("FROM_EMAIL", "hello@usefulfoundertools.me")
        m["From"] = formataddr((E("FROM_NAME", "The Stack Sheet"), frm))
        m["To"] = to
        m["Subject"] = subject
        m["Message-ID"] = make_msgid(domain=frm.split("@")[1])
        if E("REPLY_TO"): m["Reply-To"] = E("REPLY_TO")
        m["List-Unsubscribe"] = f"<{unsub}>, <mailto:{E('REPLY_TO') or frm}?subject=unsubscribe>"
        m.set_content(plain_text(html))
        m.add_alternative(html, subtype="html")
        if DRY:
            print(f"  [dry] {to}: {subject}"); return
        self.s.send_message(m)

    def close(self):
        if self.s: self.s.quit()


def telegram(msg):
    tok, ch = E("TELEGRAM_BOT_TOKEN"), E("TELEGRAM_CHANNEL")
    if not (tok and ch) or DRY: return
    data = urllib.parse.urlencode({"chat_id": ch, "text": msg}).encode()
    try: urllib.request.urlopen(f"https://api.telegram.org/bot{tok}/sendMessage", data, timeout=20)
    except Exception as e: print("telegram report failed:", e)


def ready_issues():
    flt = {"and": [{"property": "Status", "select": {"equals": "Ready"}},
                   {"property": "Send date", "date": {"on_or_before": TODAY}}]}
    issues = []
    for p in query(E("NOTION_ISSUES_DB"), flt):
        pr = p["properties"]
        issues.append({"page": p["id"], "no": int(text(pr["Issue"]) or 0), "title": text(pr["Title"]),
                       "subject": text(pr["Subject"]) or text(pr["Title"]),
                       "preview": text(pr["Preview text"]), "date": text(pr["Send date"]),
                       "sent_to": text(pr["Sent to"]) or 0})
    return sorted(issues, key=lambda i: i["no"])


def cmd_send():
    issues = ready_issues()
    if not issues:
        print(f"No Ready issue due on or before {TODAY}."); return
    people = [p for p in subscribers().values() if p["status"] == "Subscribed"]
    cap, mailer, sent_total = int(E("MAX_PER_RUN", "400")), Mailer(), 0
    try:
        for iss in issues:
            todo = [p for p in people if p["last_sent"] < iss["date"]]
            print(f"Issue #{iss['no']} '{iss['subject']}': {len(todo)} to send ({len(people)} subscribed)")
            sent = 0
            for p in todo:
                if sent_total >= cap: break
                html, unsub = render(iss["no"], p["email"])
                try:
                    mailer.send(p["email"], iss["subject"], iss["preview"], html, unsub)
                except smtplib.SMTPRecipientsRefused:
                    if not DRY: notion("PATCH", f"pages/{p['page']}", {"properties": {"Status": {"select": {"name": "Bounced"}}}})
                    continue
                if not DRY:
                    notion("PATCH", f"pages/{p['page']}", {"properties": {"Last sent": {"date": {"start": iss["date"]}}}})
                p["last_sent"] = iss["date"]; sent += 1; sent_total += 1
                time.sleep(1.2)
            left = len([p for p in people if p["last_sent"] < iss["date"]])
            if not DRY:
                props = {"Sent to": {"number": (iss["sent_to"] or 0) + sent}}
                if left == 0: props["Status"] = {"select": {"name": "Sent"}}
                notion("PATCH", f"pages/{iss['page']}", {"properties": props})
            msg = f"📬 Stack Sheet #{iss['no']}: sent to {sent} subscribers" + (f", {left} left for the next run." if left else ". Done ✓")
            print(msg); telegram(msg)
            if sent_total >= cap: break
    finally:
        mailer.close()


def cmd_test(no=None):
    to = E("TEST_TO") or sys.exit("Set TEST_TO first.")
    if no is None:
        issues = ready_issues() or sys.exit("No Ready issue; pass an issue number: test 1")
        iss = issues[0]
    else:
        iss = {"no": int(no), "subject": f"[TEST] The Stack Sheet #{int(no)}", "preview": ""}
    html, unsub = render(iss["no"], to)
    m = Mailer()
    m.send(to, "[TEST] " + iss["subject"].replace("[TEST] ", ""), iss["preview"], html, unsub)
    m.close()
    print(f"Test of issue #{iss['no']} sent to {to}")


def cmd_list():
    ppl = subscribers().values()
    by = {}
    for p in ppl: by[p["status"]] = by.get(p["status"], 0) + 1
    print(f"{len(ppl)} unique emails:", by)


if __name__ == "__main__":
    a = sys.argv[1:] or ["send"]
    {"send": cmd_send, "test": lambda: cmd_test(a[1] if len(a) > 1 and a[1] else None),
     "list": cmd_list}.get(a[0], lambda: sys.exit(f"unknown command {a[0]}"))()
