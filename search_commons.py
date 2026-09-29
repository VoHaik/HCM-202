import urllib.request
import json
import urllib.parse

def search_commons(query):
    endpoint = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}",
        "gsrlimit": 10,
        "prop": "imageinfo",
        "iiprop": "url|size|extmetadata"
    }
    url = f"{endpoint}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "EscapeRoomApp/1.0 (edu test)"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        pages = data.get("query", {}).get("pages", {})
        results = []
        for pid, page in pages.items():
            ii = page.get("imageinfo", [{}])[0]
            w = ii.get("width", 0)
            h = ii.get("height", 0)
            img_url = ii.get("url")
            title = page.get("title")
            if w > h and w >= 1600 and any(img_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                results.append({"title": title, "width": w, "height": h, "url": img_url})
        return results

queries = [
    "antique library room desk",
    "historical study room interior",
    "cabinet of curiosities room",
    "old library interior bookshelves desk",
    "vintage office interior"
]

all_imgs = []
for q in queries:
    res = search_commons(q)
    print(f"Query '{q}': {len(res)} matches")
    all_imgs.extend(res)

print("--- Top candidates ---")
for i, item in enumerate(all_imgs[:10]):
    print(f"{i}: {item['title']} ({item['width']}x{item['height']}) -> {item['url']}")

with open("commons_candidates.json", "w", encoding="utf-8") as f:
    json.dump(all_imgs, f, indent=2)
