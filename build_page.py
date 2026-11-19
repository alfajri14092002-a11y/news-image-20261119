#!/usr/bin/env python3
"""Build page.html for the 43-story Thursday 19 November 2026 front page.

Cream newspaper layout, 1024x1024: top bar, masthead, region bar,
six-number stat bar, three hero stories with drawn banners, ten small
drawn cards in two rows, a dotted world map with numbered dots beside
thirty numbered briefs, a DATE CHECK box and a sources footer.
Reads stories.json. Run: python3 build_page.py
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

STYLESHEET = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 1024px; height: 1024px; overflow: hidden; }
  body { background: #f6f1e3; color: #1a1a1a;
    font-family: "Liberation Sans", "DejaVu Sans", sans-serif; }
  .sheet { height: 1024px; padding: 8px 18px; display: flex; flex-direction: column; }
  .topbar { display: flex; justify-content: space-between; padding: 0 2px 5px;
    border-bottom: 1px solid #c9bfa4; font-size: 10px; font-weight: bold;
    letter-spacing: 2px; color: #6b6259; }
  .mast { text-align: center; padding: 6px 0 4px; }
  .mast h1 { font-family: "Liberation Serif", "DejaVu Serif", serif;
    font-size: 40px; line-height: 1; }
  .mast .standfirst { font-size: 12.5px; font-style: italic; color: #4a4238; margin-top: 4px; }
  .regionbar { display: flex; justify-content: space-between; background: #1a1a1a;
    color: #fff; font-size: 10px; font-weight: bold; letter-spacing: 1px; padding: 5px 2px 0; }
  .regionbar span { padding: 2px 6px; }
  .regionbar b { color: #e8c15a; }
  .statbar { display: grid; grid-template-columns: repeat(6, 1fr); margin-top: 6px;
    border-top: 2px solid #1a1a1a; border-bottom: 1px solid #c9bfa4; }
  .cell { text-align: center; padding: 3px 4px 4px; border-right: 1px solid #ddd2b8; }
  .cell:last-child { border-right: none; }
  .cell .big { font-family: "Liberation Serif", "DejaVu Serif", serif;
    font-size: 20px; font-weight: bold; color: #b91c1c; line-height: 1; }
  .cell .small { font-size: 9px; line-height: 1.25; color: #4a4238; margin-top: 2px; }
  .heroes { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-top: 6px; }
  .hero { background: #fffdf6; border: 1px solid #d8d0bd; }
  .hero .art { height: 44px; width: 100%; display: block; }
  .hero .text { padding: 5px 9px 6px; }
  .kick { color: #b91c1c; font-weight: bold; letter-spacing: 1px; font-size: 10px; }
  .kick .tag { background: #b91c1c; color: #fff; padding: 1px 5px; margin-right: 4px; }
  .hero h2 { font-family: "Liberation Serif", "DejaVu Serif", serif;
    font-size: 18px; line-height: 1.12; margin-top: 3px; }
  .hero p { font-size: 11px; line-height: 1.3; color: #333; margin-top: 3px; }
  .cards { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin-top: 6px; }
  .card { background: #fffdf6; border: 1px solid #d8d0bd; }
  .card .art { height: 28px; width: 100%; display: block; }
  .card .text { padding: 4px 7px 5px; }
  .card .kick { font-size: 8.5px; }
  .card .kick .tag { padding: 1px 4px; margin-right: 3px; }
  .card h3 { font-family: "Liberation Serif", "DejaVu Serif", serif;
    font-size: 12px; line-height: 1.18; margin-top: 2px; }
  .bottom { display: flex; gap: 12px; margin-top: 6px; flex: 1; min-height: 0; }
  .map { width: 330px; flex-shrink: 0; background: #10243e; color: #fff; padding: 6px 8px; }
  .map h4 { font-size: 10px; letter-spacing: 2px; color: #e8c15a; }
  .map .mapnote { font-size: 8.5px; color: #cfd8e3; margin-top: 2px; }
  .map svg { display: block; margin-top: 4px; }
  .rest { flex: 1; min-width: 0; }
  .rest h4 { color: #b91c1c; font-size: 10.5px; letter-spacing: 2px; }
  .briefcols { display: grid; grid-template-columns: 1fr 1fr; gap: 1px 16px; margin-top: 3px; }
  .brief { font-size: 10px; line-height: 1.12; padding: 0.5px 0; border-bottom: 1px solid #e3dcc9; }
  .brief .tag { color: #b91c1c; font-weight: bold; }
  .brief b { font-weight: bold; }
  .check { margin-top: 6px; background: #f3ead3; border: 1px solid #d8c98f;
    padding: 4px 10px; font-size: 10.5px; line-height: 1.35; }
  .check b { color: #b91c1c; letter-spacing: 1px; }
  .colophon { margin-top: 4px; font-size: 10px; color: #6b6259;
    text-align: center; line-height: 1.4; }
"""

