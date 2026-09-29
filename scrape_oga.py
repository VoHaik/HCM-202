import urllib.request
import re

url = 'https://opengameart.org/content/visual-novel-house-backgrounds'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        links = re.findall(r'href="(https://opengameart.org/sites/default/files/[^"]+\.(?:png|jpg))"', html)
        print('Links found:', len(links))
        for l in links[:5]:
            print(l)
except Exception as e:
    print('Error:', e)
