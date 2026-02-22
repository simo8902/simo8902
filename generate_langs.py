import requests, os

USERNAME = "simo8902"
token = os.environ["GITHUB_TOKEN"]
headers = {"Authorization": f"Bearer {token}"}

repos = []
page = 1
while True:
    r = requests.get(
        f"https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}",
        headers=headers
    ).json()
    if not r:
        break
    repos.extend(r)
    page += 1

langs = {}
for repo in repos:
    if repo.get("fork"):
        continue
    l = requests.get(repo["languages_url"], headers=headers).json()
    for k, v in l.items():
        langs[k] = langs.get(k, 0) + v

total = sum(langs.values()) or 1

height = 20 + len(langs) * 20
svg = f"<svg xmlns='http://www.w3.org/2000/svg' width='600' height='{height}'>"
y = 20

for k, v in sorted(langs.items(), key=lambda x: -x[1]):
    pct = round(v / total * 100, 2)
    svg += f"<text x='10' y='{y}' font-size='16'>{k}: {pct}%</text>"
    y += 20

svg += "</svg>"

with open("langs.svg", "w") as f:
    f.write(svg)