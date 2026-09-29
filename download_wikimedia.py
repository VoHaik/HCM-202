import urllib.request

urls = [
    ('illuminated_study.jpg', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Illuminated_study_room.JPG/1280px-Illuminated_study_room.JPG'),
    ('casa_loma.jpg', 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Casa_Loma_July_2010_17_%28Sir_Pellatt%27s_Study%29.JPG/1280px-Casa_Loma_July_2010_17_%28Sir_Pellatt%27s_Study%29.JPG'),
    ('peterhof.jpg', 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Peterhof_interior_scienceroom_20021011.jpg/1280px-Peterhof_interior_scienceroom_20021011.jpg')
]

for name, url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'})
    try:
        with urllib.request.urlopen(req) as resp, open('assets/' + name, 'wb') as f:
            f.write(resp.read())
        print('Downloaded', name)
    except Exception as e:
        print('Error', name, e)
