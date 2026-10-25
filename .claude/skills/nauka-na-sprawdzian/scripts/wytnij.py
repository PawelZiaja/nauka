#!/usr/bin/env python3
"""Wycina fragment obrazka (współrzędne w % – odczytaj je z siatka.py).
Użycie: python3 wytnij.py wej.jpg wyj.jpg x1 y1 x2 y2"""
import sys
from PIL import Image, ImageOps
im = ImageOps.exif_transpose(Image.open(sys.argv[1])); W, H = im.size
x1, y1, x2, y2 = map(float, sys.argv[3:7])
out = im.crop((int(W * x1 / 100), int(H * y1 / 100), int(W * x2 / 100), int(H * y2 / 100)))
(out.convert('RGB') if sys.argv[2].lower().endswith(('.jpg', '.jpeg')) else out).save(sys.argv[2]); print(f'Zapisano {sys.argv[2]} {out.size}')
