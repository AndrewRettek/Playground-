#!/usr/bin/env python3
"""Remove backgrounds from character images and save as portrait assets.

Takes each base character image from game/images/characters/,
removes the background using rembg, crops to 3:5 aspect ratio,
resizes to 360x600, and saves to all 4 portrait slots per character.
"""

import os
import shutil
from PIL import Image
from rembg import remove

BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(BASE_DIR, "game", "images", "characters")
DST_DIR = os.path.join(SRC_DIR, "portraits")

CHARACTERS = ["mallory", "rye", "demitria", "gabby"]
PORTRAIT_W, PORTRAIT_H = 360, 600
SLOTS_PER_CHARACTER = 4


def crop_to_aspect(img, target_w, target_h):
    """Crop image to target aspect ratio, centered."""
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


def process_character(name):
    """Remove background, crop, resize, and save to all 4 portrait slots."""
    src_path = os.path.join(SRC_DIR, f"{name}.png")
    if not os.path.exists(src_path):
        print(f"  SKIP {name} — source not found at {src_path}")
        return False

    print(f"  Processing {name}...")

    # Load and remove background
    with open(src_path, "rb") as f:
        input_data = f.read()
    output_data = remove(input_data)

    # Open as PIL image
    from io import BytesIO
    img = Image.open(BytesIO(output_data)).convert("RGBA")
    print(f"    Source: {img.size[0]}x{img.size[1]}")

    # Crop to 3:5 aspect ratio
    img = crop_to_aspect(img, PORTRAIT_W, PORTRAIT_H)

    # Resize to final portrait size
    img = img.resize((PORTRAIT_W, PORTRAIT_H), Image.LANCZOS)
    print(f"    Output: {img.size[0]}x{img.size[1]}")

    # Save to all 4 portrait slots
    for i in range(1, SLOTS_PER_CHARACTER + 1):
        dst_path = os.path.join(DST_DIR, f"{name}_{i}.png")
        img.save(dst_path)
        print(f"    Saved {name}_{i}.png")

    return True


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    print("Removing backgrounds and generating portraits...\n")

    success = 0
    for name in CHARACTERS:
        if process_character(name):
            success += 1
        print()

    print(f"Done! {success}/{len(CHARACTERS)} characters processed.")
    print(f"Portraits saved to {DST_DIR}")


if __name__ == "__main__":
    main()