# Coarse equirectangular land mask, 60 cols (lon -180..180) x 28 rows (lat 75..-55).
WORLD_MAP = [
    "..XXXX..XXXXXXXXXXX..XXXX..........XXXXXXXXXXXXXXXXXXXXXXXXX",
    "..XXXXXXXXXXXXXXXXXXX............XXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "...XXXXXXXXXXXXXXXXXX........X..XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "........XXXXXXXXXXXXXXXX.....XX..XXXXXXXXXXXXXXXXXXXXXXXXXX.",
    "........XXXXXXXXXXXXX........XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.",
    "........XXXXXXXXXXXX...........XXXXXXXXXXXXXXXXXXXXXXXXX....",
    ".........XXXXXXXXXX............XXXXXXXXXXXXXXXXXXXXXXXX.....",
    ".........XXXXXXXXXX............XXXXXXX..XXXXXXXXXXXXXXX.....",
    ".........XXXXXXXXXX.............XXXXXX.XXXXXXXXXXXXXXX.......",
    "..........XXXXXXXXX.........XXXXXXXXXXXXXXXXXXXXXXXXX.......",
    "...........XXXXX............XXXXXXXXXXXXXXXXX.XXX...........",
    "............XXXX............XXXXXXXXXXXXXXXXX.XXX...........",
    "...............XXX..........XXXXXXXXXXX....XX.XXX...........",
    "...............XXX...........XXXXXXXXXX.......XXXXXXXX......",
    ".................XXXXXX......XXXXXXXXX........XXXXXXXXX.....",
    ".................XXXXXXX......XXXXXXXX.........XXXXXXXXX....",
    "..................XXXXXX......XXXXXXX............XXXXXXX....",
    "..................XXXXXX.......XXXXXX............XXXXXXXX...",
    "..................XXXXX.........XXXXX............XXXXXXXX...",
    "..................XXXXX.........XXXX..............XXXXXXX...",
    "..................XXXX..........XXXX..............XXXXXX....",
    "..................XXXX............................XXXXX.....",
    "..................XXXX.............................XXXX...XX",
    "..................XXXX....................................XX",
    "..................XXX.....................................X.",
    "...................XX.......................................",
    "...................XX.......................................",
    "...................X........................................",
]


def project(lon, lat, width, height):
    return (lon + 180.0) / 360.0 * width, (75.0 - lat) / 130.0 * height


def dotted_map(numbered):
    """Dotted world map, 314x300, with numbered dots for the drawn stories."""
    width, height = 314, 300
    parts = []
    step_x, step_y = width / 60.0, height / 28.0
    for row_i, row in enumerate(WORLD_MAP):
        for col_i, ch in enumerate(row):
            if ch == "X":
                cx = (col_i + 0.5) * step_x
                cy = (row_i + 0.5) * step_y
                parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="1.9" fill="#7fa8c9"/>')
    for story in numbered:
        x, y = project(story["lon"], story["lat"], width, height)
        x += story.get("dx", 0)
        y += story.get("dy", 0)
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="#b91c1c"/>'
            f'<text x="{x:.1f}" y="{y + 3:.1f}" fill="#fff" font-size="9" '
            f'font-weight="bold" text-anchor="middle">{story["n"]}</text>')
    return '<svg width="314" height="300" viewBox="0 0 314 300">' + "".join(parts) + "</svg>"


def strip(label, top, height, size):
    return (f'<rect x="0" y="{top}" width="300" height="{height}" fill="#b91c1c"/>'
            f'<text x="8" y="{top + height - 3}" fill="#fff" font-family="sans-serif" '
            f'font-size="{size}" font-weight="bold" letter-spacing="1">{html.escape(label)}</text>')


