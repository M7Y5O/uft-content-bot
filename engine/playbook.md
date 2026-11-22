# Useful Founder Tools · Content playbook

This is the brief every automated run follows. The engine files (render.py, video.html,
carousel.html, this playbook, example.json) live in the "UFT Content Engine" artifact.

## Brand
- Name: **useful founder tools** (always lowercase in visuals). Handle: @usefulfoundertools.
- Positioning: the AI-first stack for founders & small teams. Tools + AI workflows that run a small company.
- Audience: solo founders, SaaS, e-commerce, freelancers/agencies, creators. English.
- Voice: short, direct, practical. No hype words ("game-changer", "revolutionary"), no emoji in visuals.
- Visual DA (already in the templates): white, ink #121212, blue #2563EB, selection-box highlight on ONE key word.
- Every piece ends with ONE call to action: the free 2-min stack audit, "link in bio".

## Hard rules
1. Never invent numbers, quotes, users, revenue or "a founder I know". Examples must be labelled as examples.
2. Any claim about a tool's price, free plan, limits or features: verify with a web search the same day. If you can't verify, leave it out.
3. Don't name a tool as "best" or "#1". Say what job it does and who it fits.
4. Partner/affiliate links: never in the video itself; captions mention "#ad" only if the post pushes a partner link.
5. Max 5 hashtags. Always include #founder.

## Weekly rotation (Europe/Paris weekday)
| Day | Format | Video scenes (types) | Carousel |
|---|---|---|---|
| Mon | AI workflow | hook → steps (ai) → prompt → cta | cover → steps → prompt → cta |
| Tue | Add / Cut (same as newsletter) | hook → card CUT (red, strike) → card ADD (blue) → cta | cover → text CUT → text ADD → cta |
| Wed | Tool vs tool | hook → versus → card verdict → cta | cover → versus → text "pick X if / Y if" → cta |
| Thu | Stack for a niche | hook → list → card "what can wait" → cta | cover → list → text → cta |
| Fri | Tool in 30 seconds | hook → card (what it is) → steps (how to start) → cta | cover → text → steps → cta |
| Sat | Founder mistake | hook → text-style card → card fix → cta | cover → text (bullets) → text fix → cta |
| Sun | Stack audit promo | hook → list (example result, labelled "example") → cta | cover → steps (how the audit works) → cta |

## Topic bank (take the next unused one: index = days since 2026-11-23, modulo the list for that weekday)
- Mon AI workflow: inbox reply templates (Claude+Notion) · call notes to tasks (Fathom+Notion) · lead research first lines (Clay) · monthly money summary (accounting export+Claude) · Friday founder review (n8n+Claude) · landing page copy in an afternoon (Claude+Framer) · repurpose one newsletter into 10 posts (Claude) · competitor research in an hour (Perplexity+Claude)
- Tue Add/Cut: use the newsletter's ADD and CUT for that week (see newsletter task); if none, pick from: add Tally / cut paid analytics · add Cal.com / cut email back-and-forth · add Notion wiki / cut scattered docs · add Make / cut copy-paste between apps · add Loops / cut manual onboarding emails · add Plausible / cut cookie-heavy analytics · add Crisp / cut support in your personal inbox · add Qonto or Mercury / cut mixing personal and business money
- Wed Versus: Stripe vs Paddle · Make vs Zapier vs n8n · Framer vs Webflow · Beehiiv vs Kit · Notion vs Linear · Cal.com vs Calendly · HubSpot vs Attio · Lovable vs Cursor
- Thu Niche stack: solo SaaS · e-commerce brand · freelance designer · agency of 3 · newsletter creator · coach/consultant · developer tool · course creator
- Fri Tool in 30s: Tally · Fathom · Gamma · Perplexity · Lovable · Clay · PostHog · Cursor
- Sat Mistake: paying for tools before revenue · no business bank account · no email list · building before validating · 5 tools doing one job · no booking link · ignoring sales tax/VAT when selling abroad · doing by hand what AI drafts in seconds
- Sun Audit promo: rotate the example business type (SaaS, e-commerce, freelance, creator)

## content.json (what each run writes, then renders)
See example.json for a full, valid file. Shape:
```
{ "date": "YYYY-MM-DD", "format": "AI workflow",
  "video": { "scenes": [ {"type":"hook","lines":["…","…"],"sel":"word.","sub":"…","dur":3.2}, … ] },
  "carousel": { "slides": [ {"type":"cover","lines":["…"],"sel":"…","sub":"…"}, … ] },
  "captions": { "tiktok": "…", "instagram": "…" },
  "x_post": "…",            // ≤ 280 chars, no hashtags or one max
  "x_thread": ["…","…"]     // optional, 4–6 tweets for Mon/Wed
}
```
Video scene types: hook, card, steps, list, versus, prompt, cta. Fields: see video.html `sceneHTML`.
Carousel slide types: cover, text, steps, list, versus, prompt, cta (see carousel.html `body`).
Lengths: video 22–32 s total (hook 3–3.5 s, cta 5–6 s); carousel 5–8 slides.
Text budget: hook ≤ 6 words + 1 selected word; card titles ≤ 6 words; steps ≤ 9 words each; ≤ 5 steps.

## Quality check before delivering
Render frames first (`python3 render.py content.json out frames`) and look at each one:
no text clipped or overflowing, nothing under y=1600 in the video (TikTok UI), selection box on one word only.
Fix the JSON, then the full render (`python3 render.py content.json out`).
