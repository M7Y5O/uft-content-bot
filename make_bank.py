"""Writes the content bank: one JSON per day in content/YYYY-MM-DD.json."""
import json, pathlib, datetime

OUT = pathlib.Path(__file__).parent / "content"
OUT.mkdir(exist_ok=True)
TAGS = "#founder #startup #aitools #solofounder"

def cta_scene(lines, sel, follow="Follow for one tool to add & one to cut, every week."):
    return {"type": "cta", "lines": lines, "sel": sel, "button": "Free 2-min stack audit", "follow": follow, "dur": 6}

def cta_slide(lines, sel, sub="Our free 2-min audit names your gaps."):
    return {"type": "cta", "lines": lines, "sel": sel, "sub": sub}

DAYS = []

# ---------- Week 1 ----------
DAYS.append(("2026-11-23", json.loads((pathlib.Path(__file__).parent / "engine" / "example.json").read_text())))

DAYS.append(("2026-11-24", {
 "format": "Add / Cut",
 "video": {"scenes": [
   {"type": "hook", "lines": ["Stop", "paying for"], "sel": "this.", "sub": "if you're a founder ↓", "dur": 3.2},
   {"type": "card", "tag": "CUT", "tone": "red", "strike": True, "title": "Premium analytics plan", "body": "At a few hundred visitors a month,<br><b>a free plan tells you the same thing.</b>", "chips": ["PostHog · free tier", "Google Analytics · free"], "dur": 6.5},
   {"type": "card", "tag": "ADD", "tone": "blue", "title": "Tally", "body": "Waitlists, surveys, onboarding forms.<br><b>Type a question, hit enter, done.</b>", "dur": 6.5},
   cta_scene(["What else", "should you"], "cut?")]},
 "carousel": {"slides": [
   {"type": "cover", "lines": ["One tool to cut.", "One to"], "sel": "add.", "sub": "This week's Stack Sheet, in 4 slides."},
   {"type": "text", "eyebrow": "cut", "tone": "red", "lines": ["The paid analytics plan", "you don't have traffic for"], "bullets": ["A few hundred visitors a month", "One number matters: visitors → signups", "Free tiers of PostHog or Google Analytics cover it"]},
   {"type": "text", "eyebrow": "add", "tone": "blue", "lines": ["Tally, for every form", "you'll need this year"], "bullets": ["Waitlists, surveys, client briefs", "Builds like a doc: type, enter, done", "Put 3 questions behind every 'contact us'"]},
   cta_slide(["What else", "should you"], "cut?")]},
 "captions": {
   "tiktok": f"Stop paying for analytics you don't have traffic for. Add Tally instead. Free stack audit in bio. {TAGS}",
   "instagram": f"CUT: the premium analytics plan at a few hundred visitors a month.\nADD: Tally for every waitlist, survey and onboarding form.\n\nSave this. Free 2-min stack audit: link in bio.\n\n{TAGS}"},
 "x_post": "Cut: the premium analytics plan you don't have traffic for. A free tier tells you the same thing at a few hundred visitors a month.\n\nAdd: Tally. Every waitlist, survey and onboarding form, built like a doc."}))

