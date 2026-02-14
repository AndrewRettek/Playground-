#!/usr/bin/env python3
"""Generate phone UI PNG assets for the Ren'Py game (1920x1080 resolution).

Design reference: Nighten's "Yet Another Phone for Ren'Py" (CC0)
https://github.com/NathanGuilhot/yet-another-phone-for-renpy
"""

import os
import math
from PIL import Image, ImageDraw, ImageFilter

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "game", "gui", "phone")
CHAR_DIR = os.path.join(os.path.dirname(__file__), "game", "images", "characters")

# Phone dimensions
PHONE_W, PHONE_H = 630, 810
PHONE_RADIUS = 42
BEZEL = 4  # bezel thickness around screen area

COLORS = {
    "phone_body": "#1a1a2e",
    "phone_body_edge": "#252540",     # lighter edge for depth
    "phone_body_inner": "#111122",    # darker inner for depth
    "phone_border": "#3a3a5a",        # outer frame highlight
    "phone_border_dark": "#0e0e1c",   # outer frame shadow
    "screen_bezel": "#0a0a16",        # screen edge (very dark)
    "bubble_player": "#4a6cf7",
    "bubble_player_dark": "#3d5cd4",  # darker edge for depth
    "bubble_npc": "#2b2d42",
    "bubble_npc_dark": "#1e2033",     # darker edge
    "contact_card": "#1e1e30",
    "contact_card_hover": "#2a2a40",
    "input_field": "#12121e",
    "input_field_border": "#2a2a44",
    "send_btn": "#4a6cf7",
    "send_btn_hover": "#6182fa",
    "nav_icon": "#555570",
    "bg_edge": "#0a0a14",
    "camera_lens": "#1a1a30",
    "camera_ring": "#333355",
    "speaker": "#222240",
}

CHAR_BORDER_COLORS = {
    "mallory": "#daa520",
    "rye": "#cc4444",
    "demitria": "#8844aa",
    "gabby": "#44aaaa",
}

CHARACTERS = ["mallory", "rye", "demitria", "gabby"]


