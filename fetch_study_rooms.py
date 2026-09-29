import urllib.request
import json
import urllib.parse
import os

endpoint = 'https://commons.wikimedia.org/w/api.php'

queries = [
    'Sherlock Holmes study Baker Street',
    'Victorian study room desk',
    'antique study interior desk bookshelf',
    'vintage study room desk library',
    'escape room game room',
    'detective study room desk'
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

candidates = []
for q in queries:
    params = {
        'action': 'query',
        'format': 'json',
        'generator': 'search',
        'gsrsearch': q,
        'gsrnamespace': '6',
        'gsrlimit': '15',
        'prop': 'imageinfo',
        'iiprop': 'url|size|mime'
    }
    try:
        url = f"{endpoint}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for k, v in data.get('query', {}).get('pages', {}).items():
                ii = v.get('imageinfo', [{}])[0]
                w = ii.get('width', 0)
                h = ii.get('height', 0)
                img_url = ii.get('url', '')
                mime = ii.get('mime', '')
                if 'image' in mime and w > h and w >= 1200 and not any(bad in img_url.lower() for bad in ['.svg', '.tif', '.pdf']):
                    candidates.append({
                        'title': v.get('title'),
                        'w': w,
                        'h': h,
                        'url': img_url
                    })
    except Exception as e:
        print(f"Error {q}: {e}")

print(f"Found {len(candidates)} candidates.")
os.makedirs('downloaded_rooms', exist_ok=True)

# Download top 6 distinct candidates
downloaded = []
seen_titles = set()
for c in candidates:
    if c['title'] in seen_titles:
        continue
    seen_titles.add(c['title'])
    
    ext = os.path.splitext(c['url'].split('?')[0])[1] or '.jpg'
    filename = f"room_{len(downloaded)+1}{ext}"
    filepath = os.path.join('downloaded_rooms', filename)
    print(f"Downloading {c['title']} ({c['w']}x{c['h']}) to {filename}...")
    try:
        req = urllib.request.Request(c['url'], headers=headers)
        with urllib.request.urlopen(req) as resp, open(filepath, 'wb') as f:
            f.write(resp.read())
        downloaded.append({
            'filename': filename,
            'filepath': filepath,
            'title': c['title'],
            'w': c['w'],
            'h': c['h']
        })
    except Exception as err:
        print(f"Failed {c['title']}: {err}")
    if len(downloaded) >= 6:
        break

with open('downloaded_rooms/manifest.json', 'w', encoding='utf-8') as f:
    json.dump(downloaded, f, indent=2)
print("Done! Downloaded:", len(downloaded))