DAYS.append(("2026-11-25", {
 "format": "Tool vs tool",
 "video": {"scenes": [
   {"type": "hook", "lines": ["Stripe or", "Paddle?"], "sel": "taxes.", "sub": "the answer is about ↑", "dur": 3.4},
   {"type": "versus", "title": "Who handles the tax?", "left": {"name": "Stripe", "points": ["You are the seller", "You file sales tax / VAT", "Lower fees, full control"]}, "right": {"name": "Paddle", "points": ["Merchant of record", "They collect and file tax", "Higher fees, less work"]}, "dur": 8},
   {"type": "card", "tag": "PICK", "tone": "green", "title": "Selling software worldwide?", "body": "A merchant of record saves you the tax work.<br><b>One country or services? Stripe.</b>", "dur": 6.5},
   cta_scene(["Which payment tool", "fits your"], "stack?")]},
 "carousel": {"slides": [
   {"type": "cover", "lines": ["Stripe vs Paddle:", "it's about"], "sel": "taxes.", "sub": "Merchant of record, explained in 4 slides."},
   {"type": "versus", "eyebrow": "the difference", "lines": ["Who is the", "seller?"], "left": {"name": "Stripe", "points": ["You are the seller", "You register and file tax", "Lower fees"]}, "right": {"name": "Paddle", "points": ["They are the seller", "They collect and file tax", "Higher fees"]}},
   {"type": "text", "eyebrow": "how to pick", "tone": "green", "lines": ["Pick Paddle if…", "pick Stripe if…"], "bullets": ["Software sold in many countries, small team → Paddle", "One country, services or custom billing → Stripe", "Physical products → your store's checkout"], "body": "Not tax advice: check your obligations with an accountant."},
   cta_slide(["Which tools", "fit your"], "stack?")]},
 "captions": {
   "tiktok": f"Stripe vs Paddle isn't about features. It's about who files your sales tax. Free stack audit in bio. {TAGS} #saas",
   "instagram": f"Stripe or Paddle? Ask one question: who is the seller?\n\nStripe: you are, you handle tax.\nPaddle: they are (merchant of record), they handle tax.\n\nNot tax advice. Free 2-min stack audit: link in bio.\n\n{TAGS}"},
 "x_post": "Stripe vs Paddle isn't a feature question.\n\nStripe: you're the seller, you file sales tax/VAT.\nPaddle: merchant of record, they collect and file it.\n\nSoftware sold worldwide with a tiny team? MoR usually wins. One country? Stripe.",
 "x_thread": ["Stripe vs Paddle, explained in 5 tweets:", "Stripe is a payment processor. You're the seller, so registering and filing sales tax/VAT is on you.", "Paddle is a merchant of record. It's legally the seller, collects the tax, files it, pays you the rest.", "MoR fees are higher, but the cross-border tax work leaves your desk.", "Rule of thumb: software sold in many countries → MoR. One country, services, custom billing → Stripe. Not tax advice.", "Free 2-min stack audit picks the right one for you. Link in bio."]}))

DAYS.append(("2026-11-26", {
 "format": "Stack for a niche",
 "video": {"scenes": [
   {"type": "hook", "lines": ["The solo", "SaaS"], "sel": "stack.", "sub": "6 tools, one job each ↓", "dur": 3.2},
   {"type": "list", "tag": "SOLO SAAS", "title": "Everything you need", "items": [
     {"name": "Framer", "meta": "marketing site"}, {"name": "Supabase", "meta": "database + auth"}, {"name": "Vercel", "meta": "deploys"},
     {"name": "Stripe or Paddle", "meta": "payments"}, {"name": "Loops", "meta": "product email"}, {"name": "Claude", "meta": "AI assistant", "badge": "✦ AI"}], "dur": 9},
   {"type": "card", "tag": "WHAT CAN WAIT", "tone": "amber", "title": "CRM, helpdesk, Slack", "body": "Add them when the volume shows up.<br><b>Not before.</b>", "dur": 5.5},
   cta_scene(["What's missing", "from your"], "stack?")]},
 "carousel": {"slides": [
   {"type": "cover", "lines": ["The solo", "SaaS"], "sel": "stack.", "sub": "Six tools, one job each. Save it."},
   {"type": "list", "eyebrow": "the stack", "lines": ["Everything you need", "to launch"], "items": [
     {"name": "Framer", "meta": "marketing site"}, {"name": "Supabase + Vercel", "meta": "database, auth, deploys"},
     {"name": "Stripe or Paddle", "meta": "payments"}, {"name": "Loops", "meta": "onboarding and product email"}, {"name": "Claude", "meta": "writing, code review, research", "badge": "✦ AI"}]},
   {"type": "text", "eyebrow": "what can wait", "tone": "amber", "lines": ["Don't buy these", "yet"], "bullets": ["A CRM before you have leads", "A helpdesk before you have tickets", "Team chat before you have a team"]},
   cta_slide(["What's missing", "from your"], "stack?")]},
 "captions": {
   "tiktok": f"The solo SaaS stack: 6 tools, one job each. Save it. Free stack audit in bio. {TAGS} #saas #indiehacker",
   "instagram": f"The solo SaaS stack ✦\n\nFramer · Supabase · Vercel · Stripe or Paddle · Loops · Claude\n\nWhat can wait: CRM, helpdesk, team chat.\n\nSave this. Free 2-min stack audit: link in bio.\n\n{TAGS}"},
 "x_post": "The solo SaaS stack:\n\nFramer (site)\nSupabase (db + auth)\nVercel (deploys)\nStripe or Paddle (payments)\nLoops (product email)\nClaude (everything else)\n\nCRM, helpdesk, team chat: later."}))