def hex_to_rgba(hex_color, alpha=255):
    """Convert hex color to RGBA tuple."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (r, g, b, alpha)


def lerp_color(c1, c2, t):
    """Linearly interpolate between two RGBA tuples."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def gen_phone_body():
    """Generate a realistic phone body with gradient bezel, camera, and speaker."""
    w, h = PHONE_W, PHONE_H
    # Work at 2x for anti-aliasing, then downscale
    scale = 2
    sw, sh = w * scale, h * scale
    sr = PHONE_RADIUS * scale

    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # --- Outer body (the phone chassis) ---
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
    # Top highlight edge (subtle)
    draw.rounded_rectangle(
        [(1 * scale, 0), (sw - 1 * scale - 1, sh - 3 * scale)],
        radius=sr - scale,
        fill=hex_to_rgba(COLORS["phone_body_edge"]),
    )
    # Inner body (slightly darker, creates depth)
    inner_margin = 3 * scale
    draw.rounded_rectangle(
        [(inner_margin, inner_margin), (sw - inner_margin - 1, sh - inner_margin - 1)],
        radius=sr - inner_margin // 2,
        fill=hex_to_rgba(COLORS["phone_body"]),
    )

    # --- Screen cutout (very dark, inset) ---
    screen_margin = BEZEL * scale + 2 * scale
    screen_top = 40 * scale  # space for camera/speaker area
    screen_bottom = 36 * scale  # space for bottom chin
    screen_radius = (PHONE_RADIUS - BEZEL - 2) * scale

    # Screen bezel shadow (slightly larger, gives inset look)
    draw.rounded_rectangle(
        [
            (screen_margin - scale, screen_top - scale),
            (sw - screen_margin + scale, sh - screen_bottom + scale),
        ],
        radius=screen_radius + scale,
        fill=hex_to_rgba(COLORS["screen_bezel"]),
    )
    # Screen area (dark fill — content renders on top via Ren'Py frame)
    draw.rounded_rectangle(
        [
            (screen_margin, screen_top),
            (sw - screen_margin, sh - screen_bottom),
        ],
        radius=screen_radius,
        fill=(15, 15, 26, 255),  # matches PHONE_BG
    )

    # --- Camera island (top center) ---
    cam_y = 18 * scale
    cam_cx = sw // 2

    # Speaker slit
    slit_w, slit_h = 60 * scale, 4 * scale
    draw.rounded_rectangle(
        [
            (cam_cx - slit_w // 2, cam_y - slit_h // 2),
            (cam_cx + slit_w // 2, cam_y + slit_h // 2),
        ],
        radius=slit_h // 2,
        fill=hex_to_rgba(COLORS["speaker"]),
    )

    # Camera lens (left of center)
    cam_lens_x = cam_cx - 45 * scale
    lens_r = 5 * scale
    # Outer ring
    draw.ellipse(
        [
            (cam_lens_x - lens_r - 2 * scale, cam_y - lens_r - 2 * scale),
            (cam_lens_x + lens_r + 2 * scale, cam_y + lens_r + 2 * scale),
        ],
        fill=hex_to_rgba(COLORS["camera_ring"]),
    )
    # Inner lens
    draw.ellipse(
        [
            (cam_lens_x - lens_r, cam_y - lens_r),
            (cam_lens_x + lens_r, cam_y + lens_r),
        ],
        fill=hex_to_rgba(COLORS["camera_lens"]),
    )
    # Lens highlight
    hl_r = 2 * scale
    draw.ellipse(
        [
            (cam_lens_x - hl_r + scale, cam_y - hl_r - scale),
            (cam_lens_x + hl_r + scale, cam_y + hl_r - scale),
        ],
        fill=(80, 80, 120, 100),
    )

    # --- Side buttons (right edge) ---
    btn_x = sw - 2 * scale
    # Power button
    draw.rounded_rectangle(
        [(btn_x, 180 * scale), (btn_x + 3 * scale, 230 * scale)],
        radius=scale,
        fill=hex_to_rgba(COLORS["phone_border"]),
    )
    # Volume up
    draw.rounded_rectangle(
        [(0 - 1 * scale, 160 * scale), (2 * scale, 200 * scale)],
        radius=scale,
        fill=hex_to_rgba(COLORS["phone_border"]),
    )
    # Volume down
    draw.rounded_rectangle(
        [(0 - 1 * scale, 215 * scale), (2 * scale, 255 * scale)],
        radius=scale,
        fill=hex_to_rgba(COLORS["phone_border"]),
    )

    # --- Bottom home indicator ---
    ind_y = sh - 18 * scale
    ind_w = 90 * scale
    ind_h = 4 * scale
    draw.rounded_rectangle(
        [(cam_cx - ind_w // 2, ind_y - ind_h // 2),
         (cam_cx + ind_w // 2, ind_y + ind_h // 2)],
        radius=ind_h // 2,
        fill=(80, 80, 110, 160),
    )

    # --- Glass reflection overlay ---
    reflection = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    ref_draw = ImageDraw.Draw(reflection)
    # Diagonal highlight across upper portion
    points = [
        (sw * 0.15, 0),
        (sw * 0.55, 0),
        (sw * 0.25, sh * 0.45),
        (sw * 0.0, sh * 0.35),
    ]
    points = [(int(x), int(y)) for x, y in points]
    ref_draw.polygon(points, fill=(255, 255, 255, 8))
    reflection = reflection.filter(ImageFilter.GaussianBlur(radius=15 * scale))

    # Composite reflection
    img = Image.alpha_composite(img, reflection)

    # Downscale with anti-aliasing
    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, "phone_body.png"))


def gen_phone_shadow():
    """Generate a multi-layer phone shadow for depth."""
    w, h = PHONE_W + 60, PHONE_H + 60
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outer soft shadow
    draw.rounded_rectangle(
        [(10, 15), (w - 10, h - 5)],
        radius=PHONE_RADIUS + 10,
        fill=(0, 0, 0, 80),
    )
    img = img.filter(ImageFilter.GaussianBlur(radius=20))

    # Inner sharper shadow
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
    """Generate a chat bubble with subtle gradient depth (for 9-slice)."""
    scale = 2
    sw, sh, sr = w * scale, h * scale, radius * scale

    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Bottom shadow edge
    draw.rounded_rectangle(
        [(0, 2 * scale), (sw - 1, sh - 1)],
        radius=sr,
        fill=hex_to_rgba(dark_color),
    )
    # Main fill
    draw.rounded_rectangle(
        [(0, 0), (sw - 1, sh - 2 * scale)],
        radius=sr,
        fill=hex_to_rgba(fill_color),
    )
    # Top highlight
    highlight = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    hl_draw = ImageDraw.Draw(highlight)
    hl_draw.rounded_rectangle(
        [(1 * scale, 0), (sw - 1 * scale, sh // 3)],
        radius=sr,
        fill=(255, 255, 255, 12),
    )
    img = Image.alpha_composite(img, highlight)

    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, filename))


def gen_contact_card(filename, fill_color, w=150, h=54, radius=12):
    """Generate a contact card with subtle depth."""
    scale = 2
    sw, sh, sr = w * scale, h * scale, radius * scale
    fill = hex_to_rgba(fill_color)

    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Main fill
    draw.rounded_rectangle([(0, 0), (sw - 1, sh - 1)], radius=sr, fill=fill)

    # Subtle top highlight line
    highlight = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    hl_draw = ImageDraw.Draw(highlight)
    hl_draw.rounded_rectangle(
        [(2 * scale, 0), (sw - 2 * scale, 2 * scale)],
        radius=sr,
        fill=(255, 255, 255, 10),
    )
    img = Image.alpha_composite(img, highlight)

    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, filename))


def gen_input_field():
    """Generate input field with subtle border."""
    w, h, r = 90, 54, 27
    scale = 2
    sw, sh, sr = w * scale, h * scale, r * scale

    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Border
    draw.rounded_rectangle(
        [(0, 0), (sw - 1, sh - 1)],
        radius=sr,
        fill=hex_to_rgba(COLORS["input_field_border"]),
    )
    # Inner fill
    draw.rounded_rectangle(
        [(2 * scale, 2 * scale), (sw - 2 * scale - 1, sh - 2 * scale - 1)],
        radius=sr - 2 * scale,
        fill=hex_to_rgba(COLORS["input_field"]),
    )

    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, "input_field.png"))


