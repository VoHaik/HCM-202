import urllib.request
import json
import urllib.parse
import os

endpoint = 'https://commons.wikimedia.org/w/api.php'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

queries = [
    'Ho Chi Minh Presidential Palace study',
    'Ho Chi Minh house on stilts room',
    'Ho Chi Minh desk Hanoi',
    'Presidential Palace Hanoi interior room',
    'vintage study room desk interior',
    'antique writing desk room'
]

results = []
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
                if w > h and w >= 1200:
                    results.append({
                        'title': v.get('title'),
                        'w': w,
                        'h': h,
                        'url': img_url
                    })
    except Exception as e:
        print(f"Error {q}: {e}")

print(f"Total found: {len(results)}")
for r in results:
    print(r['title'], r['w'], r['h'], r['url'])

with open('hcm_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
