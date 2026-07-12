"""
Build a neofetch-style info card SVG to sit to the RIGHT of
the ASCII portrait: colored key/value rows for OS, Uptime, Host, etc.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 540, 490
PAD = 10
KEY_X = PAD
VAL_X = PAD + 190
LINE_H = 20.5

BG = "#0d1117"
BG2 = "#0d1117"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
KEY = "#ffa657"      # orange keys
GREEN = "#3fb950"
ACCENT = "#22d3ee"

# ===========================================================================
#  EDIT THIS
# ===========================================================================
USER = "Aswin Kumar Reddy Koothedhula"
DOMAIN = "buildwithash.dev"
GH_USERNAME = "ASH274946"

def fetch_github_stats(username):
    stats = {"repos": 0, "stars": 0, "followers": 0, "contributions": 0}
    try:
        import requests
        import json
        # User details
        u_resp = requests.get(f"https://api.github.com/users/{username}", timeout=5)
        if u_resp.status_code == 200:
            d = u_resp.json()
            stats["repos"] = d.get("public_repos", 0)
            stats["followers"] = d.get("followers", 0)
        # Stars (summing from up to 100 recent repos)
        r_resp = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100", timeout=5)
        if r_resp.status_code == 200:
            stats["stars"] = sum(r.get("stargazers_count", 0) for r in r_resp.json() if not r.get("fork", False))
        # Contributions (from fetch_contributions.py data)
        c_path = os.path.join(HERE, "..", "data", "contributions.json")
        if os.path.exists(c_path):
            with open(c_path, "r") as f:
                stats["contributions"] = json.load(f).get("total_contributions", 0)
    except Exception as e:
        print(f"Stats fetch failed: {e}")
    return stats

gh_stats = fetch_github_stats(GH_USERNAME)

ROWS = [
    ("host",),
    ("kv", "Role:", "AI-native Builder & Full-stack Dev"),
    ("kv", "Education:", "B.Tech CSE (AI & ML) @ St. Peter's"),
    ("kv", "Stack.AI:", "LangChain, ChromaDB, OpenAI, Gemini"),
    ("kv", "Stack.Web:", "Next.js, React, Node.js, FastAPI, Flutter"),
    ("kv", "Cloud/DB:", "GCP, Firebase, Supabase, MongoDB, SQLite"),
    ("gap",),
    ("kv", "Languages.Programming:", "Python, TypeScript, JavaScript, Dart"),
    ("kv", "Languages.Computer:", "HTML, CSS, SQL, JSON"),
    ("kv", "Languages.Real:", "English, Telugu"),
    ("gap",),
    ("kv", "Tools.Product:", "Figma, Notion, Streamlit, Stitch"),
    ("kv", "Tools.Dev:", "GitHub, Vercel, Google Cloud, Antigravity"),
    ("gap",),
    ("sec", "Contact"),
    ("kv", "Email.Personal:", "Koothedhulaa@gmail.com"),
    ("kv", "Portfolio:", "portfolio.buildwithash.dev"),
    ("kv", "LinkedIn:", "ash274946"),
    ("kv", "GitHub:", "ASH274946"),
    ("gap",),
    ("sec", "GitHub Stats"),
    ("kv", "Repos:", f"{gh_stats['repos']} | Stars: {gh_stats['stars']}"),
    ("kv", "Followers:", f"{gh_stats['followers']} | Contr. (1 Yr): {gh_stats['contributions']}"),
]

def esc(s):
    return html.escape(s)

def rise(inner, i):
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.15 + i * 0.06
    return (f'<g opacity="0" transform="translate(0,5)">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" '
            f'begin="{delay:.2f}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>')

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>'
    f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.55"/>',
    f'<line x1="0" y1="30" x2="{W}" y2="30" stroke="{FRAME}" stroke-opacity="0.35"/>',
]

for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{22 + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

y = 45
for i, row in enumerate(ROWS):
    kind = row[0]
    if kind == "gap":
        y += LINE_H * 0.6
        continue
    if kind == "host":
        user = esc(USER)
        domain = esc(DOMAIN)
        rule_x = KEY_X + (len(USER) + len(DOMAIN) + 1) * 8 + 20
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" font-size="14" font-weight="700">'
                 f'<tspan fill="{GREEN}">{user}</tspan><tspan fill="{MUTED}">@</tspan>'
                 f'<tspan fill="{ACCENT}">{domain}</tspan></text>'
                 f'<line x1="{rule_x}" y1="{y-4:.1f}" x2="{W-PAD-10}" y2="{y-4:.1f}" '
                 f'stroke="{FRAME}" stroke-dasharray="4 4" stroke-opacity="0.8"/>')
    elif kind == "sec":
        title = esc(row[1])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{INK}" font-size="12.5" font-weight="700">'
                 f'- {title}</text>'
                 f'<line x1="{KEY_X + 16 + len(row[1])*7.5 + 4}" y1="{y-4:.1f}" x2="{W-PAD-10}" y2="{y-4:.1f}" '
                 f'stroke="{FRAME}" stroke-dasharray="4 4" stroke-opacity="0.8"/>')
    elif kind == "kv":
        key, val = esc(row[1]), esc(row[2])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY}" font-size="12.5">{key}</text>'
                 f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="12.5">{val}</text>')
    else:
        continue
    parts.append(rise(inner, i))
    y += LINE_H

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes;", W, "x", H, "content_bottom", round(y))
