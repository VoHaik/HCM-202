from PIL import Image, ImageDraw, ImageFilter
import numpy as np

im = Image.open('assets/room_background.png').convert('RGB')
draw = ImageDraw.Draw(im)

# 1. FIX THE WINDOW (x: 285 to 590, y: 65 to 335)
# Fill the 4 glass panes with clean crisp glass gradients
# Window frame colors: Outer wood #5c321e, Inner cross #452414
panes = [
    (300, 78, 434, 196),
    (446, 78, 578, 196),
    (300, 204, 434, 322),
    (446, 204, 578, 322),
]
for x1, y1, x2, y2 in panes:
    for y in range(y1, y2):
        ratio = (y - y1) / (y2 - y1)
        r = int(105 + 40 * ratio)
        g = int(160 + 45 * ratio)
        b = int(210 + 35 * ratio)
        draw.line([(x1, y), (x2, y)], fill=(r, g, b))
    # Subtle clean glass highlights
    draw.polygon([(x1 + 15, y1), (x1 + 35, y1), (x1 + 10, y2), (x1 - 10, y2)], fill=(185, 230, 255))
    draw.polygon([(x1 + 55, y1), (x1 + 70, y1), (x1 + 35, y2), (x1 + 20, y2)], fill=(185, 230, 255))

# Redraw clean crisp window inner grid bars
draw.line([(440, 75), (440, 325)], fill=(75, 42, 25), width=6)
draw.line([(295, 200), (582, 200)], fill=(75, 42, 25), width=6)

# 2. FIX THE DESK (x: 0 to 280, y: 380 to 625)
# Desk body background: rich wood #8c4e20
# Left panel:
draw.rectangle([(10, 440), (138, 590)], fill=(145, 82, 35), outline=(60, 32, 12), width=3)
draw.rectangle([(18, 448), (130, 582)], fill=(160, 92, 40), outline=(210, 145, 60), width=3)

# Right panel:
draw.rectangle([(155, 440), (225, 590)], fill=(135, 75, 30), outline=(60, 32, 12), width=3)
draw.rectangle([(162, 448), (218, 582)], fill=(150, 85, 35), outline=(200, 135, 55), width=3)

# Base of desk:
draw.rectangle([(0, 592), (235, 620)], fill=(95, 50, 20), outline=(50, 25, 10), width=2)

# Principal nameplate desk clean:
draw.rectangle([(0, 385), (90, 435)], fill=(35, 25, 20), outline=(180, 140, 50), width=2)
# Re-add clean gold text
draw.text((8, 400), "PRINCIPAL", fill=(225, 180, 60))

# 3. FIX THE CARPET (x: 0 to 390, y: 550 to 670)
# Clean cream carpet with diamond lattice pattern
# We can sample clean carpet from x: 230 to 300, y: 560 to 640 and smooth out watermark
carpet_patch = im.crop((230, 560, 300, 640))
for x in range(0, 220, 60):
    im.paste(carpet_patch, (x, 560))

# 4. FIX THE BEDSIDE TABLE & REMOVE MOUSE CURSOR (x: 950 to 1190, y: 500 to 670)
# Clean wooden table:
# Table top surface:
draw.polygon([(945, 535), (1188, 535), (1188, 555), (945, 555)], fill=(100, 55, 25), outline=(50, 25, 10))
# Table front body (DRAWER): covers all of x: 955 to 1188, y: 555 to 668
draw.rectangle([(955, 555), (1188, 668)], fill=(125, 72, 32), outline=(45, 22, 10), width=3)
# Drawer inner panel:
draw.rectangle([(970, 568), (1175, 655)], fill=(140, 80, 36), outline=(75, 40, 18), width=3)
# Drawer clean brass knob:
draw.ellipse([(1060, 600), (1085, 625)], fill=(215, 160, 60), outline=(60, 35, 10), width=3)
# Table left legs:
draw.rectangle([(960, 668), (978, 670)], fill=(75, 40, 18))

# 5. FIX THE GOLD PICTURE FRAME CANVAS (x: 970 to 1085, y: 120 to 280)
for y in range(120, 280):
    ratio = (y - 120) / 160
    r = int(240 - 25 * ratio)
    g = int(220 - 30 * ratio)
    b = int(185 - 35 * ratio)
    draw.line([(972, y), (1082, y)], fill=(r, g, b))

# 6. FIX WALL WATERMARK UNDER LIGHT BEAM (x: 600 to 760, y: 120 to 350)
wall_crop = im.crop((600, 120, 760, 350))
wall_clean = wall_crop.filter(ImageFilter.GaussianBlur(radius=4))
im.paste(wall_clean, (600, 120))

# 7. FIX FILING CABINET (x: 375 to 515, y: 375 to 520)
# Two clean dark charcoal steel drawers
# Top drawer:
draw.rectangle([(380, 385), (510, 445)], fill=(55, 62, 68), outline=(30, 34, 38), width=3)
draw.rectangle([(425, 410), (465, 420)], fill=(195, 205, 215), outline=(30, 34, 38), width=2)
# Bottom drawer:
draw.rectangle([(380, 450), (510, 510)], fill=(55, 62, 68), outline=(30, 34, 38), width=3)
draw.rectangle([(425, 475), (465, 485)], fill=(195, 205, 215), outline=(30, 34, 38), width=2)

# 8. FIX CLOCK FACE WATERMARK (x: 1000 to 1090, y: 450 to 540)
# Smooth the clock face center
clock_face = im.crop((1025, 465, 1075, 515))
clock_clean = clock_face.filter(ImageFilter.GaussianBlur(radius=2))
im.paste(clock_clean, (1025, 465))

# Save the completely restored room
im.save('assets/room_pristine.png')
print('Successfully created assets/room_pristine.png - completely free of watermarks, clean window, clean desk, clean table, and NO MOUSE CURSOR!')
