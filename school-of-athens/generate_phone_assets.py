#!/usr/bin/env python3
"""Generate phone UI PNG assets for School of Athens (1280x720, warm marble & gold theme)."""

import os
import math
from PIL import Image, ImageDraw, ImageFilter

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "game", "gui", "phone")
CHAR_DIR = os.path.join(os.path.dirname(__file__), "game", "images", "characters")

# Phone dimensions (scaled for 1280x720)
PHONE_W, PHONE_H = 420, 540
PHONE_RADIUS = 28
BEZEL = 3

COLORS = {
    "phone_body": "#3a3020",
    "phone_body_edge": "#4a3d2a",
    "phone_body_inner": "#2c2418",
    "phone_border": "#5a4d3a",
    "phone_border_dark": "#1a140a",
    "screen_bezel": "#1a140a",
    "bubble_player": "#8a6832",
    "bubble_player_dark": "#6a5025",
    "bubble_npc": "#3d3225",
    "bubble_npc_dark": "#2c2418",
    "contact_card": "#352c1e",
    "contact_card_hover": "#4a3d2a",
    "input_field": "#2c2418",
    "input_field_border": "#4a3d2a",
    "send_btn": "#8a6832",
    "send_btn_hover": "#c4a265",
    "nav_icon": "#7a6a50",
    "bg_edge": "#1a140a",
    "camera_lens": "#2c2418",
    "camera_ring": "#5a4d3a",
    "speaker": "#3a3020",
}

CHAR_BORDER_COLORS = {
    "socrates": "#c4a265",
    "aristotle": "#2c5f8a",
    "heraclitus": "#d4722a",
    "epicurus": "#5a8a4e",
    "herodotus": "#8a3040",
    "diogenes": "#7a6540",
}

CHARACTERS = ["socrates", "aristotle", "heraclitus", "epicurus", "herodotus", "diogenes"]


def hex_to_rgba(hex_color, alpha=255):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (r, g, b, alpha)