DAYS.append(("2026-11-27", {
 "format": "Tool in 30 seconds",
 "video": {"scenes": [
   {"type": "hook", "lines": ["Decks in", "minutes,", "not"], "sel": "hours.", "dur": 3.4},
   {"type": "card", "tag": "✦ AI TOOL", "tone": "solid", "title": "Gamma", "body": "Turns a prompt or your notes into<br><b>a deck, a doc or a one-page site.</b>", "dur": 6},
   {"type": "steps", "tag": "HOW TO START", "tone": "blue", "title": "Your first deck", "steps": ["Paste your notes or outline", "Pick a theme close to your brand", "Edit the 2–3 slides that matter", "Export or share the link"], "dur": 8},
   cta_scene(["Which AI tools", "fit your"], "stack?", "Follow for one AI tool every week.")]},
 "carousel": {"slides": [
   {"type": "cover", "lines": ["Pitch decks in minutes,", "not"], "sel": "hours.", "sub": "Gamma, in 30 seconds."},
   {"type": "text", "eyebrow": "✦ ai tool", "tone": "solid", "lines": ["What Gamma", "does"], "bullets": ["Turns a prompt or notes into slides", "Also makes docs and one-page sites", "Good for proposals, pitch decks, recaps"]},
   {"type": "steps", "eyebrow": "how to start", "lines": ["Your first", "deck"], "steps": ["Paste your notes or outline", "Pick a theme close to your brand", "Edit the 2–3 slides that matter", "Export or share the link"]},
   cta_slide(["Which AI tools", "fit your"], "stack?")]},
 "captions": {
   "tiktok": f"Gamma turns your notes into a deck in minutes. Here's how to start. Free stack audit in bio. {TAGS}",
   "instagram": f"Gamma in 30 seconds ✦\n\nPaste notes → pick a theme → edit what matters → share.\n\nSave this for your next pitch. Free 2-min stack audit: link in bio.\n\n{TAGS}"},
 "x_post": "Stop building decks slide by slide.\n\nPaste your notes into Gamma, pick a theme, then spend your time on the 2-3 slides that actually matter."}))

DAYS.append(("2026-11-28", {
 "format": "Founder mistake",
 "video": {"scenes": [
   {"type": "hook", "lines": ["The most", "expensive", "founder"], "sel": "mistake.", "dur": 3.4},
   {"type": "card", "tag": "MISTAKE", "tone": "red", "title": "Paying before revenue", "body": "CRM, analytics, helpdesk, automations…<br><b>for a company with no customers yet.</b>", "dur": 6.5},
   {"type": "card", "tag": "FIX", "tone": "green", "title": "Free plans first", "body": "Upgrade only when a limit blocks revenue<br><b>or a missing feature costs you an hour a week.</b>", "dur": 7},
   cta_scene(["What are you", "overpaying"], "for?")]},
 "carousel": {"slides": [
   {"type": "cover", "lines": ["The most expensive", "founder"], "sel": "mistake.", "sub": "And the rule that fixes it."},
   {"type": "text", "eyebrow": "the mistake", "tone": "red", "lines": ["Paying for tools", "before revenue"], "bullets": ["A CRM with no leads", "An analytics suite with no traffic", "Automations for work you do once a month"], "strike": True},
   {"type": "text", "eyebrow": "the rule", "tone": "green", "lines": ["Upgrade only", "when…"], "bullets": ["A limit blocks revenue", "A missing feature costs you 1h+ a week", "A customer needs the paid feature"]},
   cta_slide(["What are you", "overpaying"], "for?")]},
 "captions": {
   "tiktok": f"Paying for tools before you have revenue. Here's the rule for when to upgrade. Free stack audit in bio. {TAGS}",
   "instagram": f"The most expensive founder mistake: paying for tools before revenue.\n\nUpgrade only when a limit blocks revenue, a missing feature costs you an hour a week, or a customer needs it.\n\nFree 2-min stack audit: link in bio.\n\n{TAGS}"},
 "x_post": "Every subscription before revenue is a bet on a company that doesn't exist yet.\n\nUpgrade when:\n- a limit blocks revenue\n- a missing feature costs you 1h+ a week\n- a customer needs it\n\nOtherwise, free plan."}))

