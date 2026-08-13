#!/usr/bin/env python3
"""Render PDF pages as images for visual inspection."""
import sys
sys.path.insert(0, "/tmp/pymupdf_lib")
import pymupdf

PDF = "/home/karimboy/.hermes/cache/documents/doc_e7d8c4ad4246_B1 Middle (8).pdf"
OUT = "/home/karimboy/projects/ielts-zone-online/static/images/b1mid8"

doc = pymupdf.open(PDF)
for pno in [1, 2, 6, 7]:  # 0-indexed: page 2 (listening p1), page 3 (listening p2?), page 7, 8
    page = doc[pno]
    pix = page.get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5))
    fname = f"{OUT}/page{pno+1}_render.png"
    pix.save(fname)
    print(f"page{pno+1}_render.png {pix.width}x{pix.height}")
