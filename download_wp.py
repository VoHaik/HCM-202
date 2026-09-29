import urllib.request
import re
import os

os.makedirs('wallpapers_test', exist_ok=True)
urls_to_try = [
    'https://wallpaperaccess.com/detective-office',
    'https://wallpaperaccess.com/vintage-study',
    'https://wallpaperaccess.com/escape-room'
]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

saved = 0
for u in urls_to_try:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            imgs = re.findall(r'src="(/full/[^"]+)"', html)
            print(u, 'found:', len(imgs))
            for img in imgs:
                img_url = 'https://wallpaperaccess.com' + img
                ext = os.path.splitext(img)[1] or '.jpg'
                dest = f'wallpapers_test/wp_{saved+1}{ext}'
                try:
                    ireq = urllib.request.Request(img_url, headers=headers)
                    with urllib.request.urlopen(ireq) as iresp, open(dest, 'wb') as f:
                        f.write(iresp.read())
                    saved += 1
                    print('Saved:', dest, 'from', img_url)
                except Exception as err:
                    print('Failed img:', err)
                if saved >= 8:
                    break
    except Exception as e:
        print('Error', u, e)
    if saved >= 8:
        break

print('Total saved:', saved)
