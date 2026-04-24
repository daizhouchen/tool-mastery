---
name: tool-mastery
description: Teach the user a new tool — or a combination of tools — by producing a polished, minimal single-file HTML site covering what each tool is, how to actually use it, real scenarios, pitfalls, and (when multiple tools are in scope) how to wire them together end-to-end. Use this whenever the user asks to "explain / introduce / onboard me to / teach me / walk me through" a tool, asks "how do I use X", "how do X and Y work together", "integrate X with Y", or wants a usage guide / handbook / cheat sheet / quick start — even if they don't explicitly say "website". Trigger liberally: if the user names one or more concrete products and wants to understand or adopt them, this skill applies. Skip only when the user is asking about a coding problem inside an already-adopted tool (e.g. "fix my Linear API bug"), not learning the tool itself.
---

# tool-mastery

Produces a single-file HTML site that makes a reader **actually able to use** one or more tools — not a marketing overview and not an exhaustive manual. The site feels like something a senior colleague would write to onboard a new hire.

The key idea: split the work into **three discrete phases**. Each phase has one job. Don't mix them.

```
Phase 1: Intel         Phase 2: Structure      Phase 3: Render
─────────────          ────────────────        ───────────────
Fetch the facts   →    Shape them into a   →  Pipe JSON through
from source            structured JSON         render.py to get
(web, docs, repo)      that matches the        the final HTML
                       data schema
```

Every phase has a deliverable. You can only enter the next phase when the previous one is done — this is what keeps the output tight and prevents you from drifting into a wall-of-text Wikipedia entry.

---

## Phase 1 — Intel gathering

**Goal:** produce a short research note (kept in your scratchpad, not shown to the user) with *factual, sourced* material for every tool in scope and, if relevant, every integration between them.

**Why this matters:** tools evolve fast. Your training data lags. If you skip this step and write from memory, you will invent outdated CLI flags, retired feature names, or integrations that don't exist. That's the single biggest failure mode for this skill.

### For each tool, fetch three things

Use the `WebFetch` tool on the canonical sources, in this order:

1. **Landing page** (e.g. `https://linear.app`) — for the one-line tagline, product category, target user. You're harvesting the *framing*, not features.
2. **Docs home or Getting Started** (e.g. `https://linear.app/docs`) — for core primitives, quickstart steps, and the vocabulary the product uses for itself.
3. **GitHub repo README** if the tool is open source or has a CLI (e.g. `https://github.com/anthropics/claude-code`) — for install commands, flags, and real usage examples.

If the tool has a well-known CLI or SDK, also fetch the CLI reference page. Capture exact commands verbatim — do not paraphrase `npm install -g X` into "install via npm".

### For each combination in scope

If the user asked about two or more tools working together, also fetch:

- The **official integration page** if it exists (e.g. `https://linear.app/integrations/github`). This is where the actual supported wiring lives.
- Any **setup guide** the vendor publishes for that integration.

If the integration genuinely doesn't exist as a first-party offering, say so in the output — do not fabricate a workflow. It's legitimate to describe a *pattern* (webhooks, CLI chaining) as long as you label it as such.

### What to record per tool

For your own use in Phase 2, jot down:

- Exact product name and one-sentence positioning (from the landing page)
- 3–5 primitives the product is built around (from docs — things like "issues", "cycles", "projects" for Linear)
- The install / signup path (exact command or URL)
- 2–3 usage patterns the docs themselves emphasize
- Any footguns the docs call out (rate limits, destructive actions, required scopes)

Skip: exhaustive feature lists, pricing, company history, customer logos.

---

## Phase 2 — Structure

**Goal:** produce a single JSON file matching `references/data-schema.md`, saved to a working path you'll use as `render.py` input. This is where the opinionated craft happens.

Read `references/data-schema.md` before starting — it documents every field and the conventions for each one.

### Writing guidance — grounded in theory, not feature dumps

Four frameworks decide *how* Claude writes, not what new fields to invent. They never appear as visible labels — they shape the sentences.

