#!/usr/bin/env python3
"""Generate placeholder portrait images for each character (4 poses each).

These are temporary stand-ins until real art is added.
Each portrait is 360x600 with a colored silhouette and pose label.
"""

import os
from PIL import Image, ImageDraw, ImageFilter

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "game", "images", "characters", "portraits")

CHARACTERS = {
    "mallory": {"color": "#daa520", "bg": "#2a2010"},
    "rye":     {"color": "#cc4444", "bg": "#2a1010"},
    "demitria":{"color": "#8844aa", "bg": "#1a1028"},
    "gabby":   {"color": "#44aaaa", "bg": "#102828"},
}

POSES = ["default", "happy", "thinking", "flirty"]

W, H = 360, 600


def gen_placeholder(name, pose_index, color_hex, bg_hex):
    """Generate a placeholder portrait with silhouette shape."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Parse colors
    c = color_hex.lstrip("#")
    cr, cg, cb = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    b = bg_hex.lstrip("#")
    br, bg_r, bb = int(b[0:2], 16), int(b[2:4], 16), int(b[4:6], 16)

    # Background gradient (fades to transparent at top)
    for y in range(H):
        alpha = int(180 * (y / H))
        draw.line([(0, y), (W, y)], fill=(br, bg_r, bb, alpha))

    # Silhouette body (simple shape)
    body_color = (cr, cg, cb, 140)

    # Head
    head_cx, head_cy = W // 2, 120
    head_r = 55
    # Vary head position slightly per pose
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

    # Pose label text at bottom
    pose_name = POSES[pose_index]
    label = f"{name.upper()} — {pose_name}"

    # Draw label background bar
    draw.rectangle([(0, H - 50), (W, H)], fill=(0, 0, 0, 160))

    # Draw text (simple, no custom font needed)
    # Calculate rough center for the label
    text_x = W // 2
    text_y = H - 35
    draw.text((text_x, text_y), label, fill=(255, 255, 255, 220), anchor="mm")

    # Accent border on the right edge
    draw.rectangle([(W - 4, 0), (W, H)], fill=(cr, cg, cb, 100))

    # Apply slight blur for softness
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