DAYS.append(("2026-11-29", {
 "format": "Stack audit promo",
 "video": {"scenes": [
   {"type": "hook", "lines": ["What's missing", "from your"], "sel": "stack?", "sub": "find out in 2 minutes ↓", "dur": 3.4},
   {"type": "steps", "tag": "HOW IT WORKS", "tone": "blue", "title": "8 questions", "steps": ["What you build, your stage, your team", "Region, budget, biggest pain", "How much you use AI today", "What you already have"], "dur": 7.5},
   {"type": "list", "tag": "EXAMPLE RESULT · SAAS", "title": "Your gaps, ranked", "items": [
     {"name": "PostHog", "meta": "analytics", "badge": "now", "tone": "red"}, {"name": "Loops", "meta": "product email", "badge": "next", "tone": "amber"},
     {"name": "Cursor + Claude", "meta": "AI workflow", "badge": "✦ AI", "tone": "solid"}], "dur": 7.5},
   cta_scene(["Run yours.", "It's"], "free.")]},
 "carousel": {"slides": [
   {"type": "cover", "lines": ["What's missing", "from your"], "sel": "stack?", "sub": "A free 2-minute audit tells you."},
   {"type": "steps", "eyebrow": "how it works", "lines": ["8 questions,", "2 minutes"], "steps": ["What you build, your stage, your team", "Region, budget, biggest pain", "How much you use AI today", "What you already have"]},
   {"type": "list", "eyebrow": "example result", "lines": ["Your gaps,", "ranked"], "items": [
     {"name": "Set up now", "meta": "the tools you're missing today", "badge": "now", "tone": "red"},
     {"name": "Next 30 days", "meta": "what to add next", "badge": "next", "tone": "amber"},
     {"name": "3 AI workflows", "meta": "matched to how you work", "badge": "✦ AI", "tone": "solid"}]},
   cta_slide(["Run yours.", "It's"], "free.", "Link in bio.")]},
 "captions": {
   "tiktok": f"8 questions, 2 minutes: find what's missing from your stack, plus 3 AI workflows. Link in bio. {TAGS}",
   "instagram": f"What's missing from your stack?\n\n8 questions → your gaps ranked (now / next / later) + 3 AI workflows matched to you.\n\nFree. Link in bio.\n\n{TAGS}"},
 "x_post": "Built a free stack audit for founders.\n\n8 questions → your missing tools ranked (now / next / later) + 3 AI workflows matched to how you work.\n\nTakes 2 minutes."}))