def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def gen_phone_body():
    """Generate a realistic phone body with gradient bezel, camera, and speaker."""
    w, h = PHONE_W, PHONE_H
    scale = 2
    sw, sh = w * scale, h * scale
    sr = PHONE_RADIUS * scale

    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Bottom shadow edge
    draw.rounded_rectangle(
        [(0, 2 * scale), (sw - 1, sh - 1)],
        radius=sr,
        fill=hex_to_rgba(COLORS["phone_border_dark"]),
    )
    # Main body fill
    draw.rounded_rectangle(
        [(0, 0), (sw - 1, sh - 2 * scale)],
        radius=sr,
        fill=hex_to_rgba(COLORS["phone_body"]),
    )
    # Top highlight edge
    draw.rounded_rectangle(
        [(1 * scale, 0), (sw - 1 * scale - 1, sh - 3 * scale)],
        radius=sr - scale,
        fill=hex_to_rgba(COLORS["phone_body_edge"]),
    )
    # Inner body
    inner_margin = 3 * scale
    draw.rounded_rectangle(
        [(inner_margin, inner_margin), (sw - inner_margin - 1, sh - inner_margin - 1)],
        radius=sr - inner_margin // 2,
        fill=hex_to_rgba(COLORS["phone_body"]),
    )

    # Screen cutout
    screen_margin = BEZEL * scale + 2 * scale
    screen_top = 27 * scale
    screen_bottom = 24 * scale
    screen_radius = (PHONE_RADIUS - BEZEL - 2) * scale

    draw.rounded_rectangle(
        [
            (screen_margin - scale, screen_top - scale),
            (sw - screen_margin + scale, sh - screen_bottom + scale),
        ],
        radius=screen_radius + scale,
        fill=hex_to_rgba(COLORS["screen_bezel"]),
    )
    draw.rounded_rectangle(
        [
            (screen_margin, screen_top),
            (sw - screen_margin, sh - screen_bottom),
        ],
        radius=screen_radius,
        fill=(44, 36, 24, 255),  # matches PHONE_BG
    )

    # Camera island
    cam_y = 12 * scale
    cam_cx = sw // 2

    # Speaker slit
    slit_w, slit_h = 40 * scale, 3 * scale
    draw.rounded_rectangle(
        [
            (cam_cx - slit_w // 2, cam_y - slit_h // 2),
            (cam_cx + slit_w // 2, cam_y + slit_h // 2),
        ],
        radius=slit_h // 2,
        fill=hex_to_rgba(COLORS["speaker"]),
    )

    # Camera lens
    cam_lens_x = cam_cx - 30 * scale
    lens_r = 4 * scale
    draw.ellipse(
        [
            (cam_lens_x - lens_r - 2 * scale, cam_y - lens_r - 2 * scale),
            (cam_lens_x + lens_r + 2 * scale, cam_y + lens_r + 2 * scale),
        ],
        fill=hex_to_rgba(COLORS["camera_ring"]),
    )
    draw.ellipse(
        [
            (cam_lens_x - lens_r, cam_y - lens_r),
            (cam_lens_x + lens_r, cam_y + lens_r),
        ],
        fill=hex_to_rgba(COLORS["camera_lens"]),
    )
    hl_r = 2 * scale
    draw.ellipse(
        [
            (cam_lens_x - hl_r + scale, cam_y - hl_r - scale),
            (cam_lens_x + hl_r + scale, cam_y + hl_r - scale),
        ],
        fill=(120, 100, 70, 100),
    )

    # Side buttons
    btn_x = sw - 2 * scale
    draw.rounded_rectangle(
        [(btn_x, 120 * scale), (btn_x + 3 * scale, 153 * scale)],
        radius=scale,
        fill=hex_to_rgba(COLORS["phone_border"]),
    )
    draw.rounded_rectangle(
        [(0 - 1 * scale, 107 * scale), (2 * scale, 133 * scale)],
        radius=scale,
        fill=hex_to_rgba(COLORS["phone_border"]),
    )
    draw.rounded_rectangle(
        [(0 - 1 * scale, 143 * scale), (2 * scale, 170 * scale)],
        radius=scale,
        fill=hex_to_rgba(COLORS["phone_border"]),
    )

    # Bottom home indicator
    ind_y = sh - 12 * scale
    ind_w = 60 * scale
    ind_h = 3 * scale
    draw.rounded_rectangle(
        [(cam_cx - ind_w // 2, ind_y - ind_h // 2),
         (cam_cx + ind_w // 2, ind_y + ind_h // 2)],
        radius=ind_h // 2,
        fill=(120, 100, 70, 160),
    )

    # Glass reflection overlay
    reflection = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    ref_draw = ImageDraw.Draw(reflection)
    points = [
        (sw * 0.15, 0),
        (sw * 0.55, 0),
        (sw * 0.25, sh * 0.45),
        (sw * 0.0, sh * 0.35),
    ]
    points = [(int(x), int(y)) for x, y in points]
    ref_draw.polygon(points, fill=(255, 240, 200, 6))
    reflection = reflection.filter(ImageFilter.GaussianBlur(radius=15 * scale))
    img = Image.alpha_composite(img, reflection)

    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, "phone_body.png"))


def gen_phone_shadow():
    w, h = PHONE_W + 40, PHONE_H + 40
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [(10, 15), (w - 10, h - 5)],
        radius=PHONE_RADIUS + 10,
        fill=(0, 0, 0, 80),
    )
    img = img.filter(ImageFilter.GaussianBlur(radius=20))

    inner = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    inner_draw = ImageDraw.Draw(inner)
    inner_draw.rounded_rectangle(
        [(25, 28), (w - 25, h - 18)],
        radius=PHONE_RADIUS + 2,
        fill=(0, 0, 0, 60),
    )
    inner = inner.filter(ImageFilter.GaussianBlur(radius=8))
    img = Image.alpha_composite(img, inner)
    img.save(os.path.join(OUTPUT_DIR, "phone_shadow.png"))


def gen_chat_bubble(filename, fill_color, dark_color, w=72, h=54, radius=20):
    scale = 2
    sw, sh, sr = w * scale, h * scale, radius * scale
    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle(
        [(0, 2 * scale), (sw - 1, sh - 1)],
        radius=sr,
        fill=hex_to_rgba(dark_color),
    )
    draw.rounded_rectangle(
        [(0, 0), (sw - 1, sh - 2 * scale)],
        radius=sr,
        fill=hex_to_rgba(fill_color),
    )
    highlight = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    hl_draw = ImageDraw.Draw(highlight)
    hl_draw.rounded_rectangle(
        [(1 * scale, 0), (sw - 1 * scale, sh // 3)],
        radius=sr,
        fill=(255, 240, 200, 10),
    )
    img = Image.alpha_composite(img, highlight)
    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, filename))


def gen_contact_card(filename, fill_color, w=150, h=54, radius=12):
    scale = 2
    sw, sh, sr = w * scale, h * scale, radius * scale
    fill = hex_to_rgba(fill_color)
    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(0, 0), (sw - 1, sh - 1)], radius=sr, fill=fill)

    highlight = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    hl_draw = ImageDraw.Draw(highlight)
    hl_draw.rounded_rectangle(
        [(2 * scale, 0), (sw - 2 * scale, 2 * scale)],
        radius=sr,
        fill=(255, 240, 200, 8),
    )
    img = Image.alpha_composite(img, highlight)
    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, filename))


