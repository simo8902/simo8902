import requests, os

token = os.environ["GITHUB_TOKEN"]
headers = {"Authorization": f"Bearer {token}"}

repos = requests.get("https://api.github.com/users/simo8902/repos?per_page=100", headers=headers).json()

langs = {}
for r in repos:
    if r.get("fork"):
        continue
    l = requests.get(r["languages_url"], headers=headers).json()
    for k, v in l.items():
        langs[k] = langs.get(k, 0) + v

total = sum(langs.values()) or 1
svg = "<svg xmlns='http://www.w3.org/2000/svg' width='600' height='200'>"
y = 20
for k, v in sorted(langs.items(), key=lambda x: -x[1]):
    pct = round(v / total * 100, 2)
    svg += f"<text x='10' y='{y}' font-size='16'>{k}: {pct}%</text>"
    y += 20
svg += "</svg>"

open("langs.svg", "w").write(svg)