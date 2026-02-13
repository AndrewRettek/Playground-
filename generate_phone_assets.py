#!/usr/bin/env python3
"""Generate phone UI PNG assets for the Ren'Py game."""

import os
from PIL import Image, ImageDraw, ImageFilter

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "game", "gui", "phone")
CHAR_DIR = os.path.join(os.path.dirname(__file__), "game", "images", "characters")

COLORS = {
    "phone_body": "#1a1a2e",
    "phone_border": "#2d2d4a",
    "bubble_player": "#4a6cf7",
    "bubble_npc": "#2b2d42",
    "contact_card": "#1e1e30",
    "contact_card_hover": "#2a2a40",
    "input_field": "#12121e",
    "send_btn": "#4a6cf7",
    "send_btn_hover": "#6182fa",
    "nav_icon": "#666680",
    "bg_edge": "#0a0a14",
}

CHAR_BORDER_COLORS = {
    "mallory": "#daa520",
    "rye": "#cc4444",
    "demitria": "#8844aa",
    "gabby": "#44aaaa",
}

CHARACTERS = ["mallory", "rye", "demitria", "gabby"]


def gen_rounded_rect(filename, w, h, radius, fill, outline=None, outline_width=1):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [(0, 0), (w - 1, h - 1)],
        radius=radius,
        fill=fill,
        outline=outline,
        width=outline_width,
    )
    img.save(os.path.join(OUTPUT_DIR, filename))


def gen_phone_shadow():
    w, h = 460, 740
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(0, 0), (w - 1, h - 1)], radius=34, fill=(0, 0, 0, 120))
    img = img.filter(ImageFilter.GaussianBlur(radius=15))
    img.save(os.path.join(OUTPUT_DIR, "phone_shadow.png"))


def gen_circular_avatar(name):
    avatar_path = os.path.join(CHAR_DIR, f"{name}.png")
    if not os.path.exists(avatar_path):
        print(f"  Skipping {name} - avatar not found at {avatar_path}")
        return
    avatar = Image.open(avatar_path).convert("RGBA").resize((120, 120), Image.LANCZOS)
    mask = Image.new("L", (120, 120), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([(0, 0), (119, 119)], fill=255)
    output = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(output)
    border_color = CHAR_BORDER_COLORS.get(name, "#4a6cf7")
    border_draw.ellipse([(0, 0), (127, 127)], fill=border_color)
    avatar.putalpha(mask)
    output.paste(avatar, (4, 4), avatar)
    output.save(os.path.join(OUTPUT_DIR, f"avatar_{name}_circle.png"))
    print(f"  Generated avatar_{name}_circle.png")


def gen_nav_icons():
    size = 20
    color = COLORS["nav_icon"]

    # Back triangle
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.polygon([(16, 2), (4, 10), (16, 18)], fill=color)
    img.save(os.path.join(OUTPUT_DIR, "icon_nav_back.png"))

    # Home circle
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([(2, 2), (17, 17)], outline=color, width=2)
    img.save(os.path.join(OUTPUT_DIR, "icon_nav_circle.png"))

    # Recent apps square
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(3, 3), (16, 16)], radius=3, outline=color, width=2)
    img.save(os.path.join(OUTPUT_DIR, "icon_nav_square.png"))


def gen_status_icons():
    # Signal bars
    img = Image.new("RGBA", (20, 14), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    bar_heights = [4, 7, 10, 13]
    x = 1
    for h in bar_heights:
        draw.rectangle([(x, 13 - h), (x + 3, 13)], fill="#ffffffcc")
        x += 4
    img.save(os.path.join(OUTPUT_DIR, "icon_signal.png"))

    # Battery
    img = Image.new("RGBA", (24, 12), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(0, 1), (20, 10)], radius=2, outline="#ffffffcc", width=1)
    draw.rectangle([(21, 4), (23, 7)], fill="#ffffffcc")
    draw.rectangle([(2, 3), (17, 8)], fill="#66cc66cc")
    img.save(os.path.join(OUTPUT_DIR, "icon_battery.png"))

    # WiFi arcs
    img = Image.new("RGBA", (18, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for r in [14, 10, 6]:
        cx, cy = 9, 14
        draw.arc(
            [(cx - r, cy - r), (cx + r, cy + r)],
            start=225,
            end=315,
            fill="#ffffffcc",
            width=2,
        )
    draw.ellipse([(7, 12), (11, 16)], fill="#ffffffcc")
    img.save(os.path.join(OUTPUT_DIR, "icon_wifi.png"))


def gen_phone_bg():
    w, h = 1280, 720
    img = Image.new("RGBA", (w, h), COLORS["bg_edge"])
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = w // 2, h // 2
    draw.ellipse(
        [(cx - 400, cy - 300), (cx + 400, cy + 300)], fill=(22, 22, 42, 180)
    )
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=120))
    img = Image.alpha_composite(img, overlay)
    img.save(os.path.join(OUTPUT_DIR, "phone_bg.png"))


def gen_misc():
    # Camera dot
    img = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([(1, 1), (8, 8)], fill="#333348")
    img.save(os.path.join(OUTPUT_DIR, "camera_dot.png"))

    # Home indicator bar
    img = Image.new("RGBA", (80, 4), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(0, 0), (79, 3)], radius=2, fill="#555568")
    img.save(os.path.join(OUTPUT_DIR, "home_indicator.png"))


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating phone UI assets...")

    # Phone frame
    print("  Phone body + shadow...")
    gen_rounded_rect(
        "phone_body.png", 420, 700, 28, COLORS["phone_body"], COLORS["phone_border"], 1
    )
    gen_phone_shadow()

    # Chat bubbles (small, for 9-slice)
    print("  Chat bubbles...")
    gen_rounded_rect("bubble_player.png", 48, 36, 14, COLORS["bubble_player"])
    gen_rounded_rect("bubble_npc.png", 48, 36, 14, COLORS["bubble_npc"])

    # Contact cards
    print("  Contact cards...")
    gen_rounded_rect("contact_card.png", 100, 36, 8, COLORS["contact_card"])
    gen_rounded_rect(
        "contact_card_hover.png", 100, 36, 8, COLORS["contact_card_hover"]
    )

    # Input / buttons
    print("  Input field + buttons...")
    gen_rounded_rect("input_field.png", 60, 36, 18, COLORS["input_field"])
    gen_rounded_rect("send_btn.png", 60, 36, 18, COLORS["send_btn"])
    gen_rounded_rect("send_btn_hover.png", 60, 36, 18, COLORS["send_btn_hover"])

    # Circular avatars
    print("  Circular avatars...")
    for name in CHARACTERS:
        gen_circular_avatar(name)

    # Icons
    print("  Nav + status icons...")
    gen_nav_icons()
    gen_status_icons()
    gen_misc()

    # Background
    print("  Phone background...")
    gen_phone_bg()

    print(f"\nDone! Assets saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
