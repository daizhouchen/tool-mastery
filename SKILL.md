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

### Writing guidance that matters more than the schema

**`whatItIs`** — 2–4 sentences. First sentence: what the tool is. Second: who it's for. Third (optional): why they pick it over the obvious alternative. Avoid adjectives like "powerful", "seamless", "intuitive" — they say nothing.

**`coreCapabilities`** — 3 to 5. Each title is a *noun* (the primitive), not a verb ("Issues & cycles" not "Track issues"). Each desc is *one* sentence that names the primitive and what it does. If you have 8 capabilities you want to mention, collapse them — the reader cannot hold 8 things in their head.

**`quickStart`** — the minimum steps to make the tool do something real. Not sign-up alone — that's useless. End on a step where the tool has produced value ("Create your first issue", "Run your first command"). Use `code` for copy-pasteable commands; omit `code` for click-through UI steps.

**`scenarios`** — 2 to 3, and this is the highest-leverage section. A scenario is a *named workflow* a real user does. Each one has:
- a concrete `title` ("Run weekly triage", not "Using the triage view")
- a one-line `goal` that explains why someone would do this
- ordered `steps` at a "what I click / type" granularity

If you find yourself writing a scenario called "Using Feature X", delete it and think about what someone would actually use Feature X *for*.

**`pitfalls`** — 2 to 4. The test: would a new user only learn this by getting burned? If it's in the marketing copy, it's not a pitfall. Examples of real pitfalls: undocumented rate limits, "free tier doesn't include X", "this action is irreversible", "requires scope Y which admins must approve".

### Combos

Only emit a `combos` entry when the user asked about two or more tools *working together*. A combo section is not "here are three tools side by side" — it is a *joint workflow* that only makes sense when the tools are wired up.

**`overview`** — why you'd wire these together. The reader should finish reading it thinking "ah, that's the point". If you can't articulate a joint outcome, the combo probably shouldn't be in the doc.

**`ascii`** (optional but high-value) — a plain-text diagram of data flow between the tools. Keep it short (≤10 lines). Use `──►` arrows, alignment, and one or two labeled branches. It will render in a monospace block. Example:

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

**After rendering**, open the file or at least print the absolute path clearly. The user's next move is to open it in a browser and read it.

### If render.py fails

Most failures are malformed JSON. Read the error, fix the JSON, rerun. Do not attempt to inline-render HTML as a workaround — the point of the template is visual consistency, and a hand-rolled fallback will look different from the rest.

---

## Output quality bar

Before declaring done, skim the rendered page and check:

- **Hero** answers "what will I learn here" in one line.
- **Each tool** has a scenario I can imagine myself doing tomorrow.
- **Each combo** ends with a concrete outcome, not vibes.
- **No marketing filler.** Search the output for "powerful", "seamless", "intuitive", "leverage", "unleash" — if you find them, rewrite.
- **Every command is copy-pasteable.** No placeholders like `<your-api-key>` without a comment explaining what it is.
- **The page fits on one screen of reading at the hero + ~3 scrolls of content per tool.** If it's longer than that, trim.

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