def skyline(heights, base_y, color, gap=4, width=14):
    """A row of buildings from a list of heights, starting at x=16."""
    out = []
    x = 16
    for h in heights:
        out.append(f'<rect x="{x}" y="{base_y - h}" width="{width}" height="{h}" fill="{color}"/>')
        x += width + gap
    return "".join(out)


def trend(points, color, width=2.5):
    """A polyline through (x, y) points."""
    pts = " ".join(f"{x},{y}" for x, y in points)
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}"/>'


def hero_art(kind, label):
    if kind == "shenzhen":
        body = ('<rect width="300" height="82" fill="#0e2a4e"/>'
                + skyline([38, 52, 30, 58, 44, 34, 54, 40, 48, 32, 42, 50], 82, "#e8c15a")
                + '<g fill="#fff"><circle cx="48" cy="12" r="2"/><circle cx="118" cy="9" r="1.6"/>'
                  '<circle cx="196" cy="14" r="2"/><circle cx="258" cy="11" r="1.6"/>'
                  '<circle cx="150" cy="7" r="1.4"/></g>')
    elif kind == "gta":
        body = ('<rect width="300" height="82" fill="#12041f"/>'
                '<circle cx="248" cy="20" r="13" fill="#ff2e88"/>'
                + skyline([36, 48, 30, 54, 40, 28, 46, 34, 42, 30], 82, "#1f0b33", gap=5, width=16)
                + '<g fill="#ff2e88"><rect x="42" y="34" width="12" height="2"/>'
                  '<rect x="90" y="28" width="11" height="2"/><rect x="156" y="36" width="13" height="2"/>'
                  '<rect x="204" y="40" width="11" height="2"/></g>'
                + '<g fill="#00e5ff"><rect x="18" y="46" width="14" height="2"/>'
                  '<rect x="64" y="52" width="16" height="2"/><rect x="112" y="42" width="14" height="2"/>'
                  '<rect x="178" y="50" width="15" height="2"/></g>'
                + '<g stroke="#00e5ff" stroke-width="1.2" fill="none">'
                  '<path d="M28 82 q9 -13 18 0"/><path d="M268 82 q9 -13 18 0"/></g>')
    elif kind == "ipo":
        body = ('<rect width="300" height="82" fill="#0d2b1a"/>'
                '<g fill="#e8c15a">'
                '<rect x="28" y="54" width="22" height="12"/><rect x="64" y="46" width="22" height="20"/>'
                '<rect x="100" y="36" width="22" height="30"/><rect x="136" y="26" width="22" height="40"/>'
                '</g>'
                + trend([(28, 54), (75, 44), (111, 34), (147, 24), (188, 14), (238, 8)], "#fff")
                + '<polygon points="238,8 226,10 234,18" fill="#fff"/>'
                + '<g fill="#e8c15a"><circle cx="212" cy="50" r="13"/>'
                  '<rect x="206" y="32" width="4" height="10"/><rect x="214" y="32" width="4" height="10"/></g>'
                + '<rect x="196" y="63" width="32" height="4" fill="#e8c15a"/>')
    else:
        raise ValueError(f"unknown hero art {kind}")
    return ('<svg class="art" viewBox="0 0 300 82" preserveAspectRatio="none">'
            + body + strip(label, 66, 16, 10) + "</svg>")


