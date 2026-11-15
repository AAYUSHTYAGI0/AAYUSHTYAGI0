"""Generates assets/stats.svg straight from the GitHub API (no third-party servers).
Runs in GitHub Actions with the built-in GITHUB_TOKEN; also works locally without a token
(then the contribution chart is skipped).
"""
import datetime
import json
import os
import urllib.request
from html import escape

USER = os.environ.get("GH_USER", "AAYUSHTYAGI0")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.environ.get("OUT", "assets/stats.svg")


def call(url, data=None):
    h = {"Accept": "application/vnd.github+json", "User-Agent": "profile-stats"}
    if TOKEN:
        h["Authorization"] = "Bearer " + TOKEN
    if data:
        h["Content-Type"] = "application/json"
    with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=h), timeout=30) as r:
        return json.load(r)


try:
    user = call(f"https://api.github.com/users/{USER}")
    repos = [r for r in call(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner") if not r["fork"]]
except Exception as e:
    print("GitHub API unavailable:", e)
    if os.path.exists(OUT):
        raise SystemExit(0)  # keep the last good card
    user, repos = None, []  # first run: draw an empty card
stars = sum(r["stargazers_count"] for r in repos) if user else None

langs = {}
for r in repos[:40]:
    try:
        for k, v in call(r["languages_url"]).items():
            langs[k] = langs.get(k, 0) + v
    except Exception as e:  # keep going if one repo fails
        print("languages skipped:", r["name"], e)

days, commits, total = [], None, None
if TOKEN:
    try:
        q = ('{user(login:"%s"){contributionsCollection{totalCommitContributions '
             'contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}' % USER)
        d = call("https://api.github.com/graphql", json.dumps({"query": q}).encode())["data"]["user"]["contributionsCollection"]
        commits = d["totalCommitContributions"]
        total = d["contributionCalendar"]["totalContributions"]
        days = [x["contributionCount"] for w in d["contributionCalendar"]["weeks"] for x in w["contributionDays"]][-60:]
    except Exception as e:
        print("graphql skipped:", e)

LANG_COLORS = {"JavaScript": "f1e05a", "TypeScript": "3178c6", "Python": "3572A5", "HTML": "e34c26", "CSS": "563d7c",
               "Dart": "00B4AB", "Kotlin": "A97BFF", "Java": "b07219", "Shell": "89e051", "C++": "f34b7d",
               "C": "888888", "Swift": "F05138", "Jupyter Notebook": "DA5B0B", "PLpgSQL": "336790"}
FALLBACK = ["22d3ee", "a78bfa", "f472b6", "fbbf24", "34d399", "60a5fa"]

tiles = [("STARS EARNED", stars), ("REPOSITORIES", user and user["public_repos"]), ("FOLLOWERS", user and user["followers"]),
         ("CONTRIBUTIONS \u00b7 1Y", total) if total is not None else ("FOLLOWING", user and user["following"])]
tile_svg = ""
for i, (label, val) in enumerate(tiles):
    x = 40 + i * 210
    tile_svg += (
        f'<g class="in" style="animation-delay:{i * 120}ms">'
        f'<rect x="{x}" y="72" width="190" height="82" rx="14" fill="#fff" fill-opacity=".05" stroke="#fff" stroke-opacity=".12"/>'
        f'<text x="{x + 20}" y="116" font-size="36" font-weight="800" fill="url(#acc)">{f"{val:,}" if isinstance(val, int) else "\u2014"}</text>'
        f'<text x="{x + 20}" y="138" font-size="11" fill="#94a3b8" letter-spacing="2">{label}</text></g>'
    )

tot = sum(langs.values())
top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]
bar_svg, legend_svg = "", ""
if top:
    x = 40.0
    for i, (name, b) in enumerate(top):
        w = 820 * b / tot
        col = LANG_COLORS.get(name, FALLBACK[i % len(FALLBACK)])
        bar_svg += f'<rect x="{x:.1f}" y="206" width="{w:.1f}" height="14" fill="#{col}"/>'
        lx = 40 + i * 164
        legend_svg += (f'<circle cx="{lx + 5}" cy="244" r="5" fill="#{col}"/>'
                       f'<text x="{lx + 16}" y="248" font-size="13" fill="#e2e8f0">{escape(name)} <tspan fill="#94a3b8">{100 * b / tot:.0f}%</tspan></text>')
        x += w
else:
    legend_svg = '<text x="40" y="244" font-size="13" fill="#94a3b8">Language data appears after your first public repos.</text>'

bars = ""
if days:
    mx = max(days) or 1
    for i, c in enumerate(days):
        h = max(3, round(c / mx * 52)) if c else 3
        extra = 'fill="url(#acc)"' if c else 'fill="#fff" fill-opacity=".12"'
        bars += f'<rect class="b" x="{40 + i * 13.7:.1f}" y="{346 - h}" width="11" height="{h}" rx="2" {extra} style="animation-delay:{i * 12}ms"/>'
    bars_title = "LAST 60 DAYS"
else:
    bars_title = "ACTIVITY \u00b7 loads on the next scheduled run"

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 366" width="900" height="366" role="img" aria-label="GitHub stats for {escape(USER)}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#150a30"/></linearGradient>
<linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#22d3ee"/><stop offset="1" stop-color="#a78bfa"/></linearGradient>
<clipPath id="lc"><rect x="40" y="206" width="820" height="14" rx="7"/></clipPath>
</defs>
<style>
text{{font-family:'Segoe UI',Ubuntu,Arial,sans-serif}}
.in{{animation:in .7s ease-out backwards}}
@keyframes in{{from{{opacity:0;transform:translateY(10px)}}}}
.b{{transform-box:fill-box;transform-origin:50% 100%;animation:grow .7s ease-out backwards}}
@keyframes grow{{from{{transform:scaleY(0)}}}}
</style>
<rect width="900" height="366" rx="20" fill="url(#bg)"/>
<rect width="900" height="366" rx="20" fill="none" stroke="#fff" stroke-opacity=".08"/>
<text x="40" y="46" font-size="13" font-weight="700" fill="#22d3ee" letter-spacing="4">GITHUB PULSE</text>
<text x="860" y="46" font-size="12" fill="#64748b" text-anchor="end">@{escape(USER)} \u00b7 updated {datetime.date.today().isoformat()}</text>
{tile_svg}
<text x="40" y="192" font-size="11" fill="#94a3b8" letter-spacing="3">TOP LANGUAGES</text>
<g clip-path="url(#lc)"><rect x="40" y="206" width="820" height="14" fill="#fff" fill-opacity=".08"/>{bar_svg}</g>
{legend_svg}
<text x="40" y="282" font-size="11" fill="#94a3b8" letter-spacing="3">{bars_title}</text>
{bars}
</svg>
"""
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write(svg)
print("wrote", OUT, "| repos:", len(repos), "| langs:", [n for n, _ in top], "| days:", len(days))
