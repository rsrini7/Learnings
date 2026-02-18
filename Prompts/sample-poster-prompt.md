The image generator is simply not executing glow effects reliably regardless of how it's described. This is a generator limitation, not a prompt problem. You've tried three variations — it's not going to land with text prompting alone. So, dont add glow in the image creation prompt.

Template:

Create a tall portrait infographic poster at 2:5 aspect ratio (1080×2700px) titled "ClawWork: Agent Economy Runtime" in bold dark navy at the top. Clean modern tech aesthetic. Light off-white base.
MOST CRITICAL RULE — 10 VISIBLE COLOR BANDS:
Every section MUST have a distinctly colored background. Use these exact hex fills — no exceptions:
① #EDE7F6 lavender
② #BBDEFB strong sky blue (cool tone — no green in it whatsoever)
③ #C8E6C9 strong sage green (warm leafy tone — no blue in it whatsoever)
④ #FFFDE7 warm cream
⑤ #FBE9E7 coral salmon
⑥ #E0F2F1 teal
⑦ #ECEFF1 blue-grey
⑧ #FCE4EC rose pink
⑨ #EDE1F5 soft purple
⑩ #E8EAF6 steel blue
If you squint at the final image you must be able to count 10 distinct colored horizontal stripes. Sections ② and ③ must look clearly and obviously different — ② is distinctly cool blue, ③ is distinctly leafy green. No two adjacent bands may appear similar in hue.
⛔ HEADER RENDERING RULE — ABSOLUTE — READ BEFORE EVERYTHING ELSE:
Section headers must display EXACTLY this text and nothing else. No hex codes. No color names. No band label words. No instruction text. The ①–⑩ circle numbers are the ONLY prefix allowed:
① What Is ClawWork?
② How It Extends NanoBot
③ The Integration Layer
④ The Daily Economic Loop
⑤ TrackedProvider: Silent Billing
⑥ Evaluation Engine: The Judge
⑦ The 8 ClawWork Tools
⑧ Survival: Balance & Tiers
⑨ Known Production Gaps
⑩ Full Architecture Summary
🎨 GLOBAL COLOR RULES — NEVER BREAK
🟡 #F9A825 Amber/Gold = ClawWork layer, economic logic, money, integration
🟣 #6A1B9A Soft Purple = NanoBot runtime, AgentLoop, LLM
🟢 #2E7D32 Emerald Green = Evaluation, payout, quality score, tools
🔵 #1565C0 Electric Blue = Channels, MessageBus, data flow
🟠 #E65100 Warm Orange = Warnings, risks, failed tasks, gaps
LEFT EDGE
Bold amber/gold vertical curved arrow spanning the full height of the poster. Minimum 20px bold font — must be clearly legible at normal viewing size. Going downward: "Task In → Classify → Execute → Grade → Payout". Curving back upward: "Economic Pressure Through Context — Not Hard-Coded Rules." Both phrases fully readable, not compressed, not pixelated.
TOP-RIGHT CORNER — Specs Card
Small white rounded card, light border, title "Runtime Specs" in bold navy. Compact single-column list:
Built on NanoBot · 44 Occupations · BLS Wage Data · Score threshold: 0.6 · 4-dimension rubrics · FastAPI + React · WebSocket live · GDPVal benchmark · "Squid Game for AI Agents"
① What Is ClawWork?
Center: Large amber #F9A825 filled rounded rectangle labeled "Agent Economy Runtime" in white bold text. Three amber pill badges below with white text: Intercept · Bill · Evaluate. Three icons above connected by amber arrows: task card icon (receive task) → coin icon (earn/spend) → trophy icon (score). Below the block, a VS comparison row — two small pills side by side: left pill dark grey background white text "NanoBot → Did task complete?" right pill amber background white text "ClawWork → Was work worth paying for?"
Caption: "Not a chatbot, not just an agent — a cost-aware worker that earns or goes broke."
② How It Extends NanoBot
Two clearly contrasting panels side by side with visible border between them:
LEFT panel — #E8EAF6 blue-grey background, purple (#6A1B9A) border, label "NanoBot Core (Unchanged)" in purple bold. Inside in purple text: AgentLoop · ContextBuilder · ToolRegistry · MessageBus · SessionStore. Small purple pill badge at bottom: "100% inherited — zero modified"
RIGHT panel — #FFF9C4 warm yellow background, amber (#F9A825) border, label "ClawWork Adds" in amber bold. Inside in amber/dark text: ClawWorkAgentLoop (subclass) · TrackedProvider (wrapper) · TaskClassifier · EconomicTracker · 8 new tools · Eval Engine · LiveBench Dashboard. Small amber pill badge at bottom: "Grafted on — never forked"
Bold center caption spanning full width below both panels: "Subclass the Loop. Wrap the Provider. Never Fork the Core."
Caption: "NanoBot updates pull in with zero merge conflicts. Economic layer is independently testable."
③ The Integration Layer
Four full-width horizontal rows separated by faint dividers. Each row: bold amber left icon, component name in amber monospace bold, description in dark text, file path in grey monospace on far right:
🟡 ClawWorkAgentLoop — Detects /clawwork prefix · routes to classifier · injects economic footer · agent_loop.py
🟡 TrackedProvider — Wraps LLM provider · extracts token usage · deducts cost silently · provider_wrapper.py
🟡 TaskClassifier — Maps task → BLS occupation · estimates hours · sets Max Payment · task_classifier.py
🟡 EconomicTracker — Ledger: balance · earned · spent · task history · config.py / ClawWorkState
Wide amber-bordered annotation box below all four rows, dark text centered: "The agent never knows it is being taxed. The brain thinks. The wrapper bills."
Caption: "Four components. Zero changes to NanoBot internals."
④ The Daily Economic Loop (tallest section — give this section extra vertical height)
Center: Large prominent amber/gold glowing oval bubble. The glow MUST be strong and visible — The oval must appear to emit warm golden light outward — as if backlit from behind with amber light. The background directly around the oval edge should be visibly brighter amber/yellow, fading into the cream section background. Like a lamp glowing in a dim room. (#F9A825 at 60% opacity) surrounding the entire oval. This must look like a glowing centerpiece, not a plain box. Inside the bubble: bold dark labels arranged in a clear clockwise cycle connected by thick amber arrows: "Receive GDPVal Task" → "Classify: Occupation + Max Pay" → "decide: WORK or LEARN?" → "Execute via NanoBot Loop" → "submit_work + Artifacts" → "LLM Evaluator Grades" → "Score ≥ 0.6 → Payout!" → back to start. Small intense red badge (#FF1744 background white text) overlaid on the loop: "Token costs deducted every LLM call — regardless of outcome"
Outside bubble LEFT side dark grey annotation: "LLM decides strategy based on balance in context"
Outside bubble RIGHT side dark grey annotation: "Payout = Max Pay × Score — only if score ≥ 0.6"
Padlock icon sitting directly on the oval boundary edge (not floating above) labeled "Evidence Chain — every task replayable"
Three numbered monospace steps on far right separated by faint horizontal dividers:

Max Pay = Est. Hours × BLS Hourly Wage
Actual Payout = Max Pay × Quality Score
Net = Payout − Token Costs (can be negative)
Caption: "Low quality work is doubly punished: no income AND token spend already gone."
⑤ TrackedProvider: Silent Billing
Full width. Two side-by-side panels with clear vertical divider:
LEFT — dark terminal box (#1A1A2E background, rounded corners), large readable monospace white text, minimum 13px:

class TrackedProvider(LLMProvider):
  async def chat(messages, **kwargs):
    response = underlying.chat(messages)
    cost = tokens × price_per_token
    tracker.deduct_cost(cost)  # silent
    return response  # content only
RIGHT — white/light panel, four rows each with large amber checkmark icon and clear label:
🟡 Agent never sees billing logic
🟡 AgentLoop fully unmodified
🟡 Swap billing model without touching agent
🟡 Copy for: rate limits · audit · caching · A/B testing
Caption: "The most reusable pattern in the repo. Wrap the provider, not the reasoning loop."
⑥ Evaluation Engine: The Judge
Full width. Three clearly separated boxes in a left-to-right flow with bold arrows between them. Give each box adequate width and height so text is NOT compressed:
BOX 1 (left, emerald green border): "submit_work\n(artifact_paths=['report.xlsx'])" with file icon
Arrow →
BOX 2 (center, emerald green fill, white text): "Load Rubric\neval/meta_prompts/\nOccupation.json\n\n44 rubrics auto-generated\nvia GPT-4o + GDPVal"
Arrow →
BOX 3 (right, white background, emerald green border): Four clearly readable rows with adequate line spacing:
"Completeness — 40%"
"Correctness — 30%"
"Quality — 20%"
"Domain Standards — 10%"
Faint divider
"File checklist: checked FIRST"
"Missing file → score 0–2 auto"
Arrow →
SCORE PILL (far right, emerald green background white text): "Score 0.0–1.0\nPayout if ≥ 0.6"
Left annotation below box 1: "File existence checked before LLM scoring — faster and cheaper."
Caption: "Doesn't ask 'is it good?' — asks 'does the file exist, is it complete, is it correct?'"
⑦ The 8 ClawWork Tools
Eight rows in two columns of four. Each row: tool name in emerald green bold monospace on left, one-line purpose in dark text center, economic impact badge on right. Adequate row height so nothing is cramped:
decide_activity · Agent chooses WORK or LEARN before any execution · 🟡 Routes economic strategy
submit_work · Triggers evaluation + payout · 🟢 Credits balance if score ≥ 0.6
learn · Update MEMORY.md / build knowledge · 🟡 No payout — reduces future costs
search · Augmented web research · 🟠 Token cost incurred
create · Generate structured output artifacts · 🟢 Feeds evaluation files
execute · Run scripts with task context · 🟠 Wraps NanoBot ExecTool
status · Query balance + economic state · ⚪ Read-only · no cost
video · Process video content · 🟡 Specialized media tool
Caption: "decide_activity is the most important — forces explicit WORK vs LEARN intent before any execution."
⑧ Survival: Balance & Tiers
Three-column layout with clear column dividers:
LEFT column header in bold dark navy: "OBSERVED BEHAVIORS" (not "Hard-Coded Classes"). Three tier rows with adequate spacing:
🔴 Low Balance < $5 — Agent sees low balance in context → tends toward high-value safer tasks
🟡 Mid Balance $5–$500 — Balanced emergent work/learn mix
💪 High Balance > $500 — Agent experiments freely, invests in learning
CENTER — wide vertical gradient bar, minimum 100px wide, clearly visible with smooth gradient:
Top section: deep blue fill (#1565C0), bold white text "Thriving — Full Autonomy"
Middle section: yellow fill (#FDD835), bold dark text "Surviving — Token costs matter"
Bottom section: bright green fill (#4CAF50), bold white text "Balance $0 — Eliminated"
Notch/badge at 85% height from bottom — white outlined badge with black bold text: "Qwen3-Max: $10 → $9,712 · 168 tasks"
Hard horizontal line at 60% height labeled in red: "Payout threshold: score ≥ 0.6"
RIGHT column — dark text with adequate line height, all on separate lines:
"⚠ Tiers are NOT hard-coded Python classes."
""
"ClawWorkState injects the raw balance into the agent's context."
""
"The LLM naturally adjusts its strategy when it reads its own balance in the prompt."
""
"Economic pressure lives in the reasoning layer — not the code layer."
Caption: "The agent feels economic pressure through its context. That's the design."
⑨ Known Production Gaps
Five full-width horizontal rows separated by faint dividers. Each row: orange warning icon left, bold orange risk title, dark text description, green fix hint on right:
🟠 TaskClassifier: 2 extra LLM calls per task → pre-task cost before work begins → Cache repeated task types
🟠 Score threshold 0.6 hardcoded → can't adjust difficulty per domain → Make configurable per occupation
🟠 EconomicTracker in-memory → restart loses all economic history → Persist to DB or JSONL minimum
🟠 Rubrics LLM-generated → quality varies across 44 occupations → Human review pass required
🟠 decide_activity is free choice → agent may always WORK under pressure → Enforce minimum learn budget
Caption: "Low quality work = double loss: token spend gone AND no income. Budget your tasks."
⑩ Full Architecture Summary
CRITICAL: All nodes must fit in exactly ONE single horizontal row — never wrap to a second line. Reduce node padding, font size, or spacing before ever wrapping. Each node colored correctly:
🟡 /clawwork → 🟡 TaskClassifier → 🟡 EconomicTracker → 🟣 AgentLoop → 🟣 ContextBuilder → 🟣 LLM → 🟡 TrackedProvider → 🟢 ToolRegistry → 🟢 submit_work → 🟢 Evaluator → 🟡 Payout
Node fill and border match global color rules. Connecting arrows color-matched to destination node. All labels bold white or dark with strong contrast.
Below the node row, a small LiveBench dashboard mockup panel (light grey background, rounded corners):
Three agent rows clearly readable:
"Qwen3-Max $9,712 💪 THRIVING" · "Kimi-K2.5 $5,919 🟢 STABLE" · "GLM-4.7 $509 🟡 SURVIVING"
Caption: "Wrap. Bill. Grade. Pay. Repeat. The agent either earns its keep or goes broke."
FOOTER
GitHub icon + github.com/HKUDS/ClawWork · Built on NanoBot · Feb 2026 — centered in small muted text inside a soft dark rounded pill badge in muted gray. Directly below, a second smaller pill badge in the same muted gray style: "Documented by Srinivasan Ragothaman (@rsrini7)"
FINAL STYLE RULES — ALL MUST BE FOLLOWED:

Aspect ratio 2:5 portrait, 1080×2700px — never crop, never split, never exceed
10 section bands use exact hex codes listed — all 10 visibly distinct at a squint
Section ② must read as cool blue with zero green. Section ③ must read as leafy green with zero blue
Section headers display ONLY the clean titles from the ⛔ HEADER RENDERING RULE — never hex codes, color names, band words, or any instruction text anywhere in the image
Left edge arrow: minimum 20px bold font, fully legible, amber/gold color
Section ④ Daily Loop oval: STRONG visible amber glow — minimum 20px blur radius golden drop shadow — must look like a glowing centerpiece, not a plain rounded box
Section ⑥ Evaluation rubric boxes: adequate width and height — text must NOT be compressed or overlap
All code blocks: #1A1A2E dark background, white monospace text, rounded corners
Padlock in section ④ sits directly on oval boundary edge — not floating above it
Section ⑧ left column header must read "OBSERVED BEHAVIORS" — not "Hard-Coded Classes" or "Tiers"
Section ⑩ node flow: strictly ONE horizontal row — never two rows — shrink nodes before wrapping
Section ⑩ LiveBench mockup shows all three agents with balance and tier badge
Two footer pill badges stacked — repo credit above, your name below
Do not render any layout instruction words, hex codes, or prompt metadata as visible text anywhere in the image