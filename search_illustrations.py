import urllib.request
import json

queries = [
    'category:Rooms_in_art',
    'category:Interior_illustrations',
    'office+interior+drawing',
    'study+room+illustration',
    'room+vector'
]

for q in queries:
    url = f'https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={q}&gsrnamespace=6&gsrlimit=10&prop=imageinfo&iiprop=url|size&format=json'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            for pid, p in pages.items():
                title = p.get('title')
                ii = p.get('imageinfo', [{}])[0]
                url = ii.get('url')
                w, h = ii.get('width', 0), ii.get('height', 0)
                if w and w > 1200 and ('jpg' in url or 'png' in url or 'svg' in url):
                    print(f'{title} ({w}x{h}): {url}')
    except Exception as e:
        print(f'Error for {q}: {e}')
