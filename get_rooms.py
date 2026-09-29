import urllib.request
import json
import urllib.parse
import os

endpoint = 'https://commons.wikimedia.org/w/api.php'
headers = {'User-Agent': 'EscapeRoomEdu/1.0 (contact: student@edu.vn)'}

queries = [
    'antique study room desk',
    'Victorian study room interior',
    'vintage library desk bookshelves',
    'cabinet of curiosities interior',
    'classic study room mahogany'
]

os.makedirs('room_candidates', exist_ok=True)
downloaded = []
seen = set()

for q in queries:
    params = {
        'action': 'query',
        'format': 'json',
        'generator': 'search',
        'gsrsearch': q,
        'gsrnamespace': '6',
        'gsrlimit': '10',
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
                if w > h and w >= 1600 and title not in seen:
                    seen.add(title)
                    # Convert to 1920px thumbnail URL
                    # e.g. https://upload.wikimedia.org/wikipedia/commons/a/b/File.jpg -> https://upload.wikimedia.org/wikipedia/commons/thumb/a/b/File.jpg/1920px-File.jpg
                    parts = img_url.split('/commons/')
                    if len(parts) == 2:
                        sub = parts[1].split('?')[0]
                        filename = os.path.basename(sub)
                        thumb_url = f"https://upload.wikimedia.org/wikipedia/commons/thumb/{sub}/1920px-{filename}"
                        
                        save_name = f"candidate_{len(downloaded)+1}.jpg"
                        save_path = os.path.join('room_candidates', save_name)
                        try:
                            treq = urllib.request.Request(thumb_url, headers=headers)
                            with urllib.request.urlopen(treq) as tresp, open(save_path, 'wb') as out:
                                out.write(tresp.read())
                            downloaded.append({
                                'id': len(downloaded)+1,
                                'file': save_name,
                                'title': title,
                                'w': w,
                                'h': h
                            })
                            print(f"Downloaded {save_name}: {title}")
                        except Exception as e:
                            # fallback to direct
                            try:
                                dreq = urllib.request.Request(img_url, headers=headers)
                                with urllib.request.urlopen(dreq) as dresp, open(save_path, 'wb') as out:
                                    out.write(dresp.read())
                                downloaded.append({
                                    'id': len(downloaded)+1,
                                    'file': save_name,
                                    'title': title,
                                    'w': w,
                                    'h': h
                                })
                                print(f"Downloaded {save_name} via direct: {title}")
                            except Exception as e2:
                                print(f"Failed {title}: {e2}")
                if len(downloaded) >= 8:
                    break
    except Exception as e:
        print(f"Error {q}: {e}")
    if len(downloaded) >= 8:
        break

print(f"Done! {len(downloaded)} candidates downloaded.")
with open('room_candidates/info.json', 'w', encoding='utf-8') as f:
    json.dump(downloaded, f, indent=2)
