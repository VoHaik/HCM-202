import urllib.request
import re

url = 'https://stockcake.com/search?q=detective+office'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        imgs = re.findall(r'https://images\.stockcake\.com/public/[^"]+\.jpg', html)
        print('Found StockCake images:', len(imgs))
        for img in set(imgs)[:10]:
            print(img)
except Exception as e:
    print('Error:', e)
