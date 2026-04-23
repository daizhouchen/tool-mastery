#!/usr/bin/env python3
"""Render a tool-mastery site from a structured JSON payload.

Usage:
    python render.py <data.json> [--output index.html] [--template assets/template.html]

The JSON schema is documented in references/data-schema.md.
"""
from __future__ import annotations

import argparse
import html as html_lib
import json
import sys
from pathlib import Path


def esc(text) -> str:
    if text is None:
        return ""
    return html_lib.escape(str(text), quote=True)


def render_code_block(code: str, lang: str = "") -> str:
    if not code:
        return ""
    lang_attr = f' class="lang-{esc(lang)}"' if lang else ""
    return f"<pre><code{lang_attr}>{esc(code)}</code></pre>"


def render_capabilities(caps: list[dict]) -> str:
    if not caps:
        return ""
    cards = []
    for c in caps:
        cards.append(
            f'<div class="cap-card">'
            f'<div class="cap-title">{esc(c.get("title", ""))}</div>'
            f'<div class="cap-desc">{esc(c.get("desc", ""))}</div>'
            f"</div>"
        )
    return '<div class="cap-grid">' + "".join(cards) + "</div>"


def render_quickstart(steps: list[dict]) -> str:
    if not steps:
        return ""
    items = []
    for s in steps:
        title = esc(s.get("title", ""))
        desc = esc(s.get("desc", ""))
        code = render_code_block(s.get("code", ""), s.get("lang", ""))
        items.append(
            f"<li>"
            f'<div class="step-title">{title}</div>'
            + (f'<div class="step-desc">{desc}</div>' if desc else "")
            + code
            + f"</li>"
        )
    return '<ol class="steps">' + "".join(items) + "</ol>"


def render_scenarios(scenarios: list[dict]) -> str:
    if not scenarios:
        return ""
    items = []
    for sc in scenarios:
        title = esc(sc.get("title", ""))
        goal = sc.get("goal", "")
        goal_html = (
            f'<div class="scenario-goal"><strong>Goal</strong> · {esc(goal)}</div>'
            if goal
            else ""
        )
        step_items = "".join(f"<li>{esc(x)}</li>" for x in sc.get("steps", []))
        items.append(
            f'<div class="scenario">'
            f'<div class="scenario-title">{title}</div>'
            f"{goal_html}"
            f"<ol>{step_items}</ol>"
            f"</div>"
        )
    return '<div class="scenarios">' + "".join(items) + "</div>"


def render_pitfalls(pitfalls: list[dict]) -> str:
    if not pitfalls:
        return ""
    items = []
    for p in pitfalls:
        label = p.get("label", "Watch out")
        text = p.get("text", "")
        items.append(
            f"<li><strong>{esc(label)}</strong> · {esc(text)}</li>"
        )
    return f'<ul class="pitfalls">{"".join(items)}</ul>'


def render_docs_link(tool: dict) -> str:
    url = tool.get("docsUrl")
    if not url:
        return ""
    label = tool.get("docsLabel") or "Read the official docs"
    return f'<a class="docs-link" href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>'


def render_tool_section(tool: dict) -> str:
    slug = esc(tool.get("slug", ""))
    name = esc(tool.get("name", ""))
    badge = tool.get("badge", "")
    badge_html = f'<span class="badge">{esc(badge)}</span>' if badge else ""
    tagline = esc(tool.get("tagline", ""))
    what = esc(tool.get("whatItIs", ""))

    parts = [
        f'<section class="tool" id="{slug}">',
        f"<h2>{name}{badge_html}</h2>",
        f'<p class="tagline">{tagline}</p>' if tagline else "",
        f'<p class="what">{what}</p>' if what else "",
    ]

    caps_html = render_capabilities(tool.get("coreCapabilities", []))
    if caps_html:
        parts.append("<h3>Core capabilities</h3>")
        parts.append(caps_html)

    qs_html = render_quickstart(tool.get("quickStart", []))
    if qs_html:
        parts.append("<h3>Quick start</h3>")
        parts.append(qs_html)

    sc_html = render_scenarios(tool.get("scenarios", []))
    if sc_html:
        parts.append("<h3>Real scenarios</h3>")
        parts.append(sc_html)

    pf_html = render_pitfalls(tool.get("pitfalls", []))
    if pf_html:
        parts.append("<h3>Pitfalls</h3>")
        parts.append(pf_html)

    docs_html = render_docs_link(tool)
    if docs_html:
        parts.append(docs_html)

    parts.append("</section>")
    return "\n".join(p for p in parts if p)


