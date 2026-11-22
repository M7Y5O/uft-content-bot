#!/usr/bin/env python3
"""The Stack Sheet sender: Notion (subscribers + issues) -> SMTP.

Commands:
  send          send every issue marked Ready whose Send date is today or earlier
  test [N]      send issue N (or the next Ready one) to TEST_TO only
  list          print subscriber counts, send nothing
  setup         create the two databases inside the shared Notion page and print their ids

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
    if t == "status": return (v or {}).get("name", "")
    if t == "multi_select": return ", ".join(x["name"] for x in v or [])
    return ""


def setv(page, prop, value):
    """Write a value whatever type the column has (select, status, text, date, number)."""
    t = page["properties"].get(prop, {}).get("type")
    if t is None: return
    if t == "select": body = {"select": {"name": value}}
    elif t == "status": body = {"status": {"name": value}}
    elif t == "date": body = {"date": {"start": value}}
    elif t == "number": body = {"number": float(value)}
    elif t == "checkbox": body = {"checkbox": bool(value)}
    else: body = {t: [{"type": "text", "text": {"content": str(value)}}]}
    notion("PATCH", f"pages/{page['id']}", {"properties": {prop: body}})


def subscribers():
    """One entry per email. The newest row wins, so an unsubscribe row cancels an older signup."""
    rows = sorted(query(E("NOTION_SUBSCRIBERS_DB")), key=lambda p: p["created_time"])
    people = {}
    for p in rows:
        pr = p["properties"]
        title_key = next((k for k, v in pr.items() if v["type"] == "title"), "Email")
        email = str(text(pr.get("Email")) or text(pr.get(title_key))).strip().lower()
        if "@" not in email: continue
        status = text(pr.get("Status")) or "Subscribed"
        prev = people.get(email, {})
        people[email] = {"email": email, "status": status, "page": p,
                         "last_sent": str(text(pr.get("Last sent")) or prev.get("last_sent", ""))[:10]}
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
    issues = []
    for p in query(E("NOTION_ISSUES_DB")):
        pr = p["properties"]
        title_key = next((k for k, v in pr.items() if v["type"] == "title"), "Title")
        date = str(text(pr.get("Send date")) or "")[:10]
        if str(text(pr.get("Status"))).strip().lower() != "ready" or not date or date > TODAY: continue
        try: no = int(float(str(text(pr.get("Issue")) or "0").lstrip("#")))
        except ValueError: continue
        try: sent_to = int(float(text(pr.get("Sent to")) or 0))
        except ValueError: sent_to = 0
        issues.append({"page": p, "no": no, "title": text(pr[title_key]),
                       "subject": text(pr.get("Subject")) or text(pr[title_key]),
                       "preview": text(pr.get("Preview text")), "date": date, "sent_to": sent_to})
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
                    if not DRY: setv(p["page"], "Status", "Bounced")
                    continue
                if not DRY:
                    setv(p["page"], "Last sent", iss["date"])
                p["last_sent"] = iss["date"]; sent += 1; sent_total += 1
                time.sleep(1.2)
            left = len([p for p in people if p["last_sent"] < iss["date"]])
            if not DRY:
                setv(iss["page"], "Sent to", (iss["sent_to"] or 0) + sent)
                if left == 0: setv(iss["page"], "Status", "Sent")
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


def cmd_setup():
    """Create the Subscribers + Issues databases inside the Notion page shared with the integration."""
    pages = notion("POST", "search", {"filter": {"property": "object", "value": "page"}})["results"]
    want = (E("NOTION_PAGE_TITLE") or "useful founder tool").lower()
    def title(pg):
        for v in pg["properties"].values():
            if v["type"] == "title": return "".join(x["plain_text"] for x in v["title"]).strip()
        return ""
    page = next((pg for pg in pages if title(pg).lower().startswith(want[:12])), None)
    if not page:
        sys.exit("Page not found. In Notion open the page, ••• → Connections → add your integration, then run setup again. "
                 f"Pages visible: {[title(pg) for pg in pages]}")
    existing = notion("POST", "search", {"filter": {"property": "object", "value": "database"}})["results"]
    have = {"".join(x["plain_text"] for x in d["title"]).strip(): d["id"] for d in existing
            if d.get("parent", {}).get("page_id", "").replace("-", "") == page["id"].replace("-", "")}
    sel = lambda *o: {"select": {"options": [{"name": n, "color": c} for n, c in o]}}
    if "Subscribers" not in have:
        have["Subscribers"] = notion("POST", "databases", {
            "parent": {"type": "page_id", "page_id": page["id"]},
            "title": [{"type": "text", "text": {"content": "Subscribers"}}],
            "properties": {"Email": {"title": {}},
                           "Status": sel(("Subscribed", "green"), ("Unsubscribed", "gray"), ("Bounced", "red")),
                           "Topics": {"rich_text": {}},
                           "Source": sel(("heroForm", "blue"), ("nlForm", "purple"), ("import", "gray")),
                           "Audit score": {"number": {}}, "Signed up": {"created_time": {}},
                           "Last sent": {"date": {}}}})["id"]
    if "Issues" not in have:
        have["Issues"] = notion("POST", "databases", {
            "parent": {"type": "page_id", "page_id": page["id"]},
            "title": [{"type": "text", "text": {"content": "Issues"}}],
            "properties": {"Title": {"title": {}}, "Issue": {"number": {}},
                           "Status": sel(("Draft", "gray"), ("Ready", "blue"), ("Sent", "green")),
                           "Send date": {"date": {}}, "Subject": {"rich_text": {}},
                           "Preview text": {"rich_text": {}}, "Sent to": {"number": {}}}})["id"]
    if not [r for r in query(have["Issues"]) if text(next(v for v in r["properties"].values() if v["type"] == "title"))]:
        rt = lambda t: {"rich_text": [{"type": "text", "text": {"content": t}}]}
        for r in query(have["Issues"]):  # drop the blank starter rows Notion adds
            notion("PATCH", f"pages/{r['id']}", {"archived": True})
        notion("POST", "pages", {"parent": {"database_id": have["Issues"]}, "properties": {
            "Title": {"title": [{"type": "text", "text": {"content": "The week-one stack & your first AI workflow"}}]},
            "Issue": {"number": 1}, "Status": {"select": {"name": "Ready"}},
            "Send date": {"date": {"start": "2026-11-24"}},
            "Subject": rt("The Stack Sheet #1: the week-one stack + your first AI workflow"),
            "Preview text": rt("One tool to add, one to cut, and a workflow you can set up before lunch.")}})
    print(f"Page: {title(page)}")
    print(f"NOTION_SUBSCRIBERS_DB={have['Subscribers'].replace('-', '')}")
    print(f"NOTION_ISSUES_DB={have['Issues'].replace('-', '')}")


if __name__ == "__main__":
    a = sys.argv[1:] or ["send"]
    if not E("NOTION_TOKEN"):
        print("Newsletter not configured yet: add the NOTION_TOKEN secret."); sys.exit(0)
    if a[0] != "setup" and not (E("NOTION_SUBSCRIBERS_DB") and E("NOTION_ISSUES_DB")):
        print("Run the workflow with command 'setup' first, then add NOTION_SUBSCRIBERS_DB and NOTION_ISSUES_DB variables."); sys.exit(0)
    {"send": cmd_send, "test": lambda: cmd_test(a[1] if len(a) > 1 and a[1] else None),
     "list": cmd_list, "setup": cmd_setup}.get(a[0], lambda: sys.exit(f"unknown command {a[0]}"))()
