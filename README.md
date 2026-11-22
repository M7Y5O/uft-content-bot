# useful founder tools · daily content bot

Every morning it renders the day's **TikTok video**, **Instagram carousel** and **X post** in the site's DA and sends them to your private Telegram channel **UFT · Daily content**. You post them yourself.

Same setup as `meme-smart-money`: free GitHub Actions + a Telegram bot. No Zapier, no paid API.

## What's in here

| Path | What it is |
|---|---|
| `content/YYYY-MM-DD.json` | One day of content (video scenes, carousel slides, captions, X post). 14 days written, Nov 23 → Dec 6. |
| `engine/` | Renderer (`render.py`, `video.html`, `carousel.html`) and the content playbook. |
| `bot.py` | Renders today's file and sends it to Telegram. |
| `.github/workflows/daily.yml` | Runs `bot.py daily` every morning (~06:40 Paris). |

## Setup (10 minutes)

1. **Create the bot**: in Telegram, message **@BotFather** → `/newbot` → name `UFT Content` → username e.g. `uft_content_bot`. Copy the token. Keep it private.
2. **Add the bot to the channel**: open **UFT · Daily content** → Manage channel → Administrators → Add admin → your bot (it only needs "Post messages").
3. **Publish this folder to GitHub** with GitHub Desktop: File → Add local repository → `development/uft-content-bot` → Publish repository (untick "Keep this code private" so Actions minutes are free; the token stays secret).
4. On github.com → repo → **Settings → Secrets and variables → Actions**:
   - **Secrets**: `TELEGRAM_BOT_TOKEN` = the token from BotFather
   - **Variables**: `DRY_RUN` = `true` for now
5. **Find the channel id**: post any message in the channel, then Actions → "UFT daily content" → Run workflow → command `chats`. The log prints a number like `-1001234567890  UFT · Daily content`. Add it as the variable `TELEGRAM_CHANNEL`.
6. **Test**: Run workflow → `test` (sends "connected" to the channel). Then set `DRY_RUN` = `false` and Run workflow → `daily` to receive today's content.

From then on it runs every morning by itself.

## Good to know

- **Content bank**: `bot.py` posts the file for today's date. When fewer than 5 days are left, the daily message warns you. Ask Claude to "write the next 2 weeks of UFT content" and drop the new JSON files in `content/`, then push with GitHub Desktop.
- **Preview locally**: `python3 bot.py preview 2026-11-24` renders into `out/` without sending (needs `pip install playwright && playwright install chromium` and ffmpeg).
- GitHub can start scheduled runs a few minutes late, and pauses schedules in public repos after 60 days without commits; adding new content files keeps it active.
- Videos have no sound: add a trending sound in TikTok/Instagram when you post.
