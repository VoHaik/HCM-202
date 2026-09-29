import urllib.request
import json
import os

with open('hcm_candidates.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
os.makedirs('hcm_rooms', exist_ok=True)

downloaded = []
seen = set()
for item in items:
    url = item['url']
    if url in seen:
        continue
    seen.add(url)
    
    # Use Wikimedia thumbnail at 2560px for fast, high-quality loading
    # e.g. https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Humble_interior_of_Uncle_Ho%27s_wooden_house_%2831083384310%29.jpg/2560px-Humble_interior_of_Uncle_Ho%27s_wooden_house_%2831083384310%29.jpg
    filename = f"hcm_room_{len(downloaded)+1}.jpg"
    filepath = os.path.join('hcm_rooms', filename)
    print(f"Downloading {item['title']} to {filename}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp, open(filepath, 'wb') as out:
            out.write(resp.read())
        downloaded.append({
            'filename': filename,
            'filepath': filepath,
            'title': item['title'],
            'w': item['w'],
            'h': item['h']
        })
    except Exception as e:
        print(f"Failed {filename}: {e}")

print("Downloaded", len(downloaded))
