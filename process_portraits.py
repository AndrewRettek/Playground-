#!/usr/bin/env python3
"""Remove backgrounds from Gemini-generated character portraits.

Reads 16 source JPG images from game/images/characters/,
removes backgrounds using rembg, crops to 3:5 aspect ratio, resizes to
360x600, and saves as character_n.png in the portraits directory.
"""

import os
from io import BytesIO
from PIL import Image
from rembg import remove

BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(BASE_DIR, "game", "images", "characters")
DST_DIR = os.path.join(SRC_DIR, "portraits")

PORTRAIT_W, PORTRAIT_H = 360, 600

# Source filename → output filename mapping
# Source: "Character N.png", Output: "character_n.png"
PORTRAITS = [
    ("Mallroy1.jpg", "mallory_1.png"),
    ("mallory2.jpg", "mallory_2.png"),
    ("mallory3.jpg", "mallory_3.png"),
    ("mallory4.jpg", "mallory_4.png"),
    ("Rye1.jpg", "rye_1.png"),
    ("rye2.jpg", "rye_2.png"),
    ("rye3.jpg", "rye_3.png"),
    ("rye4.jpg", "rye_4.png"),
    ("Demetria.jpg", "demitria_1.png"),
    ("Demetria2.jpg", "demitria_2.png"),
    ("Demetria3.jpg", "demitria_3.png"),
    ("Demetria4.jpg", "demitria_4.png"),
    ("Gabby1.jpg", "gabby_1.png"),
    ("Gabby2.jpg", "gabby_2.png"),
    ("Gabby3.jpg", "gabby_3.png"),
    ("Gabby4.jpg", "gabby_4.png"),
]


def crop_to_aspect(img, target_w, target_h):
    """Crop image to target aspect ratio, centered horizontally, anchored to top."""
    iw, ih = img.size
    target_ratio = target_w / target_h
    img_ratio = iw / ih

    if img_ratio > target_ratio:
        # Image is wider than needed — crop sides
        new_w = int(ih * target_ratio)
        left = (iw - new_w) // 2
        img = img.crop((left, 0, left + new_w, ih))
    else:
        # Image is taller than needed — crop bottom (keep head/top)
        new_h = int(iw / target_ratio)
        img = img.crop((0, 0, iw, new_h))

    return img


def process_portrait(src_name, dst_name):
    """Remove background from one portrait, crop, resize, and save."""
    src_path = os.path.join(SRC_DIR, src_name)
    dst_path = os.path.join(DST_DIR, dst_name)

    if not os.path.exists(src_path):
        print(f"  SKIP {src_name} — not found")
        return False

    # Load and remove background
    with open(src_path, "rb") as f:
        input_data = f.read()
    output_data = remove(input_data)

    # Open as PIL image
    img = Image.open(BytesIO(output_data)).convert("RGBA")

    # Crop to 3:5 aspect ratio, resize to final size
    img = crop_to_aspect(img, PORTRAIT_W, PORTRAIT_H)
    img = img.resize((PORTRAIT_W, PORTRAIT_H), Image.LANCZOS)

    img.save(dst_path)
    print(f"  {src_name} → {dst_name} ({img.size[0]}x{img.size[1]})")
    return True


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    print("Processing Gemini portraits...\n")

    success = sum(1 for src, dst in PORTRAITS if process_portrait(src, dst))

    print(f"\nDone! {success}/{len(PORTRAITS)} portraits processed.")
    print(f"Output: {DST_DIR}")


if __name__ == "__main__":
    main()
