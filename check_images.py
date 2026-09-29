import glob
from PIL import Image

for f in sorted(glob.glob('assets/page5_extracted/*.*')):
    im = Image.open(f)
    print(f, im.size, im.mode)
