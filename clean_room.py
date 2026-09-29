from PIL import Image, ImageDraw, ImageFilter
import numpy as np

im = Image.open('assets/room_background.png').convert('RGB')
draw = ImageDraw.Draw(im)

# 1. REMOVE THE MOUSE CURSOR on the side table (x: 1080 to 1180, y: 550 to 670)
# Look at the bedside table: it has a top surface (dark brown) and a drawer front (medium brown with border and knob).
# We can sample the clean brown wood from (x: 1050 to 1090, y: 560 to 650) and patch over the cursor!
table_clean = im.crop((1050, 560, 1080, 660))
# Let's clone table_clean across x: 1080 to 1180
for x in range(1080, 1185, 25):
    im.paste(table_clean, (x, 560))

# Redraw the table drawer border and knob
# Drawer top line
draw.line([(960, 570), (1185, 570)], fill=(30, 18, 10), width=4)
# Drawer bottom/edges
draw.rectangle([(970, 575), (1180, 665)], outline=(50, 28, 15), width=3)
# Drawer knob
draw.ellipse([(1050, 605), (1070, 625)], fill=(60, 35, 20), outline=(20, 10, 5), width=3)

# 2. CLEAN THE WINDOW PANES (Canva watermark removal)
# The window is located at x: 285 to 590, y: 65 to 335
# Panes coordinates:
panes = [
    # Top left pane
    (305, 80, 435, 195),
    # Top right pane
    (450, 80, 575, 195),
    # Bottom left pane
    (305, 205, 435, 320),
    # Bottom right pane
    (450, 205, 575, 320),
]
for x1, y1, x2, y2 in panes:
    # Fill each pane with clean sky blue gradient / glass reflection
    for y in range(y1, y2):
        ratio = (y - y1) / (y2 - y1)
        r = int(95 + 40 * ratio)
        g = int(145 + 45 * ratio)
        b = int(185 + 40 * ratio)
        draw.line([(x1, y), (x2, y)], fill=(r, g, b))
    # Glass light reflection streaks
    draw.polygon([(x1 + 20, y1), (x1 + 45, y1), (x1 + 10, y2), (x1 - 15, y2)], fill=(160, 210, 240, 100))
    draw.polygon([(x1 + 60, y1), (x1 + 75, y1), (x1 + 35, y2), (x1 + 20, y2)], fill=(160, 210, 240, 70))

# 3. CLEAN DESK PANELS (x: 0 to 275, y: 380 to 620)
# Inner gold framed panel on desk front: x: 10 to 140, y: 440 to 590
# Clean solid fill with gold border
draw.rectangle([(12, 442), (138, 588)], fill=(168, 100, 42))
draw.rectangle([(16, 446), (134, 584)], outline=(205, 140, 55), width=3)
# Right desk panel
draw.rectangle([(160, 442), (225, 588)], fill=(145, 85, 35))
draw.rectangle([(164, 446), (221, 584)], outline=(195, 130, 50), width=3)

# 4. CLEAN THE PICTURE FRAME ON THE WALL (x: 945 to 1110, y: 90 to 310)
# Fill the canvas inside the frame (x: 975 to 1080, y: 125 to 275) with clean vintage portrait / parchment
for y in range(125, 275):
    ratio = (y - 125) / 150
    r = int(235 - 30 * ratio)
    g = int(215 - 35 * ratio)
    b = int(180 - 40 * ratio)
    draw.line([(975, y), (1080, y)], fill=(r, g, b))

# 5. CLEAN THE SPOTLIGHT WALL AREA (x: 600 to 780, y: 120 to 350)
# Smooth out the watermark lines with a subtle blend
wall_patch = im.crop((600, 120, 780, 350))
wall_smooth = wall_patch.filter(ImageFilter.GaussianBlur(radius=3))
im.paste(wall_smooth, (600, 120))

im.save('assets/room_clean.png')
print('Successfully saved assets/room_clean.png without watermark or mouse cursor!')
