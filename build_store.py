"""Builds the static Decky store files served by GitHub Pages from plugins.json.

Decky asks a store for two things (decky-loader frontend/src/store.tsx):
  GET <base>?<query>        -> [StorePlugin]             (served as plugins/index.html)
  GET <base>/versions       -> {name: [version, sha256, artifact]}   (served as plugins/versions/index.html)
<base> is https://musika08.github.io/decky-windows-store/plugins. Pages ignores the query string.
Each version's artifact is the plugin's own GitHub release zip; Decky checks the zip against sha256 before installing.
It also writes index.html, the landing page for people at the store's root, from the site/landing.html template.
Run: python build_store.py   (from the repo root)."""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_IMG = "https://musika08.github.io/decky-windows-store/images/"

with open(os.path.join(ROOT, "plugins.json"), encoding="utf-8") as f:
    plugins = json.load(f)

store, versions = [], {}
for p in plugins:
    vers = [{"name": v["version"], "hash": v["sha256"], "artifact": v["url"]} for v in p["versions"]]
    store.append({"id": p["id"], "name": p["name"], "versions": vers, "author": p["author"],
                  "description": p["description"], "tags": p["tags"], "image_url": BASE_IMG + p["image"]})
    latest = p["versions"][0]
    versions[p["name"]] = [latest["version"], latest["sha256"], latest["url"]]

for rel, data in (("plugins/index.html", store), ("plugins/versions/index.html", versions)):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write("\n")


def repo_url(p):
    """https://github.com/<owner>/<repo>, taken from the latest version's release download URL."""
    m = re.match(r"(https://github\.com/[^/]+/[^/]+)/releases/", p["versions"][0]["url"])
    return m.group(1) if m else None


def card(p):
    """One plugin card for the landing page (site/landing.html), built from plugins.json."""
    e = html.escape
    latest = p["versions"][0]
    links = ['<a class="btn btn-primary" href="%s">Download v%s</a>' % (e(latest["url"]), e(latest["version"]))]
    repo = repo_url(p)
    if repo:
        links.insert(0, '<a class="btn btn-ghost" href="%s">GitHub</a>' % e(repo))
    tags = "".join('<span class="tag">%s</span>' % e(t) for t in p["tags"] if t != "windows")
    # The page footer has the Ko-fi button, so a trailing "Support: ..." in a store description is left off the card.
    desc = re.sub(r"\s*Support: \S+\s*$", "", p["description"])
    return ("      <article class=\"card\">\n"
            "        <img src=\"images/%s\" alt=\"%s\" width=\"920\" height=\"430\" loading=\"lazy\">\n"
            "        <div class=\"card-body\">\n"
            "          <div class=\"card-head\"><h3>%s</h3><span class=\"ver\">v%s</span></div>\n"
            "          <p class=\"desc\">%s</p>\n"
            "          <div class=\"tags\">%s</div>\n"
            "          <div class=\"links\">%s</div>\n"
            "        </div>\n"
            "      </article>") % (e(p["image"]), e(p["name"]), e(p["name"]), e(latest["version"]),
                                  e(desc), tags, "".join(links))


# The human landing page at the store's root (Decky reads only plugins/ and plugins/versions/).
with open(os.path.join(ROOT, "site", "landing.html"), encoding="utf-8") as f:
    page = f.read()
page = (page.replace("{{CARDS}}", "\n".join(card(p) for p in plugins))
            .replace("{{PLUGIN_COUNT}}", str(len(plugins)))
            .replace("{{PLUGIN_NAMES}}", html.escape(", ".join(p["name"] for p in plugins))))
with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(page)
print("wrote", len(store), "plugins and the landing page")