def gen_send_button(filename, fill_color):
    """Generate send button with gradient and depth."""
    w, h, r = 90, 54, 27
    scale = 2
    sw, sh, sr = w * scale, h * scale, r * scale
    fill = hex_to_rgba(fill_color)

    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Shadow
    draw.rounded_rectangle(
        [(0, 2 * scale), (sw - 1, sh - 1)],
        radius=sr,
        fill=lerp_color(fill, (0, 0, 0, 255), 0.3),
    )
    # Main fill
    draw.rounded_rectangle(
        [(0, 0), (sw - 1, sh - 2 * scale)],
        radius=sr,
        fill=fill,
    )
    # Top highlight
    highlight = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    hl_draw = ImageDraw.Draw(highlight)
    hl_draw.rounded_rectangle(
        [(2 * scale, 0), (sw - 2 * scale, sh // 3)],
        radius=sr,
        fill=(255, 255, 255, 20),
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

    size = 192
    border = 6
    inner = size - border * 2

    avatar = Image.open(avatar_path).convert("RGBA").resize((inner, inner), Image.LANCZOS)

    # Create circular mask
    mask = Image.new("L", (inner, inner), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([(0, 0), (inner - 1, inner - 1)], fill=255)

    # Output with border
    output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(output)
    border_color = CHAR_BORDER_COLORS.get(name, "#4a6cf7")
    border_draw.ellipse([(0, 0), (size - 1, size - 1)], fill=border_color)

    # Inner shadow ring for depth
    border_draw.ellipse(
        [(border - 1, border - 1), (size - border, size - border)],
        fill=(0, 0, 0, 40),
    )

    avatar.putalpha(mask)
    output.paste(avatar, (border, border), avatar)
    output.save(os.path.join(OUTPUT_DIR, f"avatar_{name}_circle.png"))
    print(f"  Generated avatar_{name}_circle.png")


def gen_nav_icons():
    """Generate navigation bar icons at 2x with anti-aliasing."""
    size = 30
    scale = 2
    ss = size * scale
    color = hex_to_rgba(COLORS["nav_icon"])

    # Back triangle
    img = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.polygon(
        [(48, 6), (12, 30), (48, 54)],
        fill=color,
    )
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
    """Generate status bar icons at 2x with anti-aliasing."""
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
            fill=(255, 255, 255, 200),
        )
        x += 7
    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, "icon_signal.png"))

    # Battery
    w, h = 36, 18
    img = Image.new("RGBA", (w * scale, h * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Body
    draw.rounded_rectangle(
        [(0, 4), (60, 32)], radius=6, outline=(255, 255, 255, 200), width=3
    )
    # Nub
    draw.rounded_rectangle([(63, 11), (71, 25)], radius=2, fill=(255, 255, 255, 200))
    # Fill
    draw.rounded_rectangle([(4, 8), (54, 28)], radius=3, fill=(102, 204, 102, 200))
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
            fill=(255, 255, 255, 200), width=5,
        )
    draw.ellipse([(cx - 5, cy - 3), (cx + 5, cy + 7)], fill=(255, 255, 255, 200))
    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, "icon_wifi.png"))


