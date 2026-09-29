from PIL import Image, ImageDraw, ImageFilter

im = Image.open('assets/room_pristine.png').convert('RGB')
draw = ImageDraw.Draw(im)

# 1. Clean the Desk Front completely (x: 0 to 230, y: 440 to 625)
# Draw an authentic dark mahogany executive desk
# Desk top overhang shadow:
draw.rectangle([(0, 435), (230, 445)], fill=(45, 22, 10))

# Left drawer pedestal: x: 0 to 140, y: 445 to 615
draw.rectangle([(0, 445), (140, 615)], fill=(120, 68, 30), outline=(50, 25, 10), width=3)
# Draw 3 elegant drawers on the pedestal:
# Drawer 1:
draw.rectangle([(8, 452), (132, 498)], fill=(140, 80, 36), outline=(70, 38, 16), width=2)
draw.ellipse([(62, 470), (78, 480)], fill=(210, 160, 60), outline=(60, 35, 10), width=2)
# Drawer 2:
draw.rectangle([(8, 506), (132, 552)], fill=(140, 80, 36), outline=(70, 38, 16), width=2)
draw.ellipse([(62, 524), (78, 534)], fill=(210, 160, 60), outline=(60, 35, 10), width=2)
# Drawer 3:
draw.rectangle([(8, 560), (132, 606)], fill=(140, 80, 36), outline=(70, 38, 16), width=2)
draw.ellipse([(62, 578), (78, 588)], fill=(210, 160, 60), outline=(60, 35, 10), width=2)

# Desk kneehole modesty panel: x: 140 to 230, y: 445 to 585
draw.rectangle([(140, 445), (228, 585)], fill=(80, 42, 18), outline=(40, 20, 8), width=2)
# Kneehole space below:
draw.rectangle([(140, 585), (228, 620)], fill=(30, 15, 8))

# Desk base plinth:
draw.rectangle([(0, 615), (140, 625)], fill=(60, 30, 12))

# 2. Clean the Carpet at the bottom (x: 0 to 380, y: 620 to 670)
# Clean warm woven rug
for y in range(620, 670):
    ratio = (y - 620) / 50
    r = int(230 - 20 * ratio)
    g = int(218 - 25 * ratio)
    b = int(195 - 30 * ratio)
    draw.line([(0, y), (380, y)], fill=(r, g, b))
# Fringe on the rug edge:
for x in range(0, 380, 8):
    draw.line([(x, 665), (x + 4, 670)], fill=(180, 160, 140), width=2)

# 3. Clean the plant leaves watermark:
# Apply a subtle selective blur over the plant watermark center (x: 230 to 310, y: 635 to 665)
plant_patch = im.crop((230, 630, 310, 665))
plant_clean = plant_patch.filter(ImageFilter.GaussianBlur(radius=3))
im.paste(plant_clean, (230, 630))

im.save('assets/room_pristine.png')
print('Pristine room perfected!')
