#!/usr/bin/env python3
"""Generate phone UI PNG assets for the Ren'Py game (1920x1080 resolution)."""

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
    w, h = 690, 1110
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(0, 0), (w - 1, h - 1)], radius=51, fill=(0, 0, 0, 120))
    img = img.filter(ImageFilter.GaussianBlur(radius=22))
    img.save(os.path.join(OUTPUT_DIR, "phone_shadow.png"))


def gen_circular_avatar(name):
    avatar_path = os.path.join(CHAR_DIR, f"{name}.png")
    if not os.path.exists(avatar_path):
        print(f"  Skipping {name} - avatar not found at {avatar_path}")
        return
    avatar = Image.open(avatar_path).convert("RGBA").resize((180, 180), Image.LANCZOS)
    mask = Image.new("L", (180, 180), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([(0, 0), (179, 179)], fill=255)
    output = Image.new("RGBA", (192, 192), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(output)
    border_color = CHAR_BORDER_COLORS.get(name, "#4a6cf7")
    border_draw.ellipse([(0, 0), (191, 191)], fill=border_color)
    avatar.putalpha(mask)
    output.paste(avatar, (6, 6), avatar)
    output.save(os.path.join(OUTPUT_DIR, f"avatar_{name}_circle.png"))
    print(f"  Generated avatar_{name}_circle.png")


def gen_nav_icons():
    size = 30
    color = COLORS["nav_icon"]

    # Back triangle
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.polygon([(24, 3), (6, 15), (24, 27)], fill=color)
    img.save(os.path.join(OUTPUT_DIR, "icon_nav_back.png"))

    # Home circle
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([(3, 3), (26, 26)], outline=color, width=3)
    img.save(os.path.join(OUTPUT_DIR, "icon_nav_circle.png"))

    # Recent apps square
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(5, 5), (24, 24)], radius=4, outline=color, width=3)
    img.save(os.path.join(OUTPUT_DIR, "icon_nav_square.png"))


def gen_status_icons():
    # Signal bars
    img = Image.new("RGBA", (30, 21), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    bar_heights = [6, 10, 15, 20]
    x = 1
    for h in bar_heights:
        draw.rectangle([(x, 20 - h), (x + 5, 20)], fill="#ffffffcc")
        x += 7
    img.save(os.path.join(OUTPUT_DIR, "icon_signal.png"))

    # Battery
    img = Image.new("RGBA", (36, 18), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(0, 2), (30, 15)], radius=3, outline="#ffffffcc", width=2)
    draw.rectangle([(32, 6), (35, 11)], fill="#ffffffcc")
    draw.rectangle([(3, 5), (26, 12)], fill="#66cc66cc")
    img.save(os.path.join(OUTPUT_DIR, "icon_battery.png"))

    # WiFi arcs
    img = Image.new("RGBA", (27, 24), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for r in [21, 15, 9]:
        cx, cy = 13, 21
        draw.arc(
            [(cx - r, cy - r), (cx + r, cy + r)],
            start=225,
            end=315,
            fill="#ffffffcc",
            width=3,
        )
    draw.ellipse([(10, 18), (16, 24)], fill="#ffffffcc")
    img.save(os.path.join(OUTPUT_DIR, "icon_wifi.png"))


def gen_phone_bg():
    w, h = 1920, 1080
    img = Image.new("RGBA", (w, h), COLORS["bg_edge"])
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = w // 2, h // 2
    draw.ellipse(
        [(cx - 600, cy - 450), (cx + 600, cy + 450)], fill=(22, 22, 42, 180)
    )
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=180))
    img = Image.alpha_composite(img, overlay)
    img.save(os.path.join(OUTPUT_DIR, "phone_bg.png"))


def gen_misc():
    # Camera dot
    img = Image.new("RGBA", (15, 15), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([(2, 2), (12, 12)], fill="#333348")
    img.save(os.path.join(OUTPUT_DIR, "camera_dot.png"))

    # Home indicator bar
    img = Image.new("RGBA", (120, 6), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(0, 0), (119, 5)], radius=3, fill="#555568")
    img.save(os.path.join(OUTPUT_DIR, "home_indicator.png"))


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating phone UI assets (1080p)...")

    # Phone frame
    print("  Phone body + shadow...")
    gen_rounded_rect(
        "phone_body.png", 630, 1050, 42, COLORS["phone_body"], COLORS["phone_border"], 2
    )
    gen_phone_shadow()

    # Chat bubbles (for 9-slice)
    print("  Chat bubbles...")
    gen_rounded_rect("bubble_player.png", 72, 54, 21, COLORS["bubble_player"])
    gen_rounded_rect("bubble_npc.png", 72, 54, 21, COLORS["bubble_npc"])

    # Contact cards
    print("  Contact cards...")
    gen_rounded_rect("contact_card.png", 150, 54, 12, COLORS["contact_card"])
    gen_rounded_rect(
        "contact_card_hover.png", 150, 54, 12, COLORS["contact_card_hover"]
    )

    # Input / buttons
    print("  Input field + buttons...")
    gen_rounded_rect("input_field.png", 90, 54, 27, COLORS["input_field"])
    gen_rounded_rect("send_btn.png", 90, 54, 27, COLORS["send_btn"])
    gen_rounded_rect("send_btn_hover.png", 90, 54, 27, COLORS["send_btn_hover"])

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
