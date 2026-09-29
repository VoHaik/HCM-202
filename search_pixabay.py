import urllib.request
import json
import re

url = 'https://pixabay.com/images/search/escape%20room/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        # Find CDN image links
        imgs = re.findall(r'https://cdn\.pixabay\.com/photo/[^"]+\.jpg', html)
        print('Found pixabay images:', len(imgs))
        for img in set(imgs)[:10]:
            print(img)
except Exception as e:
    print('Error:', e)
