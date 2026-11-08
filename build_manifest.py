# photos/ 以下の日付フォルダを読んで photos.json を作るスクリプト
# フォルダ名は 2026-11-09 / 2026.11.09 / 20261109 のどれでもOK
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(ROOT, "photos")
EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif"}
pat = re.compile(r"^(\d{4})[-.]?(\d{2})[-.]?(\d{2})")

days = []
if os.path.isdir(PHOTOS):
    for name in os.listdir(PHOTOS):
        m = pat.match(name)
        folder = os.path.join(PHOTOS, name)
        if not m or not os.path.isdir(folder):
            continue
        files = sorted(
            f for f in os.listdir(folder)
            if os.path.splitext(f)[1].lower() in EXTS
        )
        if files:
            days.append({
                "key": "".join(m.groups()),
                "date": ".".join(m.groups()),
                "photos": [f"photos/{name}/{f}" for f in files],
            })

days.sort(key=lambda d: d["key"], reverse=True)
for d in days:
    d.pop("key")

with open(os.path.join(ROOT, "photos.json"), "w", encoding="utf-8") as fp:
    json.dump(days, fp, ensure_ascii=False, indent=1)

print(f"{len(days)} days, {sum(len(d['photos']) for d in days)} photos")