def small_art(kind, label):
    if kind == "court":
        body = """
        <rect width="300" height="48" fill="#3a2c1c"/>
        <rect x="147" y="8" width="6" height="28" fill="#e8c15a"/>
        <rect x="122" y="36" width="56" height="4" fill="#e8c15a"/>
        <line x1="112" y1="13" x2="188" y2="13" stroke="#e8c15a" stroke-width="2.5"/>
        <path d="M112 13 L100 28 L124 28 Z" fill="#e8c15a"/>
        <path d="M188 13 L176 28 L200 28 Z" fill="#e8c15a"/>
        <rect x="140" y="40" width="20" height="4" fill="#e8c15a"/>"""
    elif kind == "cyclone":
        body = """
        <rect width="300" height="48" fill="#0f3d4a"/>
        <g fill="none" stroke="#7fb8a8" stroke-width="2">
          <circle cx="150" cy="24" r="5"/><circle cx="150" cy="24" r="11"/>
          <circle cx="150" cy="24" r="17"/><circle cx="150" cy="24" r="22"/>
        </g>
        <g stroke="#bfe3d8" stroke-width="1.2">
          <line x1="32" y1="9" x2="26" y2="20"/><line x1="62" y1="7" x2="56" y2="18"/>
          <line x1="238" y1="9" x2="244" y2="20"/><line x1="268" y1="7" x2="274" y2="18"/>
        </g>
        <circle cx="150" cy="24" r="2.5" fill="#e8c15a"/>"""
    elif kind == "flood":
        body = """
        <rect width="300" height="48" fill="#1c2733"/>
        <g stroke="#7fb8a8" stroke-width="1.6">
          <line x1="42" y1="6" x2="36" y2="15"/><line x1="72" y1="4" x2="66" y2="13"/>
          <line x1="102" y1="6" x2="96" y2="15"/><line x1="202" y1="4" x2="196" y2="13"/>
          <line x1="232" y1="6" x2="226" y2="15"/><line x1="262" y1="4" x2="256" y2="13"/>
        </g>
        <path d="M0 31 q25 -8 50 0 t50 0 t50 0 t50 0 t50 0 t50 0" fill="none" stroke="#e8c15a" stroke-width="2"/>
        <path d="M0 41 q25 -8 50 0 t50 0 t50 0 t50 0 t50 0 t50 0" fill="none" stroke="#e8c15a" stroke-width="2"/>
        <g fill="#fff"><rect x="142" y="21" width="18" height="7"/><rect x="147" y="17" width="8" height="4"/></g>"""
    elif kind == "cop31":
        body = """
        <rect width="300" height="48" fill="#14532d"/>
        <circle cx="150" cy="24" r="15" fill="#7fb8a8"/>
        <g fill="none" stroke="#14532d" stroke-width="1.2">
          <ellipse cx="150" cy="24" rx="6" ry="15"/><path d="M135 24 h30"/>
          <path d="M139 15 q11 9 22 0"/><path d="M139 33 q11 -9 22 0"/>
        </g>
        <g fill="#e8c15a"><path d="M54 34 q7 -13 14 0 q-7 4 -14 0"/>
        <path d="M232 34 q7 -13 14 0 q-7 4 -14 0"/></g>"""
    elif kind == "fed":
        body = """
        <rect width="300" height="48" fill="#10243e"/>
        <g fill="#e8e4d8">
          <rect x="42" y="17" width="9" height="20"/><rect x="38" y="14" width="17" height="3"/><rect x="38" y="37" width="17" height="3"/>
          <rect x="72" y="17" width="9" height="20"/><rect x="68" y="14" width="17" height="3"/><rect x="68" y="37" width="17" height="3"/>
          <rect x="102" y="17" width="9" height="20"/><rect x="98" y="14" width="17" height="3"/><rect x="98" y="37" width="17" height="3"/>
        </g>
        <polyline points="150,37 184,27 214,29 256,11" fill="none" stroke="#e8c15a" stroke-width="2.5"/>
        <polygon points="256,11 244,13 252,21" fill="#e8c15a"/>"""
    elif kind == "chip":
        body = """
        <rect width="300" height="48" fill="#0b0b18"/>
        <g stroke="#22c55e" stroke-width="1.5">
          <line x1="126" y1="24" x2="110" y2="24"/><line x1="126" y1="18" x2="110" y2="18"/><line x1="126" y1="30" x2="110" y2="30"/>
          <line x1="174" y1="24" x2="190" y2="24"/><line x1="174" y1="18" x2="190" y2="18"/><line x1="174" y1="30" x2="190" y2="30"/>
        </g>
        <rect x="126" y="9" width="48" height="30" fill="#14532d" stroke="#22c55e" stroke-width="1.5"/>
        <rect x="139" y="17" width="22" height="14" fill="#22c55e"/>"""
    elif kind == "drones":
        body = """
        <rect width="300" height="48" fill="#1c2733"/>
        <g stroke="#7fb8a8" stroke-width="1" stroke-dasharray="3 3" fill="none">
          <path d="M22 13 L88 25"/><path d="M122 9 L188 23"/><path d="M212 15 L278 29"/>
        </g>
        <g fill="#e8c15a">
          <rect x="84" y="21" width="10" height="3"/><rect x="87" y="18" width="3" height="9"/>
          <rect x="184" y="19" width="10" height="3"/><rect x="187" y="16" width="3" height="9"/>
          <rect x="274" y="25" width="10" height="3"/><rect x="277" y="22" width="3" height="9"/>
        </g>
        <g fill="#b91c1c"><circle cx="89" cy="23" r="2"/><circle cx="189" cy="21" r="2"/><circle cx="279" cy="27" r="2"/></g>"""
    elif kind == "tanks":
        body = """
        <rect width="300" height="48" fill="#c9a86a"/>
        <circle cx="264" cy="12" r="7" fill="#e8c15a"/>
        <rect y="36" width="300" height="12" fill="#a9854e"/>
        <g fill="#5a4632">
          <rect x="42" y="27" width="50" height="9"/><rect x="60" y="20" width="17" height="8"/>
          <rect x="77" y="22" width="32" height="3"/>
          <rect x="182" y="29" width="42" height="8"/><rect x="196" y="23" width="14" height="7"/>
          <rect x="210" y="25" width="26" height="2.6"/>
        </g>
        <g fill="#3d2f1e">
          <circle cx="54" cy="38" r="2.4"/><circle cx="68" cy="38" r="2.4"/><circle cx="82" cy="38" r="2.4"/>
          <circle cx="192" cy="39" r="2.2"/><circle cx="204" cy="39" r="2.2"/><circle cx="216" cy="39" r="2.2"/>
        </g>"""
    elif kind == "rocket":
        body = """
        <rect width="300" height="48" fill="#0b1e3a"/>
        <g fill="#fff"><circle cx="42" cy="11" r="1.4"/><circle cx="82" cy="17" r="1.2"/>
        <circle cx="232" cy="11" r="1.4"/><circle cx="264" cy="19" r="1.2"/><circle cx="198" cy="9" r="1.2"/></g>
        <g fill="#e8e4d8"><path d="M150 7 L157 23 L150 29 L143 23 Z"/><rect x="143" y="23" width="14" height="6"/></g>
        <path d="M147 29 L150 41 L153 29 Z" fill="#e8c15a"/>
        <g stroke="#7fb8a8" stroke-width="1.2" fill="none"><path d="M150 41 q-4 4 0 6"/><path d="M150 41 q4 4 0 6"/></g>"""
    elif kind == "eu":
        body = """
        <rect width="300" height="48" fill="#1e3a8a"/>
        <g fill="#e8c15a">
          <circle cx="150" cy="11" r="2.5"/><circle cx="165" cy="15" r="2.5"/><circle cx="171" cy="24" r="2.5"/>
          <circle cx="165" cy="33" r="2.5"/><circle cx="150" cy="37" r="2.5"/><circle cx="135" cy="33" r="2.5"/>
          <circle cx="129" cy="24" r="2.5"/><circle cx="135" cy="15" r="2.5"/>
        </g>
        <circle cx="150" cy="24" r="4.5" fill="none" stroke="#e8c15a" stroke-width="1.2"/>"""
    elif kind == "ipo":
        body = ('<rect width="300" height="48" fill="#0d2b1a"/>'
                + skyline([10, 16, 22, 28], 40, "#e8c15a", gap=10, width=16)
                + '<polyline points="40,30 74,22 100,16 126,10 160,6 200,4" fill="none" stroke="#fff" stroke-width="2"/>'
                + '<polygon points="200,4 188,6 196,12" fill="#fff"/>')
    elif kind == "skyline":
        body = ('<rect width="300" height="48" fill="#0e2a4e"/>'
                + skyline([24, 32, 20, 36, 26, 18, 30, 22, 34, 24, 18], 48, "#e8c15a", gap=8, width=12)
                + '<g fill="#fff"><circle cx="160" cy="10" r="1.6"/><circle cx="60" cy="8" r="1.4"/>'
                  '<circle cx="250" cy="8" r="1.4"/></g>')
    else:
        raise ValueError(f"unknown small art {kind}")
    return ('<svg class="art" viewBox="0 0 300 48" preserveAspectRatio="none">'
            + body + strip(label, 36, 12, 8) + "</svg>")


