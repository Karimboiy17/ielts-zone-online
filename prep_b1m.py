#!/usr/bin/env python3
"""Copy audio + crop people photos from p7_img2."""
import sys, os
sys.path.insert(0, "/tmp/pymupdf_lib")
from PIL import Image

BASE = "/home/karimboy/projects/ielts-zone-online"
AUDIO_SRC = "/home/karimboy/.hermes/cache/audio/audio_723507df5a9f.mp3"
AUDIO_DST = f"{BASE}/static/audio/b1mid8_listening_full.mp3"

# Copy audio
import shutil
shutil.copy(AUDIO_SRC, AUDIO_DST)
print("Audio copied:", os.path.getsize(AUDIO_DST), "bytes")

# Crop people photos (5 people, photos on left like before)
SRC = f"{BASE}/static/images/b1mid8"
img = Image.open(f"{SRC}/p7_img2.png")
w, h = img.size
print(f"p7_img2: {w}x{h}")

rows = [
    ("p7_person6.png", 0.02, 0.20),
    ("p7_person7.png", 0.22, 0.40),
    ("p7_person8.png", 0.42, 0.60),
    ("p7_person9.png", 0.62, 0.80),
    ("p7_person10.png", 0.82, 0.98),
]

for fname, y_top, y_bot in rows:
    top = int(h * y_top)
    bot = int(h * y_bot)
    crop = img.crop((int(w * 0.05), top, int(w * 0.30), bot))
    out = os.path.join(SRC, fname)
    crop.save(out)
    print(f"{fname} {crop.size}")
print("DONE")
