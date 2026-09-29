import urllib.request
import json
import os

queries = [
    'antique-study-room',
    'vintage-library',
    'detective-office',
    'mystery-room',
    'dark-academia-study'
]

results = []
for q in queries:
    url = f'https://unsplash.com/napi/search/photos?query={q}&per_page=10'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for item in data.get('results', []):
                urls = item.get('urls', {})
                desc = item.get('alt_description') or item.get('description') or ''
                width = item.get('width', 0)
                height = item.get('height', 0)
                # Landscape only
                if width > height and (urls.get('full') or urls.get('regular')):
                    results.append({
                        'id': item.get('id'),
                        'desc': desc,
                        'width': width,
                        'height': height,
                        'regular': urls.get('regular'),
                        'full': urls.get('full') or urls.get('regular')
                    })
    except Exception as e:
        print(f"Error {q}: {e}")

print(f"Total found: {len(results)}")
for i, r in enumerate(results[:15]):
    print(f"{i}: [{r['id']}] {r['desc'][:60]} ({r['width']}x{r['height']}) -> {r['regular']}")

with open('scratch_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