def gen_input_field():
    w, h, r = 90, 54, 27
    scale = 2
    sw, sh, sr = w * scale, h * scale, r * scale
    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [(0, 0), (sw - 1, sh - 1)],
        radius=sr,
        fill=hex_to_rgba(COLORS["input_field_border"]),
    )
    draw.rounded_rectangle(
        [(2 * scale, 2 * scale), (sw - 2 * scale - 1, sh - 2 * scale - 1)],
        radius=sr - 2 * scale,
        fill=hex_to_rgba(COLORS["input_field"]),
    )
    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, "input_field.png"))


def gen_send_button(filename, fill_color):
    w, h, r = 90, 54, 27
    scale = 2
    sw, sh, sr = w * scale, h * scale, r * scale
    fill = hex_to_rgba(fill_color)
    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [(0, 2 * scale), (sw - 1, sh - 1)],
        radius=sr,
        fill=lerp_color(fill, (0, 0, 0, 255), 0.3),
    )
    draw.rounded_rectangle(
        [(0, 0), (sw - 1, sh - 2 * scale)],
        radius=sr,
        fill=fill,
    )
    highlight = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    hl_draw = ImageDraw.Draw(highlight)
    hl_draw.rounded_rectangle(
        [(2 * scale, 0), (sw - 2 * scale, sh // 3)],
        radius=sr,
        fill=(255, 240, 200, 18),
    )
    img = Image.alpha_composite(img, highlight)
    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, filename))


def gen_circular_avatar(name):
    """Generate circular avatar with colored border ring."""
    avatar_path = os.path.join(CHAR_DIR, f"{name}.png")
    if not os.path.exists(avatar_path):
        print(f"  Skipping {name} - avatar not found at {avatar_path}")
        return

    size = 128
    border = 4
    inner = size - border * 2

    avatar = Image.open(avatar_path).convert("RGBA").resize((inner, inner), Image.LANCZOS)

    mask = Image.new("L", (inner, inner), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([(0, 0), (inner - 1, inner - 1)], fill=255)

    output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(output)
    border_color = CHAR_BORDER_COLORS.get(name, "#c4a265")
    border_draw.ellipse([(0, 0), (size - 1, size - 1)], fill=border_color)
    border_draw.ellipse(
        [(border - 1, border - 1), (size - border, size - border)],
        fill=(0, 0, 0, 40),
    )

    avatar.putalpha(mask)
    output.paste(avatar, (border, border), avatar)
    output.save(os.path.join(OUTPUT_DIR, f"avatar_{name}_circle.png"))
    print(f"  Generated avatar_{name}_circle.png")


def gen_nav_icons():
    size = 30
    scale = 2
    ss = size * scale
    color = hex_to_rgba(COLORS["nav_icon"])

    # Back triangle
    img = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.polygon([(48, 6), (12, 30), (48, 54)], fill=color)
    img = img.resize((size, size), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, "icon_nav_back.png"))

    # Home circle
    img = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([(6, 6), (53, 53)], outline=color, width=5)
    img = img.resize((size, size), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, "icon_nav_circle.png"))

    # Recent apps square
    img = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([(10, 10), (49, 49)], radius=8, outline=color, width=5)
    img = img.resize((size, size), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, "icon_nav_square.png"))