# ---------- Week 2 ----------
DAYS.append(("2026-11-30", {
 "format": "AI workflow",
 "video": {"scenes": [
   {"type": "hook", "lines": ["Stop rewriting", "the same"], "sel": "emails.", "sub": "a 20-minute AI setup ↓", "dur": 3.4},
   {"type": "steps", "tag": "✦ AI WORKFLOW", "title": "Answer templates", "ai": True, "steps": ["List your 10 most common questions", "Copy 2 emails that sound like you", "Ask Claude for replies in your voice", "Save them in Notion, reuse daily"], "dur": 8.5},
   {"type": "prompt", "tag": "THE PROMPT", "title": "Copy this", "text": "Here are 10 questions my customers ask and 2 emails I wrote. For each question, write a reply in my voice, under 120 words, with [brackets] for details.", "dur": 7},
   cta_scene(["Which AI workflows", "fit your"], "stack?", "Follow for one AI workflow every week.")]},
 "carousel": {"slides": [
   {"type": "cover", "lines": ["Stop rewriting", "the same"], "sel": "emails.", "sub": "A 20-minute AI workflow."},
   {"type": "steps", "eyebrow": "✦ ai workflow", "tone": "solid", "lines": ["Answer templates", "in your voice"], "ai": True, "steps": ["List your 10 most common questions", "Copy 2 emails that sound like you", "Ask Claude for replies in your voice", "Save them in Notion, reuse daily"]},
   {"type": "prompt", "eyebrow": "the prompt", "lines": ["Copy", "this"], "text": "Here are 10 questions my customers often ask, and two emails I wrote so you can learn my tone.\n\nFor each question, write a reply in my voice: under 120 words, friendly and direct, with [brackets] where I add details.\n\nQUESTIONS: [paste]\nMY EMAILS: [paste]"},
   cta_slide(["Which AI workflows", "fit your"], "stack?")]},
 "captions": {
   "tiktok": f"Write your most common email replies once, in your own voice, with this prompt. Free stack audit in bio. {TAGS} #productivity",
   "instagram": f"Answer templates in your voice ✦\n\n1. List your 10 most common questions\n2. Copy 2 emails that sound like you\n3. Paste both into Claude with the prompt (slide 3)\n4. Save in Notion, reuse daily\n\nSave this. Free 2-min stack audit: link in bio.\n\n{TAGS}"},
 "x_post": "You answer the same 10 emails every week.\n\nGive Claude those 10 questions + 2 emails you wrote. Ask for replies in your voice, under 120 words, with [brackets] for details.\n\nSave them. Copy, fill, send.",
 "x_thread": ["You answer the same 10 emails every week. Here's the 20-minute fix:", "1. Search your sent mail. List the 10 questions you answer most.", "2. Copy two emails you wrote that sound like you.", "3. Paste both into Claude: \"For each question, write a reply in my voice, under 120 words, with [brackets] for details.\"", "4. Save the replies in a Notion page. Next time: copy, fill the brackets, send.", "Want 2 more workflows matched to your stack? Free 2-min audit, link in bio."]}))

DAYS.append(("2026-12-01", {
 "format": "Add / Cut",
 "video": {"scenes": [
   {"type": "hook", "lines": ["Stop the", "email"], "sel": "ping-pong.", "sub": "one tool fixes it ↓", "dur": 3.2},
   {"type": "card", "tag": "CUT", "tone": "red", "strike": True, "title": "\"When works for you?\"", "body": "Five emails to book one call.<br><b>Every single time.</b>", "dur": 6},
   {"type": "card", "tag": "ADD", "tone": "blue", "title": "Cal.com", "body": "One booking link with your real availability.<br><b>They pick a slot. Done.</b>", "dur": 6.5},
   cta_scene(["What else", "should you"], "cut?")]},
 "carousel": {"slides": [
   {"type": "cover", "lines": ["Stop the email"], "sel": "ping-pong.", "sub": "One tool to cut, one to add."},
   {"type": "text", "eyebrow": "cut", "tone": "red", "lines": ["\"When works", "for you?\""], "bullets": ["5 emails to book one call", "Time zones get mixed up", "Leads go cold while you wait"]},
   {"type": "text", "eyebrow": "add", "tone": "blue", "lines": ["One booking", "link"], "bullets": ["Cal.com or Calendly", "Shows your real availability", "Put it on your site, email signature and bio"]},
   cta_slide(["What else", "should you"], "cut?")]},
 "captions": {
   "tiktok": f"Five emails to book one call? Cut it. One booking link instead. Free stack audit in bio. {TAGS}",
   "instagram": f"CUT: the 5-email dance to book a call.\nADD: one booking link (Cal.com or Calendly) on your site, signature and bio.\n\nFree 2-min stack audit: link in bio.\n\n{TAGS}"},
 "x_post": "Cut: \"when works for you?\" (5 emails to book one call).\n\nAdd: one booking link with your real availability. On your site, your email signature and your bio."}))