def build():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as handle:
        data = json.load(handle)
    all_stories = data["stories"]
    heroes = [s for s in all_stories if s.get("hero")]
    cards = [s for s in all_stories if s.get("drawn")]
    briefs = [s for s in all_stories if not s.get("hero") and not s.get("drawn")]
    assert len(heroes) == 3, f"need 3 heroes, got {len(heroes)}"
    assert len(cards) == 10, f"need 10 drawn, got {len(cards)}"
    assert len(briefs) == 30, f"need 30 briefs, got {len(briefs)}"
    assert len(all_stories) == 43, f"need 43 stories, got {len(all_stories)}"

    for idx, story in enumerate(heroes + cards + briefs, 1):
        story["n"] = idx

    region_order = ["ASIA", "MIDDLE EAST", "EUROPE", "AFRICA",
                    "NORTH AMERICA", "SOUTH AMERICA", "OCEANIA"]
    tallies = {r: sum(1 for s in all_stories if s["region"] == r) for r in region_order}
    assert all(tallies[r] > 0 for r in region_order), f"empty region: {tallies}"
    region_bar = "".join(
        f"<span>{name.title()} <b>{tallies[name]}</b></span>" for name in region_order)

    stats = data["stats"]
    assert len(stats) == 6, f"need 6 stats, got {len(stats)}"
    stat_bar = "".join(
        f'<div class="cell"><div class="big">{html.escape(item["num"])}</div>'
        f'<div class="small">{html.escape(item["cap"])}</div></div>' for item in stats)

    esc = html.escape

    hero_cards = []
    for story in heroes:
        hero_cards.append(f"""
    <article class="hero">
      {hero_art(story["art"], story["label"])}
      <div class="text">
        <div class="kick"><span class="tag">{story["n"]}</span>{esc(story["region"])} &bull; {esc(story["topic"])}</div>
        <h2>{esc(story["headline"])}</h2>
        <p>{esc(story["summary"])}</p>
      </div>
    </article>""")

    small_cards = []
    for story in cards:
        small_cards.append(f"""
    <article class="card">
      {small_art(story["art"], story["label"])}
      <div class="text">
        <div class="kick"><span class="tag">{story["n"]}</span>{esc(story["region"])} &bull; {esc(story["topic"])}</div>
        <h3>{esc(story["headline"])}</h3>
      </div>
    </article>""")

    columns = [[], []]
    for pos, story in enumerate(briefs):
        columns[pos % 2].append(story)
    column_html = []
    for column in columns:
        lines = []
        for story in column:
            lines.append(
                f'        <div class="brief"><span class="tag">{story["n"]}</span> '
                f'<b>{esc(story["lead"])}</b> {esc(story["clause"])}</div>')
        column_html.append("      <div>\n" + "\n".join(lines) + "\n      </div>")

    for story in heroes + cards:
        assert "lon" in story and "lat" in story, f"story {story['n']} missing lon/lat"
    map_svg = dotted_map(heroes + cards)

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Thursday 19 November 2026 — The Day in World News</title>
<style>{STYLESHEET}</style>
</head>
<body>
<div class="sheet">

  <div class="topbar"><span>THE WORLD IN ONE PICTURE</span><span>EVERY STORY FROM ONE DAY</span><span>THURSDAY EDITION &bull; ONE PAGE</span></div>

  <header class="mast">
    <h1>Thursday 19 November 2026</h1>
    <div class="standfirst">{esc(data["subline"])}</div>
  </header>

  <div class="regionbar">{region_bar}</div>

  <div class="statbar">{stat_bar}</div>

  <section class="heroes">{''.join(hero_cards)}
  </section>

  <section class="cards">{''.join(small_cards)}
  </section>

  <div class="bottom">
    <div class="map">
      <h4>WHERE IT HAPPENED</h4>
      <div class="mapnote">NUMBERED &bull; CARDS &bull; DOTS &bull; BRIEFS</div>
      {map_svg}
    </div>
    <div class="rest">
      <h4>THE REST OF THE DAY &mdash; 30 MORE STORIES</h4>
      <div class="briefcols">
{chr(10).join(column_html)}      </div>
    </div>
  </div>

  <div class="check"><b>DATE CHECK</b> &mdash; {esc(data["datecheck"])}</div>
  <footer class="colophon">All 43 stories happened, or were first reported, on Thursday 19 November 2026; claims are attributed. Original drawings.<br>Sources: {esc(data["sources"])}</footer>

</div>
</body>
</html>
"""
    target = os.path.join(HERE, "page.html")
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(document)
    print(f"wrote {target}: {len(all_stories)} stories, regions {tallies}")


if __name__ == "__main__":
    build()
