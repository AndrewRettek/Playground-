#!/usr/bin/env python3
"""Generate textured UI panel PNG assets for BindrChat menu screens.

Follows the same patterns as generate_phone_assets.py:
  - PIL/Pillow for image generation
  - 2x rendering with LANCZOS downscale for anti-aliasing
  - hex_to_rgba() color conversion
  - All assets output to game/gui/panels/
"""

import os
from PIL import Image, ImageDraw, ImageFilter

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "game", "gui", "panels")

# ── Color palette ──────────────────────────────────────────────────
COLORS = {
    "panel_fill": "#1a1a2e",        # Main dark panel body
    "panel_border": "#d4af37",      # Gold border
    "panel_solid_fill": "#1a1a2eFF",  # Fully opaque version
    "slot_fill": "#0d2f44",         # Save-slot background
    "slot_hover_fill": "#1a5276",   # Save-slot hover
    "slot_border": "#2a4a6a",       # Subtle border for slots
    "btn_rose_start": "#E8849A",    # Rose gradient start
    "btn_rose_end": "#D4607A",      # Rose gradient end (darker)
    "btn_rose_hover_start": "#FFB0C0",  # Hover lighter
    "btn_rose_hover_end": "#E8849A",
    "btn_outline": "#E8849A",       # Secondary button outline color
    "btn_outline_hover": "#FFB0C0",
    "btn_outline_fill": "#E8849A11",  # Very faint fill
    "btn_outline_hover_fill": "#E8849A22",
    "divider_gold": "#d4af37",      # Ornate divider line
    "divider_diamond": "#d4af37",   # Diamond accent
}


def hex_to_rgba(hex_color, alpha=255):
    """Convert hex color to RGBA tuple."""
    h = hex_color.lstrip("#")
    if len(h) == 8:
        r, g, b, a = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16)
        return (r, g, b, a)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (r, g, b, alpha)