DAYS.append(("2026-12-02", {
 "format": "Tool vs tool",
 "video": {"scenes": [
   {"type": "hook", "lines": ["Zapier, Make", "or n8n?"], "sel": "pick one.", "dur": 3.4},
   {"type": "list", "tag": "AUTOMATION", "title": "One job, three tools", "items": [
     {"name": "Zapier", "meta": "widest app coverage, easiest"}, {"name": "Make", "meta": "visual, multi-step, cheaper per run"},
     {"name": "n8n", "meta": "open source, self-host, AI agents", "badge": "✦ AI", "tone": "solid"}], "dur": 8},
   {"type": "card", "tag": "PICK", "tone": "green", "title": "Not technical? Zapier.", "body": "Complex flows on a budget: Make.<br><b>Technical and want control: n8n.</b>", "dur": 6.5},
   cta_scene(["Which tools", "fit your"], "stack?")]},
 "carousel": {"slides": [
   {"type": "cover", "lines": ["Zapier, Make", "or n8n?"], "sel": "Pick one.", "sub": "One job, three tools, how to choose."},
   {"type": "list", "eyebrow": "the options", "lines": ["Three ways to", "automate"], "items": [
     {"name": "Zapier", "meta": "widest app coverage, easiest to start"}, {"name": "Make", "meta": "visual builder, complex flows"},
     {"name": "n8n", "meta": "open source, self-hostable, AI agent nodes", "badge": "✦ AI", "tone": "solid"}]},
   {"type": "text", "eyebrow": "how to pick", "tone": "green", "lines": ["Pick by who", "you are"], "bullets": ["Not technical, want it working today → Zapier", "Multi-step flows, watching costs → Make", "Technical, want full control → n8n"]},
   cta_slide(["Which tools", "fit your"], "stack?")]},
 "captions": {
   "tiktok": f"Zapier vs Make vs n8n: pick by who you are, not by features. Free stack audit in bio. {TAGS} #automation #nocode",
   "instagram": f"Zapier, Make or n8n?\n\nNot technical → Zapier\nComplex flows on a budget → Make\nTechnical, want control → n8n\n\nSave this. Free 2-min stack audit: link in bio.\n\n{TAGS}"},
 "x_post": "Zapier vs Make vs n8n, the short version:\n\nNot technical, want it working today → Zapier\nMulti-step flows, watching costs → Make\nTechnical, want control and self-hosting → n8n",
 "x_thread": ["Zapier, Make or n8n? Pick by who you are, not by feature lists:", "Zapier: the widest app coverage and the easiest start. Best if you're not technical.", "Make: a visual builder for multi-step flows. Good when flows get complex and you watch costs.", "n8n: open source, self-hostable, with AI agent nodes. Best if you're technical and want control.", "Start with one workflow that saves you an hour a week. Then decide.", "Free 2-min stack audit tells you which one fits. Link in bio."]}))

DAYS.append(("2026-12-03", {
 "format": "Stack for a niche",
 "video": {"scenes": [
   {"type": "hook", "lines": ["The e-commerce", "brand"], "sel": "stack.", "sub": "6 tools, one job each ↓", "dur": 3.4},
   {"type": "list", "tag": "E-COMMERCE", "title": "Everything you need", "items": [
     {"name": "Shopify", "meta": "store + checkout"}, {"name": "Klaviyo", "meta": "email and SMS flows"}, {"name": "Gorgias", "meta": "support with order data"},
     {"name": "Canva", "meta": "ads and product visuals"}, {"name": "Google Analytics", "meta": "traffic and ads"}, {"name": "Claude", "meta": "product pages, ad angles", "badge": "✦ AI"}], "dur": 9},
   {"type": "card", "tag": "FIRST FLOW", "tone": "green", "title": "Abandoned cart email", "body": "Set it up before anything else.<br><b>It's the email that pays for the rest.</b>", "dur": 5.5},
   cta_scene(["What's missing", "from your"], "stack?")]},
 "carousel": {"slides": [
   {"type": "cover", "lines": ["The e-commerce", "brand"], "sel": "stack.", "sub": "Six tools, one job each. Save it."},
   {"type": "list", "eyebrow": "the stack", "lines": ["Everything you", "need"], "items": [
     {"name": "Shopify", "meta": "store, checkout, payments"}, {"name": "Klaviyo", "meta": "email and SMS flows"}, {"name": "Gorgias", "meta": "support with order data"},
     {"name": "Canva", "meta": "ads and product visuals"}, {"name": "Claude", "meta": "product pages, ad angles", "badge": "✦ AI"}]},
   {"type": "text", "eyebrow": "first flow", "tone": "green", "lines": ["Set this up", "first"], "bullets": ["Abandoned cart email", "Welcome series for new subscribers", "Post-purchase thank you + review ask"]},
   cta_slide(["What's missing", "from your"], "stack?")]},
 "captions": {
   "tiktok": f"The e-commerce brand stack, and the first email flow to set up. Free stack audit in bio. {TAGS} #ecommerce #shopify",
   "instagram": f"The e-commerce stack ✦\n\nShopify · Klaviyo · Gorgias · Canva · Google Analytics · Claude\n\nFirst flow to build: abandoned cart.\n\nSave this. Free 2-min stack audit: link in bio.\n\n{TAGS}"},
 "x_post": "The e-commerce brand stack:\n\nShopify (store)\nKlaviyo (email/SMS)\nGorgias (support)\nCanva (visuals)\nGoogle Analytics (traffic)\nClaude (product pages, ad angles)\n\nFirst flow: abandoned cart."}))

