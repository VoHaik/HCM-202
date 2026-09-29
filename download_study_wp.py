import urllib.request
import re
import os

os.makedirs('wallpapers_study', exist_ok=True)
pages = [
    'https://wallpaperaccess.com/study-room',
    'https://wallpaperaccess.com/antique-library',
    'https://wallpaperaccess.com/vintage-library',
    'https://wallpaperaccess.com/old-library',
    'https://wallpaperaccess.com/dark-academia'
]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

downloaded = []
for p in pages:
    try:
        req = urllib.request.Request(p, headers=headers)
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            imgs = re.findall(r'src="(/full/[^"]+)"', html)
            print(p, 'found:', len(imgs))
            for img in imgs[:4]:
                img_url = 'https://wallpaperaccess.com' + img
                dest = f"wallpapers_study/study_{len(downloaded)+1}.jpg"
                try:
                    ireq = urllib.request.Request(img_url, headers=headers)
                    with urllib.request.urlopen(ireq) as iresp, open(dest, 'wb') as f:
                        f.write(iresp.read())
                    downloaded.append(dest)
                    print("Saved", dest)
                except Exception as err:
                    pass
                if len(downloaded) >= 12:
                    break
    except Exception as e:
        print("Failed page", p, e)
    if len(downloaded) >= 12:
        break

print("Total saved:", len(downloaded))
