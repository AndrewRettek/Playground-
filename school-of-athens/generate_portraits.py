#!/usr/bin/env python3
"""Generate placeholder portrait images for each philosopher (4 poses each).

These are temporary stand-ins until real art is added.
Each portrait is 360x600 with a colored silhouette and pose label.
"""

import os
from PIL import Image, ImageDraw, ImageFilter

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "game", "images", "characters", "portraits")

CHARACTERS = {
    "socrates":   {"color": "#c4a265", "bg": "#3a3020"},
    "aristotle":  {"color": "#2c5f8a", "bg": "#1a2a3a"},
    "heraclitus": {"color": "#d4722a", "bg": "#3a2010"},
    "epicurus":   {"color": "#5a8a4e", "bg": "#1a3018"},
    "herodotus":  {"color": "#8a3040", "bg": "#3a1820"},
    "diogenes":   {"color": "#7a6540", "bg": "#2a2418"},
}

POSES = ["default", "happy", "thinking", "flirty"]

W, H = 360, 600


def gen_placeholder(name, pose_index, color_hex, bg_hex):
    """Generate a placeholder portrait with silhouette shape."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    c = color_hex.lstrip("#")
    cr, cg, cb = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    b = bg_hex.lstrip("#")
    br, bg_r, bb = int(b[0:2], 16), int(b[2:4], 16), int(b[4:6], 16)

    # Background gradient (fades to transparent at top)
    for y in range(H):
        alpha = int(180 * (y / H))
        draw.line([(0, y), (W, y)], fill=(br, bg_r, bb, alpha))

    body_color = (cr, cg, cb, 140)

    # Head
    head_cx, head_cy = W // 2, 120
    head_r = 55
    offsets = [0, -5, 8, -3]
    head_cx += offsets[pose_index] * 2

    draw.ellipse(
        [(head_cx - head_r, head_cy - head_r),
         (head_cx + head_r, head_cy + head_r)],
        fill=body_color,
    )

    # Neck
    draw.rectangle(
        [(head_cx - 18, head_cy + head_r - 10),
         (head_cx + 18, head_cy + head_r + 30)],
        fill=body_color,
    )

    # Shoulders + torso
    shoulder_y = head_cy + head_r + 20
    torso_points = [
        (head_cx - 120, shoulder_y + 30),
        (head_cx - 90, shoulder_y - 10),
        (head_cx + 90, shoulder_y - 10),
        (head_cx + 120, shoulder_y + 30),
        (head_cx + 100, H + 20),
        (head_cx - 100, H + 20),
    ]
    draw.polygon(torso_points, fill=body_color)

    # Pose label
    pose_name = POSES[pose_index]
    label = f"{name.upper()} — {pose_name}"
    draw.rectangle([(0, H - 50), (W, H)], fill=(0, 0, 0, 160))
    text_x = W // 2
    text_y = H - 35
    draw.text((text_x, text_y), label, fill=(245, 240, 224, 220), anchor="mm")

    # Accent border
    draw.rectangle([(W - 4, 0), (W, H)], fill=(cr, cg, cb, 100))

    img = img.filter(ImageFilter.GaussianBlur(radius=1))

    filename = f"{name}_{pose_index + 1}.png"
    img.save(os.path.join(OUTPUT_DIR, filename))
    print(f"  {filename}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating placeholder portraits...")
    for name, colors in CHARACTERS.items():
        for i in range(len(POSES)):
            gen_placeholder(name, i, colors["color"], colors["bg"])
    print(f"\nDone! Portraits saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