DAYS.append(("2026-12-04", {
 "format": "Tool in 30 seconds",
 "video": {"scenes": [
   {"type": "hook", "lines": ["Market research", "in an"], "sel": "hour.", "dur": 3.2},
   {"type": "card", "tag": "✦ AI TOOL", "tone": "solid", "title": "Perplexity", "body": "An AI search engine that answers<br><b>with the sources it used.</b>", "dur": 6},
   {"type": "steps", "tag": "HOW TO USE IT", "tone": "blue", "title": "Competitor research", "steps": ["Ask who the top 5 competitors are", "Ask for their pricing pages", "Open the sources, check them", "Have Claude write a 1-page summary"], "dur": 8},
   cta_scene(["Which AI tools", "fit your"], "stack?", "Follow for one AI tool every week.")]},
 "carousel": {"slides": [
   {"type": "cover", "lines": ["Market research", "in an"], "sel": "hour.", "sub": "Perplexity, in 30 seconds."},
   {"type": "text", "eyebrow": "✦ ai tool", "tone": "solid", "lines": ["What Perplexity", "does"], "bullets": ["Searches the web and answers", "Shows the sources it used", "Good for competitors, pricing, markets"]},
   {"type": "steps", "eyebrow": "how to use it", "lines": ["Competitor research", "in 4 steps"], "steps": ["Ask who the top 5 competitors are", "Ask for their pricing pages", "Open the sources and check them", "Have Claude write a 1-page summary"]},
   cta_slide(["Which AI tools", "fit your"], "stack?")]},
 "captions": {
   "tiktok": f"Competitor research in an hour with Perplexity, then a 1-page summary with Claude. Free stack audit in bio. {TAGS}",
   "instagram": f"Perplexity in 30 seconds ✦\n\nAsk → check the sources → summarize with Claude.\n\nAlways open the sources before you trust an answer.\n\nFree 2-min stack audit: link in bio.\n\n{TAGS}"},
 "x_post": "Competitor research in an hour:\n\n1. Ask Perplexity for the top 5 competitors\n2. Ask for their pricing pages\n3. Open every source, check it\n4. Have Claude turn it into a 1-page positioning doc"}))

