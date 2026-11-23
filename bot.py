"""useful founder tools · daily content bot.

Renders today's post (content/YYYY-MM-DD.json) and sends it to your Telegram channel:
Video with voiceover (TikTok + Instagram Reels) + caption, Instagram carousel + caption, X post (+ thread).
You post it yourself. The voiceover script is sent too, in case you'd rather record your own voice.

Commands:
  python3 bot.py daily [YYYY-MM-DD]   render and send (today, Europe/Paris, by default)
  python3 bot.py preview [YYYY-MM-DD] render only, into out/ (no Telegram)
  python3 bot.py test                 send a test message to the channel
  python3 bot.py chats                list chats the bot has seen (to find the channel id)
  python3 bot.py bank                 how many days of content are left
Env: TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL (e.g. -1001234567890), DRY_RUN=true|false
Standard library only, plus engine/render.py (Playwright + ffmpeg) for rendering
and engine/voice.py (edge-tts) for the voiceover. VOICE / VOICE_RATE pick the voice.
"""
import datetime
import html
import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT = os.environ.get("TELEGRAM_CHANNEL", "")
DRY = os.environ.get("DRY_RUN", "true").lower() != "false"


def api(method, fields=None, files=None, timeout=180):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    if files:
        b = uuid.uuid4().hex
        parts = [f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
                 for k, v in (fields or {}).items()]
        for name, (fn, data, mime) in files.items():
            parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{name}"; filename="{fn}"\r\n'
                         f'Content-Type: {mime}\r\n\r\n'.encode() + data + b"\r\n")
        parts.append(f"--{b}--\r\n".encode())
        data, headers = b"".join(parts), {"Content-Type": f"multipart/form-data; boundary={b}"}
    else:
        data, headers = json.dumps(fields or {}).encode(), {"Content-Type": "application/json"}
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            last = RuntimeError(f"{method} -> HTTP {e.code}: {e.read().decode(errors='replace')[:400]}")
            if e.code == 429 or e.code >= 500:
                time.sleep(5 * (attempt + 1))
                continue
            raise last
        except (urllib.error.URLError, TimeoutError) as e:
            last = RuntimeError(f"{method} -> {e}")
            time.sleep(3 * (attempt + 1))
    raise last


def send_text(text):
    if DRY:
        print("[DRY RUN] message:\n" + text + "\n")
        return
    api("sendMessage", {"chat_id": CHAT, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True})


def pre(s):
    return f"<pre>{html.escape(s)}</pre>"


def today_paris():
    return datetime.datetime.now(ZoneInfo("Europe/Paris")).date().isoformat()


sys.path.insert(0, str(ROOT / "engine"))
import voice  # noqa: E402


def render(day, out):
    """Voice first (it sets each scene's length), then the video, then the voice goes under it.
    Returns (content, error): error is None when the voiceover worked, else why the video is silent."""
    c = json.loads((ROOT / "content" / f"{day}.json").read_text())
    out.mkdir(parents=True, exist_ok=True)
    clips, err = None, None
    try:
        clips = voice.prepare(c, out)
    except Exception as e:
        err = str(e)[:300]
        print("Voiceover skipped:", err)
    tmp = out / "_content.json"
    tmp.write_text(json.dumps(c))
    subprocess.run([sys.executable, str(ROOT / "engine" / "render.py"), str(tmp), str(out)], check=True)
    if clips:
        try:
            voice.mux(c, out, clips)
        except Exception as e:
            err = "mixing the voice failed: " + str(e)[:250]
            print(err)
    return c, err


def daily(day):
    src = ROOT / "content" / f"{day}.json"
    if not src.exists():
        send_text(f"⚠️ <b>No content for {day}.</b>\nThe content bank is empty. Ask Claude to write the next 2 weeks "
                  f"and add the files to <code>content/</code>.")
        return
    out = ROOT / "out" / day
    c, vo_err = render(day, out)
    left = days_left(day)

    send_text(f"📅 <b>{day} · {html.escape(c.get('format', ''))}</b>\nToday's useful founder tools content. "
              f"Post the video on TikTok and as an Instagram Reel, the carousel on Instagram, the text on X."
              + (f"\n\n⏳ {left} days of content left in the bank." if left <= 4 else ""))

    vcap = f"🎬 <b>TikTok</b> (also Reels / Shorts)\n\n{pre(c['captions']['tiktok'])}"
    if DRY:
        print("[DRY RUN] video:", out / "tiktok.mp4")
    else:
        api("sendVideo", {"chat_id": CHAT, "caption": vcap[:1024], "parse_mode": "HTML", "supports_streaming": "true"},
            {"video": ("tiktok.mp4", (out / "tiktok.mp4").read_bytes(), "video/mp4")})

    say = "\n\n".join(voice.lines(c))
    if vo_err:
        send_text(f"⚠️ <b>The voiceover didn't work today</b>, so the video is silent ({html.escape(vo_err[:200])}).\n"
                  f"Record it yourself, or paste this script into TikTok's text-to-speech:\n\n{pre(say)}")
    else:
        send_text(f"🎙 <b>Voiceover script</b> (already in the video)\n\n{pre(say)}")

    slides = sorted(out.glob("carousel-*.png"))[:10]
    icap = f"🖼 <b>Instagram carousel</b>\n\n{pre(c['captions']['instagram'])}"
    if DRY:
        print("[DRY RUN] carousel:", [p.name for p in slides])
    else:
        media, files = [], {}
        for i, p in enumerate(slides):
            m = {"type": "photo", "media": f"attach://s{i}"}
            if i == 0:
                m.update(caption=icap[:1024], parse_mode="HTML")
            media.append(m)
            files[f"s{i}"] = (p.name, p.read_bytes(), "image/png")
        api("sendMediaGroup", {"chat_id": CHAT, "media": json.dumps(media)}, files)

    send_text(f"𝕏 <b>X post</b>\n\n{pre(c['x_post'])}")
    if c.get("x_thread"):
        send_text("🧵 <b>X thread</b>\n\n" + "\n".join(pre(f"{i+1}/ {t}") for i, t in enumerate(c["x_thread"])))


def days_left(day):
    return len([p for p in (ROOT / "content").glob("*.json") if p.stem >= day])


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "daily"
    day = sys.argv[2] if len(sys.argv) > 2 else today_paris()
    if cmd in ("daily", "test", "chats") and not DRY and not (TOKEN and CHAT or cmd == "chats" and TOKEN):
        sys.exit("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL (or DRY_RUN=true).")
    if cmd == "daily":
        daily(day)
    elif cmd == "preview":
        _, err = render(day, ROOT / "out" / day)
        print("Rendered to", ROOT / "out" / day, "(silent: " + err + ")" if err else "with voiceover")
    elif cmd == "test":
        send_text("✅ useful founder tools bot is connected to this channel.")
    elif cmd == "chats":
        r = api("getUpdates", {"allowed_updates": ["channel_post", "message", "my_chat_member"]})
        seen = {}
        for u in r.get("result", []):
            for k in ("channel_post", "message", "my_chat_member"):
                ch = (u.get(k) or {}).get("chat")
                if ch:
                    seen[ch["id"]] = ch.get("title") or ch.get("username") or ch.get("first_name")
        print("\n".join(f"{i}  {t}" for i, t in seen.items()) or
              "No chats yet: add the bot as admin of the channel, post any message there, then run again.")
    elif cmd == "bank":
        print(f"{days_left(day)} days of content from {day}.")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
