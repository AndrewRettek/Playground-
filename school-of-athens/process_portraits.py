#!/usr/bin/env python3
"""Remove backgrounds from character portraits for School of Athens.

Reads source images from game/images/characters/,
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

# Source filename -> output filename mapping
# Update these entries when real art is provided
PORTRAITS = [
    # ("Socrates1.jpg", "socrates_1.png"),
    # ("Socrates2.jpg", "socrates_2.png"),
    # etc.
]


def crop_to_aspect(img, target_w, target_h):
    """Crop image to target aspect ratio, centered horizontally, anchored to top."""
    iw, ih = img.size
    target_ratio = target_w / target_h
    img_ratio = iw / ih

    if img_ratio > target_ratio:
        new_w = int(ih * target_ratio)
        left = (iw - new_w) // 2
        img = img.crop((left, 0, left + new_w, ih))
    else:
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

    with open(src_path, "rb") as f:
        input_data = f.read()
    output_data = remove(input_data)

    img = Image.open(BytesIO(output_data)).convert("RGBA")
    img = crop_to_aspect(img, PORTRAIT_W, PORTRAIT_H)
    img = img.resize((PORTRAIT_W, PORTRAIT_H), Image.LANCZOS)

    img.save(dst_path)
    print(f"  {src_name} → {dst_name} ({img.size[0]}x{img.size[1]})")
    return True


def main():
    os.makedirs(DST_DIR, exist_ok=True)

    if not PORTRAITS:
        print("No portrait source files configured yet.")
        print("Add source -> output mappings to PORTRAITS list when art is provided.")
        return

    print("Processing portraits...\n")
    success = sum(1 for src, dst in PORTRAITS if process_portrait(src, dst))
    print(f"\nDone! {success}/{len(PORTRAITS)} portraits processed.")
    print(f"Output: {DST_DIR}")


if __name__ == "__main__":
    main()