DAYS.append(("2026-12-05", {
 "format": "Founder mistake",
 "video": {"scenes": [
   {"type": "hook", "lines": ["Your personal", "account is not", "a business"], "sel": "account.", "dur": 3.6},
   {"type": "card", "tag": "MISTAKE", "tone": "red", "title": "Mixing the money", "body": "Client payments and groceries in one account.<br><b>Your accountant will hate it.</b>", "dur": 6},
   {"type": "card", "tag": "FIX", "tone": "green", "title": "Open a business account", "body": "Do it before your first invoice.<br><b>Qonto in the EU, Mercury in the US.</b>", "dur": 6.5},
   cta_scene(["What's missing", "from your"], "stack?")]},
 "carousel": {"slides": [
   {"type": "cover", "lines": ["Your personal account", "is not a business"], "sel": "account.", "sub": "A week-one mistake that costs you at tax time."},
   {"type": "text", "eyebrow": "the mistake", "tone": "red", "lines": ["Mixing business", "and personal"], "bullets": ["Hard to see what the business earns", "Painful bookkeeping at year end", "Higher accountant fees"]},
   {"type": "text", "eyebrow": "the fix", "tone": "green", "lines": ["Open it", "before invoice #1"], "bullets": ["Qonto for French and EU companies", "Mercury for US companies", "Wise if you get paid in many currencies"]},
   cta_slide(["What's missing", "from your"], "stack?")]},
 "captions": {
   "tiktok": f"Mixing business and personal money is a week-one mistake. Here's the fix. Free stack audit in bio. {TAGS}",
   "instagram": f"Your personal account is not a business account.\n\nOpen one before your first invoice: Qonto (EU), Mercury (US), Wise (many currencies).\n\nFree 2-min stack audit: link in bio.\n\n{TAGS}"},
 "x_post": "Week-one founder mistake: client payments landing in your personal account.\n\nOpen a business account before invoice #1. Your bookkeeping (and your accountant) will thank you."}))

DAYS.append(("2026-12-06", {
 "format": "Stack audit promo",
 "video": {"scenes": [
   {"type": "hook", "lines": ["Freelancer?", "Here's your"], "sel": "stack.", "sub": "from our free audit ↓", "dur": 3.4},
   {"type": "list", "tag": "EXAMPLE RESULT · FREELANCE", "title": "Your gaps, ranked", "items": [
     {"name": "Webflow", "meta": "portfolio site", "badge": "now", "tone": "red"}, {"name": "Cal.com", "meta": "booking link", "badge": "now", "tone": "red"},
     {"name": "Attio", "meta": "client pipeline", "badge": "next", "tone": "amber"}, {"name": "Fathom + Notion", "meta": "call notes workflow", "badge": "✦ AI", "tone": "solid"}], "dur": 9},
   {"type": "card", "tag": "HOW", "tone": "blue", "title": "8 questions, 2 minutes", "body": "Your business, stage, budget and AI use.<br><b>Picks tuned to you.</b>", "dur": 5.5},
   cta_scene(["Run yours.", "It's"], "free.")]},
 "carousel": {"slides": [
   {"type": "cover", "lines": ["Freelancer?", "Here's your"], "sel": "stack.", "sub": "An example result from our free audit."},
   {"type": "list", "eyebrow": "example result", "lines": ["Your gaps,", "ranked"], "items": [
     {"name": "Webflow", "meta": "portfolio site", "badge": "now", "tone": "red"}, {"name": "Cal.com", "meta": "booking link", "badge": "now", "tone": "red"},
     {"name": "Attio", "meta": "client pipeline", "badge": "next", "tone": "amber"}, {"name": "Fathom + Notion", "meta": "call notes workflow", "badge": "✦ AI", "tone": "solid"}]},
   {"type": "steps", "eyebrow": "how it works", "lines": ["8 questions,", "2 minutes"], "steps": ["What you build and your stage", "Region, budget, biggest pain", "How much you use AI", "What you already have"]},
   cta_slide(["Run yours.", "It's"], "free.", "Link in bio.")]},
 "captions": {
   "tiktok": f"Example freelance result from our free stack audit. Run yours in 2 minutes, link in bio. {TAGS} #freelance",
   "instagram": f"Freelancer? Example result from our free stack audit:\n\nNOW: portfolio site + booking link\nNEXT: client pipeline\n✦ AI: call notes workflow\n\nRun yours in 2 minutes: link in bio.\n\n{TAGS}"},
 "x_post": "Example result from our free stack audit (freelancer, making revenue, wants more clients):\n\nNow: portfolio site, booking link\nNext: client pipeline\nAI workflow: call notes → tasks\n\n8 questions, 2 minutes."}))

for date, c in DAYS:
    c["date"] = date
    (OUT / f"{date}.json").write_text(json.dumps(c, ensure_ascii=False, indent=1))
print(len(DAYS), "days written")