def lerp_color(c1, c2, t):
    """Linearly interpolate between two RGBA tuples."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


# ── Panel: semi-transparent dark with gold border (for modals/menus) ──

def gen_panel_dark():
    """Semi-transparent dark panel with gold border and rounded corners."""
    w, h, r = 200, 200, 12  # 9-slice friendly size
    scale = 2
    sw, sh, sr = w * scale, h * scale, r * scale
    border_w = 2 * scale

    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Gold border
    draw.rounded_rectangle(
        [(0, 0), (sw - 1, sh - 1)],
        radius=sr,
        fill=hex_to_rgba(COLORS["panel_border"]),
    )
    # Inner fill (semi-transparent)
    draw.rounded_rectangle(
        [(border_w, border_w), (sw - border_w - 1, sh - border_w - 1)],
        radius=sr - border_w // 2,
        fill=hex_to_rgba(COLORS["panel_fill"], alpha=204),  # ~80% opaque
    )
    # Subtle top highlight
    highlight = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    hl_draw = ImageDraw.Draw(highlight)
    hl_draw.rounded_rectangle(
        [(border_w + 2, border_w + 1), (sw - border_w - 2, sh // 4)],
        radius=sr,
        fill=(255, 255, 255, 8),
    )
    img = Image.alpha_composite(img, highlight)

    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, "panel_dark.png"))


def gen_panel_dark_solid():
    """Fully opaque dark panel with gold border (for modals that need no bleed-through)."""
    w, h, r = 200, 200, 12
    scale = 2
    sw, sh, sr = w * scale, h * scale, r * scale
    border_w = 2 * scale

    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Gold border
    draw.rounded_rectangle(
        [(0, 0), (sw - 1, sh - 1)],
        radius=sr,
        fill=hex_to_rgba(COLORS["panel_border"]),
    )
    # Inner fill (fully opaque)
    draw.rounded_rectangle(
        [(border_w, border_w), (sw - border_w - 1, sh - border_w - 1)],
        radius=sr - border_w // 2,
        fill=hex_to_rgba(COLORS["panel_fill"], alpha=255),
    )
    # Subtle top highlight
    highlight = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    hl_draw = ImageDraw.Draw(highlight)
    hl_draw.rounded_rectangle(
        [(border_w + 2, border_w + 1), (sw - border_w - 2, sh // 4)],
        radius=sr,
        fill=(255, 255, 255, 8),
    )
    img = Image.alpha_composite(img, highlight)

    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, "panel_dark_solid.png"))


# ── Save slot backgrounds ──

def gen_panel_slot(filename, fill_color):
    """Save-slot card background with subtle border."""
    w, h, r = 120, 80, 8
    scale = 2
    sw, sh, sr = w * scale, h * scale, r * scale
    border_w = 1 * scale

    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Subtle border
    draw.rounded_rectangle(
        [(0, 0), (sw - 1, sh - 1)],
        radius=sr,
        fill=hex_to_rgba(COLORS["slot_border"]),
    )
    # Inner fill
    draw.rounded_rectangle(
        [(border_w, border_w), (sw - border_w - 1, sh - border_w - 1)],
        radius=sr - 1,
        fill=hex_to_rgba(fill_color),
    )

    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, filename))


# ── Primary buttons (rose gradient) ──

def gen_button_primary(filename, start_color, end_color):
    """Rose gradient button with depth shadow."""
    w, h, r = 120, 60, 10
    scale = 2
    sw, sh, sr = w * scale, h * scale, r * scale

    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Bottom shadow
    draw.rounded_rectangle(
        [(0, 2 * scale), (sw - 1, sh - 1)],
        radius=sr,
        fill=lerp_color(hex_to_rgba(end_color), (0, 0, 0, 255), 0.3),
    )

    # Create gradient fill
    gradient = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    start_rgba = hex_to_rgba(start_color)
    end_rgba = hex_to_rgba(end_color)
    for y in range(sh - 2 * scale):
        t = y / max(1, sh - 2 * scale - 1)
        color = lerp_color(start_rgba, end_rgba, t)
        for x in range(sw):
            gradient.putpixel((x, y), color)

    # Mask gradient to rounded rectangle
    mask = Image.new("L", (sw, sh), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(
        [(0, 0), (sw - 1, sh - 2 * scale)],
        radius=sr,
        fill=255,
    )
    gradient.putalpha(mask.split()[0] if hasattr(mask, 'split') else mask)

    img = Image.alpha_composite(img, gradient)

    # Top highlight
    highlight = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    hl_draw = ImageDraw.Draw(highlight)
    hl_draw.rounded_rectangle(
        [(2 * scale, 0), (sw - 2 * scale, sh // 3)],
        radius=sr,
        fill=(255, 255, 255, 25),
    )
    img = Image.alpha_composite(img, highlight)

    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, filename))


# ── Secondary buttons (outline style) ──

def gen_button_secondary(filename, outline_color, fill_color):
    """Outline-style button with very faint fill."""
    w, h, r = 120, 60, 10
    scale = 2
    sw, sh, sr = w * scale, h * scale, r * scale
    border_w = 2 * scale

    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outline
    draw.rounded_rectangle(
        [(0, 0), (sw - 1, sh - 1)],
        radius=sr,
        fill=hex_to_rgba(outline_color),
    )
    # Inner faint fill
    draw.rounded_rectangle(
        [(border_w, border_w), (sw - border_w - 1, sh - border_w - 1)],
        radius=sr - border_w // 2,
        fill=hex_to_rgba(fill_color),
    )

    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, filename))


# ── Ornate divider (gold line with diamond center) ──

def gen_divider_ornate():
    """Gold horizontal line with a small diamond shape in the center."""
    w, h = 400, 16
    scale = 2
    sw, sh = w * scale, h * scale

    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    gold = hex_to_rgba(COLORS["divider_gold"])
    cy = sh // 2

    # Main horizontal line (1px at final res = 2px at 2x)
    line_h = 2
    draw.rectangle(
        [(0, cy - line_h), (sw, cy + line_h)],
        fill=(*gold[:3], 140),  # slightly transparent
    )

    # Fade-out at edges (gradient alpha)
    fade_len = 60 * scale
    for x in range(fade_len):
        alpha_factor = x / fade_len
        fade_color = (*gold[:3], int(140 * alpha_factor))
        # Left fade
        draw.rectangle([(x, cy - line_h), (x, cy + line_h)], fill=fade_color)
        # Right fade
        draw.rectangle([(sw - 1 - x, cy - line_h), (sw - 1 - x, cy + line_h)], fill=fade_color)

    # Center diamond
    diamond_size = 6 * scale
    cx = sw // 2
    diamond_points = [
        (cx, cy - diamond_size),       # top
        (cx + diamond_size, cy),       # right
        (cx, cy + diamond_size),       # bottom
        (cx - diamond_size, cy),       # left
    ]
    draw.polygon(diamond_points, fill=gold)

    # Small inner diamond (brighter highlight)
    inner_size = 3 * scale
    inner_points = [
        (cx, cy - inner_size),
        (cx + inner_size, cy),
        (cx, cy + inner_size),
        (cx - inner_size, cy),
    ]
    draw.polygon(inner_points, fill=(*gold[:3], 255))

    img = img.resize((w, h), Image.LANCZOS)
    img.save(os.path.join(OUTPUT_DIR, "divider_ornate.png"))


# ── Main ──

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating UI panel assets...")

    print("  panel_dark.png (semi-transparent with gold border)...")
    gen_panel_dark()

    print("  panel_dark_solid.png (opaque with gold border)...")
    gen_panel_dark_solid()

    print("  panel_slot.png / panel_slot_hover.png (save slot backgrounds)...")
    gen_panel_slot("panel_slot.png", COLORS["slot_fill"])
    gen_panel_slot("panel_slot_hover.png", COLORS["slot_hover_fill"])

    print("  button_primary.png / button_primary_hover.png (rose gradient)...")
    gen_button_primary("button_primary.png", COLORS["btn_rose_start"], COLORS["btn_rose_end"])
    gen_button_primary("button_primary_hover.png", COLORS["btn_rose_hover_start"], COLORS["btn_rose_hover_end"])

    print("  button_secondary.png / button_secondary_hover.png (outline)...")
    gen_button_secondary("button_secondary.png", COLORS["btn_outline"], COLORS["btn_outline_fill"])
    gen_button_secondary("button_secondary_hover.png", COLORS["btn_outline_hover"], COLORS["btn_outline_hover_fill"])

    print("  divider_ornate.png (gold line with diamond)...")
    gen_divider_ornate()

    print(f"\nDone! Assets saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
