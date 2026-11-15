"""Builds animated wave banners + project cards into ./assets (no external services).
Edit PROJECTS below (set the real repo name), then run:  python3 tools/build_assets.py
"""
import os
import textwrap
from html import escape

USER = "AAYUSHTYAGI0"

# (display name, repo name, description, tags, (color1, color2))
PROJECTS = [
    ("AURA", "AURA", "Social media platform concept in React with live Claude API calls", ["React", "Claude API"], ("22d3ee", "a78bfa")),
    ("ExpertEdge", "ExpertEdge", "Marketplace for paid consultations with retired professionals", ["React Native"], ("f472b6", "fb923c")),
    ("MEMORY AI", "MEMORY-AI", "Searchable personal memory app on Supabase + Gemini File Search", ["Supabase", "Gemini"], ("34d399", "22d3ee")),
    ("LaptopIQ", "LaptopIQ", "Laptop discovery and recommendation platform", ["Discovery", "Recommendations"], ("fbbf24", "f97316")),
    ("MindCraft AI", "MindCraft-AI", "Gemini-powered study tool generator", ["Gemini", "Study tools"], ("a78bfa", "f472b6")),
    ("Stock Council AI", "Stock-Council-AI", "Multi-agent investment analysis platform", ["Multi-agent", "AI"], ("60a5fa", "34d399")),
    ("VaultMind", "VaultMind", "Local-first Android personal digital vault", ["Android", "Local-first"], ("f87171", "a78bfa")),
]
MORE = ("More on GitHub", None, "Every repository, experiment and work in progress", ["All repos"], ("94a3b8", "e2e8f0"))

CARD_CSS = """text{font-family:'Segoe UI',Ubuntu,Arial,sans-serif}
.in{animation:in .7s ease-out backwards}
@keyframes in{from{opacity:0;transform:translateY(12px)}}
.sweep{animation:sw 4.5s linear infinite}
@keyframes sw{0%{transform:translateX(0)}60%,100%{transform:translateX(580px)}}
.glow{animation:gl 4s ease-in-out infinite alternate}
@keyframes gl{from{opacity:.07}to{opacity:.16}}"""


def card(name, desc, tags, c1, c2, cta):
    initials = "".join(w[0] for w in name.split()[:2]).upper() if " " in name else name[:2].upper()
    lines = textwrap.wrap(desc, 46)[:2]
    desc_svg = "".join(
        f'<text x="92" y="{70 + 18 * i}" font-size="13" fill="#94a3b8">{escape(l)}</text>' for i, l in enumerate(lines)
    )
    x, chips = 24, ""
    for t in tags:
        w = int(len(t) * 7.2 + 22)
        chips += (
            f'<rect x="{x}" y="108" width="{w}" height="26" rx="13" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".18"/>'
            f'<text x="{x + w / 2}" y="125.5" font-size="12" fill="#e2e8f0" text-anchor="middle">{escape(t)}</text>'
        )
        x += w + 8
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 150" width="440" height="150" role="img" aria-label="{escape(name)}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f1730"/><stop offset="1" stop-color="#170c36"/></linearGradient>
<linearGradient id="ac" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#{c1}"/><stop offset="1" stop-color="#{c2}"/></linearGradient>
<linearGradient id="sg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#{c1}" stop-opacity="0"/><stop offset=".5" stop-color="#{c1}"/><stop offset="1" stop-color="#{c2}" stop-opacity="0"/></linearGradient>
<clipPath id="cp"><rect x="1" y="1" width="438" height="148" rx="16"/></clipPath>
</defs>
<style>{CARD_CSS}</style>
<g class="in">
<rect x="1" y="1" width="438" height="148" rx="16" fill="url(#bg)"/>
<g clip-path="url(#cp)"><circle class="glow" cx="400" cy="20" r="80" fill="#{c1}" opacity=".1"/></g>
<g clip-path="url(#cp)"><rect class="sweep" x="-140" y="0" width="140" height="3" fill="url(#sg)"/></g>
<rect x="1" y="1" width="438" height="148" rx="16" fill="none" stroke="url(#ac)" stroke-opacity=".55" stroke-width="1.2"/>
<rect x="24" y="26" width="52" height="52" rx="14" fill="url(#ac)"/>
<text x="50" y="60" font-size="20" font-weight="800" fill="#0b1020" text-anchor="middle">{escape(initials)}</text>
<text x="92" y="46" font-size="20" font-weight="800" fill="#fff">{escape(name)}</text>
{desc_svg}
{chips}
<text x="416" y="125.5" font-size="12" font-weight="600" fill="#{c1}" text-anchor="end">{escape(cta)}</text>
</g>
</svg>
"""


def wave_path(base, amp):
    p, x = f"M0,{base} ", 0
    for _ in range(4):
        p += f"C{x + 150},{base - amp} {x + 300},{base + amp} {x + 450},{base} "
        x += 450
    return p + "V120 H0Z"


def wave(flip):
    layers = [(60, 16, .30, "18s", "", 0), (72, 12, .45, "12s", "reverse", -4), (84, 9, .85, "9s", "", -2)]
    paths = "".join(
        f'<path class="w" d="{wave_path(b, a)}" fill="url(#g)" opacity="{o}" style="animation-duration:{d};animation-direction:{r or "normal"};animation-delay:{dl}s"/>'
        for b, a, o, d, r, dl in layers
    )
    body = f'<g transform="translate(0,120) scale(1,-1)">{paths}</g>' if flip else paths
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 120" preserveAspectRatio="none" width="900" height="120" role="img" aria-label="wave">
<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="900" y2="0" spreadMethod="repeat"><stop offset="0" stop-color="#22d3ee"/><stop offset=".5" stop-color="#a78bfa"/><stop offset="1" stop-color="#22d3ee"/></linearGradient></defs>
<style>.w{{animation:mv 12s linear infinite}}@keyframes mv{{to{{transform:translateX(-900px)}}}}</style>
{body}
</svg>
"""


def main():
    os.makedirs("assets/projects", exist_ok=True)
    for flip, fn in ((True, "wave-top.svg"), (False, "wave-bottom.svg")):
        open(f"assets/{fn}", "w").write(wave(flip))
    md = []
    for name, repo, desc, tags, (c1, c2) in PROJECTS + [MORE]:
        slug = (repo or "more").lower()
        open(f"assets/projects/{slug}.svg", "w").write(card(name, desc, tags, c1, c2, "View repo  \u2192" if repo else "Browse all  \u2192"))
        url = f"https://github.com/{USER}/{repo}" if repo else f"https://github.com/{USER}?tab=repositories"
        md.append(f'<a href="{url}"><img src="./assets/projects/{slug}.svg" width="49%" alt="{escape(name)}"/></a>')
    print("\n".join(md))


if __name__ == "__main__":
    main()
