"""Voiceover for the daily video.

For each video scene: speak scene["say"] (or a line built from the scene's on-screen text) with a free
Microsoft neural voice (edge-tts), stretch the scene so the voice fits, then lay the voice track under
tiktok.mp4 once it is rendered.

  prepare(content, out) -> list of clip paths, and updates each scene's "dur" in content (call BEFORE rendering)
  mux(content, out, clips)  -> adds the voice to out/tiktok.mp4 (call AFTER rendering)
  script(content)           -> the full voiceover text

Env: VOICE (default en-US-AndrewNeural), VOICE_RATE (default +6%)
"""
import asyncio
import os
import re
import subprocess

FPS = 30
VOICE = os.environ.get("VOICE") or "en-US-AndrewNeural"
RATE = os.environ.get("VOICE_RATE") or "+6%"
LEAD = 0.25   # silence before the voice starts in each scene (s)
TAIL = 0.55   # breathing room after the voice, before the next scene (s)


def clean(t):
    t = re.sub(r"<[^>]+>", " ", str(t or ""))
    t = re.sub(r"[↓↑→←✦·•]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def auto_say(s):
    """A spoken line from the on-screen text, for scenes without a written "say"."""
    k = s.get("type")
    head = " ".join(s.get("lines", [])) + (" " + s["sel"] if s.get("sel") else "")
    if k == "hook":
        return clean(head + ". " + s.get("sub", ""))
    if k == "cta":
        return clean(head + " Take the free two-minute stack audit. Link in bio.")
    parts = [s.get("title", "")]
    if s.get("body"):
        parts.append(s["body"])
    parts += [x if isinstance(x, str) else f"{x.get('name', '')}, {x.get('meta', '')}" for x in s.get("steps", []) + s.get("items", [])]
    for side in ("left", "right"):
        if s.get(side):
            parts.append(s[side]["name"] + ": " + ", ".join(s[side].get("points", [])))
    if s.get("text"):
        parts.append(s["text"])
    return clean(". ".join(p.rstrip(".") for p in parts if p)) + "."


def lines(content):
    return [clean(s.get("say")) or auto_say(s) for s in content["video"]["scenes"]]


def script(content):
    return "\n".join(lines(content))


def length(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


async def _edge(text, path):
    import edge_tts
    await edge_tts.Communicate(text, VOICE, rate=RATE).save(str(path))


def speak(text, path):
    last = None
    for _ in range(3):
        try:
            asyncio.run(_edge(text, path))
            if path.exists() and path.stat().st_size > 1000:
                return
        except Exception as e:  # network hiccup or service change
            last = e
    raise RuntimeError(f"text-to-speech failed: {last}")


def prepare(content, out, synth=speak):
    clips = []
    for i, (s, text) in enumerate(zip(content["video"]["scenes"], lines(content))):
        p = out / f"_vo{i}.mp3"
        synth(text, p)
        need = LEAD + length(p) + TAIL
        s["dur"] = round(max(float(s.get("dur", 5)), need), 2)
        clips.append(p)
    return clips


def scene_seconds(content):
    """Exact length of each rendered scene, matching render.py's frame rounding."""
    secs, t = [], 0.0
    for s in content["video"]["scenes"]:
        d = s.get("dur") or 5
        secs.append(round((t + d - t) * FPS) / FPS)
        t += d
    return secs


def mux(content, out, clips):
    video = out / "tiktok.mp4"
    secs = scene_seconds(content)
    ms = int(LEAD * 1000)
    chains = [f"[{i + 1}:a]aresample=44100,aformat=channel_layouts=mono,adelay={ms},apad,atrim=0:{d:.4f},asetpts=N/SR/TB[a{i}]"
              for i, d in enumerate(secs)]
    graph = ";".join(chains) + ";" + "".join(f"[a{i}]" for i in range(len(secs))) + f"concat=n={len(secs)}:v=0:a=1[vo]"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video)]
    for c in clips:
        cmd += ["-i", str(c)]
    tmp = out / "tiktok.voiced.mp4"
    cmd += ["-filter_complex", graph, "-map", "0:v", "-map", "[vo]", "-c:v", "copy",
            "-c:a", "aac", "-b:a", "160k", "-ac", "2", "-shortest", "-movflags", "+faststart", str(tmp)]
    subprocess.run(cmd, check=True)
    os.replace(tmp, video)
    for c in clips:
        c.unlink(missing_ok=True)
