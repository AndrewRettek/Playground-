#!/usr/bin/env python3
"""Process uploaded Midjourney UI art into properly sized game assets."""

import os
from PIL import Image, ImageFilter

SRC = "/home/user/Playground-/game/images/characters"
DST = "/home/user/Playground-/game/images/ui"

FILES = {
    "oscredwin_dark_fantasy_cityscape_at_twilight_ornate_gothic_ar_d817ab2a-6796-427e-b60c-f20735032108_2.png": {
        "name": "menu_bg.png",
        "size": (1280, 720),
        "desc": "Main menu background",
    },
    "oscredwin_dark_elegant_desktop_workspace_soft_ambient_lightin_94ec082b-d7ea-436d-a418-0180670047c4_2.png": {
        "name": "desktop_bg.png",
        "size": (1280, 720),
        "desc": "Desktop background (behind phone)",
    },
    "oscredwin_seamless_dark_subtle_pattern_texture_very_faint_orn_2812dcc5-681b-4e17-b3f7-37bc39613af1_2.png": {
        "name": "chat_bg.png",
        "size": (420, 700),
        "desc": "Chat background texture",
    },
    "oscredwin_dark_horizontal_banner_subtle_gold_and_purple_gradi_40ad2e1e-031b-4d47-8d00-07f3afa19e82_2.png": {
        "name": "messages_header.png",
        "size": (416, 44),
        "desc": "Messages header banner",
    },
    "oscredwin_FutaDomWorld_Chat_elegant_fantasy_game_logo_gold_an_409ed910-c4a3-4254-aa74-3718aa7b0b52_2.png": {
        "name": "logo.png",
        "size": (500, 200),
        "desc": "Game logo",
    },
}


def resize_cover(img, target_size):
    """Resize image to cover target size (crop to fit, no letterboxing)."""
    tw, th = target_size
    iw, ih = img.size
    target_ratio = tw / th
    img_ratio = iw / ih

    if img_ratio > target_ratio:
        # Image is wider - crop sides
        new_h = ih
        new_w = int(ih * target_ratio)
        left = (iw - new_w) // 2
        img = img.crop((left, 0, left + new_w, ih))
    else:
        # Image is taller - crop top/bottom
        new_w = iw
        new_h = int(iw / target_ratio)
        top = (ih - new_h) // 2
        img = img.crop((0, top, iw, top + new_h))

    return img.resize(target_size, Image.LANCZOS)


def process_desktop_bg(img, target_size):
    """Darken the desktop bg slightly so the phone stands out more."""
    from PIL import ImageEnhance
    img = resize_cover(img, target_size)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.6)
    return img


def main():
    os.makedirs(DST, exist_ok=True)

    for filename, info in FILES.items():
        src_path = os.path.join(SRC, filename)
        dst_path = os.path.join(DST, info["name"])

        if not os.path.exists(src_path):
            print(f"  SKIP {info['name']} - source not found")
            continue

        img = Image.open(src_path).convert("RGBA")

        if info["name"] == "desktop_bg.png":
            img = process_desktop_bg(img, info["size"])
        elif info["name"] == "chat_bg.png":
            # Darken the chat texture so it doesn't overwhelm text
            from PIL import ImageEnhance
            img = resize_cover(img, info["size"])
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.3)
        elif info["name"] == "logo.png":
            # Fit logo (don't crop, use thumbnail)
            img.thumbnail(info["size"], Image.LANCZOS)
        else:
            img = resize_cover(img, info["size"])

        img.save(dst_path)
        print(f"  OK {info['name']} ({img.size[0]}x{img.size[1]}) - {info['desc']}")

    print("\nDone! Assets saved to", DST)


if __name__ == "__main__":
    main()