def render_workflow(steps: list[dict]) -> str:
    if not steps:
        return ""
    rows = []
    for i, s in enumerate(steps, 1):
        tools = s.get("tools", [])
        tools_html = "".join(f"<span>{esc(t)}</span>" for t in tools)
        code = render_code_block(s.get("code", ""), s.get("lang", ""))
        rows.append(
            f'<div class="workflow-step">'
            f'<div class="step-idx">Step {i}'
            f'<div class="tools">{tools_html}</div>'
            f"</div>"
            f'<div class="step-body">'
            f'<div class="wf-title">{esc(s.get("title", ""))}</div>'
            f'<div class="wf-desc">{esc(s.get("desc", ""))}</div>'
            f"{code}"
            f"</div>"
            f"</div>"
        )
    return "".join(rows)


def render_combo_section(combo: dict) -> str:
    slug = esc(combo.get("slug", ""))
    title = esc(combo.get("title", ""))
    tagline = esc(combo.get("tagline", ""))
    overview = esc(combo.get("overview", ""))
    ascii_flow = combo.get("ascii", "")

    parts = [
        f'<section class="combo" id="{slug}">',
        f"<h2>{title}</h2>",
        f'<p class="tagline">{tagline}</p>' if tagline else "",
        f'<p class="what">{overview}</p>' if overview else "",
    ]

    if ascii_flow:
        parts.append("<h3>Flow at a glance</h3>")
        parts.append(f'<div class="combo-flow">{esc(ascii_flow)}</div>')

    wf_html = render_workflow(combo.get("workflow", []))
    if wf_html:
        parts.append("<h3>End-to-end workflow</h3>")
        parts.append(wf_html)

    setup = combo.get("setup", [])
    if setup:
        parts.append("<h3>One-time setup</h3>")
        parts.append(render_quickstart(setup))

    pitfalls_html = render_pitfalls(combo.get("pitfalls", []))
    if pitfalls_html:
        parts.append("<h3>Pitfalls</h3>")
        parts.append(pitfalls_html)

    parts.append("</section>")
    return "\n".join(p for p in parts if p)


def render_toc(tools: list[dict], combos: list[dict]) -> str:
    items = []
    if tools:
        items.append('<li style="margin-top: 12px;"><span class="toc-label" style="font-size:10px;">Tools</span></li>')
        for t in tools:
            items.append(
                f'<li><a href="#{esc(t.get("slug", ""))}">{esc(t.get("name", ""))}</a></li>'
            )
    if combos:
        items.append('<li style="margin-top: 16px;"><span class="toc-label" style="font-size:10px;">Combinations</span></li>')
        for c in combos:
            items.append(
                f'<li><a href="#{esc(c.get("slug", ""))}">{esc(c.get("title", ""))}</a></li>'
            )
    return "".join(items)


def render_meta(meta: list[dict]) -> str:
    if not meta:
        return ""
    return "".join(
        f'<span><strong>{esc(m.get("label", ""))}</strong> · {esc(m.get("value", ""))}</span>'
        for m in meta
    )


def render_site(data: dict, template: str) -> str:
    tools = data.get("tools", []) or []
    combos = data.get("combos", []) or []

    sections_html = "\n".join(render_tool_section(t) for t in tools)
    sections_html += "\n" + "\n".join(render_combo_section(c) for c in combos)

    replacements = {
        "{{LANG}}": esc(data.get("lang", "en")),
        "{{TITLE}}": esc(data.get("title", "Tool Mastery")),
        "{{DESCRIPTION}}": esc(data.get("description", "")),
        "{{KICKER}}": esc(data.get("kicker", "TOOL MASTERY")),
        "{{HERO_TITLE}}": esc(data.get("heroTitle", "")),
        "{{HERO_SUBTITLE}}": esc(data.get("heroSubtitle", "")),
        "{{HERO_META}}": render_meta(data.get("heroMeta", [])),
        "{{TOC_HTML}}": render_toc(tools, combos),
        "{{SECTIONS_HTML}}": sections_html,
        "{{FOOTER_LEFT}}": esc(data.get("footerLeft", "Generated by the tool-mastery skill")),
        "{{FOOTER_RIGHT}}": esc(data.get("footerRight", "")),
    }
    out = template
    for key, val in replacements.items():
        out = out.replace(key, val)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", help="Path to the JSON data file")
    parser.add_argument("--output", "-o", default="index.html", help="Output HTML path")
    parser.add_argument(
        "--template",
        "-t",
        default=None,
        help="Override the template path (defaults to ../assets/template.html next to this script)",
    )
    args = parser.parse_args()

    data_path = Path(args.data)
    data = json.loads(data_path.read_text(encoding="utf-8"))

    if args.template:
        template_path = Path(args.template)
    else:
        template_path = Path(__file__).resolve().parent.parent / "assets" / "template.html"

    template = template_path.read_text(encoding="utf-8")
    out_html = render_site(data, template)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(out_html, encoding="utf-8")
    print(f"Rendered → {output_path.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
