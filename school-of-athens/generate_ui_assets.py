#!/usr/bin/env python3
"""Generate procedural UI assets for School of Athens (warm marble & gold theme).

Creates menu_bg, desktop_bg, chat_bg, messages_header, and logo placeholder
using PIL drawing — no external source images required.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "game", "images", "ui")


def gen_menu_bg():
    """Generate a warm marble-textured main menu background."""
    w, h = 1920, 1080
    img = Image.new("RGBA", (w, h), (42, 35, 24, 255))
    draw = ImageDraw.Draw(img)

    # Warm marble-like gradients
    for i in range(20):
        x = int(w * (i * 0.07 + 0.05 * math.sin(i * 0.8)))
        y = int(h * (0.1 + i * 0.04))
        rw = int(w * 0.4 + i * 30)
        rh = int(h * 0.3 + i * 20)
        alpha = max(10, 30 - i)
        draw.ellipse(
            [(x - rw // 2, y - rh // 2), (x + rw // 2, y + rh // 2)],
            fill=(196, 162, 101, alpha),
        )

    # Column-like vertical stripes for classical feel
    for i in range(6):
        cx = int(w * (0.1 + i * 0.16))
        col_w = 40
        draw.rectangle(
            [(cx - col_w // 2, 0), (cx + col_w // 2, h)],
            fill=(58, 48, 32, 25),
        )
        # Column highlight
        draw.rectangle(
            [(cx - col_w // 4, 0), (cx + col_w // 4, h)],
            fill=(196, 162, 101, 10),
        )

    img = img.filter(ImageFilter.GaussianBlur(radius=30))

    # Vignette
    vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    for r in range(0, 400, 2):
        alpha = int(120 * (r / 400))
        vdraw.rectangle([(0, 0), (w, r)], fill=(0, 0, 0, alpha))
        vdraw.rectangle([(0, h - r), (w, h)], fill=(0, 0, 0, alpha))
        vdraw.rectangle([(0, 0), (r, h)], fill=(0, 0, 0, alpha // 2))
        vdraw.rectangle([(w - r, 0), (w, h)], fill=(0, 0, 0, alpha // 2))

    img = Image.alpha_composite(img, vignette)
    img.save(os.path.join(OUTPUT_DIR, "menu_bg.png"))
    print(f"  menu_bg.png (1920x1080)")


def gen_desktop_bg():
    """Generate warm parchment-toned desktop background."""
    w, h = 1920, 1080
    img = Image.new("RGBA", (w, h), (26, 20, 10, 255))
    draw = ImageDraw.Draw(img)

    # Warm center glow
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    cx, cy = w // 2, h // 2
    odraw.ellipse(
        [(cx - 500, cy - 350), (cx + 500, cy + 350)],
        fill=(58, 48, 32, 100),
    )
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=150))
    img = Image.alpha_composite(img, overlay)

    img.save(os.path.join(OUTPUT_DIR, "desktop_bg.png"))
    print(f"  desktop_bg.png (1920x1080)")


def gen_chat_bg():
    """Generate dark parchment chat texture."""
    w, h = 630, 1050
    img = Image.new("RGBA", (w, h), (35, 28, 18, 255))
    draw = ImageDraw.Draw(img)

    # Subtle grain
    import random
    random.seed(42)
    grain = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grain)
    for _ in range(3000):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        a = random.randint(3, 12)
        gdraw.point((x, y), fill=(196, 162, 101, a))

    img = Image.alpha_composite(img, grain)
    img.save(os.path.join(OUTPUT_DIR, "chat_bg.png"))
    print(f"  chat_bg.png (630x1050)")


def gen_messages_header():
    """Generate warm gold header banner."""
    w, h = 624, 66
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Gold gradient bar
    for y in range(h):
        t = y / h
        r = int(138 + (196 - 138) * (1 - abs(2 * t - 1)))
        g = int(104 + (162 - 104) * (1 - abs(2 * t - 1)))
        b = int(50 + (101 - 50) * (1 - abs(2 * t - 1)))
        draw.line([(0, y), (w, y)], fill=(r, g, b, 180))

    # Subtle border lines
    draw.line([(0, 0), (w, 0)], fill=(196, 162, 101, 60))
    draw.line([(0, h - 1), (w, h - 1)], fill=(100, 80, 40, 80))

    img.save(os.path.join(OUTPUT_DIR, "messages_header.png"))
    print(f"  messages_header.png (624x66)")


def gen_logo():
    """Generate a text-based logo placeholder."""
    w, h = 750, 300
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Decorative border
    draw.rounded_rectangle(
        [(20, 20), (w - 20, h - 20)],
        radius=15,
        outline=(196, 162, 101, 120),
        width=2,
    )

    # Inner decorative border
    draw.rounded_rectangle(
        [(28, 28), (w - 28, h - 28)],
        radius=12,
        outline=(196, 162, 101, 60),
        width=1,
    )

    # Title text (using default font)
    try:
        font_path = os.path.join(os.path.dirname(__file__), "game", "gui", "fonts", "Inter-Bold.ttf")
        title_font = ImageFont.truetype(font_path, 48)
        sub_font = ImageFont.truetype(font_path, 22)
    except (OSError, IOError):
        title_font = ImageDraw.Draw(img).getfont()
        sub_font = title_font

    draw.text((w // 2, h // 2 - 25), "SCHOOL OF ATHENS", fill=(196, 162, 101, 255), anchor="mm", font=title_font)
    draw.text((w // 2, h // 2 + 30), "Converse with the Great Minds", fill=(160, 149, 128, 200), anchor="mm", font=sub_font)

    # Greek key decorative line
    line_y = h // 2 + 60
    for x in range(100, w - 100, 20):
        draw.rectangle([(x, line_y), (x + 10, line_y + 3)], fill=(196, 162, 101, 50))

    img.save(os.path.join(OUTPUT_DIR, "logo.png"))
    print(f"  logo.png (750x300)")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating UI assets (warm marble & gold theme)...")
    gen_menu_bg()
    gen_desktop_bg()
    gen_chat_bg()
    gen_messages_header()
    gen_logo()
    print(f"\nDone! Assets saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
