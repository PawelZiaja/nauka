#!/usr/bin/env python3
"""Nakłada na obrazek podpisaną siatkę co 10% (i cieńszą co 5%), żeby odczytać współrzędne
punktu do zadania „spot” albo granice wycinka.  Użycie: python3 siatka.py wej.jpg wyj.png
Obejrzyj wynik narzędziem view i odczytaj x, y w procentach (0–100) od lewego górnego rogu."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
im = ImageOps.exif_transpose(Image.open(sys.argv[1])).convert('RGB'); im.thumbnail((1400, 1400))
W, H = im.size; d = ImageDraw.Draw(im, 'RGBA')
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', max(12, W // 70))
except Exception: f = ImageFont.load_default()
for p in range(5, 100, 5):
    x, y = W * p / 100, H * p / 100; a = 170 if p % 10 == 0 else 70; c = (255, 0, 0, a)
    d.line([(x, 0), (x, H)], fill=c, width=2 if p % 10 == 0 else 1); d.line([(0, y), (W, y)], fill=c, width=2 if p % 10 == 0 else 1)
    if p % 10 == 0:
        for t, pos in ((str(p), (x + 3, 3)), (str(p), (3, y + 3))):
            d.rectangle([pos, (pos[0] + f.size * 1.6, pos[1] + f.size * 1.2)], fill=(255, 255, 255, 200)); d.text(pos, t, fill=(200, 0, 0), font=f)
im.save(sys.argv[2]); print(f'Zapisano {sys.argv[2]} ({W}×{H})')