def gen_status_icons():
    scale = 2

    # Signal bars
    w, h = 30, 21
    img = Image.new("RGBA", (w * scale, h * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    bar_heights = [12, 20, 30, 40]
    x = 2
    for bh in bar_heights:
        draw.rounded_rectangle(
            [(x * scale, (h * scale) - bh), ((x + 5) * scale, h * scale)],
            radius=2,
            fill=(245, 240, 224, 200),
        )
        x += 7
    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, "icon_signal.png"))

    # Battery
    w, h = 36, 18
    img = Image.new("RGBA", (w * scale, h * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [(0, 4), (60, 32)], radius=6, outline=(245, 240, 224, 200), width=3
    )
    draw.rounded_rectangle([(63, 11), (71, 25)], radius=2, fill=(245, 240, 224, 200))
    draw.rounded_rectangle([(4, 8), (54, 28)], radius=3, fill=(140, 160, 100, 200))
    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, "icon_battery.png"))

    # WiFi arcs
    w, h = 27, 24
    img = Image.new("RGBA", (w * scale, h * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = w * scale // 2, h * scale - 4
    for r in [42, 30, 18]:
        draw.arc(
            [(cx - r, cy - r), (cx + r, cy + r)],
            start=225, end=315,
            fill=(245, 240, 224, 200), width=5,
        )
    draw.ellipse([(cx - 5, cy - 3), (cx + 5, cy + 7)], fill=(245, 240, 224, 200))
    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, "icon_wifi.png"))


def gen_phone_bg():
    """Generate the desktop background behind the phone."""
    w, h = 1280, 720
    img = Image.new("RGBA", (w, h), hex_to_rgba(COLORS["bg_edge"]))
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = w // 2, h // 2
    # Warm radial glow
    draw.ellipse(
        [(cx - 400, cy - 300), (cx + 400, cy + 300)],
        fill=(58, 48, 32, 180),
    )
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=120))
    img = Image.alpha_composite(img, overlay)
    img.save(os.path.join(OUTPUT_DIR, "phone_bg.png"))


def gen_misc():
    # Camera dot
    img = Image.new("RGBA", (15, 15), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([(2, 2), (12, 12)], fill="#4a3d2a")
    img.save(os.path.join(OUTPUT_DIR, "camera_dot.png"))

    # Home indicator bar
    scale = 2
    w, h = 80, 4
    img = Image.new("RGBA", (w * scale, h * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [(0, 0), (w * scale - 1, h * scale - 1)],
        radius=h * scale // 2,
        fill=(120, 100, 70, 180),
    )
    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, "home_indicator.png"))


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating phone UI assets (marble & gold theme)...")

    print("  Phone body...")
    gen_phone_body()
    print("  Phone shadow...")
    gen_phone_shadow()

    print("  Chat bubbles...")
    gen_chat_bubble("bubble_player.png", COLORS["bubble_player"], COLORS["bubble_player_dark"])
    gen_chat_bubble("bubble_npc.png", COLORS["bubble_npc"], COLORS["bubble_npc_dark"])

    print("  Contact cards...")
    gen_contact_card("contact_card.png", COLORS["contact_card"])
    gen_contact_card("contact_card_hover.png", COLORS["contact_card_hover"])

    print("  Input field + buttons...")
    gen_input_field()
    gen_send_button("send_btn.png", COLORS["send_btn"])
    gen_send_button("send_btn_hover.png", COLORS["send_btn_hover"])

    print("  Circular avatars...")
    for name in CHARACTERS:
        gen_circular_avatar(name)

    print("  Nav + status icons...")
    gen_nav_icons()
    gen_status_icons()
    gen_misc()

    print("  Desktop background...")
    gen_phone_bg()

    print(f"\nDone! Assets saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
