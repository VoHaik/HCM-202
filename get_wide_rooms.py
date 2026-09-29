import urllib.request
import json
import urllib.parse
import os

endpoint = 'https://commons.wikimedia.org/w/api.php'
headers = {'User-Agent': 'EscapeRoomEdu/1.0 (contact: student@edu.vn)'}

queries = [
    'Victorian study room interior fireplace',
    'library reading room wood interior',
    'antique study bookshelves globe desk',
    'historic office interior wood paneling',
    'private library study interior'
]

os.makedirs('room_wide', exist_ok=True)
downloaded = []
seen = set()

for q in queries:
    params = {
        'action': 'query',
        'format': 'json',
        'generator': 'search',
        'gsrsearch': q,
        'gsrnamespace': '6',
        'gsrlimit': '8',
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
                title = v.get('title', '')
                # Looking for landscape, aspect ratio ~ 1.3 to 1.8 (w/h)
                aspect = w / h if h else 0
                if 1.25 <= aspect <= 1.85 and w >= 2000 and title not in seen:
                    seen.add(title)
                    parts = img_url.split('/commons/')
                    if len(parts) == 2:
                        sub = parts[1].split('?')[0]
                        filename = os.path.basename(sub)
                        thumb_url = f"https://upload.wikimedia.org/wikipedia/commons/thumb/{sub}/1920px-{filename}"
                        
                        save_name = f"wide_{len(downloaded)+1}.jpg"
                        save_path = os.path.join('room_wide', save_name)
                        try:
                            treq = urllib.request.Request(thumb_url, headers=headers)
                            with urllib.request.urlopen(treq) as tresp, open(save_path, 'wb') as out:
                                out.write(tresp.read())
                            downloaded.append({
                                'id': len(downloaded)+1,
                                'file': save_name,
                                'title': title,
                                'w': w,
                                'h': h,
                                'aspect': round(aspect, 2)
                            })
                            print(f"Downloaded {save_name}: {title} (aspect {aspect:.2f})")
                        except Exception as e:
                            pass
                if len(downloaded) >= 6:
                    break
    except Exception as e:
        print(f"Error {q}: {e}")
    if len(downloaded) >= 6:
        break

print(f"Done! {len(downloaded)} wide rooms downloaded.")
with open('room_wide/manifest.json', 'w', encoding='utf-8') as f:
    json.dump(downloaded, f, indent=2)
