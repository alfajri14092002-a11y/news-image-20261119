#!/usr/bin/env python3
"""Build page.html for the 43-story Thursday 19 November 2026 front page.

Layout (1024x1024), cream newspaper style: masthead, region strip,
6-stat strip, 3 hero drawn stories, 10 small drawn stories (2 rows of 5),
dotted world map with numbered location dots + 30 numbered briefs,
DATE CHECK box, footer. Reads stories.json. Run: python3 build_page.py
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

CSS = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 1024px; height: 1024px; overflow: hidden; }
  body {
    background: #f6f1e3; color: #1a1a1a;
    font-family: "Liberation Sans", "DejaVu Sans", sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  .page { height: 1024px; padding: 8px 18px 8px; display: flex; flex-direction: column; }
  .serif { font-family: "Liberation Serif", "DejaVu Serif", serif; }
  .kicker { color: #b91c1c; font-weight: bold; letter-spacing: 1px; }

  .topline { display: flex; justify-content: space-between; font-size: 10px; font-weight: bold; letter-spacing: 2px; color: #6b6259; padding: 0 2px 5px; border-bottom: 1px solid #c9bfa4; }
  .masthead { text-align: center; padding: 6px 0 4px; }
  .masthead h1 { font-family: "Liberation Serif", "DejaVu Serif", serif; font-size: 42px; line-height: 1; font-weight: bold; }
  .masthead .sub { font-size: 12.5px; font-style: italic; color: #4a4238; margin-top: 4px; }

  .regions { display: flex; justify-content: space-between; padding: 5px 2px 0; font-size: 10px; font-weight: bold; letter-spacing: 1px; color: #fff; background: #1a1a1a; }
  .regions span { padding: 2px 6px; }
  .regions b { color: #e8c15a; }

  .stats { display: grid; grid-template-columns: repeat(6, 1fr); gap: 0; margin-top: 6px; border-top: 2px solid #1a1a1a; border-bottom: 1px solid #c9bfa4; }
  .stat { text-align: center; padding: 4px 4px 5px; border-right: 1px solid #ddd2b8; }
  .stat:last-child { border-right: none; }
  .stat .num { font-family: "Liberation Serif", "DejaVu Serif", serif; font-size: 21px; font-weight: bold; color: #b91c1c; line-height: 1; }
  .stat .cap { font-size: 9px; line-height: 1.25; color: #4a4238; margin-top: 2px; }

  .top3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-top: 6px; }
  .topstory { background: #fffdf6; border: 1px solid #d8d0bd; }
  .topstory .banner { height: 52px; width: 100%; display: block; }
  .topstory .body { padding: 5px 9px 6px; }
  .topstory .kicker { font-size: 10px; }
  .topstory .kicker .n { background: #b91c1c; color: #fff; padding: 1px 5px; margin-right: 4px; }
  .topstory h2 { font-family: "Liberation Serif", "DejaVu Serif", serif; font-size: 19px; line-height: 1.12; margin-top: 3px; }
  .topstory p { font-size: 11px; line-height: 1.3; color: #333; margin-top: 3px; }

  .drawn10 { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin-top: 6px; }
  .drawn { background: #fffdf6; border: 1px solid #d8d0bd; }
  .drawn .banner { height: 32px; width: 100%; display: block; }
  .drawn .body { padding: 4px 7px 5px; }
  .drawn .kicker { font-size: 8.5px; }
  .drawn .kicker .n { background: #b91c1c; color: #fff; padding: 1px 4px; margin-right: 3px; }
  .drawn h3 { font-family: "Liberation Serif", "DejaVu Serif", serif; font-size: 12px; line-height: 1.18; margin-top: 2px; }

  .lower { display: flex; gap: 12px; margin-top: 6px; flex: 1; min-height: 0; }
  .mapbox { width: 330px; flex-shrink: 0; background: #10243e; color: #fff; padding: 6px 8px; }
  .mapbox h4 { font-size: 10px; letter-spacing: 2px; color: #e8c15a; }
  .mapbox .legend { font-size: 8.5px; color: #cfd8e3; margin-top: 2px; }
  .mapbox svg { display: block; margin-top: 4px; }
  .briefs { flex: 1; min-width: 0; }
  .briefs h4 { color: #b91c1c; font-size: 10.5px; letter-spacing: 2px; }
  .cols { display: grid; grid-template-columns: 1fr 1fr; gap: 1px 16px; margin-top: 3px; }
  .item { font-size: 10px; line-height: 1.14; padding: 1px 0; border-bottom: 1px solid #e3dcc9; }
  .item .n { color: #b91c1c; font-weight: bold; }
  .item b { font-weight: bold; }

  .datecheck { margin-top: 6px; background: #f3ead3; border: 1px solid #d8c98f; padding: 4px 10px; font-size: 10.5px; line-height: 1.35; }
  .datecheck b { color: #b91c1c; letter-spacing: 1px; }
  footer { margin-top: 4px; font-size: 10px; color: #6b6259; text-align: center; line-height: 1.4; }
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


def lonlat_to_xy(lon, lat, w, h):
    x = (lon + 180.0) / 360.0 * w
    y = (75.0 - lat) / 130.0 * h
    return x, y


def world_map_svg(numbered):
    """Dotted world map, 314x300, with numbered location dots for the drawn stories."""
    w, h = 314, 300
    dots = []
    cell_w, cell_h = w / 60.0, h / 28.0
    for r, row in enumerate(WORLD_MAP):
        for c, ch in enumerate(row):
            if ch == "X":
                cx = (c + 0.5) * cell_w
                cy = (r + 0.5) * cell_h
                dots.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="1.9" fill="#7fa8c9"/>')
    nums = []
    for s in numbered:
        x, y = lonlat_to_xy(s["lon"], s["lat"], w, h)
        x += s.get("dx", 0)
        y += s.get("dy", 0)
        nums.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="#b91c1c"/>'
            f'<text x="{x:.1f}" y="{y + 3:.1f}" fill="#fff" font-size="9" '
            f'font-weight="bold" text-anchor="middle">{s["n"]}</text>')
    return ('<svg width="314" height="300" viewBox="0 0 314 300">'
            + "".join(dots) + "".join(nums) + "</svg>")


def label_strip(label, y=70, h=12, fs=9):
    return (f'<rect x="0" y="{y}" width="300" height="{h}" fill="#b91c1c"/>'
            f'<text x="8" y="{y + h - 3}" fill="#fff" font-family="sans-serif" '
            f'font-size="{fs}" font-weight="bold" letter-spacing="1">{html.escape(label)}</text>')


def hero_svg(art, label):
    if art == "shenzhen":
        inner = """
        <rect width="300" height="82" fill="#0e2a4e"/>
        <g fill="#e8c15a">
          <rect x="18" y="42" width="16" height="40"/><rect x="40" y="30" width="14" height="52"/>
          <rect x="60" y="50" width="20" height="32"/><rect x="86" y="22" width="14" height="60"/>
          <rect x="106" y="38" width="18" height="44"/><rect x="130" y="48" width="12" height="34"/>
          <rect x="148" y="28" width="16" height="54"/><rect x="170" y="44" width="18" height="38"/>
          <rect x="194" y="34" width="13" height="48"/><rect x="213" y="52" width="20" height="30"/>
          <rect x="239" y="40" width="14" height="42"/><rect x="259" y="30" width="16" height="52"/>
        </g>
        <g fill="#fff"><circle cx="52" cy="14" r="2"/><circle cx="120" cy="10" r="1.6"/><circle cx="200" cy="16" r="2"/><circle cx="262" cy="12" r="1.6"/><circle cx="150" cy="8" r="1.4"/></g>"""
    elif art == "gta":
        inner = """
        <rect width="300" height="82" fill="#12041f"/>
        <circle cx="252" cy="18" r="12" fill="#ff2e88"/>
        <g fill="#1f0b33">
          <rect x="14" y="44" width="18" height="38"/><rect x="38" y="32" width="16" height="50"/>
          <rect x="60" y="50" width="20" height="32"/><rect x="86" y="26" width="15" height="56"/>
          <rect x="107" y="40" width="18" height="42"/><rect x="131" y="54" width="14" height="28"/>
          <rect x="151" y="34" width="17" height="48"/><rect x="174" y="48" width="19" height="34"/>
          <rect x="199" y="38" width="15" height="44"/><rect x="220" y="52" width="20" height="30"/>
        </g>
        <g fill="#ff2e88">
          <rect x="40" y="34" width="12" height="2"/><rect x="88" y="28" width="11" height="2"/>
          <rect x="153" y="36" width="13" height="2"/><rect x="201" y="40" width="11" height="2"/>
        </g>
        <g fill="#00e5ff">
          <rect x="16" y="46" width="14" height="2"/><rect x="62" y="52" width="16" height="2"/>
          <rect x="109" y="42" width="14" height="2"/><rect x="176" y="50" width="15" height="2"/>
        </g>
        <g fill="#e8c15a"><circle cx="60" cy="14" r="1.6"/><circle cx="130" cy="10" r="1.6"/><circle cx="200" cy="14" r="1.6"/></g>
        <g stroke="#00e5ff" stroke-width="1.2" fill="none"><path d="M30 82 q10 -14 20 0"/><path d="M270 82 q10 -14 20 0"/></g>"""
    elif art == "ipo":
        inner = """
        <rect width="300" height="82" fill="#0d2b1a"/>
        <g fill="#e8c15a">
          <rect x="30" y="52" width="22" height="14"/><rect x="66" y="44" width="22" height="22"/>
          <rect x="102" y="34" width="22" height="32"/><rect x="138" y="24" width="22" height="42"/>
        </g>
        <g stroke="#fff" stroke-width="2.5" fill="none"><path d="M30 52 L77 42 L113 32 L149 22 L190 12 L240 6"/></g>
        <polygon points="240,6 228,8 236,16" fill="#fff"/>
        <g fill="#e8c15a"><circle cx="212" cy="48" r="14"/><rect x="206" y="30" width="4" height="10"/><rect x="214" y="30" width="4" height="10"/></g>
        <rect x="196" y="62" width="32" height="4" fill="#e8c15a"/>"""
    else:
        raise ValueError(f"unknown hero art {art}")
    return ('<svg class="banner" viewBox="0 0 300 82" preserveAspectRatio="none">'
            + inner + label_strip(label, y=66, h=16, fs=10) + '</svg>')


def small_svg(art, label):
    scenes = {
        "court": """
        <rect width="300" height="48" fill="#3a2c1c"/>
        <rect x="146" y="6" width="8" height="30" fill="#e8c15a"/>
        <rect x="120" y="36" width="60" height="4" fill="#e8c15a"/>
        <line x1="110" y1="12" x2="190" y2="12" stroke="#e8c15a" stroke-width="2.5"/>
        <path d="M110 12 L98 28 L122 28 Z" fill="#e8c15a"/>
        <path d="M190 12 L178 28 L202 28 Z" fill="#e8c15a"/>
        <line x1="110" y1="12" x2="110" y2="28" stroke="#e8c15a" stroke-width="1.5"/>
        <line x1="190" y1="12" x2="190" y2="28" stroke="#e8c15a" stroke-width="1.5"/>
        <rect x="138" y="40" width="24" height="4" fill="#e8c15a"/>""",
        "cyclone": """
        <rect width="300" height="48" fill="#0f3d4a"/>
        <g fill="none" stroke="#7fb8a8" stroke-width="2">
          <path d="M150 24 m-4 0 a4 4 0 1 1 8 0 a4 4 0 1 1 -8 0"/>
          <path d="M150 24 m-10 0 a10 10 0 1 1 20 0 a10 10 0 1 1 -20 0"/>
          <path d="M150 24 m-17 0 a17 17 0 1 1 34 0 a17 17 0 1 1 -34 0"/>
        </g>
        <g stroke="#bfe3d8" stroke-width="1.2"><line x1="30" y1="8" x2="24" y2="20"/><line x1="60" y1="6" x2="54" y2="18"/><line x1="240" y1="8" x2="246" y2="20"/><line x1="270" y1="6" x2="276" y2="18"/></g>
        <circle cx="150" cy="24" r="2.5" fill="#e8c15a"/>""",
        "flood": """
        <rect width="300" height="48" fill="#1c2733"/>
        <g stroke="#7fb8a8" stroke-width="1.6"><line x1="40" y1="6" x2="34" y2="16"/><line x1="70" y1="4" x2="64" y2="14"/><line x1="100" y1="6" x2="94" y2="16"/><line x1="200" y1="4" x2="194" y2="14"/><line x1="230" y1="6" x2="224" y2="16"/><line x1="260" y1="4" x2="254" y2="14"/></g>
        <g fill="none" stroke="#e8c15a" stroke-width="2"><path d="M0 30 q25 -8 50 0 t50 0 t50 0 t50 0 t50 0 t50 0"/><path d="M0 40 q25 -8 50 0 t50 0 t50 0 t50 0 t50 0 t50 0"/></g>
        <g fill="#fff"><rect x="140" y="20" width="20" height="8"/><rect x="146" y="16" width="8" height="4"/></g>""",
        "cop31": """
        <rect width="300" height="48" fill="#14532d"/>
        <circle cx="150" cy="24" r="16" fill="#7fb8a8"/>
        <g fill="none" stroke="#14532d" stroke-width="1.2">
          <ellipse cx="150" cy="24" rx="7" ry="16"/><path d="M134 24 h32"/><path d="M138 14 q12 10 24 0"/><path d="M138 34 q12 -10 24 0"/>
        </g>
        <g fill="#e8c15a"><path d="M52 34 q8 -14 16 0 q-8 4 -16 0"/><path d="M232 34 q8 -14 16 0 q-8 4 -16 0"/></g>""",
        "fed": """
        <rect width="300" height="48" fill="#10243e"/>
        <g fill="#e8e4d8">
          <rect x="40" y="16" width="10" height="22"/><rect x="36" y="13" width="18" height="3"/><rect x="36" y="38" width="18" height="3"/>
          <rect x="70" y="16" width="10" height="22"/><rect x="66" y="13" width="18" height="3"/><rect x="66" y="38" width="18" height="3"/>
          <rect x="100" y="16" width="10" height="22"/><rect x="96" y="13" width="18" height="3"/><rect x="96" y="38" width="18" height="3"/>
        </g>
        <g stroke="#e8c15a" stroke-width="2.5" fill="none"><path d="M150 36 L185 26 L215 28 L258 10"/></g>
        <polygon points="258,10 246,12 254,20" fill="#e8c15a"/>""",
        "chip": """
        <rect width="300" height="48" fill="#0b0b18"/>
        <g stroke="#22c55e" stroke-width="1.5">
          <line x1="128" y1="24" x2="112" y2="24"/><line x1="128" y1="18" x2="112" y2="18"/><line x1="128" y1="30" x2="112" y2="30"/>
          <line x1="172" y1="24" x2="188" y2="24"/><line x1="172" y1="18" x2="188" y2="18"/><line x1="172" y1="30" x2="188" y2="30"/>
          <line x1="150" y1="8" x2="150" y2="2"/><line x1="142" y1="8" x2="142" y2="2"/><line x1="158" y1="8" x2="158" y2="2"/>
        </g>
        <rect x="128" y="8" width="44" height="32" fill="#14532d" stroke="#22c55e" stroke-width="1.5"/>
        <rect x="140" y="16" width="20" height="16" fill="#22c55e"/>""",
        "drones": """
        <rect width="300" height="48" fill="#1c2733"/>
        <g stroke="#7fb8a8" stroke-width="1" stroke-dasharray="3 3" fill="none">
          <path d="M20 12 L90 26"/><path d="M120 8 L190 24"/><path d="M210 14 L280 30"/>
        </g>
        <g fill="#e8c15a">
          <rect x="86" y="22" width="10" height="3"/><rect x="89" y="19" width="3" height="9"/>
          <rect x="186" y="20" width="10" height="3"/><rect x="189" y="17" width="3" height="9"/>
          <rect x="276" y="26" width="10" height="3"/><rect x="279" y="23" width="3" height="9"/>
        </g>
        <g fill="#b91c1c"><circle cx="91" cy="24" r="2"/><circle cx="191" cy="22" r="2"/><circle cx="281" cy="28" r="2"/></g>
        <g fill="#fff"><circle cx="40" cy="10" r="1.4"/><circle cx="150" cy="8" r="1.4"/><circle cx="250" cy="10" r="1.4"/></g>""",
        "tanks": """
        <rect width="300" height="48" fill="#c9a86a"/>
        <circle cx="262" cy="12" r="7" fill="#e8c15a"/>
        <rect y="36" width="300" height="12" fill="#a9854e"/>
        <g fill="#5a4632">
          <rect x="40" y="26" width="52" height="10"/><rect x="58" y="19" width="18" height="8"/>
          <rect x="76" y="21" width="34" height="3"/>
          <rect x="180" y="28" width="44" height="9"/><rect x="194" y="22" width="15" height="7"/>
          <rect x="209" y="24" width="28" height="2.6"/>
        </g>
        <g fill="#3d2f1e"><circle cx="52" cy="38" r="2.4"/><circle cx="66" cy="38" r="2.4"/><circle cx="80" cy="38" r="2.4"/><circle cx="190" cy="39" r="2.2"/><circle cx="202" cy="39" r="2.2"/><circle cx="214" cy="39" r="2.2"/></g>""",
        "rocket": """
        <rect width="300" height="48" fill="#0b1e3a"/>
        <g fill="#fff"><circle cx="40" cy="10" r="1.4"/><circle cx="80" cy="16" r="1.2"/><circle cx="230" cy="10" r="1.4"/><circle cx="266" cy="18" r="1.2"/><circle cx="200" cy="8" r="1.2"/></g>
        <g fill="#e8e4d8"><path d="M150 6 L158 24 L150 30 L142 24 Z"/><rect x="142" y="24" width="16" height="6"/></g>
        <g fill="#e8c15a"><path d="M146 30 L150 42 L154 30 Z"/></g>
        <g stroke="#7fb8a8" stroke-width="1.2" fill="none"><path d="M150 42 q-4 4 0 6"/><path d="M150 42 q4 4 0 6"/></g>""",
        "eu": """
        <rect width="300" height="48" fill="#1e3a8a"/>
        <g fill="#e8c15a">
          <circle cx="150" cy="10" r="2.6"/><circle cx="166" cy="14" r="2.6"/><circle cx="172" cy="24" r="2.6"/>
          <circle cx="166" cy="34" r="2.6"/><circle cx="150" cy="38" r="2.6"/><circle cx="134" cy="34" r="2.6"/>
          <circle cx="128" cy="24" r="2.6"/><circle cx="134" cy="14" r="2.6"/>
        </g>
        <circle cx="150" cy="24" r="5" fill="none" stroke="#e8c15a" stroke-width="1.2"/>""",
        "ipo": """
        <rect width="300" height="48" fill="#0d2b1a"/>
        <g fill="#e8c15a">
          <rect x="40" y="30" width="16" height="10"/><rect x="66" y="24" width="16" height="16"/>
          <rect x="92" y="18" width="16" height="22"/><rect x="118" y="12" width="16" height="28"/>
        </g>
        <g stroke="#fff" stroke-width="2" fill="none"><path d="M40 30 L74 22 L100 16 L126 10 L160 6 L200 4"/></g>
        <polygon points="200,4 188,6 196,12" fill="#fff"/>""",
        "skyline": """
        <rect width="300" height="48" fill="#0e2a4e"/>
        <g fill="#e8c15a">
          <rect x="30" y="24" width="14" height="24"/><rect x="50" y="16" width="12" height="32"/>
          <rect x="68" y="28" width="16" height="20"/><rect x="90" y="12" width="12" height="36"/>
          <rect x="108" y="22" width="14" height="26"/><rect x="128" y="30" width="12" height="18"/>
          <rect x="180" y="18" width="14" height="30"/><rect x="200" y="26" width="12" height="22"/>
          <rect x="218" y="14" width="14" height="34"/><rect x="238" y="24" width="12" height="24"/>
          <rect x="256" y="30" width="14" height="18"/>
        </g>
        <g fill="#fff"><circle cx="160" cy="10" r="1.6"/><circle cx="60" cy="8" r="1.4"/><circle cx="250" cy="8" r="1.4"/></g>""",
    }
    if art not in scenes:
        raise ValueError(f"unknown small art {art}")
    return ('<svg class="banner" viewBox="0 0 300 48" preserveAspectRatio="none">'
            + scenes[art] + label_strip(label, y=36, h=12, fs=8) + '</svg>')


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as f:
        data = json.load(f)
    stories = data["stories"]
    heroes = [s for s in stories if s.get("hero")]
    drawn = [s for s in stories if s.get("drawn")]
    rest = [s for s in stories if not s.get("hero") and not s.get("drawn")]
    assert len(heroes) == 3, f"need 3 heroes, got {len(heroes)}"
    assert len(drawn) == 10, f"need 10 drawn, got {len(drawn)}"
    assert len(rest) == 30, f"need 30 rest, got {len(rest)}"
    assert len(stories) == 43, f"need 43 stories, got {len(stories)}"

    order = heroes + drawn + rest
    for i, s in enumerate(order, 1):
        s["n"] = i

    regions = ["ASIA", "MIDDLE EAST", "EUROPE", "AFRICA", "NORTH AMERICA", "SOUTH AMERICA", "OCEANIA"]
    counts = {r: sum(1 for s in stories if s["region"] == r) for r in regions}
    assert all(counts[r] > 0 for r in regions), f"empty region: {counts}"
    assert sum(counts.values()) == 43
    region_strip = "".join(
        f"<span>{r.title()} <b>{counts[r]}</b></span>" for r in regions)

    stats = data["stats"]
    assert len(stats) == 6, f"need 6 stats, got {len(stats)}"
    stats_html = "".join(
        f'<div class="stat"><div class="num">{html.escape(st["num"])}</div>'
        f'<div class="cap">{html.escape(st["cap"])}</div></div>' for st in stats)

    e = html.escape

    hero_html = ""
    for s in heroes:
        hero_html += f"""
    <article class="topstory">
      {hero_svg(s["art"], s["label"])}
      <div class="body">
        <div class="kicker"><span class="n">{s["n"]}</span>{e(s["region"])} &bull; {e(s["topic"])}</div>
        <h2>{e(s["headline"])}</h2>
        <p>{e(s["summary"])}</p>
      </div>
    </article>"""

    drawn_html = ""
    for s in drawn:
        drawn_html += f"""
    <article class="drawn">
      {small_svg(s["art"], s["label"])}
      <div class="body">
        <div class="kicker"><span class="n">{s["n"]}</span>{e(s["region"])} &bull; {e(s["topic"])}</div>
        <h3>{e(s["headline"])}</h3>
      </div>
    </article>"""

    cols = [[], []]
    for i, s in enumerate(rest):
        cols[i % 2].append(s)
    cols_html = ""
    for col in cols:
        cols_html += "      <div>\n"
        for s in col:
            cols_html += (f'        <div class="item"><span class="n">{s["n"]}</span> '
                          f'<b>{e(s["lead"])}</b> {e(s["clause"])}</div>\n')
        cols_html += "      </div>\n"

    numbered = heroes + drawn
    for s in numbered:
        assert "lon" in s and "lat" in s, f"story {s['n']} missing lon/lat"
    map_svg = world_map_svg(numbered)

    datecheck = data["datecheck"]
    footer_sources = data["sources"]
    subline = data["subline"]

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Thursday 19 November 2026 — The Day in World News</title>
<style>{CSS}</style>
</head>
<body>
<div class="page">

  <div class="topline"><span>THE WORLD IN ONE PICTURE</span><span>EVERY STORY FROM ONE DAY</span><span>THURSDAY EDITION &bull; ONE PAGE</span></div>

  <header class="masthead">
    <h1>Thursday 19 November 2026</h1>
    <div class="sub">{e(subline)}</div>
  </header>

  <div class="regions">{region_strip}</div>

  <div class="stats">{stats_html}</div>

  <section class="top3">{hero_html}
  </section>

  <section class="drawn10">{drawn_html}
  </section>

  <div class="lower">
    <div class="mapbox">
      <h4>WHERE IT HAPPENED</h4>
      <div class="legend">NUMBERED &bull; CARDS &bull; DOTS &bull; BRIEFS</div>
      {map_svg}
    </div>
    <div class="briefs">
      <h4>THE REST OF THE DAY &mdash; 30 MORE STORIES</h4>
      <div class="cols">
{cols_html}      </div>
    </div>
  </div>

  <div class="datecheck"><b>DATE CHECK</b> &mdash; {e(datecheck)}</div>
  <footer>All 43 stories happened, or were first reported, on Thursday 19 November 2026; claims are attributed. Original drawings.<br>Sources: {e(footer_sources)}</footer>

</div>
</body>
</html>
"""
    out = os.path.join(HERE, "page.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"wrote {out}: {len(stories)} stories, regions {counts}")


if __name__ == "__main__":
    main()