- **Jobs to be Done (Christensen)** — readers don't buy features; they hire a tool to finish a job. `whatItIs` opens with the job.
- **Mental Models (Craik)** — people only use a tool well once they can picture its internal skeleton (the primitives and the rule for how they combine). The reader should be able to sketch that picture after reading `whatItIs` + `coreCapabilities`.
- **Activity Theory (Vygotsky → Engeström)** — in multi-tool scenarios, each tool *mediates* between a subject (a role) and an object (an outcome), under shared rules. This is what separates a real combo story from three encyclopedia entries side by side.
- **Affordance (Gibson / Norman)** — a pitfall is the tool's *negative space* — what it refuses to let you do gracefully. Not a random "be careful" warning.

Concretely:

**`whatItIs`** — 3 to 5 sentences, in this order:

1. **JTBD sentence.** Open with the job. Shape: *"When you need to <trigger>, you reach for <Tool> to <outcome> — because <decisive reason>."* Do not open with "X is a Y that does Z" marketing copy.
2. **Audience.** Who it's for, in one line.
3. **Mental-model sentence.** Name the 2–3 core primitives and the single rule for how they compose. Example: *"Linear is three primitives — an **Issue** is the atomic unit of work, a **Cycle** is a time-box it lives inside, a **View** is a filter over all of them — and every workflow is a combination of those."* This is what the reader recites back after closing the tab.
4. *(Optional)* Why pick it over the obvious alternative.

Forbidden words — zero information: `powerful`, `seamless`, `intuitive`, `leverage`, `unleash`, `robust`, `cutting-edge`, `revolutionary`.

**`coreCapabilities`** — 3 to 4 items, **hard cap at 4**. More is a feature soup the reader can't hold in their head. Each title is a *noun* (a primitive). Each `desc` is one sentence naming the primitive and what it lets the user do. The four cards should be the four legs of the mental-model picture the reader just read.

**`quickStart`** — 3 to 6 steps. End on a step where the tool produced real value ("Create your first issue", not "Verify your email"). Use `code` for copy-pasteable commands; omit `code` for UI steps. **Default to a single platform** — pick the one most likely to match the user's context. Only stack multi-platform variants (macOS + Linux + Windows) if the user explicitly asked for cross-platform.

**`scenarios`** — 2 to 3 items, the highest-leverage section. A scenario is a *named workflow* a real user does. Each one has:
- a concrete `title` ("Run weekly triage", not "Using the triage view")
- a one-line `goal` explaining why someone would do this
- ordered `steps` at "what I click / type" granularity

If you find yourself writing "Using Feature X", delete it and rewrite it as what someone would use Feature X *for*.

**`pitfalls`** — 2 to 4 items. A real pitfall is the tool's *negative affordance* — a thing it won't let you do gracefully and the reader couldn't guess from marketing. Rate limits, irreversible actions, "requires scope Y which admins must approve", "auto-close only fires on merges to the default branch". "Be careful" is not a pitfall.

**`migratingFrom`** (optional) — fill *only* when the user explicitly says they're coming from a specific tool (e.g. "I've used Jira before"). This leverages Vygotsky's Zone of Proximal Development — new knowledge anchors to what the reader already owns. Structure:

```json
"migratingFrom": {
  "fromTool": "Jira",
  "mapping": [
    { "from": "Epic", "to": "Project", "note": "optional short clarification" },
    { "from": "Sprint", "to": "Cycle" }
  ]
}
```

Renders as a two-column comparison table.

### Combos

Only emit a `combos` entry when the user asked about two or more tools *working together*. A combo section is not "here are three tools side by side" — it is a *joint workflow* that only makes sense when the tools are wired up.

**`overview`** — 2 to 4 sentences, written through the Activity Theory lens. Name four things, in this order:

1. The **subject** (the role doing the work — PM, engineer, oncall).
2. The **object** (the outcome they're chasing — "ship a feature", "close a ticket without status-wrangling").
3. The **mediating tools** (which tool plays which role in reaching the object).
4. The **rules / conventions** that make the hand-off work (branch name contains the ticket ID, magic words close issues, etc.).

If you can't articulate those four, the combo probably shouldn't be in the doc.

**`ascii`** (optional but high-value) — a plain-text diagram of data flow between the tools. Keep it short (≤10 lines). Use `──►` arrows, alignment, and one or two labeled branches. **Keep it ASCII-only — no CJK characters mixed in**: in a monospace font, CJK characters are rendered double-width and will throw the whole diagram out of alignment. If the page is in Chinese, the diagram still uses English/latin labels. Example:

```
Linear issue  ──►  Claude Code branch  ──►  GitHub PR  ──►  Linear auto-close
     │                                           │
     └────── status sync ◄────────── review ─────┘
```

**`workflow`** — 4 to 7 ordered steps, each labeled with which `tools` participate. Think of it as the end-to-end user story: "I have a ticket → … → the ticket closes itself."

**`setup`** — one-time integration steps (install the app, paste the token, pick the repos). Only include if setup is non-trivial.

### Saving the JSON

Save to a working path. A good convention is `/tmp/tool-mastery-<slug>.json`, but adapt to what the user asks for.

---

## Phase 3 — Render

**Goal:** produce the final `index.html` file and tell the user where it is.

The rendering is handled by the bundled script — do not hand-write HTML. The template enforces the visual language (dark, minimal, Linear/Vercel-inspired) so the output is consistent across every invocation of this skill.

Run the script. The script path is relative to this SKILL.md at `scripts/render.py`.

```bash
python /path/to/tool-mastery/scripts/render.py <data.json> --output <output.html>
```

If the user specified an output directory, use it. Otherwise default to the current working directory and name it after the topic (`linear-github-claude.html`, `linear.html`).

**After rendering**, print the absolute path clearly. Also add a one-line reminder to the user: *"If you previously opened this file, hard refresh (Cmd/Ctrl+Shift+R) to defeat browser cache."* — otherwise font/style upgrades will silently fail to appear.

### If render.py fails

Most failures are malformed JSON. Read the error, fix the JSON, rerun. Do not attempt to inline-render HTML as a workaround — the point of the template is visual consistency, and a hand-rolled fallback will look different from the rest.

---

## Output quality bar

Before declaring done, do **two** passes.

### Pass 1 — surface checks (grep-able)

- **No marketing filler.** Search the output for `powerful`, `seamless`, `intuitive`, `leverage`, `unleash`, `robust`, `cutting-edge`, `revolutionary` — if any appear, rewrite.
- **No unexplained placeholders.** Commands like `<your-api-key>` must come with a comment explaining what to put there.
- **`coreCapabilities` ≤ 4** per tool. If you have 5, merge two.
- **ASCII block is pure ASCII.** Grep the `ascii` field for any CJK (`[一-鿿]`). If found, rewrite the diagram in English/latin only.

### Pass 2 — Feynman checks (the hard ones)

Close your eyes and pretend you're the reader who just finished this page. Honest answers:

1. **Job check.** Can I state each tool's job in one sentence without looking at the page? ("Linear is what I hire to *make the cross-team status of work legible*." If the answer is a feature list, `whatItIs` failed its JTBD duty.)
2. **Mental-model check.** Can I draw each tool's internal skeleton — the 2–3 primitives and the rule binding them — from memory? (If I can only recall scattered features, the mental-model sentence was too weak.)
3. **Combo role check.** For each tool in the combo, can I say one sentence about what role it plays in the joint workflow — without confusing it with the other tools? (If two tools sound interchangeable, the combo `overview` failed its Activity Theory duty.)
4. **Scenario check.** Is there at least one scenario per tool I could actually carry out tomorrow with only what's on this page?
5. **Pitfall check.** Are the pitfalls things I'd only learn by getting burned? (If any sound like generic "be careful" warnings, replace them with concrete negative-affordance facts.)

If any check fails, go back to Phase 2 and rewrite — not Phase 3. Re-rendering doesn't fix shallow content.

---

## When to push back on the user's request

If the user asks for a tool-mastery page about something that isn't a tool (a methodology, a programming language, a concept), say so — this skill is scoped to concrete products/CLIs/services. Offer to do a regular explainer instead.

If the user names 5+ tools, warn them that the output will be long and ask which 2–3 they most need to combine. More is not better here.

---

## Files in this skill

- `SKILL.md` — this file
- `assets/template.html` — the HTML shell with baked-in CSS and layout
- `scripts/render.py` — the JSON → HTML renderer
- `references/data-schema.md` — full schema for the JSON payload (read this in Phase 2)