def gen_phone_bg():
    """Generate the desktop background behind the phone."""
    w, h = 1920, 1080
    img = Image.new("RGBA", (w, h), hex_to_rgba(COLORS["bg_edge"]))
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = w // 2, h // 2
    # Subtle radial glow
    draw.ellipse(
        [(cx - 600, cy - 450), (cx + 600, cy + 450)],
        fill=(22, 22, 42, 180),
    )
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=180))
    img = Image.alpha_composite(img, overlay)
    img.save(os.path.join(OUTPUT_DIR, "phone_bg.png"))


def gen_misc():
    """Generate camera dot and home indicator."""
    # Camera dot (now part of phone_body, but keep for compat)
    img = Image.new("RGBA", (15, 15), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([(2, 2), (12, 12)], fill="#333348")
    img.save(os.path.join(OUTPUT_DIR, "camera_dot.png"))

    # Home indicator bar
    scale = 2
    w, h = 120, 6
    img = Image.new("RGBA", (w * scale, h * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [(0, 0), (w * scale - 1, h * scale - 1)],
        radius=h * scale // 2,
        fill=(85, 85, 104, 180),
    )
    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, "home_indicator.png"))


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating phone UI assets (1080p, polished)...")

    # Phone frame
    print("  Phone body (with bezel, camera, speaker, glass)...")
    gen_phone_body()
    print("  Phone shadow (multi-layer)...")
    gen_phone_shadow()

    # Chat bubbles with depth
    print("  Chat bubbles (with depth/shadow)...")
    gen_chat_bubble(
        "bubble_player.png",
        COLORS["bubble_player"],
        COLORS["bubble_player_dark"],
    )
    gen_chat_bubble(
        "bubble_npc.png",
        COLORS["bubble_npc"],
        COLORS["bubble_npc_dark"],
    )

    # Contact cards
    print("  Contact cards...")
    gen_contact_card("contact_card.png", COLORS["contact_card"])
    gen_contact_card("contact_card_hover.png", COLORS["contact_card_hover"])

    # Input / buttons
    print("  Input field + buttons (with depth)...")
    gen_input_field()
    gen_send_button("send_btn.png", COLORS["send_btn"])
    gen_send_button("send_btn_hover.png", COLORS["send_btn_hover"])

    # Circular avatars
    print("  Circular avatars (with border ring)...")
    for name in CHARACTERS:
        gen_circular_avatar(name)

    # Icons (2x rendered, anti-aliased)
    print("  Nav + status icons (anti-aliased)...")
    gen_nav_icons()
    gen_status_icons()
    gen_misc()

    # Background
    print("  Desktop background...")
    gen_phone_bg()

    print(f"\nDone! Assets saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
