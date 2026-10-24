"""Builds the static Decky store files served by GitHub Pages from plugins.json.

Decky asks a store for two things (decky-loader frontend/src/store.tsx):
  GET <base>?<query>        -> [StorePlugin]             (served as plugins/index.html)
  GET <base>/versions       -> {name: [version, sha256, artifact]}   (served as plugins/versions/index.html)
<base> is https://musika08.github.io/decky-windows-store/plugins. Pages ignores the query string.
Each version's artifact is the plugin's own GitHub release zip; Decky checks the zip against sha256 before installing.
Run: python build_store.py   (from the repo root)."""
import json
import os

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
print("wrote", len(store), "plugins")
