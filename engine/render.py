"""Useful Founder Tools content engine.
Usage: python3 render.py content.json OUTDIR
Renders: OUTDIR/tiktok.mp4 (1080x1920, 30fps), OUTDIR/carousel-NN.png (1080x1350),
and OUTDIR/posts.md (X post + captions). Needs playwright (chromium) and ffmpeg.
"""
import asyncio, json, os, subprocess, sys, pathlib
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).resolve().parent
FPS = 30

async def render_video(pg, content, out):
    await pg.set_viewport_size({"width": 1080, "height": 1920})
    await pg.goto((HERE / "video.html").as_uri()); await pg.wait_for_timeout(300)
    spans = await pg.evaluate("c => build(c)", content["video"])
    parts, frame = [], 0
    for i, (a, b) in enumerate(spans):
        n = round((b - a) * FPS); tmp = out / f"_scene{i}.tmp.mp4"; fin = out / f"_scene{i}.mp4"
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS),
                               "-c:v", "mjpeg", "-i", "-", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                               "-pix_fmt", "yuv420p", "-r", str(FPS), str(tmp)], stdin=subprocess.PIPE)
        for k in range(n):
            await pg.evaluate(f"render({(frame + k) / FPS})")
            ff.stdin.write(await pg.screenshot(type="jpeg", quality=92))
        frame += n; ff.stdin.close()
        if ff.wait() != 0: raise SystemExit(f"ffmpeg failed on scene {i}")
        os.replace(tmp, fin); parts.append(fin)
    lst = out / "_list.txt"; lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(out / "tiktok.tmp.mp4")], check=True, cwd=out)
    os.replace(out / "tiktok.tmp.mp4", out / "tiktok.mp4")
    for p in parts: p.unlink()
    lst.unlink()

async def render_carousel(pg, content, out):
    slides = content["carousel"]["slides"]
    await pg.set_viewport_size({"width": 1080, "height": 1350})
    await pg.goto((HERE / "carousel.html").as_uri()); await pg.wait_for_timeout(300)
    for i in range(len(slides)):
        await pg.evaluate("([s,i]) => show(s,i)", [slides, i])
        await pg.screenshot(path=str(out / f"carousel-{i+1:02d}.png"))

async def frames(pg, content, out, times):
    await pg.set_viewport_size({"width": 1080, "height": 1920})
    await pg.goto((HERE / "video.html").as_uri()); await pg.wait_for_timeout(300)
    await pg.evaluate("c => build(c)", content["video"])
    for t in times:
        await pg.evaluate(f"render({t})")
        await pg.screenshot(path=str(out / f"_frame_{t}.jpg"), type="jpeg", quality=80)

def write_posts(content, out):
    c = content
    md = [f"# {c.get('date','')} · {c.get('format','')}", "",
          "## TikTok caption", c["captions"]["tiktok"], "",
          "## Instagram caption", c["captions"]["instagram"], "",
          "## X post", c["x_post"], ""]
    if c.get("x_thread"):
        md += ["## X thread"] + [f"{i+1}/ {t}" for i, t in enumerate(c["x_thread"])] + [""]
    (out / "posts.md").write_text("\n".join(md))

async def main():
    content = json.loads(pathlib.Path(sys.argv[1]).read_text())
    out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    mode = sys.argv[3] if len(sys.argv) > 3 else "all"
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        if mode == "frames":
            ts = []; t = 0
            for s in content["video"]["scenes"]:
                d = s.get("dur", 5); ts.append(round(t + d - 0.5, 2)); t += d
            await frames(pg, content, out, ts)
        elif mode == "carousel":
            await render_carousel(pg, content, out)
        else:
            await render_carousel(pg, content, out)
            await render_video(pg, content, out)
            write_posts(content, out)
        await b.close()

asyncio.run(main())
